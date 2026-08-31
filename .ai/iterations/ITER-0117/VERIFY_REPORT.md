<!-- butler-artifact-template: 1.0.0 artifact=verify_report -->
# VERIFY_REPORT — ITER-0117

## Verification Summary

- 12 条 AC 全部通过，11 份可重跑证据全绿，两组扫描零命中零缺席（收口态扫描 508 份文本文件），CI 退出码 0，项目审计退出码 0（857 条 OK，仅 2 条 `[UNRELEASED]`，是未切版的预期态）。
- 本轮产出一份新规则真源 `Coder/40_Context_Management/intake-schema.md`（184 行），定义闪念口 / 孵化区 / 执行分流三层的数据形态；旧 inbox 全链 13 份文件逐字节未动；`.ai/MILESTONES.md` 逐字节未动。
- **机器只能证「结构齐备、路径为真、旧链没碰」，证不了「这个结构好用」**。新契约在 MILE-0016 R7 把命令做出来之前没有任何使用者，写得对不对要等真跑一条闪念到执行才知道。这条已记入剩余风险。

## AC Status

- [x] AC1 (auto·可靠): 三层结构定义齐备，三处封闭枚举用脚本解析成列表后断言集合与顺序相等（状态四态、规模三档、出口三条），不靠字样在场。
- [x] AC2 (auto·可靠): 生效时点声明五个关键要素在场且位于 H1 底下的引用块；`inbox-schema.md` 与 `inbox-workflow.md` 与 P2 基线哈希一致。
- [x] AC3 (auto·可靠): 新契约零命中 R9 才存在的孵化区路径；真实路径 `.ai/milestone-backlog/` 出现 6 次；R9 改名预告在场。
- [x] AC4 (auto·可靠): 9 份草稿逐个 `git diff --numstat` 恰 1 增 0 删；`规模` 与既有两标记同处一块。
- [x] AC5 (auto·可靠): `.ai/MILESTONES.md` 哈希与 P4 前基线完全相同（`dd8846af…`），表头仍 5 列、待办区仍 9 行。
- [x] AC6 (auto·可靠): `milestone-schema.md` 的改动只有 1 处 hunk、落在第 112 行，处于 §4.5 区间 (95, 116) 内；5 列索引表模板与 §5 四段标题零改动。
- [x] AC7 (auto·可靠): `Coder/README.md` 目录结构树与读取顺序逐文件指针各恰好一条新注册；CI 退出码 0。
- [x] AC8 (auto·可靠): `.ai/MILESTONE.md §5.4` 的 R6 登记恰 3 条，三条各含处置与理由的关键措辞。
- [x] AC9 (auto·可靠): `.ai/debt.md` 由 10 条增为 12 条；原 10 条标题与顺序逐条断言未动；新增两条各含缺口、有意不做的理由与自然消解路径。
- [x] AC10 (auto·可靠): 旧 inbox 链 13 份文件逐份哈希比对全部未变；`workflows/registry.json` 的 inbox 条目在场，业务工作流仍 12 个。
- [x] AC11 (auto·可靠): `sync-project-overview.py --check` 退出码 0；`40_Context_Management/` 规则文件计数 11 → 12，与目录实际文件数一致；工作流清单仍 12 行。
- [x] AC12 (auto·可靠): CI 退出码 0；审计退出码 0、`[UNRELEASED]` 恰 2 条、无 `[DRIFT]`；两组扫描 A 组零命中、B 组零缺席。

## 人测道小结

- N/A（本轮全部改动是规则文本与台账，界面上看不出效果，无 human·待人 档 AC，人测道不适用）。

## Evidence Index

| Evidence ID | AC | 强度 | Outcome | Record |
|---|---|---|---|---|
| ac1-three-layers | AC1 | 可靠 | passed | .ai/iterations/ITER-0117/evidence/ac1-three-layers/record.json |
| ac2-declaration | AC2 | 可靠 | passed | .ai/iterations/ITER-0117/evidence/ac2-declaration/record.json |
| ac3-paths | AC3 | 可靠 | passed | .ai/iterations/ITER-0117/evidence/ac3-paths/record.json |
| ac4-drafts | AC4 | 可靠 | passed | .ai/iterations/ITER-0117/evidence/ac4-drafts/record.json |
| ac5-index-untouched | AC5 | 可靠 | passed | .ai/iterations/ITER-0117/evidence/ac5-index-untouched/record.json |
| ac6-ac7-schema-readme | AC6, AC7 | 可靠 | passed | .ai/iterations/ITER-0117/evidence/ac6-ac7-schema-readme/record.json |
| ac8-milestone-log | AC8 | 可靠 | passed | .ai/iterations/ITER-0117/evidence/ac8-milestone-log/record.json |
| ac9-debt | AC9 | 可靠 | passed | .ai/iterations/ITER-0117/evidence/ac9-debt/record.json |
| ac10-legacy-chain | AC10 | 可靠 | passed | .ai/iterations/ITER-0117/evidence/ac10-legacy-chain/record.json |
| ac11-overview | AC11 | 可靠 | passed | .ai/iterations/ITER-0117/evidence/ac11-overview/record.json |
| ac12-gates | AC12 | 可靠 | passed | .ai/iterations/ITER-0117/evidence/ac12-gates/record.json |

