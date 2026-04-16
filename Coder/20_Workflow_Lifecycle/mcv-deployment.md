---
title: 基地车 (MCV) 部署协议
audience: AI / 开发者
scope: 新项目接入或显式部署指令下的 .ai 基础设施侦察、展开与本地化适配
---

# 基地车部署协议 (MCV Deployment)

### 0. Butler 路径发现 (Path Discovery)

部署前 AI 必须先确定 butler 仓库的绝对路径。按以下优先级依次尝试，命中即停：

1. **环境变量**：执行 `echo $BUTLER_PATH`，若非空则使用。
2. **全局 CLAUDE.md**：读取 `~/.claude/CLAUDE.md`，查找其中的 butler 路径声明。
3. **用户提供**：若以上均未命中，向用户询问一次 butler 仓库路径。

确定路径后，将其记为 `$BUTLER` 供后续步骤引用。若路径无效（目录不存在或缺少 `Coder/README.md`），中止部署并报错。

### 1. 落地前侦察 (Scouting)

在创建任何目录前，AI 必须执行以下动作并简要汇报：

- 扫描根目录判断技术栈 (`package.json`, `tsconfig.json`)。
- 识别项目结构 (`src`, `packages`, `docs`)。
- 识别当前项目命中的 domain / stack profile。
- **批判性任务：** 如果发现当前项目环境与已选中的 profile 冲突，必须在部署报告中指出；若未命中任何 profile，则仅按通用 SOP 落地。

### 2. 基础设施展开 (Scaffold)

在项目根目录强制创建 `.ai/` 与 `deliveries/` 两类基础目录，并分别承担不同职责：

- `.ai/`：AI 工作空间，包含运行态文件与阶段产物两类内容。
- `deliveries/`：完整交付后的人类可读交付总结归档目录。

部署阶段**仅创建目录**，不预置任何 `.md` 文件内容；具体文件在任务推进到对应阶段或触发对应条件时按需产生。

`.ai/` 目录下分为两类文件：

**运行态文件**（按需产生，随会话更新）：

- `00_IDEATION.md`：`/ideation` 模式下的脑暴过程与中间结论；收敛后由 `CONCEPT.md` 承载进入 P2 的已确认结论。
- `01_CHANGELOG.md`：记录经过确认的技术决策与需求增量。
- `02_SESSION_HANDOFF.md`：跨会话冷启动入口，内容结构参考 `40_Context_Management/handoff-spec.md`。
- `03_BUG_LOG.md`：Ralph-Loop 熔断后的 RCA 报告或高价值逻辑坑位。
- `task-state.md`：运行时状态，按 `40_Context_Management/context-persistence.md` 维护。

**阶段产物**（任务推进时按需产生，决策记录，可复盘可审计）：

- `CONCEPT.md`：P1 问题理解说明，字段参考 `concept-schema.md`。
- `AC_LIST.md`：P2 验收清单，字段参考 `acceptance-schema.md`。
- `TECH_PLAN.md`：P3 技术方案，字段参考 `tech-plan-schema.md`。
- `VERIFY_REPORT.md`：P5 验证报告，字段参考 `verify-schema.md`。

阶段产物不在部署时创建，而是随 `lifecycle.md` 状态机推进时强制产出。每个阶段从上一阶段的产物文件读取输入，不依赖对话记忆。

**外部参考资料**（用户提供时按需处理并存入）：

- `references/` 子目录：存放经 skill 处理后的外部参考资料（API 文档、设计稿等）。
- 命名规则：`api-<name>.md`（Confluence API 文档）、`design-<name>.md`（MasterGo 设计稿）、`insight-<name>.md`（独立 Agent 产出的分析报告）、`<name>.md`（其他）。
- 处理规则参考 `00_System_Prompt/logic-protocol.md` 的参考资料注入规则。
- `references/` 目录不在部署时创建，而是在用户首次提供外部参考资料时按需创建。

### 3. 规则注入 (Rule Injection)

在目标项目根目录生成 `CLAUDE.md`（或目标 AI 工具对应的配置文件），内容由两部分组成：

1. **内联规则卡**：从 butler 仓库的 `templates/rule-card.md` 读取浓缩规则，直接写入文件正文。内联而非引用，确保 AI 在高注意力区域读到核心约束。
2. **完整规则指针**：附上 butler 仓库的绝对路径，列出深度阅读的文件清单（identity.md、logic-protocol.md、lifecycle.md 等）。路径在部署时由 AI 根据实际环境自动填入，不使用占位符。

若目标项目已存在 `CLAUDE.md`，不得覆盖，应将规则卡追加到现有内容末尾，并用分隔线标记 butler 规则区块。

### 4. 本地化适配 (Local Adaptation)

- 生成 `.ai/local-constraints.md`。
- **逻辑：** 不要复制通用规则，而是通过”指针”引用。例如：”本项目遵循通用需求开发 SOP，并启用 TypeScript profile；针对 `/legacy` 目录下的旧代码，允许局部放宽类型检查。”
