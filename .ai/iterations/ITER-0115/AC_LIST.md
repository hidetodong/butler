---
状态: ack-frozen
ACK 日期: 2026-08-20
---
<!-- butler-artifact-template: 1.0.0 artifact=acceptance -->
# AC_LIST — ITER-0115

## Goal

- 把 `/butler:progress` 这条链从 Butler 里整个拿掉：命令、Codex skill、注册表条目、路由样例、生成文档、人读引用与硬编码计数全部收敛，业务工作流从 13 变 12，全仓不剩活引用。同时把这次删除暴露出的两条纪律问题一并修掉——不变量里不该复述「13 个」这种会随机制变化的数字，纯散文里的计数没有机器兜底。

## In Scope

- 删 `.claude/commands/butler/progress.md`、`plugins/butler/skills/butler-progress/` 与 `.agents/skills/butler-progress` 软链。
- 从 `workflows/registry.json` 摘掉 progress 工作流块，并清掉 `review` 的 `项目进度` 负向触发词（它唯一的作用是把请求推向 progress）。
- 改 `workflows/router-examples.json`：`现在项目进度怎么样` 这条请求文字保留，期望结果改为 `not-butler`（不是 Butler 工作流，AI 直接读台账回答）。
- 改 `scripts/sync-workflow-registry.py` 的 `EXPECTED_IDS` 与生成模板文案，用 `--write` 重算 `docs/workflows.md`。
- 改三处机器断言：`scripts/verify-codex-workflows.sh`（2 处名单 + 2 处数量 + 结尾文案）、`scripts/test-workflow-registry.py`（工作流数量 13→12）、`tools/project-config/tests/test_consumers.py`（摘 3 处 progress 路径）。
- 改 `plugins/butler/.codex-plugin/plugin.json` 的 longDescription。
- 改人读引用：`README.md` 能力表删「进度总览」一行且不补替代、`HUMAN_GUIDE.md` 3 处计数、`Coder/README.md`、`docs/codex-compatibility.md`。
- 改 `.ai/invariants.md` 两条含「13 个业务 skill」的不变量——不是把 13 改成 12，而是按 ITER-0114 立的写作纪律把具体数字整个拿掉、改为指向 `workflows/registry.json`。
- 新增一条可重跑的扫描断言，同时守两件事：progress 活引用零命中、散文里的「Router + 13 个业务」类表述零命中。
- 用 `scripts/sync-project-overview.py --write` 重算 `.ai/OVERVIEW.md`。
- 在 `.ai/MILESTONE.md §5.4` 登记两条事实：路线图点名的「规则真源」与「rule-card 引用」在本命令上不存在；Codex 个人安装副本的清理归 R15。

## Out of Scope

- 不新增替代命令，不把进度聚合搬进别的工作流；问进度就直接读 `.ai/task-state.md` 与双台账。
- 不动 `/butler:loop` 的降级与候办清理（R5）。
- 不改 `Coder/00_System_Prompt/workflow-router.md` 的路由算法，只删被路由的目标。
- 不动已部署项目的升级路径与 `migrations/v4.0.0.md`（R15）；用户机器上 Codex 个人安装的 `butler-progress` 副本本轮不清。
- 不清理历史归档（`.ai/iterations/`、`.ai/history/`、`deliveries/`、`migrations/`）里对 progress 的提及——那是既成事实记录，不是活引用。
- 不回头改 `.ai/invariants.md` 另外那些复述了机制形状的条目，本轮只改因删除而变假的两条。
- 不切版、不发布。

## Acceptance Checklist

