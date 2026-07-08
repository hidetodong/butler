# VERIFY_REPORT — ITER-0034（MILE-0003 R8 · dogfood 迁 .ai/project/ + 切 v2.0.0）

> 监督态自驱（非 `/dangerous`）· 全为规则 / 文档 / 台账改动，验证=读产物核契约 + `git`/`grep` 核守恒 + dogfood 冷启动走查，确定性可复现（**auto·可靠**）· 无人测道残余（纯文档、无运行时）。分段A（AC1–9、16–17，本报告已验）+ 段B（AC10–15，切版时补验）。

## 段A 验收结果（逐 AC · auto·可靠）

- [x] **AC1 ✓** `.ai/project/00_INDEX.md` 已建，含 R2 §8 入口三块：一段话"butler 是什么"+ 读序地图（7 条"想知道 X → 读 Y"）+ 主题登记表（7 主题各一行 = 文件名 + 管什么 + 边界）。
- [x] **AC2 ✓** 7 主题文件全建（`identity`/`architecture`/`capabilities`/`invariants`/`constraints`/`debt`/`frontier`）。旧单文件 6 段无遗漏迁入：目的→`identity`、架构→`architecture`、不变量→`invariants`、约束→`constraints`、欠债→`debt`、指针→`00_INDEX` 读序 + 各主题指针；R2 新增两层 `capabilities`（命令 / P1–P5 SOP / 驻留工具 / 帮手）+ `frontier`（v2.0.0 在即 + MILE-0003 收尾 + 下一瓶颈）从现状新写。
- [x] **AC3 ✓** 密度守 digest-and-point（名 + 干什么 + 指针），每份有界可整篇读完。`architecture` 只摘三层全貌 + 补"成熟度"层（真源没有的现状），目录树 / 各规则一句话职责显式指 `Coder/README.md` 不抄；`capabilities` 引擎细节指各扩展模块。无一主题整段搬真源。
- [x] **AC4 ✓** 迁入内容守 R7 说人话（术语先解释 / 无悬空比喻 / 英文变量首现带解释）；各主题只承载当前真相、无历史层（overwrite 语义）。
- [x] **AC5 ✓** `.ai/PROJECT.md` 已删（`git status` 显 `D`）。`.ai/project/` 内引用 PROJECT.md 仅 2 处且合法：`frontier.md`（"从 PROJECT.md 迁走"的历史叙述）、`invariants.md`（"单文件老项目读 PROJECT.md"的通用规则）——**非** butler 自身全貌产物的踩空活引用。
- [x] **AC6 ✓** `.ai/task-state.md` 冷启动入口改 `.ai/project/00_INDEX.md`、butler 自身描述转"文件夹态"。
- [x] **AC7 ✓** 对齐现实 3 处，单文件分支逻辑**保留**（红线守住）：`mcv-deployment.md §2`（"R6 前部署尚未迁移的老项目"，去 butler 自身）、`context-persistence.md §6`（单文件分支去 butler、注"butler 走文件夹分支"）、`project-digest-schema.md §9`（R8 待→已接线 ITER-0034 + line 149/152 两态并存说明）。`milestone-schema` grep 无"含 butler 单文件"命中、无需动。
- [x] **AC8 ✓** README 为通用规则描述（两态分支都在、不点 butler 自身现状），核对无需改。
- [x] **AC9 ✓（dogfood 走查通过）** ①从 `00_INDEX` 登记表可定位任一主题、7 登记 = 7 实际文件（对账一致）；②`git grep --untracked` 证 `.ai/project/` 无指向已删 `PROJECT.md` 的踩空自引用（2 处合法）、其余指针真源（README/各 schema/HUMAN_GUIDE/CLAUDE.md）均存在；③第 6 不变量（知识文件夹漂移）对 butler 自身转适用，主题从当前现实新写、当轮不漂移。

## scope 守恒（AC16）

- [x] **AC16 ✓** `git status` 段A 改动集 = `.ai/project/`（新 8 文件）+ `.ai/PROJECT.md`（删）+ `.ai/` 四件套与台账 + 3 规则文件对齐（`mcv-deployment`/`context-persistence`/`project-digest-schema`）。**无** VERSION/CHANGELOG/migrations（段B）、**无** hook 代码 / 四件套字段结构 / 两态分支逻辑 / R2·R3·R5·R7 定义 / `Learner`·`Composer` / rename 改动。

## dogfood 说人话自检（AC17）

- [x] **AC17 ✓** 四件套 + `.ai/project/` 8 文件 + （交付于收口产）按 R7 三条自检：术语（digest-and-point / dogfood / 冷启动 / 两态 / 折叠）首现均有一句话解释或比喻落地；英文标识（`00_INDEX` / `[split]` / `$BUTLER` / `single_active_iteration`）首现带上下文；无悬空比喻。

## 段B 待验（切版时补，AC10–15）

- [ ] AC10 VERSION 2.0.0 + MAJOR 判级 / AC11 CHANGELOG [2.0.0] 聚合 / AC12 `migrations/v2.0.0.md`（`[split]`+`[regen-claude]`+`[restamp]` 幂等）/ AC13 收口 MILE-0003 / AC14 两提交分离 / AC15 切版前后一致性 + tag 用户放行。

## 独立复核

- **结论 APPROVE**（干净上下文子 agent、验证者≠实现者、只读、对抗式）。逐条核过 7 个对抗重点：迁移无遗漏（旧 6 段全进新 7 主题）/ 不逐字抄真源（`architecture` 回指 README 不搬目录、`capabilities` 不搬引擎正文）/ 单文件分支逻辑未误删（红线守住）/ 指针不踩空（无指向已删 `PROJECT.md` 的活引用）/ `00_INDEX` 三块齐 + 登记表对账 / 说人话无裸奔黑话 / scope 守恒无越界。**无 Must Fix、无 Should Fix。**

## Remaining Risks

- 段B `git tag v2.0.0` 不可逆、对外发布锚点——执行前须用户明确放行（AC15 闸）。
- `/butler-upgrade` 仍未真跑（既存欠债，见 `debt.md`），本轮产的 `migrations/v2.0.0.md` `[split]` 配方首次真实老项目端到端验证仍悬。
