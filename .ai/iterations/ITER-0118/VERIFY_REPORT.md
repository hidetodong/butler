<!-- butler-artifact-template: 1.0.0 artifact=verify_report -->
# VERIFY_REPORT — ITER-0118

## Verification Summary

- 15 条验收标准全部关闭，14 条机器证据全部 passed（含一对 Red → Green 配对），两条门禁退出码均为 0，两组扫描 38 项零命中。
- 本轮把 R6 定的三层录入契约接上了电：新建确定性工具 `tools/intake/`（`intake.py` 767 行、测试 493 + 82 行、28 条用例）与动作层规则 `Coder/40_Context_Management/intake-workflow.md`（101 行），`/butler:inbox` 的命令与 skill 两份薄壳改读新契约、改调新工具，注册表 inbox 条目 `rule_source` 改指新动作层。
- 真实 dogfood 走通了「记一条真闪念 → 孵化成一份真草稿」这一段：候办由 9 增为 10，butler 仓第一次有了 `.ai/INBOX.md`。**另外两条出口只有沙箱证据**，这个折扣在 AC11 与 Remaining Risks 里单独摊开写，没有混进「dogfood 已完成」。
- 旧链（`inbox-schema.md`、`inbox-workflow.md`、`test_inbox_contract.py`、`tools/inbox/` 全目录，共 8 份）逐字节未动，有开工前哈希为证。

## AC Status

- [x] AC1 (auto·可靠): 工具存在且自带测试；三个子命令都收 `--project-root`、输出可解析 JSON；校验不过时退出码 1 且目标文件哈希不变。
- [x] AC2 (auto·可靠): `add` 生成 `2026-08-20-fix-the-renderer` 形态的键、同日撞名退让为 `-2` / `-3`、新条目恒为 `new` 且去向 `—`；文件不存在时建出契约表头，存在时只追加、既有字节不动。
- [x] AC3 (auto·可靠): `list` 跑完前后 `.ai/INBOX.md` 哈希与孵化区文件数均不变；按状态、按规模筛选各有用例。
- [x] AC4 (auto·可靠): 工具的合法转移集合从 `intake-schema.md §1.5` 的表格解析出来逐一比对，**恰是那四条**；终态回退、`incubated → done` 直跳等组合逐条被拒且不留写入痕迹。
- [x] AC5 (auto·可靠): 转 `incubated` 一次写三处；注入第二处、第三处写失败的两条用例断言三处全部回到原始字节且退出码非零。
- [x] AC6 (auto·可靠): `sync-workflow-registry.py --check` 退出码 0，业务工作流仍 12 个；两份薄壳正文的旧来源目录与旧动作层文件名各 0 命中。
- [x] AC7 (auto·可靠): 旧链 8 份文件哈希与 `pre-p4.baseline` 逐一相同；`test_inbox_workflow.py` 只动了活接线那两个用例，描述旧规则文件的那个用例仍在断言旧文件。
- [x] AC8 (auto·可靠): §7.6 已改指工具；该文件对 HEAD 的两个改动块里，本轮那一块（第 282 行起 6 行）完全落在 §7.6 的 [276, 297] 区间内。
- [x] AC9 (auto·可靠): `Coder/README.md` 目录结构与读取顺序两处注册各 1 次；动作层文件三个动作都写了「工具确定性决定的」与「必须问用户的」两小节。
- [x] AC10 (auto·可靠): 闪念行状态 `incubated`、去向指向草稿；草稿三行头部标记齐备、`iteration` 档两段齐备、占位标记已被真内容替换；待办区索引 10 行、草稿文件 10 份且两个集合相等。
- [x] AC11 (auto·可靠·**沙箱**): `promote` 领到 MILE-0002、`iterate` 领到 ITER-0002，两侧删净、`current` 已指向；对照组把 `current` 改成非 `none` 后两条出口都被拦下且草稿仍在。**这一档证明代码路径通，不证明真实使用下好用**，见 Remaining Risks。
- [x] AC12 (auto·可靠): `.ai/MILESTONE.md §5.4` 追加 4 条 R7 登记，AC 点名的三项（复用 id、必须动那份测试及边界、两条出口跑不通与沙箱折衷）逐条在场。
- [x] AC13 (auto·可靠): 债务条目 12 → 14；两份 inbox 真源那条已按 R7 后的剩余范围重新表述；原有 7 条抽样逐条仍在。
- [x] AC14 (auto·可靠): `--check` 退出码 0；驻留工具清单新增 `tools/intake/` 且说明非破折号；`40_Context_Management/` 规则文件数 12 → 13；工作流清单仍 12 行且 inbox 行的规则真源已改指新动作层。
- [x] AC15 (auto·可靠): `verify-ci.sh` 退出码 0 且日志里有新工具的 `Ran 28 tests`；审计退出码 0、862 条 `[OK]`、`[UNRELEASED]` 恰 2 条、`[DRIFT]` 0 条；两组扫描 38 项全通过（A 组扫了 516 份活跃面文件）。

