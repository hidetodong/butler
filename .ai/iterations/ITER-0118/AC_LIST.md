---
状态: ack-frozen
ACK 日期: 2026-08-20
---
<!-- butler-artifact-template: 1.0.0 artifact=acceptance -->
# AC_LIST — ITER-0118

## Goal

- 把 R6 定下的三层录入契约接上电：一份确定性工具承担全部文件读写与校验，`/butler:inbox add | list | handle` 三个动作可用，并用真实使用证明它跑得通。收口态必须是「工具拒绝一切非法转移、写盘不留半截态、活接线不再指向旧规则、旧链一字未动、CI 全绿」，且 dogfood 的真实程度分档如实写清——哪一段是真需求真执行，哪一段只是沙箱里的代码路径。

## In Scope

- 新建确定性工具 `tools/intake/`（Python 零依赖，与 `tools/decision-map/`、`tools/prd-status/` 同套 CLI 约定：子命令 + `--project-root` + JSON 输出），实现 `add` / `list` / `handle` 三个动作与全部契约校验。
- 重写 `.claude/commands/butler/inbox.md` 与 `plugins/butler/skills/butler-inbox/SKILL.md` 两份薄壳，改读 `intake-schema.md` 并调用新工具；同步更新 `workflows/registry.json` 的 inbox 条目并重跑投影生成。
- 新增动作层规则文件，定义三个动作的语义边界：什么归工具确定性决定、什么必须问用户、`handle` 的分流决定怎么做出来。
- 拆 `templates/hooks/tests/test_inbox_workflow.py`：描述活接线的两个用例改指新契约与新工具，描述旧规则文件内容的用例原样留到 R8。
- 让 `milestone-schema.md §7.6` 的暂缓入库指向工具，不再并行描述一套手工步骤。
- 真实 dogfood 两档：butler 仓上记一条真闪念并孵化成真草稿；沙箱项目根上把被 active 挡住的两条出口各跑一遍。
- 在 `Coder/README.md` 注册新规则文件；`.ai/MILESTONE.md §5.4` 登记本轮定序处置；`.ai/debt.md` 按实际增减。

## Out of Scope

- 不删旧链：`inbox-schema.md`、`inbox-workflow.md`、`tools/inbox/`、`test_inbox_contract.py`、`SRC-` 编号、双指纹、scanner 全部留着，退役归 R8。
- 不改目录名 `.ai/milestone-backlog/`（归 R9）。
- 不做隐式扫描：不扫 `origin/`、不扫对话历史、不做内容指纹认亲。
- 不写已部署项目的迁移配方（归 R15）。
- 不动 `.ai/MILESTONES.md` 的正式表，不改待办区的列结构。
- 不新增工作流 id，业务工作流仍是 12 个。
- 不切版、不发布、不提交。

## Acceptance Checklist

- [ ] AC1: `tools/intake/` 存在且自带测试；工具是**唯一写盘者**——`add` / `list` / `handle` 三个子命令均接受 `--project-root`，输出机器可解析的 JSON，任何契约校验不过时**整次不落盘**并以非零码退出。
- [ ] AC2: `add` 行为符合 `intake-schema.md §1`——生成 `YYYY-MM-DD-<kebab>` 形态的闪念键、同日撞名自动退让为 `-2` / `-3`、新条目状态恒为 `new` 且去向为 `—`；`.ai/INBOX.md` 不存在时按契约建出固定表头，存在时只在表尾追加、其余行逐字节不动。
- [ ] AC3: `list` 是**只读**动作——跑完前后 `.ai/INBOX.md` 与 `.ai/milestone-backlog/` 全目录哈希不变；能同时列出闪念与孵化区条目，并支持按状态、按规模筛选。
- [ ] AC4: `handle` 只接受 `intake-schema.md §1.5` 穷举的四条转移，其余组合（含终态回退、`incubated → done` 直跳）一律拒绝、退出码非零且给出可读原因；拒绝时不留任何写入痕迹。
- [ ] AC5: `handle` 转到 `incubated` 时**三处联动、两侧原子**——回写闪念行、写 `.ai/milestone-backlog/<候办键>.md`、在待办区追加索引行，三处要么全成要么全不成。有一条可重跑证据用注入失败的方式证明中断不落半截态。
- [ ] AC6: 活接线全部改指新契约——`workflows/registry.json` 的 inbox 条目 `rule_source` 指向新动作层规则，两份薄壳正文读 `intake-schema.md` 并调用 `tools/intake/`，正文不再出现 `origin/` 与 `inbox-workflow.md`；`sync-workflow-registry.py --check` 退出码 0，业务工作流仍 12 个。
- [ ] AC7: `test_inbox_workflow.py` 只改活接线相关的两个用例，且改后断言的是新契约与新工具；`test_inbox_contract.py`、`inbox-schema.md`、`inbox-workflow.md`、`tools/inbox/` 全目录与本轮开工前哈希逐一相同。
- [ ] AC8: `milestone-schema.md §7.6` 的「普通暂缓」不再并行描述手工写盘步骤，改为指向 `tools/intake/` 与新动作层规则；该文件 `git diff` 的改动行全部落在 §7.6 内。
- [ ] AC9: 新动作层规则文件在 `Coder/README.md` 的目录结构与读取顺序两处都注册；文件里明确写出三个动作各自的「工具决定 / 必须问用户」分界。
- [ ] AC10: **butler 仓真实 dogfood**——用新命令记下一条真实闪念，`list` 能看见，`handle` 把它孵化成 `.ai/milestone-backlog/` 下一份真草稿并在待办区留下索引行；收口后候办数由 9 增为 10，闪念行状态为 `incubated` 且去向指向那份草稿。全程用工具写盘，不手工编辑。
- [ ] AC11: **沙箱 dogfood**——在临时项目根上把「提升为里程碑」与「开为迭代」两条出口各跑一遍并留证；验证报告里必须把这一档与 AC10 分开写明，说清它证明的是代码路径通、不是真实使用下好用。
- [ ] AC12: `.ai/MILESTONE.md §5.4` 追加登记——①为什么复用 `inbox` 这个 id 而不新开；②为什么本轮必须动 R6 声明不碰的 `test_inbox_workflow.py`，以及边界划在哪；③执行分流两条出口在 active 状态下跑不通这个事实与沙箱折衷。
- [ ] AC13: `.ai/debt.md` 如实增减——R6 记的「两份 inbox 规则真源并存无机器兜底」在活接线改指新契约后要重新表述或标注剩余范围；新增的缺口（若有）各写明理由与自然消解路径；原有条目未被误删。
- [ ] AC14: `.ai/OVERVIEW.md` 由 `--write` 重算且 `--check` 退出码 0；规则文件计数随新增文件递增，驻留工具清单新增 `tools/intake/`，工作流清单仍 12 行。
- [ ] AC15: `bash scripts/verify-ci.sh` 退出码 0（含新工具的测试已接入 CI）；`python3 scripts/audit-project-state.py --project-root . --allow-unreleased` 退出码 0，`[UNRELEASED]` 恰 2 条。可重跑扫描断言两组均零命中——A 组查越界（活跃面不出现 `.ai/backlog/`、新工具与新规则不出现 `SRC-` 与双指纹字段名、薄壳不再出现 `origin/`），B 组查在场（旧链哈希未变、三个动作在场、README 两处注册、§7.6 已改指、候办 9 → 10）。

