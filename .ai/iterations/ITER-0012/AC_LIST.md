---
状态: ack-frozen
ACK 日期: 2026-06-30
---

# Goal

- 给四件套补一条"内容怎么写"的纪律：讲人话、不啰嗦；字段结构不动。

# In Scope

- 新增 `Coder/20_Workflow_Lifecycle/artifact-style.md`：四件套通用书写口径。
- 四个 schema（concept / acceptance / tech-plan / verify）各加一行指针引用新口径，并把现有零散的"不写流水账"弱约束收编过去。
- `templates/rule-card.md` 加一条紧凑口径（写进 AI 最先读到的浓缩规则卡）。
- `Coder/README.md` 注册新文件（目录结构 + 读取顺序 + 分工说明）。

# Out of Scope

- 不改四 schema 的字段结构、必填字段、模板骨架。
- 不改 lifecycle 的分流行格式、不改对话层的 presentation-protocol 与 delivery-summary §8。
- 不回填 / 重写历史已归档的四件套。
- 本轮不切版，累积到下次发布（预计 MINOR）。

# Acceptance Checklist

- [ ] AC1: 新文件 `artifact-style.md` 存在，frontmatter 有 audience（AI / 开发者）与 scope（四件套字段正文书写纪律，不改字段结构）。
- [ ] AC2: 文件含"讲人话"原则——字段正文要让不懂 butler 内部机制的人也读得懂；内部黑话能用大白话就别用，真要指某机制就讲清楚；并点名几个典型反面词（如 护栏 / 正交 / 高注意力区 / BLUF / fresh-context）。
- [ ] AC3: 文件含"反啰嗦"原则——一律 bullet、嵌套 ≤2 层、不复述模板提示语与上阶段已写内容、宁缺毋滥（没有就写"无"）；升级信号只列名不展开；VERIFY 用 `[x] ACn ✓ 一句话证据` 紧凑式不重抄原文。
- [ ] AC4: 文件给至少一组 before / after 对照例，直观可照抄。
- [ ] AC5: 文件写明边界——与四 schema（字段结构）各管各的、与对话层两规则分层（本口径管产物文件层）。
- [ ] AC6: 四个 schema 的编写规则各加一行指针指向 `artifact-style.md`，措辞用"必须 / 应"。
- [ ] AC7: `rule-card.md` 新增一条紧凑"产物书写"口径，与新文件正文口径一致、不矛盾。
- [ ] AC8: `Coder/README.md` 完成注册——目录结构列出新文件、读取顺序提及、规则目录说明加一行分工。
- [ ] AC9: 本迭代自己的四件套即按新口径书写（讲人话、不啰嗦），作为 dogfood 证据。
- [ ] AC10: 本仓 CLAUDE.md 五约束自检通过（分层不混 / 产物链字段未动 / 新文件已注册 / rule-card 与正文单一来源不双写矛盾 / frontmatter 合规）。

# Verification Method

- AC1 / AC2 / AC3 / AC4 / AC5: 读 `artifact-style.md` 核对各节齐全；grep 反面词清单与 before/after 块在位。
- AC6: grep 四个 schema 均命中 `artifact-style`。
- AC7: grep `rule-card.md` 命中新口径节；比对措辞与新文件一致。
- AC8: grep `Coder/README.md` 三处（目录结构 / 读取顺序 / 分工说明）均命中。
- AC9: 通读本迭代 CONCEPT / AC_LIST / TECH_PLAN / VERIFY，确认无黑话堆砌、无整段重述。
- AC10: 对照本仓 CLAUDE.md 五条逐项自检，写进 VERIFY 的 Gate Coverage。

# Open Questions / Risks

- 风险：口径靠会话起始读取 + 遵守，没有 hook 强制——和 identity / presentation-protocol 一样都这样，可接受。
- 风险："讲人话 vs 必要的机制名"边界靠语义判断，有模型自由度——用"能用大白话就别用 + before/after 例"兜底。