## Verification Results

**新契约的三处封闭枚举怎么证的。** 只 grep 字样在场证不了「恰好这几个、没有第七个」，所以三处都是把表格解析成列表再断言相等：闪念状态 `['new','incubated','done','dropped']`、合法转移 `[('new','incubated'),('new','done'),('new','dropped'),('incubated','dropped')]`、规模三档 `['milestone','iteration','undecided']`、执行出口 `['提升为里程碑','开为迭代','撤回']`。任何一处多一行少一行都会红。另有一条反向断言：全文不得出现「等等」「视情况而定」这类给枚举留开口的措辞。

**AC5 一度被一个工具动过，但结果是字节相同。** 收口前跑 `state-ledger migrate` 消审计漂移时，工具报告改写了 `.ai/MILESTONES.md`。逐字节比对确认它写回的内容与 P4 前基线**完全相同**（`dd8846af…`），属于无变化的重写，AC5 成立。这里如实记一笔：AC5 的保证是「内容字节相同」，不是「文件从未被写过」。

**`milestone-schema.md` 的改动溢出检查是按行号做的。** §4.5 的行号区间是 (95, 116)，`git diff -U0` 只有一个 hunk、落在第 112 行，在区间内。改法是把原来那一条 bullet（同时管头部标记和四段结构）拆成两条：一条把标记由两项扩为三项，一条把「沿用 §5 四段」改为按档并指向 `intake-schema.md`。原 bullet 删 1 增 2。

**AC12 的 A 组排除面，逐份摊开。** A 组要证「全仓活跃面不出现 R9 才存在的孵化区路径」。扫描覆盖 10 个活跃目录（`Coder/`、`templates/`、`tools/`、`scripts/`、`workflows/`、`plugins/`、`.claude/`、`docs/`、`migrations/`、`deliveries/`）加根级 `*.md`，共 508 份文本文件（收口态，含本轮新出的交付页），**零命中**。

刻意排除的是 `.ai/` 下的迭代产物，全仓仅 4 份文件命中该路径，逐份说明：

| 文件 | 命中数 | 为什么放行 |
|---|---|---|
| `.ai/MILESTONE.md` | 5 | R5.3 路线图里 R6 / R9 两条本来就写着这个将来的路径，另有本轮 §5.4 那条「按现实路径写」的登记要引用它 |
| `.ai/CONCEPT.md` | 3 | P1 分析里「这条路径到 R9 才存在」这个发现本身 |
| `.ai/AC_LIST.md` | 3 | AC3 / AC8 / AC12 的标准文本要点名禁的是哪条路径 |
| `.ai/TECH_PLAN.md` | 2 | 失败路径与验证策略里同样要点名 |

这 4 份都是本迭代的**工作产物**，不是任何宿主、工具或规则会读进去当依据的接线面。它们讨论的正是「这条路径现在还不存在」这件事，出现该路径是正确的。

**收口时扫描抓到了一处真命中，不是误报。** 交付总结初稿里有一句「路线图里写的孵化区路径 `.ai/backlog/` 到 R9 改名时才存在」，把那条未来路径的字面写进了 `deliveries/`——而 `deliveries/` 正在 A 组的扫描范围内。这是脚本第一次在收口阶段拦下真东西，不是排除面漏配。改法是把那句话里的字面路径去掉（「路线图里给孵化区写的是它 R9 改名之后的新路径，那个路径现在还不存在」），语义没损失，重渲染交付页后 A 组回到零命中。

**收口态的两次数字变动要说明。** 上面的 508 份与 857 条 OK 是**收口后**的复跑结果；P5 首次跑时分别是 507 份与 848 条，差额来自本轮新出的交付页与台账收口带来的新增审计项。报告以收口态数字为准。

**扫描脚本自命中的防法。** 脚本里要查的三个禁用串（未来路径、旧编号前缀、旧双指纹字段名）全部用片段拼接构造（`".ai/" + "backlog" + "/"`、`"SR" + "C-"`、`"observed" + "_sha256"`），脚本本身不含完整串。

**一处写法上的取舍要说明。** AC12 的 A 组要求新契约不出现旧契约的编号前缀。但新契约的生效时点声明和 §1.3 都需要说清「旧契约用的是哪种方案、我们为什么不用」。初稿直接写了那个前缀的字面形式，与 AC 冲突；改成描述性写法——「带固定前缀的四位递增编号」，并在两处都给出 `inbox-schema.md` 的指针供读者自查。**代价是具体性下降了一点**，换来 AC 字面成立且新契约里不残留旧方案的标识符。

