---
状态: ack-frozen
ACK 日期: 2026-08-20
修订记录: 2026-08-19 · ② AC12 的「零命中」口径改为「零活引用」，并剔除无法达成的裸 `frontier` 字样——Decision Map 的 `frontier`（依赖 DAG 可推进前沿）与本轮退役的知识文件同名不同物，且迁出留痕本身必须提到旧文件名。｜ 2026-08-19 · ① AC2 的驻留工具计数由「24 项」改为「与 `tools/` 实际子目录一致，当前 22」——冻结时的 24 把 `ls` 输出里的 `.` 与 `..` 数进去了；同时把硬编码数字换成对源头的引用。影响面未变。
---
<!-- butler-artifact-template: 1.0.0 artifact=acceptance -->
# AC_LIST — ITER-0114

## Goal

- 把「项目整体长什么样」这件事重新变成一份可信产物，且这次按内容性质分家落地：可从机器源头派生的事实进 `.ai/OVERVIEW.md`，由一条命令生成、CI 比对，人不许手改；机器算不出来的长期决策与理由进 `.ai/invariants.md`，纯追加并补上「只写理由、指向真源、不复述机制形状」的纪律；会过期的判断进 `.ai/debt.md`，本来就有还清的路径。三份各自单一性质，`.ai/project/` 与 `frontier.md` 随之退役。

## In Scope

- 新建 `scripts/sync-project-overview.py`，`--check` / `--write` 二选一 + `--project-root` / `--butler-root`（沿用 `sync-workflow-registry.py` 的形状）。从五个现成机器源头派生：`VERSION`、双台账 `.ai/ITERATIONS.md` / `.ai/MILESTONES.md`（含 `.ai/state-index.json` 的冷片计数）、`Coder/README.md` 的目录结构与职责、`workflows/registry.json` 的 Router + 13 个业务工作流、`tools/` 目录清单。
- 生成 `.ai/OVERVIEW.md`：全文由生成器写，页首挂「本页由 … 生成，请勿手改」，正文不含任何手写槽位；体量设上限并机器校验。
- `--check` 模式进 `scripts/verify-ci.sh`：生成结果与磁盘不一致即非零退出，诊断指名是哪一节对不上。
- `git mv .ai/project/invariants.md .ai/invariants.md`，内容原样迁移；同批修两条已被证伪的条目（第 47 行收口仪式五步→四步、第 42 行冷启动读序四步→R2 的五步语义阶段），并在文件头补写作纪律：只写决策与理由、指向真源、不复述机制的具体形状（步数 / 清单 / 顺序）。
- 无真源指针的条目加棘轮：现存 16 条豁免并在文件头登记，机器校验其数量**不得增加**；新增条目必须至少带一个反引号真源指针。
- 退役 `frontier.md`：三节逐节处置并留痕——「当前形态」「活跃战线」里可派生的并入 `OVERVIEW` 生成段，「下一个瓶颈」里仍成立的判断迁入 `.ai/debt.md`，其余逐条写明为何可弃（照 ITER-0112 删 `capabilities.md` 的逐节核查格式）。
- 删空并移除 butler 仓自己的 `.ai/project/` 目录。
- 读序第 5 步补一句按需指针，点名 `.ai/OVERVIEW.md` 与 `.ai/invariants.md`；改真源一处、四处投影同步，读序块体量仍须在 1400 字节上限内。
- `.ai/MILESTONE.md §5.4` 登记两条前提修正：`frontier.md` 实测已漂移两个迭代（整体覆写要有强制触发才活得下来）、`invariants.md` 实测有两条已假（纯追加不保证旧条目描述的东西没变）。
- `Coder/README.md` 注册新脚本；`Coder/40_Context_Management/context-persistence.md` 写清三份产物的性质分工与重算命令。

## Out of Scope

- 不把全貌产物接回任何 delta 折叠机制，不为它做原地重评（里程碑两条硬边界）。
- 不新建采集：只读现有机器源头，不改 `registry.json` / 双台账 / `tools/` / `Coder/README.md` 的结构与字段。
- 不做部署侧接线：不改 `mcv-deployment.md` 的部署种子、不动升级器动作与迁移配方；已部署项目何时拿到新产物归 R15，本轮只登记。
- 不动 `.ai/project/workspaces.md` 这个路径规格——它是目标项目侧 PRD / 工作区机制的落点，butler 仓自己没有这个文件；该路径的去留归 R9 根布局整理。
- 不改 R2 定的读序五步语义结构（只在第 5 步内加指针文字，不增删步骤）。
- 不改 `.ai/debt.md` 既有条目的格式与语义，只追加。
- 不回头补那 16 条缺指针条目的真源（棘轮只防增量）。
- 不动 `/butler:progress`（R4）、`/butler:loop`（R5）、旧 inbox 全链（R8）、根布局改名与迁位（R9）、升级器动作类型（R14）、v4.0.0 迁移配方（R15）。
- 不切版、不发布。