## Verification Method

- AC1 / AC2 / AC3 / AC4: `tools/intake/tests/` 下的单元测试逐条覆盖，CI 接入；另有端到端脚本在临时目录里跑真实 CLI 并断言退出码与 JSON 结构。
- AC5: 用注入写失败的测试（让第二处或第三处写盘抛错）断言三处全部未变，且退出码非零。
- AC6 / AC7: `sync-workflow-registry.py --check` 取退出码；`grep -c` 断言薄壳正文的禁用字样为 0；旧链哈希与 `pre-p4.baseline` 逐份比对；`git diff` 人读确认 `test_inbox_workflow.py` 只动了两个用例。
- AC8 / AC9: `git diff` 取 `milestone-schema.md` 改动行号并断言落在 §7.6 区间内；`grep -c` 断言 README 两处注册各 1。
- AC10: 收口态直接查产物——`.ai/INBOX.md` 的闪念行、草稿文件存在性、待办区行数 9 → 10；另留工具调用的完整输出作为证据。
- AC11: 在 `$TMPDIR` 下造项目根，跑完两条出口后断言里程碑台账 / 迭代台账各自出现预期行；证据保留完整输出。
- AC12 / AC13: 逐条 `grep -qF` 断言关键措辞；`grep -c '^- \*\*'` 断言 debt 条目数与原有条目首句仍在。
- AC14: `--write` 后 `--check` 取退出码；`grep -c` 断言三处计数。
- AC15: 两条命令各取退出码并留完整输出；新增 `.ai/iterations/ITER-0118/` 下一条两组扫描脚本，模式串用变量拼接避免自命中，排除面在 VERIFY_REPORT 里逐份摊开。

## External References

- 本迭代无 `.ai/references/` 外部参考资料。
- 内部依赖：`Coder/40_Context_Management/intake-schema.md`（R6 定的数据契约，本轮的实现依据）、`Coder/20_Workflow_Lifecycle/milestone-schema.md §4.5 / §7.6`、`Coder/20_Workflow_Lifecycle/iteration-schema.md §5.1`、`scripts/sync-workflow-registry.py`（注册表校验与投影规则）、`tools/decision-map/`（同类工具的 CLI 与测试约定）。

## Open Questions / Risks

- **`handle` 的分流决定由谁做出来**（P3 定）。倾向是工具只接受已定好的目标态、由命令层负责问用户；代价是 `handle` 退化成写盘器。
- **孵化区草稿正文的交接点**（P3 定）。工具产骨架、模型填内容，交接点必须定死，否则会出现「工具写了个空壳、模型以为已经写好」。
- **动作层规则是新增文件还是改写现有的**（P3 定）。新增会让 `40_Context_Management/` 再多一份；改写 `inbox-workflow.md` 则违反 Out of Scope。
- **风险 · 沙箱 dogfood 的折扣**。两条出口只能在没有 active 的环境里跑，那必然是造出来的。它证明代码路径通，证明不了真实使用下好用；这个折扣要单独成段写，不能混进「dogfood 已完成」。
- **风险 · 动 `test_inbox_workflow.py` 可能提前引爆 R8**。边界是：只改活接线相关的两个用例，旧规则文件与 `test_inbox_contract.py` 逐字节未动，有哈希为证。
- **风险 · 本轮的 dogfood 会在 butler 仓留下真实状态变化**。候办会从 9 变 10，那是一份真的、要长期存在的草稿。选题必须是真实想做的事，不能为了跑通流程编一条假需求——否则就是在自己的台账里造假条目，正是 MILE-0016 一直在修的那类问题。
