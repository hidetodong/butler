# ITER-0114 · 项目全貌产物重建：按内容性质分家（MILE-0016 R3）

- 交付级别：迭代交付（小版本）
- 收口日期：2026-08-20
- 所属里程碑：MILE-0016（Butler 瘦身与重造）

## 本次交付目标

「这个项目现在长什么样」这件事，butler 仓里原本靠 `.ai/project/frontier.md` 一份手写文件回答。开工前一核查，它已经停更两个迭代：正文写着版本 v3.5.1（实际 3.6.0）、写着「当前无 active 迭代」（实际 MILE-0016 与本迭代都在跑）。同一份复盘还判定 `.ai/project/invariants.md`「纯追加、一直准确」，实测也只对了一半——47 条里有两条已经假了。这一轮不是把这两份文件修一修，而是按内容性质拆成三份，各自装一种东西：机器算得出来的事实交给生成器 + CI 比对，机器算不出来的长期决策留给人写但上纪律，会过期的判断进本来就有还清路径的欠债表。

## 已完成内容

- 新建 `scripts/sync-project-overview.py`，从五个现成机器源头派生全貌：`VERSION`、双台账 `.ai/ITERATIONS.md` / `.ai/MILESTONES.md`（含 `.ai/state-index.json` 的冷片计数）、`Coder/README.md` 的目录结构与职责、`workflows/registry.json` 的 Router + 13 条业务工作流、`tools/` 目录清单。`--check` 与 `--write` 互斥必选，`--project-root` 与 `--butler-root` 分开传。
- 生成 `.ai/OVERVIEW.md`（收口时 8897 字节 / 五节 / 上限 12000）：版本与当前状态、里程碑时间线（16 行）、规则体系目录与职责（12 个目录）、工作流清单（Router + 13）、驻留工具清单（22 项）。全文由生成器写，页首挂「请勿手改」与生成命令原文，正文零手写槽位。
- 缺任意一个源头都在渲染前抛 `missing source: <路径>` 并拒绝出页——不产出残缺页比产出一份看起来完整的错页重要。`Coder/` 下的目录若在 `Coder/README.md` 里没有职责说明，同样 fail-closed；这一条当场逼出两个此前漏登记的目录（`55_Extension_ConvergenceLoop/` 与 `60_Extension_CodeReview/`），顺手补上。
- `--check` 逐节 sha256 比对，诊断指名 `overview section drift: <节标题>`，不是笼统一句「文件有差异」；另有节集不匹配、页首漂移、产物缺失三类各自的诊断。这一行进了 `scripts/verify-ci.sh`，和 artifact-pipeline、context-budget、domain-contract 三组排成同一类「先跑测试、紧跟 --check」的成对形状。
- `git mv .ai/project/invariants.md .ai/invariants.md`，47 条正文原样带走（git 记为 R100 全等重命名）。文件头补三条写作纪律：只写决策与理由不复述机制形状、每条至少一个反引号真源指针、还成立才留作废即删。
- 两条已被证伪的条目改对：「收口是原子仪式」删掉五步清单与早已作废的 `fold receipt`，改为指向 `iteration-schema.md §5.5`；「冷启动读序固定」删掉旧四步措辞，改为指向 `context-persistence.md §6` 的读序块。两条都只留「为什么」那半。
- 无真源指针的条目上棘轮：基线 16 写死在生成器常量里，`--check` 卡住不许再增，超基线时把全部无指针条目逐条列进诊断。基线同时以欠账形式记进 `.ai/debt.md`，防止它变成「永久豁免」的体面说法。
- 退役 `.ai/project/frontier.md`，三节 28 条逐条处置并写进本迭代变更流：可派生的并入 `OVERVIEW` 生成段，仍成立的判断迁进 `.ai/debt.md`（4 条），其余逐条写明为何可弃。`.ai/project/` 目录随之删空移除。
- 读序块第 5 步补一句按需指针，点名 `.ai/OVERVIEW.md` 与 `.ai/invariants.md`，措辞明确是「按需读，不是必读」。真源改一处、四处投影同步，五处仍逐字节相同，块体量 1284 字节（上限 1400）。

## 关键变更 / 用户可感知变化

- **全貌产物从此不会烂，因为有东西强制它重写**。源头一动，CI 就红并指名是哪一节对不上。这正是 `frontier.md` 缺的那半——它靠折叠仪式驱动整体覆写，MILE-0016 R1 删掉仪式，覆写随之停止，没有任何机器检查发现得了。
- **`.ai/OVERVIEW.md` 不许手改**。要改内容得去改源头，然后跑 `python3 $BUTLER_PATH/scripts/sync-project-overview.py --write --project-root .` 重算。这条不是纪律劝导，是 CI 层面的硬约束。
- **写不变量的规矩变了**：往 `.ai/invariants.md` 加条目必须带一个反引号真源指针，且不许复述步数、清单、顺序。复述了形状，机制一改这条就假——实测已经这样假掉过两条。
- **`.ai/project/` 在 butler 仓自己已经没有了**。但这个路径仍是目标项目侧 `workspaces.md` 的规格落点，名字已名不副实，去留归 MILE-0016 R9。
- **冷启动每次会话多付 90 字节**（读序块 1194 → 1284）。换来的是新会话知道全貌产物在哪、并且知道它是按需读不是必读。

## 高层影响范围

