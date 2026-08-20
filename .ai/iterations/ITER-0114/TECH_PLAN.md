<!-- butler-artifact-template: 1.0.0 artifact=tech_plan -->
# TECH_PLAN — ITER-0114

方案状态: pass
方案审查日期: 2026-08-19
方案审查方式: user-ack

## Design Decisions

**D1 · 三份产物、三种性质、互不混装（AC 全局前提）**

`frontier.md` 死于混装：可派生事实与会过期判断塞在同一节，人一次只改一半。所以这轮的落点按性质切，每份文件只有一种性质，任何一份都不允许出现第二种：

| 文件 | 性质 | 谁写 | 不烂的机制 |
|---|---|---|---|
| `.ai/OVERVIEW.md` | 可从机器源头派生的事实 | 生成器独写，人不许碰 | `--check` 进 CI，与源头不一致就红 |
| `.ai/invariants.md` | 长期决策与理由 | 纯手写、纯追加 | 写作纪律 + 无指针条目棘轮 |
| `.ai/debt.md` | 会过期的判断 | 纯手写、追加为主 | 还掉即删，本来就有消解路径 |

`.ai/OVERVIEW.md` 全文生成、**不留手写槽位**。这是与入口模板 `user-managed` 那套的关键区别：入口模板必须保留用户区，全貌产物不需要——手写内容有另外两个落点。少一个保留区就少一整类「生成器吃掉用户文字」的故障。

**D2 · 生成器形状照抄 `sync-workflow-registry.py`**

新建 `scripts/sync-project-overview.py`：

- CLI：`--check` / `--write` 互斥必选（`add_mutually_exclusive_group(required=True)`），`--project-root`（默认脚本上溯两级）、`--butler-root`（默认同 `--project-root`）。
- 写盘走 `atomic_write`（临时文件 + `os.replace`），与既有生成器一致。
- 五个源头分别由一个 `section_*(ctx)` 函数产出一节，函数返回 `(标题, markdown 正文)`；缺源头时抛 `OverviewError(f"missing source: {relative}")`，不产出残缺页。
- 页首固定三行：标题、`> 本页由 <源头列表> 通过 \`python3 scripts/sync-project-overview.py --write\` 生成，请勿手改。`、生成口径一句。**不写生成时间戳**——时间戳会让每次重跑都产生 diff，`--check` 就永远红。

五节与各自源头：

| 节 | 源头 | 派生内容 |
|---|---|---|
| 版本与当前状态 | `VERSION`、双台账 `current` 行 | 版本号、当前 active 里程碑与迭代（或 `none`） |
| 里程碑时间线 | `.ai/MILESTONES.md` 热表 + `.ai/state-index.json` | 每个里程碑一行（号 / 标题 / 状态 / 起止 / 含迭代数），冷片只报计数不展开 |
| 规则体系目录与职责 | `Coder/README.md` 的「规则目录说明」+ `Coder/` 实际子目录 | 每个子目录一行：目录名 / 文件数（实测）/ 职责一句（README 原文） |
| 工作流清单 | `workflows/registry.json` | Router 一行 + 13 个业务工作流各一行（id / 双宿主入口 / 风险 / 规则真源） |
| 驻留工具清单 | `tools/` 子目录 + 各自 `README.md` 首个非空标题行 | 每个工具一行：目录名 / 一句用途 |

**D3 · `--check` 的诊断必须指名到节，不是「文件有差异」**

逐节比对而不是整文件比对：生成器先算出 `[(节标题, 正文)]`，再把磁盘上的文件按同一套节标题切开，逐节比 sha256。不一致时报 `overview section drift: <节标题>`；节数量对不上时报 `overview section set mismatch: expected=[...] actual=[...]`。整文件 diff 只在切不开时兜底。这条是从 ITER-0113 的教训来的——投影校验当初就是因为「指名到文件」才有用。

**D4 · 体量上限 12000 字节写死在生成器常量**

`OVERVIEW_MAX_BYTES = 12000`。`--write` 与 `--check` 都校验，超限报 `overview too large: <实测> > 12000`。这个数没有成本锚点（全貌产物按需读，不像读序块每次会话都付），它的职责只是拦住 `capabilities.md` 那种无上限膨胀。P5 要如实记实测值与「这个数是拍的」。

**D5 · `Coder/README.md` 的两个未登记目录当场补上，并让生成器 fail-closed**

核查发现 `55_Extension_ConvergenceLoop` 与 `60_Extension_CodeReview` 两个目录在文件系统里存在，但 README 的「规则目录说明」没给职责。生成器对这种情况 fail-closed（报 `directory has no description in Coder/README.md: <目录名>`），同批把这两条职责补进 README。补两行不算改 README 的结构与字段，属于填既有结构里的空洞；不补的话「目录与职责」这一节从第一天起就是残的。

**D6 · `invariants.md` 迁移用 `git mv`，只改两条**

`git mv .ai/project/invariants.md .ai/invariants.md` 保住 `--follow` 的历史可追溯。同批只动两处：

