---
状态: ack-frozen
ACK 日期: 2026-08-21
修订记录: 2026-08-21 · ① ACK 前调整：`origin/` 的落点由「用户点名任意路径」改为「收进 `.ai/references/raw/`」，由用户拍板——所有外部资料引用统一进 `.ai/references/`，不再另开通道；随之新增 `references-schema.md` 定位扩写与 hook 门禁两条，AC 由 15 增为 17。② P3 修订（按 `iteration-schema.md §5.3` 退回 draft 并重新 ACK）：撤回原 AC10（给 `.ai/references/raw/` 加 hook 门禁）。实测证明它与本轮 Out of Scope 不可兼得——`scripts/test-butler-upgrade.py` 有一条断言要求工作区 hook 树摘要等于当前 `VERSION` 对应 tag 的摘要，而 `VERSION` 是 3.6.0、`v3.6.0` 已打 tag，改 `templates/hooks/` 任何非测试文件都会让 CI 红（探针实测：`bd92a614…` != `84a3c089…`）；抬 VERSION 绕不开（1 失败变 1 失败 + 4 错误）。门禁改为记账（`debt.md` 加条目 + §5.4 登记），条件写明「下次切版之后的任意一轮」。③ 同时修订原 AC12：旧格式回归防线去掉「先红后绿有配对证据」——实测 `add` / `list` / `handle` 三个子命令在旧格式 `.ai/INBOX.md` 上都已经报错退出且零写入，行为已正确，写出来就是绿的，没有真实的红；降级为回归防线，本轮不声称 TDD 配对。原 AC11–AC17 顺延为 AC10–AC16，共 16 条。
---
<!-- butler-artifact-template: 1.0.0 artifact=acceptance -->
# AC_LIST — ITER-0119

## Goal

- 把旧的需求收件箱体系整套拆掉，让仓里只剩一套录入机制；同时把散在项目根的 `origin/` 收进 `.ai/references/raw/`，让「外部资料」这件事只有一个家。收口态是「两份旧规则真源、整个 `tools/inbox/`、旧合同测试全部消失，`origin/` 退出活跃面，CI 与审计全绿，全仓静态扫描零残留」，并且「AI 对用户原件只读不改」这条纪律要活下来、绑定新位置。给这条纪律装机器门禁本轮做不到（与切版顺序冲突，见修订记录），如实记账而不是假装做了。已部署项目侧本轮只能做到「不再创建、不再读、不再教」，做不到的部分明确指向 R14。

## In Scope

- 删规则真源两份：`Coder/40_Context_Management/inbox-schema.md`、`inbox-workflow.md`；同步摘掉 `Coder/README.md` 的目录树与职责段两处注册。
- 删整个 `tools/inbox/` 目录，并摘掉 `scripts/verify-ci.sh` 里那行 `tools.inbox.tests.test_inbox`。
- 删 `templates/hooks/tests/test_inbox_contract.py` 整份；删 `test_inbox_workflow.py` 里 R7 特意留下的 `test_inbox_workflow_route_and_safety_contract` 一个用例。（`templates/hooks/tests/` 不进 hook 树摘要，已实测确认，不触发升级器白名单对账。）
- 改 `tools/mile0009-e2e/tests/test_mile0009_e2e.py`：摘掉链条开头调 `inbox scan` 的那一段与 `origin/` 夹具，其余工具链断言原样保留。
- 退役 `origin/` 目录名，原件改放 `.ai/references/raw/`：扩写 `references-schema.md` 的定位与资料分类，改写部署协议、里程碑 brief 通道、`/butler:prd` 材料来源，并一次性清掉 `mcv-deployment.md`、`milestone-schema.md`、`butler-upgrade.md`、`/butler:init`、`butler-init` skill、`templates/rule-card.md`、`README.md`、`HUMAN_GUIDE.md`、`docs/prd-migration-guide.md` 与三份测试夹具里的旧目录名。
- 清掉新链文件里对旧链的过渡性表述：`intake-schema.md` 的生效时点声明与两处旧契约引用、`intake-workflow.md` 的「与旧链的关系」一节。
- 改写 `.ai/invariants.md` 第 48 条，让它描述现行三层录入契约并带真源指针。
- 给 `tools/intake/` 补一道回归防线：遇到旧格式 `.ai/INBOX.md` 必须报错、非零退出、零写入。
- 按 `migration-schema.md §5` 判定本轮对已部署项目的影响，结论写进 `.ai/MILESTONE.md §5.4`。
- `.ai/debt.md` 清账；`.ai/OVERVIEW.md` 重算。

