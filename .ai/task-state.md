# Task State

> 无活跃迭代 · MILE-0002 R4（ITER-0024）已收口 · R5 待开。

## 当前状态

- 无活跃迭代（current=none）。上一收口 **ITER-0024**（MILE-0002 R4，2026-07-02）。
- 活跃里程碑 **MILE-0002**：R1 / R2 / R3 / R4 closed，R5 planned（未绑号）。
- 危险模式：本次自治（ITER-0024 P2→P5→收口）已终止交还；butler 仓无 `.ai/local-constraints.md` 落点，退出即回标准模式。

## 下一步入口

- MILE-0002 下一路线项 **R5**：部署 / 使用文档 + dogfood——`mcv-deployment` / `HUMAN_GUIDE` / `README` 注册桥的外部调用方式（butler 驻留工具的路径解析）；样例跑通一遍（真实项目端到端 dogfood）；长程 / 无人的残余异步入账 + 准入闸落地。R4 已铺好 SOP 协议（`Coder/20_Workflow_Lifecycle/human-test-bridge.md`）+ 桥契约（`tools/delivery-selftest/README.md`）。需用户确认后开迭代。
