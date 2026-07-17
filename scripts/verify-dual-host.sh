#!/usr/bin/env bash
set -euo pipefail
export LC_ALL=C
export LANG=C

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WORK="$(mktemp -d "${TMPDIR:-/tmp}/butler-dual-host.XXXXXX")"
trap 'rm -rf "$WORK"' EXIT HUP INT TERM

python3 "$ROOT/scripts/test-render-project-entrypoints.py"

run_setup() {
  local home="$1"
  shift
  mkdir -p "$home"
  : > "$home/.zshrc"
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
grep -Fq '[regen-entrypoints]' "$ROOT/Coder/20_Workflow_Lifecycle/migration-schema.md"
grep -Fq '[global-install]' "$ROOT/Coder/20_Workflow_Lifecycle/migration-schema.md"
grep -Fq 'scripts/setup.sh' "$ROOT/docs/codex-compatibility.md"

bash "$ROOT/scripts/verify-codex-foundation.sh"
bash "$ROOT/scripts/verify-codex-workflows.sh"
bash "$ROOT/scripts/verify-codex-hooks.sh"
uv run --with pytest pytest "$ROOT/templates/hooks/tests" -q
uv run --with pyyaml python \
  "${BUTLER_PLUGIN_CREATOR_DIR:-${CODEX_HOME:-$HOME/.codex}/skills/.system/plugin-creator}/scripts/validate_plugin.py" \
  "$ROOT/plugins/butler"
python3 -m compileall -q "$ROOT/templates/hooks" "$ROOT/scripts/render-project-entrypoints.py"

echo "[OK] Claude/Codex unified setup and project entrypoint matrix passed"
