#!/usr/bin/env python3
"""ITER-0120 layout / hook / ledger assertions. Exit 0 only if all hold."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools/butler-upgrade"))
from upgrade import hook_source_files, tree_digest  # noqa: E402

base = json.loads((ROOT / ".ai/iterations/ITER-0120/pre-p4.baseline.json").read_text())
errors: list[str] = []


def check(cond: bool, msg: str) -> None:
    if not cond:
        errors.append(msg)


check(not (ROOT / ".ai/milestone-backlog").exists(), "old backlog dir exists")
check((ROOT / ".ai/backlog").is_dir(), "new backlog missing")
names = sorted(p.name for p in (ROOT / ".ai/backlog").glob("*.md"))
check(names == base["backlog"], f"backlog names {names}")
inbox = (ROOT / ".ai/INBOX.md").read_text(encoding="utf-8")
check(".ai/backlog/delivery-renderer-in-repo.md" in inbox, "inbox pointer")
check(".ai/milestone-backlog" not in inbox, "inbox still old")

check(not (ROOT / "deliveries").exists(), "old deliveries exists")
check(not (ROOT / "deliveries").is_symlink(), "deliveries symlink")
n = sum(1 for p in (ROOT / ".ai/deliveries").rglob("*") if p.is_file())
check(n == 272, f"deliveries count {n}")
check((ROOT / ".ai/deliveries/milestones").is_dir(), "milestones subdir missing")

st = subprocess.check_output(
    ["git", "diff", "--cached", "--name-status"], cwd=ROOT, text=True
)
check(
    "R100\tdeliveries/ITER-0119-retire-old-inbox-chain.md\t.ai/deliveries/ITER-0119-retire-old-inbox-chain.md" in st
    or "R100deliveries/ITER-0119-retire-old-inbox-chain.md.ai/deliveries/ITER-0119-retire-old-inbox-chain.md" in st.replace("\t", ""),
    "git mv not R100 for ITER-0119",
)

digest = tree_digest(hook_source_files(ROOT))
check(digest == base["hook_digest"], f"hook digest {digest}")
check(len(hook_source_files(ROOT)) == 19, "hook file count")

ledger = (ROOT / ".ai/ITERATIONS.md").read_text(encoding="utf-8")
check(".ai/deliveries/ITER-0119-retire-old-inbox-chain.md" in ledger, "hot delivery prefix")
check("| deliveries/" not in ledger, "hot ledger old prefix")
cold = (ROOT / ".ai/history/iterations/ITER-000001-000050.md").read_text(encoding="utf-8")
check(".ai/deliveries/2026-04-20-chat-recap-style.md" in cold, "ITER-0001 dated delivery")
check("| deliveries/" not in cold, "cold shard old prefix")

diff = subprocess.check_output(
    ["git", "diff", "--name-only", "HEAD", "--",
     ".ai/milestones", "migrations", "docs/research", "docs/superpowers"],
    cwd=ROOT, text=True,
)
check(diff.strip() == "", f"archive dirty: {diff}")
# existing iteration archives: only allow untracked ITER-0120
status = subprocess.check_output(
    ["git", "status", "--short", "--", ".ai/iterations"], cwd=ROOT, text=True
)
for line in status.splitlines():
    if not line.strip():
        continue
    path = line[3:]
    if not path.startswith(".ai/iterations/ITER-0120"):
        errors.append(f"unexpected iterations change: {line}")

if errors:
    print("FAIL")
    for item in errors:
        print(item)
    raise SystemExit(1)
print("OK layout hook ledger archive")
print(f"hook_digest={digest}")
print(f"backlog={len(names)} deliveries={n}")
raise SystemExit(0)
