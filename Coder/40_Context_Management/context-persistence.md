---
title: 上下文持久化规范
audience: AI / 开发者
scope: 长任务中的状态外化、阶段结晶与冷启动蒸馏的统一规则
---

# Context Persistence

> 双台账采用热/冷分层的项目，冷启动只读根 `.ai/ITERATIONS.md` / `.ai/MILESTONES.md` 热表与 `.ai/state-index.json`；追溯具体身份时用 state-ledger `lookup` 只读命中的一个 `.ai/history/{iterations,milestones}/` 固定区间分片。机器审计必须跨全部分片对账，AI 不得为“完整”默认吞入冷历史。

## 1. 目标

长任务质量下降的根因之一，是关键状态只存在于对话上下文里，而没有被外部化。

本规则统一管理三种密度的持久化动作：

- **运行时增量**：记录当前进度指针，防止上下文压缩后丢失。
- **阶段结晶**：在阶段边界固化最终结论，为下一阶段提供高密度入口。
- **冷启动蒸馏**：在会话边界将结论压缩为冷启动入口，写入 `02_SESSION_HANDOFF.md`。

## 2. 适用范围

以下场景必须启用状态持久化：

- 新项目接入、基地车部署或 `.ai` 基础设施初始化
- 明确需要跨会话继续
- 多阶段、多子任务推进，且阶段之间需要保留状态
- 需要等待用户 ACK、外部结果或后续回合
- 任务预计无法在单轮内闭合，或会持续产生不会自然写回代码的中间状态
- 准备压缩上下文前
- 准备切换执行者、模式或会话前

极小、低风险、一次性即可完成的任务可不强制维护外部状态。

## 3. 状态载体

载体：`.ai/task-state.md`。按任务复杂度调整内容粒度，但格式保持 Markdown 以保证人类与 AI 双向可读。载体的目标是保留**当前有效结论**，不是完整思考过程。

## 4. 运行时增量 (Incremental)

### 触发时机

- 切换子任务前
- 长任务出现方向修正时
- 已经出现目标漂移、接口遗忘、边界模糊等迹象时

### 最小记录集合

- 当前子任务是什么
- 已完成的逻辑点有哪些
- 尚未处理的边缘情况有哪些
- 当前已确认的接口契约、关键变量或结构边界
- 当前剩余风险与阻塞项
- 下一步应从哪里继续
- 出现运行时坏消息时，按 `20_Workflow_Lifecycle/goal-calibration.md` 维护 `# Goal Calibration` 表的 ID/Signal/Fact Source/Goal Impact/Route/Status；只存 open/blocked 与必要的最近 resolved 投影
- 若 `.ai/TECH_PLAN.md` 的 `Execution Steps` 是可勾选任务清单，则按任务粒度镜像完成态（已完成 / 进行中 / 下一条任务），作为 P4 的活进度板

### 记录原则

- 只记录当前仍然成立的结论
- 不记录冗长日志、失败尝试与噪音过程
- 优先记录边界、契约、风险与下一步入口
- 若代码或文档已成为权威来源，状态文件只补充"当前推进状态"，不重复复制实现细节
- 任务清单镜像服务运行态续接，**不取代**验收脊柱：AC 的勾选（§5 阶段结晶）与 P5 的 AC 回填仍以 AC 为单位，task-state 的任务进度只是其执行侧投影
- 可按 `20_Workflow_Lifecycle/goal-contract.md` 回声当前派生 Goal 状态与原因，但它仍是可重算缓存：真源冲突时重算并改正 task-state，不反向覆盖 AC、evidence、review 或台账。
- Goal Calibration 表同样是可重算投影：不能靠删行或手改 resolved 清风险，处置依据留在对应阶段产物/evidence/review。

## 5. 阶段结晶 (Crystallize)

### 触发时机

- 一个 AC 被勾选后
- 一个子任务完成后
- 一个阶段（Analysis / Acceptance / Design / Verify）结束后
- 准备切换模式前

### 动作

清理状态文件，只保留经过验证的最终结论。阶段结晶不是额外产物——它是状态文件在边界时刻的净化版。

### 最小结构

- 当前已完成项
- 关键设计决策（含被否方案及理由）
- 已修改文件
- 尚未完成项
- 剩余风险或待确认问题
- 下一步入口

### 输出约束

- 只保留最终有效结论，不保留失败尝试
- 不复制大段终端日志
- 不把临时猜测写成既定事实
- 文件列表、接口边界、风险与下一步必须明确

## 6. 冷启动蒸馏 (Distill)

### 触发时机

- 会话即将结束但任务尚未整体完成
- 上下文已严重退化，需要 clean-slate 重启

