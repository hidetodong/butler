<!-- butler-artifact-template: 1.0.0 artifact=verify_report -->
# VERIFY_REPORT — ITER-0119

## Verification Summary

16 条 AC 全绿，7 份自动道 evidence record 全部 `passed`，CI 与状态审计双 0。

本轮拆掉的东西：两份旧规则真源（`inbox-schema.md` / `inbox-workflow.md`）、整个 `tools/inbox/`（348 行的确定性扫描器）、合同测试 `test_inbox_contract.py`、CI 里那行调用、`test_inbox_workflow.py` 里那个随旧规则退役的用例、`test_mile0009_e2e.py` 开头那段 inbox 扫描。同时把项目根的 `origin/` 收进 `.ai/references/raw/`，`origin/` 这个目录名退出全部活跃面。

本轮守住的东西：「AI 对用户原件只读、不写不改不重命名不移动不归档不删除」这条纪律活了下来，换了主语没换语义，并且它跟合同测试的逐字配对**现场演过一次红**（把规则正文那句删掉 → 6 passed 变 1 failed，还原 → 6 passed）。`templates/hooks/` 下进摘要的 19 份文件**一个字节没动**，摘要仍是 `bd92a614f9582451ec3150d2c1113a2262bb874b97fd085adf6ad0ce7c91e56d`。

两件本轮做不到、如实记账而不假装做了的事：给原件只读加机器门禁（撞上切版顺序，见「Remaining Risks」第 1 条）、搬走已部署项目里残留的 `origin/` 与旧格式 `.ai/INBOX.md`（升级器没有删除与移动动作，归 R14 / R15）。

## AC Status

- [x] AC1 (auto·可靠): 两份旧规则真源在工作树中不存在（`git rm` 删除）；`Coder/README.md` 全文对 `inbox-schema` / `inbox-workflow` 零命中，目录树与职责段两处注册均已摘除。
- [x] AC2 (auto·可靠): `tools/inbox/` 整目录（含 `README.md`、`__init__.py`、`inbox.py`、`tests/`）不存在；`scripts/verify-ci.sh` 对 `inbox` 零命中；活跃面对 `tools/inbox` 与 `tools.inbox` 两个字样零命中。
- [x] AC3 (auto·可靠): `test_inbox_contract.py` 不存在；`test_inbox_workflow.py` 用例数由 3 变 2，两个存活用例的函数体与断言**逐字节与 P4 开工前相同**（证法见下方 Verification Results 第 3 条）；hook 树 19 份文件摘要与开工前逐字相同。
- [x] AC4 (auto·可靠): `test_mile0009_e2e.py` 对 `INBOX` 与 `origin/` 零命中；prd-migrate / prd-status / prd-update / workspace-scope 四段断言逐条保留；单独跑 `Ran 1 test ... OK`。
- [x] AC5 (auto·可靠): 扫描面 311 份文件对 `origin/` 零命中。排除面与理由见下方 Verification Results 第 5 条。
- [x] AC6 (auto·可靠): `references-schema.md` §1 定位段重写为「`raw/` 原件 vs 其余受控投影」两类保真度对照，并点破「引用 `.ai/references/` 不等于引用权威投影」；§2 由两类资料扩为三类；§1 不再引用已退役的 `.ai/project/`（全文对它零命中）。
- [x] AC7 (auto·可靠): `mcv-deployment.md §2` 明写创建 `.ai/` 与 `deliveries/` 两类基础目录，并说明 `references/`（含 `references/raw/`）按需产生、部署时不建；`Coder/README.md`、`/butler:init`、`butler-init` skill、`templates/rule-card.md` 四处措辞一致。
- [x] AC8 (auto·可靠): `milestone-schema.md` 的输入通道表（§6.1）、合成步骤（§6.4 步 1）、命令表（§6.5）三处均改指 `.ai/references/raw/`；`/butler:prd` 材料来源与 `HUMAN_GUIDE.md` 三处同步；无残留指向项目根 `origin/` 的说法。
- [x] AC9 (auto·可靠): 只读纪律在 `mcv-deployment.md` §2 与 `references-schema.md` §1/§10 三处可 grep；`test_prd_collection_contract.py` 第 56 行那条逐字断言改指新措辞而非删除，**现场演过红**（删掉规则正文那句 → 退出码 1，还原 → 6 passed）。
- [x] AC10 (auto·可靠): `.ai/invariants.md` 第 48 条改写为描述现行三层录入契约（三层名称、日期化闪念键、四态封闭枚举、`tools/intake/intake.py` 是唯一写盘者），并带真源指针 `Coder/40_Context_Management/intake-schema.md`；条目总数 47 不变，其余条目未动。
- [x] AC11 (auto·可靠): `tools/intake/tests/test_intake.py` 新增 `TestLegacyInboxIsRefusedNotRewritten` 四个用例，锁住「旧格式 `.ai/INBOX.md` 喂给 `add` / `list` / `handle` 三个子命令都非零退出、错误信息含逐字表头、`.ai` 全树字节快照前后相同」。**本条是回归防线不是 TDD 配对**：这个行为在本轮之前就已经是对的，本轮只是加锁（详见 TDD Pair Status）。
- [x] AC12 (auto·可靠): `.ai/MILESTONE.md §5.4` 追加五条 2026-08-21（R8 ...）登记，逐条对应 AC12 要求的五个主题。
- [x] AC13 (auto·可靠): `.ai/debt.md` 由 14 条变 15 条——删 1（「两份 inbox 规则真源并存」，旧链已删、自然消解）、改 1（旧格式 INBOX 那条并入「残留 `origin/` 无人搬运」）、增 2（「原件只读无机器兜底」「hook 树一改就必须跟切版绑在一起」）；其余 12 条首句逐条仍在。
- [x] AC14 (auto·可靠): `.ai/OVERVIEW.md` 由 `--write` 重算、`--check` 返回 `{"status": "ok"}`；`40_Context_Management/` 计数 13 → 11；驻留工具清单对 `tools/inbox` 零命中；工作流清单仍 12 行。
- [x] AC15 (auto·可靠): `bash scripts/verify-ci.sh` 退出码 0；`audit-project-state.py --allow-unreleased` 退出码 0，872 OK / 0 DRIFT / 0 FAIL / 恰 2 条 UNRELEASED（工作树未发布、tag 不指向 HEAD——本轮 Out of Scope 明写不切版，属预期）。
- [x] AC16 (auto·可靠): `.ai/iterations/ITER-0119/ac-sweep.py` 可重跑，A 组 8 项零命中、B 组 25 项在场，退出码 0。

