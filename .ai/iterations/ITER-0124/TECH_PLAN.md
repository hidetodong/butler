<!-- butler-artifact-template: 1.0.0 artifact=tech_plan -->
# TECH_PLAN — ITER-0124

方案状态: pass
方案审查日期: 2026-10-20
方案审查方式: user-ack

## Design Decisions

- 实验只回答「现在有没有代码在读画像之后重排选项」。没有，就固定打出排序没变，然后退役 preference 的机器入口。不新写排序器。
- evidence 的命令和记录格式不动。只加测试，锁住子命令和读者。
- loop 保持冻结。改冻结段的结论，并删掉欠债里等 R13 的那句。
- 本轮不声明 TDD。没有先失败再通过的配对。

### D1 · 实验不调用任何排序器

新建 `tools/preference-experiment/`。命令读取仓库内夹具，stdout 一份 JSON：`ranking_changed`、`order_off`、`order_on`。不含时间戳，所以同一夹具连续两次字节相同。

夹具的通识偏好是把「保持冻结」放在「删除」前面，初始顺序相反。扫描仓库 Python 时，跳过本工具和测试。找不到名为重排的函数，两份顺序都等于夹具原顺序，`ranking_changed` 为 false。找到了就退出码 2，stdout 不是成功 JSON。这样后加的排序器不能把结果改成 true。

实验不读、不写项目外的偏好目录。

### D2 · 真实结果走退役，true 只做不落地的对照

处置跟实验 JSON 走。false 时删掉 registry 里 `"id": "preference"` 那一条，以及它指向的三份文件：规则真源、Claude 命令、Codex skill。`.agents/skills/butler-preference` 软链一起删。实验目录留下。

`scripts/sync-workflow-registry.py` 的 `EXPECTED_IDS` 去掉 `preference`。`workflows/router-examples.json` 里那条偏好示例删掉。然后重跑 registry 同步，让 `docs/workflows.md` 跟上。

会因文件消失而变红的测试和活规则一起改：`tools/project-config/tests/test_consumers.py` 不再要求这三份文件存在。`Coder/README.md` 的目录和读取顺序拿掉这一节。`logic-protocol.md`、`templates/rule-card.md`、`dangerous-engine.md` 里仍教人去调用这条命令的句子，改成机器入口已退役。`templates/preference/` 骨架留下，开头写明引擎已退役，避免指向一个不存在的文件。`project-config` 的 `preference` 布尔不删。`CHANGELOG.md` 和 `migrations/` 里的历史不改。

true 分支不在本仓库落地。测试喂一份假的 true JSON，只断言「文件应留下、规则应写上触发条件」，不按它删文件。

### D3 · 个数只改三份人读文档里的现数

registry 从 12 条业务工作流变成 11 条。`HUMAN_GUIDE.md`、`Coder/README.md`、`docs/codex-compatibility.md` 里现在写着的 12，改成 11。不新做一套永久扫描器。实验测试核对这三处的数和 registry 条数一致。

### D4 · evidence 只加锁，不改行为

`evidence.py` 的子命令保持 `run`、`verify`、`check-tdd`、`archive`、`reopen`。不改 record 字段，不改 `goal.py`。`goal.py` 继续只读 `.ai/verification-evidence/`。

在 `tools/verification-evidence/test_evidence.py` 加两道锁：子命令集合恰好是这五个；除 `evidence.py`、`goal.py`、`scripts/audit-project-state.py` 和测试文件以外，没有 Python 读取证据 `record.json`。README 不得出现人读摘要或看板。

### D5 · loop 改结论，不改引擎

`convergence-loop-engine.md` 顶部改成最终处置是保持冻结。理由写明 `workflow:loop` 没有最后调用时间，不能当成已经证实没人用，所以不删除。拿掉「等 R13 再决定」这句。registry 的 `"id": "loop"` 和规则文件都留着。引擎正文不改。

`.ai/debt.md` 删掉含「随 MILE-0016 R13 对 loop 做最终处置」的那一条。

### D6 · 新工具要进名单，全貌要重算

`preference-experiment` 加入 `tools/usage/usage.py` 的 `PRODUCT_TOOLS`，否则目录对账会红。`scripts/verify-ci.sh` 加上这个工具的 pytest。`scripts/sync-project-overview.py --write` 重算全貌。

### 执行顺序

- [ ] T1 实验、夹具和测试，真实结果必须是 false → AC1 AC2
- [ ] T2 按 false 退役 preference 入口，并改会变红的引用 → AC3
- [ ] T3 三份人读文档的个数改成 11 → AC4
- [ ] T4 [P] 改 loop 冻结段，删 debt 那一条 → AC5 AC6
- [ ] T5 [P] 给 evidence 加读者和子命令测试 → AC7 AC8
- [ ] T6 登记工具、接入 CI、重算全貌，跑验证和审计 → AC9

### Plan Admission

- **AC Coverage**：AC1 与 AC2 由 T1 覆盖。AC3 由 T2。AC4 由 T3。AC5 与 AC6 由 T4。AC7 与 AC8 由 T5。AC9 由 T6。
- **Assumptions**：仓库里现在没有重排函数，所以真实实验是 false，退役会真的发生。`preference` 配置布尔不是命令入口，留下。
- **Alternatives / Trade-offs**：否掉先写排序器再证明有影响。否掉删掉 evidence 的归档搬家，收口仪式和审计还在用。否掉把 loop 删掉，C 档不能当成没人用。否掉连 `project-config` 的布尔一起删，那会变成已部署项目的迁移，归 R15。
- **Failure Modes**：扫描到重排函数时实验非零退出，不当成 true。退役后 registry 校验、消费者测试、全貌检查任何一条红了，都不算 AC3 完成。
- **Impact / Scope Challenge**：历史 changelog 和 migrations 不动。Decision Map 不动。不切版。
- **Verification Blind Spots**：这轮不证明模型在对话里会不会自己重排。外置偏好目录里已经有的旧数据，不删除，也不迁移。
- **Verdict**：pass。用户在 2026-10-20 说「方案可以」。没有必须先改的设计缺陷。

## Failure Paths

- 扫描到重排函数：退出码 2，stdout 不是成功 JSON，不进入退役。
- 实验过程不创建、不修改项目外的偏好目录。
- 假的 true JSON 只留在测试里，不删仓库文件。
- 旧证据归档继续用原来的字段校验。ITER-0123 的 `verify --source archive` 必须仍是 0。

## Test Strategy

本轮不声明 TDD cycle。`tools/preference-experiment/tests` 锁两次输出相同、夹具顺序相反、没有重排函数时结果为 false、注入重排函数时退出码 2、假 true 不落地、退役后的入口和三处个数。`tools/verification-evidence/test_evidence.py` 锁子命令和读者。`tools/goal-assurance/test_goal.py` 与 ITER-0123 归档校验保持原样通过。

## References Compliance

- N/A
