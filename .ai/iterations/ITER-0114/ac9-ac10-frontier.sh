#!/usr/bin/env bash
# ITER-0114 · AC9 / AC10：frontier.md 退役逐条留痕，debt.md 只追加。
set -uo pipefail
cd "$(dirname "$0")/../../.."
fail=0
ok()  { echo "[OK]   $*"; }
bad() { echo "[FAIL] $*"; fail=1; }

echo "=== AC9 · 两者都不存在 ==="
[ -e .ai/project/frontier.md ] && bad ".ai/project/frontier.md 仍在" || ok ".ai/project/frontier.md 不存在"
[ -e .ai/project ] && bad ".ai/project/ 目录仍在" || ok ".ai/project/ 目录不存在"
if git ls-files --error-unmatch .ai/project/frontier.md >/dev/null 2>&1; then
  bad "git 索引里还留着 .ai/project/frontier.md"
else
  ok "git 索引里也已移除"
fi

echo "=== AC9 · 退役前三节各有多少条（以 HEAD 原文实测） ==="
old=$(git show HEAD:.ai/project/frontier.md)
count_section() {
  printf '%s\n' "${old}" | awk -v want="$1" '
    /^## /   { sec = substr($0, 4) }
    /^- /    { if (sec == want) n++ }
    END      { print n + 0 }'
}
c1=$(count_section "当前形态"); c2=$(count_section "活跃战线"); c3=$(count_section "下一个瓶颈")
total=$((c1 + c2 + c3))
echo "       当前形态 ${c1} 条 / 活跃战线 ${c2} 条 / 下一个瓶颈 ${c3} 条 = 共 ${total} 条"
if [ "$total" = 28 ]; then ok "原文实测 28 条"; else bad "原文实测 ${total} 条，与留痕声称的 28 不符"; fi

echo "=== AC9 · 变更流的逐节处置段 ==="
del=$(awk '/^## DELETE/,0' .ai/01_CHANGELOG.md)
say() {
  if printf '%s\n' "${del}" | grep -q -- "$1"; then ok "$2"; else bad "$2（缺）"; fi
}
say "当前形态 ${c1} 条" "DELETE 段声明当前形态 ${c1} 条，与原文实测对得上"
say "活跃战线 ${c2} 条" "DELETE 段声明活跃战线 ${c2} 条，与原文实测对得上"
say "下一个瓶颈 ${c3} 条" "DELETE 段声明下一个瓶颈 ${c3} 条，与原文实测对得上"
say "三节 28 条逐条处置" "DELETE 段声明逐条处置、无一条无交代"
for word in "并入" "迁入 \`.ai/debt.md\`" "可弃"; do
  if printf '%s\n' "${del}" | grep -q -- "$word"; then
    n=$(printf '%s\n' "${del}" | grep -o -- "$word" | wc -l | tr -d ' ')
    ok "三类去向之一「${word}」出现 ${n} 处"
  else
    bad "三类去向缺「${word}」"
  fi
done
if printf '%s\n' "${del}" | grep -q 'AC9'; then ok "处置段绑定 AC9"; else bad "处置段没绑 AC9"; fi

echo "=== AC10 · debt.md 只有追加 ==="
removed=$(git diff -U0 -- .ai/debt.md | grep -c '^-[^-]')
added=$(git diff -U0 -- .ai/debt.md | grep -c '^+[^+]')
if [ "$removed" = 0 ]; then
  ok "既有条目零改动（删除行 0，新增行 ${added}）"
else
  bad "改到了既有条目：删除行 ${removed}"
fi
before=$(git show HEAD:.ai/debt.md | grep -c '^- \*\*')
after=$(grep -c '^- \*\*' .ai/debt.md)
if [ "$after" = $((before + 6)) ]; then
  ok "条目数 ${before} → ${after}（追加 6 条）"
else
  bad "条目数 ${before} → ${after}，与预期追加 6 条不符"
fi

echo "=== AC10 · 迁入项写明来源与迁入日期 ==="
migrated=$(grep -c '2026-08-20（ITER-0114）从已删除的 `.ai/project/frontier.md`' .ai/debt.md)
if [ "$migrated" = 4 ]; then
  ok "4 条迁入项都写了来源 frontier.md + 迁入日期 2026-08-20"
else
  bad "带来源与日期的迁入项只有 ${migrated} 条"
fi
for key in "运行时观测缺位" "远端 required check 未启用" "双宿主语义入口未经真实安装人测" "危险模式规则真源"; do
  if grep -q "$key" .ai/debt.md; then ok "迁入项在场：${key}"; else bad "迁入项缺失：${key}"; fi
done

echo "=== AC10 · 本轮新记的两条不冒充迁入项 ==="
for key in "有 16 条不带真源指针" "的修订记录要求与产物合同冲突"; do
  line=$(grep -n "$key" .ai/debt.md | head -1)
  if [ -z "$line" ]; then
    bad "新记条目缺失：${key}"
  elif printf '%s\n' "${line}" | grep -q 'frontier.md'; then
    bad "新记条目被写成了从 frontier.md 迁入：${key}"
  else
    ok "新记条目在场且未冒充迁入：${key}"
  fi
done

echo
[ "$fail" = 0 ] && echo "FRONTIER-CLEAN" || echo "FRONTIER-DIRTY"
exit "$fail"
