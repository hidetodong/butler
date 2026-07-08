# TECH_PLAN — ITER-0034（MILE-0003 R8 · dogfood 迁 .ai/project/ + 切 v2.0.0）

> 监督态自驱（用户"继续 / 开始"接力，非 `/dangerous`）。目标见 CONCEPT、验收见 AC_LIST，不重述。段A（迁移 + 对齐，`feat`）先执行；段B（切版，`chore(release)`）切 tag 前另请用户放行。

## 设计决策（DD）

- **DD1 · 主题拆分照 R2 §3 推荐集**（AC1/AC2）：直接采用 `project-digest-schema §3` 的 7 主题（identity/architecture/capabilities/invariants/constraints/debt/frontier），不自造结构。旧单文件 6 段按 CONCEPT 映射表路由；`capabilities`（现状命令 + SOP + 驻留工具）与 `frontier`（当前形态 + 下一瓶颈）是 R2 新增层、单文件没有，需从现状**新写**（源自代码现实，非搬旧文）。
- **DD2 · 已有真源只摘不抄**（AC3，R2 §5 明点最吃劲处）：`architecture` 的目录树与分层说明真源在 `Coder/README.md` / `architecture-overview.md`——知识文件夹**只摘全貌 + 补成熟度层 + 留指针**，不复制目录。`capabilities` 的命令/引擎细节指各扩展模块，不搬引擎正文。校准样例照 §5 line 82–91。
- **DD3 · 对齐现实=挪例子不改逻辑**（AC7，红线）：两态规则（`context-persistence §6` 读序、`mcv-deployment §2` 部署、`migration-schema`）的**单文件分支保留**给 R6 前老项目；只把其中"含 butler 自身 / butler 仍单文件"的**举例**翻成"butler 已迁文件夹态"。`project-digest-schema §9` 的 R8 指针 待→已、暂态说明改"已完成"。改的是**例子与状态叙述**，非规则分支。
- **DD4 · 迁后 butler 转文件夹态、状态文件必须翻到位**（AC6/AC9，对照 R6 MF-1 教训）：`task-state` 冷启动入口 + `.ai/project/` 各处自述都按"butler 现为文件夹态"写；第 6 不变量对 butler 自身**转适用**、收口步④按主题**必做**折叠。走查从 `00_INDEX` 出发不踩已删的 `PROJECT.md`。
- **DD5 · 两提交严格分离**（AC14，`versioning §5.3`）：段A `feat` 只装 `.ai/project/`+删 `PROJECT.md`+对齐例子+`.ai/` 产物；段B `chore(release)` 只装 VERSION/CHANGELOG/`migrations/v2.0.0.md`/里程碑收口。`git status` 核两次提交内容不交叉。
- **DD6 · migration 实例照 R6 备的形态**（AC12）：`migrations/v2.0.0.md` = `[split]`（PROJECT.md→.ai/project/，起始态校验 + 冲突即停）+ `[regen-claude]`（区间 `rule-card` 改过）+ `[restamp]`；typed 步骤幂等。先 `git log v1.7.0..HEAD` 核 hooks / schema 字段有无变更决定要不要 `[sync-hooks]`/`[add-field]`，不需则显式写"无"。
- **DD7 · dogfood 说人话**（AC17）：四件套 + `.ai/project/` 全部主题 + 交付按 R7 三条自检，写"知识文件夹要真懂项目"的迭代不许自己堆黑话。

## 影响面（段A · 章节级）

| 文件 | 改动 | AC |
|---|---|---|
| `.ai/project/00_INDEX.md` | 新建（入口三块） | AC1 |
| `.ai/project/{identity,architecture,capabilities,invariants,constraints,debt,frontier}.md` | 新建 7 主题（迁 + 补两层） | AC2/3/4 |
| `.ai/PROJECT.md` | 删除（内容已迁） | AC5 |
| `.ai/task-state.md` | 冷启动入口 → `00_INDEX`、butler 转文件夹态 | AC6 |
| `Coder/20_Workflow_Lifecycle/mcv-deployment.md §2` | butler 自身例子 → 已迁 | AC7 |
| `Coder/40_Context_Management/context-persistence.md §6` | 单文件分支 butler 举例 → 已迁（分支逻辑留） | AC7 |
| `Coder/40_Context_Management/project-digest-schema.md §9` | R8 指针 待→已、暂态说明改完成 | AC7 |
| `Coder/20_Workflow_Lifecycle/milestone-schema.md` | 若点名 butler 单文件则对齐（先核） | AC7 |
| `Coder/README.md` | butler 自身现状 / 读序描述对齐（若有） | AC8 |

