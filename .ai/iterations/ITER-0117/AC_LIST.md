---
状态: ack-frozen
ACK 日期: 2026-08-20
修订记录: 2026-08-20 · ① P3 查出「待办区索引加规模列」的真实代价与真实副作用：`scripts/audit-project-state.py` 的候办解析硬编码 5 列并按下标取草稿路径，加列要改 3 处代码，`scripts/test-audit-project-state.py` 有 6 个测试方法、11 行 fixture 钉着 5 列表头；更要紧的是**规模同时写在草稿头部和索引行会造出第二个真源**，而防漂移要新增一条一致性断言，正是本轮 Out of Scope 明写不做的。故改判：规模只写在草稿头部，索引一字不改。按 `iteration-schema.md §5.3` 退回 draft——AC5 由「索引加列」改为「索引逐字未改」，AC1 第二层去掉索引行字段，AC6 的两处改点收敛为 §4.5 内的两处（草稿头部标记加规模、四段强制改为按档），AC12 的 A 组增一条「待办区索引未被改动」。影响面只缩不扩。
---
<!-- butler-artifact-template: 1.0.0 artifact=acceptance -->
# AC_LIST — ITER-0117

## Goal

- 把「闪念 → 孵化 → 执行」三层的数据形态定死在一份新的规则真源里，只写结构与状态、不写任何命令或工具。同时处理三处定序冲突：新契约与旧 `inbox-schema.md` 共占 `.ai/INBOX.md` 这一路径、孵化区目录到 R9 才改名、9 份存量候办草稿没有规模字段。收口态必须是「新契约句句为真、旧链一字未动、CI 全绿」。

## In Scope

- 新建规则真源（新文件，落点与文件名 P3 定），定义三层：闪念口 `.ai/INBOX.md` 的最小结构与状态机；孵化区在现有 `.ai/milestone-backlog/<slug>.md` 上加 `规模` 字段（`milestone` / `iteration` / `undecided`）并按档分定结构要求；执行分流的合法去向与前置条件。
- 在新契约里写明与旧 `inbox-schema.md` 的分工和生效时点：R8 删旧契约前，`.ai/INBOX.md` 的旧格式仍是唯一在用的定义，新契约在 R7 命令落地前零写入。
- 回填 9 份存量候办草稿的 `规模: milestone`。索引不承载规模——`.ai/MILESTONES.md` 待办区一字不改（理由见修订记录）。
- 改 `milestone-schema.md §4.5` 编写规则里的两处：草稿头部标记加 `规模`、「沿用 §5 的四段结构」改为按档并指向新契约。§4.5 的索引表模板与 §5 正文不动。
- 在 `Coder/README.md` 的目录结构与读取顺序里注册新规则文件。
- 在 `.ai/MILESTONE.md §5.4` 登记三处定序处置与「新契约无机器兜底」这个事实。
- 在 `.ai/debt.md` 登记两条新欠账：两份 inbox 规则真源并存无机器兜底、已部署项目的旧格式 `.ai/INBOX.md` 迁移义务未兑现。

## Out of Scope

- 不写 `/butler:inbox add | list | handle` 的命令、参数、回执格式与任何可执行实现（归 R7）。
- 不动 `inbox-schema.md`、`inbox-workflow.md`、`templates/hooks/tests/test_inbox_contract.py`、`test_inbox_workflow.py`、`tools/inbox/`、`origin/`、SRC-NNNN、双 SHA-256、scanner 一个字（归 R8）。
- 不改目录名 `.ai/milestone-backlog/`（归 R9）。
- 不动 `workflows/registry.json` 的 inbox 条目、`.claude/commands/butler/inbox.md`、Codex skill。
- 不给新契约加机器断言或 CI 检查。
- 不切版、不发布、不提交。

## Acceptance Checklist

