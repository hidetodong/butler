#!/usr/bin/env python3
"""Claude Code PreToolUse dispatcher for butler harness gating.

Invoked by Claude Code with tool-call JSON on stdin. Exit code semantics:
  0  = allow
  2  = deny (either a rule said deny with no valid bypass, or internal crash)

Rule modules are evaluated in registered order; the first deny wins.
Hook itself is fail-closed on any uncaught exception.
"""
from __future__ import annotations

import sys
import traceback
from pathlib import Path

# Make absolute imports work when invoked as a script.
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from lib.bypass import evaluate_bypass
from lib.io import Context, Decision, parse_stdin, resolve_target
from rules import artifact_chain, ledger_status, phase_gate, protected_paths

GATED_TOOLS = frozenset({"Edit", "Write", "MultiEdit"})

# Registered in evaluation order. First deny wins; more specific rules first.
RULE_MODULES = [protected_paths, phase_gate, ledger_status, artifact_chain]


def main() -> int:
    try:
        payload = parse_stdin()
        tool_name = payload.get("tool_name", "")
        if tool_name not in GATED_TOOLS:
            return 0

        cwd = payload.get("cwd", ".")
        tool_input = payload.get("tool_input", {})
        target = resolve_target(tool_input, cwd)

        ctx = Context(
            cwd=cwd,
            tool_name=tool_name,
            target_path=target,
            tool_input=tool_input,
        )

        for mod in RULE_MODULES:
            decision = mod.evaluate(ctx)
            if decision.verdict == "deny":
                final = evaluate_bypass(ctx, decision)
                if final.verdict == "allow":
                    return 0
                _print_denial(ctx, final)
                return 2
        return 0
    except Exception:
        print("❌ butler-gate internal error:", file=sys.stderr)
        traceback.print_exc(limit=3, file=sys.stderr)
        print(
            "  bypass: 若要继续，设 BUTLER_BYPASS=1 并在 .ai/bypass-reason.md 写明理由",
            file=sys.stderr,
        )
        return 2


def _print_denial(ctx: Context, decision: Decision) -> None:
    print(f"❌ butler-gate denied: {decision.rule_id}", file=sys.stderr)
    print(f"  tool: {ctx.tool_name}", file=sys.stderr)
    print(f"  target: {ctx.target_path.as_posix()}", file=sys.stderr)
    print(f"  reason: {decision.reason}", file=sys.stderr)
    if decision.remediation:
        print(f"  remediation: {decision.remediation}", file=sys.stderr)
    print(
        "  bypass: 若坚持绕过，设 BUTLER_BYPASS=1 并在 .ai/bypass-reason.md 写明理由",
        file=sys.stderr,
    )


if __name__ == "__main__":
    sys.exit(main())
