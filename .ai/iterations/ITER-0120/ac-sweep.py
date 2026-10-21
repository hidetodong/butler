#!/usr/bin/env python3
"""ITER-0120 AC12 可重跑扫描。模式串拼接，避免脚本自命中。"""
from pathlib import Path
import sys

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()

OLD_DIR = "milestone" + "-backlog"
OLD_ROOT = "deliveries/"
NEW_BACKLOG = ".ai/backlog"
NEW_DELIVERIES = ".ai/deliveries"

SKIP_PREFIXES = (
    ".git/",
    "__pycache__/",
    ".ai/iterations/",
    ".ai/milestones/",
    ".ai/deliveries/",
    ".ai/history/",
    "migrations/",
    "docs/research/",
    "docs/superpowers/",
    "templates/hooks/lib/",
    "templates/hooks/rules/",
    "templates/hooks/README.md",
    "templates/hooks/butler_gate.py",
    "templates/hooks/butler_advisor.py",
    "templates/hooks/tests/test_io.py",
    ".ai/CONCEPT.md",
    ".ai/AC_LIST.md",
    ".ai/TECH_PLAN.md",
    ".ai/VERIFY_REPORT.md",
    ".ai/01_CHANGELOG.md",
    ".ai/02_SESSION_HANDOFF.md",
    ".ai/task-state.md",
    ".ai/MILESTONE.md",
    ".ai/handoff-state.json",
    ".ai/RUN_LOG.md",
    ".claude/settings.local.json",
)

HISTORICAL_SLUG = "ITER-0068-" + OLD_DIR + "-numbering"


def skipped(rel: str) -> bool:
    return any(rel == prefix.rstrip("/") or rel.startswith(prefix) for prefix in SKIP_PREFIXES)


def iter_files():
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in {".git", "__pycache__", "node_modules"} for part in path.parts):
            continue
        rel = path.relative_to(ROOT).as_posix()
        if skipped(rel):
            continue
        yield path, rel


def group_a() -> list[str]:
    hits = []
    for path, rel in iter_files():
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            if HISTORICAL_SLUG in line:
                line = line.replace(HISTORICAL_SLUG, "")
            stripped = line.replace(NEW_DELIVERIES + "/", "")
            if OLD_DIR in stripped:
                hits.append(f"{rel}:{lineno}: {OLD_DIR}")
            elif OLD_ROOT in stripped and NEW_DELIVERIES not in line:
                # .ai/ 树里的子目录名 deliveries/ 允许
                if rel in {"HUMAN_GUIDE.md", "README.md"} and "└── deliveries/" in line:
                    continue
                if rel == "Coder/20_Workflow_Lifecycle/mcv-deployment.md" and (
                    line.lstrip().startswith("- `deliveries/`") or "`.ai/` 下的" in line
                ):
                    continue
                hits.append(f"{rel}:{lineno}: {OLD_ROOT}")
    return hits


def group_b() -> list[str]:
    missing = []
    backlog = ROOT / ".ai" / "backlog"
    if not backlog.is_dir():
        missing.append("backlog dir missing")
        return missing
    names = sorted(p.name for p in backlog.glob("*.md"))
    if len(names) != 10:
        missing.append(f"backlog count {len(names)} != 10")
    intake = (ROOT / "tools/intake/intake.py").read_text(encoding="utf-8")
    if 'BACKLOG_REL = ".ai/backlog"' not in intake:
        missing.append("intake BACKLOG_REL")
    audit = (ROOT / "scripts/audit-project-state.py").read_text(encoding="utf-8")
    if '".ai" / "backlog"' not in audit and '/ "backlog"' not in audit:
        missing.append("audit backlog root")
    iterations = (ROOT / ".ai/ITERATIONS.md").read_text(encoding="utf-8")
    if NEW_DELIVERIES + "/ITER-0119" not in iterations:
        missing.append("hot ledger delivery prefix")
    summary = (ROOT / "Coder/20_Workflow_Lifecycle/delivery-summary.md").read_text(encoding="utf-8")
    if "存放位置：`.ai/deliveries/`" not in summary and "`.ai/deliveries/`" not in summary.split("存放位置", 1)[-1][:80]:
        missing.append("delivery-summary location")
    deploy = (ROOT / "Coder/20_Workflow_Lifecycle/mcv-deployment.md").read_text(encoding="utf-8")
    if "强制创建 `.ai/` 这一个基础目录" not in deploy:
        missing.append("deploy only .ai")
    order = (ROOT / "Coder/40_Context_Management/context-persistence.md").read_text(encoding="utf-8")
    if "或 `.ai/deliveries/` 历史归档" not in order:
        missing.append("cold-start order new path")
    return missing


def main() -> int:
    a = group_a()
    b = group_b()
    print(f"A_hits={len(a)}")
    for hit in a:
        print("A", hit)
    print(f"B_missing={len(b)}")
    for item in b:
        print("B", item)
    return 0 if not a and not b else 1


if __name__ == "__main__":
    raise SystemExit(main())