## 人测道小结

- N/A（本轮无 human·待人 档 AC，改的全是规则文本、工具代码与台账，没有需要人眼看渲染效果的界面产物；人测道不适用）。

## Evidence Index

| Evidence ID | AC | 强度 | Outcome | Record |
|---|---|---|---|---|
| ac1-ac4-old-chain-gone-v2 | AC1, AC2, AC3, AC4 | 可靠 | passed | .ai/iterations/ITER-0119/evidence/ac1-ac4-old-chain-gone-v2/record.json |
| ac1-ac4-old-chain-gone | AC1, AC2, AC3, AC4 | 可靠 | passed | .ai/iterations/ITER-0119/evidence/ac1-ac4-old-chain-gone/record.json |
| ac5-ac16-sweep | AC5, AC16 | 可靠 | passed | .ai/iterations/ITER-0119/evidence/ac5-ac16-sweep/record.json |
| ac6-ac8-references-and-deploy | AC6, AC7, AC8 | 可靠 | passed | .ai/iterations/ITER-0119/evidence/ac6-ac8-references-and-deploy/record.json |
| ac9-readonly-red-green | AC9 | 可靠 | passed | .ai/iterations/ITER-0119/evidence/ac9-readonly-red-green/record.json |
| ac10-ac11-invariant-and-regression-v2 | AC10, AC11 | 可靠 | passed | .ai/iterations/ITER-0119/evidence/ac10-ac11-invariant-and-regression-v2/record.json |
| ac10-ac11-invariant-and-regression | AC10, AC11 | 可靠 | passed | .ai/iterations/ITER-0119/evidence/ac10-ac11-invariant-and-regression/record.json |
| ac12-ac14-ledgers-v2 | AC12, AC13, AC14 | 可靠 | passed | .ai/iterations/ITER-0119/evidence/ac12-ac14-ledgers-v2/record.json |
| ac12-ac14-ledgers | AC12, AC13, AC14 | 可靠 | passed | .ai/iterations/ITER-0119/evidence/ac12-ac14-ledgers/record.json |
| ac15-gates | AC15 | 可靠 | passed | .ai/iterations/ITER-0119/evidence/ac15-gates/record.json |

