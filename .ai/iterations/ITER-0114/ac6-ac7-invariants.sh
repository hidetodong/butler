#!/usr/bin/env bash
# ITER-0114 · AC6 / AC7：invariants 迁位是搬家不是重写，两条已假的条目按新纪律改对。
set -uo pipefail
cd "$(dirname "$0")/../../.."
fail=0
ok()  { echo "[OK]   $*"; }
bad() { echo "[FAIL] $*"; fail=1; }

echo "=== AC6 · 位置 ==="
[ -f .ai/invariants.md ] && ok ".ai/invariants.md 在位" || bad ".ai/invariants.md 不存在"
[ -e .ai/project/invariants.md ] && bad ".ai/project/invariants.md 仍在" || ok ".ai/project/invariants.md 已不存在"

echo "=== AC6 · 条目数 47 不变 ==="
before=$(git show HEAD:.ai/project/invariants.md | grep -c '^- \*\*')
after=$(grep -c '^- \*\*' .ai/invariants.md)
if [ "$before" = 47 ] && [ "$after" = 47 ]; then
  ok "迁移前 $before 条 / 迁移后 $after 条"
else
  bad "条目数变了：迁移前 $before / 迁移后 $after"
fi

echo "=== AC6 · git 认得出是迁位（R100 全等重命名） ==="
renamed=$(git diff --cached -M --name-status -- .ai/invariants.md .ai/project/invariants.md | head -1)
if [ -z "$renamed" ]; then renamed="(空)"; fi
case "$renamed" in
  R100*".ai/project/invariants.md"*".ai/invariants.md")
    ok "暂存区记为 R100 重命名：${renamed}（提交后 git log --follow 即可穿透）" ;;
  *) bad "暂存区没记成全等重命名：$renamed" ;;
esac

echo "=== AC6 · 迁位之外只动了这两条 + 文件头纪律 ==="
touched=$(git diff -- .ai/invariants.md | grep -c '^[+-][^+-]')
entry_diff=$(git diff -- .ai/invariants.md | grep -c '^[+-]- \*\*')
if [ "$entry_diff" = 4 ]; then
  ok "正文条目只动 4 行（两条各一删一增），另有文件头新增；改动行合计 $touched"
else
  bad "条目级改动行数不是 4：${entry_diff}（改动行合计 ${touched}）"
fi

echo "=== AC7 · 收口仪式那条 ==="
close_line=$(grep -n '^- \*\*收口是原子仪式\*\*' .ai/invariants.md | cut -d: -f1)
if [ -n "$close_line" ]; then
  body=$(sed -n "${close_line}p" .ai/invariants.md)
  case "$body" in
    *'iteration-schema.md §5.5'*) ok "指向真源 iteration-schema.md §5.5" ;;
    *) bad "没指向 §5.5" ;;
  esac
  case "$body" in
    *'fold receipt'*) bad "仍出现 fold receipt" ;;
    *) ok "不再出现 fold receipt" ;;
  esac
  case "$body" in
    *'五步'*) bad "仍写着五步" ;;
    *) ok "不再写步数" ;;
  esac
  case "$body" in
    *'*为什么*'*) ok "保留了「为什么」半句" ;;
    *) bad "丢了「为什么」" ;;
  esac
else
  bad "找不到「收口是原子仪式」条目"
fi

echo "=== AC7 · 冷启动读序那条 ==="
order_line=$(grep -n '^- \*\*冷启动读序固定且只有一处真源\*\*' .ai/invariants.md | cut -d: -f1)
if [ -n "$order_line" ]; then
  body=$(sed -n "${order_line}p" .ai/invariants.md)
  case "$body" in
    *'context-persistence.md §6'*) ok "指向真源 context-persistence.md §6" ;;
    *) bad "没指向 §6" ;;
  esac
  case "$body" in
    *'四步'*) bad "仍写着旧四步措辞" ;;
    *) ok "不再出现旧四步措辞" ;;
  esac
  case "$body" in
    *'*为什么*'*) ok "保留了「为什么」半句" ;;
    *) bad "丢了「为什么」" ;;
  esac
else
  bad "找不到「冷启动读序固定且只有一处真源」条目"
fi

echo "=== AC7 · 全文不再复述这两套步骤清单 ==="
if grep -n '^- \*\*' .ai/invariants.md | grep -q 'fold receipt'; then
  bad "仍有条目复述 fold receipt"
else
  ok "全文条目零 fold receipt"
fi

echo "=== AC7 · 真源自身确实是四步、第四步是自检（指针指得对） ==="
sec=$(awk '/^### 5\.5 /,/^### 5\.6 /' Coder/20_Workflow_Lifecycle/iteration-schema.md)
steps=$(printf '%s\n' "$sec" | grep -c '^  [0-9]\. ')
if [ "$steps" = 4 ]; then ok "§5.5 实测 4 步"; else bad "§5.5 实测 $steps 步"; fi
if printf '%s\n' "$sec" | grep -q '^  4\. \*\*收口自检\*\*'; then
  ok "§5.5 第四步是收口自检"
else
  bad "§5.5 第四步不是收口自检"
fi

echo
[ "$fail" = 0 ] && echo "INVARIANTS-CLEAN" || echo "INVARIANTS-DIRTY"
exit "$fail"
