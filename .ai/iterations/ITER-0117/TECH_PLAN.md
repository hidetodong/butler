<!-- butler-artifact-template: 1.0.0 artifact=tech_plan -->
# TECH_PLAN — ITER-0117

方案状态: pass

## Design Decisions

- **D1 · 新契约落 `Coder/40_Context_Management/intake-schema.md`，标题「需求录入三层契约」。** 落 40 目录，是因为闪念口和孵化区管的都是「一个想法跨会话别丢」，跟同目录的 `inbox-schema.md`、`references-schema.md` 是一类事；R8 删掉旧契约之后，新文件不用搬家。名字取 `intake`（录入），因为 butler 里已经有这个词——`20_Workflow_Lifecycle/iteration-intake.md` 讲的就是「外面来的东西怎么接进流程」，读者不用学新词。**不用** `inbox-schema-v2` 这类带版本号的临时名：那种名字到 R8 还得再改一次，白搭一轮改名和一轮全仓引用修正。

- **D2 · 闪念口 `.ai/INBOX.md` 用一张表，不设受管区块标记。** 受管区块标记就是 `<!-- xxx:begin -->` / `<!-- xxx:end -->` 那种成对注释，机器靠它认边界、然后整块覆盖重写。旧契约需要它，是因为 scanner（自动扫盘登记来源的程序）每次都要把整块推倒重写。新的闪念口只有两种写法——在表尾追加一行、改某一行的状态列——没有整块重写这回事，标记就成了纯负担。表头定死为 `| 闪念键 | 记于 | 一句话 | 状态 | 去向 |`，整张表放在一个固定的二级标题下。

- **D3 · 闪念键用「日期 + 短横线短句」，不做号池、不做指纹认亲。**（对应 AC_LIST 里那条未定项）形如 `2026-08-20-inbox-too-heavy`，同一文件内唯一，同一天撞名就在尾巴上接 `-2`、`-3`。**不做**递增号池（`SRC-0001` 那种全局计数器，得有人维护「下一个号是几」），**也不做**内容指纹认亲（旧契约拿两个 SHA-256 比「这份来源变没变、是不是同一条」）。理由是闪念本来就是人随口记的一句话，没有「同一条内容的第二版」这个概念；真重复记了两条，人自己删一条比机器认亲便宜得多。先例现成：`.ai/references/prd/` 底下的需求目录早就是日期加 slug，读者不用再学第二套命名。

- **D4 · 闪念状态四态封闭，转移只有四条，终态不回头。** 四态是 `new` / `incubated` / `done` / `dropped`。合法转移穷举：`new → incubated`（进了孵化区，去向列填草稿路径）、`new → done`（当场就办了，去向列填迭代号或一句话）、`new → dropped`（不办了，去向列填一句话原因）、`incubated → dropped`（孵化区草稿被撤回时回写这一笔）。终态（`done` / `dropped`）**不许**回 `new`——同一件事又想起来，那就是一条新闪念、新日期新键。允许回退等于给状态机开一个环，而本轮没有任何机器检查能拦住环里的错。清理纪律：终态行等「去向」指的东西真落地之后可以整行删掉，不留墓碑（跟 `.ai/debt.md` 一个规矩，还清了就删）；`new` 行**不许**删，只许转移，否则「记了但被悄悄抹掉」这条路就通了。

- **D5 · 孵化区草稿头部由两行加到三行，结构按档分。** 头部改为 `候办键:` / `候办状态: deferred` / `规模: milestone|iteration|undecided`，三行各恰好一次。每档要求的段落：`milestone` 档维持现有四段（范围评估 / 理解阐释 / 拆分路线图 / 范围演进记录）一字不减，9 份存量草稿全归这一档；`iteration` 档只要两段——「要解决什么」和「暂缓原因」，因为迭代真开起来的第一件事就是 P1 重写 CONCEPT，草稿里写再多拆分路线图也会被覆盖；`undecided` 档也是两段——「想做什么」和「卡在哪」。**「卡在哪」是强制的，而且必须点名一个具体缺口**（缺哪份数据、缺哪个决定、缺哪个前置件），不接受「还没想好」这种话。这是 `undecided` 档的出区压力：写不出卡在哪，说明这条根本不配占孵化区一个位置。档位允许改（升降都行），但改档必须把新档要求的段落补齐，并在草稿里记一行改档原因。