## Acceptance Checklist

- [ ] AC1: `scripts/sync-project-overview.py` 存在且 `--check` 与 `--write` 互斥、`--project-root` 与 `--butler-root` 可分别指定；五个机器源头全部实际读取——删掉任一源头文件后 `--write` 报错并指名缺的是哪一个，不静默产出残缺页。
- [ ] AC2: `--write` 生成的 `.ai/OVERVIEW.md` 页首含「请勿手改」与生成命令原文；全文无手写标记区；内容至少覆盖五节——版本与当前活跃状态、里程碑时间线、规则体系目录与职责、工作流清单（Router + 13）、驻留工具清单（数量与 `tools/` 实际子目录一致，当前 22），每节的数字与其机器源头实测一致。
- [ ] AC3: `--check` 在磁盘与生成结果一致时退出码 0；手工改动 `.ai/OVERVIEW.md` 任意一节后退出码非 0，且诊断指名是哪一节不一致，不只说「文件有差异」。
- [ ] AC4: `.ai/OVERVIEW.md` 体量不超过 12000 字节，上限写死在生成器常量里并在 `--check` 时校验；超限时诊断给出实测值与上限。
- [ ] AC5: `scripts/verify-ci.sh` 含 `sync-project-overview.py --check` 一行，位置与其他 `--check` 类检查一致；完整 CI 退出码 0。
- [ ] AC6: `.ai/invariants.md` 存在且 `.ai/project/invariants.md` 不存在；迁移前后条目数一致（47 条），除下述两条修正外正文逐条未改（`git log --follow` 可追溯为迁位而非重写）。
- [ ] AC7: 两条已证伪的条目改对——收口仪式那条写四步且第四步是自检（与 `iteration-schema.md §5.5` 一致，不再出现 fold receipt），冷启动读序那条写 R2 的五步语义阶段（与 `context-persistence.md §6` 一致）；两条都不再复述完整步骤清单，改为「指向真源 + 只说为什么」。
- [ ] AC8: `.ai/invariants.md` 文件头含写作纪律三条（只写决策与理由 / 必带真源指针 / 不复述机制的具体形状）与棘轮基线数字；机器校验无指针条目数不超过基线 16，超出时诊断列出新增的是哪几条。
- [ ] AC9: `.ai/project/frontier.md` 与 `.ai/project/` 目录均不存在；`frontier.md` 三节的处置在本迭代变更流里逐条留痕，每条注明去向（并入 OVERVIEW 生成段 / 迁入 `debt.md` / 可弃及理由），无一条无交代。
- [ ] AC10: `.ai/debt.md` 追加了从「下一个瓶颈」迁来的仍成立条目，且追加内容不改动既有条目；迁入项写明来源是 `frontier.md` 及迁入日期。
- [ ] AC11: 读序块第 5 步含 `.ai/OVERVIEW.md` 与 `.ai/invariants.md` 两个按需指针且措辞明确是「按需读」不是「必读」；五处载体仍逐字节相同，`context_budget.py check` 退出码 0 且 `order_bytes` 仍不超过 1400。
- [ ] AC12: 全仓活跃文件中不再有指向 `.ai/project/invariants.md` 与 `.ai/project/frontier.md` 的**活引用**（把它们当作现存产物去读、去写或要求读取的引用）；**叙述性提及**（迁出留痕、设计理由、历史记录）允许保留，但每一处都要能举出理由、逐处白名单登记。扫描面排除历史归档（`.ai/iterations/`、`.ai/history/`、`deliveries/`）、已发布的迁移配方（`migrations/`，改了 manifest 一致性校验会红）、本迭代自己的工作区产物与第三方依赖（`.venv/`）。Decision Map 的 `frontier` 是依赖 DAG 的可推进前沿，与本轮退役的知识文件同名不同物，不在清理范围。另需：`Coder/README.md` 已注册 `sync-project-overview.py`，`context-persistence.md` 写清三份产物的性质分工与重算命令。
- [ ] AC13: `.ai/MILESTONE.md §5.4` 含两条前提修正登记，各自写明实测证据（`frontier.md` 停更在 ITER-0111 且正文写 v3.5.1 / `invariants.md` 第 42、47 行已假）与修正后的规律表述。
- [ ] AC14: 新增 fixture 不少于 8 条，覆盖——五个源头各自缺失时报错指名（5 条）、手改任一节被 `--check` 抓到并指名（1 条）、体量超限（1 条）、无指针条目数超基线（1 条）；每条断言具体诊断字符串，不只断言非零退出。
- [ ] AC15: `scripts/audit-project-state.py --project-root . --allow-unreleased` 退出码 0，非 OK 行只剩两条 `UNRELEASED` 亮牌与历史诊断 `INFO`；交付总结如实记录一项覆盖面事实——`OVERVIEW` 的 `--check` 只能证明「生成段与机器源头一致」，证明不了「这份全貌被任何会话读过」，后者仍要等 R11 的运行时观测。

