# ITER-0115 · 砍 /butler:progress 全链（MILE-0016 R4）

- 交付级别：迭代交付（小版本）
- 收口日期：2026-08-20
- 所属里程碑：MILE-0016（Butler 瘦身与重造）

## 本次交付目标

`/butler:progress` 做的事是把 `.ai/task-state.md`、双台账、`AC_LIST.md`、`VERIFY_REPORT.md` 聚合成一份「现在项目什么情况」的总览。问题是这些文件每一份都已经在冷启动读序里、每次会话本来就读得到，progress 只是在上面加了一层转述——而转述层自己不带任何校验，聚合得对不对没有机器能判。MILE-0016 砍的正是这类东西：占着入口、加着维护成本、却不产生新的确定性。这一轮把它整条链拿掉，业务工作流从 13 变 12。

顺手修掉的是这次删除暴露出来的一个老毛病：「13 个业务工作流」这个数字散在九个地方，删一个工作流就要手工改九处。本轮把生成投影那两处改成从注册表算出来，把不变量那两条的数字整个拿掉，剩下三份人读手册保留具体数字但把缺口记进欠债表。

## 已完成内容

- 删掉三个实体：`.claude/commands/butler/progress.md`（Claude 命令，122 行）、`plugins/butler/skills/butler-progress/`（Codex skill 整目录）、`.agents/skills/butler-progress`（仓库发现用的相对软链）。一律走 `git rm`，让 `git log --follow` 追得到是哪个迭代删的。
- 从 `workflows/registry.json` 摘掉整个 progress 工作流块。注册表是元数据真源，删了它，`docs/workflows.md`、命令与 skill 的 frontmatter、`.agents/skills/` 软链这些投影才会跟着重算。
- 清空 `review` 的负向触发词。实测那里有两条（`project status` 与 `项目进度`），存在的唯一作用是把「看看现在怎么样」这类请求推离 review、推向 progress；progress 一死，两条都指向不存在的目标，所以一并删。review 的正向触发词（`review`、`代码复核`、`产物复核`、`independent review`）跟「项目进度」没有任何词面重叠，这层保险本来就多余。
- 路由样例改写而不是删除。`workflows/router-examples.json` 里「现在项目进度怎么样」这条请求文字保留，期望结果改成 `not-butler`。删了等于把「问进度该怎么处理」这个回归一起丢掉；改期望反而把这次的结果钉成一条断言——以后谁把 progress 加回来、或者让别的工作流去接进度请求，这条样例会红。
- **把生成投影里的两个硬编码数字改成算出来的**。`scripts/sync-workflow-registry.py` 的文档模板原本写死「其余十一项」和「Router + 13 个业务 Skill」，现在分别由 `len(data["workflows"])` 与 `allow_implicit_invocation` 的计数派生；注册表长度校验也从写死的 `!= 13` 改成 `!= len(EXPECTED_IDS)`。以后再增删任何工作流，`docs/workflows.md` 的计数自动跟上。
- `.ai/invariants.md` 那两条不变量**不是把 13 改成 12，而是把个数整个拿掉**，改为「名单以 `workflows/registry.json` 为准」。个数正是 ITER-0114 刚立的写作纪律所说的「机制形状」——复述了形状，机制一改这条就假。条目总数仍 47，本轮 diff 恰好 2 增 2 删。
- 改齐五处机器断言：`scripts/verify-codex-workflows.sh`（两处名单 + 两处数量 + 结尾文案）、`scripts/test-workflow-registry.py`、`scripts/test-goal-host-wiring.py`、`tools/codex-validators/test_vendored_validators.py`、`tools/project-config/tests/test_consumers.py`（净删 14 行，含一整个 progress 专属测试方法）。另改 `plugins/butler/.codex-plugin/plugin.json` 的 longDescription。
- 四份人读文档收敛：`README.md` 能力表那行**纯删不补替代**（+0 / -1）；`HUMAN_GUIDE.md` 3 处、`Coder/README.md` 1 处、`docs/codex-compatibility.md` 1 处的「13 个业务」改为 12。
- 两份生成产物各跑一次写模式重算：`docs/workflows.md`（恰好三行变化）与 `.ai/OVERVIEW.md`（8798 字节，工作流清单 12 行）。顺序上先摘注册表条目再删实体文件——反过来生成器会因为注册表里还留着 progress 而找不到文件直接报错。
- 新写一条可重跑的扫描脚本 `.ai/iterations/ITER-0115/ac11-ac12-sweep.py`，一次守两组模式：progress 链的活引用、散文里会变假的计数表述。全仓 394 个文本文件，两组各 0 命中。扫描面排除历史归档、已发布迁移配方、第三方依赖，以及本迭代自己的四件套与状态台账——最后这组里有 41 处 `progress` 字样，全是「这东西被删了、怎么删的」的记录本身，机器接线面（`workflows/`、`scripts/`、`tools/`、`plugins/`、`.claude/`、`.agents/`、`templates/`、`Coder/`、`docs/` 与仓根文档）一处不漏地扫了、一处不剩。模式串用变量拼接，脚本不会命中自己。**它有意不接 CI**，理由见下一节。

