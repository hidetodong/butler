<!-- butler-artifact-template: 1.0.0 artifact=changelog -->
# ITER-0119 变更流

> 退役旧 inbox 全链（MILE-0016 R8） · closed · 2026-08-21

## ADD

- `tools/intake/tests/test_intake.py` `TestLegacyInboxIsRefusedNotRewritten` — 旧格式 `.ai/INBOX.md` 的回归防线：四个用例锁住「`add` / `list` / `handle` 三个子命令一律非零退出、错误信息含逐字表头、`.ai` 全树字节快照前后相同」。旧工具删掉之后没有降级读法，唯一能守的就是「宁可停下也不写坏」 → AC11
- `.ai/iterations/ITER-0119/ac-sweep.py` — 可重跑验收扫描，A 组 8 项查残留零命中、B 组 25 项查该活下来的还在；扫描面与排除面的理由写死在脚本注释里 → AC5, AC16
- `.ai/iterations/ITER-0119/ac1-ac4-old-chain-gone.sh` — 旧链四类实体已删、hook 树摘要未变、两个存活用例逐字节未动（重建法证明）、e2e 余下四段仍跑通 → AC1, AC2, AC3, AC4
- `.ai/iterations/ITER-0119/ac6-ac8-references-and-deploy.sh` — references 定位重写、部署两目录四处一致、brief 与 PRD 文件通道改指新位置 → AC6, AC7, AC8
- `.ai/iterations/ITER-0119/ac9-readonly-red-green.sh` — 只读纪律的红绿演示：删掉规则正文那句 → 合同测试红 → 还原 → 绿 → AC9
- `.ai/iterations/ITER-0119/ac10-ac11-invariant-and-regression.sh` `ac12-ac14-ledgers.sh` `ac15-gates.sh` `ac5-ac16-sweep.sh` — 其余 AC 的取证脚本 → AC5, AC10~AC16
- `.ai/iterations/ITER-0119/pre-p4.baseline` — P4 开工前基线：8 份待删文件的 SHA-256、3 份待改文件的 SHA-256、hook 树摘要、规则计数 → AC3, AC16
- `Coder/40_Context_Management/references-schema.md` §1 两类保真度对照表与「引用 references 不等于引用权威投影」那段 — `.ai/references/` 要容纳 AI 一个字都不许动的原件，定位必须扩 → AC6
- `Coder/20_Workflow_Lifecycle/mcv-deployment.md` §2 用户原件段 — 讲清 `.ai/references/raw/` 是用户自管的可选投放点、AI 只读、不是快速路径的必经站 → AC7, AC9
- `HUMAN_GUIDE.md` 目录树 `references/raw/` 一行与其下的辨析段 — 教用户「原件」和「派生投影」的差别 → AC8
- `.ai/debt.md` 两条新账 — 「原件只读无机器兜底」与「hook 树一改就必须跟切版绑在一起」 → AC13
- `.ai/MILESTONE.md §5.4` 五条 2026-08-21（R8 ...）登记 — 落点决定与代价、hook 门禁撤出的实测依据与恢复条件、四条迁移判定、已部署项目做不干净的部分、本轮无 TDD 配对的理由 → AC12

## EDIT

