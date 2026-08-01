#!/usr/bin/env bash
set -euo pipefail
export LC_ALL=C
export LANG=C

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PLUGIN_CREATOR_ROOT="${CODEX_HOME:-$HOME/.codex}/skills/.system/plugin-creator"
WORK="$(mktemp -d "${TMPDIR:-/tmp}/butler-dual-host.XXXXXX")"
trap 'rm -rf "$WORK"' EXIT HUP INT TERM

python3 "$ROOT/scripts/test-render-project-entrypoints.py"
python3 "$ROOT/scripts/test-resolve-project-root.py"
python3 "$ROOT/scripts/test-configure-global-install.py"
python3 "$ROOT/scripts/test-butler-upgrade.py"
python3 "$ROOT/scripts/test-workflow-registry.py"
python3 "$ROOT/tools/iteration-intake/test_intake.py"
python3 "$ROOT/scripts/sync-workflow-registry.py" --check
python3 "$ROOT/tools/verification-evidence/test_evidence.py"
python3 "$ROOT/scripts/test-audit-project-state.py"
python3 "$ROOT/scripts/test-check-markdown-links.py"
python3 "$ROOT/scripts/check-markdown-links.py" --root "$ROOT"
python3 "$ROOT/scripts/test-ci-contract.py"

run_setup() {
  local home="$1"
  shift
  mkdir -p "$home"
  [[ -e "$home/.zshrc" ]] || : > "$home/.zshrc"
  HOME="$home" "$@" bash "$ROOT/scripts/setup.sh"
}

# Codex 不可用：Claude 安装仍成功且幂等。
NO_CODEX_HOME="$WORK/no-codex-home"
run_setup "$NO_CODEX_HOME" env BUTLER_CODEX_COMMAND=butler-codex-missing > "$WORK/no-codex-1.log"
run_setup "$NO_CODEX_HOME" env BUTLER_CODEX_COMMAND=butler-codex-missing > "$WORK/no-codex-2.log"
grep -q '未找到 Codex CLI' "$WORK/no-codex-2.log"
[[ "$(grep -Fc '<!-- butler-global-config -->' "$NO_CODEX_HOME/.claude/CLAUDE.md")" -eq 2 ]]
[[ -L "$NO_CODEX_HOME/.claude/commands/butler" ]]
[[ -L "$NO_CODEX_HOME/.claude/commands/butler.md" ]]
[[ "$(grep -c '^export BUTLER_PATH=' "$NO_CODEX_HOME/.zshrc")" -eq 1 ]]

# 用户配置异常：全量预检失败，shell/Claude/commands 都不产生部分写入。
CONFLICT_HOME="$WORK/conflict-home"
mkdir -p "$CONFLICT_HOME/.claude"
printf '%s\n' '# mentions BUTLER_PATH only' > "$CONFLICT_HOME/.zshrc"
printf '%s\n' 'owner-before' '<!-- butler-global-config -->' 'owner-after' > "$CONFLICT_HOME/.claude/CLAUDE.md"
conflict_shell_before="$(shasum "$CONFLICT_HOME/.zshrc")"
conflict_claude_before="$(shasum "$CONFLICT_HOME/.claude/CLAUDE.md")"
set +e
run_setup "$CONFLICT_HOME" env BUTLER_CODEX_COMMAND=butler-codex-missing > "$WORK/conflict.log" 2>&1
conflict_rc=$?
set -e
[[ "$conflict_rc" -eq 2 ]]
grep -q '应有 0 个或 2 个 Butler marker' "$WORK/conflict.log"
[[ "$conflict_shell_before" == "$(shasum "$CONFLICT_HOME/.zshrc")" ]]
[[ "$conflict_claude_before" == "$(shasum "$CONFLICT_HOME/.claude/CLAUDE.md")" ]]
[[ ! -e "$CONFLICT_HOME/.claude/commands/butler" ]]
[[ ! -e "$CONFLICT_HOME/.claude/commands/butler.md" ]]

