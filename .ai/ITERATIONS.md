# 迭代台账

current: none

| 迭代号 | 标题 | 状态 | 开启 | 收口 | 所属 milestone | 交付 |
|---|---|---|---|---|---|---|
| ITER-0033 | R7 说人话三条硬标准 + 发长文前自检：artifact-style 新增「说人话三条」（术语先解释 / 比喻要落地 / 别让英文·变量裸奔）为跨对话与文档的通则·单一真源 + scope 从四件套扩到所有面向人落地文档 + §8 自检扩为发长文前自检；presentation-protocol 对话层引用同守（不双写）；rule-card + README 同步。不碰 identity / delivery-summary 字段、不改四件套字段结构、不做 R8、不切版、不动 hook | closed | 2026-07-07 | 2026-07-07 | MILE-0003 | deliveries/ITER-0033-plain-language-standards.md |
| ITER-0032 | R6 部署种子 + 文件夹化迁移配方（规则层准备）：mcv-deployment §2 全貌产物条两态化 + 部署建空 .ai/project/ 种子（唯一部署即建的 .ai/ 子目录例外、00_INDEX 不 stub·键控入口文件）+ line 45 老项目升级指针指 R6 配方；migration-schema §4 新增 [split] typed 标签（通用定义 + PROJECT.md→.ai/project/ 首例 + 起始态校验 + 冲突即停）+ 形态文档化·条件式前向指针指 R8/v2.0.0；翻 project-digest §9 R6 指针待→已 + header + §150；README 部署清单补空种子。不写 migrations/v2.0.0.md 实例（切版产·R8）、不迁 butler 自身、不切版、不改 R3/R5 语义、不动 hook | closed | 2026-07-07 | 2026-07-07 | MILE-0003 | deliveries/ITER-0032-deploy-seed-and-folder-migration.md |
| ITER-0031 | R5 冷启动读序切换 + digest-and-point 读纪律：context-persistence §冷启动读序 第 1 项两态化（文件夹态先读 00_INDEX + 按需主题 / 单文件态读 .ai/PROJECT.md）+ 读侧 digest-and-point 纪律（读地图→按需钻主题→指针钻代码）+ 翻 project-digest R5 指针（待→已）+ README/handoff-spec 两态措辞同步；不越 R6/R8/R7、不改 R3 强制语义 | closed | 2026-07-07 | 2026-07-07 | MILE-0003 | deliveries/ITER-0031-coldstart-read-order-switch.md |
| ITER-0030 | R4 更新说明 + 查过时两帮手定义成型 + 接线：新建 62_Extension_Agents/knowledge-fold.md（收尾把 delta 折进 .ai/project/、只写该目录）+ drift-check.md（冷启动/收口抽查说明过时、只读）+ overview 名册表两行转 ✅ + 最小回指接线（iteration §5.5 步④ / context-persistence 第 6 条）+ README 注册；两帮手 opt-in 非强制、不改 R3 折叠必做语义 | closed | 2026-07-07 | 2026-07-07 | MILE-0003 | deliveries/ITER-0030-fold-drift-helpers.md |
| ITER-0029 | R3 维护回路接线：泛化收口步④为两态（文件夹态按主题必做折叠 / 单文件暂态前滚，iteration §5.5 + milestone §7.4）+ 冷启动一致性自检加第 6 条知识文件夹漂移（条件适用）+ 全仓 5→6 计数同步 + 顺修 R2 遗留 §5→§6 引用漂移 + 翻 project-digest §6/§9 R3 指针 | closed | 2026-07-07 | 2026-07-07 | MILE-0003 | deliveries/ITER-0029-maintenance-loop-wiring.md |
| ITER-0028 | R2 知识文件夹 schema：改写 project-digest-schema 为 .ai/project/ 文件夹契约（00_INDEX 入口 + 推荐 topic 集 + 每份边界 + digest-and-point 密度 + 折叠模型声明 + 受控扩展）；哲学切换薄索引→知识地图，强制折叠/读序/迁移/自身适配留 R3/R5/R6/R8 | closed | 2026-07-06 | 2026-07-07 | MILE-0003 | deliveries/ITER-0028-knowledge-folder-schema.md |
| ITER-0027 | 吸纳最小实现纪律：新建 Coder/30_Quality_Gate/implementation-discipline.md（最小实现阶梯 + 有意简化标记 + 修根因不修症状 + 不许偷懒边界）+ rule-card 压缩条 + correction-contract 互引 + README 注册（素材取自 ponytail、用 butler 话重写、独立迭代） | closed | 2026-07-06 | 2026-07-06 | — | deliveries/ITER-0027-implementation-discipline.md |
| ITER-0026 | R1 帮手名册骨架 + 复核三拆 + 通用规矩单源化：新建 Coder/62_Extension_Agents/（overview 总述 + independent-review 复核定义）+ G1–G4 通用规矩提总述当唯一真源 + G2 诚实兜底单源回指 + 注册进 Coder/README | closed | 2026-07-05 | 2026-07-05 | MILE-0003 | deliveries/ITER-0026-agent-roster-review-split.md |
| ITER-0025 | R5 部署 / 使用文档 + dogfood：mcv-deployment 新增 butler 驻留工具调用节 + HUMAN_GUIDE 人测桥使用说明 + 真样例端到端跑通四态回路（收尾 MILE-0002） | closed | 2026-07-02 | 2026-07-02 | MILE-0002 | deliveries/ITER-0025-bridge-usage-docs.md |
| ITER-0024 | R4 等待-回收-续跑接线：新增 human-test-bridge 闭环协议（触发 + run_in_background 起桥 + 阻塞等待 + 读 results.json + 四态路由）+ 接线 P5（verify-schema/testing-strategy）/ 纠错（correction-contract）/ 无人降级（dangerous §7.4）+ 机械跑通验证 | closed | 2026-07-02 | 2026-07-02 | MILE-0002 | deliveries/ITER-0024-human-test-bridge-wiring.md |
| ITER-0023 | R3「交付自测」桥工具：Node 零依赖、GitHub 风格——manifest JSON → 渲染分步流程页 + 本地服务 + 开浏览器 → 每项四态（通过/未通过/跳过/延后处理）+ 备注 → 写 results.json + 进程自退；定义输入/输出契约 + 真测（node 断言 + Playwright） | closed | 2026-07-02 | 2026-07-02 | MILE-0002 | deliveries/ITER-0023-delivery-selftest-bridge.md |
| ITER-0022 | R2 分级置信 + 代理验证 + 依赖感知准入：verify-schema 加「可靠 / 弱 / 待人」置信档 + testing-strategy 代理验证（截图 diff / VLM 判图）earned 弱档 + dangerous-engine 无人残余处置（不阻塞入账 / 卡下游不硬闯 / 绝不假绿） | closed | 2026-07-02 | 2026-07-02 | MILE-0002 | deliveries/ITER-0022-graded-confidence-proxy-and-admission.md |
| ITER-0021 | R1 自动化优先纪律 + 分道口径：testing-strategy 升级为竭尽自动化（含浏览器自动化覆盖 UI / 交互）+ verify-schema 双道回填；人测道界定为机器不可测残余 | closed | 2026-07-02 | 2026-07-02 | MILE-0002 | deliveries/ITER-0021-automation-first-testing-lanes.md |
| ITER-0020 | 提交与切版 SOP：提交规约成文（`type(scope): 描述 (ITER-NNNN)` + `chore(release)`）+ versioning-schema §5 切版 git 仪式补全 | closed | 2026-07-02 | 2026-07-02 | — | deliveries/ITER-0020-commit-release-sop.md |
| ITER-0019 | 收口门槛：执行门禁 hook（单 active 迭代不变量）+ 冷启动一致性自检探针 + 原子收口仪式 | closed | 2026-06-30 | 2026-06-30 | MILE-0001 | deliveries/ITER-0019-close-gate.md |
| ITER-0018 | 每迭代 changelog 正式化：01_CHANGELOG 重定义为严格 ADD/EDIT/DELETE 变更流 + 新 schema + 收编半成品 + Should-Fix 迁新家 | closed | 2026-06-30 | 2026-06-30 | MILE-0001 | deliveries/ITER-0018-changelog-formalization.md |
| ITER-0017 | 新增 .ai/PROJECT.md 常驻项目摘要：冷启动全貌产物（状态取向）+ schema + 读序接线 + 收口前滚 + 部署种子 | closed | 2026-06-30 | 2026-06-30 | MILE-0001 | deliveries/ITER-0017-project-digest.md |
| ITER-0016 | tasks 步骤轻量引入（方案 A）：强化 TECH_PLAN.Execution Steps 为可勾选任务清单 + task-state 镜像活进度 | closed | 2026-06-30 | 2026-06-30 | — | deliveries/ITER-0016-tasks-step-lite.md |
| ITER-0015 | handoff 格式契约补全：固化 02_SESSION_HANDOFF 模板骨架 + 蒸馏生成流程（补领入账） | closed | 2026-06-30 | 2026-06-30 | — | deliveries/ITER-0015-handoff-template-and-flow.md |
| ITER-0014 | 版本升级 SOP 化：新增结构化迁移配方台账 + butler-upgrade 改执行器（危险模式自治） | closed | 2026-06-30 | 2026-06-30 | — | deliveries/ITER-0014-migration-ledger.md |
| ITER-0013 | CONCEPT 分层 / 渐进展开：顶部一句话 + 一行一意 + 精度单独成层，同时对人和 AI 友好 | closed | 2026-06-30 | 2026-06-30 | — | deliveries/ITER-0013-concept-layering.md |
| ITER-0012 | 四件套讲人话 + 反啰嗦：新增产物书写口径并接线四 schema / rule-card / README | closed | 2026-06-30 | 2026-06-30 | — | deliveries/ITER-0012-artifact-plain-language.md |
| ITER-0011 | 对话输出呈现协议：方案/分析/选项统一为结论先行 + 标号统一 + 表格化（过程层，与 §8 交付摘要分工） | closed | 2026-06-22 | 2026-06-22 | — | deliveries/ITER-0011-presentation-protocol.md |
| ITER-0010 | 交付总结增加固定格式 HTML 阅读视图：收口与 MD 并列产出、MD 仍为引用真源 | closed | 2026-06-20 | 2026-06-20 | — | deliveries/ITER-0010-delivery-html-view.md |
| ITER-0009 | preference 接入项目级配置：local-constraints 增 per-project 抑制开关（外置仍为跨项目真源） | closed | 2026-06-19 | 2026-06-19 | — | deliveries/ITER-0009-preference-per-project-toggle.md |
| ITER-0008 | 迭代状态枚举固化：封闭三态 + hook 机械门禁 ledger_status | closed | 2026-06-19 | 2026-06-19 | — | deliveries/ITER-0008-iteration-status-enum-lockdown.md |
| ITER-0007 | 引入硬版本概念：semver 基线 v1.0.0 + 部署版本戳 + 升级版本 gap | closed | 2026-06-19 | 2026-06-19 | — | deliveries/ITER-0007-versioning-baseline-v1.0.0.md |
| ITER-0006 | Butler 功能开关外化：local-constraints 统一持久配置（含 dangerous 跨会话）+ 里程碑自动归属显式化 | closed | 2026-06-19 | 2026-06-19 | — | deliveries/ITER-0006-feature-toggles-and-milestone-auto-attach.md |
| ITER-0005 | 里程碑录入交互优化：一次性 brief + /milestone 命令 | closed | 2026-06-19 | 2026-06-19 | — | deliveries/ITER-0005-milestone-intake-origin-command.md |
| ITER-0004 | 控制状态外化：ACK 冻结 + 入口分流可审计 | closed | 2026-06-15 | 2026-06-15 | — | deliveries/ITER-0004-ack-freeze-and-triage.md |
| ITER-0003 | 文档 scoped 有界硬约束 | closed | 2026-06-03 | 2026-06-03 | — | deliveries/ITER-0003-doc-scoping-hardening.md |
| ITER-0002 | 迭代化需求管理 | closed | 2026-06-03 | 2026-06-03 | — | deliveries/ITER-0002-iteration-requirement-mgmt.md |
| ITER-0001 | chat-recap-style 对话层风格约束 | closed | 2026-04-20 | 2026-04-20 | — | deliveries/2026-04-20-chat-recap-style.md |

> 备注：ITER-0001 是迭代机制上线前完成的任务，回溯补号；其交付文件沿用上线前的日期命名，不回溯重命名。迭代机制自 ITER-0002 起正式生效。
