# TECH_PLAN — ITER-0028（MILE-0003 R2）

> 监督态自驱（非 `/dangerous`）：本产物由用户"继续"委托、模型自驱产出，P5 起独立复核守质量（ITER-0028，2026-07-06）。

# Goal

- 支撑 AC1–AC8：把 `project-digest-schema.md` 整篇改写为 `.ai/project/` 知识文件夹契约（结构 + INDEX + topic 集 + 边界 + 密度 + 折叠模型声明 + 受控扩展 + 骨架 + 关系），README 描述行改准。

# Files / Modules to Change

**改写（整篇）**

- `Coder/40_Context_Management/project-digest-schema.md` — 新结构：frontmatter（scope 改文件夹）+ §1 定位（知识文件夹 = 整体/积分、越补越全、冷启动第一读 00_INDEX、四产物边界表）+ §2 核心哲学（三条矛盾消解 + 最大风险）+ §3 文件夹结构 + 00_INDEX 契约 + 推荐 topic 集 + §4 每份边界 + §5 写作密度（digest-and-point + 校准样例）+ §6 折叠维护模型（声明 + 强制留 R3 标注）+ §7 受控扩展登记 + §8 模板骨架（00_INDEX + topic 骨架）+ §9 与其他规则关系（前向指针 R3/R5/R6/R8）。→ AC1–AC8

**改（一行描述）**

- `Coder/README.md` — 分文件说明里 `project-digest-schema.md` 那条：`.ai/PROJECT.md 格式契约` → `.ai/project/ 知识文件夹格式契约`，反映文件夹 + 保留"冷启动第一读 00_INDEX"（读序实际切换 R5）。→ AC8

**收口前滚（close 步④，按判据）**

- `.ai/PROJECT.md`「关键长期决策与不变量」— 若判据成立，记一句"项目全貌产物契约升级为知识文件夹（schema 已定，butler 自身 R8 适配）"。→ 非 AC，收口仪式

# Interface / Contract

- **知识文件夹结构**：`.ai/project/00_INDEX.md`（入口）+ 主题文件（`identity.md` / `architecture.md` / `capabilities.md` / `invariants.md` / `constraints.md` / `debt.md` / `frontier.md`，推荐核心集、可受控扩展）。
- **00_INDEX 契约**：冷启动第一读；含①一段话项目是什么 ②文件夹读序/地图 ③topic 登记表（每 topic 一行 + 边界）。新 topic 必登记（无隐式依赖）。
- **密度 = digest-and-point**：每项 = 名 + 它到底干什么 + 真源指针；已有真源（如 `Coder/README.md` / `architecture-overview`）不逐字抄，只摘当前全貌 + 补真源没有的现状/成熟度层 + 指针。
- **折叠模型（声明）**：收口时本迭代 delta 按主题路由折进对应文件、overwrite 当前真相、成本∝改动量。**强制化 + 漂移自检不变量的接线**=后续路线项 R3，本 schema 不实现。

# State / Boundary

- 落点 `Coder/40_Context_Management/`（不变）；文件名不改（沿用 `project-digest-schema.md`）。
- **不改**：`.ai/PROJECT.md` 现结构、`iteration-schema §5.5`、`milestone-schema §7.4`、`context-persistence §6`、`mcv-deployment`、`migrations/`、P1–P5 状态机、四件套字段、hook、VERSION。
- 归属 MILE-0003 R2；不预占 R3–R8。

# Design Decisions

- **DD1（哲学切换写进 §2 独立成段）**：把"薄索引→知识地图"的反转 + 三条矛盾消解 + 最大风险显式成 §2，不埋在定位里——这是本迭代的价值内核，也是防"腐坏的完整"的认知护栏。→ AC5
- **DD2（折叠模型声明、强制留 R3）**：schema §6 只**声明**折叠维护模型（what），强制化（泛化收口步为必做）+ 漂移自检（扩一致性自检）明标"R3 接线"。理由：R2/R3 边界据 MILESTONE 路线图分明；schema 定契约、收口步定强制是两件事。防"要求了没强制"的假绿由如实标注化解。→ AC6/AC7
- **DD3（文件名不 rename）**：沿用 `project-digest-schema.md`，改名连锁 5+ 处引用失效、违最小实现纪律（`implementation-discipline §4`：最小改动定位）；内容改、名不动，rename 留后续 tidy。→ AC8
- **DD4（前向指针不越位）**：§9 关系段用"待后续路线项 R3/R5/R6/R8"如实标注下游接线，本轮一字不改那些文件；`git diff` 兜底证明。→ AC7
- **DD5（topic 集照预研定稿）**：核心 topic 集直接采预研 §7 草案（identity/architecture/capabilities/invariants/constraints/debt/frontier），标"推荐核心、可受控扩展"，不自创新主题（保真预研、避免未拍板设计混入）。→ AC3
- **DD6（butler 自身暂态不一致如实说）**：schema 定"采用知识文件夹时的契约"；butler 自身 `.ai/PROJECT.md` 仍单文件、R8 适配；§1 / §9 说清暂态，不制造"schema 生效但自身没跟上"的隐性矛盾。→ AC1/AC7

# Execution Steps

- [ ] T1 整篇改写 `project-digest-schema.md`（§1–§9）→ AC1–AC8
- [ ] T2 改 `Coder/README.md` 描述行 → AC8
- [ ] T3 自检：读全文逐 AC 核 + 对预研 HTML §4/§5/§7 保真 + `git status --short` 证明未触 R3/R5/R6/R8 文件、未 rename → AC7/AC8
- [ ] T4 P5 起独立复核子 agent（fresh-context，验证者≠实现者，重点预研保真 + scope 边界）→ 全 AC

# Verification Plan

- AC1–AC6: 读改写后正文逐条核要素 + 对预研设计保真。
- AC7: 读 §9 前向指针 + `git status --short` 证明 iteration-schema/milestone-schema/context-persistence/mcv-deployment/migrations/.ai/PROJECT.md 结构未在改动集。
- AC8: 读 frontmatter + 骨架 + README 描述行；`git status` 核文件集=schema + README + .ai 台账，无 rename、无越界。
- P5 独立复核逐 AC + 预研保真 + scope 边界 + 对抗探测（越界改 R3/R5 / 伪强制折叠 / 密度自相矛盾 / 历史层复活 / topic 自创未拍板）。

# Risks / Open Questions

- **伪强制风险**：§6 折叠模型若读成"已强制"→ DD2 明标"R3 接线"+ 独立复核核。
- **暂态不一致**：文件夹契约 vs 自身单文件 PROJECT.md → DD6 §1/§9 说清、butler R8 适配。
- **越界风险**：改写时手滑改了 R3/R5 文件 → DD4 前向指针 + T3 `git status` 兜底。
- 已定：topic 集照预研 §7；折叠只声明强制留 R3；文件不 rename。
