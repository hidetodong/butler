---
title: 迭代化需求管理规范
audience: AI / 开发者
scope: 迭代号分配、迭代台账字段、工作区/归档/交付三层落盘关系与"固定需求"锁定纪律
---

# Iteration Schema

## 1. 目标

增量迭代场景下，单套阶段产物（`CONCEPT.md` / `AC_LIST.md` / `TECH_PLAN.md` / `VERIFY_REPORT.md`）会被一轮轮覆盖，导致"某次迭代到底固定了哪些需求、产出了哪套文档"无法回溯。

本规范引入**迭代 (Iteration)** 作为"固定需求"的单元：一次锁定验收范围的 `P1 -> P5` 闭环，用单调递增的迭代号标识，并把对应文档稳定落盘，使每个迭代都可追溯、可审计、可复盘。

核心原则：

- 每个迭代必须有一个确定的迭代号。
- 每个迭代必须落下对应的文档（工作区四件套 + 归档快照 + 人类交付总结）。
- 每次迭代只做该迭代号锁定的事情，不在迭代内偷偷扩张范围。
- **文档有界，历史横向归档**：单份文档只承载当前迭代内容，体量恒定；跨迭代的历史靠 `iterations/ITER-NNNN/` 目录**横向铺开**，严禁纵向堆进同一文件。任何"保留上一迭代内容再追加本迭代"的写法都被禁止。

## 2. 迭代号

- 格式：`ITER-<数字>`，至少四位、四位内零填充、超过四位自然增长且单调递增（`ITER-0001`、`ITER-9999`、`ITER-10000`）。编号比较一律取数字部分，不按字符串排序。
- 分配来源：未分片项目从 `.ai/ITERATIONS.md` 读取最大号；已分片项目从 `.ai/state-index.json` 的 `max_used` 读取并由 `state-ledger check` 对账，再 +1。**不依赖对话记忆或只扫热表推断**。
- 单调性：迭代号只增不减、不复用；废弃的迭代在台账标记 `abandoned`，号不回收。
- 唯一性：同一时刻最多只有一个 `active` 迭代。

## 3. 三层落盘结构

迭代相关文档分三层，职责互不重叠：

| 层 | 位置 | 角色 |
|---|---|---|
| 迭代台账 | `.ai/ITERATIONS.md` + `.ai/state-index.json` + `.ai/history/iterations/*.{md,json}` | 复合真源：根文件保存 `current` 与近期热行，有界 index 保存最大号、计数和固定路由公式；固定区间 `.md` 保存旧行，同名 `.json` 保存该片范围、数量与哈希 |
| 当前迭代工作区 | `.ai/CONCEPT.md` / `AC_LIST.md` / `TECH_PLAN.md` / `VERIFY_REPORT.md` | 固定路径的活产物，始终对应 `current` 指向的活跃迭代；hook 机械校验的就是这组路径 |
| 迭代归档 | `.ai/iterations/ITER-NNNN/` | 迭代收口时四件套的冻结快照，只读，供复盘审计 |
| 人类交付 | `deliveries/ITER-NNNN-<slug>.md` + 同名 `.html` | 迭代收口后给人看的交付总结：`.md` 为引用真源，同名 `.html` 为固定格式阅读视图（`delivery-summary.md` §9）；结构与触发参考 `delivery-summary.md` |

约束：

- 工作区四件套路径固定不变（`.ai/CONCEPT.md` 等），**不得**改成按迭代号分目录，以保证 hook 的 `phase_gate` 无需改动。
- `.ai/iterations/` 与各 `ITER-NNNN/` 子目录不在基地车部署时创建，而是在**首次迭代收口**时按需产生。
- 归档是工作区在收口时刻的快照副本，不是工作区的迁移；快照后工作区四件套保留，等待下一迭代覆写。

## 4. 迭代台账 `.ai/ITERATIONS.md`

### 4.1 必填字段