- **D6 · 规模只写在草稿头部，`.ai/MILESTONES.md` 待办区索引一列不加。** 这是本轮相对 P2 的改判，已按 `iteration-schema.md §5.3` amend 进 AC_LIST。明面成本是改代码：`scripts/audit-project-state.py` 的 `milestone_backlog_rows()` 写死 5 列（列数不对直接抛错）、用 `values[1:-3]` 兜住标题里的竖线、用 `row[3]` 取草稿路径，加一列要动 3 处；`scripts/test-audit-project-state.py` 6 个测试方法里有 11 行 5 列夹具跟着改。但真正劝退的是暗成本：规模同时躺在草稿头部和索引行，就有了两个真源，防它俩漂移得再加一条一致性断言——**而那正是本轮 Out of Scope 明写不做的**。butler 已经被这种「登记了但没人对账」的假条目咬过好几次（`invariants.md` 的假条目、`.ai/debt.md` 里那条已经还清却还挂着的欠账）。将来 `/butler:inbox list` 要按规模筛，R7 直接从 9 份小文件的头部读就行，读取成本可以忽略。

- **D7 · 执行分流三条出口，封闭；`undecided` 不能直接出区。** 三条穷举：①**提升为里程碑**——只有 `milestone` 档能走，前置是当前没有 active 里程碑，动作走 `milestone-schema.md §7.1`（开启 / 候办提升）；②**开为迭代**——只有 `iteration` 档能走，前置是当前没有 active 迭代，动作走 `iteration-schema.md §5.1`（开启）；③**撤回**——任意档都能走，理由记进 `.ai/MILESTONE.md §5.4`（范围演进记录）。`undecided` 档必须先定档才能走前两条，这是它的第二道出区压力。每条出口都**两侧原子**：删草稿文件和删索引行必须一起做。现成的兜底是审计里的 `milestones.backlog_set` 检查（索引行集合必须与目录里的文件集合完全相等），漏删任一侧，下一次审计就红。另外明写一句：**ideation（探索）是孵化的手段，不是出口**——探完了还得走上面三条之一。写这句是因为它最容易被误当成第四条路。

- **D8 · 生效时点声明用 H1 底下一段引用块，三要素齐备。** 形状照抄 ITER-0116 给 `/butler:loop` 写冻结声明那次，已经验证过读者一眼能看见。三要素：①点明 `.ai/INBOX.md` 当前由 `inbox-schema.md` 定义、两份规则真源并存；②写明本契约在 R7 命令落地前对该路径零写入，R8 删掉旧契约后才独占；③给判据一句话——**凡涉及 `.ai/INBOX.md` 的读写格式，在 R8 删掉 `inbox-schema.md` 之前一律以 `inbox-schema.md` 为准**。声明里还要如实写一句「这条分工没有任何机器检查兜底，靠本段和评审自觉」，同一件事另记进 `.ai/debt.md`。分工只能单向声明（新契约指回旧的），因为本轮 Out of Scope 明写不动 `inbox-schema.md` 一个字。

- **D9 · `milestone-schema.md` 只改 §4.5 编写规则那一段里的两条，索引表模板与 §5 正文零改动。** 两条分别是：①草稿头部标记那条，由「恰好标明一次 `候办键` 和一次 `候办状态`」扩为三项，加上 `规模`；②「候办草稿沿用 §5 的四段结构」那条，改为「`milestone` 档必须四段，`iteration` 与 `undecided` 档按 `intake-schema.md` 分档」并给出指针。§4.5 里那段 5 列表模板一个字不动（这是 D6 的直接后果），§5 正文也不动。

- **D10 · `Coder/README.md` 注册两处，但要知道只有目录级有机器检查。** 两处是：`## 目录结构` 里 `/40_Context_Management` 那棵树（插在 `inbox-workflow.md` 之后）、`## 读取顺序` 底下那串逐文件指针说明（同样插在 `inbox-workflow.md` 那条之后）。**实话**：`scripts/sync-project-overview.py` 只校验「每个目录有没有说明」，不校验「每个文件有没有指针」，所以文件级注册漏掉了机器不会报——本轮靠 `grep -c` 逐处自证，不假装有门禁。

- **执行顺序**：T1 写 `intake-schema.md` 全文（含 D8 声明）→ T2 回填 9 份草稿的 `规模: milestone` → T3 改 `milestone-schema.md §4.5` 两条 → T4 `Coder/README.md` 两处注册 → T5 `.ai/MILESTONE.md §5.4` 追加三条登记 → T6 `.ai/debt.md` 加两条（10 → 12）→ T7 `sync-project-overview.py --write` 重算 OVERVIEW → T8 写两组扫描脚本并跑通 → T9 CI + 审计取退出码。基线已在 P3 末录好：`.ai/iterations/ITER-0117/legacy-inbox.baseline`（旧 inbox 全链 13 行）与 `.ai/iterations/ITER-0117/pre-p4.baseline`（`.ai/MILESTONES.md`、`milestone-schema.md`、`Coder/README.md`、9 份草稿，共 12 行）。

