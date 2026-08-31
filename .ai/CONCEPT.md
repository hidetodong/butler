<!-- butler-artifact-template: 1.0.0 artifact=concept -->
# CONCEPT — ITER-0119 · 退役旧 inbox 全链（MILE-0016 R8）

## Current Understanding

- **R7 只搬了活接线，没拆旧机构。** 上一轮把 `/butler:inbox` 的命令薄壳、skill、注册表条目全部改指新契约 `intake-schema.md` 与新工具 `tools/intake/`，但按 Out of Scope 明确保留了旧链一字未动。结果是今天仓里同时躺着两套需求录入体系：新的在用，旧的没人调用却仍被 CI 跑、被 `Coder/README.md` 注册、被人读文档当成现行机制介绍。
- **旧链的实体清单（本轮的拆除对象）**：规则真源两份 `Coder/40_Context_Management/inbox-schema.md`（8.6 KB，定 `SRC-NNNN` 稳定来源身份、observed/processed 双 SHA-256、七态处理状态机、派生关系表）与 `inbox-workflow.md`（6.1 KB，定扫描 → 语义分类 → 确认 → 委托路由）；确定性工具 `tools/inbox/`（`inbox.py` 348 行，只有 `status` 与 `scan` 两个子命令，`scan` 遍历 `origin/` 算双指纹写回执）；合同测试 `templates/hooks/tests/test_inbox_contract.py`（59 行 / 7 个用例，逐条断言上面那份数据契约的措辞）；`templates/hooks/tests/test_inbox_workflow.py` 里 R7 特意留下的那一个用例 `test_inbox_workflow_route_and_safety_contract`；CI 里那行 `python -m unittest tools.inbox.tests.test_inbox`；`tools/mile0009-e2e/tests/test_mile0009_e2e.py` 开头调 `inbox scan` 的那一段。
- **`origin/` 不是旧链的私产，是整个部署协议的一部分。** 它是 `mcv-deployment.md §2` 规定部署时必建的三个目录之一（另两个是 `.ai/` 与 `deliveries/`），定位是「用户原始需求材料的可选收件箱，AI 只读」。今天在活跃面上有 18 份文件提到它：部署协议、`milestone-schema.md` 的 brief 材料通道（§6.1 输入表、§6.4 合成步 1、§7 命令表）、`butler-upgrade.md` 的两处写集排除、`/butler:init` 与 `/butler:prd` 两个命令、`butler-init` skill、`rule-card.md`、`README.md`、`HUMAN_GUIDE.md`、`references-schema.md` 的原稿保护条款、`docs/prd-migration-guide.md`，再加三份测试的夹具。**所以「退役 `origin/`」比「删 `tools/inbox/`」重得多**，它要改的是部署时建什么目录、里程碑 brief 从哪来、人读文档怎么教用户投材料。
- **`origin/` 的「AI 只读、不改用户原稿」是有价值的、要活下来的东西。** 那条纪律保护的不是这个目录名，是「用户自己写的原始材料，AI 不许改写、重命名、移动、归档、删除」这件事。退役目录不等于放弃纪律——纪律要跟着搬到新的载体上（用户点名的任意文件路径）。
- **拆除会踩到的机器约束**：`scripts/audit-project-state.py` 与 `sync-project-overview.py` 会重算规则文件数与驻留工具清单（规则少两份、工具少一个）；`context-budget` 有分层预算表；`.ai/invariants.md` 第 48 条整条讲的就是旧契约（`SRC-NNNN` + 双指纹 + scanner + `origin/` 只读），它会立刻变成假话。
- **已部署项目那边这轮做不干净，且不是本轮的锅。** 升级器的 typed 动作标签只有 `[rename]` / `[split]` / `[add-field]` / `[regen-entrypoints]` / `[sync-hooks]` / `[restamp]` / `[no-op]` 这几种，**没有删除、也没有移动**——新增这两类正是 R14 的活。所以本轮对已部署项目最多只能做到「butler 不再创建、不再读、不再教」，别人硬盘上已经存在的 `origin/` 目录和旧格式 `.ai/INBOX.md` 只能留在原地。好消息是 `origin/` 从来就是用户自管、AI 零写入的，留着不构成漂移；坏消息是旧格式 `.ai/INBOX.md` 会让新工具直接报错停下（已实测：表头不符即 fail-closed、不落一个字节），这条已在 `.ai/debt.md` 有账，本轮只补一道回归防线证明它不会把旧文件写坏。

## Scope