- `current`：当前活跃迭代号；无活跃迭代时为 `none`。
- 迭代表，每行一个迭代，含：`迭代号`、`标题`、`状态`、`开启日期`、`收口日期`、`所属 milestone`、`交付链接`。
- `所属 milestone`：该迭代归属的里程碑号（`MILE-NNNN`）；不归属任何里程碑的独立迭代填 `—`。本列与里程碑复合台账「含迭代」互为对账。全量时间线由热表与冷分片合并得到，不能只把根热表当全量历史。

### 4.2 状态取值

迭代行「状态」是**封闭枚举**：合法值**仅**下列三个，其他值（含 `planned`）对迭代行**非法**，不得写入台账。

- `active`：当前进行中，工作区四件套属于它。
- `closed`：已收口，已归档并已交付。
- `abandoned`：已废弃，号不回收，需在备注说明原因。

消歧与机制：

- `planned` **不是迭代状态**——它是 `milestone-schema.md §5.3` 拆分路线图的「路线项状态」，语义为"已规划未开启、`实际 ITER` 列仍为 `—`"。未开启的未来迭代由路线图的 `planned` 路线项承载，**不在 `.ai/ITERATIONS.md` 预占行**（与 §5.3「不预先占号」一致）；迭代号在开启时才绑定，那一刻才以 `active` 进台账。
- 部署了 hook 的项目，本封闭枚举由 `ledger_status` 规则**机械校验**：写 `.ai/ITERATIONS.md` 时若某 `ITER-NNNN` 行状态越界（如 `planned`），`phase_gate` 同级拦截（`exit 2`），绕过需显式 `BUTLER_BYPASS`。规则的合法值集是本节枚举的镜像，二者须一致。

### 4.3 标准模板

```md
# 迭代台账

current: ITER-0002

| 迭代号 | 标题 | 状态 | 开启 | 收口 | 所属 milestone | 交付 |
|---|---|---|---|---|---|---|
| ITER-0002 | <本迭代标题> | active | YYYY-MM-DD | — | MILE-0001 | — |
| ITER-0001 | <上一迭代标题> | closed | YYYY-MM-DD | YYYY-MM-DD | MILE-0001 | deliveries/ITER-0001-<slug>.md |
```

不归属任何里程碑的独立迭代，「所属 milestone」列填 `—`。

### 4.4 编写规则

- 台账只记结论性索引信息，不写迭代内的过程细节（迭代内的对象级变更记录归 `01_CHANGELOG.md`，格式见 `changelog-schema.md`；活产物在各迭代工作区）。
- 每次开启 / 收口 / 废弃迭代，必须同步更新本表与 `current` 指针，二者不得不一致。
- 台账超过热窗口后，用 `tools/state-ledger/state_ledger.py migrate` 把旧行写入固定数字区间冷分片；根表保留 `current` 与近期行。分片布局、index schema、命令和退出码以工具 README 为真源。

## 5. "固定需求"锁定纪律

迭代是需求的锁定单元。锁定纪律采用"允许修订、扩张才开新迭代"口径：

### 5.1 开启 (Open)

- 时机：进入 P1 或 P2、准备固定一轮需求时。
- 动作：从台账领下一个 `ITER-NNNN`，写入台账并置 `active`、`current` 指向它；本迭代的 `CONCEPT.md` / `AC_LIST.md` 即产在工作区四件套中。
- **overwrite-only（硬约束）**：开启新迭代时，工作区四件套必须以本迭代内容**整体覆写**。**严禁**保留、续写或在上一迭代内容下追加；上一迭代的产物只在收口时归档的 `iterations/ITER-NNNN/` 中存续，不得在工作区残留。`01_CHANGELOG.md` 同步重置为本迭代热数据（见 §5.5）。
- 上一迭代若已收口，`current` 应为 `none`；开启即把 `current` 指向新号。若上一迭代未收口就要开新迭代，先按 §5.4 / §5.6 处理旧迭代，不得跳过。部署项目由 hook `single_active_iteration` 机械兜底：写入台账后若出现 ≥2 个 `active` 行即 `deny`（见 `templates/hooks/README.md`）；butler 仓自身不跑 hook，靠 §5.5 收口自检 + 冷启动一致性自检把关。

