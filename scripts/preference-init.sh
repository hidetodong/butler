#!/usr/bin/env bash
set -euo pipefail

# 偏好探针的机器入口已在 ITER-0124 退役。
# 本脚本不再拷贝骨架，也不创建仓库外的偏好目录。

echo "偏好探针已退役（ITER-0124）。不再初始化外置偏好目录，也不再提供 /butler:preference。"
exit 0
