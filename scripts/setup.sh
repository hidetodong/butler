#!/usr/bin/env bash
set -euo pipefail

# Butler 一次性全局安装脚本
# 运行后，所有 AI 工具会话都能自动发现 butler 规则仓库

BUTLER_DIR="$(cd "$(dirname "$0")/.." && pwd)"
export BUTLER_PATH="$BUTLER_DIR"

echo "Butler 路径: $BUTLER_DIR"
echo ""

# --- 1. 用户级配置（先完整预检，再逐对象原子替换） ---

GLOBAL_CONFIGURATOR="${BUTLER_GLOBAL_CONFIGURATOR:-$BUTLER_DIR/scripts/configure-global-install.py}"
if ! command -v python3 >/dev/null 2>&1; then
  echo "[错误] 未找到 python3；未修改任何 Butler 用户配置。" >&2
  exit 2
fi
if [[ ! -f "$GLOBAL_CONFIGURATOR" ]]; then
  echo "[错误] 全局配置 helper 不存在：$GLOBAL_CONFIGURATOR" >&2
  exit 2
fi
if ! python3 "$GLOBAL_CONFIGURATOR" --butler-root "$BUTLER_DIR" --home "$HOME"; then
  echo "[错误] Butler 用户配置未完成；Codex plugin 未开始安装。" >&2
  exit 2
fi

# --- 2. Codex plugin（独立组件；首次 hook trust 仍由用户审阅） ---

CODEX_COMMAND="${BUTLER_CODEX_COMMAND:-codex}"
CODEX_INSTALLER="${BUTLER_CODEX_INSTALLER:-$BUTLER_DIR/scripts/install-codex-plugin.sh}"
if command -v "$CODEX_COMMAND" >/dev/null 2>&1; then
  if [[ -x "$CODEX_INSTALLER" ]]; then
    if "$CODEX_INSTALLER"; then
      echo "[安装] Codex Butler plugin 已安装/刷新（请新开会话；首次 hook 启用须审阅并信任）"
    else
      rc=$?
      echo "[部分完成] Claude 与 shell 配置已完成，但 Codex plugin 安装失败（exit ${rc}）。" >&2
      echo "[错误] 修复上方 Codex 错误后重跑 setup.sh；安全配置会幂等保持。" >&2
      exit "$rc"
    fi
  else
    echo "[部分完成] Claude 与 shell 配置已完成，但 Codex installer 不可执行：$CODEX_INSTALLER" >&2
    exit 2
  fi
else
  echo "[跳过] 未找到 Codex CLI；Claude Code 安装已完成。安装 Codex 后重跑 setup.sh 即可补装 plugin。"
fi

# --- 3. Pi extension（幂等软链；Pi CLI 不可用时降级跳过） ---

PI_COMMAND="${BUTLER_PI_COMMAND:-pi}"
PI_EXTENSIONS_DIR="$HOME/.pi/agent/extensions"
PI_EXTENSION_SRC="$BUTLER_DIR/plugins/butler-pi"
PI_EXTENSION_LINK="$PI_EXTENSIONS_DIR/butler-pi"
if command -v "$PI_COMMAND" >/dev/null 2>&1; then
  mkdir -p "$PI_EXTENSIONS_DIR"
  # Idempotent: remove old symlink or directory before creating new one.
  if [[ -L "$PI_EXTENSION_LINK" ]] || [[ -d "$PI_EXTENSION_LINK" ]]; then
    rm -rf "$PI_EXTENSION_LINK"
  fi
  ln -sfn "$PI_EXTENSION_SRC" "$PI_EXTENSION_LINK"
  echo "[安装] Pi Butler 扩展已安装到 ${PI_EXTENSION_LINK}（请新开 Pi 会话生效）"
else
  echo "[跳过] 未找到 Pi CLI；Claude Code 与 Codex 安装已完成。安装 Pi 后重跑 setup.sh 即可补装扩展。"
fi

echo ""
echo "安装完成。请重启终端，或 source 你当前使用的 shell 配置文件，使环境变量生效。"
echo ""
echo "使用方式："
echo "  在任何项目中启动 AI 会话，直接给工程任务即可。"
echo "  AI 会自动从入口文件读取规则，新项目会自动触发基地车部署。"
echo "  slash 命令（如 /butler:prd）已全局安装，在所有项目里都能用。"
echo "  检测到 Codex CLI 时，Butler plugin 也会安装/刷新；新会话首次启用 hook 请审阅并信任。"
echo "  检测到 Pi CLI 时，Butler 扩展也会安装/刷新；新会话自动生效。"
echo ""
echo "可选（实验性）：偏好探针 /preference 默认关、数据外置。"
echo "  如需启用，运行一次：./scripts/preference-init.sh"
