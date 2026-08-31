<!-- butler-artifact-template: 1.0.0 artifact=changelog -->
# ITER-0117 变更流

## ADD

- `Coder/40_Context_Management/intake-schema.md`（新建，184 行）— 需求录入三层契约。frontmatter 声明 title / audience / scope；H1 底下一段引用块是生效时点声明（两份规则真源并存、R7 前零写入、分歧一律以 `inbox-schema.md` 为准、无机器兜底）。§1 闪念口定 `.ai/INBOX.md` 的单表结构、日期化闪念键、五个字段、四态封闭枚举、四条合法转移、终态不回头与清理纪律；§2 孵化区定 `规模` 三档、按档段落要求与改档规则；§3 执行分流定三条封闭出口、各自前置条件、两侧原子、`undecided` 不得直接出区、ideation 不是出口、回写闪念；§4 划三层互不重复的边界；§5 明写本契约管不到的四件事。绑 AC1 / AC2 / AC3。
- `.ai/debt.md` 新增 2 条欠账（10 → 12）— 「两份 inbox 规则真源并存，没有机器兜底」（归 R8 自然消解）、「已部署项目里旧格式 `.ai/INBOX.md` 的迁移义务没人认领」（归 R15）。绑 AC9。
- `.ai/MILESTONE.md` §5.4 新增 3 条范围演进登记 — 路径撞车的处置与理由、孵化区目录按现实路径写的定序判断、规模分档的连带影响与索引为什么不加列。绑 AC8。
- `.ai/iterations/ITER-0117/` 新增 13 份验证资产 — 11 份 AC 证据脚本、1 份两组扫描脚本 `ac-sweep.py`、1 份 P4 前哈希基线 `pre-p4.baseline`（`.ai/MILESTONES.md`、`milestone-schema.md`、`Coder/README.md`、9 份草稿，共 12 行）。绑 AC12。

## EDIT

- `.ai/milestone-backlog/` 下 9 份候办草稿 — 各在 `候办状态: deferred` 之后插入一行 `规模: milestone`，每份恰 1 增 0 删，其余内容逐字未改。绑 AC4。
- `Coder/20_Workflow_Lifecycle/milestone-schema.md` §4.5 编写规则 — 原「候办草稿沿用 §5 的四段结构，但顶部必须恰好标明一次 `候办键` 和一次 `候办状态`」拆成两条：一条把头部必标记号由两项扩为三项（加 `规模`），一条把段落结构改为按 `规模` 分档并指向 `intake-schema.md §2`。改动集中在第 112 行，§4.5 的 5 列索引表模板与 §5 正文零改动。绑 AC6。
- `Coder/README.md` 两处注册 — `## 目录结构` 的 `/40_Context_Management` 树里加 `intake-schema.md`；`## 读取顺序` 的逐文件指针列表里加一条完整说明（三层要点 + 与 `inbox-schema.md` 的并存分工）。绑 AC7。
- `.ai/OVERVIEW.md` — 由 `scripts/sync-project-overview.py --write` 重算，`40_Context_Management/` 规则文件计数 11 → 12，工作流清单仍 12 行。绑 AC11。
- `.ai/AC_LIST.md` — 按 `iteration-schema.md §5.3` 走一次 amend：退回 `draft`、加 `修订记录:` 单行、AC5 由「待办区索引加规模列」改为「索引逐字节未改」，连带收窄 AC1 / AC6 / AC12 与 In Scope，再重新 ACK 冻结。
- `.ai/ITERATIONS.md` / `.ai/state-index.json` / `.ai/02_SESSION_HANDOFF.md` / `.ai/handoff-state.json` / `.ai/task-state.md` — 台账与交接状态随迭代推进同步。

## DELETE

- 无。本轮零删除：旧 inbox 全链（`inbox-schema.md`、`inbox-workflow.md`、两份 hook 测试、`tools/inbox/` 全 5 份、inbox 命令与 skill、`workflows/registry.json` 的 inbox 块）共 13 份文件逐字节未动，删除归 MILE-0016 R8。绑 AC10。