- **删两份规则真源**：`Coder/40_Context_Management/inbox-schema.md`、`inbox-workflow.md`，连同 `Coder/README.md` 里的目录树与职责段两处注册。
- **删整个 `tools/inbox/`**（含 `README.md`、`inbox.py`、`tests/`），并摘掉 CI 里那行。
- **删旧链合同测试** `templates/hooks/tests/test_inbox_contract.py` 整份；删 `test_inbox_workflow.py` 里 R7 留下的那一个旧规则用例，另两个描述活接线的用例原样保留。
- **改 `tools/mile0009-e2e/tests/test_mile0009_e2e.py`**：摘掉链条开头调 `inbox scan` 的那一段（连同 `origin/` 夹具），后面 prd-migrate → prd-status → prd-update → workspace-scope 的部分原样保留。
- **退役 `origin/` 这个目录名，原件搬进 `.ai/references/raw/`**（用户 2026-08-21 定的方向：所有外部资料引用收进 `.ai/references/`，不再另开通道）。部署时不再创建 `origin/`；里程碑 brief 与 `/butler:prd` 的文件通道改指新位置；`references-schema.md` 的定位段扩成两类保真度——原件（用户自管、AI 只读）与投影（AI 派生、受控、可 bump 版本），并顺手修掉 §1 那张还在拿已退役的 `.ai/project/` 做对照的表。
- **改写 `.ai/invariants.md` 第 48 条**，让它描述现行的三层录入契约，而不是已删的 `SRC-NNNN` + 双指纹 + scanner。
- **给「AI 对用户原件只读」装上机器门禁**：新增 hook 规则拦住 AI 对 `.ai/references/raw/` 的写操作，让这条一直是散文的纪律第一次有兜底。
- **按 `migration-schema.md §5` 判本轮对已部署项目的影响**，结论写进 §5.4，并把「删除 / 移动两类动作缺失」明确指向 R14。
- **重算派生产物**：`.ai/OVERVIEW.md` 走 `--write`，审计、CI、两组扫描全绿。
- **补一道回归防线**：新工具遇到旧格式 `.ai/INBOX.md` 必须报错退出且零写入。
- Out of Scope：不改 `.ai/milestone-backlog/` 目录名、不迁 `deliveries/`（都归 R9）；不给升级器加删除/移动动作（归 R14）；不写已部署项目的完整升级回归（归 R15）；不动 `.ai/INBOX.md` 里 R7 记下的那条真实闪念；不切版、不发布、不提交。

## Open Questions / Risks

- **~~`origin/` 退役后文件通道落到哪~~（已定）**：2026-08-21 用户拍板——所有外部资料引用统一收进 `.ai/references/`，不另开通道。落地形态是在其下开 `raw/` 子目录专放原件，用目录而非文件名前缀承载身份，因为路径前缀能被 hook 与工具机械判定。**代价是 `.ai/references/` 的定位要扩**：它今天写的是「外部权威资料的落盘区」、里面全是 AI 派生的受控投影，现在要容纳一类 AI 一个字都不许动的原件，§1 与 §2 都得改写。
- **风险 · 一次删掉两份规则真源会不会删掉还有人读的东西。** 判断依据只有静态引用扫描（改完全仓不得再出现 `inbox-schema` / `inbox-workflow` / `tools/inbox` 三个字样，归档与历史 migrations 除外），扫不到「某次会话里模型凭记忆去读」。这个洞是 `.ai/debt.md` 里「运行时观测缺位」那条的老问题，本轮不解决，只如实记。
- **风险 · `origin/` 的引用面跨了 18 份文件、含两个命令薄壳与两份人读手册。** 漏一处就会留下指向不存在目录的死引用。防线是全仓零命中扫描 + `sync-workflow-registry.py --check` + CI，但人读文档里的措辞是否读得通只能人眼过。
- **`origin/` 的「AI 只读」从来没有机器兜底**（实测：整个 `templates/hooks/` 对 `origin` 零命中，唯一一处是 `bypass.py` 注释里的英文单词 original）。所以搬家不弄丢任何保护——本来就没有。但这也意味着，如果只是把散文换个地方写，等于把「写了没人执行」这个毛病换个地方再犯一遍，因此本轮顺带给新位置加一条 hook 门禁。代价是改动 hook 树：要更新 `migrations/manifest.json` 的 `known_hook_tree_digests`，切版配方要多一步 `[sync-hooks]`。
- **风险 · `test_prd_collection_contract.py` 有一条断言逐字锁着 `origin/` 字样**（"`origin/` 用户原稿不因 PRD 集合而被改写、移动或删除"）。改 `references-schema.md` 的措辞就会红。这是好事——它证明防线有效——但要连测试一起改，且改完断言的必须仍是同一条纪律，不能把纪律一起删掉。
- **风险 · 删掉旧链后，`.ai/debt.md` 里那条「两份 inbox 规则真源并存」自然消解。** 要顺手清账，不能留着说假话；同时「已部署项目旧格式 INBOX.md 无人认领」那条要留着并更新表述——旧链删了之后它反而更尖锐，因为连回退的旧工具都没有了。
