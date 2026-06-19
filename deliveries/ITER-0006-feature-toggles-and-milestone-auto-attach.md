# ITER-0006 Butler 功能开关外化：local-constraints 统一持久配置 + 里程碑自动归属显式化

## 本次交付目标
补上与 ITER-0004（外化 ACK/分流）同源的一类洞：butler 的**持久运行模式**（危险模式、独立复核）被标为"持久、跨迭代有效"，却**没有任何文件记录**，只活在对话里——新会话无从得知上次开着什么。本轮把这类状态外化为**项目级可读可写持久配置**，统一落在已有的 `.ai/local-constraints.md`；并把里程碑"active 自动归属 / closed 不再写入"的现有行为写明白。

## 已完成内容
- **统一功能开关落点**：`.ai/local-constraints.md` 新增「Butler 功能开关」段（`dangerous` / `independent_review`，默认 off），作为"对 butler 功能做项目级持久化配置"的统一入口。原独立 `Review Policy` 字段并入，旧形式保留 legacy 兼容。
- **读写口径（schema §4.1）**：① AI 会话起始读取并据此激活/抑制持久模式；② 模式命令 NL 触发回写；③ 用户可手改；④ `dangerous: on` 跨会话生效但 **announce-on-read**——每会话起始显式声明后才自动进入，绝不静默。preference 明确排除（跨项目、外置 `$BUTLER_PREF`）。
- **读取接线**：`logic-protocol §1.3` 规定已部署项目会话起始必须读功能开关段；§4 Dangerous 条目改写为"持久态外化 + 跨会话声明后自动进入"。
- **危险模式跨会话语义改写**：`dangerous-engine §3` 把原"会话结束即回 Standard、不自动续开"改为"状态外化到 local-constraints、跨会话读到 on 声明后自动进入"，并以 §3.1 + 安全取舍说明**如实标注**这是降低安全冗余的取舍及其风险。
- **部署默认**：`mcv-deployment §4` 生成 local-constraints 时即含功能开关段、安全默认全 off。
- **里程碑自动归属显式化（Ask A）**：`lifecycle §P1` + `milestone-schema §7.2/§7.4` 明确——active 里程碑期间开启的迭代一律自动归属（认台账 `current`），收口（`current: none`）后开启的迭代独立、不写入已收口里程碑、不回挂。
- **传播**：rule-card（SSOT，模板占位符自动继承）、HUMAN_GUIDE（新增「项目级功能开关」子节 + 里程碑归属边界）、README。

## 关键变更 / 使用者可感知变化
- 危险模式/独立复核的开关现在**写在 `.ai/local-constraints.md`、跨会话保留**，不再关掉窗口就忘；可对话 NL 改、也可手改，AI 每会话开始都读。
- ⚠️ `dangerous: on` 会跨会话留存：新会话 AI 会**先显式声明**再自动进入无人值守（绝不静默）。忘了关，下次进来声明完就自己跑——只在可隔离/可回滚环境保留 on。
- 里程碑开着时新迭代自动并入、收口后新迭代独立——行为写明，不再含糊。

## 高层影响范围
- 规则层：`Coder/00_System_Prompt/logic-protocol.md`、`Coder/20_Workflow_Lifecycle/{local-constraints-schema,mcv-deployment,lifecycle,milestone-schema}.md`、`Coder/65_Extension_Dangerous/dangerous-engine.md`、`Coder/README.md`、`templates/rule-card.md`、`HUMAN_GUIDE.md`。
- 不涉及（零改动护栏）：`70_Extension_Preference/preference-probe-engine.md` 数据流、`templates/hooks/`、`iteration-schema.md`、台账 `current` 真源地位。

## 验证方式与结果摘要
- 逐 AC（AC1–AC11）grep 关键句命中各目标文件，15/15 通过。
- AC9 SSOT：`templates/CLAUDE.md.template` 仅 `{{RULE_CARD_CONTENT}}` 占位符、0 处手写功能开关。
- AC12 零改动：`git diff --name-only` 确认 preference-engine / hooks / iteration-schema 未动。
- dangerous-engine 旧"不自动续开"生效规则已替换，仅 §3.1 保留对旧设计的解释性风险引用。
- 详见 `.ai/iterations/ITER-0006/VERIFY_REPORT.md`。

## 已知剩余风险 / 延后事项
- 危险模式跨会话自动生效削弱 §3 原安全冗余——announce-on-read 兜底 + 文档如实标注，用户知情拍板。
- 功能开关靠规则纪律保证"会话起始必读"（无 hook 强制），与现有读取顺序同源同险。
- 已部署旧项目未自动回填功能开关段（legacy 全 off 兼容）；纳入 `butler-upgrade` 迁移协议属后续候选。

## 引用
- `.ai/iterations/ITER-0006/CONCEPT.md`
- `.ai/iterations/ITER-0006/AC_LIST.md`
- `.ai/iterations/ITER-0006/TECH_PLAN.md`
- `.ai/iterations/ITER-0006/VERIFY_REPORT.md`
