# 迭代台账

current: ITER-0021

| 迭代号 | 标题 | 状态 | 开启 | 收口 | 所属 milestone | 交付 |
|---|---|---|---|---|---|---|
| ITER-0021 | R1 自动化优先纪律 + 分道口径：testing-strategy 升级为竭尽自动化（含浏览器自动化覆盖 UI / 交互）+ verify-schema 双道回填；人测道界定为机器不可测残余 | active | 2026-07-02 | — | MILE-0002 | — |
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
