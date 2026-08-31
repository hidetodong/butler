#!/usr/bin/env bash
# AC3 / AC5 · 冻结声明三要素 + 激活清单降为 2 条 + 两处镜像清除 + 正文其余未改
set -euo pipefail
cd "$(dirname "$0")/../../.."
E=Coder/55_Extension_ConvergenceLoop/convergence-loop-engine.md
L=Coder/00_System_Prompt/logic-protocol.md

echo "===== AC3 · 冻结声明 ====="
echo "-- 声明块落在 H1 之后、'## 1. 身份' 之前 --"
awk '/^# Butler 收敛闭环引擎/{f=1} /^## 1\. 身份/{f=0} f' "$E"

echo
echo "-- 三要素断言 --"
HEAD_PART=$(awk '/^# Butler 收敛闭环引擎/{f=1} /^## 1\. 身份/{exit} f' "$E")
need() { printf '%s\n' "$HEAD_PART" | grep -qF -- "$2" && echo "OK   $1" || { echo "FAIL $1 — 缺 '$2'"; exit 1; }; }
need "冻结含义·保留行为"   "原样保留并照常生效"
need "冻结含义·停的是演进" "冻结的是**演进**"
need "冻结起始"           "自 ITER-0116（MILE-0016 R5）起"
need "解冻条件·归 R13"     "MILE-0016 R13"
need "解冻条件·依使用数据" "真实使用数据"
need "摆明无机器兜底"      "没有任何机器检查会拦住违反它的改动"

echo
echo "-- §3–§8 章节标题齐全（算法正文零改动） --"
grep -n '^## ' "$E"

echo
echo "-- 改动范围：新增声明块 + §2 那一处 --"
git diff --numstat -- "$E"
git diff -- "$E" | grep '^[-+]' | grep -vE '^(\+\+\+|---) ' | awk '{print substr($0,1,200)}'
echo
echo "NOTE: 删除行为 2 行而非 AC3 写的 1 行——第 2 行是把新末条的句末 '；' 改为 '。'。"
echo "      Coder/ 全仓没有任何列表以 '；' 收尾（实测 0 例），留着会是首例。详见 VERIFY_REPORT。"

echo
echo "===== AC5 · 两处镜像清除 ====="
Q="是否需要开启收敛闭环模式"
A="Butler 检测到极高复杂度任务"
echo "-- logic-protocol 主动询问（应 0） --"
n=$(grep -c "$Q" "$L" || true); echo "count=${n}"; [ "$n" -eq 0 ] || { echo "FAIL"; exit 1; }
echo "-- 规则真源激活第三条（应 0） --"
n=$(grep -c "$A" "$E" || true); echo "count=${n}"; [ "$n" -eq 0 ] || { echo "FAIL"; exit 1; }

echo
echo "-- §2 激活条件应为 2 条 --"
sed -n '/^满足以下任一条件时激活/,/^## 3\./p' "$E"
n=$(sed -n '/^满足以下任一条件时激活/,/^## 3\./p' "$E" | grep -c '^- ')
echo "count=${n}"; [ "$n" -eq 2 ] || { echo "FAIL"; exit 1; }

echo
echo "-- logic-protocol 模式清单仍 8 条、loop 那条仍在、其余 7 条未动 --"
n=$(awk '/^你必须根据用户的指令或语义环境/{f=1} /^### 审计者意识/{f=0} f && /^- \*\*/{c++} END{print c+0}' "$L")
echo "modes=${n}"; [ "$n" -eq 8 ] || { echo "FAIL"; exit 1; }
awk '/^你必须根据用户的指令或语义环境/{f=1} /^### 审计者意识/{f=0} f && /^- \*\*/' "$L" | awk '{print substr($0,1,70)}'
echo
echo "-- logic-protocol 改动范围：应只删那一段（0 增） --"
git diff --numstat -- "$L"
git diff -- "$L" | grep '^[-+]' | grep -vE '^(\+\+\+|---) ' | awk '{print substr($0,1,200)}'
a=$(git diff --numstat -- "$L" | awk '{print $1}')
[ "$a" -eq 0 ] || { echo "FAIL: logic-protocol 有新增行"; exit 1; }
echo "AC3-AC5-OK"
