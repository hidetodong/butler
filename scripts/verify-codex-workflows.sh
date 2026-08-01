#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
plugin="$repo_root/plugins/butler"
validator_root="$repo_root/tools/codex-validators"
plugin_validator="$validator_root/plugin-creator/validate_plugin.py"
skill_validator="$validator_root/skill-creator/quick_validate.py"
names=(router inbox prd review milestone upgrade init setup ideation preference progress iteration loop dangerous)

fail() { echo "[FAIL] $*" >&2; exit 1; }
require_text() { rg -q --fixed-strings "$2" "$1" || fail "$1 missing: $2"; }

[[ -f "$plugin/.codex-plugin/plugin.json" ]] || fail "missing plugin manifest"
python3 -m json.tool "$plugin/.codex-plugin/plugin.json" >/dev/null
require_text "$plugin/.codex-plugin/plugin.json" '"name": "butler"'
require_text "$plugin/.codex-plugin/plugin.json" '"skills": "./skills/"'
if rg -q '"(hooks|mcpServers|apps)"' "$plugin/.codex-plugin/plugin.json"; then
  fail "R2 manifest must not declare hooks, MCP, or apps"
fi

[[ "$(find "$plugin/skills" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')" == 14 ]] || fail "plugin must contain Router plus exactly 13 workflow skills"
[[ "$(find "$repo_root/.agents/skills" -mindepth 1 -maxdepth 1 -type l | wc -l | tr -d ' ')" == 14 ]] || fail "repo fallback must contain exactly 14 symlinks"

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
  require_text "$skill_root/agents/openai.yaml" "\$$skill"
  if [[ "$name" == router ]]; then
    require_text "$skill_root/SKILL.md" 'workflow-router.md'
    require_text "$repo_root/.claude/commands/butler.md" 'workflow-router.md'
  elif [[ "$name" == iteration ]]; then
    require_text "$skill_root/SKILL.md" 'iteration-intake.md'
    require_text "$repo_root/.claude/commands/butler/iteration.md" 'iteration-intake.md'
  elif [[ "$name" == setup ]]; then
    require_text "$skill_root/SKILL.md" 'butler-setup.md'
    require_text "$skill_root/SKILL.md" 'scripts/setup.sh'
    require_text "$repo_root/.claude/commands/butler/setup.md" 'butler-setup.md'
    require_text "$repo_root/.claude/commands/butler/setup.md" 'scripts/setup.sh'
  else
    require_text "$skill_root/SKILL.md" 'mcv-deployment.md §0.1'
    require_text "$repo_root/.claude/commands/butler/$name.md" 'mcv-deployment.md §0.1'
  fi
done

for name in loop dangerous; do
  require_text "$plugin/skills/butler-$name/agents/openai.yaml" 'allow_implicit_invocation: false'
done
for name in router inbox prd review milestone upgrade init setup ideation preference progress iteration; do
  if rg -q 'allow_implicit_invocation: false' "$plugin/skills/butler-$name/agents/openai.yaml"; then
    fail "$name must remain eligible for implicit invocation"
  fi
done

if rg -q '\[TODO:|TODO:' "$plugin"; then
  fail "plugin contains TODO placeholders"
fi

[[ -f "$plugin_validator" ]] || fail "missing pinned plugin validator: $plugin_validator"
[[ -f "$skill_validator" ]] || fail "missing pinned skill validator: $skill_validator"
python3 "$validator_root/test_vendored_validators.py" >/dev/null
python3 "$plugin_validator" "$plugin" >/dev/null
for skill_root in "$plugin"/skills/*; do
  python3 "$skill_validator" "$skill_root" >/dev/null
done

for doc in "$repo_root/README.md" "$repo_root/Coder/README.md" "$repo_root/HUMAN_GUIDE.md" "$repo_root/docs/codex-compatibility.md"; do
  require_text "$doc" 'plugins/butler'
done

echo "[OK] Codex workflow/plugin checks passed (Router + 13 workflow skills)"