### 5.2 冻结 (Freeze)

- 时机：`AC_LIST.md` 被用户 ACK 后。（`/butler:dangerous` 危险模式下，改为模型过 `65_Extension_Dangerous/dangerous-engine.md` §5.1 自审门后自主 ACK 即冻结，冻结纪律不变。）
- 物化标志：冻结 = AC_LIST 顶部 `状态: ack-frozen`（字段定义见 `acceptance-schema.md §4`）。部署了 hook 的项目，未冻结（`draft`）时源码写操作会被 `phase_gate` 拦截，使"冻结"从对话约定变成可校验状态。
- 含义：本迭代验收范围锁定，进入 P3/P4 后默认不再扩张。

### 5.3 迭代内修订 (Amend)

- 适用：冻结后需求发生**小幅**变化，且未突破原影响面。
- 动作：更新 `AC_LIST.md`，把 `状态` 退回 `draft`、**重新等待用户 ACK**（再置 `ack-frozen` 并更新 `ACK 日期`），并在 `AC_LIST.md` 顶部"修订记录"追加一行（含日期与一句变更摘要）。
- 修订仍属于同一迭代号，不另开迭代。

### 5.4 扩张转迭代 (Escalate)

- 触发：需求变化命中 `lifecycle.md` §5 回退规则中的影响面扩大信号（跨模块、契约级新增、关键路径变化等）。
- 动作：先收口或显式废弃当前迭代，再开下一个迭代号承接扩张部分；**不得**把扩张内容塞进已冻结迭代。
- 判定边界：拿不准"修订还是扩张"时，按扩张处理，开新迭代，避免范围悄悄膨胀。

### 5.5 收口 (Close)

- 时机：P5 达到可交付、可验收的闭环状态。
- 动作（收口原子仪式，按序执行；前三步必做、缺一不可，第四步前滚项目全貌产物[文件夹态必做 / 单文件态按需]，第五步自检）：
  1. 完整路径先用 `tools/verification-evidence/evidence.py verify --source hot` 校验证据热区，再用 `archive` 把整包原子移动到 `.ai/iterations/ITER-NNNN/evidence/` 并以 `verify --source archive` 复核；然后把工作区四件套快照复制到 `.ai/iterations/ITER-NNNN/`。完整路径迭代**必产** `01_CHANGELOG.md`（严格 ADD/EDIT/DELETE，格式见 `changelog-schema.md`），其当前迭代切片一并归档为 `iterations/ITER-NNNN/CHANGELOG.md`（简化路径可省）。后续收口失败需退回 P4 时用 `reopen` 整包移回，禁止 hot/archive 双真源。
  2. 生成人类交付总结 `deliveries/ITER-NNNN-<slug>.md`，并按 `delivery-summary.md` §9 用固定模板填槽并列产出同名 `deliveries/ITER-NNNN-<slug>.html` 阅读视图；结构与触发参考 `delivery-summary.md`；`.md` 与 `.html` 均只引用产物路径，**不得全文嵌入**四件套内容（见 `delivery-summary.md §4.7`）。
  3. 台账该行置 `closed`、填收口日期与交付链接，`current` 置 `none`；全局 `01_CHANGELOG.md` 收敛为只含开放迭代热数据（已归档切片不再留在全局文件）。
  4. **前滚项目全貌产物**（两态，按项目是否已采用 `.ai/project/` 知识文件夹分支）：
     - **已采用 `.ai/project/` 知识文件夹**：把本迭代 `01_CHANGELOG.md` 的 ADD/EDIT/DELETE **按主题路由折进对应 topic 文件**（identity / architecture / invariants / …），**必做**——有对象级 delta 即折，不再"按需"。当前真相 overwrite 旧结论、被取代内容删除不叠（禁历史层）；是定向路由不是重写全份，成本 ∝ 本迭代改动量、不 ∝ 文件夹大小。判据与格式见 `40_Context_Management/project-digest-schema.md §6`（折叠维护模型）。折叠**必做**，"谁折"推荐唤 `62_Extension_Agents/knowledge-fold.md` 帮手 fresh-context 执行（避免主线疲劳顺手折质量差）；起不了子 agent 则主线自折并如实标注（G2），不因此跳过折叠。
     - **仍单文件 `.ai/PROJECT.md`**（未迁移暂态，含尚未部署知识文件夹种子的项目）：本迭代若改变了某条长期事实（架构 / 不变量 / 现行约束 / 长期欠债）才更新对应字段，否则不动（多数迭代只动 0-2 行或不动）。迁移到知识文件夹的时机见 `40_Context_Management/project-digest-schema.md §9`（部署种子 R6 / 自身适配 R8）。
  5. **收口自检**（原子仪式最后一步）：先运行 `$BUTLER/scripts/audit-project-state.py --project-root "$PROJECT_ROOT"` 机械核对确定性状态；若 `PROJECT_ROOT` 就是 Butler 规则仓且尚处提交/发布前，改用 `--allow-unreleased` 并保留其 `UNRELEASED` 亮牌，不能把它复述成已发布。再跑 `40_Context_Management/context-persistence.md` §冷启动一致性自检的 6 条不变量（current↔状态 / 至多一个 active / closed 有交付 / closed 有归档〔含新口径 Evidence Index ↔ evidence record〕/ 路线项对账 / 知识文件夹漂移[第 6 条条件不变量，采用 `.ai/project/` 的项目适用、单文件暂态 N/A]），确认台账↔产物↔交付↔证据↔知识文件夹无漂移；有漂移当场修正，不留待冷启动才发现。
