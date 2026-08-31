<!-- butler-artifact-template: 1.0.0 artifact=tech_plan -->
# TECH_PLAN — ITER-0119

方案状态: pass

## Design Decisions

### D1 · 原件落 `.ai/references/raw/`，用目录承载身份

`.ai/references/` 下并存两类保真度，靠**目录**区分而不是文件名前缀：`raw/` 之下是用户原件（自管、AI 只读、非权威），其余（扁平资料与 `prd/` 集合）是 AI 派生的受控投影。选目录的理由是路径前缀能被工具与 hook 机械判定，而文件名前缀写错一个字就静默丢掉保护。`raw/` 与 `references/` 其余子目录一样按需产生，部署时不建——部署只建 `.ai/` 与 `deliveries/` 两个目录。

`references-schema.md` 的改写落在两处：§1 把「外部真源的落盘区」这句保留，下面那张对照表重做——现在的表拿 `.ai/references/` 对比 `.ai/project/`，而 `.ai/project/` 在 R1（ITER-0112）已退役，对比对象本身不存在了。新表改为在 `.ai/references/` **内部**对比两类保真度，列是「子区 / 存什么 / 谁写 / 权威性」，把「引用 references 里的东西不再自动等于引用权威投影」这件事写在最显眼处。§2「两类资料」扩为三类，原件一类明写不受 `prd_id` 约束、不进版本历史、不被 `prd-split` 消费。

### D2 · `origin/` 的改写按「纪律搬家、目录退役」两件事分开做

18 份文件里提到 `origin/` 的语句分三种，改法不同：

| 语句类型 | 出现处 | 改法 |
|---|---|---|
| 部署要建这个目录 | `mcv-deployment.md §2`、`/butler:init` 步 2、`butler-init` skill、`rule-card.md` 第 63 行 | 目录集由三个减为两个 |
| 材料从这里来 | `milestone-schema.md`（输入表 / §6.4 步 1 / §7 命令表 / 第 208、212 行）、`/butler:prd` 第 19 行、`HUMAN_GUIDE.md` 第 247、255、258 行、`rule-card.md` 第 51 行 | 路径改指 `.ai/references/raw/` |
| AI 不许动用户原稿 | `mcv-deployment.md §0.1 / §2`、`references-schema.md §10`、`butler-upgrade.md` 第 76、115 行、`README.md` 第 315 行、`HUMAN_GUIDE.md` 第 174、177 行 | 纪律逐字保留，主语从 `origin/` 换成 `.ai/references/raw/` |

第三类是本轮最容易做错的地方：删目录时顺手把纪律一起删掉，扫描会显示零命中、看起来很干净，实际上把一条真规矩弄丢了。防线是 AC9——`references-schema.md §10` 那条非回归门与 `test_prd_collection_contract.py` 第 56 行的逐字断言配对，改完要现场演一次「把规则正文那句删掉、测试必须红」。

`mcv-deployment.md` 另有两处连带：第 61 行整段重写（`origin/` 的职责段搬进 `.ai/` 的说明里），第 79 行 `INBOX.md` 的描述还在说「双指纹、派生关系回执」并指向 `inbox-schema.md`，那是旧契约的形状，改指 `intake-schema.md` 并改成闪念口的描述。

### D3 · 删除的执行顺序：先摘引用，后删文件

顺序是「改所有引用方 → 删被引用的文件 → 跑扫描」。反过来先删文件会让中间态出现一堆指向不存在文件的死引用，若中途中断就留下比开工前更烂的现场。具体批次：

1. **B1 引用改写**：`Coder/README.md`（目录树第 96–97 行、职责段第 220–221 行）、`mcv-deployment.md`、`HUMAN_GUIDE.md`、`intake-schema.md`（第 10 行生效时点声明整块、第 49、182 行两处旧契约引用）、`intake-workflow.md` §6「与旧链的关系」整节、`.ai/invariants.md` 第 48 条。
2. **B2 `origin/` 改写**：按 D2 那张表逐份改。
3. **B3 删除**：`inbox-schema.md`、`inbox-workflow.md`、`tools/inbox/` 整目录、`templates/hooks/tests/test_inbox_contract.py`。
4. **B4 测试面**：`test_inbox_workflow.py` 删一个用例、`test_mile0009_e2e.py` 摘 inbox 段、`test_prd_collection_contract.py` 改断言、`scripts/test-butler-upgrade.py` 第 398 行夹具改路径、`tools/intake/tests/` 加回归用例、`verify-ci.sh` 删一行。
5. **B5 台账与派生**：`.ai/debt.md`、`.ai/MILESTONE.md §5.4`、`.ai/OVERVIEW.md --write`。

