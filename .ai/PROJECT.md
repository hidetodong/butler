# Project Digest

## 目的

butler 是一套面向 AI 辅助工程开发的通用协作 SOP **规则仓库**（Markdown）。它定义 AI 接手工程任务时怎么分析 / 验收 / 设计 / 执行 / 验证，并把过程产物结构化落盘，使协作可追溯、可审计、可跨会话恢复。使用者：用 Claude Code 等 AI 编程的开发者。注意：编辑本仓 = 改规则本身，不是用规则开发软件。

## 架构与模块地图

- `Coder/`：核心 SOP 体系，三层分明——SOP Core（`00` 身份/逻辑/呈现、`20` 生命周期、`30` 质量门禁、`40` 上下文）、Domain Profiles（`10` 按栈启用）、Business Extension（`99` 最高优先级业务约束）。入口 `Coder/README.md`（目录 + 读取顺序真源）。
- 扩展模块（按需触发）：`50` 脑暴 `/ideation`、`55` 收敛闭环 `/loop`、`60` 代码复核 `/review`、`62` 帮手名册（帮手中立定义 + 通用规矩 G1–G4 唯一真源，触发式加载、不进冷启动必读）、`65` 危险模式 `/dangerous`、`70` 偏好探针 `/preference`。
- `templates/`：目标项目的 CLAUDE.md 模板、浓缩规则卡（`rule-card.md` SSOT）、交付 HTML 模板、hook 体系（PreToolUse 机械门禁）。
- `tools/`：butler 驻留可执行工具（非规则、非部署模板；目标项目传参调用、不拷副本）。当前含 `delivery-selftest/`（交付自测人测回传桥，Node 零依赖：manifest JSON → GitHub 风格分步流程页 → 四态回传 → 写 results.json + 自退；MILE-0002 R3，契约见其 README；P5 下游接线协议见 `Coder/20_Workflow_Lifecycle/human-test-bridge.md`，R4；外部调用 / 部署方式见 `mcv-deployment.md §6`「butler 驻留工具调用」、人类使用说明见 `HUMAN_GUIDE.md §5 人测回环`，R5）。
- `Learner/` / `Composer/`：学习事务 / 杂项事务子系统。
- 发布元数据：`VERSION`（版本号机器 SSOT）、`CHANGELOG.md`（发布史）、`migrations/`（迁移配方）、`deliveries/`（交付总结）。

## 关键长期决策与不变量

- **三层分层不混**：SOP Core / Domain / Business 职责不互窜。
- **产物链不依赖对话记忆**：P1 CONCEPT → P2 AC_LIST → P3 TECH_PLAN → P5 VERIFY，每阶段从上一阶段文件读取。
- **迭代/里程碑双层**：迭代(ITER-NNNN)是固定需求的 P1-P5 闭环单元；里程碑(MILE-NNNN)是套在其上的版本范围单元，松耦合可选。台账 `.ai/ITERATIONS.md` / `.ai/MILESTONES.md` 是号与状态真源。
- **AC 是验收脊柱**：贯穿 P2→P4→P5；tasks（Execution Steps + task-state）只是执行侧投影，不取代 AC。
- **模板单一来源**：强制约束改 `rule-card.md` 一处，`CLAUDE.md.template` 占位符引用。
- **文档有界、历史横向归档**：单份产物只承载当前迭代，历史靠 `iterations/ITER-NNNN/` 横向铺开，禁纵向堆积。
- **hook 机械门禁**：部署项目由 PreToolUse hook 拦截跳阶段 / 未冻结 AC / 越界写 / 双 active 迭代（`single_active_iteration`：写 ITERATIONS 后 active 行 >1 即 deny）；butler 仓自身不跑自己的 hook（规则仓非部署项目），改由 prompt 级一致性自检兜底。
- **冷启动读序固定**：`PROJECT.md`（状态全貌）→ `ITERATIONS.md`（变更流）→ `02_SESSION_HANDOFF.md`（断点）→ 代码；读序末尾 + 收口末步各跑一遍一致性自检 5 不变量（current↔状态 / 至多一 active / closed 有交付且文件在 / closed 有归档 / 里程碑路线项对账），漂移先暴露；收口时按需前滚 PROJECT.md（见 `project-digest-schema.md` / `context-persistence.md`）。
- **收口是原子仪式**：`iteration-schema §5.5` 五步——①归档四件套+changelog切片 ②交付 md+html ③翻台账+收编 01_CHANGELOG ④按需前滚 PROJECT ⑤收口自检；前三必做、缺一不可，末步强制自检。
- **每迭代对象级变更流**：`01_CHANGELOG.md` 记本迭代 ADD/EDIT/DELETE（绑 AC、文件+章节级），收口归档 `iterations/ITER-NNNN/CHANGELOG.md`（见 `changelog-schema.md`）；Review/自评的 Should Fix 归 `VERIFY_REPORT.md` 的 Remaining Risks，不入 changelog。
- **帮手名册（MILE-0003 R1 起）**：butler 派出去的"帮手"= 一份中立定义资料、用时读、临时起干净子 agent 执行、**不下发到项目**；总述 `62_Extension_Agents/overview.md` 是名册与通用规矩 G1–G4（干净上下文 / 叫不起来如实说·绝不假装做过 / 权限约定 / 定义资料用时读不下发）的**唯一真源**，各引用点回指不双写。当前住册：复核 `independent-review`（已立）；更新说明 / 查过时（占位，R4）。复核的共享审查流程仍以 `60_Extension_CodeReview/review-engine.md` 为真源，名册只管"把流程放进隔离上下文跑"的专有部分。