- `Coder/40_Context_Management/references-schema.md` — §1 定位段重写（对照表从「跟已退役的 `.ai/project/` 比」改成「`raw/` 原件 vs 受控投影」两类保真度）、§2 由两类资料扩为三类、§5 身份证据去掉旧 INBOX 的来源锚点绑定、§6 的 `.ai/project/` 比喻改指 `.ai/OVERVIEW.md`、§10 非回归门那条纪律换主语 → AC6, AC9
- `Coder/20_Workflow_Lifecycle/mcv-deployment.md` — §0.1 路径清单去掉 `origin/`、§2 改为「强制创建 `.ai/` 与 `deliveries/` 两类基础目录」、`INBOX.md` 的描述从旧契约的双指纹形状改成闪念口并改指 `intake-schema.md` → AC7, AC9
- `Coder/20_Workflow_Lifecycle/milestone-schema.md` — brief 的三条文件通道（§6.1 输入表、§6.4 合成步 1、§6.5 命令表）与 brief 定位段共 7 处改指 `.ai/references/raw/` → AC8
- `Coder/20_Workflow_Lifecycle/butler-upgrade.md` — 两处写集排除从 `origin/` 改为 `.ai/references/`（升级器的 rename 保护集本来就含 `references`） → AC5
- `Coder/40_Context_Management/prd-split.md` — §1 身份证据、§2 日期证据与冲突判据、§6 结尾四处摘掉旧 INBOX 回执机制；第 77 行那句指向不存在接线的「交回 inbox 工作流记录」删掉不另造 → AC5, AC6
- `Coder/40_Context_Management/intake-schema.md` `intake-workflow.md` — 摘掉与旧链并存期的过渡语（生效时点声明收成三行、递增号池的出处改为「上一代契约，已随 R8 退役」、`## 6. 与旧链的关系` 整节删除后章节号顺延） → AC1
- `Coder/README.md` — 目录树与职责段两处注销旧链；部署说明改为只建两个目录并指向 `.ai/references/raw/`；录入通道改成「对话与文件两通道」 → AC1, AC7
- `.claude/commands/butler/init.md` `plugins/butler/skills/butler-init/SKILL.md` `templates/rule-card.md` — 部署产物清单去掉 `origin/`，统一成「`.ai/` 与 `deliveries/` 两个目录」 → AC7
- `.claude/commands/butler/prd.md` — PRD 材料来源从 `origin/` 改为 `.ai/references/raw/` → AC8
- `README.md` `HUMAN_GUIDE.md` `docs/prd-migration-guide.md` — 三份人读文档的目录树与投料说明改指新位置；`HUMAN_GUIDE.md` 的树在删行后重排了画线 → AC5, AC8
- `templates/hooks/tests/test_prd_collection_contract.py` 第 56 行 — 逐字断言改指新措辞而非删除，改后仍能红（现场演过） → AC9
- `templates/hooks/tests/test_inbox_workflow.py` — 文档字符串重写；两个存活用例的函数体与断言逐字节未动（重建法证明 SHA 对上开工前基线） → AC3
- `tools/mile0009-e2e/tests/test_mile0009_e2e.py` — 摘掉链条开头调 `inbox scan` 的那一段（第 12 行常量、`origin/` 夹具、三条断言）；余下四个工具的断言逐条保留 → AC4
- `scripts/test-butler-upgrade.py` 第 398 行 — 负向夹具路径由 `origin/owner.md` 改为 `.ai/references/raw/owner.md` → AC5
- `.ai/invariants.md` 第 48 条 — 由旧契约（`SRC-NNNN` + 双指纹 + scanner + `origin/` 只读）改写为现行三层录入契约（三层名称、日期化闪念键、四态封闭枚举、唯一写盘者），带真源指针；用户原稿只读那半条纪律保留、换主语 → AC10
- `.ai/debt.md` — 「旧格式 `.ai/INBOX.md` 迁移义务没人认领」条目改写，写明旧工具已删无回退路径，并纳入「已部署项目残留 `origin/` 无人搬运」这一新事实 → AC13
- `.ai/OVERVIEW.md` — `--write` 重算：`40_Context_Management/` 计数 13 → 11，驻留工具清单去掉 `tools/inbox/` → AC14

## DELETE

- `Coder/40_Context_Management/inbox-schema.md` — 上一代收件箱数据契约（`SRC-NNNN` 稳定来源身份、observed/processed 双 SHA-256、七态处理状态机、多对多派生关系表） → AC1
- `Coder/40_Context_Management/inbox-workflow.md` — 上一代收件箱动作层（扫描 → 语义分类 → 确认 → 委托路由） → AC1
- `tools/inbox/` 整目录 — `README.md`、`__init__.py`、`inbox.py`（348 行，`status` 与 `scan` 两个子命令）、`tests/test_inbox.py` → AC2
- `templates/hooks/tests/test_inbox_contract.py` — 旧数据契约的合同测试（7 个用例，逐条断言那份契约的措辞） → AC3
- `templates/hooks/tests/test_inbox_workflow.py::test_inbox_workflow_route_and_safety_contract` — 断言旧规则文件内容的那一个用例，随该文件一起退役 → AC3
- `scripts/verify-ci.sh` 里 `python -m unittest tools.inbox.tests.test_inbox` 那一行 → AC2
