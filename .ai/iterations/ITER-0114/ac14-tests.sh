#!/usr/bin/env bash
# ITER-0114 · AC14：新增夹具覆盖八类负例，每条断言具体诊断串而不是只断言非零退出。
set -uo pipefail
cd "$(dirname "$0")/../../.."
fail=0
ok()  { echo "[OK]   $*"; }
bad() { echo "[FAIL] $*"; fail=1; }

T=scripts/test-sync-project-overview.py

echo "=== AC14 · 用例跑通 ==="
if python3 "$T" > /tmp/iter0114-tests.log 2>&1; then
  ran=$(grep -oE 'Ran [0-9]+ tests?' /tmp/iter0114-tests.log | head -1)
  ok "${T} 全过（${ran}）"
else
  bad "${T} 失败："; tail -25 /tmp/iter0114-tests.log | sed 's/^/       /'
fi

echo "=== AC14 · 负例场景计数 ==="
methods=$(grep -c '^    def test_' "$T")
subcases=$(awk '/def test_missing_sources_are_named/,/def test_missing_tools_directory_is_named/' "$T" | grep -c '^            ("')
neg=$(grep -c '^    def test_missing_\|^    def test_check_names\|^    def test_check_reports\|^    def test_size_ceiling\|^    def test_invariant_pointer\|^    def test_directory_without' "$T")
scenarios=$((neg - 1 + subcases))
echo "       测试方法 ${methods} 个（其中负例方法 ${neg} 个），五源缺失展开 ${subcases} 个子例"
echo "       负例场景合计 ${scenarios} 个"
if [ "$scenarios" -ge 8 ]; then
  ok "负例场景 ${scenarios} ≥ AC14 要求的 8 条"
else
  bad "负例场景只有 ${scenarios} 条，不足 8"
fi
if [ "$subcases" = 5 ]; then ok "五个源头各自缺失都有子例"; else bad "源头缺失子例是 ${subcases} 个，不是 5 个"; fi

echo "=== AC14 · AC 点名的七类各有对应用例 ==="
one() { grep -q "def $1" "$T" && ok "$2 → ${1}()" || bad "$2（缺 ${1}）"; }
one test_missing_sources_are_named          "五个源头各自缺失时报错指名"
one test_missing_tools_directory_is_named   "tools/ 整个不在"
one test_check_names_the_drifting_section   "手改任一节被 --check 抓到并指名"
one test_check_reports_section_set_mismatch "节标题被改 → 节集不匹配"
one test_size_ceiling_is_enforced           "体量超限"
one test_invariant_pointer_ratchet_blocks_new_entries "无指针条目数超基线"
one test_directory_without_description_is_rejected    "目录在 Coder/README.md 无说明"

echo "=== AC14 · 正例三条 ==="
for name in test_write_then_check_is_clean test_write_is_idempotent test_check_and_write_are_mutually_exclusive; do
  grep -q "def ${name}" "$T" && ok "正例：${name}" || bad "正例缺失：${name}"
done

echo "=== AC14 · 每条负例断言的是具体诊断串，不是只看退出码 ==="
python3 - <<'PY'
import pathlib, re, sys
text = pathlib.Path("scripts/test-sync-project-overview.py").read_text(encoding="utf-8")
needles = [
    "missing source: {needle}",
    "missing source: tools/",
    "overview section drift: {overview.SECTION_TOOLS}",
    "overview section set mismatch",
    "overview too large:",
    "invariants without source pointer:",
    "directory has no description in Coder/README.md:",
]
bad = 0
for needle in needles:
    if needle in text:
        print(f"[OK]   诊断串被断言：{needle}")
    else:
        print(f"[FAIL] 没有用例断言诊断串：{needle}")
        bad = 1
# 每个负例方法体内至少有一句 assertIn（断言诊断内容），不能只有 assertEqual(1, code)
bodies = re.split(r"\n    def ", text)
for body in bodies:
    name = body.split("(", 1)[0]
    if not name.startswith("test_") or "stderr_of" not in body:
        continue
    if "assertIn(" in body:
        print(f"[OK]   {name}() 断言了诊断内容")
    else:
        print(f"[FAIL] {name}() 只断言了退出码")
        bad = 1
# 反证：诊断断言不是空转——把断言串改一个字应当匹配不上
assert "assertIn(\"overview section set mismatch\", err)" in text
print("[OK]   反证：断言用的是 assertIn 精确串，改一个字即失配")
sys.exit(bad)
PY
[ $? = 0 ] || bad "有负例只断言退出码"

echo
[ "$fail" = 0 ] && echo "TESTS-CLEAN" || echo "TESTS-DIRTY"
exit "$fail"
