<!-- butler-artifact-template: 1.0.0 artifact=verify_report -->
# VERIFY_REPORT — ITER-0115

## Verification Summary

- 14 条验收标准全部达成。9 条机器证据（`ac1-ac2-entities` / `ac3-ac4-registry` / `ac5-router-example` / `ac6-ac7-assertions` / `ac8-ac9-docs` / `ac10-overview` / `ac11-ac12-sweep-final` / `ac13-registration` / `ac13-ac14-ci-audit`）全部 passed，另有一条 failed 记录 `ac11-ac12-sweep` 按证据不可覆盖的规矩留存（见下方 Verification Results 第一条）。
- 置信档分布：AC1–AC7、AC10–AC12、AC14 为 auto·可靠（确定性断言，且大部分是既有 CI 断言而非本轮自造）；AC8、AC9、AC13 为 auto·弱档——机器只查得出旧表述没了、新表述在、登记段落在不在，判不了改后的话写得对不对，那部分靠人读 `git diff`。无 human·待人 档，与 TECH_PLAN 的预判一致。
- 本轮无验收标准修订：没有走 `iteration-schema.md §5.3` 的 amend，AC_LIST 自 2026-08-20 ACK 后一字未改。有三处「实测与措辞不完全对齐」，都在下方 Verification Results 逐条如实记明，无一处构成需求变化。
- **最该记住的一条**：本轮设计的扫描模式漏掉了两处裸数字断言，是跑完整 CI 才暴露的。扫描器守得住有语义前缀的表述，守不住 `assertEqual(13, ...)` 这种光秃秃的数字——这个局限已写进 Remaining Risks。

## AC Status

