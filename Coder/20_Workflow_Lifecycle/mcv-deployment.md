---
title: 基地车 (MCV) 部署协议
audience: AI / 开发者
scope: 新项目接入或显式部署指令下的 .ai 基础设施侦察、展开与本地化适配
---

# 基地车部署协议 (MCV Deployment)

## 0. Butler 路径发现 (Path Discovery)

部署前 AI 必须先确定 butler 仓库的绝对路径。按以下优先级依次尝试，命中即停：

1. **环境变量**：执行 `echo $BUTLER_PATH`，若非空则使用。
2. **全局 CLAUDE.md**：读取 `~/.claude/CLAUDE.md`，查找其中的 butler 路径声明。
3. **用户提供**：若以上均未命中，向用户询问一次 butler 仓库路径。

确定路径后，将其记为 `$BUTLER` 供后续步骤引用。若路径无效（目录不存在或缺少 `Coder/README.md`），中止部署并报错。

## 1. 落地前侦察 (Scouting)

在创建任何目录前，AI 必须执行以下动作并简要汇报：

- 扫描根目录判断技术栈 (`package.json`, `tsconfig.json`)。
- 识别项目结构 (`src`, `packages`, `docs`)。
- 识别当前项目命中的 domain / stack profile。
- **批判性任务：** 如果发现当前项目环境与已选中的 profile 冲突，必须在部署报告中指出；若未命中任何 profile，则仅按通用 SOP 落地。

## 2. 基础设施展开 (Scaffold)

在项目根目录强制创建 `.ai/`、`deliveries/` 与 `origin/` 三类基础目录，并分别承担不同职责：

- `.ai/`：AI 工作空间，包含运行态文件与阶段产物两类内容。
- `deliveries/`：完整交付后的人类可读交付总结归档目录。
- `origin/`：**人类原始概念输入收件箱**——用户自管，存放自由格式的原始想法/概念文件（任意命名、任意数量）；AI **只读、不写不改不重塑不归档**，是 `/milestone` 等录入流的文件通道源（见 `milestone-schema.md` §6.4）。它与 `.ai/references/` 角色互斥：`references/` 是外部第三方资料（API 文档、设计稿），由 AI 处理改名注入；`origin/` 是用户自己的原始概念，始终归用户管。

部署阶段**仅创建目录**，不预置任何 `.md` 文件内容；具体文件在任务推进到对应阶段或触发对应条件时按需产生。`.ai/`、`deliveries/`、`origin/` 三个目录在部署时即创建（其中 `origin/` 为空收件箱待用户投放）；`.ai/` 下的 `references/`、`iterations/`、`milestones/` 等子目录仍按需产生。

`.ai/` 目录下分为两类文件：

**运行态文件**（按需产生，随会话更新）：

- `00_IDEATION.md`：`/ideation` 模式下的脑暴过程与中间结论；收敛后由 `CONCEPT.md` 承载进入 P2 的已确认结论。
- `01_CHANGELOG.md`：记录经过确认的技术决策与需求增量，**作用域为当前活跃迭代**（热数据）；迭代收口时其切片随迭代归档进 `iterations/ITER-NNNN/CHANGELOG.md`，全局文件随之收敛，不跨迭代无界累积（见 `iteration-schema.md` §5.5）。
- `02_SESSION_HANDOFF.md`：跨会话冷启动入口，内容结构参考 `40_Context_Management/handoff-spec.md`。
- `03_BUG_LOG.md`：收敛闭环熔断后的 RCA 报告或高价值逻辑坑位。
- `task-state.md`：运行时状态，按 `40_Context_Management/context-persistence.md` 维护。
- `ITERATIONS.md`：迭代台账，记录 `current` 指针与全部迭代的号/标题/状态/所属 milestone/交付链接，字段参考 `iteration-schema.md`。
- `MILESTONES.md`：里程碑台账，记录 `current` 指针与全部里程碑的号/标题/状态/含迭代/交付链接，字段参考 `milestone-schema.md`；首次开启里程碑时按需产生。
- `MILESTONE.md`：当前活跃里程碑工作区，承载范围评估 / 理解阐释 / 拆分路线图 / 范围演进记录，字段参考 `milestone-schema.md`；松耦合可选、方向性不冻结，不被 hook 拦截。首次开启里程碑时按需产生。

**阶段产物 / 当前迭代工作区**（任务推进时按需产生，决策记录，可复盘可审计）：

- `CONCEPT.md`：P1 问题理解说明，字段参考 `concept-schema.md`。
- `AC_LIST.md`：P2 验收清单，字段参考 `acceptance-schema.md`。
- `TECH_PLAN.md`：P3 技术方案，字段参考 `tech-plan-schema.md`。
- `VERIFY_REPORT.md`：P5 验证报告，字段参考 `verify-schema.md`。

这四件套是固定路径的活产物，始终对应当前活跃迭代。阶段产物不在部署时创建，而是随 `lifecycle.md` 状态机推进时强制产出。每个阶段从上一阶段的产物文件读取输入，不依赖对话记忆。

**迭代归档**（首次迭代收口时按需产生，只读快照）：

- `iterations/ITER-NNNN/` 子目录：迭代收口时四件套的冻结快照（含本迭代 `CHANGELOG.md` 切片，若有），供复盘审计。归档机制以 `iteration-schema.md` 为准。
- `iterations/` 目录不在部署时创建，而是在首次迭代收口时按需产生。
- 每个 `ITER-NNNN/` 只承载该迭代内容，体量恒定；历史靠目录横向铺开，不纵向堆进单文件。

