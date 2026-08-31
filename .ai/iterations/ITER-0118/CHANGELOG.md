<!-- butler-artifact-template: 1.0.0 artifact=changelog -->
# ITER-0118 变更流

> /butler:inbox 命令与工具实现（MILE-0016 R7） · closed · 2026-08-20

## ADD

- `tools/intake/intake.py` — 三层录入契约的唯一写盘者：`add` / `list` / `handle` 三个子命令、四条合法转移的校验、三条执行分流出口、跨文件「先算后写 + 失败即回滚」 → AC1, AC2, AC3, AC4, AC5
- `tools/intake/README.md` — 工具说明，第一个标题接入 `.ai/OVERVIEW.md` 的驻留工具清单；含「关于原子的实话」一节 → AC1, AC14
- `tools/intake/tests/test_intake.py` `tools/intake/tests/helpers.py` — 28 条用例，覆盖键生成与撞名、只读性、四条转移与非法组合、注入写失败的回滚、三条出口、端到端 CLI → AC1, AC2, AC3, AC4, AC5
- `Coder/40_Context_Management/intake-workflow.md` — 需求录入动作层：三个动作各自的「工具决定 / 必须问用户」分界、结构归工具正文归模型、不是事务的实话、与旧链的关系 → AC9
- `.ai/INBOX.md` — 闪念口首次建出（由工具写），含一条真实闪念「交付页渲染器只活在会话临时目录里」 → AC10
- `.ai/milestone-backlog/delivery-renderer-in-repo.md` — 真实 dogfood 产出的 `iteration` 档草稿，正文已补实 → AC10
- `scripts/verify-ci.sh` — 紧挨旧 inbox 工具那行之后新增一行跑 `tools/intake/tests` 的发现式测试（旧行保留） → AC15
- `.ai/iterations/ITER-0118/sandbox-dogfood.py` `ac-sweep.py` 与 11 份 `ac*.sh` — 沙箱 dogfood、两组扫描与逐 AC 证据脚本 → AC11, AC15

## EDIT

- `workflows/registry.json §inbox` — `rule_source` 改指 `intake-workflow.md`，双宿主 description 与语义触发词改写为新语义；id 与工作流个数不变 → AC6
- `workflows/router-examples.json` — inbox 那条示例请求原文描述的是即将不存在的行为，改成新语义说法 → AC6
- `.claude/commands/butler/inbox.md` `plugins/butler/skills/butler-inbox/SKILL.md` — 两份薄壳改读 `intake-schema.md` / `intake-workflow.md`、改调 `tools/intake/`，`argument-hint` 改为 `add | list | handle` → AC6
- `docs/workflows.md` `plugins/butler/skills/butler-inbox/agents/openai.yaml` — 由 `sync-workflow-registry.py --write` 重生成的投影 → AC6
- `templates/hooks/tests/test_inbox_workflow.py` — 只改活接线那两个用例（注册断言改指新动作层、薄壳断言改指新契约与新工具并删掉旧来源目录那条）；描述旧规则文件内容的用例原样保留，文件头加分工说明 → AC7
- `Coder/40_Context_Management/intake-schema.md §生效时点声明` — 由「R7 前零写入、分歧以旧契约为准」改为「自 R7 起生效、分歧以本文件为准」 → AC6
- `Coder/20_Workflow_Lifecycle/milestone-schema.md §7.6` — 「普通暂缓」原第 3、4 步（手工写草稿 + 手工追加索引行）合并为一步调工具，写明先 `add` 再 `handle` 两次调用；改动全落 §7.6 内 → AC8
- `Coder/README.md` — 目录结构与读取顺序两处注册 `intake-workflow.md`；`intake-schema.md` 那条指针同步改为「自 R7 起生效」 → AC9
- `.ai/MILESTONES.md §待办区` — 由工具追加 `delivery-renderer-in-repo` 索引行，候办 9 → 10 → AC10
- `.ai/MILESTONE.md §5.4` — 追加 4 条 R7 定序登记（复用 id / 必须动那份测试的边界 / 两条出口跑不通与沙箱折衷 / §7.6 改成两次调用） → AC12
- `.ai/debt.md` — 「两份 inbox 真源」按 R7 后剩余范围重新表述；新增「回滚本身失败仍会留半截态」与「六条动作路径只有两条被真实用过」两条；12 → 14 → AC13
- `.ai/OVERVIEW.md` — 由 `sync-project-overview.py --write` 重算：驻留工具清单新增 `tools/intake/`，`40_Context_Management/` 规则文件数 12 → 13 → AC14
- `.ai/TECH_PLAN.md §Test Strategy` — P5 补一张机器可读的 `butler-tdd-cycles` 声明表，与原散文声明同义 → AC1

## DELETE

- 无（旧链 `inbox-schema.md` / `inbox-workflow.md` / `test_inbox_contract.py` / `tools/inbox/` 全目录逐字节未动，退役归 MILE-0016 R8）
