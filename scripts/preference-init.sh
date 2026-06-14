#!/usr/bin/env bash
set -euo pipefail

# Butler 偏好探针存储初始化（可选·幂等）
# 把 templates/preference/ 骨架拷到外置存储 $BUTLER_PREF。
# 注：引擎在取得同意后首次采集时会自动惰性初始化；本脚本仅作可选的显式初始化。
# 已存在的 config.md / profile.md 不覆盖，保护既有数据。

BUTLER_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKEL="$BUTLER_DIR/templates/preference"

# --- 解析存储根 $PREF：环境变量优先，否则默认 ~/.butler/preferences ---
PREF="${BUTLER_PREF:-$HOME/.butler/preferences}"

echo "Butler 偏好存储根: $PREF"
if [[ -z "${BUTLER_PREF:-}" ]]; then
  echo "（未设 BUTLER_PREF 环境变量，使用默认路径；可在 shell rc 中 export BUTLER_PREF 改用别处）"
fi
echo ""

if [[ ! -d "$SKEL" ]]; then
  echo "[错误] 找不到骨架目录: $SKEL" >&2
  exit 1
fi

mkdir -p "$PREF/signals"

# config.md / profile.md：不存在才拷，存在则保留（不覆盖数据真源的派生层与参数）
for f in config.md profile.md; do
  if [[ -f "$PREF/$f" ]]; then
    echo "[保留] $PREF/$f 已存在，跳过（不覆盖）"
  else
    cp "$SKEL/$f" "$PREF/$f"
    echo "[写入] $PREF/$f"
  fi
done

# signals.example.md 仅作参考，放到存储根，不进 signals/
if [[ ! -f "$PREF/signals.example.md" ]]; then
  cp "$SKEL/signals.example.md" "$PREF/signals.example.md"
  echo "[写入] $PREF/signals.example.md （格式参考）"
fi

echo ""
echo "初始化完成（可选——引擎在取得同意后首次采集时也会自动惰性初始化）。"
echo "  采集经一次性同意后默认常驻；反哺默认关，需 /preference reback on 才开、且仅作用于有监督工作。"
echo "  真源为 $PREF/signals/，蒸馏产物为 $PREF/profile.md（通识层）。"
