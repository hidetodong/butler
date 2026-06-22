# Goal
- 支撑 AC1–AC19：新增 `Coder/00_System_Prompt/presentation-protocol.md`（对话输出呈现协议）并接线到入口/高注意力区/人类指南，把 P1-P3 方案/分析/选项输出统一为「结论先行 + 统一标号 + 表格」，默认固定 + 弹性、仅管较长输出，与 §8 分场景共存。

# Files / Modules to Change

| # | 文件 | 改动 | 覆盖 AC |
|---|---|---|---|
| 1 | **新增** `Coder/00_System_Prompt/presentation-protocol.md` | 协议正文：8 节（见 Interface） | AC1–9 |
| 2 | `Coder/00_System_Prompt/identity.md` | §2 输出风格加一条指针引用协议 | AC10 |
| 3 | `Coder/00_System_Prompt/logic-protocol.md` | §1.1 基础读取顺序纳入协议（identity 之后、lifecycle 之前） | AC11 |
| 4 | `Coder/README.md` | 目录结构（00 下列出）+ 读取顺序 + 规则目录说明三处登记 | AC12 |
| 5 | `templates/rule-card.md` | 新增精简「## 输出呈现」节 | AC13 |
| 6 | `Coder/20_Workflow_Lifecycle/delivery-summary.md` | §8 加一句边界互指 | AC14 |
| 7 | `HUMAN_GUIDE.md` | 提一句方案输出统一呈现格式 | AC15 |

零改动护栏（AC17）：四件套 schema、`templates/hooks/`、`VERSION`、`CHANGELOG.md`、iteration/milestone/versioning-schema、扩展模块、`deliveries/` 历史 + ITER-0010 的 `delivery.html.template` 一律不动。

# Interface / Contract

## `presentation-protocol.md` 正文结构（8 节）
1. **目标**：消除标号随机/概念堆叠，统一过程方案呈现、提升易读性。
2. **适用范围**（AC2）：适用 = P1-P3 方案提案/选项对比/分析说明等较长输出；不适用 = 简短问答/纯澄清/单点确认/进度汇报/P5 交付摘要（走 §8）。
3. **结论先行 BLUF**（AC3）：开头一句话结论/建议；不得大段背景概念开场。
4. **统一标号**（AC4，可执行口径）：无序 `-`；有序 `1. 2. 3.`；禁字母标号 `A)`/`a)` 作层级；多级嵌套用缩进 `-`、不混体系。
5. **选项表格化**（AC5）：≥2 方案对比用表格，固定列建议「方案/选项 | 优势 | 代价·取舍」（可按场景增列）。
6. **概念后置 + 收尾下一步**（AC6）：决策/建议前置、概念精简后置；结尾给明确「建议/下一步」。
7. **弹性条款**（AC7）：默认套骨架，§2 豁免清单不强行套；强度=默认固定+弹性，显式防僵硬。
8. **与 §8 边界 + 标准骨架样例**（AC8/AC9）：声明 §8 管 P5 交付摘要散文、本协议管过程结构化呈现、分场景；附可套用骨架（结论 → 关键点 → 选项表 → 建议/下一步），样例自身遵守本协议。

## 接线契约
- `identity.md §2`：末尾加一条 bullet「方案/分析/选项类对话输出遵循 `presentation-protocol.md`（结论先行 + 统一标号 + 表格）」。
- `logic-protocol.md §1.1`：读取顺序在 `identity.md` 与 `logic-protocol.md` 之后插入 `00_System_Prompt/presentation-protocol.md`（作为第 3 项，原 3/4 顺延）。
- `Coder/README.md`：① 目录结构 txt 的 `/00_System_Prompt` 下加一行；② 读取顺序加一项；③ 规则目录说明「00_System_Prompt/」描述补「+ 对话输出呈现协议」。
- `rule-card.md`：在「## 角色」后或「执行纪律」前插入「## 输出呈现」精简节（≤6 行）。
- `delivery-summary.md §8.5`（与 §4 的关系处）或 §8.1：加一句指向 presentation-protocol 的边界互指。