- [ ] AC1: 三个实体消失——`.claude/commands/butler/progress.md`、`plugins/butler/skills/butler-progress/`、`.agents/skills/butler-progress` 均不存在；`.agents/skills/` 剩 13 个软链且每条都指向存在的 `SKILL.md`，无断链。
- [ ] AC2: `workflows/registry.json` 的 `workflows` 长度为 12 且无 `id == "progress"`；`review` 的 `routing.negative_triggers` 不再含 `项目进度`；除这两处外，其余 12 个工作流块内容与删除前逐字段相同（`git diff` 可核）。
- [ ] AC3: `scripts/sync-workflow-registry.py` 的 `EXPECTED_IDS` 为 12 项且不含 `progress`；`--check` 模式退出码 0（注册表与全部投影对账通过）。
- [ ] AC4: `docs/workflows.md` 由 `--write` 重算——工作流表 12 行且无 progress 行，安全段文案从「其余十一项」改为「其余十项」，分发状态表的 `.agents/skills/` 一行不再写「13 个业务 Skill」；页首「请勿手改」声明保留。
- [ ] AC5: `workflows/router-examples.json` 中 `现在项目进度怎么样` 这条请求仍在，`expected_status` 为 `not-butler`、`expected_primary` 为 `null`、`expected_state_writes` 为 `false`；样例集仍覆盖全部 12 个工作流 ID（覆盖校验通过，不因删样例而漏 ID）。
- [ ] AC6: 三处机器断言改齐并各自跑绿——`bash scripts/verify-codex-workflows.sh` 退出码 0 且结尾文案报 12 个 workflow skills；`scripts/test-workflow-registry.py` 的数量断言为 12 且全部用例通过；`tools/project-config/tests` 全绿且不再含任何 progress 路径。
- [ ] AC7: `plugins/butler/.codex-plugin/plugin.json` 的 longDescription 不含 `progress`，其余字段未动；固定版 plugin validator 与全部 skill validator 通过。
- [ ] AC8: 四份人读文档改齐——`README.md` 能力表不再有 `/butler:progress` 行且未补任何替代说法；`HUMAN_GUIDE.md` 3 处、`Coder/README.md` 1 处、`docs/codex-compatibility.md` 1 处的「13 个业务」全部收敛到 12。
- [ ] AC9: `.ai/invariants.md` 那两条不变量（Codex skill 单一实体源、工作流元数据单一注册源）不再出现任何工作流个数，改为指向 `workflows/registry.json` 与 `plugins/butler/skills/`；条目总数不变（47 条）、除这两条外正文未改；无真源指针条目数仍不超过棘轮基线 16。
- [ ] AC10: `.ai/OVERVIEW.md` 由 `sync-project-overview.py --write` 重算，工作流清单 12 行且无 progress；`--check` 退出码 0，体量仍在 12000 字节上限内。
- [ ] AC11: 活引用零命中——全仓活跃文件中检索 `/butler:progress`、`$butler-progress`、`butler-progress`、`commands/butler/progress.md` 四个模式，命中数为 0。扫描面排除历史归档（`.ai/iterations/`、`.ai/history/`、`deliveries/`）、已发布迁移配方（`migrations/`）、本迭代工作区产物与第三方依赖（`.venv/`、`.git/`）。
- [ ] AC12: 散文计数有机器兜底——同一扫描脚本另检索「Router + 13」「13 个业务」「13 workflow skills」「其余十一项」四类表述，在同一排除面下命中数为 0；脚本可重跑、诊断指名文件与行号，不只报总数。
- [ ] AC13: `.ai/MILESTONE.md §5.4` 追加两条登记——①路线图点名的「规则真源」与「rule-card 引用」在 progress 上不存在（registry 的 `rule_source` 指回命令自身、`templates/rule-card.md` 全文未提），本轮如实记为不适用而非假装完成；②Claude 侧靠软链删即生效，Codex 个人安装是拷贝、用户机器上的副本需重跑安装才清掉，归 R15。
- [ ] AC14: `bash scripts/verify-ci.sh` 退出码 0；`python3 scripts/audit-project-state.py --project-root . --allow-unreleased` 退出码 0，非 OK 行只剩 `UNRELEASED` 亮牌与历史诊断 `INFO`。

## Verification Method

- AC1: `test -e` 三连断言不存在；`find .agents/skills -maxdepth 1 -type l | wc -l` 等于 13，逐条 `test -e "$link/SKILL.md"`。
- AC2: `python3 -c` 读 JSON 断言长度与 ID 集合；`git diff workflows/registry.json` 人读确认改动只有两处。
- AC3: 读 `EXPECTED_IDS` 常量断言集合；跑 `sync-workflow-registry.py --check` 取退出码。
- AC4: `--write` 后 `git diff docs/workflows.md`；`grep -c` 断言表格行数与三处文案。
- AC5: `python3 -c` 读 JSON 断言那条样例的三个字段；`sync-workflow-registry.py --check` 的覆盖校验退出码 0。
- AC6: 三条命令各自取退出码；`grep -rn progress tools/project-config/tests/` 零命中。
- AC7: `python3 -c` 读 JSON 断言 longDescription 不含 progress；`verify-codex-workflows.sh` 内已跑固定版 validator，取其退出码。
- AC8: 逐文件 `grep -c` 断言旧表述零命中、新表述存在；`git diff` 人读确认 README 那行是删除而非替换。
- AC9: `grep -c '^- \*\*'` 断言仍 47；`git diff .ai/invariants.md` 人读确认只改两条；`sync-project-overview.py --check` 内置的棘轮校验退出码 0。
- AC10: `--write` 后 `--check` 取退出码；`wc -c` 实测；`grep -c progress .ai/OVERVIEW.md` 为 0。
- AC11 / AC12: 新增 `scripts/`（或迭代证据目录下）一条扫描脚本，两组模式各自跑 `grep -rn` 并在有命中时非零退出、打印文件与行号；命令与输出整份进 evidence。
- AC13: 人读 `.ai/MILESTONE.md §5.4` 末两条。
- AC14: 两条命令取退出码并留存完整输出。

## External References

- N/A（本迭代无 `.ai/references/` 外部参考资料）。

## Open Questions / Risks

- **风险 · 这次砍是靠审计判断，不是靠使用数据**。装监视器是 R11/R12 的事，本轮没有「过去 90 天 progress 被调用几次」这种确定性数据可依，依据是「它读的每份文件都在冷启动读序里、转述层自己不带校验」。这个判断可能错——如果以后发现真需要，得重开一条链而不是复活旧的。交付总结要如实写明依据性质，不能写成「数据证明没人用」。
- **风险 · 已部署侧会有一段不一致**。Claude 命令删了立刻全局生效，Codex 个人安装的拷贝还在，用户在 Codex 里仍能触发 `$butler-progress`，而它读的规则文件已经不存在。这段窗口有意接受，归 R15 一次性交代；本轮只登记，不做兼容降级。
- **已定 · README 不补替代说法**。补替代等于把砍掉的能力用文字续命，而且 `/butler:milestone status` 只报里程碑，覆盖不了验收和风险，写上去反而误导。
- **已定 · 路由样例改 `not-butler` 而非 `ambiguous`**。问进度现在就是普通对话——AI 读台账直接答，不需要澄清也不需要走任何工作流。