- 收口仪式那条：删掉五步清单与 `fold receipt`，改为「收口是原子仪式，步骤与顺序以 `iteration-schema.md §5.5` 为准」+ 原有的为什么。
- 冷启动读序那条：删掉四步清单，改为「读序固定且只有一处真源 `context-persistence.md §6`」+ 原有的为什么，并删掉那句已经过期的 `*ITER-0112 修订*`（R3 就是它等的那个答案）。

两条都按 D7 的纪律重写——**不复述机制形状，只留决策 + 理由 + 真源指针**。这不是顺手多改，正是这两条变假的根因治理。

**D7 · 写作纪律与棘轮进文件头，校验进生成器**

`.ai/invariants.md` 文件头三条纪律：①只写决策与理由，不复述机制的具体形状（步数 / 清单 / 顺序）②每条至少带一个反引号真源指针 ③还成立才留，作废即删不留历史。

棘轮实现放进 `sync-project-overview.py` 而不是新建脚本——它已经要读 `.ai/`，多一个校验不值得再开一个入口。常量 `INVARIANT_POINTER_EXEMPT = 16`，统计 `^- \*\*` 开头且不含 ``` `…/…` ``` 或 ``` `….md` ``` 形态指针的条目数，超过基线报 `invariants without source pointer: <实测> > 16` 并列出超出的条目标题。基线本身也是欠债，进 `debt.md`。

**D8 · `frontier.md` 逐节处置，照 ITER-0112 删 `capabilities.md` 的格式留痕**

三节逐条判定，判定口径：

- 能从五个机器源头之一算出来 → 弃，注明「已由 OVERVIEW 的 X 节覆盖」。
- 算不出来、且是「还没做完、有还清路径」 → 迁 `.ai/debt.md`，注明来源与迁入日期。
- 算不出来、且是陈述已发生的事实（「MILE-0009 已随 v3.0.0 发布」这类） → 弃，注明「历史事实，归 `ITERATIONS` / `deliveries`」。

每条的判定结果逐条写进本迭代变更流 DELETE 段，无一条无交代。

**D9 · 读序第 5 步只加按需指针，不动分步**

在第 5 步末尾追加一句：需要项目全貌时按需读 `.ai/OVERVIEW.md`（生成物）与 `.ai/invariants.md`（长期决策与理由）。措辞必须显式说「按需」，不能让它读起来像必读。改真源 `context-persistence.md §6` 一处，四处投影同步，跑 `context_budget.py check` 确认 `order_bytes` 仍 ≤ 1400（当前 1194，余 206 字节，这句约 80 字节，够）。

**执行顺序**：D5 补 README 两行 → D2/D3/D4 建生成器 + 首次 `--write` → D6 迁 `invariants.md` 改两条 → D7 加纪律与棘轮校验 → D8 处置 `frontier.md` 并删目录 → D9 改读序并同步投影 → 接 CI → 登记 §5.4 → P5。

## Failure Paths

1. **生成器读到半截源头就产出残缺页**。任一源头缺失或解析失败必须抛错退出，绝不产出「少一节但看起来正常」的页面——那正是 `capabilities.md` 的死法（有覆盖但内容失真）。所有 `section_*` 在缺源头时抛 `OverviewError`，`main` 捕获后打印到 stderr 并 `sys.exit(1)`，不写盘。
2. **`--check` 因非语义差异永远红**。时间戳、字典序不稳定、路径分隔符、行尾都可能造成假红。对策：不写时间戳；所有列表显式排序（工具按目录名、工作流按 registry 中的出现顺序、里程碑按号倒序）；统一 `\n` 行尾；写盘与比对用同一个 `render()` 的返回值，不重新读盘再拼。
3. **棘轮把基线锁成永久豁免**。16 条无指针条目本身就是最容易悄悄变假的那批，棘轮只防增量。若不登记，三个月后这 16 条会被当成「合规」。对策：基线数字同时写进 `.ai/debt.md` 一条明确欠债，并在 `invariants.md` 文件头写明「16 是历史欠账，不是允许额度」。
4. **`git mv` 之后有活引用漏改**。`invariants.md` 被 `context_budget.py` 的测试 fixture 清单引用（`.ai/project/invariants.md`），漏改会让测试套直接红。执行时先全仓 `grep -rn 'project/invariants'` 拉出全部命中再改，不靠印象。
5. **改读序块撞上 1400 字节上限**。余量只有 206 字节，追加的句子必须压在 100 字节内。若超限，退路是把两个指针合并成一句（「全貌与长期决策见 `.ai/OVERVIEW.md` 与 `.ai/invariants.md`，按需读」），而不是抬高上限——上限抬了就再也压不回来。
6. **D5 补 README 两行被判为越界**。AC 的 Out of Scope 写的是「不改 `Coder/README.md` 的结构与字段」。补两条职责说明是填既有结构里的空洞，不是改结构；但这是我的判断，若用户认为越界，退路是生成器对这两个目录输出「README 未登记职责」而不 fail-closed，OVERVIEW 如实显示缺口。两条路都不掩盖问题，区别只在把缺口摆在哪。
7. **`.ai/project/` 删目录影响目标项目侧规格**。butler 仓自己删得干净，但 `.ai/project/workspaces.md` 仍是目标项目侧 PRD / 工作区机制的规格落点（AC 已列 Out of Scope）。执行时不得顺手改 `workspace-scope-schema.md` 里的路径；只在 §5.4 登记这个名字已名不副实、去留归 R9。
8. **OVERVIEW 生成得准但没人读**。`--check` 只能证明「生成段与机器源头一致」，证不了「有会话读过它」。AC15 要求交付如实记这条；本轮不得把「有全貌产物了」说成「冷启动全貌问题已解决」。真实消费数据要等 R11。