# State / Boundary
- **呈现层与产物层正交**：协议只管对话框呈现，不碰任何产物文件 schema 字段。
- **与 §8 分场景**：§8 = P5 最终交付摘要（散文、禁编号、3-6 句）；本协议 = 过程方案/选项（结构化、统一标号、表格）。两侧各自声明分工，避免「交付摘要也被要求表格化」或「方案也被要求散文化」的冲突。
- **弹性边界**：豁免清单（短问答/澄清/单点确认/进度汇报）显式列出；「较长输出」靠语义判断、无机械门禁。
- **不在范围**：不给 hook 强制、不改 §8 散文口径、不约束简短交流、不发版。

# Design Decisions
1. **独立文件放 `00_System_Prompt/`**（已与用户对齐）：而非扩 identity §2——可被 rule-card 单独引用、放最高注意力区、可独立演进。identity §2 只留一条指针。
2. **进 rule-card（高注意力区）是关键**：规则卡会内联到目标项目 CLAUDE.md，是 AI 实际高频读到处；只写进 00 层正文而不进 rule-card，规则会「写了但不被遵守」。故 AC13 必做且口径与正文一致。
3. **可执行标号口径而非模糊指引**：明确 `-`/`1.`/禁字母，杜绝「请统一」式空话——这正是当前问题（即兴）的反面。
4. **附标准骨架样例**：给一个可直接套用的骨架，降低每次即兴成本、提高一致性；样例自身遵守协议（自洽自证）。
5. **协议自洽**：本规范讲「如何呈现」，其正文与样例自身就是良好呈现的示范。
6. **active profiles 约束**：无（Markdown 规则仓库）。

# Execution Steps
1. **写协议**（AC1–9）：新建 `presentation-protocol.md`，8 节齐全 + frontmatter（audience/scope）+ 骨架样例。
2. **接线入口**（AC10–12）：identity §2 指针、logic-protocol §1.1 读取顺序、Coder/README 三处登记。
3. **高注意力区**（AC13）：rule-card 新增「## 输出呈现」精简节。
4. **边界互指 + 指南**（AC14–15）：delivery-summary §8 边界句、HUMAN_GUIDE 一句。
5. **P5 验证**（AC1–18）：逐 AC grep + 读协议自洽核对 + `git diff --stat` 护栏。
6. **收口**（AC19）：四件套快照 `.ai/iterations/ITER-0011/`；写 `deliveries/ITER-0011-presentation-protocol.md` + 同名 `.html`（用 ITER-0010 模板填槽）；台账 closed + `current: none`。

# Verification Plan
- AC1–9：读 `presentation-protocol.md`，逐节核对 frontmatter / 适用+豁免 / BLUF / 标号可执行 / 表格 / 概念后置+下一步 / 弹性 / §8 边界 / 骨架样例，且样例遵守协议。
- AC10–13：grep identity/logic-protocol/README/rule-card 命中协议引用、读取顺序、输出呈现节。
- AC14–15：grep delivery-summary §8 / HUMAN_GUIDE 命中边界互指与呈现说明。
- AC16：全仓 grep 呈现/§8 分工句，人工核对无矛盾。
- AC17：`git diff --stat` 确认护栏文件零改动。
- AC18：对照 CLAUDE.md 五约束自检；确认新文件在 README 目录+读取顺序均注册。
- AC19：收口三步后核台账、归档、`deliveries/ITER-0011-*.{md,html}` 齐全且 HTML 可打开。

# Risks / Open Questions
- 协议靠会话起始读取 + 遵守，无 hook 强制——与 identity/logic-protocol 同源同险。
- rule-card 体量预算（约 800 tokens）：新增节须精简（≤6 行），避免规则卡显著膨胀。
- 「较长输出」与豁免边界靠语义判断，存在模型自由度——用「默认套 + 豁免清单」兜底，可接受。
- 无外部参考资料（External References 空）。