**证据脚本自身发现并修掉的两个缺陷。**
- 两组扫描脚本的转移表正则最初写成 `` ^\| `(\w+)` → `(\w+)` \| ``，而契约里整个转移写在一对反引号内（`` `new → incubated` ``），导致解析出空列表却仍走到断言——第一次跑就红了（`合法转移不是预期的四条：[]`），改正则后通过。
- `ac10-legacy-chain.sh` 读 `workflows/registry.json` 的 inbox 条目时取了不存在的 `command` 键（实际键是 `claude`），第一次干跑抛 `KeyError`，改为读 `claude` 与 `rule_source` 后通过。

两处都是脚本自己失败、而不是悄悄放过，说明断言确实在跑。

## TDD Pair Status

- N/A。本轮改动全是规则文本与台账，没有可执行的代码路径，做不出「同一条测试命令先失败、后通过」的配对。TECH_PLAN 已在验证策略里声明本轮不做 TDD 配对。

## Goal Calibration

- 当前无未闭合运行时信号（N/A）。

## Completion Inputs

- Review Verdict: not-run
- Completion Blockers: none

## Gate Coverage

- `bash scripts/verify-ci.sh` → 退出码 0。
- `python3 scripts/audit-project-state.py --project-root . --allow-unreleased` → 退出码 0，857 条 OK，2 条 `[UNRELEASED]`（工作树有未发布改动、`v3.6.0` 不指向 HEAD），无 `[DRIFT]`。
- `python3 .ai/iterations/ITER-0117/ac-sweep.py` → 退出码 0，A 组零命中、B 组零缺席。
- `python3 scripts/sync-project-overview.py --check` → 退出码 0。
- `python3 tools/handoff/handoff.py check --project-root .` → `fresh`。
- 五份产物合同（concept / acceptance / tech_plan / verify_report / changelog）→ 全部 `ok`。

## References Compliance

- 本迭代无 `.ai/references/` 外部参考资料，无 PRD 约束，无 workspace scope 边界需要对账。
- 内部依赖全部以**指针引用**方式接入，未重抄他人真源：`milestone-schema.md §4.5`（本轮改两条）、`§5`（新契约 §2.1 明写「真源在那里，本文件不重抄」）、`§7.1`（出口一的动作真源）；`iteration-schema.md §5.1`（出口二的动作真源）、`§5.3`（本轮 amend 依据）；`inbox-schema.md`（只读参照，零改动）。
- 新增规则文件按 `CLAUDE.md` 的约束在 `Coder/README.md` 两处注册，未引入隐式依赖。
- 书写口径按 `artifact-style.md`：契约正文对 AI 用「必须 / 不得」，给人读的说明句守说人话四条——「受管区块标记」「指纹认亲」「号池」这几个词第一次出现都紧跟了一句大白话。

## Remaining Risks

- **新契约在 R7 之前没有任何使用者。** 三层结构写得对不对、`undecided` 档的出区压力管不管用，机器只能证字样在场。真话要等 R7 把 `/butler:inbox` 做出来、真跑一条闪念走到执行才知道。
- **两份 inbox 规则真源并存三个迭代，没有机器兜底。** 分工只能单向声明（新契约指回旧的），因为本轮明确不动旧契约一个字——从旧契约那边读进来的人看不到这段分工。已登记 `.ai/debt.md`，自然消解路径是 R8 删掉旧契约。
- **`Coder/README.md` 的文件级注册机器不查。** `sync-project-overview.py` 只校验「每个目录有没有说明」，不校验「每个文件有没有指针」。本轮靠 `grep -c` 逐处自证，将来漏注册一份规则文件不会有门禁报警。
- **已部署项目里旧格式 `.ai/INBOX.md` 的迁移义务没人认领。** 新旧格式不兼容，本轮既没写迁移配方也没写降级读法。已登记 `.ai/debt.md`，归 R15。
- **孵化区目录名到 R9 才改。** 新契约按现实路径 `.ai/milestone-backlog/` 写，正文明写了届时同批更新；但这条靠的是 R9 执行时记得回来改，没有机器提醒。

## Handoff / Next Step

- ITER-0117 已具备收口条件，按 `iteration-schema.md §5.5` 走四步收口仪式。
- MILE-0016 下一条路线项是 R7（重造·`/butler:inbox` 命令层：把本轮定的三层契约变成可执行的 add / list / handle）。R7 落地后本契约才第一次有使用者，届时应回头核对结构是否够用。
- 未切版、未提交、未推送——按用户指令，这三件事都等显式要求。
