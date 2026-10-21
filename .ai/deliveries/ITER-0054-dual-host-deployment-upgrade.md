# 双宿主部署升级收官：一次安装，两份入口，一套状态

> ITER-0054 · MILE-0006 R4 · 危险模式自主 ACK + P5 完整强审 · 2026-07-17 · v2.15.0

## 交付结果

- `setup.sh` 继续安装 Claude 全局配置、命令与沟通风格；检测到 Codex CLI 时同时安装/刷新 Butler plugin，无 Codex 时明确跳过。
- 新标准库 renderer 从两模板和单一 rule-card 幂等维护 CLAUDE.md + AGENTS.md；两份 user-managed 区、管理区外用户原文与旧文件权限受到保护。
- MCV 首次部署与 butler-upgrade 共用 renderer；migration schema 新增 `[regen-entrypoints]` / `[global-install]`，历史 `[regen-claude]` 自动提升为双入口动作。
- README、HUMAN_GUIDE 与兼容说明已从“R4 待办”切到完成态。

## 验证

- renderer 7 tests：首次生成、重复无 diff、普通用户内容、两份 user 区、legacy 前后缀、marker 冲突、缺模板。
- 隔离 HOME：Codex 缺失与可用两分支；Claude marker、rc、命令软链与 plugin installer 调用均通过。
- `verify-dual-host.sh` 汇总 R1–R3 scripts、124 hook tests、官方 plugin validator 和 compile，全绿。

## 危险模式披露

P2/P3 由模型自审后自主 ACK。P5 主代理发现并修正两项 Must Fix（legacy 外部用户内容保真、临时文件 0600 mode），复跑后 0 Must Fix；团队策略未授权子 agent，故不宣称独立复核。

## 边界

- hook 首次信任仍是用户动作；setup 不绕过。
- 跨文件不是文件系统级事务；写前全校验，各文件用原子 replace。
- PreToolUse 保护声明仍只覆盖已验证的 apply_patch，不外推 shell/MCP。
