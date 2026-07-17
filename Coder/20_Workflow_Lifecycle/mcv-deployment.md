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

## 0.1 施工项目根解析 (Project Root Resolution)

**会话启动目录不等于施工项目根。** 在读写任何项目级 `.ai/`、`deliveries/`、`origin/`、`CLAUDE.md` 或 `AGENTS.md` 前，AI 必须先解析唯一的 `$PROJECT_ROOT`、向用户回声绝对路径与证据，后续所有项目级路径都以它为基准。`cwd` 只是发现起点，不单独构成写入授权。

调用 `$BUTLER/scripts/resolve-project-root.py`，按以下优先级命中即停：

1. 用户在任务中明确点名/确认的项目路径（`--user-target`）。
2. 从会话位置向上找到的最近已部署 Butler 项目根（`.ai/` + 带 Butler 签名/管理区的宿主入口）。
3. 会话位置所在的 Git 顶层仓库根。
4. 都不成立则 fail-closed：停下请用户点名项目，**不扫描子目录猜测，不创建任何基地车文件**。

用户已点名目标时：

```bash
PROJECT_ROOT="$(python3 "$BUTLER/scripts/resolve-project-root.py" \
  --user-target "<用户点名的项目路径>")" || exit 2
```

用户未点名、需从会话位置安全发现时：

```bash
PROJECT_ROOT="$(python3 "$BUTLER/scripts/resolve-project-root.py" \
  --start "$PWD")" || exit 2
```

严禁为了省事把 `--user-target "$PWD"` 当默认写法；只有用户确实点名/确认了该目录时它才是“用户目标”。目标不存在、不是目录、不可读写，或聚合目录本身无法证明是项目根时，解析器退出 2 且零写入。

## 1. 落地前侦察 (Scouting)

在创建任何目录前，AI 必须以 `$PROJECT_ROOT` 为边界执行以下动作并简要汇报：

- 扫描根目录判断技术栈 (`package.json`, `tsconfig.json`)。
- 识别项目结构 (`src`, `packages`, `docs`)。
- 识别当前项目命中的 domain / stack profile。
- **批判性任务：** 如果发现当前项目环境与已选中的 profile 冲突，必须在部署报告中指出；若未命中任何 profile，则仅按通用 SOP 落地。

## 2. 基础设施展开 (Scaffold)

在已解析的 `$PROJECT_ROOT` 下强制创建 `.ai/`、`deliveries/` 与 `origin/` 三类基础目录，并分别承担不同职责：

- `.ai/`：AI 工作空间，包含运行态文件与阶段产物两类内容。
- `deliveries/`：完整交付后的人类可读交付总结归档目录。
- `origin/`：**人类原始概念输入收件箱**——用户自管，存放自由格式的原始想法/概念文件（任意命名、任意数量）；AI **只读、不写不改不重塑不归档**，是 `/milestone` 等录入流的文件通道源（见 `milestone-schema.md` §6.4）。它与 `.ai/references/` 角色互斥：`references/` 是外部第三方资料（API 文档、设计稿），由 AI 处理改名注入；`origin/` 是用户自己的原始概念，始终归用户管。

部署阶段**仅创建目录**，不预置任何 `.md` 文件内容；具体文件在任务推进到对应阶段或触发对应条件时按需产生。`.ai/`、`deliveries/`、`origin/` 三个目录在部署时即创建（其中 `origin/` 为空收件箱待用户投放）。`.ai/` 下另建一个**空知识文件夹种子** `.ai/project/`（MILE-0003 R6 起）——它是**唯一在部署时即建的 `.ai/` 子目录例外**（`references/`、`iterations/`、`milestones/` 等仍按需产生），例外理由=它是项目**全貌产物之家**、空目录**标记该项目采用文件夹态**（供收口步④判"折进文件夹还是前滚单文件"），同 `origin/` 先建后投的形态。守本节"仅创建目录、不预置内容"：**只建空目录、不写 `00_INDEX` 占位**——`00_INDEX.md` + 主题文件在**首次收口前滚**时才由更新说明帮手按 `project-digest-schema.md §8` 折叠生成（部署到首收口之间无全貌可读，属与单文件项目首收口前同类暂态，冷启动键控**入口文件是否存在**而非目录存在，不误触"读不存在的 `00_INDEX`"，见 `40_Context_Management/context-persistence.md §6` 缺全貌产物倒推兜底）。