## 现行约束

- 写作面向 AI 执行：用"必须 / 不得 / 应"，中文说明、标识符与文件名用英文。
- 新增规则文件必须在 `Coder/README.md` 目录结构 + 读取顺序注册（无隐式依赖）。
- 每个规则文件 frontmatter 必须标 audience + scope。
- 版本 semver：MAJOR 破坏 / MINOR 兼容新增 / PATCH 澄清；切版必写迁移配方 + 打 tag `vX.Y.Z`，切版前后各跑一遍一致性自检（见 `versioning-schema.md §6`）。
- 提交规约：commit message 用 `type(scope): 中文描述 (ITER-NNNN)`、发布用 `chore(release): vX.Y.Z — 聚合 …`、末行 `Co-Authored-By` 署名；提交单元=迭代收口，"提交 ≠ 切版"；非 hook 门禁，靠纪律兜底（见 `versioning-schema.md §5`）。
- 测试自动化优先：能自动化的验证必须自动化（含浏览器自动化覆盖 UI / 交互），人测只留机器不可测残余；P5 验证按自动道 / 人测道分道回填、叠**分级置信**「可靠 / 弱 / 待人」（见 `testing-strategy.md §3` / `verify-schema.md`）。感知项先造**代理验证**（截图 diff / VLM 判图，`testing-strategy §3.1`）earned 弱档、不冒充可靠绿。人测残余的**回传闭环**走 `human-test-bridge.md`——有人场次经交付自测桥四态回传续跑（通过=收口 / 未通过=纠错 / 延后=入账不阻塞 / 跳过=N/A）、无人值守不起桥走 `dangerous §7.4`。非 hook 门禁，靠纪律 + 收口自检兜底。
- 最小实现纪律（P4 常驻写码底线，与纠错契约并列，见 `implementation-discipline.md`）：写新码爬「最小实现阶梯」（YAGNI→复用→标准库→平台原生→已装依赖→一行→最小新代码，停在第一个成立的档）；有意简化用 `butler-min:` 注释标明天花板 + 升级路径；修 bug 挖根因不打症状补丁（grep 全 caller、守卫放共享函数一处）。但信任边界校验 / 防丢数据 / 安全 / 无障碍 / 用户明确要求不得砍，且绝不对"理解问题"偷懒。
- 无人残余处置（`/dangerous`）：无人值守下人测残余按 `dangerous-engine §7.4` 依赖感知准入闸处置——不阻塞异步入账、卡下游不硬闯（弱验证顶 / 砍分支 / 不具准入资格交还）、**红线绝不假绿**。

## 已知长期欠债

- butler 仓自身不 dogfood 运行自己的 hook → live 机械门槛（含 `single_active_iteration`）在 butler 内不触发，靠 pytest 验证 + prompt 级一致性自检覆盖 butler 侧（MILE-0001 R2 已补执行门禁 hook + 自检探针；butler 侧不 live 化仍是已知设计约束）。
- `/butler-upgrade` 协议从未在真实老项目实跑过（历史 dogfood 债）。

## 指针

- 规则入口：`Coder/README.md`（目录 + 读取顺序）、`Coder/architecture-overview.md`（分层说明）。
- 当前迭代 / 里程碑：`.ai/ITERATIONS.md`、`.ai/MILESTONES.md`、`.ai/MILESTONE.md`。
- 发布史：`CHANGELOG.md`、`deliveries/`、`migrations/`。
- 本仓编辑约定：仓库根 `CLAUDE.md`。
