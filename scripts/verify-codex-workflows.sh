#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
plugin="$repo_root/plugins/butler"
creator_root="${BUTLER_PLUGIN_CREATOR_DIR:-${CODEX_HOME:-$HOME/.codex}/skills/.system/plugin-creator}"
skill_creator_root="${BUTLER_SKILL_CREATOR_DIR:-${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator}"
names=(prd review milestone upgrade ideation preference loop dangerous)

fail() { echo "[FAIL] $*" >&2; exit 1; }
require_text() { rg -q --fixed-strings "$2" "$1" || fail "$1 missing: $2"; }

[[ -f "$plugin/.codex-plugin/plugin.json" ]] || fail "missing plugin manifest"
python3 -m json.tool "$plugin/.codex-plugin/plugin.json" >/dev/null
require_text "$plugin/.codex-plugin/plugin.json" '"name": "butler"'
require_text "$plugin/.codex-plugin/plugin.json" '"skills": "./skills/"'
if rg -q '"(hooks|mcpServers|apps)"' "$plugin/.codex-plugin/plugin.json"; then
  fail "R2 manifest must not declare hooks, MCP, or apps"
fi

[[ "$(find "$plugin/skills" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')" == 8 ]] || fail "plugin must contain exactly 8 skills"
[[ "$(find "$repo_root/.agents/skills" -mindepth 1 -maxdepth 1 -type l | wc -l | tr -d ' ')" == 8 ]] || fail "repo fallback must contain exactly 8 symlinks"

for name in "${names[@]}"; do
  skill="butler-$name"
  skill_root="$plugin/skills/$skill"
  link="$repo_root/.agents/skills/$skill"
  [[ -f "$skill_root/SKILL.md" ]] || fail "missing $skill/SKILL.md"
  [[ -f "$skill_root/agents/openai.yaml" ]] || fail "missing $skill agents/openai.yaml"
  [[ -L "$link" && -e "$link/SKILL.md" ]] || fail "broken repo fallback: $link"
  [[ "$(readlink "$link")" == "../../plugins/butler/skills/$skill" ]] || fail "fallback must be a relative canonical link: $link"
  require_text "$skill_root/SKILL.md" "name: $skill"
  require_text "$skill_root/SKILL.md" 'BUTLER_PATH'
  require_text "$skill_root/SKILL.md" 'mcv-deployment.md §0.1'
  require_text "$skill_root/agents/openai.yaml" "\$$skill"
  require_text "$repo_root/.claude/commands/butler/$name.md" 'mcv-deployment.md §0.1'
done

for name in loop dangerous; do
  require_text "$plugin/skills/butler-$name/agents/openai.yaml" 'allow_implicit_invocation: false'
done
for name in prd review milestone upgrade ideation preference; do
  if rg -q 'allow_implicit_invocation: false' "$plugin/skills/butler-$name/agents/openai.yaml"; then
    fail "$name must remain eligible for implicit invocation"
  fi
done

if rg -q '\[TODO:|TODO:' "$plugin"; then
  fail "plugin contains TODO placeholders"
fi

if [[ -f "$creator_root/scripts/validate_plugin.py" ]]; then
  command -v uv >/dev/null 2>&1 || fail "uv is required to run official validators without modifying repo dependencies"
  uv run --with pyyaml python "$creator_root/scripts/validate_plugin.py" "$plugin" >/dev/null
fi
if [[ -f "$skill_creator_root/scripts/quick_validate.py" ]]; then
  for skill_root in "$plugin"/skills/*; do
    uv run --with pyyaml python "$skill_creator_root/scripts/quick_validate.py" "$skill_root" >/dev/null
  done
fi

for doc in "$repo_root/README.md" "$repo_root/Coder/README.md" "$repo_root/HUMAN_GUIDE.md" "$repo_root/docs/codex-compatibility.md"; do
  require_text "$doc" 'plugins/butler'
done

echo "[OK] Codex R2 workflow/plugin checks passed (8 skills)"