`.ai/` 目录下分为两类文件：

**运行态文件**（按需产生，随会话更新）：

- `00_IDEATION.md`：`/ideation` 模式下的脑暴过程与中间结论；收敛后由 `CONCEPT.md` 承载进入 P2 的已确认结论。
- `01_CHANGELOG.md`：记录本迭代的**对象级变更流**（严格 ADD/EDIT/DELETE、绑 AC，格式见 `changelog-schema.md`），**作用域为当前活跃迭代**（热数据）；迭代收口时其切片随迭代归档进 `iterations/ITER-NNNN/CHANGELOG.md`，全局文件随之收敛，不跨迭代无界累积（见 `iteration-schema.md` §5.5）。
- `02_SESSION_HANDOFF.md`：跨会话冷启动入口，内容结构参考 `40_Context_Management/handoff-spec.md`。
- **项目全貌产物**（项目常驻全貌摘要·状态取向，冷启动**第一读**，格式参考 `40_Context_Management/project-digest-schema.md`）——**两态**（MILE-0003 R6 起）：
  - **新项目 → `.ai/project/` 知识文件夹**（部署即带空种子，见 §2）：`00_INDEX.md` 入口 + 按主题分文件。**按需产生**——首次迭代收口前滚时由更新说明帮手按 `project-digest-schema.md §8` 折叠生成，其后每次收口按主题必做折叠（`iteration-schema.md §5.5` 步④）。
  - **单文件 `.ai/PROJECT.md`**（遗留 / 暂态形态：R6 前部署、尚未迁移的老项目；butler 仓自身已于 ITER-0034 迁为文件夹态，不再属此类）：**按需产生**——首次迭代收口前滚时落地（部署时不预置内容，符合 §2 仅创建目录原则），其后每次收口按需前滚。
  - **老项目迁移**：R6 前部署、已积累单文件 `.ai/PROJECT.md` 的老项目，其 `PROJECT.md → .ai/project/` 文件夹化由升级按 R6 迁移配方（`[rename]` + `[split]` + `[restamp]`，见 `migration-schema.md §4`）执行；实际配方实例在 butler 切版时产出（`versioning-schema.md §6.3` 步4，R8 切 v2.0.0 时落 `migrations/v2.0.0.md`）。从未产生过 `PROJECT.md` 的更老项目由升级补建：新建全貌产物并由 AI 据 `ITERATIONS.md` / `deliveries/` 首次回填一次。
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

在 `$PROJECT_ROOT` 同时生成 `CLAUDE.md`（Claude Code）与 `AGENTS.md`（Codex）。两份入口共享 `templates/rule-card.md` 真源，但各自保留宿主需要的读序；不得只生成当前会话所用宿主的那一份。

统一调用：

```bash
python3 "$BUTLER/scripts/render-project-entrypoints.py" \
  --target "$PROJECT_ROOT" --butler-root "$BUTLER"
```

渲染器按以下契约处理两份文件：

1. 分别读取 `templates/CLAUDE.md.template` 与 `templates/AGENTS.md.template`。
2. 用 `templates/rule-card.md` 中 `## 角色` 起的章节内容替换 `{{RULE_CARD_CONTENT}}` 占位符（不包含 rule-card.md 的 H1 与顶部引述）；这是浓缩规则卡的内联，确保 AI 在高注意力区域读到核心约束。
3. 用 butler 仓库的绝对路径替换 `{{BUTLER_PATH}}` 占位符，让深度阅读指针指向真实路径。
4. 读取 `$BUTLER/VERSION`，用其内容替换 `{{BUTLER_VERSION}}` 占位符，戳上目标项目所基于的 butler 规则源版本（落在 butler 管理区，供后续升级原地重戳；见 `versioning-schema.md §7`）。
5. 两份生成内容都包在 `<!-- butler-managed:start -->` / `<!-- butler-managed:end -->` 外层管理区，并各含自己的 `<!-- user-managed -->` 保护区。首次渲染后，把侦察结果分别填入两份文件的项目特定约束；后续渲染会逐字保留各自保护区。
6. 两文件先全部校验再写入；占位符、外层 marker 或 user-managed marker 异常时 fail-closed，两份都不改。