## Out of Scope

- **不动 `templates/hooks/` 下任何进摘要的文件**（`README.md`、`butler_gate.py`、`lib/`、`rules/`）——改一个字节 CI 必红，见修订记录。原件只读的机器门禁本轮不做，记账留待切版之后。
- 不改 `.ai/milestone-backlog/` 目录名、不迁 `deliveries/`（归 R9）。
- 不给升级器新增删除 / 移动两类 typed 动作（归 R14）；不写 `migrations/v4.0.0.md` 配方正文与已部署项目升级回归（归 R15，配方在切版时统一产出）。
- 不迁移已部署项目里已有的 `origin/` 内容——升级器没有移动动作，本轮做不到，只登记不假装。
- 不动 `.ai/INBOX.md` 里 R7 记下的那条真实闪念，不改 `tools/intake/` 的实现（只加测试）。
- 不动 `CHANGELOG.md`、`migrations/` 下已发布配方、`.ai/iterations/`、`.ai/milestones/`、`deliveries/` 与 `docs/research/` 里的历史记述——历史就该保留旧名。
- 不新增工作流 id，不改 `workflows/registry.json`（R7 已改完，本轮零改动）。
- 不切版、不发布、不提交、不打 tag。

## Acceptance Checklist

- [ ] AC1: `Coder/40_Context_Management/inbox-schema.md` 与 `inbox-workflow.md` 两份文件在工作树中不存在；`Coder/README.md` 的目录树与职责段两处注册均已摘除，全文不再出现 `inbox-schema` / `inbox-workflow` 任一字样。
- [ ] AC2: `tools/inbox/` 整目录（含 `README.md`、`__init__.py`、`inbox.py`、`tests/`）不存在；`scripts/verify-ci.sh` 不再出现 `tools.inbox`；全仓活跃面对 `tools/inbox` 与 `tools.inbox` 两个字样零命中。
- [ ] AC3: `templates/hooks/tests/test_inbox_contract.py` 不存在；`test_inbox_workflow.py` 仍在且只少了 `test_inbox_workflow_route_and_safety_contract` 一个用例——另两个用例的函数体与断言逐字节与开工前相同，用例数由 3 变 2。`templates/hooks/` 下进摘要的文件集与开工前逐字节相同（用升级器现有的 `hook_source_files` + `tree_digest` 口径断言摘要未变）。
- [ ] AC4: `tools/mile0009-e2e/tests/test_mile0009_e2e.py` 不再引用 `tools/inbox/inbox.py` 与 `origin/`，链条余下四个工具（prd-migrate / prd-status / prd-update / workspace-scope）的断言逐条保留；该测试单独跑通过。
- [ ] AC5: 全仓活跃面对 `origin/` 字样零命中。排除面必须在验证报告里逐份列明并给出理由，且只允许是「历史记述不改写」这一类：`.git/`、`__pycache__/`、`migrations/`（已发布配方）、`CHANGELOG.md`、`.ai/iterations/`、`.ai/milestones/`、`deliveries/`、`docs/research/`，以及本迭代自己的四件套。
- [ ] AC6: `references-schema.md` 的定位改写完整——§1 说明 `.ai/references/` 下并存两类保真度（`raw/` 原件：用户自管、AI 只读、非权威；其余：AI 派生的受控投影、供 P2/P3/P5 引用对账），§2 的资料分类同步加入原件一类并写明它不受 `prd_id` 约束；§1 那张对照表不再引用 R1 已退役的 `.ai/project/`。
- [ ] AC7: 部署协议只建两个目录——`mcv-deployment.md §2` 明写创建 `.ai/` 与 `deliveries/`，并说明 `.ai/references/raw/` 与 `references/` 其余子目录一样按需产生、部署时不建；`.claude/commands/butler/init.md`、`plugins/butler/skills/butler-init/SKILL.md`、`templates/rule-card.md` 三处同步，四处措辞互不矛盾。
- [ ] AC8: 里程碑 brief 与 PRD 的文件通道改写完整且自洽——`milestone-schema.md` 的输入通道表、合成步骤、命令表三处都改指 `.ai/references/raw/`，`.claude/commands/butler/prd.md` 的材料来源同步，`HUMAN_GUIDE.md` 教用户投材料的段落同步；改后不残留指向项目根 `origin/` 的说法。
- [ ] AC9: 「AI 对用户原件只读、不改写不重命名不移动不归档不删除」这条纪律仍可被 grep 到且已绑定新位置——`mcv-deployment.md` 与 `references-schema.md` 各至少一处；`templates/hooks/tests/test_prd_collection_contract.py` 那条逐字断言改指新措辞而非删除，改后仍能红（把纪律从规则正文里删掉会让它失败，需有取证）。
- [ ] AC10: `.ai/invariants.md` 第 48 条改写为描述现行三层录入契约（闪念口 / 孵化区 / 执行分流三层、日期化闪念键、四态封闭状态机、`tools/intake/` 是唯一写盘者），带可核对的真源指针；条目总数不减，其余条目逐字节未动。
- [ ] AC11: `tools/intake/tests/` 新增回归用例锁住现有行为——给一个旧格式 `.ai/INBOX.md`（`SRC-NNNN` 表头、managed marker），`add`、`list`、`handle` 三个子命令均须非零退出、输出可读错误，且文件字节与调用前完全相同。本条是回归防线不是 TDD 配对，验证报告须写明「行为在本轮之前已正确，本轮只是加锁」。
- [ ] AC12: `.ai/MILESTONE.md §5.4` 追加登记五条——①`origin/` 收进 `.ai/references/raw/` 的决定、用目录而非文件名前缀承载身份的理由、以及 `.ai/references/` 定位被迫扩写的代价；②hook 门禁撤出本轮的实测依据与恢复条件；③按 `migration-schema.md §5` 的迁移判定结论（改了 `templates/rule-card.md` → 配方必须含 `[regen-entrypoints]`；未改 hook 树 → 不需要 `[sync-hooks]`）；④已部署项目侧做不干净的部分（残留 `origin/` 目录与旧格式 `.ai/INBOX.md`）及其指向 R14 / R15 的处置路径；⑤本轮无 TDD 配对的理由。
- [ ] AC13: `.ai/debt.md` 清账正确——「两份 inbox 规则真源并存」条目删除（旧链已删、自然消解）；「已部署项目里旧格式 `.ai/INBOX.md` 的迁移义务没人认领」条目更新表述，写明旧工具已删、无回退路径，并纳入「已部署项目残留 `origin/` 无人搬运」这一新事实；新增两条——「原件只读无机器兜底」与「hook 树一改就必须跟切版绑在一起」（后者写明那条断言把「未发布的 hook 改动」判成了「白名单不可信」，两件事不是一回事）；其余条目首句逐条仍在，条目数变化如实说明。
- [ ] AC14: `.ai/OVERVIEW.md` 由 `--write` 重算且 `--check` 退出码 0；`40_Context_Management/` 规则文件计数比开工前少 2（13 → 11），驻留工具清单不含 `tools/inbox/`，工作流清单仍 12 行。
- [ ] AC15: `bash scripts/verify-ci.sh` 退出码 0；`python3 scripts/audit-project-state.py --project-root . --allow-unreleased` 退出码 0 且 `[UNRELEASED]` 恰 2 条、`[DRIFT]` 为 0。
- [ ] AC16: 可重跑扫描脚本两组均零命中——A 组查残留（活跃面无 `inbox-schema` / `inbox-workflow` / `tools/inbox` / `tools.inbox` / `origin/` / `SRC-NNNN` 身份字样 / `observed_sha256` 等旧字段名），B 组查在场（新契约与新工具三处仍在、原件只读纪律两处仍在且已绑 `raw/`、部署两目录四处一致、`test_inbox_workflow.py` 余两个用例仍在、hook 树摘要与开工前相同、`.ai/INBOX.md` 那条真实闪念行逐字节未动）。

