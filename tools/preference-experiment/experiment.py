#!/usr/bin/env python3
"""Read-only check: does this repo reorder options after reading a preference profile?"""

from __future__ import annotations

import argparse
import ast
import json
import sys
from pathlib import Path

RANKER_NAMES = {"reorder_options", "reorder_by_profile"}
TRIGGER_TEXT = "反哺开、有监督、只参考通识层、排序变化"


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def fixture_path() -> Path:
    return Path(__file__).resolve().parent / "fixtures" / "case.json"


def load_fixture() -> dict:
    return json.loads(fixture_path().read_text(encoding="utf-8"))


def _skipped(relative: Path) -> bool:
    if relative.name.startswith("test_"):
        return True
    if "tools/preference-experiment" in relative.as_posix():
        return True
    return "tests" in relative.parts


def discover_rankers(root: Path) -> list[str]:
    found: list[str] = []
    for path in sorted(root.rglob("*.py")):
        relative = path.relative_to(root)
        if _skipped(relative):
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(relative))
        except (OSError, SyntaxError, UnicodeError):
            continue
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name in RANKER_NAMES:
                found.append(f"{relative.as_posix()}:{node.name}")
    return found


def evaluate(root: Path) -> dict:
    fixture = load_fixture()
    options = list(fixture["options"])
    rankers = discover_rankers(root)
    if rankers:
        raise RuntimeError("ranker present: " + ", ".join(rankers))
    return {
        "order_off": options,
        "order_on": list(options),
        "ranking_changed": False,
    }


def disposition(result: dict) -> dict:
    changed = result["ranking_changed"]
    if changed is True:
        return {"action": "keep", "required_text": TRIGGER_TEXT}
    if changed is False:
        return {"action": "retire"}
    raise ValueError("ranking_changed must be a boolean")


def dumps(result: dict) -> str:
    return json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=repo_root())
    args = parser.parse_args(argv)
    root = args.project_root.expanduser().resolve()
    try:
        import importlib.util

        usage_path = Path(__file__).resolve().parents[1] / "usage" / "usage.py"
        spec = importlib.util.spec_from_file_location("_butler_usage", usage_path)
        if spec is not None and spec.loader is not None:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            module.stamp_tool(__file__, argv)
    except Exception:
        pass
    try:
        sys.stdout.write(dumps(evaluate(root)))
    except RuntimeError as error:
        print(f"preference-experiment: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