若目标项目已有任一入口且没有 Butler 外层管理区，渲染器保留原文并在末尾追加管理区；已有一对合法管理区则原位更新。重复/残缺 marker 不猜测、不覆盖，停下报告冲突。Codex plugin、skills 与 hooks 是 setup 安装的机器级能力，不复制进目标项目；项目内只落两份宿主入口和宿主无关 `.ai/` 状态。

## 4. 本地化适配 (Local Adaptation)

- 生成 `.ai/local-constraints.md`，字段定义与最小模板参考 `local-constraints-schema.md`。
- **逻辑：** 不要复制通用规则，而是通过”指针”引用。例如：”本项目遵循通用需求开发 SOP，并启用 TypeScript profile；针对 `/legacy` 目录下的旧代码，允许局部放宽类型检查。”
- **必含「Butler 功能开关」段**：生成时即写入该段，作为项目级 butler 功能持久配置的统一入口——`dangerous: off`、`independent_review: off`（安全默认），`preference: on`（默认 on；`on` 安全：实际采集仍需全局同意，未同意时不采集）。后续由命令回写或用户手改，AI 会话起始读取（见 `local-constraints-schema.md §4.1`）。

## 5. Hook 注入 (Hook Injection)

把 butler 的 hook 体系部署到目标项目的 `.claude/`。分两类：

- **PreToolUse 门禁**（`butler_gate.py`，deny-based、fail-closed）——机制化的流程约束：源码路径写操作在 P1/P2/P3 产物缺失时被拦截、AC_LIST 未冻结（`状态` 非 `ack-frozen`；无该字段的旧产物按 legacy 放行）时被拦截、`99_Business_Extension/` 写操作被拦截、迭代台账 `.ai/ITERATIONS.md` 状态列出现封闭枚举（active/closed/abandoned）外的值（如 `planned`）时被拦截、写入台账后出现 ≥2 个 `active` 迭代行（上一迭代未收口就开新）时被拦截，绕过需显式 `BUTLER_BYPASS=1` + `.ai/bypass-reason.md`（非空）。
- **PostToolUse 提醒**（`butler_advisor.py`，advisory-only、fail-open）——非阻塞自检：工具执行**之后**跑，只经 `hookSpecificOutput.additionalContext` 向模型注入提醒、**绝不 deny、绝不改写操作结果**。当前承载一条——写 `.ai/MILESTONE.md` 时若 `.ai/references/prd/` 不存在，提醒"brief 若源自外部权威规格先经 prd-split 落盘再推进"（`prd_split_reminder`，兜 PRD 先行软触发被绕过的漏切）。为什么与门禁分两套：风险方向相反——门禁宁可错拦（fail-closed），提醒宁可漏提（fail-open），advisory 混进 deny 链会误伤正常的非 PRD 里程碑写。

### 5.1 文件拷贝

将 `$BUTLER/templates/hooks/` 除 `tests/` 子目录外的内容全部拷贝到 `<target>/.claude/hooks/`：

- `butler_gate.py`（PreToolUse 门禁入口）
- `butler_advisor.py`（PostToolUse 提醒入口）
- `rules/` 整目录（含门禁 rules 与 advisory rules，如 `prd_split_reminder.py`）
- `lib/` 整目录
- `README.md`

若目标目录已存在同名文件，**以 butler 版本为准覆盖**（目标项目的 hooks 是 butler 的拷贝副本，不得本地改动；本地化需求应回流到 butler 仓库）。

### 5.2 settings.json 幂等合并

读 `$BUTLER/templates/settings.hooks-snippet.json`（含 `hooks.PreToolUse` 与 `hooks.PostToolUse` 两个键），合并进 `<target>/.claude/settings.json`。对**每个** hook 键（`PreToolUse` → `butler_gate.py`、`PostToolUse` → `butler_advisor.py`）各自套用同一套幂等规则：

1. 若目标 `settings.json` 不存在 → 直接写入整份 snippet 内容。
2. 若存在但无该键的数组 → 添加 `hooks.<键> = [snippet 中该键的条目]`。
3. 若已有该键的数组 → 检查是否已有 `matcher == “Edit|Write|MultiEdit”` 且 `command` 以对应入口（`butler_gate.py` / `butler_advisor.py`）结尾的条目；已有则跳过，否则追加。

