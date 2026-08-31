#!/usr/bin/env bash
# AC5/AC16 —— 两组可重跑扫描：A 组查残留零命中，B 组查该活下来的都还在。
set -euo pipefail
cd "$(dirname "$0")/../../.."
UV_NO_SYNC=1 uv run --locked --python 3.12.12 python .ai/iterations/ITER-0119/ac-sweep.py