## 关键变更 / 用户可感知变化

- **`/butler:progress` 与 `$butler-progress` 没有了，也没有替代品**。问进度现在就是普通对话——直接读 `.ai/task-state.md` 与双台账回答。`README.md` 那行没补任何替代说法：补了等于把砍掉的能力用文字续命，而 `/butler:milestone status` 只报里程碑、覆盖不了验收和风险，写上去反而误导。
- **Claude 侧立刻生效，Codex 侧不会**。Claude 全局命令是 `scripts/setup.sh` 建的软链，指向本仓文件，删了立刻全局失效；Codex 个人安装的是**拷贝**，你机器上的 `butler-progress` 副本还在，在 Codex 里仍能触发，而它 SKILL.md 指的规则文件已经不存在了。要清掉得重跑 `scripts/setup.sh`。这段窗口是有意接受的，正式清理归 MILE-0016 R15 的 `migrations/v4.0.0.md`（会带 `[global-install]` 动作）。
- **本轮不触发 `[regen-entrypoints]`**。`templates/rule-card.md` 与两份入口模板全文未提 progress、本轮未动，改动没有流进目标项目的 `CLAUDE.md` / `AGENTS.md`。
- **增删工作流的成本降了一半，但没降到零**。生成投影和不变量这两档以后自动跟随；三份人读手册里的数字仍要手工改，改漏了 CI 不会红。这个缺口已记进 `.ai/debt.md`——**没往 CI 里塞一条扫描是有意的**，为一次性清理留一条永久检查，正是 MILE-0016 在砍的那类积累。自然消解路径是 R12 的 usage 报告落地时本来就要重做工作流呈现层。

## 高层影响范围

- 删除 3 个实体 + 1 个注册表块 + 1 行能力表 + 1 个测试方法。
- 改动机器侧 6 处：`sync-workflow-registry.py`（3 处，其中 2 处是改成派生）、`verify-codex-workflows.sh`、`test-workflow-registry.py`、`test-goal-host-wiring.py`、`test_vendored_validators.py`、`test_consumers.py`。
- 改动元数据 3 处：`registry.json`（删块 + 清负向触发词）、`router-examples.json`（改期望）、`plugin.json`（longDescription）。
- 重算生成产物 2 份：`docs/workflows.md`、`.ai/OVERVIEW.md`。
- 改动人读与规则文档 5 处：`README.md`、`HUMAN_GUIDE.md`、`Coder/README.md`、`docs/codex-compatibility.md`、`.ai/invariants.md`。
- 台账 2 处：`.ai/debt.md` 追加 1 条、`.ai/MILESTONE.md §5.4` 登记 2 条。
- 未触碰：`Coder/00_System_Prompt/workflow-router.md` 的路由算法（只删被路由的目标）、`templates/` 下的规则卡与两份入口模板、已部署项目的升级路径、历史归档（`.ai/iterations/`、`.ai/history/`、`deliveries/`、`migrations/`）里对 progress 的既成事实记录。未切版、未发布、未提交。

## 验证方式与结果摘要