### 动作

从当前状态文件蒸馏出冷启动入口，写入 `.ai/02_SESSION_HANDOFF.md`。

蒸馏规则：

- `02_SESSION_HANDOFF.md` 的格式与字段约束以 `handoff-spec.md` 为准，模板骨架见 `handoff-spec.md` §4，具体生成步骤见 `handoff-spec.md` §5
- handoff 是**入口**而非自足包——通过状态指针引用完整 context
- 简单任务中 handoff 可自足，无需跟指针
- 复杂任务中 handoff 给方向，状态文件给细节

### Clean-Slate 协议

当上下文噪音已经影响判断质量时：

1. 执行阶段结晶，净化状态文件
2. 运行 `tools/handoff/handoff.py sync`，从权威状态生成 `02_SESSION_HANDOFF.md`
3. 以 `02_SESSION_HANDOFF.md` 为入口重新开始
4. 新入口优先读取最终结论，而不是旧日志

### 冷启动读序

冷启动 / clean-slate 重启时，按 状态 → 时间线 → 断点 → 代码 的顺序建立上下文：

1. **长期欠债与硬约束** `.ai/debt.md` —— 冷启动**第一读**：还悬着什么账、哪些是不能碰的边界。
   > 过渡说明：面向人的项目全貌摘要（原 `.ai/project/` 知识文件夹）已于 ITER-0112 退役，新的全貌产物由 MILE-0016 R2 定读序、R3 定形态与落点。在 R3 交付前，冷启动的全貌只能靠本节其余四步加 `Coder/README.md` 建立。
2. `.ai/ITERATIONS.md`（及 `MILESTONES.md`）—— 只读当前与近期热时间线；需要旧身份时沿 `.ai/state-index.json` 用 state-ledger `lookup` 定向读取一个冷分片，禁止默认读取整个 history 目录。
3. 先运行 `$BUTLER_PATH/tools/handoff/handoff.py check --project-root "$PROJECT_ROOT"`；fresh 才读 `.ai/02_SESSION_HANDOFF.md`，stale 先 sync 重建，error 先修权威状态。
4. 当前 TECH_PLAN 的方案 verdict、task-state `Goal Calibration` 与 VERIFY `Completion Inputs` —— 恢复 Goal state/reason/next；宿主 Goal/Task 只是随后可重建的投影。
5. 代码 / `deliveries/` —— 按上面三者给的指针按需钻取。

`debt.md` 与 handoff 互补：前者给"还欠什么、哪些边界不能碰"、后者给"此刻断点"。二者都不给"系统整体是什么"——在 R3 的全貌产物交付前，新会话只能从一堆迭代 delta 倒推全貌（管中窥豹），这是已知且有意接受的过渡代价。

### 冷启动一致性自检

读完台账后、动手前，核对台账↔产物↔交付↔证据无漂移。部署项目的 hook 只在**写台账时**机械兜底（`single_active_iteration` 等），此自检覆盖全部漂移面、对所有项目（含不跑自身 hook 的 butler 仓）生效。发现漂移先暴露、不静默继续：

1. **current ↔ 状态**：`current` 指向的迭代号，其台账行须为 `active`；`current: none` 时台账无 `active` 行。
2. **至多一个 active**：`ITERATIONS.md` 至多一行 `active`（多于一行 = 上一迭代未收口就开新）。
3. **closed 有交付**：每个 `closed` 行须有收口日期 + 交付链接，且 `deliveries/<链接>` 文件存在。
4. **closed 有归档**：每个 `closed` 行须有 `iterations/ITER-NNNN/` 归档快照；归档 VERIFY 含 `Evidence Index` 的新口径迭代，还须有对应 `evidence/` record，ID/日志/字节/SHA-256 全部通过只读校验。
5. **路线项对账**：`MILESTONE.md` 拆分路线图各路线项状态与其绑定迭代的实际台账状态一致（见 `20_Workflow_Lifecycle/milestone-schema.md §5.3`）。

这 5 条都是台账↔产物↔交付↔证据的对账。确定性部分先运行 `$BUTLER/scripts/audit-project-state.py --project-root "$PROJECT_ROOT"`，语义部分再按上方口径检查。这套不变量同时是收口的最后一步（见 `20_Workflow_Lifecycle/iteration-schema.md §5.5`）。

## 7. 与其他规则的关系

- 本规则负责"何时写、写什么、写到哪"。
- `handoff-spec.md` 负责 `02_SESSION_HANDOFF.md` 的格式契约。
- `20_Workflow_Lifecycle/progressive-handoff.md` 负责"长链路任务何时拆分与接力"。
- `role-switch.md` 负责角色切换时的职责边界。
