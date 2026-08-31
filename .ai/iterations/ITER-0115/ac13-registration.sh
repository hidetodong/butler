#!/usr/bin/env bash
# ITER-0115 · AC13：MILESTONE.md §5.4 两条登记在场且写到位。
# 说明：同样的断言也在 ac13-ac14-ci-audit.sh 里跑过，但那条记录捕获时 --ac 传错、
# 机器绑定只留下了 AC14。此脚本给 AC13 单独留一条绑定正确的记录，不是重复验证。
set -uo pipefail
cd "$(dirname "$0")/../../.."
fail=0
ok()  { echo "[OK]   $*"; }
bad() { echo "[FAIL] $*"; fail=1; }
M=.ai/MILESTONE.md
need() { grep -qF -- "$1" "$M" && ok "$2" || bad "$2（缺）"; }

echo "=== 登记一 · 路线图点名两项在 progress 上不存在 ==="
need 'R4 · 路线图点名两项不存在' "标题行在场"
need 'rule_source'               "写明 registry 的 rule_source 指回命令文件自身"
need 'templates/rule-card.md'    "写明 rule-card 全文未提 progress"
need '如实记为不适用'            "表态：不适用，不假装完成"

echo "=== 登记二 · 发布处置 ==="
need 'R4 · 发布处置登记'   "标题行在场"
need '软链'                "写明 Claude 侧是软链、删即生效"
need '[global-install]'    "写明 Codex 侧需要 [global-install]"
need '[regen-entrypoints]' "写明本轮不触发 [regen-entrypoints]"
need 'R15'                 "写明归 R15"

echo "       —— §5.4 末两条原文 ——"
awk '/^## 5\.4 /{flag=1} flag' "$M" | grep -n 'R4 · ' | cut -c1-160 | sed 's/^/       /'

echo
[ "$fail" = 0 ] && echo "REGISTRATION-CLEAN" || echo "REGISTRATION-DIRTY"
exit "$fail"