- [x] AC1 (auto·可靠): 三个实体全部消失——`.claude/commands/butler/progress.md`、`plugins/butler/skills/butler-progress/`、`.agents/skills/butler-progress` 逐个 `test -e` 为假。`.agents/skills/` 剩 13 条软链（Router + 12 业务），逐条 `test -e "$link/SKILL.md"` 全部指向存在的文件、无断链；`plugins/butler/skills/` 实体目录同为 13 个，两侧对得上。证据 `ac1-ac2-entities`。
- [x] AC2 (auto·可靠): `workflows/registry.json` 的 `workflows` 长度 12，ID 集合实测为 `inbox / prd / review / milestone / upgrade / init / setup / ideation / preference / loop / dangerous / iteration`，无 progress；全文零 `progress` 字样。`review` 的 `routing.negative_triggers` 由两条清为空数组——**删的是两条不是一条**，口径说明见 Verification Results。其余 12 个工作流块 `git diff` 逐字段未动。证据 `ac1-ac2-entities`。
- [x] AC3 (auto·可靠): `scripts/sync-workflow-registry.py` 的 `EXPECTED_IDS` 实测 12 项且不含 progress；长度校验由写死的 `!= 13` 改为 `!= len(EXPECTED_IDS)`，不再有第二个需要人记得改的数字。`--check` 退出码 0，对账覆盖 `workflows=12 projections=53`。证据 `ac3-ac4-registry`。
- [x] AC4 (auto·可靠): `docs/workflows.md` 由 `--write` 重算，工作流表 12 行、无 progress 行；安全段文案为「其余 10 项」、分发状态表为「Router + 12 个业务 Skill」，两处都已改成从 registry 派生而非硬编码；页首「请勿手改」声明保留；再跑一次 `--write` 逐字节不变（幂等）。`git diff` 恰好三行变化，无非语义 diff。**AC 原文写的是「其余十项」、实际产出「其余 10 项」**，口径说明见 Verification Results。证据 `ac3-ac4-registry`。
- [x] AC5 (auto·可靠): `workflows/router-examples.json` 里「现在项目进度怎么样」这条请求文字仍在，`expected_status` = `not-butler`、`expected_primary` = `null`、`expected_state_writes` = `false`；样例文件全文零 progress 字样。覆盖校验断言样例集仍覆盖全部 12 个工作流 ID，无缺无余——没有因为改这一条而漏掉某个 ID 的覆盖。证据 `ac5-router-example`。
- [x] AC6 (auto·可靠): 三处机器断言各自跑绿——`bash scripts/verify-codex-workflows.sh` 退出码 0 且结尾报 `(Router + 12 workflow skills)`，两处 names 名单已去 progress；`scripts/test-workflow-registry.py` 数量断言为 12、13 个用例全过；`pytest tools/project-config/tests` 31 passed，`test_consumers.py` 零 progress 路径、progress 专属测试方法已删，且反向断言 dangerous / preference / review 三个消费者仍被覆盖（没有误删同元组的邻居）。证据 `ac6-ac7-assertions`。
- [x] AC7 (auto·可靠): `plugins/butler/.codex-plugin/plugin.json` 的 `longDescription` 已去 progress，`name` 与 `skills` 两个字段未动；官方固定版 plugin validator 与全部 skill validator 通过，含实体数量断言 13。证据 `ac6-ac7-assertions`。
- [x] AC8 (auto·弱档): `README.md` 能力表那行是**纯删**——本轮 diff 实测 +0 / -1，没补任何替代说法，全文无 `/butler:progress`。三份散文计数收敛到位：`HUMAN_GUIDE.md` 旧表述零命中、新表述 3 处；`Coder/README.md` 1 处；`docs/codex-compatibility.md` 1 处，数量与 AC 声明逐份对上。证据 `ac8-ac9-docs`。
- [x] AC9 (auto·弱档): `.ai/invariants.md` 条目总数仍 47，本轮 diff 恰好 2 增 2 删，只动了那两条。两条都通过三项断言：不再出现任何工作流个数、带反引号真源指针（`workflows/registry.json` 与 `plugins/butler/skills/`）、保留原有的 `*为什么*` 半句。无真源指针条目的棘轮未触发（`sync-project-overview.py --check` 内含该校验，退出码 0）。证据 `ac8-ac9-docs`。
- [x] AC10 (auto·可靠): `.ai/OVERVIEW.md` 由 `--write` 重算，`--check` 退出码 0，体量 8798 字节（上限 12000），工作流清单 12 行、全文零 progress。diff 是 3 增 4 删：progress 那行消失是本轮结果，另三行（active 迭代 none → ITER-0115、累计迭代 114 → 115、MILE-0016 含迭代 3 → 4）是台账推进的正常跟随，不是误改。证据 `ac10-overview`。
- [x] AC11 (auto·可靠): 全仓 394 个文本文件，四个活引用模式（`/butler:progress`、`$butler-progress`、`butler-progress`、`commands/butler/progress.md`）命中数 0。排除面按 AC 写死，另加四个同性质目录与 13 份本迭代工作区状态文件——**后一组里有 41 处叙述性提及**，都是删除动作本身的记录，逐项摊开在 Verification Results，不是暗中放行。证据 `ac11-ac12-sweep-final`。
- [x] AC12 (auto·可靠): 同一脚本第二组模式（`Router + 13`、`13 个业务`、`13 workflow skills`、`其余十一项`）在同一排除面下命中数 0；脚本可重跑，有命中时逐条打印文件与行号而不只报总数，模式串用变量拼接因而不命中自身。证据 `ac11-ac12-sweep-final`。
- [x] AC13 (auto·弱档): `.ai/MILESTONE.md §5.4` 末两条登记在场且写到位——登记一点明 registry 的 `rule_source` 指回命令文件自身、`templates/rule-card.md` 全文未提 progress，并明确表态「如实记为不适用」；登记二写明 Claude 侧是软链删即生效、Codex 个人安装是拷贝需要 `[global-install]`、本轮不触发 `[regen-entrypoints]`、清理归 R15。证据 `ac13-registration`（同样的断言也在 `ac13-ac14-ci-audit` 里跑过，那条记录的机器绑定漏了 AC13，说明见 Verification Results）。
- [x] AC14 (auto·可靠): `bash scripts/verify-ci.sh` 退出码 0；`python3 scripts/audit-project-state.py --project-root . --allow-unreleased` 退出码 0，非 OK 行只剩两条 `UNRELEASED` 发布态亮牌（工作树有未发布改动、v3.6.0 不指向 HEAD）与 26 条历史迭代的 `INFO` 诊断留存行，零 `DRIFT` / `ERROR`。证据 `ac13-ac14-ci-audit`。

## 人测道小结

- N/A（本轮无 human·待人 档 AC，人测道不适用）。AC8、AC9、AC13 三条本可归人测，但都能造出弱检查（旧表述在不在、条目数变没变、登记段落写没写），按 `testing-strategy.md §3` 仍归自动道弱档；判「改后的话写得对不对」那半靠人读 `git diff`，本轮改动面小（invariants 2 行、散文 5 处、README 1 行），逐行读过。

## Evidence Index

