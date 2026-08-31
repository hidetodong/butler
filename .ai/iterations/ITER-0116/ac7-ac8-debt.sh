#!/usr/bin/env bash
# AC7 / AC8 · debt 一删一增，净额仍 10，删的加的各是哪条
set -euo pipefail
cd "$(dirname "$0")/../../.."

echo "== 条目数（AC7 先减为 9、AC8 再补回 10；收口态应为 10） =="
n=$(grep -c '^- \*\*' .ai/debt.md); echo "count=${n}"; [ "$n" -eq 10 ] || { echo "FAIL"; exit 1; }

echo
echo "== AC7 · 已还清的旧账已删（关键字应零命中） =="
k=$(grep -c '自动绑定' .ai/debt.md || true); echo "'自动绑定' count=${k}"; [ "$k" -eq 0 ] || { echo "FAIL"; exit 1; }

echo
echo "== AC8 · 新欠账在场且三要素齐备 =="
grep -n '演进冻结没有机器兜底' .ai/debt.md | awk '{print substr($0,1,100)}'
for s in '没有任何检查能拦住' '本轮有意不加检查' 'R13 对 loop 做最终处置'; do
  grep -qF -- "$s" .ai/debt.md && echo "OK   含 '${s}'" || { echo "FAIL 缺 '${s}'"; exit 1; }
done

echo
echo "== 其余 9 条首句逐条仍在 =="
for s in 'butler 仓自身不 dogfood 运行自己的 hook' \
         '项目自有 hook 与 Butler 受管目录不能共存' \
         '`/butler:upgrade` 从未在真实已部署项目上跑过' \
         '运行时观测缺位' \
         '远端 required check 未启用' \
         '双宿主语义入口未经真实安装人测' \
         '`.ai/invariants.md` 有 16 条不带真源指针' \
         '`iteration-schema.md §5.3` 的修订记录要求与产物合同冲突' \
         '人读文档里的工作流计数没有机器兜底'; do
  grep -qF -- "- **${s}" .ai/debt.md && echo "OK   ${s}" || { echo "FAIL 丢了: ${s}"; exit 1; }
done

echo
echo "== 改动范围 =="
git diff --numstat -- .ai/debt.md
echo "AC7-AC8-OK"