## Test Strategy

新建 `tools/../scripts` 侧测试：沿用本仓 `scripts/test-*.py` 的位置约定，新建 `scripts/test-sync-project-overview.py`，`unittest` 在临时根上造 fixture（拷贝真实源头后定向篡改），不碰真实仓。

**新增 fixture（AC14 要求不少于 8 条，实际 9 条）**：

1–5. 五个源头各自删除后跑 `--write`，断言诊断含 `missing source:` 与被删文件的相对路径（`VERSION` / `.ai/MILESTONES.md` / `Coder/README.md` / `workflows/registry.json` / `tools/`）。
6. 生成后手改任意一节正文，断言 `--check` 退出码非 0 且诊断含 `overview section drift: <该节标题>`，且**不**报其他节。
7. 造一份超限内容，断言诊断含 `overview too large:` 与实测值。
8. 在 `.ai/invariants.md` 追加一条无真源指针的条目，断言诊断含 `invariants without source pointer: 17 > 16` 并列出该条标题。
9. `Coder/README.md` 删掉某目录的职责说明，断言诊断含 `directory has no description in Coder/README.md: <目录名>`。

另加正例 2 条：真实仓跑 `--check` 退出码 0；`--write` 两次结果逐字节相同（幂等，防非语义差异）。

**证据捕获**（`tools/verification-evidence/evidence.py run`，`--ac` 传逗号分隔列表）：

- `ac1-ac2-generate` (AC1,AC2)：`--write` 后逐节数字与源头实测比对的脚本
- `ac3-ac4-check` (AC3,AC4)：`--check` 正例 + 逐节篡改负例 + 超限负例
- `ac5-ac15-ci-audit` (AC5,AC15)：完整 `verify-ci.sh` + `audit-project-state.py --allow-unreleased`
- `ac6-ac7-invariants` (AC6,AC7)：条目数 47 不变、`git log --follow` 可追溯、两条修正的定向 grep
- `ac8-ratchet` (AC8)：文件头三条纪律在场 + 棘轮基线校验 + 加一条无指针条目的负例
- `ac9-ac10-frontier` (AC9,AC10)：两文件与目录不存在、变更流逐节处置段在场、`debt.md` 只有追加
- `ac11-order` (AC11)：`context_budget.py check` 退出码 0 + `order_bytes` 实测 + 重跑 ITER-0113 的 `ac2-projection-sha.py`
- `ac12-ac13-sweep` (AC12,AC13)：全仓残留字样零命中 + README/context-persistence/§5.4 登记在场的弱档代理
- `ac14-tests` (AC14)：`python3 -m unittest scripts.test_sync_project_overview` 全过

**置信档**：AC1–AC7、AC9、AC11、AC14 为 auto·可靠（确定性断言 + 实造负例）；AC8、AC10、AC12、AC13、AC15 为 auto·弱（机器只查得出写没写、指针在不在，判不了写得对不对）。无 human·待人 档。

## References Compliance

- 本迭代无 `.ai/references/` 外部参考资料，无外部引用合规项。
- 内部规则引用：新建脚本必须在 `Coder/README.md` 的驻留工具段注册（`CLAUDE.md` 第 3 条「不引入隐式依赖」）；`context-persistence.md` 补三份产物的性质分工与重算命令。
- 分层不破：本轮只动 SOP Core（40 上下文治理）与仓根 `.ai/` 状态层，不碰 Domain Profiles（10）与 Business Extension（99）。
- 产物链不破：本方案的每条设计决策都可追到 `.ai/AC_LIST.md` 的对应 AC，不新增未经 AC 覆盖的改动；D5 补 README 两行是 D2 第三节的前置条件，已在 Failure Paths 6 写明判断依据与退路。
- 模板 SSOT 不破：本轮不改 `templates/rule-card.md`，读序块仍以 `context-persistence.md §6` 为唯一真源、四处字节投影，投影同步由 `context_budget.py` 兜。但 D9 改读序正文意味着 `templates/AGENTS.md.template` 与 `templates/CLAUDE.md.template` 这两份注入目标项目的载体也跟着变，**照 `migration-schema.md §5` 的领域变更判据仍然命中 `[regen-entrypoints]`**。该要求 ITER-0113 已登记且至今未发布，本轮不重复开新条目，只在 §5.4 的 R2 登记后追记一句「R3 再次改动同两份模板，要求不变」。