## 人测道小结

- N/A（本轮 15 条 AC 全为 auto·可靠档，无 human·待人档，人测道不适用）。

## Evidence Index

| Evidence ID | AC | 强度 | Outcome | Record |
|---|---|---|---|---|
| tdd-intake-red | AC1, AC2, AC3, AC4, AC5 | 可靠 | failed | .ai/iterations/ITER-0118/evidence/tdd-intake-red/record.json |
| tdd-intake-green | AC1, AC2, AC3, AC4, AC5 | 可靠 | passed | .ai/iterations/ITER-0118/evidence/tdd-intake-green/record.json |
| tdd-red-intake | AC1 | 可靠 | failed | .ai/iterations/ITER-0118/evidence/tdd-red-intake/record.json |
| tdd-green-intake | AC1 | 可靠 | passed | .ai/iterations/ITER-0118/evidence/tdd-green-intake/record.json |
| ac1-cli-contract | AC1 | 可靠 | passed | .ai/iterations/ITER-0118/evidence/ac1-cli-contract/record.json |
| ac2-ac3-ac4-add-list-transitions | AC2, AC3, AC4 | 可靠 | passed | .ai/iterations/ITER-0118/evidence/ac2-ac3-ac4-add-list-transitions/record.json |
| ac5-atomic-rollback | AC5 | 可靠 | passed | .ai/iterations/ITER-0118/evidence/ac5-atomic-rollback/record.json |
| ac6-ac7-wiring-and-old-chain | AC6, AC7 | 可靠 | passed | .ai/iterations/ITER-0118/evidence/ac6-ac7-wiring-and-old-chain/record.json |
| ac8-ac9-schema-readme | AC8, AC9 | 可靠 | passed | .ai/iterations/ITER-0118/evidence/ac8-ac9-schema-readme/record.json |
| ac10-real-dogfood | AC10 | 可靠 | passed | .ai/iterations/ITER-0118/evidence/ac10-real-dogfood/record.json |
| ac11-sandbox-dogfood | AC11 | 可靠 | passed | .ai/iterations/ITER-0118/evidence/ac11-sandbox-dogfood/record.json |
| ac12-ac13-log-and-debt | AC12, AC13 | 可靠 | passed | .ai/iterations/ITER-0118/evidence/ac12-ac13-log-and-debt/record.json |
| ac14-overview | AC14 | 可靠 | passed | .ai/iterations/ITER-0118/evidence/ac14-overview/record.json |
| ac15-gates | AC15 | 可靠 | passed | .ai/iterations/ITER-0118/evidence/ac15-gates/record.json |

## Verification Results

**AC4 的「穷举」是解析出来比的，不是 grep 字样。** 只断言四条转移各自在场，证不了「恰好这四条、没有第五条」。所以证据脚本把 `intake-schema.md §1.5` 的表格用正则解析成集合，再与工具里的 `TRANSITIONS` 常量做集合相等断言。契约多一行少一行、工具多认一条少认一条，两边任一侧漂移都会红。

**AC5 的回滚是注入失败测的，不是靠读代码相信的。** 测试把工具的写盘原语替换成「第 N 次调用抛异常」的版本，分别在第二处和第三处注入，然后对整个 `.ai/` 目录做字节级快照比对，断言三处文件全部回到原始状态、草稿文件不存在、退出码非零。要说清楚的是**这不等于事务**：回滚过程本身也可能失败（磁盘满、权限变化），那种情况覆盖不了，已按同口径写进 `intake-workflow.md §5`、工具 README 与 `.ai/debt.md`，文档里也没有用「原子事务」这类过头的词。

**AC7 的边界怎么划的。** R6 的 Out of Scope 说旧链一字不动，但 `test_inbox_workflow.py` 不是纯旧链测试——三个用例里两个断言的是当前活着的接线（注册表 `rule_source`、两份薄壳必须提到的字样），活接线一改指新契约这两个必红。处置是拆成两半：断言旧规则文件内容的 `test_inbox_workflow_route_and_safety_contract` 原样保留，随 R8 一起退役；另外两个改指新契约与新工具，并删掉旧来源目录那条断言（新薄壳不扫那个目录，留着断言等于逼薄壳写假话）。文件头加了一段注释说明这个分工。边界的硬证据是旧链 8 份文件的哈希与开工前基线逐一相同。