七组断言、十条记录，因为其中三组录完第一版之后又补了断言重录了一次：AC3 补逐字节重建证明、AC10 补三层契约的完整不变量描述、AC14 补工作流清单 12 行断言。evidence 工具禁止覆盖同名 ID，所以补证只能录成带 `-v2` 后缀的新记录；不带后缀的第一版是同一批断言的更早一次运行，不是被推翻的结论，一并留在归档里。以 `-v2` 为准。

## Verification Results

1. **旧链拆得干不干净（AC1/AC2）**：两份规则真源与整个 `tools/inbox/` 走 `git rm` 删除，`Coder/40_Context_Management/` 的规则文件数从 13 变 11。CI 里那行 `python -m unittest tools.inbox.tests.test_inbox` 一并摘掉，摘完 CI 仍退出码 0——说明这行不是别的测试的前置。

2. **改引用与删文件的顺序（AC1/AC5）**：按 TECH_PLAN D3 的批次走「先改所有引用方，再删被引用的文件」。反过来先删会让中间态出现一堆指向不存在文件的死引用，中途被打断就留下比开工前更烂的现场。实际执行时把 B1（摘旧链引用）与 B2（改 `origin/`）按文件合并了——同一份文件常常两件事都要改，分两轮打开同一个文件没有收益，而「引用改写在删除之前」这个唯一的硬顺序仍然守住。

3. **两个存活用例逐字节未动，怎么证的（AC3）**：这份文件在 R7（ITER-0118）就改过、改动尚未提交，所以直接跟 `git HEAD` 比会把 R7 的改动也算进来。改用重建法：拿当前文件，把已知的两处本轮改动（文档字符串重写、删掉那个退役用例）原样倒回去，算出的 SHA 与 `pre-p4.baseline` 记的 `686251801c2c…` **完全一致**——这就证明了本轮对这份文件只做了那两件事，没有第三处改动。再从重建结果里切出两个存活用例与当前版逐字节 diff，无差异（`3cb6c556f6184eea…`）。

4. **hook 树为什么必须一个字节不动（AC3）**：`scripts/test-butler-upgrade.py` 有一条断言要求工作区 `templates/hooks/` 的树摘要等于当前 `VERSION` 对应 git tag 的摘要。本轮唯一动到 `templates/hooks/` 的是删了 `tests/` 下一份合同测试，而升级器的 `skip_hook_file()` 本来就把 `tests` 排除在摘要之外，所以摘要不受影响。现场用与 `hook_source_files()` + `tree_digest()` 逐条对齐的口径复算：19 份文件，摘要 `bd92a614f958…`，与开工前基线相同。

5. **`origin/` 零命中的扫描面与排除面（AC5）**：A 组扫的是**「教人怎么做事」的那一面**——`Coder/`、`templates/`、`.claude/`、`plugins/`、`scripts/`、`tools/`、`workflows/`、`docs/`，加上仓根的 `README.md` / `HUMAN_GUIDE.md` / `CLAUDE.md` / `AGENTS.md`，共 311 份文件。这一面上出现旧名字就是一条指向不存在东西的死引用，必须零命中。排除面分两类，理由都写死在 `ac-sweep.py` 的注释里：

   | 排除项 | 理由 |
   |---|---|
   | `migrations/` | 已发布的迁移配方，逐版冻结不回写 |
   | `CHANGELOG.md` | 人读发布史，讲的是当时发生了什么 |
   | `deliveries/` | 已归档交付总结 |
   | `.ai/history/`、`.ai/iterations/`、`.ai/milestones/` | 台账冷分片与已收口快照 |
   | `docs/research/` | 预研记录，结论未冻结也不回写 |
   | `.ai/` 下的当期工作产物（四件套、`MILESTONE.md`、`debt.md`、`task-state.md`、两份 handoff 投影） | 它们要能说清「这轮退役了什么」，就必然得叫出旧东西的名字；改写等于让记录描述不了自己在做什么 |
   | `tools/intake/tests/test_intake.py` | 旧格式**负向夹具**：整份存在的意义就是拿一份长得像旧契约的文件证明工具会拒绝，里面必须有 `SRC-0001`、双指纹字段和旧的受管区块标记 |

   前六项属 AC5 列举的「历史记述不改写」。后两项是 AC5 原文没列到的：`.ai/` 当期产物按性质与 `CHANGELOG.md` / `.ai/milestones/` 同类（记述而非指引），负向夹具则是测试资产而非引用。**两处都不是白名单式放行**——B 组反过来逐条钉住了它们里面真正要紧的东西：`.ai/invariants.md` 第 48 条、`.ai/OVERVIEW.md` 的计数、`.ai/INBOX.md` 的字节，以及夹具里那三个旧标记必须仍在（免得有人为了让 A 组变绿把夹具掏空）。