## 影响面（段B · 切 tag 前请用户放行）

| 文件 | 改动 | AC |
|---|---|---|
| `VERSION` | 1.7.0 → 2.0.0 | AC10 |
| `CHANGELOG.md` | 加 `## [2.0.0]` 聚合 ITER-0026~0034 + 收口 MILE-0003 | AC11 |
| `migrations/v2.0.0.md` | 新建（`[split]`+`[regen-claude]`+`[restamp]`） | AC12 |
| `.ai/MILESTONE.md`→`milestones/MILE-0003/`、`deliveries/milestones/MILE-0003-*` | 里程碑收口快照 + 聚合交付 | AC13 |
| `.ai/MILESTONES.md` | MILE-0003 翻 closed + 补迭代 0033/0034 | AC13 |

**不碰**（AC16）：两态规则的单文件分支逻辑、R2 结构契约 / R3 折叠语义 / R5 读序逻辑 / R7 说人话定义、hook 代码、四件套字段结构、`Learner/` `Composer/`。

## Execution Steps（可勾选）

**段A · 迭代**
- [ ] S1 · 建 `.ai/project/00_INDEX.md`（入口三块 + 主题登记表）→ AC1
- [ ] S2 · 写 7 主题文件（identity/architecture/capabilities/invariants/constraints/debt/frontier；迁 6 段 + 补两层、已有真源只摘不抄、说人话）→ AC2/3/4/17
- [ ] S3 · 删 `.ai/PROJECT.md` + 全仓核无残留活引用 → AC5
- [ ] S4 · 翻 `task-state` 冷启动入口 + butler 文件夹态 → AC6
- [ ] S5 · 对齐现实：`mcv-deployment §2` / `context-persistence §6` / `project-digest §9` / `milestone-schema`(先核) 里 butler 自身例子（分支逻辑留）→ AC7
- [ ] S6 · `Coder/README.md` butler 现状对齐（若有）+ scope 守恒核对（`git status`）→ AC8/16
- [ ] S7 · dogfood 冷启动走查（从 `00_INDEX` 定位任一主题、指针不踩空、第 6 不变量不漂移）→ AC9
- [ ] S8 · P5 独立复核（干净上下文子 agent，对抗式：无遗漏迁 / 不逐字抄 / 单文件分支未误删 / 指针不踩空 / 两提交可分）
- [ ] S9 · 段A 原子收口（归档四件套 + 交付 md+html + 翻台账 + **文件夹态按主题折叠** + 6 不变量自检[第 6 条对 butler 转适用]）+ `feat` 提交

**段B · 发布（切 tag 前请用户放行）**
- [ ] S10 · `git log v1.7.0..HEAD` 核 hooks/schema 有无变更 → 定 migration typed 标签集
- [ ] S11 · VERSION 2.0.0 + CHANGELOG [2.0.0] + `migrations/v2.0.0.md`
- [ ] S12 · 收口 MILE-0003（MILESTONE 快照 + 聚合交付 + MILESTONES closed）
- [ ] S13 · 切版前 6 不变量预检 → **请用户放行** → `chore(release)` 提交 + `git tag v2.0.0` → 切版后三处版本载体对齐核对

## 验证策略

全 auto·可靠（规则 / 文档 / 台账）：每 AC 读产物核契约 + `git`/`grep` 核守恒。核心对抗点＝**迁移无遗漏 + 不逐字抄真源**（DD2）+ **单文件分支逻辑未误删**（DD3 红线）+ **迁后指针不踩空**（DD4）+ **两提交内容不交叉**（DD5）。dogfood=冷启动走查 + 四件套/主题过说人话三条。无人测道残余（纯文档、无运行时）。
