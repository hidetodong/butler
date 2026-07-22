---
description: 扫描需求收件箱，逐项分类并安全路由到 PRD、ideation、milestone backlog 或仅记录
argument-hint: "[status | scan | apply | route]"
---

你正在执行 Butler 需求收件箱动作。本入口是薄壳，不复制扫描、分类或派生算法。

1. 从 `$BUTLER_PATH` 解析 Butler 仓库；未设置或缺少 `Coder/README.md` 时停止，不猜规则位置。
2. 按 `$BUTLER_PATH/Coder/20_Workflow_Lifecycle/mcv-deployment.md §0.1` 解析唯一 `PROJECT_ROOT`；所有 `.ai/` 写入都相对它。
3. 读取并执行 `$BUTLER_PATH/Coder/40_Context_Management/inbox-schema.md` 与 `inbox-workflow.md`。
4. 按 `$ARGUMENTS` 选择 status / scan / apply / route；留空按 scan 的零写计划处理。
5. `origin/` 始终只读；真正派生动作必须委托协议指定的现有规则真源。

收尾按 source_id 汇报 routed、ignored、awaiting-confirmation 与 failed；不得把待确认项说成已完成。
