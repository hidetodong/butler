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

previous=0
for path in \
  ".ai/debt.md" \
  ".ai/MILESTONES.md" \
  ".ai/ITERATIONS.md" \
  ".ai/task-state.md" \
  ".ai/02_SESSION_HANDOFF.md" \
  ".ai/CONCEPT.md" \
  ".ai/AC_LIST.md" \
  ".ai/TECH_PLAN.md" \
  ".ai/VERIFY_REPORT.md"; do
  current="$(line_of "$AGENTS" "$path")"
  [[ -n "$current" ]] || fail "AGENTS.md 冷启动读序缺少：$path"
  (( current > previous )) || fail "AGENTS.md 冷启动读序错误：$path"
  previous="$current"
done

current="$(line_of "$AGENTS" '最后按文件中的指针读取 `Coder/`')"
[[ -n "$current" ]] || fail "AGENTS.md 冷启动读序缺少最终 Coder 真源步骤"
(( current > previous )) || fail "AGENTS.md 的 Coder 真源步骤不在四件套之后"
require_text "$AGENTS" "Coder/README.md"
require_text "$AGENTS" '不要全量读取 `.ai/iterations/`'

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