6. **只读纪律的红绿演示（AC9）**：这是本轮最容易做错的地方——删目录时顺手把纪律一起删掉，扫描会显示零命中、看起来很干净，实际上把一条真规矩弄丢了。防线是规则正文与合同测试的逐字配对。现场演了一遍：现状 6 passed → 把 `references-schema.md §10` 那句纪律删掉 → `1 failed, 5 passed`（退出码 1）→ 还原 → 6 passed。

7. **`origin/` 的三类语句分开改（AC7/AC8/AC9）**：33 处提及按 TECH_PLAN D2 分三类处理——部署协议类 7 处（目录不再创建）、材料通道类 13 处（改指 `.ai/references/raw/`）、只读纪律类 13 处（纪律逐字保留、只换主语）。第三类是唯一不能简单删的，AC9 的红绿演示就是给它上的保险。

8. **顺带修掉的三处旧引用（AC6 范围内的同类缺陷）**：改 `references-schema.md` 时发现三处指向已退役东西的说法，与 AC6 是同一缺陷类、同一批文件，一并修掉——①§1 那张对照表拿 R1 已退役的 `.ai/project/` 当参照（AC6 明列）；②§6 另有一处同样的 `.ai/project/` 比喻，改指 `.ai/OVERVIEW.md`；③§5 与 `prd-split.md` 四处把「INBOX 首见回执」「INBOX 来源关系绑定」当身份证据，那是旧契约的机制，新闪念口没有来源锚点绑定。日期证据这一条保留但改按新契约的字段说（去向指向本需求的那条闪念，取它的「记于」）；`prd-split.md` 第 77 行那句「调用方若来自 INBOX ... 交回 inbox 工作流记录」写的是不存在的接线，删掉不另造——新的 `intake-workflow.md` 里没有这条回传。

9. **门禁双绿（AC15）**：CI 退出码 0；审计 872 OK / 0 DRIFT / 0 FAIL / 2 UNRELEASED。中途出现过两条 DRIFT（handoff 与 state-index 陈旧），跑 `state_ledger migrate` 与 `handoff.py sync` 后消掉；注意 handoff 必须最后同步，先同步再改别的文件会立刻再次陈旧。

## TDD Pair Status

- N/A（TECH_PLAN 明确声明本轮不走 TDD cycle）。

理由说在前面：AC11 原本打算写成「先红后绿」的配对——拿旧格式 `.ai/INBOX.md` 喂 `add` / `list` / `handle`，期望先看到工具把旧文件写坏或误读，再修成拒绝。**P3 探针实测三个子命令都已经是正确行为**：都以退出码 1 停下、都报「表头必须逐字是 `| 闪念键 | 记于 | 一句话 | 状态 | 去向 |`」、都零字节写入。行为本来就对，写出来就是绿的，**没有真实的红**。硬造一个红（比如先把校验删掉再加回来）是伪造配对证据，比不做更坏。所以 AC11 降级为回归防线：断言这个行为存在并锁死。

## Goal Calibration

- 当前无未闭合运行时信号（N/A）。

## Completion Inputs

- Review Verdict: not-run
- Completion Blockers: none

## Gate Coverage

