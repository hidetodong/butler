> 分流: 完整 | 命中升级信号: 契约变更（新增对话层呈现行为契约，贯穿各阶段输出）、跨模块影响（影响 P1-P3 所有方案/分析对话输出 + 须与 delivery-summary §8 划清边界）、多文件改动（新增规范文件 + identity/logic-protocol/rule-card/README/HUMAN_GUIDE 接线 ≥5）、设计取舍（落点：新建 00 层文件 vs 扩 identity §2；与 §8 边界） | 2026-06-22

# Goal

- 解决「每次输出方案时格式不固定、不易读」的体验问题：标号忽 ABC 忽 123 忽 a)、开场堆大段概念。
- 补一条**常驻的「对话输出呈现协议」**，把 P1-P3 的方案/分析/选项类对话输出统一为：**结论先行 + 统一标号 + 选项表格化**；默认固定、按内容弹性、仅管较长输出。
- 与现有 `delivery-summary.md §8`（P5 交付摘要散文化）**分场景共存、不打架**。

# Current Understanding

- **根因**：butler 现有所有 schema 只约束**产物文件**字段（CONCEPT/AC_LIST/TECH_PLAN 写什么），从未约束**对话框里怎么把方案呈现给人看**。唯一的对话层规则是 `delivery-summary §8`，且只管 P5 交付摘要那一刻。其余阶段（P1 分析、P2 AC 呈现、P3 方案、选项对比）的对话输出全靠模型即兴 → 标号随机、概念堆叠、不易读。
- **已与用户锁定的三个设计参数**（本轮 AskUserQuestion 裁定）：
  1. **呈现骨架 = 结论先行 + 选项表格（BLUF）**：开头一句话结论/建议，再用统一标号要点展开，多方案对比一律用表格。
  2. **约束强度 = 默认固定 + 弹性**：定一套默认骨架，但允许按内容繁简调整——短回答/纯澄清/单点确认不强行套骨架，避免僵硬。
  3. **作用范围 = 仅方案/分析/选项**：只约束 P1-P3 方案提案、选项对比、分析说明这类较长输出；简短问答与进度汇报不受约束。
- **预期产出**：一条新规则文件（对话输出呈现协议）定义骨架/标号/表格/弹性条款与 §8 边界，并接线到入口规则（identity / logic-protocol）、浓缩规则卡（rule-card，高注意力区，影响实际遵守）、人类指南与 Coder/README 注册。

# Constraints

- **显性约束**：
  - 协议只管**对话层呈现**，**不改产物文件 schema**（CONCEPT/AC_LIST/TECH_PLAN/VERIFY 字段一字不动）——呈现层与产物层正交。
  - 与 `delivery-summary §8` **边界清晰**：§8 管 P5 最终交付摘要（散文、禁编号、3-6 句）；本协议管**过程中**的方案/选项呈现（结构化、统一标号、表格）。两者按场景分工，互不覆盖、互不矛盾。
  - **弹性内建**：默认骨架 + 显式「不套骨架」豁免清单（短问答/澄清/进度汇报），防止把轻量交流变重、防僵硬。
  - 统一标号必须给**可执行的具体规则**（如：无序用 `-`、有序用 `1.`、禁字母标号做层级），不能只说「请统一」这种模糊话。
- **隐性约束**：
  - 不破坏分层：这是 SOP Core 通用输出治理，归 `00_System_Prompt/`（系统级输出协议层），不混进 Domain Profile 或 Business Extension。
  - 高注意力区落地：必须进 `rule-card.md`（会内联到目标项目 CLAUDE.md），否则规则写了但 AI 实际读不到、不遵守。
  - CLAUDE.md 编辑五约束：新增规则文件须在 `Coder/README.md` 目录结构 + 读取顺序注册；措辞用「必须/不得/应」；frontmatter 标 audience/scope。
  - 协议本身要简洁、可执行，且**自洽**（一份规范「如何呈现」的规则，自己也要做到良好呈现）。

# Impact Scope

- **会改/新增**：
  - **新增** `Coder/00_System_Prompt/presentation-protocol.md`（对话输出呈现协议，本迭代核心产物）。
  - `Coder/00_System_Prompt/identity.md`（§2 输出风格加指针引用新协议）。
  - `Coder/00_System_Prompt/logic-protocol.md`（§1.1 基础读取顺序纳入新协议）。
  - `Coder/README.md`（目录结构 00_System_Prompt 下登记 + 读取顺序登记 + 规则分工一行）。
  - `templates/rule-card.md`（新增精简「输出呈现」节，高注意力区）。
  - `HUMAN_GUIDE.md`（提一句：方案输出有统一呈现格式）。
  - 可能微调：`delivery-summary.md §8`（加一句与本协议的边界互指，确保两侧都声明分工）。
- **明确不影响**（零改动护栏）：
  - 产物链四件套 schema（concept/acceptance/tech-plan/verify）字段语义。
  - hook 体系（phase_gate/ledger_status）、迭代/里程碑/版本治理机制。
  - `VERSION`/`CHANGELOG.md`（本轮不发版，累积到下次切版，预计 MINOR：新增可选输出协议、向后兼容）。
  - 各扩展模块（ideation/loop/review/dangerous/preference）与 ITER-0010 的 HTML 视图。
  - `deliveries/` 历史交付。

# Project Type / Active Profiles

- 项目形态：**Markdown 规则仓库**（butler 自身），编辑协作 SOP 规则本身。
- 命中 Domain / Stack Profiles：**无**，仅按通用 SOP + 本仓库 CLAUDE.md 编辑约束推进。

# Open Questions

- 落点最终定在 `00_System_Prompt/` 独立文件（倾向）还是扩 `identity.md §2`——倾向独立文件（可被 rule-card 引用、可单独演进、放高注意力区），P3 定稿。
- 标号统一的精确口径（无序 `-` / 有序 `1.` / 禁字母层级 / 嵌套缩进）在 P2 AC 与 P3 规范正文定稿。
- 是否需要在协议里给一个「标准骨架样例」（结论 → 关键点 → 选项表 → 建议/下一步）作为可套用模板——倾向给，P3 定。
- 以上均为方案层细节，不改 Goal 与已锁定的三参数，进入 P2 不阻塞。