- [ ] AC1: 新规则真源存在，且三层各自的结构定义齐备——第一层写明 `.ai/INBOX.md` 的条目字段清单、条目稳定键的形态、状态枚举与合法转移；第二层写明 `规模` 三档取值、每档对草稿的结构要求（`milestone` 档维持「范围评估 / 理解阐释 / 拆分路线图 / 范围演进记录」四段，另两档给出各自的轻量段落集）；第三层写明出区的合法去向与各自前置条件。三层的状态枚举都是封闭枚举，逐条给出取值与转移条件，无「等等」「视情况」这类开口。
- [ ] AC2: 新契约含**生效时点声明**，三要素齐备——①点明 `.ai/INBOX.md` 当前由 `inbox-schema.md` 定义、两份规则真源并存；②写明新契约在 R7 命令落地前零写入、R8 删旧契约后才独占该路径；③给出读者遇到分歧时该听哪一份的判据。`inbox-schema.md` 与 `inbox-workflow.md` 逐字节未改（哈希比对为证）。
- [ ] AC3: 新契约里出现的每一个仓内路径都指向**当前真实存在**的落点——全文不出现 `.ai/backlog/`；孵化区一律写 `.ai/milestone-backlog/`。另有一处明写该目录将在 R9 改名、届时本契约同批更新。
- [ ] AC4: 9 份存量候办草稿全部带上 `规模: milestone`，位置与既有的 `候办键:` / `候办状态:` 同处一块；9 份的其余内容逐字未改（`git diff` 每份恰 1 增 0 删）。
- [ ] AC5: `.ai/MILESTONES.md` **逐字节未改**——待办区表头仍是 5 列、9 行取值与顺序全部未动、正式表未动。规模只由草稿头部承载，索引不产生第二个真源。
- [ ] AC6: `milestone-schema.md §4.5` 的编写规则改到位——「候办草稿沿用 §5 的四段结构」那条改为「`milestone` 档必须四段，`iteration` 与 `undecided` 档按新契约分档」并给出新规则文件的指针，同时把草稿头部必须标明的标记由两项扩为三项（加 `规模`）。该文件 `git diff` 的改动行全部落在 §4.5 编写规则那一段内，§4.5 的索引表模板与 §5 正文零改动。
- [ ] AC7: `Coder/README.md` 的目录结构与读取顺序两处都注册了新文件；`scripts/verify-ci.sh` 里既有的注册一致性检查通过。
- [ ] AC8: `.ai/MILESTONE.md §5.4` 追加三条登记——①路径撞车（新旧契约共占 `.ai/INBOX.md`）的处置与理由；②`.ai/backlog/` 改名定序（为什么按现实路径写而不是按路线图字面写）；③孵化区规模分档对 `milestone-schema.md` 的连带影响与 9 份回填。
- [ ] AC9: `.ai/debt.md` 由 10 条增为 12 条，新增的两条各自写明缺口、有意不做的理由与自然消解路径（分别归 R8 与 R15）；原 10 条首句逐条未动。
- [ ] AC10: 旧 inbox 全链零改动——`inbox-schema.md`、`inbox-workflow.md`、两份 hook 测试、`tools/inbox/` 全目录、`.claude/commands/butler/inbox.md`、`plugins/butler/skills/butler-inbox/`、`workflows/registry.json` 的 inbox 块，逐一与本轮开工前的内容哈希相同。
- [ ] AC11: `.ai/OVERVIEW.md` 由 `--write` 重算且 `--check` 退出码 0；规则文件计数随新增文件递增，工作流清单仍 12 行不变。
- [ ] AC12: `bash scripts/verify-ci.sh` 退出码 0；`python3 scripts/audit-project-state.py --project-root . --allow-unreleased` 退出码 0，`[UNRELEASED]` 恰 2 条。可重跑扫描断言两组均零命中——A 组查越界（全仓活跃面不出现 `.ai/backlog/`、新契约不出现 `SRC-` 与双指纹字段名、`.ai/MILESTONES.md` 未被改动），B 组查在场（旧链七处哈希未变、新契约三层定义与生效时点声明齐备、9 份草稿规模字段齐、README 两处注册在场）。

## Verification Method

- AC1 / AC2 / AC3: 逐条 `grep -qF` 断言关键结构名、字段名、枚举取值与声明措辞在场；状态枚举用脚本解析成列表后断言长度与取值集合；`git diff` 人读确认三层定义写得对不对（机器只能证字样在场）。
- AC4 / AC5: 对 9 份草稿逐个 `git diff --numstat` 断言恰 1 增 0 删；`.ai/MILESTONES.md` 与本轮开工前的内容哈希比对，须逐字节相同。
- AC6 / AC7: `git diff` 断言 `milestone-schema.md` 的改动行全部落在 §4.5 编写规则段内；`grep -c` 断言 `Coder/README.md` 两处注册；`verify-ci.sh` 取退出码。
- AC8 / AC9: 逐条 `grep -qF` 断言关键措辞；`grep -c '^- \*\*'` 断言 debt 条目数 10 → 12，原 10 条首句逐条断言仍在。
- AC10: 开工前录下旧链七处的 sha256 基线，收口时逐一比对（`tools/inbox/` 按目录内全部文件的哈希清单比对）。
- AC11: `--write` 后 `--check` 取退出码；`wc -c` 实测；`grep -c` 断言工作流清单行数。
- AC12: 两条命令各取退出码并留存完整输出；新增 `.ai/iterations/ITER-0117/` 下一条两组扫描脚本，模式串用变量拼接避免自命中，排除面在 VERIFY_REPORT 里逐份摊开。

## External References

- 本迭代无 `.ai/references/` 外部参考资料。
- 内部依赖：`Coder/40_Context_Management/inbox-schema.md`（旧契约，只读参照）、`Coder/20_Workflow_Lifecycle/milestone-schema.md §4.5 / §5`（孵化区现行定义）、`.ai/MILESTONE.md §5.1 / §5.3`（R6–R9 的范围与定序）。

## Open Questions / Risks

- **闪念口条目的稳定键形态未定**（P3 定）。已定的是方向：给一个轻量稳定键，但**不做**递增号池、不做内容指纹认亲——那正是旧契约里最重、且被本里程碑判为过度设计的部分。
- **孵化区索引承不承载规模**：P3 已定为**不承载**（第三个选项，既不加列也不另立）。理由是加列会造出规模的第二个真源，而防漂移要新增机器断言、恰是本轮不做的；`/butler:inbox list` 需要按规模筛选时，R7 从草稿头部读即可，9 份小文件的读取成本可忽略。已按 §5.3 amend 到位。
- **`undecided` 档会不会变成垃圾桶**。缓解方向是在契约里给它一个出区压力（必须记录「卡在哪」而不只是标题），具体措辞 P3 定。
- **风险 · 两份 inbox 规则真源并存三个迭代**。缓解手段只有在两份文件里互相写明分工与生效时点，没有机器能拦住模型读错那一份。本轮如实登记为欠账，不假装解决。
- **风险 · 契约写完到 R7 实现之间，新契约完全没有使用者**。写得对不对要等 R7 真跑一条闪念到执行才知道。本轮的验收只能证「结构齐备、路径为真、旧链没碰」，证不了「这个结构好用」。
