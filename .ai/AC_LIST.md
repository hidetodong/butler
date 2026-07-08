---
状态: ack-frozen
ACK 日期: 2026-07-08
迭代: ITER-0034
里程碑: MILE-0003 R8
---

# AC_LIST — ITER-0034（MILE-0003 R8 · butler 自身 dogfood 迁 .ai/project/ + 切 v2.0.0）

> 监督态自驱（用户"继续"接力，非 /dangerous）。验收脊柱贯穿 P4→P5。分**段A 迭代**（AC1–AC9，`feat` 提交）+**段B 发布**（AC10–AC15，独立 `chore(release)`，**tag 前另请用户放行**）。验证=读产物核契约 + `git`/`grep` 核守恒 + dogfood 冷启动走查，确定性可复现（auto·可靠）。

## 段A · 迭代：迁自身 + 对齐现实（`feat`）

### 块1 · 建 `.ai/project/` 知识文件夹（消费 R2 契约）

- **AC1**：新建 `.ai/project/00_INDEX.md`，含 R2 §8 入口三块——一段话"butler 是什么"+ 读序地图（先读哪个主题）+ 主题登记表（每主题一行：名 + 干什么 + 指针）。
- **AC2**：按 P1 主题映射表拆出 7 份主题文件（`identity` / `architecture` / `capabilities` / `invariants` / `constraints` / `debt` / `frontier`），现单文件 `.ai/PROJECT.md` 六段内容**无遗漏**迁入，且补齐 R2 新增的 `capabilities`（现状命令 + SOP + 驻留工具）与 `frontier`（当前形态 + 下一瓶颈）两层。
- **AC3**：密度守 R2 digest-and-point（名 + 它干什么 + 指针），每份有界；**已有真源不逐字抄**——`architecture` 摘全貌 + 补成熟度 + 指 `README`/`architecture-overview`，不复制目录树；无一主题文件把别处真源整段搬来。
- **AC4**：迁入内容**说人话**（承 R7 三条）+ 各主题**只承载当前真相**、不留历史层（R2 overwrite 语义）。

### 块2 · 删旧单文件 + 对齐现实

- **AC5**：`.ai/PROJECT.md` 删除（内容已迁 `.ai/project/`，即 `[split]` 作用于 butler 自身）；全仓无残留指向 `.ai/PROJECT.md` 作为 butler **自身**全貌产物的活引用（两态规则里"单文件项目读 `.ai/PROJECT.md`"的**通用**表述保留给老项目，不算残留）。
- **AC6**：`.ai/task-state.md` 冷启动入口从 `.ai/PROJECT.md` 改 `.ai/project/00_INDEX.md`；butler 自身状态描述转"文件夹态"。
- **AC7**：全仓"butler 仓自身（单文件例子 / R8 前暂态）"的括号例子对齐为"已迁移文件夹态"——含 `mcv-deployment.md`、`context-persistence.md`、`project-digest-schema.md §9`（R8 指针 待→已 + line 149/152）、`milestone-schema.md`（若点名）；**红线**：两态规则的**单文件分支逻辑保留**（老项目仍支持），只挪走 butler 自身作例。
- **AC8**：`Coder/README.md` 中涉及 butler 自身现状 / 读序的描述对齐（若有）；无隐式依赖残留。

### 块3 · dogfood 收口自洽

- **AC9（dogfood 即验收）**：迁完后按 butler 冷启动读序走查——从 `.ai/project/00_INDEX.md` 出发能定位到任一主题、指针不踩空（无指向已删 `PROJECT.md`）、第 6 不变量（知识文件夹漂移）对 butler 自身转适用且当轮不漂移；ITER-0034 收口走**文件夹态**（收口步④按主题折叠进 `.ai/project/`，首次真实 dogfood 折叠）。VERIFY 记录走查结论。

## 段B · 发布 v2.0.0（独立 `chore(release)`，`versioning §6.3`；**tag 前请用户放行**）

- **AC10**：`VERSION` 由 `1.7.0` 改 `2.0.0`；bump 级别 = **MAJOR**（理由：重写冷启动第一读 + 全貌产物契约 + 维护回路，属破坏性、要求老项目迁移，`versioning §2`）。
- **AC11**：`CHANGELOG.md` 加 `## [2.0.0] - <日期>`，聚合 ITER-0026~0034（含独立 ITER-0027）+ 收口 MILE-0003；**只引用**（`deliveries/` / `ITERATIONS.md`）**不复述**，格式随现有条目。
- **AC12**：产 `migrations/v2.0.0.md`（R6 备的文件夹化配方**首次实例**）——含 `[split]`（`.ai/PROJECT.md → .ai/project/`，起始态校验 + 冲突即停退 ACK）+ `[regen-claude]`（区间内 `rule-card` 改过）+ `[restamp]`；每个 typed 步骤**幂等**、格式随现有 `migrations/v1.x.md`；核对并声明是否需 `[sync-hooks]` / `[add-field]`（不需则显式写明无 hook / schema 字段变更）。
- **AC13**：收口 MILE-0003（`milestone-schema §7`）——`MILESTONE.md` 快照进 `milestones/MILE-0003/`、聚合交付 `deliveries/milestones/MILE-0003-*.md`+`.html`、`MILESTONES.md` 台账翻 closed 且含迭代补齐 ITER-0033/0034。
- **AC14**：段A 与段B **两提交分离**（`versioning §5.3`）——段A `feat` 提交**不含** VERSION/CHANGELOG/migration/里程碑收口产物；段B `chore(release)` 提交**不含**规则逻辑改动。
- **AC15**：切版一致性——切版前预检 6 不变量、切版后三处版本载体（`VERSION` / `CHANGELOG` 顶条 / tag）互相对齐；`git tag v2.0.0` **经用户明确放行后**才打。

## 守恒 / 边界

- **AC16**：scope 守恒——**不改**两态规则的单文件分支逻辑、**不改** R2 结构契约 / R3 折叠语义 / R5 读序逻辑 / R7 说人话定义、**不动** hook 代码、**不改**四件套字段结构、**不碰** `Learner/` `Composer/`；改动集=`.ai/project/`（新增）+ `.ai/PROJECT.md`（删）+ 对齐现实的少数规则文件括号例子 + `README` + 发布元数据（VERSION/CHANGELOG/migrations/里程碑收口）。
- **AC17（dogfood·自身照说人话写）**：本迭代四件套 + `.ai/project/` 全部主题 + 交付总结过 R7 说人话三条自检，收口前逐条扫、命中即改，VERIFY 记录结论。
