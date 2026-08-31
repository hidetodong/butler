#!/usr/bin/env bash
# AC11：沙箱 dogfood——两条被 active 挡住的出口各跑一遍，外加 current 非 none 的对照
# 这一档证明的是代码路径通，不是真实使用下好用；验证报告里与 AC10 分开写。
set -uo pipefail
cd "$(dirname "$0")/../../.." || exit 1
python3 .ai/iterations/ITER-0118/sandbox-dogfood.py
