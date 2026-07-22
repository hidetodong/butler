# ITER-0081 · 确定性 PRD 改版执行与回执

## Problem

- `prd-update.md` 只有人工步骤，没有能证明“先冻旧版、再切 live/总索引、失败恢复”的机械执行器。
- 新版原文的模块边界与跨版认亲需要语义确认，但确认结果没有稳定输入格式，重复执行可能重新猜。
- 三态影响面停留在对话，`status` 无法恢复上次更新改了什么、用户决定如何处理 active/closed 工作。
- 更新目标若省略、spec 与现场漂移或切换中断，可能改错需求或留下半版。

## Goal

- 用显式 `prd_id` + 已确认 update spec 驱动零写 plan、事务 apply、持久 receipt、verify/rollback 和幂等重放。

## In Scope

- JSON update spec：old/new version、最终 active 模块原文、origins/removed 认亲、确认事实与逐影响处置。
- 复用 R6 status parser 校验 collection/index/module/workspace 基线，plan 默认零写并报告内容 diff/影响/缺失处置。
- 整个 PRD collection 同父 staging + backup + rename：目标内先建旧版全量 archive，再更新 live、单需求/项目索引和 receipt。
- receipt 保存 spec/source hash、pre/post tree、archive、module changes、三态影响与 disposition；status 只读展示最近更新。
- verify/rollback、排他 lock、重复 apply、故障注入、receipt/backup 路径加固和 closed/origin 零写。

## Out of Scope

- 不让工具自行理解原始大 PRD、猜模块边界或自动认亲；模型/用户确认后才生成 spec。
- 不自动 amend active AC、不改 closed 历史、不自动开后续迭代；只记录处置。
- 不实现 R8 workspace 自动发现、git diff/hook 门禁或真实 apps dogfood。

## Key Decisions

- 语义层产“最终 active 模块 + origins + removed + dispositions”，机械层只验证和执行；工具不内置模型启发式。
- 事务交换整个 `references/prd/`，把项目总索引、目标 live/archive 和 receipt 变成一个切换单元；pre/post 整树 hash 阻止回滚覆盖后续改动。
- source bytes 直接进入 staged live，receipt 记 SHA-256；原文路径只作证据，不复制用户源文件。
- active/closed/future 每个命中都必须有显式 disposition 才 apply；工具绝不替用户改工作产物。

## Risks

- Markdown 索引更新必须只替换目标版本/模块表，保留叙述、Workspace Scope 与其他 PRD 行。
- 整树交换需要严格 lock、路径/receipt 校验和每个 rename 点故障恢复，否则恢复动作可能伤及并发更新。
