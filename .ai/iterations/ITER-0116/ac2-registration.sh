#!/usr/bin/env bash
# AC2 · MILESTONE §5.4 追加三条 R5 登记，各自的关键措辞逐条在场
set -euo pipefail
cd "$(dirname "$0")/../../.."
S=$(awk '/^## 5\.4 范围演进记录/{f=1} f' .ai/MILESTONE.md)

echo "== R5 登记条数（应为 3） =="
n=$(printf '%s\n' "$S" | grep -c '^- 2026-08-20（R5')
echo "count=${n}"; [ "$n" -eq 3 ] || { echo "FAIL"; exit 1; }

check() {  # $1=描述 $2=必须出现的字串
  if printf '%s\n' "$S" | grep -qF -- "$2"; then
    echo "OK   $1"
  else
    echo "FAIL $1 — 缺 '$2'"; exit 1
  fi
}

echo
echo "== 第一条 · 候办与 loop 是名字撞车 =="
check "点明是名字撞车"            "名字撞车"
check "点明唯一共同点是「收敛」"   "唯一的共同点是名字里都有「收敛」"
check "写出撤候办的真实理由"       "从来没在任何真实已部署项目上跑过"
check "写出重启条件"              "R15 的真实老项目升级回归出结论之后"
check "澄清 R14/R15 未覆盖其范围"  "并没有覆盖"

echo
echo "== 第二条 · debt 那条已假 =="
check "点明开工前核查已不成立"     "开工前核查已不成立"
check "给出还清出处 commit"        "41ad694"
check "给出根因（整批迁移未复核）" "只搬字面、没有回头复核"
check "记明是已还清而非本轮修的"   "**已还清**"

echo
echo "== 第三条 · 冻结载体与无兜底 =="
check "写出落点"                  "H1 之后、\`## 1. 身份\` 之前"
check "否掉 registry 加字段"       "否掉的落点是 \`workflows/registry.json\` 加冻结字段"
check "否掉写进 frontmatter"       "也否掉了写进 frontmatter"
check "摆明没有机器兜底"           "没有任何检查会拦住有人后来又改 loop"
check "登记不触发入口重生成"       "不触发 \`[regen-entrypoints]\`"

echo "AC2-OK"