- 收口后工作区四件套保留原位（作为最近一迭代的只读残影），直到下一迭代开启时被 §5.1 整体覆写；其权威副本以 `iterations/ITER-NNNN/` 为准。

### 5.6 废弃 (Abandon)

- 时机：迭代中途确认不再继续（需求取消、方向推翻）。
- 动作：台账该行置 `abandoned` 并备注原因，`current` 置 `none`；可选择是否快照归档（若有复盘价值则归档）。

## 6. 与执行流程的关系

- 迭代不是新阶段，而是套在 `P1 -> P5` 状态机外层的需求锁定单元；阶段推进规则仍以 `lifecycle.md` 为准。
- Explore 的 resolved Decision slice 若经 `tools/decision-promotion/` 的 `iteration-start` 进入交付，仍由现有 iteration-intake 在 P1 领号和整体覆写活产物；promotion 只在 `CONCEPT.md` 留 Source References 与不可变 receipt，不产生另一种 Iteration、不直接进入 P2。存在 active Milestone 时必须指定其既有 planned route；没有 active Milestone 时才允许 standalone。
- P2 冻结后，Decision Map 的新结论不得经 promotion 覆盖当前迭代：未突破原影响面按 §5.3 amend 并重新 ACK，影响面扩大按 §5.4 进入未来 route / Iteration。
- 迭代之上还可套一层**里程碑 (Milestone)** 作为大版本范围单元：处于 `active` 里程碑期间开启的迭代自动归属它，归属关系与版本级交付机制以 `milestone-schema.md` 为准。里程碑松耦合可选，迭代不依赖里程碑也能独立成立。
- 工作区四件套字段仍分别以 `concept-schema.md` / `acceptance-schema.md` / `tech-plan-schema.md` / `verify-schema.md` 为准。
- 收口交付的文件层与对话层规则以 `delivery-summary.md` 为准。
- 台账与归档目录的部署时机以 `mcv-deployment.md` 为准。
- 极小、零升级信号的简化路径任务可不单独开迭代号，按 `lifecycle.md` §2 简化路径处理；是否纳入迭代台账由用户决定。