| Evidence ID | AC | 强度 | Outcome | Record |
|---|---|---|---|---|
| ac1-ac2-entities | AC1,AC2 | reproduced | passed | `.ai/iterations/ITER-0115/evidence/ac1-ac2-entities/record.json` |
| ac3-ac4-registry | AC3,AC4 | reproduced | passed | `.ai/iterations/ITER-0115/evidence/ac3-ac4-registry/record.json` |
| ac5-router-example | AC5 | reproduced | passed | `.ai/iterations/ITER-0115/evidence/ac5-router-example/record.json` |
| ac6-ac7-assertions | AC6,AC7 | reproduced | passed | `.ai/iterations/ITER-0115/evidence/ac6-ac7-assertions/record.json` |
| ac8-ac9-docs | AC8,AC9 | captured | passed | `.ai/iterations/ITER-0115/evidence/ac8-ac9-docs/record.json` |
| ac10-overview | AC10 | reproduced | passed | `.ai/iterations/ITER-0115/evidence/ac10-overview/record.json` |
| ac11-ac12-sweep | AC11,AC12 | reproduced | failed | `.ai/iterations/ITER-0115/evidence/ac11-ac12-sweep/record.json` |
| ac11-ac12-sweep-final | AC11,AC12 | reproduced | passed | `.ai/iterations/ITER-0115/evidence/ac11-ac12-sweep-final/record.json` |
| ac13-registration | AC13 | captured | passed | `.ai/iterations/ITER-0115/evidence/ac13-registration/record.json` |
| ac13-ac14-ci-audit | AC14 | reproduced | passed | `.ai/iterations/ITER-0115/evidence/ac13-ac14-ci-audit/record.json` |

## Verification Results

- **留了一条 failed 记录，不是没修好，是修好之后不许覆盖**。`ac11-ac12-sweep` 第一次捕获时红了，原因是扫描器扫到了自己刚被捕获的输出——`.ai/verification-evidence/*/stdout.log` 里逐字记着 `butler-progress` 这些模式串。这是自指假红，不是仓里真有活引用。修法是把 `.ai/verification-evidence` 加进排除面（性质与 `.ai/iterations/` 相同：本迭代工作区产物，不是活接线）。`evidence.py` 明令「evidence ID 已存在，禁止覆盖」，所以红记录原样留着，通过的那次以 `ac11-ac12-sweep-final` 另立一条。仓里对这类留存有先例——`audit-project-state.py` 会把它报成 `[INFO] 保留非通过记录`，不是漂移。
- **`ac13-ac14-ci-audit` 的机器绑定漏了 AC13**。捕获时把 `--ac` 传了两次（`--ac AC13 --ac AC14`），而这个参数收的是单个逗号串，argparse 只留下最后一个，`record.json` 的 `ac_ids` 因此只有 `AC14`。脚本本身跑的是两条 AC 的断言，stdout 里都在。同样因为不许覆盖，没有回头改这条记录，而是给 AC13 另写了一条只做 §5.4 登记断言的 `ac13-registration.sh` 单独捕获。两条记录有一小段重叠断言，是这次绑定失误的代价，不是重复验证。
- **AC4 写「其余十项」，实际产出「其余 10 项」**。同一个数，中文数字与阿拉伯数字的差别。已 ACK 的 TECH_PLAN D4 明确写了「中文数字『十一』换成阿拉伯数字，中文数字要额外写个转换函数、不值得，而且表格里本来就是阿拉伯数字」——执行遵的是方案。AC 那句是描述性措辞，不构成需求差异，故未走 §5.3 amend；记在这里，不掩盖。
- **`review` 删的是两条负向触发词，AC 只点名了一条**。实测 `negative_triggers` 是 `["project status", "项目进度"]`，AC2 只写了「项目进度」。两条一并删，理由同一个：它们存在的唯一作用是把「看看现在怎么样」这类请求推离 review、推向 progress，progress 一死就都指向不存在的目标。留着「project status」而删掉「项目进度」会让这条规则一半有理由一半没理由。这个判断已写进 `.ai/MILESTONE.md §5.4` 的 R4 登记里。
- **In Scope 说「摘 3 处 progress 路径」，实际 4 个编辑点**。TECH_PLAN D9 在动手前就预告了这处：`test_consumers.py` 的编辑点是 `READERS` 元组 2 条、`test_commands_surface_source_conflicts_and_legacy_write_boundary` 的路径 1 条，外加整个 `test_progress_version_does_not_come_from_project_config` 方法（内含 2 条路径），净删 14 行。影响面没变——同一个文件、同一个意图，AC6 的绑定条件写的是「不再含任何 progress 路径」，仍然精确。
- **两处硬编码计数是跑完整 CI 才发现的，本轮的扫描器抓不到**。`scripts/test-goal-host-wiring.py:49` 的 `assertEqual(13, len(registry["workflows"]))` 与 `tools/codex-validators/test_vendored_validators.py:80` 的 `assertEqual(len(skills), 14)`，写的都是光秃秃的数字，没有「个业务」「workflow skills」这类语义前缀，AC12 设计的四个模式一个也匹配不上。是 `verify-ci.sh` 先后报了 `13 != 14` 与 `13 != 12` 才暴露出来。这说明散文扫描和断言扫描是两类问题，本轮只解决了前者。
- **排除面比 AC11 列的多，逐项都属于 AC 原文的类目，这里全数摊开**。AC11 写死的是 `.ai/iterations/`、`.ai/history/`、`deliveries/`、`migrations/`、`.venv/`、`.git/`，另加一句「本迭代工作区产物」。脚本把后面这句落成了两组具体排除，都该写明：
  - 目录级另加四项：`.pytest_cache`、`node_modules`、`.ai/.artifact-migration-backups`、`.ai/verification-evidence`（最后一项是本次扫描自己被捕获的输出）。
  - 文件级排除本迭代的四件套、变更流与状态台账共 13 份：`.ai/CONCEPT.md`、`.ai/AC_LIST.md`、`.ai/TECH_PLAN.md`、`.ai/VERIFY_REPORT.md`、`.ai/01_CHANGELOG.md`、`.ai/task-state.md`、`.ai/02_SESSION_HANDOFF.md`、`.ai/handoff-state.json`、`.ai/ITERATIONS.md`、`.ai/MILESTONE.md`、`.ai/RUN_LOG.md`、`.ai/00_IDEATION.md` 与其 HTML。**这一组里确实有 41 处 `progress` 字样**（收口时实测：四件套 26 处、变更流 5 处、双台账与 task-state / handoff 共 10 处），全部是「这个东西被删了、怎么删的、为什么删」的记录本身——把删除写清楚就必然要提到被删对象的名字，和 ITER-0114 的 AC12 撞上的是同一个问题，处置口径也一样：零活引用，叙述性提及登记在案。
  - 反向确认白名单没在掩护真东西：机器接线面——`workflows/`、`scripts/`、`tools/`、`plugins/`、`.claude/`、`.agents/`、`templates/`、`Coder/`、`docs/` 与仓根人读文档——全部在扫描面内、逐个 0 命中。加排除项之前的那次运行，命中也全部来自 `.ai/verification-evidence` 的自指，源码与规则文档里一处也没有。