`intake-schema.md` 与 `intake-workflow.md` 里那些「旧链还在、R8 删」的过渡性表述本轮必须一起清掉，否则删完之后新契约自己在说假话——这是 AC1 与 AC16 A 组会抓到的。

### D4 · hook 树一个字节都不动

原 AC10 撤回的实测依据：`scripts/test-butler-upgrade.py` 的 `test_whitelist_holds_only_recomputable_history_digests` 末尾有一条断言，要求工作区 `templates/hooks/` 的树摘要等于 `VERSION` 对应 git tag 的摘要。`VERSION` 是 `3.6.0`、`v3.6.0` 已打 tag，所以任何非测试 hook 文件的改动都会让它红（探针实测 `bd92a614…` != `84a3c089…`）。把 `VERSION` 抬到 `3.7.0` 想绕开，结果是 1 失败变成 1 失败 + 4 错误。

好消息是 `skip_hook_file()` 明确排除 `tests` / `__pycache__` / `.pytest_cache` 三类路径，摘要只含 19 个文件（`README.md`、两个入口、`lib/` 5 份、`rules/` 9 份）。本轮要动的三份测试全在 `tests/` 下，不进摘要。AC3 与 AC16 B 组各有一条断言用 `upgrade.py` 的 `hook_source_files` + `tree_digest` 现场复算，确认摘要与开工前逐字相同——这既是「没越界」的证明，也是「删测试是安全的」的证明。

### D5 · `test_mile0009_e2e.py` 只摘头段，不整份删

那份 e2e 是 MILE-0009 的资产，链条是 inbox scan → prd-migrate → prd-status → prd-update → workspace-scope 五段。inbox 那一段（第 12 行常量、第 45–47 行 `origin/` 夹具、第 63–68 行三条断言）随旧工具消失，余下四段与 MILE-0009 的其它能力有关、仍然有效，整份删会连带丢掉四个工具的端到端覆盖。文件名与类名不改。

### D6 · `SRC-` 字样分两类处理

`SRC-NNNN` 作为**旧收件箱的来源身份**要清干净（`inbox-schema.md`、`tools/inbox/`、`test_inbox_contract.py` 随文件一起删；`.ai/invariants.md` 第 48 条改写）。但 `tools/prd-status/tests/`、`tools/prd-update/tests/`、`tools/mile0009-e2e/tests/` 里的 `SRC-1` / `SRC-2` 是 PRD 集合表「来源线索」列的**任意字符串夹具**——`references-schema.md` 第 66 行对那一列的定义是「可用于认回同一需求的稳定源标识或回执指针」，不绑定任何编号体系。这些夹具改成不带 `SRC-` 的值（如 `paste-1`），避免扫描误报，也避免读代码的人以为那列还锁着已退役的编号规则。这是 AC16 A 组必须能区分的两类，扫描脚本的模式串要精确到「`SRC-` 后跟四位数字」而不是裸 `SRC-`。

### D7 · `.ai/invariants.md` 第 48 条改写而不是删除

那条不变量记的是「需求录入这件事的形状」，形状变了，条目该跟着变而不是消失——删掉等于让不变量清单少一条真规矩。改写后描述现行三层契约：三层结构、日期化闪念键（不用递增号池、不做内容指纹认亲）、四态封闭状态机、`tools/intake/intake.py` 是唯一写盘者，`*为什么*` 段保留原有理由里仍成立的部分（语义判断不能冒充机械事实、处理便利不能侵犯用户原稿所有权），并补真源指针 `intake-schema.md`。条目总数不减是 AC10 的硬断言。

## Failure Paths

- **改引用时漏掉一处，扫描抓不到**：扫描按字面串匹配，改成同义但不同字面的说法（例如把「`origin/`」写成「原始材料目录」）就会漏网。防线是 AC16 A 组扫完之后人眼过一遍 `git diff` 的全部改动行，重点看四份人读文档（`README.md`、`HUMAN_GUIDE.md`、`docs/prd-migration-guide.md`、`rule-card.md`）读起来是否还通顺、有没有指向不存在目录的句子。
- **纪律被顺手删掉**：见 D2。取证方式是把 `references-schema.md §10` 那句临时删掉、跑 `test_prd_collection_contract.py`、确认红、再恢复；完整输出入证据。若那条测试改完之后删掉规则正文仍然绿，说明断言已经被架空，必须重写断言而不是接受。
- **删文件时误删还在用的东西**：`tools/inbox/` 与 `tools/intake/` 名字只差两个字母，删错整轮报废。执行时用 `git status` 逐条确认删除清单，删完立刻跑 `python -m unittest discover -s tools/intake/tests -t .`，绿了才继续。
- **中途中断留下半截态**：B1–B5 五个批次里，B3（删文件）之前的任何中断都可以 `git checkout -- .` 干净退回；B3 之后中断会留下「文件已删、引用未清」或反过来的现场。缓解是 B3 放在 B1、B2 之后执行，且 B3 一次做完不拆散。最坏情况整轮 `git checkout` 退回，代价是 `.ai/` 下本轮新写的台账与产物一起丢，要手工重开迭代——这一点已写进 AC 的风险段。
- **`OVERVIEW.md` 计数对不上**：`sync-project-overview.py` 从目录实际内容重算，删两份规则文件后 `40_Context_Management/` 应由 13 变 11。若 `--check` 仍红，先查是不是有残留的 `__pycache__` 或空目录被计入，不要改脚本迁就。
- **审计的 `[UNRELEASED]` 条数变化**：本轮不切版不提交，审计应仍是恰 2 条（未提交改动 + tag 不在 HEAD）。若变成 3 条或 0 条，说明有非预期的版本面改动，停下查清再继续。

