#!/usr/bin/env python3
"""Resolve the one project root Butler may read from or write to."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

HOOKS_ROOT = Path(__file__).resolve().parent.parent / "templates" / "hooks"
if str(HOOKS_ROOT) not in sys.path:
    sys.path.insert(0, str(HOOKS_ROOT))

from lib.project_root import RootResolutionError, resolve_project_root


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--user-target",
        type=Path,
        help="Project path explicitly named or confirmed by the user",
    )
    parser.add_argument(
        "--start",
        type=Path,
        default=Path.cwd(),
        help="Session start/cwd used only for safe discovery",
    )
    args = parser.parse_args()
    try:
        resolution = resolve_project_root(user_target=args.user_target, start=args.start)
    except RootResolutionError as error:
        print(f"resolve-project-root: {error}", file=sys.stderr)
        return 2
    print(
        f"[butler] project root ({resolution.evidence}): {resolution.root}",
        file=sys.stderr,
    )
    print(resolution.root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