**AC8 的「改动全落 §7.6 内」是怎么在有历史未提交改动的情况下证的。** 本仓当前工作树里有 MILE-0016 前几个迭代尚未提交的改动，所以 `git diff` 的范围跨了不止一个迭代——`milestone-schema.md` 对 HEAD 有两个改动块。证据脚本把两块分开认：第 112 行那块是 ITER-0117 的 §4.5 规模分档（那一轮的验证报告已记），第 282 行起 6 行那块是本轮的，落在 §7.6 的 [276, 297] 区间内。脚本同时断言「ITER-0117 遗留块恰 1 个」「本轮块恰 1 个且完全在区间内」，任何一侧多出一块都会红。

**AC10 与 AC11 是两档不同的东西，必须分开读。** AC10 是真的：选题是「交付页渲染器只活在会话临时目录里、换个会话就没了」——这是本会话反复踩到的真实缺口（`delivery-summary.md §9` 说 HTML 模板是唯一真源却从没说渲染器在哪，因为仓库里根本没有），够一个迭代收口，正好是 `iteration` 档。全程用工具写盘，草稿正文由模型补实（这是契约规定的分工：结构归工具、正文归模型）。AC11 是沙箱：`promote` 与 `iterate` 都要求台账 `current` 为 `none`，而 butler 仓 MILE-0016 与 ITER-0118 都 active，这两条出口在真实环境里**根本没法跑**，只能在临时项目根上造一个 `current: none` 的环境各跑一遍。

**执行中发现 §7.6 的形状不对，改成两次调用。** §7.6「普通暂缓」原本第 3、4 步是让模型手工写草稿和索引行，本轮要合并成一步调工具时才发现：工具的 `handle --to incubated` 要求先有一条闪念行，而 §7.6 是从 `/milestone` 的对话进来的，那个方向不一定进过闪念口。否掉了「给工具开一条直接建草稿的旁路」（等于给孵化区开第二个入口，与三层契约的意义相反），改成 §7.6 明写两次调用：先 `add` 记一条闪念拿到键，再 `handle` 孵化它。代价是敲两条命令，换来的是「这个方向什么时候第一次出现」有据可查。已登记进 §5.4。

**执行中修掉的一处自相矛盾。** 新动作层初稿写的是「AI 不得用编辑器直接改孵化区草稿」，但同一份文件又说「工具产骨架、模型填正文」——两句话打架。dogfood 填草稿正文时撞上，改成按「结构归工具、正文归模型」重新表述，四处（动作层、命令薄壳、skill、`Coder/README.md` 指针）同批改齐，`milestone-schema.md §7.6` 的措辞也跟着收窄。

**顺带修掉一条会说假话的路由示例。** `workflows/router-examples.json` 里 inbox 那条示例请求原文描述的是即将不存在的行为，改成了新语义的说法。`sync-workflow-registry.py --check` 只校验覆盖度不校验语义，这条只能靠 B 组扫描断言新措辞在场、旧措辞不在。

**TECH_PLAN 在 P5 补了一张机器可读的 TDD 声明表。** 原 `Test Strategy` 用散文写了「本轮有真代码，所以有 TDD 配对」，但 `verification-evidence check-tdd` 认的是 `<!-- butler-tdd-cycles: v1 -->` 标记后的固定表格。补的是同一件事的机器形态，不是改设计，故未按 §5.3 走方案修订。

**Red 记录抓了两次，两份都留着。** P4 开工时先写测试、实现尚不存在，抓到的原始 Red 是 `tdd-red-intake`（失败原因是导入不到实现模块）。后来发现配对检查要求 `tdd-<cycle>-red` 的命名，按该命名重抓了一次等价 Red（把实现文件临时移开，复现同一条导入失败），得到 `tdd-intake-red`。两份 record 都列进了 Evidence Index，**重抓的那次是再现不是原始**，这里如实记明。

## TDD Pair Status

- `[OK] intake` —— `python3 tools/verification-evidence/evidence.py check-tdd --project-root . --iteration ITER-0118` 退出码 0。cycle `intake` 覆盖 AC1–AC5，Red（`tdd-intake-red`，failed）与 Green（`tdd-intake-green`，passed）用同一条命令 `python3 -m unittest discover -s tools/intake/tests -t .` 在同一 cwd 下抓取，两条 record 均列入 Evidence Index。

## Goal Calibration

- 当前无未闭合运行时信号（N/A）。

## Completion Inputs

- Review Verdict: pass
- Completion Blockers: none

## Gate Coverage