合并规则的去重键：`hooks.<键>[*].matcher` + `command` 入口文件名字面比较；AI 执行此步骤时必须幂等，重复部署不重复插入。**升级既有部署时**：只有 PreToolUse 的旧项目，本步会为其补上 PostToolUse 键（幂等，不动已有 PreToolUse 条目）。

### 5.3 验证

部署完成后，以 `$PROJECT_ROOT` 为当前目录执行：

```bash
# PreToolUse 门禁：产物缺失时应拒绝
echo '{"tool_name":"Edit","tool_input":{"file_path":"src/x.ts"},"cwd":"'"$PROJECT_ROOT"'"}' \
  | python3 .claude/hooks/butler_gate.py
echo "gate exit=$?"

# PostToolUse 提醒：写 MILESTONE.md 且无 references/prd/ 时应放行(exit=0)且吐 additionalContext
echo '{"tool_name":"Write","tool_input":{"file_path":".ai/MILESTONE.md","content":"x"},"cwd":"'"$PROJECT_ROOT"'"}' \
  | python3 .claude/hooks/butler_advisor.py
echo "advisor exit=$?"
```

- 门禁：若 `.ai/CONCEPT.md` 等产物尚未产生 → 期望 `gate exit=2` 且 stderr 含 `phase_gate`。
- 提醒：`advisor exit=0`（**永远放行**）；若目标项目尚无 `.ai/references/prd/` → stdout 含 `additionalContext` 与 `references/prd`；已有则 stdout 为空。
- 这两条验证命令写入部署报告。

### 5.4 与 butler-upgrade 的联动

Hook 副本与 butler 仓库版本可能漂移。既有项目升级按 `butler-upgrade.md §6.4` 的 `[sync-hooks]` 同步；本协议只负责首次部署路径。

## 6. Butler 驻留工具调用（Resident Tools）

除 hook（拷进目标项目的副本）外，butler 还提供另一类能力——**驻留工具**：可执行工具存放在 butler 仓 `tools/` 下，**不拷进目标项目**，目标项目在需要时**传参调用** butler 仓里的那一份。与 hook 的部署方向正好相反——hook 是"拷副本进项目"，驻留工具是"项目按路径调 butler"，从而单一来源、不在每个项目留副本、免维护漂移。

### 6.1 路径解析

驻留工具的定位**复用 §0 的 butler 路径发现**结果 `$BUTLER`（`$BUTLER_PATH` → 全局 `CLAUDE.md` → 询问），不另造发现逻辑。工具位于 `$BUTLER/tools/<tool-name>/`。

### 6.2 交付自测桥（delivery-selftest）

当前唯一驻留工具是 **P5 人测回传桥**（`$BUTLER/tools/delivery-selftest/`）——把"机器测不了、需人判定的残余项"渲染成分步流程页给人勾四态、回传结果。目标项目在 P5 触发人测残余时按下述形态调用：

- **写 manifest**：把本项目的人测残余（`human·待人` 档 AC）整理成 manifest JSON，落**本项目** `.ai/human-test/manifest.json`（与四件套隔离，建议加入 `.gitignore`）。
- **传路径调桥**：`node $BUTLER/tools/delivery-selftest/bridge.js <本项目>/.ai/human-test/manifest.json --out <本项目>/.ai/human-test/results.json`（不在本项目存桥副本）。
- **后台起桥 + 阻塞等待 + 读回 + 四态路由**：SOP 语义（何时起、怎么等、四态怎么续跑）以 `human-test-bridge.md` 为准；manifest / results 字段与四态机器码以 `tools/delivery-selftest/README.md`（契约真源）为准——本节只定"怎么定位、怎么调"，不重抄字段、不重定义语义。

### 6.3 无人值守岔口

交付自测桥是**有人场次**工具（弹页面等人勾选）。`/butler:dangerous` 无人值守场次**不起桥**（否则页面无人提交、进程永久阻塞），人测残余改走 `65_Extension_Dangerous/dangerous-engine.md §7.4` 依赖感知准入闸（异步入账 / 卡下游不硬闯 / 绝不假绿）。一句话岔口：**有人 → 起桥；无人 → 走 §7.4**。
