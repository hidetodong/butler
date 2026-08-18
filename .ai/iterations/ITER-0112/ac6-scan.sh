#!/bin/bash
# 归档白名单外的活文件里，机制关键词应零命中（除本迭代产物与两条退役注记）
hits=$(grep -rEl 'project-digest|knowledge-fold|drift-check|fold-state' \
  --include='*.md' --include='*.py' --include='*.sh' --include='*.json' --include='*.template' . 2>/dev/null \
  | grep -v '^\./\.git/' \
  | grep -v '^\./\.ai/iterations/' | grep -v '^\./\.ai/milestones/' | grep -v '^\./\.ai/history/' \
  | grep -v '^\./deliveries/' | grep -v '^\./docs/research/' \
  | grep -v '^\./migrations/v[12]\.' | grep -v '^\./CHANGELOG\.md$' \
  | grep -v '^\./\.ai/[0-9A-Za-z_-]*\.md$' | grep -v '^\./\.ai/handoff-state\.json$' \
  | grep -v '^\./\.ai/task-state\.md$' \
  | grep -v '^\./\.ai/verification-evidence/' \
  | grep -v '^\./Coder/20_Workflow_Lifecycle/migration-schema\.md$' \
  | grep -v '^\./Coder/62_Extension_Agents/overview\.md$')
echo "非白名单命中:"; echo "$hits"
[[ -z "$hits" ]] || exit 1
echo "AC6-CLEAN"
# 剩余 .ai/project 路径字样必须指向实存文件
echo "--- .ai/project 路径引用去向 ---"
for f in $(grep -rl '\.ai/project/' --include='*.md' --include='*.py' Coder/ tools/ templates/ scripts/ AGENTS.md 2>/dev/null); do
  grep -o '\.ai/project/[a-z_]*\.md' "$f" | sort -u | while read -r t; do
    case "$t" in
      .ai/project/workspaces.md) echo "OK   $f -> $t (部署项目侧文件, butler 单包仓无此文件)"; continue ;;
      .ai/project/partial.md)    echo "OK   $f -> $t (测试夹具路径, 非真实文件)"; continue ;;
    esac
    if [[ -f "$t" ]]; then echo "OK   $f -> $t"; else echo "DEAD $f -> $t"; exit 1; fi
  done
done