- **`.ai/debt.md` 追加的那一行在 AC 覆盖之外**。TECH_PLAN D8 已预告：D7 第三档（三份人读手册里的数字保留具体值）留了个真缺口，下次增删工作流照样会漏改。没往 CI 里塞一条永久扫描是有意的——为一次性清理留一条永久检查，正是 MILE-0016 在砍的那类积累。这行 debt 是登记不是实现，性质与 AC13 的 §5.4 登记相同，此处如实回填。
- **这次砍是靠审计判断，不是靠使用数据**。没有「过去 90 天 `/butler:progress` 被调用几次」这类数据可依——装监视器是 MILE-0016 R11 / R12 的事。依据是：progress 读的每一份文件（`.ai/task-state.md`、双台账、`AC_LIST.md`、`VERIFY_REPORT.md`）都已在冷启动读序里，它做的只是转述聚合，而转述层自己不带任何校验，聚合得对不对没有机器能判。这个判断可能错；真发现需要，得按当时的需求重开一条链，不是复活旧的。交付总结按 AC_LIST 的风险条要求如实写明依据性质。

## TDD Pair Status

- N/A（TECH_PLAN 未声明 TDD cycle）。本迭代不新增单元测试——改的是既有断言的期望值（13→12、14→13、名单去一项），新写测试等于给「我改对了没」再套一层自己写的判断。验证力来自既有机器断言：`sync-workflow-registry.py --check`、`verify-codex-workflows.sh`、`test-workflow-registry.py` 与 `test_consumers.py`。

## Goal Calibration

- 当前无未闭合运行时信号（N/A）。开工前发现的两条前提偏差（路线图点名的「规则真源」与「rule-card 引用」在 progress 上不存在）已在 P1 阶段回流到 `.ai/CONCEPT.md` 与 `.ai/MILESTONE.md §5.4`，不作为遗留信号带出本迭代。

## Completion Inputs

- Review Verdict: pass
- Completion Blockers: none

## Gate Coverage

