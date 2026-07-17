# Session Handoff

## 任务断点

ITER-0055 已原子收口，当前无 active 迭代；只剩 v2.16.0 产品/发布提交、tag 和真实 plugin 刷新。

## 已交付

- 单一项目根 resolver + MCV/rule-card/升级接线。
- 8 Claude commands + 8 Codex skills 共用项目根契约。
- Codex patch 绝对 target 跨 cwd 支持、相对子仓偷渡/跨多根拒绝。
- `research/.ai` 误展开残留已删除；127 hook tests 与双宿主矩阵全绿。

## 发布步骤

- 先提交 ITER-0055 产品/台账/交付/归档。
- 再修改 VERSION、plugin manifest、CHANGELOG 为 v2.16.0，独立 `chore(release)` 提交并打本地 tag。
- 最后运行真实 `scripts/setup.sh`，核对 `butler@personal` 已安装/启用且版本前缀为 2.16.0。
