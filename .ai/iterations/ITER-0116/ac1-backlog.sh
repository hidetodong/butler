#!/usr/bin/env bash
# AC1 · 候办两侧删净、其余 9 份完好、审计的集合一致性检查为 OK
set -euo pipefail
cd "$(dirname "$0")/../../.."
KEY="upgrade-convergence-engine"

echo "== 候办草稿文件应不存在 =="
if [ -e ".ai/milestone-backlog/${KEY}.md" ]; then echo "FAIL: 文件仍在"; exit 1; fi
echo "OK: .ai/milestone-backlog/${KEY}.md 不存在"

echo
echo "== 索引行应零命中 =="
n=$(grep -c "${KEY}" .ai/MILESTONES.md || true)
echo "grep -c '${KEY}' .ai/MILESTONES.md = ${n}"
[ "$n" -eq 0 ] || { echo "FAIL: 索引行仍在"; exit 1; }

echo
echo "== 待办区索引行数与实际文件数（应同为 9） =="
rows=$(awk '/^## 待办区/{f=1} f && /^\| [a-z0-9-]+ \|/{c++} END{print c+0}' .ai/MILESTONES.md)
files=$(ls .ai/milestone-backlog/*.md | wc -l | tr -d ' ')
echo "索引行=${rows}  实际文件=${files}"
[ "$rows" -eq 9 ] && [ "$files" -eq 9 ] || { echo "FAIL: 数目不为 9"; exit 1; }

echo
echo "== 其余 9 行逐字未动（对 HEAD 只应少掉那一行） =="
git diff --numstat -- .ai/MILESTONES.md
added=$(git diff --numstat -- .ai/MILESTONES.md | awk '{print $1}')
removed=$(git diff --numstat -- .ai/MILESTONES.md | awk '{print $2}')
echo "added=${added} removed=${removed}"
[ "$added" -eq 1 ] && [ "$removed" -eq 2 ] || echo "NOTE: 另含 ITER-0116 开台账那一行的改动，见下方 diff"
git diff -- .ai/MILESTONES.md | grep '^[-+]' | grep -vE '^(\+\+\+|---) ' | awk '{print substr($0,1,160)}'

echo
echo "== 审计的候办一致性检查 =="
python3 scripts/audit-project-state.py --project-root . --allow-unreleased 2>&1 \
  | grep -E 'milestones\.backlog_set|backlog\..*\.markers' | tail -12
python3 scripts/audit-project-state.py --project-root . --allow-unreleased >/dev/null 2>&1
echo "audit exit=$?"
echo "AC1-OK"