- 通用质量门禁：`bash scripts/verify-ci.sh` 退出码 0（含新接入的 `tools/intake/tests` 一行，日志中可见 `Ran 28 tests`；旧工具那行原样保留，R8 才删）。
- 状态审计：`python3 scripts/audit-project-state.py --project-root . --allow-unreleased` 退出码 0，862 条 `[OK]`、2 条 `[UNRELEASED]`（工作树有未发布改动、tag 不指向 HEAD，均为预期）、0 条 `[DRIFT]`。
- 产物合同：五件套 `contract.py check` 全部 ok。
- 投影一致性：`sync-workflow-registry.py --check` 与 `sync-project-overview.py --check` 均退出码 0。
- 两组扫描：`.ai/iterations/ITER-0118/ac-sweep.py` 共 38 项，A 组查越界（活跃面 516 份文件不出现 R9 才存在的孵化区路径；新工具与新规则不出现旧编号前缀与双指纹字段名；两份薄壳不出现旧来源目录与旧动作层文件名）、B 组查在场（旧链哈希未变、三个动作与三条出口在场、README 两处注册、§7.6 已改指、候办 9 → 10 且两个集合相等、dogfood 草稿无占位残留、路由示例已换措辞、CI 新旧两行都在），全部零命中。模式串一律用片段拼接构造，避免脚本自命中。
- Workspace Scope：N/A（本轮无 `prd_refs`）。

## References Compliance

- 本迭代无 `.ai/references/` 外部参考资料，无 PRD 约束，无 workspace scope 边界需要对账。
- 内部依赖按 TECH_PLAN 声明执行：`intake-schema.md`（数据形态真源，工具与动作层都只引用不重抄）、`milestone-schema.md §4.5 / §7.1 / §7.6`、`iteration-schema.md §5.1`（`iterate` 只写台账那半，四件套仍归模型，工具在回执 `next_step` 里指路）、`scripts/sync-workflow-registry.py`（只改数据不改脚本）、`tools/decision-map/`（CLI 与测试约定照抄）。
- 新增规则文件按 `CLAUDE.md` 的约束在 `Coder/README.md` 两处注册；新增工具带 `README.md`，其第一个标题已接入 `.ai/OVERVIEW.md` 的驻留工具清单。

## Remaining Risks

- **两条出口没有真实使用证据，只有沙箱证据。** `promote` 与 `iterate` 要求台账 `current` 为 `none`，butler 仓长期有 active，这不是能靠加班补上的缺口。沙箱脚本 `.ai/iterations/ITER-0118/sandbox-dogfood.py` 可重跑，但它证明的是代码路径通，不是真实使用下好用。六条动作路径里真实用过的只有 `add` 与 `handle --to incubated` 两条，其余四条（`done` / `dropped` / 两条出口）等真实使用自然发生。已记入 `.ai/debt.md`。
- **跨文件写盘的回滚本身失败时仍会留半截态。** 做的是「先算后写、失败即回滚」，不是事务。注入失败的测试覆盖了正常回滚路径，覆盖不了回滚自己失败。事后兜底只有审计里那条「待办区索引集合等于草稿文件集合」的断言。这是明知代价后接受的取舍，已记入 `.ai/debt.md`，没有自然消解路径。
- **两份 inbox 规则真源仍并存，剩余风险是纯阅读侧的。** 活接线已全部改指新链，但 `inbox-schema.md` 还在仓库里描述同一条路径，没有任何检查能拦住有人直接翻到它并按七态结构写盘。自然消解路径是 R8 删旧链。
- **已部署项目里旧格式 `.ai/INBOX.md` 的迁移仍没人认领。** 旧格式文件遇上新工具会因为表头对不上被整次拒绝——拒绝比默默改坏强，但这不是迁移。归 R15。
- **`Coder/README.md` 的两处注册没有机器门禁。** 本轮靠证据脚本 `grep -c` 断言各 1 次，但那是一次性脚本，不是常驻检查。同类问题（人读文档里的计数没有兜底）已在 `.ai/debt.md` 有账。

## Handoff / Next Step

- ITER-0118 已具备收口条件，按 `iteration-schema.md §5.5` 走四步收口仪式：写 CHANGELOG → 归档证据与四件套快照 → 双台账置 closed 并把 `current` 置 `none` → 收口后自检（审计 + 两组扫描 + 五个冷启动不变量）。
- 下一个迭代按 MILE-0016 路线图是 **R8 — 退役旧 inbox 全链**：删 `inbox-schema.md`、`inbox-workflow.md`、`tools/inbox/`、`test_inbox_contract.py`、`test_inbox_workflow.py` 里保留的那个旧规则用例、以及 `scripts/verify-ci.sh` 里旧工具那一行。删完之后 `.ai/debt.md` 里「两份 inbox 规则真源并存」那条自动还清。
- 本轮未切版、未打 tag、未提交，按约束等用户指示。