- 新增 3 份：`scripts/sync-project-overview.py`（生成器）、`scripts/test-sync-project-overview.py`（合成夹具单测）、`.ai/OVERVIEW.md`（生成物）。
- 迁位 1 份：`.ai/project/invariants.md` → `.ai/invariants.md`，另加文件头纪律与两条修正。
- 退役 2 项：`.ai/project/frontier.md`、`.ai/project/` 目录。
- 规则与注册 2 处：`Coder/README.md`（补两条缺失的目录说明 + 注册生成器）、`Coder/40_Context_Management/context-persistence.md`（三份产物的性质分工表、重算命令、`frontier.md` 的教训）。
- 读序五处载体同步：`context-persistence.md §6`（真源）、`AGENTS.md`、`Coder/README.md`、`templates/AGENTS.md.template`、`templates/CLAUDE.md.template`。后两份是部署入口模板，本轮再次改动，`[regen-entrypoints]` 的发布要求按 R2 已登记的不变。
- 机器侧 3 处：`scripts/verify-ci.sh`（新增两行）、`tools/context-budget/context_budget.py`（必读清单改路径）、其测试套（夹具路径 + 读序基线 1284 / 9 指针）。
- 台账 2 处：`.ai/debt.md` 追加 6 条（4 条迁入 + 2 条新记，既有 3 条零改动）、`.ai/MILESTONE.md §5.4` 登记两条前提修正与一条发布处置追记。
- 未触碰：`registry.json` / 双台账 / `tools/` / `Coder/README.md` 的结构与字段（只读不改）、部署种子与升级器动作、`.ai/project/workspaces.md` 这个路径规格、读序的五步语义结构。未切版、未发布。

## 验证方式与结果摘要

- 15 条验收标准全部达成，10 条机器证据全部 passed。
- 负例是实打实造出来的：五个源头各自删掉后 `--write` 报错指名并确认不产出残缺页；`.ai/OVERVIEW.md` 五节各改一处后 `--check` 指名该节且不连坐其他四节；节标题改名报节集不匹配；产物整个删掉报 missing；400 个合成工具目录撑爆 12000 字节上限后诊断给出实测值与上限且不写盘；加第 17 条无指针不变量被棘轮拦下并列出条目，删一条则放行——棘轮只往紧的方向走。
- 单测 10 个方法覆盖 11 个负例场景 + 3 个正例，每条断言的都是具体诊断串，没有一条只断言非零退出。
- 完整 `scripts/verify-ci.sh` 退出码 0，状态审计 `--allow-unreleased` 退出码 0。
- 技术方案里估的「新增 fixture 不少于 9 条」是估数，实际是 10 个测试方法覆盖 11 个负例场景；验收标准的真实门槛是「不少于 8 条」，达标。这里如实记下估数与实测的差，没有回头改方案。
- 两条验收标准在执行中发现有缺陷，按 `iteration-schema.md §5.3` 走了 amend 退回重 ACK，没有偷偷改冻结后的标准：AC2 的「驻留工具 24 项」是把 `ls` 输出里的 `.` 与 `..` 数了进去，实际 22；AC12 的「零命中」口径无法达成——Decision Map 的 `frontier`（依赖 DAG 的可推进前沿）与本轮退役的知识文件同名不同物，且迁出留痕本身必须提到旧文件名，故改为「零活引用 + 叙述性提及逐处白名单登记」。
- **一项覆盖面事实**：`--check` 只能证明「`.ai/OVERVIEW.md` 的生成段与机器源头一致」，证明不了「这份全貌被任何会话读过」。生成得再准，它不在冷启动必读路径上（AC11 定的是按需指针），就可能永远不被打开。这半个证明要等 MILE-0016 R11 的运行时观测。

## 已知剩余风险 / 延后事项

- **生成器读的是 butler 仓自己的源头，部署到目标项目未必成立**。`registry.json` / `Coder/README.md` / `tools/` 是规则仓的，双台账与 `VERSION` 才是项目侧的。接口层面已用 `--butler-root` 与 `--project-root` 分开传参把这层区分做进去，但只在两者相同的 butler 仓自己验过。本轮交付的是「butler 仓自己有全貌产物」，不是「所有部署项目都有」——后者归 R15。
- **12000 字节的上限是拍的**。读序块的 1400 有依据（每次会话都付），全貌产物按需读，没有同等的成本锚点。12000 大致是当前内容的两倍余量，防的是无上限膨胀那类失控，真实合理值要等有人实际读过才知道。
- **16 条无指针的旧账留着**。这批恰恰是最容易悄悄变假的一类——复述了机制形状却没给可核对的真源，实测已有两条假掉。棘轮只防增量，逐条补真源的活儿没做，已记进 `.ai/debt.md`。
- **`iteration-schema.md §5.3` 与产物合同打架，本轮绕过去了**。§5.3 要求 amend 时在 `AC_LIST.md` 顶部追加「修订记录」，但产物合同只允许固定七个二级标题，`## 修订记录` 加进去就 drift。本轮把它写进 frontmatter，ITER-0112 的 amend 则是直接改正文没留记录——两次绕法不一致，已记进 `.ai/debt.md`，要么放宽合同要么改 §5.3 措辞。
- **`.ai/project/` 这个名字还在目标项目侧活着**。butler 仓自己删干净了，但 `workspace-scope-schema.md` 仍把 `.ai/project/workspaces.md` 当作规格落点，名不副实，归 R9 根布局整理。

## 引用

- `.ai/iterations/ITER-0114/CONCEPT.md`
- `.ai/iterations/ITER-0114/AC_LIST.md`
- `.ai/iterations/ITER-0114/TECH_PLAN.md`
- `.ai/iterations/ITER-0114/VERIFY_REPORT.md`
- `.ai/iterations/ITER-0114/CHANGELOG.md`
- `.ai/iterations/ITER-0114/evidence/`
- `.ai/OVERVIEW.md`
- `.ai/invariants.md`
- `.ai/debt.md`
- `scripts/sync-project-overview.py`
