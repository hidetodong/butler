# MILE-0006 · Codex 双宿主兼容层

> 2026-07-17 · ITER-0051–ITER-0054 · v2.12.0–v2.15.0

## 里程碑结果

- R1：仓根 AGENTS.md、目标模板、`.ai/` 共同状态与双宿主架构。
- R2：8 个 focused skills、个人 Butler plugin、仓内软链单一实体源。
- R3：canonical apply_patch 的共享门禁/提醒、plugin hooks 与真实 Codex deny/allow/advisor E2E。
- R4：统一 setup、目标项目 CLAUDE.md + AGENTS.md 首次部署/升级、typed migrations 与完整隔离回归矩阵。

Butler 没有为 Codex 复制一套规则：`Coder/`、rule-card、`.ai/` 与 hook rules 仍是共同内核，两个宿主只在发现、工作流入口和工具协议层做薄适配。

## 验证基线

- Codex 0.144.5 真实 apply_patch：phase deny、protected deny、allow、PostToolUse advisory。
- 8 skills/plugin 官方 validators 与真实安装刷新。
- renderer 7 tests、setup 有/无 Codex 隔离分支、124 hook tests、R1–R4 验证脚本全绿。
- Claude 原命令、全局配置、MCV `.ai`/hooks 与 Edit/Write/MultiEdit 路径保持。

## 长期边界

- 用户必须审阅并信任 plugin hooks；危险模式不绕过宿主权限。
- PreToolUse 不是 sandbox；shell/MCP/未来新工具未经过 E2E 前不纳入保护声明。
- plugin 是机器级分发，项目仓只保存双入口和共享 `.ai/` 状态。
