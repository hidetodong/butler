---
title: 逻辑协议与总调度
audience: AI / 开发者
scope: 规则读取顺序、实施协议、AI 协作约束、模块激活触发与流程总调度
---

# Logic Protocol

## 1. 规则读取协议

### 1.1 基础读取顺序

开始任务时，默认按以下顺序建立上下文：

1. `00_System_Prompt/identity.md`
2. `00_System_Prompt/logic-protocol.md`
3. `20_Workflow_Lifecycle/`
4. `30_Quality_Gate/`

当任务进入长链路、多阶段推进、角色切换或上下文压缩前，应补充读取 `40_Context_Management/`。

`40_Context_Management/` 默认不是所有任务的前置必读，但在开始阶段若满足以下任一条件，应立即补充读取：

- 新项目接入、显式的基地车部署或 `.ai/` 基础设施初始化。
- 明确需要跨会话继续，或需要 checkpoint、handoff、`02_SESSION_HANDOFF.md`。
- 明确是多阶段、多子任务推进，且阶段之间需要保留状态。
- 明确需要等待用户 ACK、外部结果或后续回合才能继续。
- 明确预计无法在单轮内闭合，或会产生大量不会自然写回代码的中间状态。

AI 不要求准确预知上下文一定会压缩，而应基于启发式信号判断是否高概率进入长链路，例如：需要连续读取较多文件、需要记录阶段决策与取舍、需要保存未完成风险或下一步动作、仅靠最终代码无法恢复当前进度。

若开始时未命中上述条件，但执行过程中出现这些升级信号，应在进入下一阶段前补充读取 `40_Context_Management/`。

若任务包含新项目接入、显式的基地车部署指令，或已经进入跨会话协作阶段，应重点读取：

- `20_Workflow_Lifecycle/mcv-deployment.md`
- `20_Workflow_Lifecycle/mcv-update.md`
- `20_Workflow_Lifecycle/maintenance-boundaries.md`
- `40_Context_Management/handoff-spec.md`

若已在 P1 识别出明确项目类型或技术栈，再按需补充读取 `10_Domain_Stack_Profiles/` 中对应的 profile 文档。

### 1.2 Context Discovery Rule

在开始任何任务前，请主动检查 `99_Business_Extension/` 目录下是否存在 `.md` 文件。

- 如果存在：将这些文件视为**最高优先级业务约束**。
- 如果不存在：仅按通用需求开发 SOP 执行。
- 业务扩展约束只提升**业务语义优先级**，不覆盖工程底座、流程协议与质量门禁。
- `10_Domain_Stack_Profiles/` 中的规则只在当前项目类型命中后生效，不作为所有任务的默认前置硬约束。

## 2. 实施协议

- 先理解目标，再设计方案。
- 先确认完成定义，再开始实现。
- 先复用现有模式，再新增结构。
- 先识别影响范围，再提交改动。
- 先识别项目类型与适用 profile，再套用领域执行细则。
- 长任务应把关键状态从对话迁移到外部状态载体，而不是只依赖历史上下文。
- 涉及基地车部署时，先侦察项目环境，再决定是否创建 `.ai/`、`deliveries/` 及其对应目录内容。

## 3. AI 协作约束

- 不混入无关变更。
- 优先复用现有模式，不擅自发明新范式。
- 发现验收项变化时，回到验收阶段重新对齐。
- 发现设计影响面扩大时，回到设计阶段重新确认。
- 发现新的业务扩展文档时，重新执行上下文发现与约束校验。
- 当准备压缩上下文、切换子任务或切换模式时，先同步状态并形成必要 checkpoint。
- 对 `.ai/` 维护文件遵循批处理边界，不记录低价值碎片变更。

## 4. 模块激活感知 (Semantic Triggers)

你必须根据用户的指令或语义环境，丝滑切换模式：

- **Standard Mode (默认)**: 保持轻量，遵循 `20_Workflow_Lifecycle/` 执行任务。
- **Ideation Mode (`/ideation`)**: 激活 `50_Extension_Ideation/ideation-engine.md`。当用户提到"脑暴"、"完善需求"、"想不清楚"、"还没想好"或输入 `/ideation` 时开启。
- **Ralph-Loop Mode (`/loop`)**: 激活 `55_Extension_RalphLoop/ralph-loop-engine.md`。当用户提到"死磕"、"必须变绿"、"不准报错"、"严格校验"或输入 `/loop` 时开启。
- **Review Mode (`/review`)**: 激活 `60_Extension_CodeReview/review-engine.md`。当用户提到"看看写得怎么样"、"有没有坑"、"评价一下"、"代码审查"或输入 `/review` 时开启。P5 交付阶段默认触发简要自评（用户明确跳过时除外）。

若检测到任务复杂度极高（如核心算法、大规模重构），应主动询问："检测到逻辑复杂，是否需要开启 Ralph-Loop 模式进行自主迭代验证？"

### 审计者意识 (Auditor Mindset)

在执行 `/review` 或 P5 自评时，必须脱离"作者"身份，以"资深技术审计专家"的第三方视角审视代码。不为自己写的代码辩护，不降低审查标准。

### 外部参考资料注入 (Reference Injection)

当用户在任意阶段提供外部参考资料时，AI 必须自动识别类型并处理：

| 输入信号 | 处理方式 | 存储位置 |
|---|---|---|
| Confluence 页面链接 | 调用 `confluence-api-extractor` skill 提取结构化 API 文档 | `.ai/references/api-<name>.md` |
| MasterGo 设计稿链接 | 调用 `mastergo-codegen` skill 提取组件规格或生成代码 | `.ai/references/design-<name>.md` |
| 独立 Agent 产出的分析报告 | 直接读取（报告由用户另启 agent 使用 skill 生成） | `.ai/references/insight-<name>.md` |
| 其他文档或文件 | 直接读取并提炼关键信息 | `.ai/references/<name>.md` |

处理规则：

- 检测到链接或文件时立即处理，不等到特定阶段。
- 处理结果必须落盘到 `.ai/references/`，后续阶段通过指针引用，不依赖用户重复提供。
- 产物链（`AC_LIST.md`、`TECH_PLAN.md`）中必须标注引用了哪些参考资料。
- 若参考资料在执行过程中被更新，应回退到受影响的阶段重新对齐。

#### Fallback（skill 不可用或调用失败时）

- 若目标 skill 未安装、认证失败或调用超时，**不得**自行使用 WebFetch 等工具越权访问外部资源。
- 应主动提示用户手动提取参考资料内容并粘贴到对话，例如："`confluence-api-extractor` skill 不可用，请将 <URL> 页面内容粘贴到对话，我将落盘到 `.ai/references/api-<name>.md`"。
- 收到用户粘贴的文本后，按上表"存储位置"约定落盘，命名前缀保持一致（`api-` / `design-` / `insight-` / 无前缀）。
- Fallback 路径产出的参考资料，在 `AC_LIST.md` / `TECH_PLAN.md` 的 `External References` 中必须标注"用户手动提供"，以便审计区分 skill 自动化产物与人工产物。

## 5. 流程总调度

除极小任务外，默认遵循 `20_Workflow_Lifecycle/lifecycle.md` 中定义的状态机：

`P1 Analysis -> P2 Acceptance -> P3 Design -> P4 Execute -> P5 Verify`

任何实现都应能回溯到：

- 当前目标
- 当前验收项
- 当前技术方案
- 当前验证结果

在形成完整交付闭环时，除验证结果外，还应补一份给人看的 Delivery Summary。
