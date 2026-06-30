> 分流: 完整 | 命中升级信号: 多文件改动、跨模块影响、设计取舍 | 2026-06-30

# Goal

- 让四件套（CONCEPT / AC_LIST / TECH_PLAN / VERIFY_REPORT）写出来的内容**讲人话、不啰嗦**。
- 现在四个 schema 只规定填哪些字段，没规定字段里的话该怎么写，于是内容里堆满内部黑话、还动辄把一条事重述好几遍。

# Current Understanding

- 病根：四件套是给 AI 续接用的，但人也会读，而四个 schema 里**一条"内容怎么写"的纪律都没有**（全仓库搜"人话/黑话/注水"只在对话层的两个文件命中）。
- 两类毛病：
  - **黑话泄漏**：字段正文里塞 `护栏`、`正交`、`高注意力区`、`BLUF`、`fresh-context` 这类只有 butler 自己懂的词，外人读不懂。
  - **啰嗦注水**：升级信号每条加一段括号小作文、验证报告把每条 AC 原文重抄一遍、嵌套四五层。
- 想清楚的边界：要治的是"往字段里写的话"，**不是字段结构**。字段名（Goal / AC Status…）、AC 编号、文件路径是跨阶段读取的锚点，必须留着。
- 也想清楚一个坑：当这次任务本身就是在改 butler 内部机制时，正文绕不开 `schema`、`rule-card` 这些词——所以纪律不能是"禁所有 butler 词"，而是"能用大白话就别用黑话；真要指某个机制就讲清楚它"。

# Constraints

- 字段结构不动：四个 schema 的必填字段、模板骨架一字不改，产物链逐阶段读取不受影响。
- 单一来源：新口径只写一份，四个 schema 各放一行指针引用它，不在四处各抄一遍（避免双写漂移）。
- 必须同步写进浓缩规则卡 `rule-card.md`（AI 每次最先读到的那一份），否则规则写了也读不到——上一版 CONCEPT 自己就栽在这点上。
- 守本仓 CLAUDE.md 五约束：新文件要在 `Coder/README.md` 双注册、措辞用"必须/不得/应"、frontmatter 标 audience / scope。

# Impact Scope

- 会改 / 新增：
  - 新增 `Coder/20_Workflow_Lifecycle/artifact-style.md`（四件套书写口径，本迭代核心产物）。
  - 四个 schema（concept / acceptance / tech-plan / verify）各在编写规则里加一行指针。
  - `templates/rule-card.md` 加一条紧凑口径。
  - `Coder/README.md` 注册新文件。
- 明确不影响：四 schema 的字段语义、lifecycle 的分流格式、hook 体系、迭代 / 里程碑 / 版本机制、各扩展模块、`deliveries/` 历史交付、已归档的历史四件套（不回填）。

# Project Type / Active Profiles

- 项目形态：Markdown 规则仓库（butler 自己），改的是协作 SOP 规则本身。
- 命中 Domain / Stack Profiles：无，只按通用 SOP + 本仓 CLAUDE.md 编辑约束推进。

# Open Questions

- 新口径放 20 层独立文件（倾向，和对话层的 presentation-protocol 对称）还是塞进某个 schema —— 倾向独立文件，P3 定。
- 要不要给一段 before / after 对照例 —— 倾向给，最有说服力，P3 定。
- 以上是落点细节，不改 Goal，进 P2 不阻塞。