**里程碑归档**（首次里程碑收口时按需产生，只读快照）：

- `milestones/MILE-NNNN/MILESTONE.md`：里程碑收口时 `.ai/MILESTONE.md` 的冻结快照，供复盘审计。归档机制以 `milestone-schema.md` 为准。
- `milestones/` 目录不在部署时创建，而是在首次里程碑收口时按需产生。
- 里程碑级人类交付落在项目根 `deliveries/milestones/MILE-NNNN-<slug>.md`，该子目录同样在首次里程碑收口时按需产生（迭代级交付仍平铺在 `deliveries/` 根，见 `delivery-summary.md` §3）。

**外部参考资料**（用户提供时按需处理并存入）：

- `references/` 子目录：存放经 skill 处理后的外部参考资料（API 文档、设计稿等）。
- 命名规则：`api-<name>.md`（Confluence API 文档）、`design-<name>.md`（MasterGo 设计稿）、`insight-<name>.md`（独立 Agent 产出的分析报告）、`<name>.md`（其他）。
- 处理规则参考 `00_System_Prompt/logic-protocol.md` 的参考资料注入规则。
- `references/` 目录不在部署时创建，而是在用户首次提供外部参考资料时按需创建。

## 3. 规则注入 (Rule Injection)

在目标项目根目录生成 `CLAUDE.md`（或目标 AI 工具对应的配置文件）。流程：

1. 读取模板骨架 `templates/CLAUDE.md.template`。
2. 用 `templates/rule-card.md` 中 `## 角色` 起的章节内容替换 `{{RULE_CARD_CONTENT}}` 占位符（不包含 rule-card.md 的 H1 与顶部引述）；这是浓缩规则卡的内联，确保 AI 在高注意力区域读到核心约束。
3. 用 butler 仓库的绝对路径替换 `{{BUTLER_PATH}}` 占位符，让深度阅读指针指向真实路径。
4. 在 `<!-- user-managed -->` 保护区内的"项目特定约束"段填入侦察结果（识别到的技术栈、project 类型、特殊约束等）。保护区标记由 `CLAUDE.md.template` 骨架提供，部署时原样保留，作为后续 `butler-upgrade.md` 协议的升级契约起点。
5. 写入目标项目根目录 `CLAUDE.md`。

若目标项目已存在 `CLAUDE.md`，不得覆盖，应将以上生成的内容追加到现有内容末尾，并用分隔线标记 butler 规则区块。

## 4. 本地化适配 (Local Adaptation)

- 生成 `.ai/local-constraints.md`，字段定义与最小模板参考 `local-constraints-schema.md`。
- **逻辑：** 不要复制通用规则，而是通过”指针”引用。例如：”本项目遵循通用需求开发 SOP，并启用 TypeScript profile；针对 `/legacy` 目录下的旧代码，允许局部放宽类型检查。”

## 5. Hook 注入 (Hook Injection)

把 butler 的 PreToolUse hook 体系部署到目标项目的 `.claude/`。Hook 提供机制化的流程约束——源码路径写操作在 P1/P2/P3 产物缺失时被拦截、AC_LIST 未冻结（`状态` 非 `ack-frozen`；无该字段的旧产物按 legacy 放行）时被拦截、`99_Business_Extension/` 写操作被拦截，绕过需显式 `BUTLER_BYPASS=1` + `.ai/bypass-reason.md`（非空）。

### 5.1 文件拷贝

将 `$BUTLER/templates/hooks/` 除 `tests/` 子目录外的内容全部拷贝到 `<target>/.claude/hooks/`：

- `butler_gate.py`
- `rules/` 整目录
- `lib/` 整目录
- `README.md`

若目标目录已存在同名文件，**以 butler 版本为准覆盖**（目标项目的 hooks 是 butler 的拷贝副本，不得本地改动；本地化需求应回流到 butler 仓库）。

### 5.2 settings.json 幂等合并

读 `$BUTLER/templates/settings.hooks-snippet.json`，合并进 `<target>/.claude/settings.json`：

1. 若目标 `settings.json` 不存在 → 直接写入 snippet 内容。
2. 若存在但无 `hooks.PreToolUse` 数组 → 添加 `hooks.PreToolUse = [snippet 中的条目]`。
3. 若已有 `hooks.PreToolUse` 数组 → 检查是否已有 `matcher == “Edit|Write|MultiEdit”` 且 `command` 以 `python3 .claude/hooks/butler_gate.py` 结尾的条目；已有则跳过，否则追加。

合并规则的去重键：`hooks.PreToolUse[*].matcher` 字面比较；AI 执行此步骤时必须幂等，重复部署不重复插入。

### 5.3 验证

部署完成后，在目标项目根执行：

```bash
echo '{"tool_name":"Edit","tool_input":{"file_path":"src/x.ts"},"cwd":"'"$(pwd)"'"}' \
  | python3 .claude/hooks/butler_gate.py
echo "exit=$?"
```

- 若 `.ai/CONCEPT.md` 等产物尚未产生 → 期望 `exit=2` 且 stderr 含 `phase_gate`。
- 这条验证命令写入部署报告。

### 5.4 与 butler-upgrade 的联动（Follow-up）

Hook 副本与 butler 仓库版本可能漂移。`butler-upgrade.md` 协议需要扩展以检测并同步 hook 副本；本协议本身只负责**首次部署路径**，不处理升级。