## Failure Paths

- **两份 inbox 契约并存三个迭代，模型读错哪一份。** 后果是把 `.ai/INBOX.md` 写成错格式。缓解只有 D8 的单向声明，没有机器能拦。本轮如实登记为欠账（归 R8 自然消解），不假装解决。
- **回填 9 份草稿时误改正文。** 检出手段：每份 `git diff --numstat` 必须恰 1 增 0 删，多一行就是误改；另有 `pre-p4.baseline` 兜底做整体对照。
- **新契约里写了 `.ai/backlog/`。** 路线图字面写的是这个路径，但它到 R9 才存在，照抄就会写出一句假话。检出手段：A 组扫描断言全仓活跃面零命中。
- **`.ai/MILESTONES.md` 被顺手改了。** D6 定了一列不加，但改 `milestone-schema.md` 时很容易顺手把索引也「对齐」一下。检出手段：与 `pre-p4.baseline` 逐字节比对。
- **`milestone-schema.md` 的改动溢出 §4.5 编写规则段。** 检出手段：`git diff` 取改动行号，断言全部落在该段的行号区间内。
- **`Coder/README.md` 漏注册一处。** 如 D10 所说机器不报，只能 `grep -c` 两处各断言 1。
- **OVERVIEW 的规则文件计数没跟上新增文件。** 检出手段：`--write` 重算后 `--check` 取退出码，另断言工作流清单仍 12 行未被牵动。
- **扫描脚本自命中**（脚本里为了查禁字样，自己先写了那个字样）。缓解：模式串用变量拼接，跟 ITER-0116 同法。
- **扫描脚本的排除面偷偷放过真问题。** 缓解：排除面在 VERIFY_REPORT 里逐份摊开，带每份命中数与放行理由，不给「扫了 N 个文件全绿」这种笼统结论。

## Test Strategy

- **本轮无 TDD 配对证据**：改动全是规则文本，没有可跑的代码路径，做不出「同一条测试命令先失败后通过」的配对。VERIFY_REPORT 的 TDD 段记 N/A 并写明理由。
- **每条 AC 一个可重跑证据脚本**，落 `.ai/iterations/ITER-0117/`，由 `tools/verification-evidence/evidence.py run` 记录，收口时归档。
- **两组扫描各一遍**：A 组查越界（全仓活跃面不出现 `.ai/backlog/`、新契约不出现 `SRC-` 与双指纹字段名、`.ai/MILESTONES.md` 未被改动），B 组查在场（旧链七类落点哈希未变、三层定义与生效时点声明的关键字样齐备、9 份草稿规模字段齐、README 两处注册在场、`milestone-schema.md` 两条改到位、debt 由 10 增为 12）。
- **状态枚举用脚本解析成列表再断言**，不只 grep 单个词——要证「恰好这四态、恰好这四条转移」，靠数量和集合相等，不靠字样在场。
- **门禁两条取退出码**：`bash scripts/verify-ci.sh` 须为 0；`python3 scripts/audit-project-state.py --project-root . --allow-unreleased` 须为 0 且 `[UNRELEASED]` 恰 2 条。
- **机器证不了的部分说清楚**：三层结构写得对不对、`undecided` 的出区压力管不管用，机器只能证字样在场，证不了好用。真话要等 R7 把命令做出来、真跑一条闪念到执行才知道。这条写进 VERIFY_REPORT 的剩余风险。

## References Compliance

- 本迭代无 `.ai/references/` 外部参考资料，无 PRD 约束，无 workspace scope 边界需要对账。
- 内部依赖与引用方式：`Coder/40_Context_Management/inbox-schema.md`（只读参照，一个字不改）；`Coder/20_Workflow_Lifecycle/milestone-schema.md §4.5`（本轮改两条）、`§5`（新契约指针引用，不重抄）、`§7.1`（出口一的动作真源，指针引用）；`Coder/20_Workflow_Lifecycle/iteration-schema.md §5.1`（出口二的动作真源，指针引用）、`§5.3`（本轮 amend 依据）；`.ai/MILESTONE.md §5.1 / §5.3`（R6–R9 的范围与定序）。
- 书写口径按 `20_Workflow_Lifecycle/artifact-style.md`：新契约面向 AI 执行，措辞用「必须 / 不得」；但里面给人读的说明句仍守说人话四条——术语第一次出现紧跟一句大白话（受管区块标记、指纹认亲、号池这几个词都已按此处理）。
- 新增文件按 `CLAUDE.md` 的约束在 `Coder/README.md` 两处注册，不引入隐式依赖。