# Codex 可用：setup 调 installer，且本进程已导出正确 BUTLER_PATH。
WITH_CODEX_HOME="$WORK/with-codex-home"
BIN="$WORK/bin"
mkdir -p "$BIN"
printf '#!/bin/sh\nexit 0\n' > "$BIN/fake-codex"
printf '#!/bin/sh\nexit 0\n' > "$BIN/fake-pi"
printf '#!/bin/sh\nprintf "%%s" "$BUTLER_PATH" > "$HOME/plugin-installed"\n' > "$BIN/fake-installer"
chmod +x "$BIN/fake-codex" "$BIN/fake-pi" "$BIN/fake-installer"
run_setup "$WITH_CODEX_HOME" env LC_ALL=C.UTF-8 LANG=C.UTF-8 PATH="$BIN:$PATH" BUTLER_CODEX_COMMAND=fake-codex BUTLER_CODEX_INSTALLER="$BIN/fake-installer" BUTLER_PI_COMMAND=fake-pi > "$WORK/with-codex.log"
grep -q 'Codex Butler plugin 已安装/刷新' "$WORK/with-codex.log"
[[ "$(cat "$WITH_CODEX_HOME/plugin-installed")" == "$ROOT" ]]
[[ -L "$WITH_CODEX_HOME/.pi/agent/extensions/butler-pi" ]]
grep -q 'Pi Butler 扩展已安装到' "$WORK/with-codex.log"

# Codex 是独立组件：它失败时保留已完成的安全配置，但不得输出总成功。
FAILED_CODEX_HOME="$WORK/failed-codex-home"
printf '#!/bin/sh\nexit 7\n' > "$BIN/failing-installer"
chmod +x "$BIN/failing-installer"
set +e
run_setup "$FAILED_CODEX_HOME" env LC_ALL=C.UTF-8 LANG=C.UTF-8 PATH="$BIN:$PATH" BUTLER_CODEX_COMMAND=fake-codex BUTLER_CODEX_INSTALLER="$BIN/failing-installer" > "$WORK/failed-codex.log" 2>&1
failed_codex_rc=$?
set -e
[[ "$failed_codex_rc" -eq 7 ]]
grep -q '部分完成.*Codex plugin 安装失败' "$WORK/failed-codex.log"
! grep -q '^安装完成' "$WORK/failed-codex.log"
[[ -f "$FAILED_CODEX_HOME/.claude/CLAUDE.md" ]]
[[ -L "$FAILED_CODEX_HOME/.claude/commands/butler" ]]
[[ -L "$FAILED_CODEX_HOME/.claude/commands/butler.md" ]]
[[ "$(grep -c '^export BUTLER_PATH=' "$FAILED_CODEX_HOME/.zshrc")" -eq 1 ]]

# 无全局 uv/PyYAML 时，installer 复用仓库锁定 venv；所有 validator runtime 都不可用则明确失败。
NO_UV_BIN="$WORK/no-uv-bin"
mkdir -p "$NO_UV_BIN"
for command_name in bash cp dirname mkdir rm; do
  ln -s "$(command -v "$command_name")" "$NO_UV_BIN/$command_name"
done
ln -s "$(command -v python3)" "$NO_UV_BIN/python3"
VALIDATOR_HOME="$WORK/validator-home"
mkdir -p "$VALIDATOR_HOME"
HOME="$VALIDATOR_HOME" PATH="$NO_UV_BIN" BUTLER_PLUGIN_CREATOR_DIR="$PLUGIN_CREATOR_ROOT" \
  bash "$ROOT/scripts/install-codex-plugin.sh" --no-add > "$WORK/validator-venv.log"
grep -q 'Plugin validation passed' "$WORK/validator-venv.log"
grep -q 'install skipped' "$WORK/validator-venv.log"

