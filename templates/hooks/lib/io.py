"""Types, constants, and stdin/path helpers for butler_gate."""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Literal

GATED_BLACKLIST = frozenset({
    ".ai/",
    "deliveries/",
    ".claude/",
    ".git/",
    "node_modules/",
    ".vscode/",
    ".idea/",
})

OUT_OF_CWD = PurePosixPath("__OUT_OF_CWD__")


@dataclass(frozen=True)
class Context:
    cwd: str
    tool_name: str
    target_path: PurePosixPath
    tool_input: dict = field(default_factory=dict)


@dataclass(frozen=True)
class Decision:
    verdict: Literal["allow", "deny"]
    rule_id: str
    reason: str = ""
    remediation: str = ""


@dataclass(frozen=True)
class Advisory:
    """PostToolUse advisory：放行 + 可选向模型注入的提醒。

    与 Decision（PreToolUse 的 allow/deny 门禁）刻意分开——advisory 只在工具
    执行之后跑，没有 verdict、不能 deny、不改工具结果。message 为空即静默不注入。
    """
    rule_id: str
    message: str = ""


def parse_stdin() -> dict:
    """Reads Claude Code PreToolUse JSON from stdin."""
    return json.loads(sys.stdin.read())


def resolve_target(tool_input: dict, cwd: str) -> PurePosixPath:
    """Normalize file_path into a path relative to cwd.

    Returns OUT_OF_CWD sentinel for missing, empty, or escaped paths.
    """
    raw = tool_input.get("file_path", "")
    if not raw:
        return OUT_OF_CWD

    p = Path(raw).expanduser()
    cwd_resolved = Path(cwd).resolve()

    if p.is_absolute():
        try:
            rel = p.resolve().relative_to(cwd_resolved)
        except ValueError:
            return OUT_OF_CWD
        return PurePosixPath(rel.as_posix())

    # Relative path: resolve against cwd, check it stays inside.
    try:
        resolved = (cwd_resolved / p).resolve()
        rel = resolved.relative_to(cwd_resolved)
    except ValueError:
        return OUT_OF_CWD
    return PurePosixPath(rel.as_posix())


def is_gated(target: PurePosixPath, blacklist: frozenset = GATED_BLACKLIST) -> bool:
    """True when the target path is subject to gating (i.e. NOT in the exempt blacklist)."""
    if target == OUT_OF_CWD:
        return True
    target_str = target.as_posix()
    for prefix in blacklist:
        p = prefix.rstrip("/")
        if target_str == p or target_str.startswith(p + "/"):
            return False
    return True
