> 分流: 完整 | 命中升级信号: 多文件改动(≥3) / 契约级新增(hook 新增 deny 条件——拦截契约扩展) / 关键路径(hook 门禁) / 跨模块影响(iteration-schema·milestone-schema·hooks·部署·文档) / 涉及代码+测试 | 2026-06-19

# Goal
- 把**迭代状态枚举固化为封闭三态**（`active` / `closed` / `abandoned`），让 schema 从"列举三个值"升级为"显式封闭、其他非法"，并在规则上消除与里程碑路线图「路线项状态」（含 `planned`）的命名串台。
- **不止于文档，要有机制**（用户明确要求）：新增一条 PreToolUse hook 规则 `ledger_status`，在写 `.ai/ITERATIONS.md` 时机械校验「状态」列，越界值（如 `planned`）即拦截——保证"枚举不会取错"，与现有 `phase_gate` / `protected_paths` 同源。

# Background / 问题
- 用户在一个已部署项目的 `.ai/ITERATIONS.md` 台账里发现了 `planned` 状态。经核对：`iteration-schema.md §4.2` 定义的迭代状态只有 `active`/`closed`/`abandoned`，**没有 `planned`**。
- `planned` 真正的归属是 `milestone-schema.md §5.3` 的**拆分路线图「路线项状态」**（`planned`/`active`/`closed`/`abandoned`），语义是"已规划未开启、`实际 ITER` 列仍为 `—`"。两张表都有「状态」列、值域不同，于是路线项的 `planned` 被误写进迭代台账。
- 根因有二：① 两个「状态」列语义串台；② 预先占号（违反 §5.3「不预先占号」，号应在开启时才绑定）。
- 现行 schema 只是**列举**三态、未声明封闭性，且**无任何机制**阻止越界值落进台账——这正是用户要补的洞。

# Scope
## In
1. **枚举固化（spec/SSOT）**：`iteration-schema.md §4.2` 改写为"封闭枚举，合法值仅 active/closed/abandoned，其他（含 planned）对迭代行非法"，并交叉引用里程碑路线项状态以消歧。
2. **消歧（milestone 侧）**：`milestone-schema.md §5.3` 增一句明确——「路线项状态」是路线项自己的命名空间，`planned` 路线项的「实际 ITER」为 `—`、**不产生迭代台账行**；迭代行的状态以 `iteration-schema §4.2` 三态为准。
3. **机制（hook）**：新增 `templates/hooks/rules/ledger_status.py`——仅针对 `.ai/ITERATIONS.md` 写操作，解析「状态」列，ITER-NNNN 行状态 ∉ 三态即 `deny`（给出违规值 + 合法枚举 + planned 归属提示）；接入 `butler_gate.py` 的 `RULE_MODULES`；配套单测 `tests/test_ledger_status.py`。
4. **传播/注册**：hook `README.md`（新增规则说明 + 执行顺序）、`mcv-deployment.md §5`（hook 拦截能力描述补台账状态校验）、`Coder/README.md`（hook 门禁一句）、`rule-card.md`/`HUMAN_GUIDE.md`（如含 hook 行为概述则补一句）。

## Out（非本轮）
- 不给迭代加 `planned` 第四态（选项 B 已否决：与「不预先占号」核心纪律冲突）。
- 不校验 `current:` 指针或里程碑台账状态（本轮聚焦迭代台账「状态」列；current/MILE 校验列为后续候选）。
- 不切新版本（releases 按需聚合，本轮不发版；ITER-0008 累积到下次切版，预计 MINOR——新增 hook 门禁能力）。
- 不改 hook 退出码契约 / bypass 机制 / 其他既有规则行为。

# Key Design Decisions
1. **机制 = hook，而非仅文档**：butler 的机制化手段就是 PreToolUse hook；新规则与 `phase_gate` 同构、复用 `lib/bypass`（可 `BUTLER_BYPASS` 显式绕过），落在已部署项目——正是 `planned` bug 出现的面。
2. **专打台账、不走 is_gated**：`.ai/` 在 `GATED_BLACKLIST` 中被源码写门豁免；新规则按 `target == .ai/ITERATIONS.md` 精确命中、独立校验内容，与现有规则路径不冲突。
3. **校验入参文本**：Write 取 `content`、Edit 取 `new_string`、MultiEdit 取各 `edits[].new_string`；逐行找 `^ITER-\d{4}$` 起头的表行，取第 3 单元格（schema 固定列序：迭代号|标题|状态|…）做大小写不敏感比对。空状态单元格放行（不误杀半写行）。
4. **封闭枚举单一定义点**：迭代状态枚举的权威定义在 `iteration-schema §4.2`，hook 的 `VALID_STATES` 是其机械镜像；文档与代码两处一致，注释互指，避免漂移。
5. **planned 保留正当出口**：固化不删 planned，只把它钉回里程碑路线项语义；"未来要做的迭代"仍由路线图 planned 路线项承载。

# Risks / Open Questions
- 列序假设：规则依赖 schema 固定列序（状态=第 3 列）。若未来改列序需同步规则——以 schema 为 hook 所执行的契约，可接受；测试覆盖固定列序。
- Edit 片段可能不含完整表头：规则按"行内 ITER-NNNN + 第 3 单元格"判定，不依赖表头，故片段编辑也能校验。
- 新增 deny 条件属 hook 拦截契约扩展：对已部署旧项目升级后会新增一道拦截——附 bypass 兜底，且只拦真正越界值，不影响合法三态写入。
- butler 仓自身不跑该 hook（hook 只部署到目标项目）；butler 自己的台账靠规则纪律——与现状一致。

# 影响文件（预估）
- 新增：`templates/hooks/rules/ledger_status.py`、`templates/hooks/tests/test_ledger_status.py`。
- 改：`templates/hooks/butler_gate.py`（接 RULE_MODULES）、`templates/hooks/README.md`、`Coder/20_Workflow_Lifecycle/iteration-schema.md`（§4.2）、`Coder/20_Workflow_Lifecycle/milestone-schema.md`（§5.3）、`Coder/20_Workflow_Lifecycle/mcv-deployment.md`（§5）、`Coder/README.md`、`templates/rule-card.md` 与 `HUMAN_GUIDE.md`（如含 hook 概述）。
- 零改动护栏：其他 hook 规则（phase_gate/protected_paths/artifact_chain）行为、lib/io·lib/bypass、产物链四 schema、versioning-schema、台账其它字段语义。