## Verification Method

- AC1 / AC2 / AC3: `test -e` 断言文件与目录不存在；`git diff` 人读确认 `test_inbox_workflow.py` 只少一个用例；用 `git show HEAD:<path>` 取开工前内容，逐字节比对余下两个用例的函数体；hook 摘要用 `tools/butler-upgrade/upgrade.py` 的 `hook_source_files` + `tree_digest` 现场复算比对。
- AC4: 单独跑 `python -m unittest discover -s tools/mile0009-e2e/tests` 取退出码；`grep -c` 断言 `inbox` 与 `origin/` 在该文件中为 0。
- AC5: 一条 `grep -rIn` 扫描，排除面写死在脚本里并在验证报告里逐份列明理由；命中数必须为 0。
- AC6 / AC7 / AC8 / AC9: `grep -qF` 逐条断言关键措辞在场与旧措辞消失；AC9 的「能红」用临时删掉规则正文那句、跑 `test_prd_collection_contract.py`、确认失败、再恢复的方式取证，完整输出入证据。
- AC10: `git diff .ai/invariants.md` 断言只有第 48 条一行变化；`grep -c '^- \*\*'` 断言条目数不变。
- AC11: 新用例走 `tools/intake/tests/`，用例内部 `read_bytes()` 前后比对断言零写入；跑 `python -m unittest discover -s tools/intake/tests -t .` 取退出码。
- AC12 / AC13: `grep -qF` 逐条断言关键措辞；`grep -c '^- \*\*'` 断言 debt 条目数。
- AC14: `--write` 后 `--check` 取退出码；`grep -c` 断言三处计数。
- AC15: 两条命令各取退出码并留完整输出。
- AC16: 新增 `.ai/iterations/ITER-0119/ac-sweep.py`，模式串用变量拼接避免自命中，排除面在验证报告里摊开。

