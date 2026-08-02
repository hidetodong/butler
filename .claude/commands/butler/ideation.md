---
description: 用户主动脑暴或接受 Explore 建议时，在 P1→P5 之外澄清决定与开放问题；显式 promotion 后从 Iteration P1 接回交付
argument-hint: "[贴一段模糊需求 / 想法，或留空=进入脑暴对话]"
---

你正在执行 Butler 的 **Explore / Ideation** 动作。本命令是薄壳路由器：只加载规则真源并委托执行；激活、探索、Decision Map、真源优先级与 promotion 口径一律以被指向的规则文件为准，本文件不复制算法。

> **路径约定（本命令可在任意项目里运行，当前目录不一定是 Butler 仓）**：下文引用的 `Coder/…` 是 Butler 规则仓库里的文件，相对 `$BUTLER_PATH` 解析。探索可以只留在对话中；需要持久化 Decision Map 或 promotion 时才解析目标项目根，绝不把产物写进 Butler 规则仓。

> **项目根硬门**：任何 `.ai/` 写入前，先按 `$BUTLER_PATH/Coder/20_Workflow_Lifecycle/mcv-deployment.md §0.1` 解析唯一 `PROJECT_ROOT`。目标不唯一时只保留对话结论。

## 执行

读 `Coder/50_Extension_Ideation/ideation-engine.md` 并完整遵循。保持在 P1→P5 之外，把结果区分为已确认决定、开放问题和参考依据；候选 AC 不冻结，也不充当 P2 ACK。

只有用户明确 promotion 到交付时，才解析 `PROJECT_ROOT` 并从 Iteration P1 进入正常 lifecycle；不得直接进入 P2。

## 收尾

简要回报已确认决定、开放问题、依据，以及当前是继续探索、暂停，还是等待用户选择 promotion。
