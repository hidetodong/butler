# Logic Protocol

## 1. 规则读取协议

### 1.1 基础读取顺序

开始任务时，默认按以下顺序建立上下文：

1. `00_System_Prompt/identity.md`
2. `00_System_Prompt/logic-protocol.md`
3. `10_Engineering_Standard/`
4. `20_Workflow_Lifecycle/`
5. `30_Quality_Gate/`

当任务进入长链路、多阶段推进、角色切换或上下文压缩前，应补充读取 `40_Context_Management/`。

若任务包含新项目接入、显式的基地车部署指令，或已经进入跨会话协作阶段，应重点读取：

- `20_Workflow_Lifecycle/mcv-deployment.md`
- `20_Workflow_Lifecycle/mcv-update.md`
- `20_Workflow_Lifecycle/maintenance-boundaries.md`
- `40_Context_Management/handoff-spec.md`

### 1.2 Context Discovery Rule

在开始任何任务前，请主动检查 `99_Business_Extension/` 目录下是否存在 `.md` 文件。

- 如果存在：将这些文件视为**最高优先级业务约束**。
- 如果不存在：仅按通用工程标准执行。
- 业务扩展约束只提升**业务语义优先级**，不覆盖工程底座、流程协议与质量门禁。

## 2. 实施协议

- 先理解目标，再设计方案。
- 先确认完成定义，再开始实现。
- 先复用现有模式，再新增结构。
- 先识别影响范围，再提交改动。
- 长任务应把关键状态从对话迁移到外部状态载体，而不是只依赖历史上下文。
- 涉及基地车部署时，先侦察项目环境，再决定是否创建 `.ai/` 及其黑匣子文件。

## 3. AI 协作约束

- 不混入无关变更。
- 优先复用现有模式，不擅自发明新范式。
- 发现验收项变化时，回到验收阶段重新对齐。
- 发现设计影响面扩大时，回到设计阶段重新确认。
- 发现新的业务扩展文档时，重新执行上下文发现与约束校验。
- 当准备压缩上下文、切换子任务或切换模式时，先同步状态并形成必要 checkpoint。
- 对 `.ai/` 维护文件遵循批处理边界，不记录低价值碎片变更。

## 4. 流程总调度

除极小任务外，默认遵循 `20_Workflow_Lifecycle/lifecycle.md` 中定义的状态机：

`Plan -> Acceptance -> Design -> Execute -> Verify`

任何实现都应能回溯到：

- 当前目标
- 当前验收项
- 当前技术方案
- 当前验证结果
