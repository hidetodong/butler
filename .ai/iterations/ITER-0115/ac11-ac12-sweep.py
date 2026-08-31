#!/usr/bin/env python3
"""ITER-0115 AC11/AC12 sweep — prove the /butler:progress chain leaves no live reference.

Two pattern groups are checked over the same exclusion surface:
  A. live references to the retired command, skill, entry or rule source
  B. prose workflow counts that the deletion made false

Patterns are assembled from fragments so this script never matches itself.
Exit code 0 when both groups are empty; 1 otherwise, listing file and line.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SELF = Path(__file__).resolve()

P = "pro" + "gress"
GROUPS = {
    "A · retired chain (live refs)": [
        "/butler:" + P,
        "$butler-" + P,
        "butler-" + P,
        "commands/butler/" + P,
    ],
    "B · stale prose counts": [
        "Router + 13",
        "13 " + "个业务",
        "13 workflow skills",
        "其余" + "十一项",
    ],
}

# Excluded because they are records of past or current work, not live wiring.
EXCLUDED_DIRS = {
    ".git", ".venv", ".pytest_cache", "node_modules",
    ".ai/iterations", ".ai/history", ".ai/.artifact-migration-backups",
    ".ai/verification-evidence",  # captured output of this very sweep, not live wiring
    "deliveries", "migrations",
}
EXCLUDED_FILES = {
    # this iteration's own workspace artifacts and state files
    ".ai/CONCEPT.md", ".ai/AC_LIST.md", ".ai/TECH_PLAN.md", ".ai/VERIFY_REPORT.md",
    ".ai/01_CHANGELOG.md", ".ai/task-state.md", ".ai/02_SESSION_HANDOFF.md",
    ".ai/handoff-state.json", ".ai/ITERATIONS.md", ".ai/MILESTONE.md",
    ".ai/RUN_LOG.md", ".ai/00_IDEATION.md", ".ai/00_IDEATION.html",
}


def excluded(path: Path) -> bool:
    if path == SELF:
        return True
    rel = path.relative_to(ROOT).as_posix()
    if rel in EXCLUDED_FILES:
        return True
    return any(rel == d or rel.startswith(d + "/") for d in EXCLUDED_DIRS)


def main() -> int:
    hits: dict[str, list[str]] = {name: [] for name in GROUPS}
    scanned = 0
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.is_symlink() or excluded(path):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        scanned += 1
        rel = path.relative_to(ROOT).as_posix()
        for number, line in enumerate(text.splitlines(), start=1):
            for name, patterns in GROUPS.items():
                for pattern in patterns:
                    if pattern in line:
                        hits[name].append(f"{rel}:{number}: {line.strip()[:160]}")

    print(f"scanned {scanned} text files under {ROOT}")
    failed = False
    for name, patterns in GROUPS.items():
        found = hits[name]
        print(f"\n[{name}] patterns={len(patterns)} hits={len(found)}")
        for item in found:
            print(f"  {item}")
        if found:
            failed = True
    print("\nRESULT:", "FAIL" if failed else "PASS")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