## External References

- 本迭代无 `.ai/references/` 外部参考资料。
- 内部依赖：`Coder/40_Context_Management/references-schema.md §1 / §2 / §5`（本轮扩写对象）、`Coder/20_Workflow_Lifecycle/migration-schema.md §4 / §5`（迁移判定与 typed 动作缺口）、`Coder/20_Workflow_Lifecycle/mcv-deployment.md §0.1 / §2`（部署目录集）、`Coder/20_Workflow_Lifecycle/milestone-schema.md §6.1 / §6.4 / §7`（brief 输入通道）、`Coder/40_Context_Management/intake-schema.md` 与 `intake-workflow.md`（现行录入契约）、`tools/butler-upgrade/upgrade.py`（hook 树摘要口径，本轮用它取证「摘要未变」）。

## Open Questions / Risks

- **风险 · `.ai/references/` 的定位被撑大**。它今天的语义是「AI 派生的受控投影、供验收对账」，塞进一类 AI 不许碰的原件之后，「引用了 references 里的东西」这句话不再自动等于「引用了权威投影」。本轮的防线只有目录边界（`raw/` 下即原件）加散文纪律——门禁被切版顺序卡住了，所以 §1 的改写必须把两类的权威性差别写在最显眼处。
- **风险 · 一次删两份规则真源，静态扫描证不了「没人凭记忆去读」**。防线只有全仓零命中扫描，扫不到运行时行为；这是 `.ai/debt.md` 里「运行时观测缺位」那条的老问题，本轮不解决。
- **风险 · `origin/` 的引用面跨 18 份文件、含两个命令薄壳与两份人读手册**，漏一处就留下指向不存在目录的死引用。机器防线是零命中扫描加 CI，但人读文档改完读不读得通只能人眼过。
- **风险 · AC9 的「纪律要活下来」容易在执行时被简化成「一起删掉」**。`references-schema.md` 与 `test_prd_collection_contract.py` 那对逐字断言是唯一锁住措辞的机器防线，改写时必须保持它仍在锁一条真实纪律，而不是锁一句被架空的空话。
- **风险 · 已部署项目里已有的 `origin/` 内容没人搬**。升级器没有移动动作（归 R14），本轮只能停止创建与引用；别人硬盘上的目录留在原地。因为它本来就是用户自管、AI 零写入，留着不构成漂移，但要在 §5.4 与 `debt.md` 双处登记，不能靠「以后都用新地方」了事。
- **风险 · 本轮删除量大，回滚成本高**。全部改动都在 git 工作树里、未提交，最坏情况可 `git checkout` 整体退回；但 `.ai/` 下的台账与产物是本轮新写的，退回会连带丢掉迭代记录，届时需要手工重开。
