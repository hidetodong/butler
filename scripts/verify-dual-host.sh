#!/usr/bin/env bash
set -euo pipefail
export LC_ALL=C
export LANG=C

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WORK="$(mktemp -d "${TMPDIR:-/tmp}/butler-dual-host.XXXXXX")"
trap 'rm -rf "$WORK"' EXIT HUP INT TERM

python3 "$ROOT/scripts/test-render-project-entrypoints.py"
python3 "$ROOT/scripts/test-resolve-project-root.py"
python3 "$ROOT/scripts/test-configure-global-install.py"
python3 "$ROOT/scripts/test-butler-upgrade.py"
python3 "$ROOT/scripts/test-workflow-registry.py"
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

# Codex 可用：setup 调 installer，且本进程已导出正确 BUTLER_PATH。
WITH_CODEX_HOME="$WORK/with-codex-home"
BIN="$WORK/bin"
mkdir -p "$BIN"
printf '#!/bin/sh\nexit 0\n' > "$BIN/fake-codex"
printf '#!/bin/sh\nprintf "%%s" "$BUTLER_PATH" > "$HOME/plugin-installed"\n' > "$BIN/fake-installer"
chmod +x "$BIN/fake-codex" "$BIN/fake-installer"
run_setup "$WITH_CODEX_HOME" env PATH="$BIN:$PATH" BUTLER_CODEX_COMMAND=fake-codex BUTLER_CODEX_INSTALLER="$BIN/fake-installer" > "$WORK/with-codex.log"
grep -q 'Codex Butler plugin 已安装/刷新' "$WORK/with-codex.log"
[[ "$(cat "$WITH_CODEX_HOME/plugin-installed")" == "$ROOT" ]]

# Codex 是独立组件：它失败时保留已完成的安全配置，但不得输出总成功。
FAILED_CODEX_HOME="$WORK/failed-codex-home"
printf '#!/bin/sh\nexit 7\n' > "$BIN/failing-installer"
chmod +x "$BIN/failing-installer"
set +e
run_setup "$FAILED_CODEX_HOME" env PATH="$BIN:$PATH" BUTLER_CODEX_COMMAND=fake-codex BUTLER_CODEX_INSTALLER="$BIN/failing-installer" > "$WORK/failed-codex.log" 2>&1
failed_codex_rc=$?
set -e
[[ "$failed_codex_rc" -eq 7 ]]
grep -q '部分完成.*Codex plugin 安装失败' "$WORK/failed-codex.log"
! grep -q '^安装完成' "$WORK/failed-codex.log"
[[ -f "$FAILED_CODEX_HOME/.claude/CLAUDE.md" ]]
[[ -L "$FAILED_CODEX_HOME/.claude/commands/butler" ]]
[[ "$(grep -c '^export BUTLER_PATH=' "$FAILED_CODEX_HOME/.zshrc")" -eq 1 ]]

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

echo "[OK] Claude/Codex unified setup and project entrypoint matrix passed"
