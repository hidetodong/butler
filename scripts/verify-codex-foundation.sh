#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
AGENTS="$ROOT/AGENTS.md"
CODEX_TEMPLATE="$ROOT/templates/AGENTS.md.template"
CLAUDE_TEMPLATE="$ROOT/templates/CLAUDE.md.template"
ARCH_DOC="$ROOT/docs/codex-compatibility.md"
ROOT_RESOLVER="$ROOT/scripts/resolve-project-root.py"

fail() {
  echo "[FAIL] $1" >&2
  exit 1
}

require_file() {
  [[ -f "$1" ]] || fail "缺少文件：${1#$ROOT/}"
}

require_text() {
  grep -Fq "$2" "$1" || fail "${1#$ROOT/} 缺少：$2"
}

line_of() {
  grep -nF "$2" "$1" | head -1 | cut -d: -f1
}

require_file "$AGENTS"
require_file "$CODEX_TEMPLATE"
require_file "$CLAUDE_TEMPLATE"
require_file "$ARCH_DOC"
require_file "$ROOT_RESOLVER"
[[ -x "$ROOT_RESOLVER" ]] || fail "scripts/resolve-project-root.py 不可执行"

for text in \
  "这是一个 Markdown 规则仓库" \
  "编辑规则本身" \
  "不破坏分层" \
  "不破坏产物链" \
  "不引入隐式依赖" \
  "模板单一来源" \
  "frontmatter"; do
  require_text "$AGENTS" "$text"
done

# 读序正文不在本脚本里另抄一份：内容与四处载体的一致性由
# tools/context-budget/context_budget.py 的 order 投影校验与结构断言负责。
# 这里只确认 Codex 入口确实带着读序块、且最终 Coder 真源步骤在块内收尾。
begin_line="$(line_of "$AGENTS" '<!-- butler-context-order:begin -->')"
end_line="$(line_of "$AGENTS" '<!-- butler-context-order:end -->')"
[[ -n "$begin_line" ]] || fail "AGENTS.md 缺少冷启动读序块起始标记"
[[ -n "$end_line" ]] || fail "AGENTS.md 缺少冷启动读序块结束标记"
(( end_line > begin_line )) || fail "AGENTS.md 冷启动读序块标记顺序错误"

current="$(line_of "$AGENTS" '按前四步给出的指针钻取工作区四件套')"
[[ -n "$current" ]] || fail "AGENTS.md 冷启动读序缺少最终 Coder 真源步骤"
(( current > begin_line && current < end_line )) || fail "AGENTS.md 的 Coder 真源步骤不在读序块内"
require_text "$AGENTS" "Coder/README.md"
require_text "$AGENTS" '不全量读取 `.ai/iterations/`'

for placeholder in '{{BUTLER_VERSION}}' '{{RULE_CARD_CONTENT}}' '{{BUTLER_PATH}}'; do
  require_text "$CODEX_TEMPLATE" "$placeholder"
  require_text "$CLAUDE_TEMPLATE" "$placeholder"
done

for marker in '<!-- user-managed -->' '<!-- /user-managed -->'; do
  count="$(grep -Fc "$marker" "$CODEX_TEMPLATE")"
  [[ "$count" -eq 1 ]] || fail "AGENTS 模板保护区标记数量错误：$marker = $count"
done

if grep -Fq '## 强制工作流' "$CODEX_TEMPLATE"; then
  fail "AGENTS 模板手写复制了规则卡正文"
fi

diff \
  <(grep -F '{{BUTLER_PATH}}/Coder/' "$CLAUDE_TEMPLATE" | sed -E 's/^[0-9]+\. //' | sort) \
  <(grep -F '{{BUTLER_PATH}}/Coder/' "$CODEX_TEMPLATE" | sed -E 's/^[0-9]+\. //' | sort) \
  >/dev/null || fail "Claude/Codex 模板的完整规则指针不一致"

for doc in README.md Coder/README.md HUMAN_GUIDE.md; do
  require_text "$ROOT/$doc" "docs/codex-compatibility.md"
done

for text in '共同内核' 'Claude Code 适配层' 'Codex 适配层' 'R1 / ITER-0051' 'R2' 'R3' 'R4' 'apply_patch'; do
  require_text "$ARCH_DOC" "$text"
done

require_text "$ROOT/templates/rule-card.md" '会话启动目录不等于项目根'
require_text "$ROOT/Coder/20_Workflow_Lifecycle/mcv-deployment.md" 'resolve-project-root.py'
require_text "$ARCH_DOC" 'resolve-project-root.py'

echo "[OK] Codex R1 地基结构检查通过"
