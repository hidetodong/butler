# Codex apply_patch hooks：Butler 门禁与提醒开始真实生效

> ITER-0053 · MILE-0006 R3 · 危险模式自主 ACK + P5 完整强审 · 2026-07-17 · v2.14.0

## 交付结果

- 新增 Codex patch parser，把 add/update/delete/move、多文件和多 hunk 转为逐目标 Context；现有规则判断不复制、不分叉。
- gate/advisor 同时接受 Claude `Edit/Write/MultiEdit` 和 Codex canonical `apply_patch`；任一目标 deny 会阻断整次 patch，提醒则去重注入上下文。
- plugin 默认发现 `hooks/hooks.json`；薄包装器从 `BUTLER_PATH` 调共享 Python 真源，分别保持门禁 fail-closed、提醒 fail-open。
- ledger 的非法状态、双 active 和同 patch 关旧开新都获得 patch 增量验证。

## 验证

- pytest 从 109 扩到 124 个用例，全部通过；R1/R2/R3 三个结构脚本和官方 plugin validator 通过。
- 真实 Codex 0.144.5 在无四件套仓拒绝源码 patch，目标文件不存在；受保护目录同样被拒。
- 冻结四件套仓允许普通源码 patch；修改 MILESTONE 后，PostToolUse 的 PRD 自检上下文被 Codex 实际收到并复述。

## 危险模式披露

P2/P3 未经用户逐项确认，由模型自审后自主 ACK；P5 为主代理完整多维强审，0 Must Fix。团队策略未授权子 agent，因此不宣称独立复核。

## 边界

- 用户首次启用 plugin hook 仍须审阅和信任；E2E 的 `--dangerously-bypass-hook-trust` 只用于自动化。
- PreToolUse 不是 sandbox；当前保护声明只覆盖已经观测、验证的 `apply_patch` 链路。
- R4 仍需把 setup、首次部署、既有升级和 Claude/Codex 回归矩阵统一接线。

## 引用

- 兼容说明：`docs/codex-compatibility.md`
- 验证：`.ai/iterations/ITER-0053/VERIFY_REPORT.md`
- 迁移：`migrations/v2.14.0.md`
