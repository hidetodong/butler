#!/usr/bin/env bash
set -euo pipefail

# Butler 一次性全局安装脚本
# 运行后，所有 AI 工具会话都能自动发现 butler 规则仓库

BUTLER_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "Butler 路径: $BUTLER_DIR"
echo ""

# --- 1. 环境变量（通用，所有 AI 工具可读） ---

SHELL_RC=""
if [[ -f "$HOME/.zshrc" ]]; then
  SHELL_RC="$HOME/.zshrc"
elif [[ -f "$HOME/.bashrc" ]]; then
  SHELL_RC="$HOME/.bashrc"
fi

if [[ -n "$SHELL_RC" ]]; then
  if grep -q 'BUTLER_PATH' "$SHELL_RC" 2>/dev/null; then
    # 更新已有的 BUTLER_PATH（macOS/BSD 与 Linux sed -i 语法不同）
    if [[ "$OSTYPE" == "darwin"* ]]; then
      sed -i '' "s|export BUTLER_PATH=.*|export BUTLER_PATH=\"$BUTLER_DIR\"|" "$SHELL_RC"
    else
      sed -i "s|export BUTLER_PATH=.*|export BUTLER_PATH=\"$BUTLER_DIR\"|" "$SHELL_RC"
    fi
    echo "[更新] $SHELL_RC 中的 BUTLER_PATH 已更新"
  else
    echo "" >> "$SHELL_RC"
    echo "# Butler 规则仓库路径" >> "$SHELL_RC"
    echo "export BUTLER_PATH=\"$BUTLER_DIR\"" >> "$SHELL_RC"
    echo "[写入] BUTLER_PATH 已写入 $SHELL_RC"
  fi
else
  echo "[跳过] 未找到 .zshrc 或 .bashrc，请手动添加: export BUTLER_PATH=\"$BUTLER_DIR\""
fi

# --- 2. Claude Code 全局配置 ---

CLAUDE_GLOBAL_MD="$HOME/.claude/CLAUDE.md"
MARKER="<!-- butler-global-config -->"

mkdir -p "$HOME/.claude"

if [[ -f "$CLAUDE_GLOBAL_MD" ]] && grep -q "$MARKER" "$CLAUDE_GLOBAL_MD" 2>/dev/null; then
  # 替换已有的 butler 区块
  # 用 awk 删除旧区块，再追加新区块
  awk -v marker="$MARKER" '
    BEGIN { skip=0 }
    $0 == marker { skip = !skip; next }
    skip { next }
    { print }
  ' "$CLAUDE_GLOBAL_MD" > "${CLAUDE_GLOBAL_MD}.tmp"
  mv "${CLAUDE_GLOBAL_MD}.tmp" "$CLAUDE_GLOBAL_MD"
  echo "[更新] $CLAUDE_GLOBAL_MD 中的 butler 配置已更新"
else
  echo "[写入] butler 配置写入 $CLAUDE_GLOBAL_MD"
fi

# 追加 butler 区块
cat >> "$CLAUDE_GLOBAL_MD" << EOF

$MARKER
## Butler 工程协作规则

本机 butler 规则仓库路径: $BUTLER_DIR

当用户给出工程开发任务时，从入口文件开始建立规则上下文：
1. 读取 $BUTLER_DIR/Coder/README.md（入口文件，包含目录结构与读取顺序）
2. 按其中定义的读取顺序依次读取规则文件
3. 若当前项目不存在 .ai/ 目录，视为新项目接入，按规则自然触发基地车部署

## 个人沟通风格（跟着 butler 仓走·每个会话常开）
下面这行把沟通风格正本 @import 进来，规定我该怎么跟你说话（语气/详略/说人话）。改说话风格改那个文件即可，它是唯一正本。
@$BUTLER_DIR/communication-style.md
$MARKER
EOF

# --- 3. Claude Code 全局 slash 命令（软链，随 butler 仓自动更新） ---
# 把 butler 仓 .claude/commands/*.md 逐个软链到 ~/.claude/commands/，
# 使 /butler-* 命令在所有项目里都能被 Claude Code 发现（不只是编辑 butler 仓时）。
# 用软链而非拷贝：butler 仓一改命令即全局生效、零漂移，无需再逐项目同步副本。

BUTLER_CMD_DIR="$BUTLER_DIR/.claude/commands"
CLAUDE_CMD_DIR="$HOME/.claude/commands"

if compgen -G "$BUTLER_CMD_DIR/*.md" > /dev/null 2>&1; then
  mkdir -p "$CLAUDE_CMD_DIR"
  linked=0
  for src in "$BUTLER_CMD_DIR"/*.md; do
    # -s 符号链接 / -f 强制替换已存在目标 / -n 不跟随已存在的目录软链
    # 逐文件软链、不接管整个目录：你自己放在 ~/.claude/commands/ 的其它命令原样保留
    ln -sfn "$src" "$CLAUDE_CMD_DIR/$(basename "$src")"
    linked=$((linked + 1))
  done
  echo "[软链] ${linked} 个 butler slash 命令 → ${CLAUDE_CMD_DIR}（随 butler 仓自动更新）"
else
  echo "[跳过] $BUTLER_CMD_DIR 下暂无 *.md，无 slash 命令可安装"
fi

echo ""
echo "安装完成。请重启终端（或 source ${SHELL_RC}）使环境变量生效。"
echo ""
echo "使用方式："
echo "  在任何项目中启动 AI 会话，直接给工程任务即可。"
echo "  AI 会自动从入口文件读取规则，新项目会自动触发基地车部署。"
echo "  slash 命令（如 /butler-prd）已全局安装，在所有项目里都能用。"
echo ""
echo "可选（实验性）：偏好探针 /preference 默认关、数据外置。"
echo "  如需启用，运行一次：./scripts/preference-init.sh"