- 14 条验收标准全部达成，9 条机器证据 passed。完整 `scripts/verify-ci.sh` 退出码 0，状态审计 `--allow-unreleased` 退出码 0（非 OK 行只剩两条 `UNRELEASED` 发布态亮牌与历史迭代的 `INFO` 留存行，零漂移）。
- 验证力主要来自**既有**机器断言而不是本轮自造：注册表与全部投影对账（12 个工作流 / 53 处投影）、官方固定版 plugin 与 skill validator（13 个 skill 实体）、消费者契约测试 31 passed、注册表测试 13 passed。删除类改动最怕的是「删了一半」，这些断言正好卡的是数量与名单的一致性。
- 反向断言也做了：删掉那个 progress 专属测试方法后，专门断言 dangerous / preference / review 三个消费者仍被覆盖，确认没有误删同一个元组里的邻居。
- **留了一条红记录**。`ac11-ac12-sweep` 第一次跑红了，原因是扫描器扫到了自己刚被捕获的输出——证据目录的 `stdout.log` 里逐字记着那些模式串。这是自指假红，不是仓里真有活引用；把证据目录加进排除面后重跑通过。`evidence.py` 明令证据不许覆盖，所以红记录原样留着，通过的那次以 `ac11-ac12-sweep-final` 另立一条。
- **有两处硬编码计数是跑完整 CI 才发现的，本轮设计的扫描器抓不到**。`test-goal-host-wiring.py` 与 `test_vendored_validators.py` 里写的是光秃秃的 `assertEqual(13, ...)` / `assertEqual(len(skills), 14)`，没有「个业务」「workflow skills」这类语义前缀，四个扫描模式一个也匹配不上。是 CI 先后报了 `13 != 14` 与 `13 != 12` 才暴露的。散文扫描和断言扫描是两类问题，本轮只解决了前者。
- **这次砍是靠审计判断，不是靠使用数据**。没有「过去 90 天 progress 被调用几次」这类数据可依——装监视器是 MILE-0016 R11 / R12 的事。依据是「它读的每份文件都在冷启动读序里、转述层自己不带校验」。这个判断可能错；真发现需要，得按当时的需求重开一条链，不是复活旧的。
- 三处「实测与措辞不完全对齐」如实记在验证报告里，都不构成需求变化、也都没走 amend：验收标准写「其余十项」而实际产出「其余 10 项」（已 ACK 的技术方案明确要求换阿拉伯数字）；范围描述写「摘 3 处 progress 路径」而实际 4 个编辑点（技术方案 D9 动手前已预告）；证据 `ac13-ac14-ci-audit` 捕获时 `--ac` 参数传法错了、机器绑定只留下 AC14，故给 AC13 另立了一条绑定正确的记录。

## 已知剩余风险 / 延后事项

- **裸数字断言没有任何兜底，这是本轮最实的缺口**。扫描器守得住有语义前缀的散文，守不住 `assertEqual(13, ...)`。下次增删工作流，还是只能靠 CI 红了再回头找。治法是让这类断言也从注册表派生，但要逐个改测试文件，超出本轮范围。
- **三份人读手册的计数靠自觉**。已记进 `.ai/debt.md`，是有意接受的欠账不是遗漏。
- **已部署的 Codex 侧会有一段不一致**，直到用户重跑安装脚本。归 R15，本轮只登记，不做兼容降级、不留 deprecated 桩。
- **砍掉之后没人验证过「确实不需要」**。问进度现在没有任何机器检查保证 AI 答得全（progress 原来至少有个固定的聚合口径）。要等 R11 / R12 的运行时观测才知道。
- **负向触发词清空了，实际路由行为没跑过回归**。删掉的两条本来就是多余保险，但这个判断来自读规则不是来自跑路由。改成 `not-butler` 的那条样例是唯一的钉子，它钉住「不该进任何工作流」，钉不住「不该被 review 抢走」。
- **路线图给 R4 点名的六个落点里有两个不存在**。「规则真源」在 progress 上就是命令文件本身（注册表的 `rule_source` 指回自己），`templates/rule-card.md` 全文没提过 progress。这两项如实记为不适用，没有假装完成，登记在 `.ai/MILESTONE.md §5.4`。

## 引用

- `.ai/iterations/ITER-0115/CONCEPT.md`
- `.ai/iterations/ITER-0115/AC_LIST.md`
- `.ai/iterations/ITER-0115/TECH_PLAN.md`
- `.ai/iterations/ITER-0115/VERIFY_REPORT.md`
- `.ai/iterations/ITER-0115/CHANGELOG.md`
- `.ai/iterations/ITER-0115/evidence/`
- `.ai/MILESTONE.md`（§5.4 的两条 R4 登记）
- `.ai/debt.md`
- `.ai/invariants.md`
- `workflows/registry.json`
- `docs/workflows.md`