## Verification Method

- AC1: 逐个源头在临时副本上删除后跑 `--write`，断言诊断含被删文件名；`--check --write` 同传断言 argparse 报互斥。
- AC2: 生成后逐节比对——`VERSION` 字面、双台账里程碑行数、`Coder/README.md` 目录段条数、`registry.json` 的 `workflows` 长度、`ls tools/` 计数。
- AC3: 生成后逐节各改一处，断言 `--check` 退出码非 0 且诊断含该节标题。
- AC4: 读生成器常量与 `wc -c` 实测；另造一份超限 fixture 断言诊断含实测值与上限。
- AC5: `grep -c 'sync-project-overview' scripts/verify-ci.sh` 不小于 1；`bash scripts/verify-ci.sh` 退出码 0。
- AC6: `git log --follow --oneline .ai/invariants.md` 可见迁移前历史；`grep -c '^- \*\*'` 两侧均为 47；`git show` 对 diff 人读确认只改两条。
- AC7: 人读两条 + 定向 `grep` 断言不再含 `fold receipt` 与旧四步读序措辞。
- AC8: 脚本按 AC8 口径统计无指针条目数并与基线比对，故意加一条无指针条目断言报错并列出它。
- AC9: `test -e` 断言两者不存在；人读本迭代变更流的逐节处置段。
- AC10: `git diff` 确认 `.ai/debt.md` 只有追加、无既有行改动。
- AC11: `python3 tools/context-budget/context_budget.py check --project-root .` 退出码 0 且 metrics `order_bytes` ≤ 1400；ITER-0113 的 `ac2-projection-sha.py` 重跑仍全 OK。
- AC12: 扫描脚本按上述排除面跑 `grep -rn`，活引用零命中；叙述性提及逐处列在脚本的白名单里并注明理由，人读核对；人读 `Coder/README.md` 与 `context-persistence.md` 对应段落。
- AC13: 人读 `.ai/MILESTONE.md §5.4` 末两条。
- AC14: `python3 -m unittest` 跑新增测试目录，用例计数与诊断断言逐条核。
- AC15: 审计脚本退出码与输出留证；人读 `deliveries/ITER-0114-*.md` 对应段落。

## External References

- N/A（本迭代无 `.ai/references/` 外部参考资料）。

## Open Questions / Risks

- **风险 · 生成器读的是 butler 仓自己的源头，部署到目标项目未必成立**。`registry.json` / `Coder/README.md` / `tools/` 是规则仓的，双台账与 `VERSION` 才是项目侧的。本轮用 `--butler-root` 与 `--project-root` 分开传参把这层区分做进接口，但只在 butler 仓自己（两者相同）验证；目标项目场景不在本轮验收范围内，也不接部署链。这是有意的分期，不是遗漏——但要清楚：**本轮交付的是「butler 仓自己有全貌产物」，不是「所有部署项目都有」**。
- **风险 · 12000 字节上限是拍的，没有依据**。读序块的 1400 字节有依据（每次会话都付），全貌产物是按需读，没有同等的成本锚点。12000 大致是五节表格化内容的两倍余量，防的是 `capabilities.md` 那种无上限膨胀。真实合理值要等有人实际读过才知道，本轮先设一个能拦住失控的数。
- **风险 · 棘轮只防增量，16 条缺指针的旧账留着**。这 16 条恰恰是最容易悄悄变假的那批（它们复述了机制形状却没给可核对的真源）。本轮不补是为了不让迭代膨胀，但这笔账要进 `.ai/debt.md`，否则棘轮会变成「永久豁免」的体面说法。
- **待定 · `.ai/OVERVIEW.md` 到底进不进冷启动必读**。AC11 定的是「第 5 步按需指针」，即不必读。这么定是因为它 12KB 上限、比读序块贵一个量级。代价是「没人读」的风险坐实——生成得再准，不在必读路径上就可能永远不被打开。反过来如果进必读，每次会话成本立刻翻几倍，而且重蹈「陈旧的完整」的另一面「准确但没人要的完整」。倾向维持按需，P3 若有更省的折中（比如生成一段 300 字节的摘要进读序、全文按需）再议。
- **待定 · `frontier.md` 的「下一个瓶颈」有几条真能迁**。当前那节 6 条里，至少「远端 required check 未启用」「hook 共存合同缺失」「危险模式与 Loop 绑定」三条是真欠债、迁 `debt.md` 顺理成章；「MILE-0009 已随 v3.0.0 发布」这类是陈述事实不是瓶颈，该弃。逐条判定放 P4 执行时做，P3 只定判定口径。