rm "$NO_UV_BIN/python3"
printf '%s\n' '#!/bin/sh' 'if [ "$1" = "-c" ] && [ "$2" = "import yaml" ]; then exit 1; fi' 'exec "$BUTLER_TEST_REAL_PYTHON" "$@"' > "$NO_UV_BIN/python3"
chmod +x "$NO_UV_BIN/python3"
set +e
HOME="$WORK/validator-missing-home" PATH="$NO_UV_BIN" BUTLER_PLUGIN_CREATOR_DIR="$PLUGIN_CREATOR_ROOT" \
  BUTLER_PLUGIN_VALIDATOR_PYTHON="$WORK/missing-python" BUTLER_TEST_REAL_PYTHON="$(command -v python3)" \
  bash "$ROOT/scripts/install-codex-plugin.sh" --no-add > "$WORK/validator-missing.log" 2>&1
validator_missing_rc=$?
set -e
[[ "$validator_missing_rc" -eq 2 ]]
grep -q 'requires uv or a Python runtime with PyYAML' "$WORK/validator-missing.log"

# 两份入口通过同一 renderer 生成，重复运行不漂移。
TARGET="$WORK/target"
mkdir -p "$TARGET"
python3 "$ROOT/scripts/render-project-entrypoints.py" --target "$TARGET" >/dev/null
before="$(shasum "$TARGET/CLAUDE.md" "$TARGET/AGENTS.md")"
python3 "$ROOT/scripts/render-project-entrypoints.py" --target "$TARGET" >/dev/null
after="$(shasum "$TARGET/CLAUDE.md" "$TARGET/AGENTS.md")"
[[ "$before" == "$after" ]]

grep -Fq 'render-project-entrypoints.py' "$ROOT/Coder/20_Workflow_Lifecycle/mcv-deployment.md"
grep -Fq 'AGENTS.md' "$ROOT/Coder/20_Workflow_Lifecycle/butler-upgrade.md"
grep -Fq 'migrations/manifest.json' "$ROOT/Coder/20_Workflow_Lifecycle/butler-upgrade.md"
grep -Fq '[regen-entrypoints]' "$ROOT/Coder/20_Workflow_Lifecycle/migration-schema.md"
grep -Fq '[global-install]' "$ROOT/Coder/20_Workflow_Lifecycle/migration-schema.md"
grep -Fq 'scripts/setup.sh' "$ROOT/docs/codex-compatibility.md"
grep -Fq '/butler:setup' "$ROOT/Coder/20_Workflow_Lifecycle/butler-setup.md"
grep -Fq 'scripts/setup.sh' "$ROOT/.claude/commands/butler/setup.md"
grep -Fq 'scripts/setup.sh' "$ROOT/plugins/butler/skills/butler-setup/SKILL.md"
grep -Fq 'Evidence Index' "$ROOT/Coder/20_Workflow_Lifecycle/verify-schema.md"
grep -Fq '无机器证据不打绿' "$ROOT/templates/rule-card.md"
grep -Fq '`reported`' "$ROOT/Coder/60_Extension_CodeReview/review-engine.md"
grep -Fq '`captured`' "$ROOT/Coder/60_Extension_CodeReview/review-engine.md"
grep -Fq '`reproduced`' "$ROOT/Coder/60_Extension_CodeReview/review-engine.md"
grep -Fq 'review-*' "$ROOT/Coder/62_Extension_Agents/independent-review.md"

bash "$ROOT/scripts/verify-codex-foundation.sh"
bash "$ROOT/scripts/verify-codex-workflows.sh"
bash "$ROOT/scripts/verify-codex-hooks.sh"
python3 -m pytest "$ROOT/templates/hooks/tests" -q
python3 -m compileall -q "$ROOT/templates/hooks" "$ROOT/scripts/render-project-entrypoints.py"
python3 -m compileall -q "$ROOT/scripts/resolve-project-root.py"
python3 -m compileall -q "$ROOT/scripts/configure-global-install.py"
python3 -m compileall -q "$ROOT/tools/verification-evidence/evidence.py"
python3 -m compileall -q "$ROOT/tools/butler-upgrade/upgrade.py"
python3 -m compileall -q "$ROOT/scripts/sync-workflow-registry.py"
python3 -m compileall -q "$ROOT/scripts/audit-project-state.py"
python3 -m compileall -q "$ROOT/tools/iteration-intake/intake.py"

echo "[OK] Claude/Codex unified setup and project entrypoint matrix passed"