- 静态门：`bash scripts/verify-ci.sh` 退出码 0（含双宿主一致性、goal / plan / calibration 契约、hook 合同测试、升级器 16 项、8 个驻留工具的单元测试与 MILE-0009 端到端）。
- 状态门：`scripts/audit-project-state.py --allow-unreleased` 退出码 0，872 OK / 0 DRIFT / 0 FAIL。
- 产物门：`tools/artifact-pipeline/contract.py check` 五件套全 ok，零 drift。
- 派生门：`scripts/sync-project-overview.py --check` 返回 ok；`tools/handoff/handoff.py` 状态 fresh。
- 迭代门：`.ai/iterations/ITER-0119/ac-sweep.py` 两组共 33 项断言，退出码 0，可重跑。

## References Compliance

- N/A（本轮不消费 `.ai/references/prd/` 下的任何 PRD 切片；改的是 `references-schema.md` 这份契约本身的措辞，不涉及任何需求规格的引用对账）。

## Remaining Risks

1. **「AI 只读用户原件」仍然只是散文，没有机器兜底**。查证结论是它**从来就没有过**——整个 `templates/hooks/` 对 `origin` 零命中，唯一一处是 `bypass.py` 注释里的英文单词 original。所以搬家不弄丢任何保护，但也等于把「写了没人执行」这个毛病换个地方再犯一遍。本轮原计划顺手加一条 PreToolUse 规则，实测撞死在切版顺序上：`scripts/test-butler-upgrade.py` 要求工作区 hook 树摘要等于当前 `VERSION` 对应 tag 的摘要，而 `VERSION` 是 3.6.0、`v3.6.0` 已打 tag，加任何非测试的 hook 文件都会让 CI 红；抬 `VERSION` 反而从 1 个失败变成 1 个失败加 4 个错误。**恢复条件写死：下次切版之后的任意一轮。** 已在 `.ai/debt.md` 记两条账。

2. **已部署项目里的残留搬不走**。butler 从此不再创建、不再读、不再教 `origin/`，但别人硬盘上已经存在的那个目录只能留在原地——升级器的 typed 动作只有 rename / split / add-field / regen-entrypoints / sync-hooks / restamp / no-op 七种，**既没有删除也没有移动**，这轮想搬也表达不出来（归 R14）。同批还有旧格式 `.ai/INBOX.md`：R8 之后仓里连一个认识旧格式的工具都没有，没有降级读法可退。兜底是 fail-closed——新工具碰到旧格式直接报错停下、零字节写入，AC11 那四个用例把这个行为锁死了，所以数据不会被改坏，但用户得自己动手。真正的迁移配方归 R15。

3. **人读文档改完读不读得通，只有人眼过**。扫描按字面串匹配，改成同义但不同字面的说法就会漏网。本轮四份人读文档（`README.md`、`HUMAN_GUIDE.md`、`docs/prd-migration-guide.md`、`templates/rule-card.md`）的改动行都逐行看过，`HUMAN_GUIDE.md` 的目录树画线在删掉 `origin/` 那行后重排过（`deliveries/` 由 `├──` 改 `└──`，子项缩进跟着改）。但这类检查没有机器兜底，这是已知的、接受的残留风险。

4. **`README.md` 目录树里还有一处与本轮无关的陈旧说法**：`.ai/project/  # 项目长期知识`——那个角色已在 ITER-0112 退役（项目全貌产物现在是 `.ai/OVERVIEW.md`），但 `.ai/project/` 目录本身还活着（放 `workspaces.md`）。本轮只在这棵树里做了 `origin/` 相关的最小改动（删掉 `origin/` 行、补上 `references/` 行），没有顺手翻修整棵树——那是另一个缺陷类，超出本轮 ACK 范围。留给后续路线处理。

## Handoff / Next Step

- 走 `iteration-schema.md §5.5` 收口四步：写 `.ai/01_CHANGELOG.md`、产 `deliveries/ITER-0119-<slug>.md` 与同名 `.html`、快照进 `.ai/iterations/ITER-0119/`、台账置 closed 并把 `.ai/MILESTONE.md` 路线表 R8 一行置 done。
- 本轮 Out of Scope 明写**不切版、不发布、不提交、不打 tag**，两条 `[UNRELEASED]` 属预期，不在本轮处理。
- MILE-0016 下一条路线是 R9（根布局整理：`.ai/milestone-backlog/` 改名 `.ai/backlog/`、`deliveries/` 迁入 `.ai/`）。本轮欠下的两笔（原件只读门禁、已部署项目残留）分别指向「下次切版之后的任意一轮」与 R14 / R15。