- 质量门禁：`bash scripts/verify-ci.sh` 退出码 0，无跳过、无单点豁免。本轮没有往 CI 里加任何新检查行（D8 的有意决定）。
- 状态审计：`python3 scripts/audit-project-state.py --project-root . --allow-unreleased` 退出码 0。非 OK 行为两条 `UNRELEASED` 发布态亮牌与 26 条历史迭代 `INFO` 诊断留存行，零 `DRIFT` / `ERROR`。OK 计数与 `INFO` 行数会随收口写盘继续变动（本迭代自己的 `ac11-ac12-sweep` 归档后也会加入 `INFO` 留存行），此处记录的是 `ac13-ac14-ci-audit` 捕获时刻的状态。
- 产物契约：四件套与变更流均通过 `tools/artifact-pipeline/contract.py` 的章节与字段校验。
- 生成投影自校验：`sync-workflow-registry.py --check`（12 个工作流 / 53 处投影）与 `sync-project-overview.py --check`（五节逐节 sha256 + 无指针条目棘轮）各自退出码 0。
- 官方固定版 validator：`verify-codex-workflows.sh` 内跑 plugin validator 与 13 个 skill validator，全部通过。

## References Compliance

- 本迭代无 `.ai/references/` 外部参考资料，无外部引用合规项需核（AC_LIST「External References」为 N/A）。
- **分层不破**：只动仓根的入口实体、注册表、生成投影与人读文档；`Coder/README.md` 的改动仅一处计数，不改结构与职责分工；`Coder/00_System_Prompt/workflow-router.md` 的路由算法未动，只删了被路由的目标。
- **产物链不破**：每条设计决策都能追到 AC；AC 之外的动作只有 D8 的一行 debt 追加与 D9 的措辞澄清，两者都已在 TECH_PLAN 正文预告并在此如实回填。
- **模板 SSOT 不破**：`templates/rule-card.md` 全文未提 progress，两份入口模板本轮未动。按 `migration-schema.md §5` 的判据，改动没有流进目标项目的 `CLAUDE.md` / `AGENTS.md`，故**本轮不触发 `[regen-entrypoints]`**；该结论已在 §5.4 登记。

## Remaining Risks

- **裸数字断言没有任何兜底，这是本轮最实的缺口**。AC12 的扫描器守的是有语义前缀的散文表述，`assertEqual(13, ...)` 这类光秃秃的数字它一个也抓不到——本轮两处都是靠 CI 报错才发现的。下次增删工作流，还是只能靠 CI 红了再回头找。真正的治法是让这类断言也从 registry 派生（像 `sync-workflow-registry.py` 那样），但那要逐个改测试文件，超出本轮范围。
- **三份人读手册的计数没有机器兜底**。已记入 `.ai/debt.md`，自然消解路径是 R12 的 usage 报告落地时本来就要重做工作流呈现层。这是有意接受的欠账，不是遗漏。
- **已部署的 Codex 侧会有一段不一致**。Claude 命令是软链、删了立刻全局生效；Codex 个人安装的 `butler-progress` 是拷贝，用户机器上还在，在 Codex 里仍能触发 `$butler-progress`，而它 SKILL.md 指的规则文件已经不存在。这段窗口有意接受，本轮只在 §5.4 登记，清理归 R15 的 `migrations/v4.0.0.md`（需要 `[global-install]`，即重跑 `scripts/setup.sh`）。本轮不做兼容降级、不留 deprecated 桩。
- **砍掉之后没有替代品，也没人验证过「不需要」**。问进度现在就是普通对话——AI 直接读 `.ai/task-state.md` 与双台账回答。这条路径没有任何机器检查保证它答得全（progress 原来至少有个固定的聚合口径）。会不会有人真的需要那份总览，要等 R11 / R12 的运行时观测才知道。
- **`review` 的负向触发词清空了，实际路由行为没有回归验证**。删掉的两条本来就是多余保险（review 的正向触发词与「项目进度」无词面重叠），但这个判断来自读规则，不是来自跑路由。`router-examples.json` 里那条改成 `not-butler` 的样例是唯一的回归钉子，它只钉住「不该进任何工作流」，钉不住「不该被 review 抢走」。

## Handoff / Next Step

- ITER-0115 收口，MILE-0016 R4 置 `closed`；`.ai/ITERATIONS.md` current 归 `none`。
- 下一项按里程碑路线是 MILE-0016 R5（`/butler:loop` 的降级与候办清理），本轮未触碰。
- 发布侧未动：未切版、未打 tag、未提交。下个发布版的迁移配方必须含 `[global-install]`（清理 Codex 个人安装的 `butler-progress` 副本，已在 §5.4 登记给 R15）；本轮**不**触发 `[regen-entrypoints]`。