## Test Strategy

本轮**不声明 TDD cycle**。理由如实写在这里：AC11 那道旧格式回归防线所锁的行为在本轮之前已经正确——实测 `add`、`list`、`handle` 三个子命令在旧格式 `.ai/INBOX.md`（`SRC-NNNN` 表头 + managed marker）上全都以退出码 1 报错、输出可读错误、且目标文件字节前后完全相同。测试写出来即绿，没有真实的红。硬造红只能把 `intake.py` 临时挪走演一遍，那是重演不是 TDD，不值得为凑一份配对证据去做。本轮其余改动是删除与文字改写，本身也没有可先红后绿的实现面。

实际的验证手段：

- **回归防线（AC11）**：`tools/intake/tests/test_intake.py` 新增一个测试类，用现有 `helpers.make_root()` 造项目根后覆写 `.ai/INBOX.md` 为旧格式，对三个子命令各断言退出码非零、`{"error": ...}` 在 stdout、`read_bytes()` 前后相等。
- **既有测试面不退化**：`templates/hooks/tests/` 全套、`tools/intake/tests/`、`tools/mile0009-e2e/tests/`、`scripts/test-butler-upgrade.py` 各自单跑取退出码，最后 `bash scripts/verify-ci.sh` 整跑取退出码。
- **删除的完整性**：`.ai/iterations/ITER-0119/ac-sweep.py` 两组扫描，模式串一律用变量拼接（`"inbox" + "-schema"`、`"SR" + "C-"` 加四位数字正则、`"ori" + "gin/"`）避免脚本自命中；排除面写死在脚本里并在 VERIFY_REPORT 逐份列明理由。
- **hook 树未变**：用 `tools/butler-upgrade/upgrade.py` 的 `hook_source_files` + `tree_digest` 现场复算，断言等于开工前记录的 `bd92a614f9582451ec3150d2c1113a2262bb874b97fd085adf6ad0ce7c91e56d`。
- **开工前基线**：B1 动手之前先把旧链 4 份文件与 `templates/hooks/tests/test_inbox_workflow.py` 的 SHA-256 存进 `.ai/iterations/ITER-0119/pre-p4.baseline`，供 AC3 的逐字节比对使用。

## References Compliance

- 本迭代无 `.ai/references/` 外部参考资料，不涉及 PRD 切片对账。
- 本轮**改写** `Coder/40_Context_Management/references-schema.md` 的 §1 与 §2（定位与资料分类），属于该契约自身的演进而非对它的消费。按其 §10 非回归门自查：不用 PRD 的对话驱动流不变；`api-` / `design-` / `insight-` 扁平资料流不变；「用户原稿不被改写、移动或删除」这条纪律逐字保留、只换主语（这是 AC9 的硬断言）；已冻结与已收口产物不被回写。§10 的最后一条要求「有意修改既有 PRD 消费者时必须列出原因与兼容策略」——本轮不改任何 PRD 消费者（`prd-split` / `prd-status` / `prd-update` / `prd-migrate` 的行为面零改动，只动测试夹具里的无语义字符串）。
- 按 `migration-schema.md §5` 判定对已部署项目的影响：改了 `templates/rule-card.md` → 切版配方**必须含 `[regen-entrypoints]`**；`templates/hooks/` 零改动 → **不需要 `[sync-hooks]`**；`.ai/` 下产物结构无新增必填字段 → 不需要 `[add-field]`；`origin/` 目录的删除与内容搬迁**无对应 typed 动作可用**（升级器只有 rename / split / add-field / regen-entrypoints / sync-hooks / restamp / no-op），归 R14 新增删除与移动两类标签之后才能表达。这四条结论要原样登记进 `.ai/MILESTONE.md §5.4`。
