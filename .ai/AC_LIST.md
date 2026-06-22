---
状态: ack-frozen
ACK 日期: 2026-06-22
---

# Goal
- 补一条常驻「对话输出呈现协议」，把 P1-P3 方案/分析/选项类对话输出统一为「结论先行 + 统一标号 + 选项表格」，默认固定 + 弹性、仅管较长输出；与 `delivery-summary §8`（P5 交付摘要散文化）分场景共存。

# In Scope
1. 新增 `Coder/00_System_Prompt/presentation-protocol.md`：定义适用范围、结论先行、统一标号（可执行口径）、选项表格、概念后置、收尾下一步、弹性豁免、与 §8 边界、标准骨架样例。
2. 入口接线：`identity.md §2`、`logic-protocol.md §1.1` 读取顺序、`Coder/README.md`（目录 + 读取顺序 + 分工）。
3. 高注意力区落地：`templates/rule-card.md` 新增精简「输出呈现」节。
4. 边界互指与人类指南：`delivery-summary.md §8` 加一句边界互指；`HUMAN_GUIDE.md` 提一句。

# Out of Scope
- 不改产物文件四 schema 字段（呈现层与产物层正交）。
- 不约束简短问答、纯澄清、单点确认、进度汇报（弹性豁免）。
- 不动 P5 交付摘要的 §8 散文化口径（只加边界互指，不改其风格）。
- 不切版本（累积到下次切版）。

# Acceptance Checklist

## A. 协议文件（核心）
- [ ] AC1: 新增 `Coder/00_System_Prompt/presentation-protocol.md`，frontmatter 含 audience（AI / 开发者）与 scope（对话层方案/分析/选项呈现，非产物文件、非简短问答）。
- [ ] AC2: 定义**适用范围**——明确「适用：P1-P3 方案提案/选项对比/分析说明等较长输出」与「不适用：简短问答/纯澄清/单点确认/进度汇报/P5 交付摘要（走 §8）」。
- [ ] AC3: **结论先行（BLUF）**条款——开头先给一句话结论/建议，再展开依据；不得用大段背景概念开场。
- [ ] AC4: **统一标号**条款给**可执行口径**——无序要点用 `-`；有序步骤用 `1. 2. 3.`；不得用字母标号 `A) B)` / `a) b)` 作列表层级；多级嵌套用缩进 `-`、不混标号体系。
- [ ] AC5: **选项表格化**条款——≥2 个方案/选项对比时用表格（如「方案 | 优势 | 代价/取舍」固定列），不用并列长段落。
- [ ] AC6: **概念后置 + 收尾下一步**条款——决策/建议前置、概念解释精简后置；方案输出结尾给明确「建议 / 下一步」。
- [ ] AC7: **弹性条款**——默认套骨架，但 AC2 豁免清单内的输出不强行套；强度为「默认固定 + 弹性」，显式写明避免僵硬。
- [ ] AC8: **与 §8 边界**——协议内显式声明：§8 管 P5 最终交付摘要（散文、禁编号），本协议管过程方案/选项呈现（结构化、统一标号、表格），按场景分工、互不覆盖。
- [ ] AC9: 协议内给一个**标准骨架样例**（结论 → 关键点 → 选项表 → 建议/下一步），可直接套用；样例本身遵守本协议（自洽）。

## B. 接线与高注意力区
- [ ] AC10: `identity.md §2 输出风格` 增一条指针，引用 `presentation-protocol.md` 作为方案/分析输出的呈现规范。
- [ ] AC11: `logic-protocol.md §1.1 基础读取顺序` 把 `presentation-protocol.md` 纳入 00_System_Prompt 读取序列。
- [ ] AC12: `Coder/README.md` 三处登记——目录结构（00_System_Prompt 下列出新文件）、读取顺序、规则目录/分工说明各加该协议。
- [ ] AC13: `templates/rule-card.md` 新增精简「输出呈现」节（结论先行 + 统一标号 + 选项表格 + 弹性 + 仅管方案/分析），与协议口径一致、措辞精炼（不显著膨胀规则卡体量）。

## C. 边界互指与人类指南
- [ ] AC14: `delivery-summary.md §8` 加一句边界互指——P5 交付摘要走 §8 散文口径，过程方案/选项呈现走 `presentation-protocol.md`，两者分工。
- [ ] AC15: `HUMAN_GUIDE.md` 提一句：方案/选项输出有统一呈现格式（结论先行 + 表格），便于阅读。

## D. 一致性与零改动护栏
- [ ] AC16: 全仓口径一致——「过程方案呈现 = 结论先行/统一标号/表格」与「P5 交付摘要 = §8 散文」处处分工清晰，无任一处把两者混为一谈或自相矛盾。
- [ ] AC17: 零改动护栏——产物链四 schema 字段、hook 脚本与契约、`VERSION`/`CHANGELOG.md`、迭代/里程碑/版本机制、各扩展模块、`deliveries/` 历史未被改动（`git diff` 确认）。
- [ ] AC18: 未破坏 `CLAUDE.md` 五约束——分层未混（协议归 00_System_Prompt SOP Core）、产物链未动、新增文件已在 `Coder/README.md` 目录 + 读取顺序注册、措辞用「必须/不得/应」、frontmatter 标 audience/scope。

## E. 收口
- [ ] AC19: ITER-0011 四件套快照归档 `.ai/iterations/ITER-0011/`，写 `deliveries/ITER-0011-<slug>.md` 及同名 `.html`（沿用 ITER-0010 起的固定格式视图），台账置 closed + 收口日期 + 交付链接，`current: none`。

# Verification Method
- AC1-AC9: 读 `presentation-protocol.md`，逐条确认 frontmatter、适用/豁免范围、BLUF、标号可执行口径、表格、概念后置、弹性、§8 边界、骨架样例俱全且自洽。
- AC10-AC13: grep `identity.md`/`logic-protocol.md`/`Coder/README.md`/`rule-card.md` 命中协议引用与读取顺序登记。
- AC14-AC15: grep `delivery-summary.md`/`HUMAN_GUIDE.md` 命中边界互指与呈现格式说明。
- AC16: 全仓 grep「呈现/§8/交付摘要」相关句，人工核对过程 vs P5 分工一致、无矛盾。
- AC17: `git diff --stat` 确认护栏文件零改动。
- AC18: 对照 CLAUDE.md 五约束逐条自检；确认新文件已注册。
- AC19: 收口三步执行后核台账、归档目录、`deliveries/ITER-0011-*.{md,html}` 双产出齐全。

# External References
- 无（本轮不涉及外部 API 文档 / 设计稿）。

# Open Questions / Risks
- 协议放 00_System_Prompt 独立文件（倾向）vs 扩 identity §2：P3 定稿，倾向独立文件（可被 rule-card 引用、放高注意力区）。
- 弹性条款边界（什么算「较长输出」须套骨架）靠语义判断、无机械门禁——与既有对话层规则（§8）同源同险，靠规则纪律。
- rule-card 新增节须控制体量（规则卡约 800 tokens 预算），精简表达。
- 协议是行为约束、无 hook 强制——靠会话起始读取 + 遵守，与 identity/logic-protocol 同源。
