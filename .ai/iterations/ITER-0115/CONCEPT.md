<!-- butler-artifact-template: 1.0.0 artifact=concept -->
# CONCEPT — ITER-0115 · 砍 `/butler:progress` 全链（MILE-0016 R4）

## Current Understanding

- **要解决的问题**：`/butler:progress` 是一个只读聚合器，把 `.ai/` 下的台账拼成一页九节的进度报告。MILE-0016 的审计把它判为该砍——它读的每一份文件（`task-state.md`、`MILESTONES.md`、`AC_LIST.md`、`TECH_PLAN.md`、`VERIFY_REPORT.md`、`01_CHANGELOG.md`）本来就在冷启动读序里，AI 直接读原文比读一层转述更准；而这层转述自己不带任何机器校验，报告写错了没人知道。R4 就是把这条链整个拿掉。

- **这一条没有独立的规则真源，删命令即等于删真源**。路线图写的是「命令、skill、规则真源、registry 条目、`docs/workflows.md` 与 rule-card 引用」六项，实测只有四项存在：

  | 路线图点名 | 实际 | 处置 |
  |---|---|---|
  | 命令 | `.claude/commands/butler/progress.md`（5.3K） | 删 |
  | skill | `plugins/butler/skills/butler-progress/` + `.agents/skills/` 软链 | 删 |
  | 规则真源 | **不存在**。registry 里 progress 的 `rule_source` 指回命令文件自身，`Coder/` 下无对应规则 | 随命令一起消失 |
  | registry 条目 | `workflows/registry.json` 一个 workflow 块 | 删 |
  | `docs/workflows.md` | 是 `sync-workflow-registry.py --write` 的生成投影 | 重算，不手改 |
  | rule-card 引用 | **不存在**。`templates/rule-card.md` 全文未提 progress | 不适用，P5 如实记 |

- **真正的工作量不在删，在改齐被硬编码的计数**。「Router + 13 个业务工作流」这个数字散在九个地方，删一个工作流就得同批改：`HUMAN_GUIDE.md`（3 处）、`Coder/README.md`、`docs/codex-compatibility.md`、`.ai/invariants.md`（2 条不变量）、`scripts/verify-codex-workflows.sh`（2 处名单 + 2 处数量断言 + 结尾文案）、`scripts/sync-workflow-registry.py`（`EXPECTED_IDS` + 生成模板里的「其余十一项」）、`scripts/test-workflow-registry.py`（数量断言 13）、`plugins/butler/.codex-plugin/plugin.json` 的 longDescription、`tools/project-config/tests/test_consumers.py`（3 处消费者路径）。漏任何一处，CI 当场红——这一点反过来是好事：**计数断言本身就是「没删干净」的机器探测器**。

- **两个隐蔽的残留点，扫的时候容易漏**。一是 `workflows/router-examples.json` 里那条 `现在项目进度怎么样 → progress` 的路由样例，`sync-workflow-registry.py` 强制要求样例集覆盖每个工作流 ID，样例不动就通不过校验。二是 `review` 工作流的 `negative_triggers` 里有一条 `项目进度`——它当初存在的唯一理由是把「问进度」推离 review、推向 progress，progress 一死这条就成了指向不存在工作流的悬空规则。

- **已部署侧不归本迭代**。Claude 命令是软链到本仓目录，删文件即全局生效；但 Codex 个人安装是**拷贝**（`scripts/install-codex-plugin.sh`），用户机器上那份 `butler-progress` skill 不会自己消失，得重跑安装。这属于已部署项目的一次性交代，按 R2/R3 的先例登记给 R15 的 `migrations/v4.0.0.md`，本轮只登记不执行。

## Scope

- 删 `.claude/commands/butler/progress.md`。
- 删 `plugins/butler/skills/butler-progress/` 整个目录与 `.agents/skills/butler-progress` 软链。
- 从 `workflows/registry.json` 摘掉 progress 工作流块；同步清掉 `review` 的 `项目进度` 负向触发词。
- 改 `workflows/router-examples.json` 那条样例：请求文字保留，期望结果从「路由到 progress」改成「不是 Butler 工作流」，用它反证链路真的死了。
- 改 `scripts/sync-workflow-registry.py` 的 `EXPECTED_IDS` 与生成模板文案，再用 `--write` 重算 `docs/workflows.md`。
- 改三处机器断言：`scripts/verify-codex-workflows.sh`（名单 / 14→13 / 文案）、`scripts/test-workflow-registry.py`（13→12）、`tools/project-config/tests/test_consumers.py`（摘 3 处路径）。
- 改人读引用：`README.md` 能力表、`HUMAN_GUIDE.md` 3 处、`Coder/README.md`、`docs/codex-compatibility.md`、`plugins/butler/.codex-plugin/plugin.json`。
- 改 `.ai/invariants.md` 两条含「13 个业务 skill」的不变量。
- 用 `scripts/sync-project-overview.py --write` 重算 `.ai/OVERVIEW.md`。
- 在 `.ai/MILESTONE.md` 范围演进记录登记两件事：路线图点名的「规则真源 / rule-card 引用」两项不存在；Codex 个人安装副本的清理归 R15。
- 跑完整 CI 与状态审计，并用一次全仓 grep 证明活引用清零。

**明确不做**：
- 不新增替代命令，不把进度聚合能力搬进别的工作流。问进度就直接读 `.ai/task-state.md` 与双台账。
- 不动 `/butler:loop` 的降级与候办清理（R5）。
- 不改 `Coder/00_System_Prompt/workflow-router.md` 的路由算法，只删被路由的目标。
- 不动已部署项目的升级路径与 `migrations/v4.0.0.md`（R15）。
- 不清理历史归档（`.ai/iterations/`、`.ai/history/`、`deliveries/`）里对 progress 的提及——那是既成事实的记录，不是活引用。
- 不切版、不发布。

## Open Questions / Risks

- **待定 · `README.md` 能力表那一行怎么处置**。「想看当前 Milestone、Iteration、验收和风险 → `/butler:progress`」删掉后，是留空还是补一句替代（比如「直接读 `.ai/task-state.md`」或指向 `/butler:milestone status`）。倾向直接删、不补替代——补替代等于把砍掉的能力用文字续命，而且 `/butler:milestone status` 只报里程碑，覆盖不了验收和风险，写上去反而误导。P2 定。
- **待定 · 路由样例改成哪个状态**。四个合法状态里，`not-butler`（不是 Butler 工作流请求）和 `ambiguous`（需要澄清）都说得通。倾向 `not-butler`：问进度现在就是普通对话，AI 读台账直接答，不需要走任何工作流。P2 定。
- **风险 · 计数断言不覆盖纯人读文档**。CI 能抓住 `verify-codex-workflows.sh` 和两个测试里的数字，但 `HUMAN_GUIDE.md`、`Coder/README.md`、`docs/codex-compatibility.md` 里的「13 个业务 skills」是纯散文，改漏了不会红。P3 要给一条机器可跑的兜底检查（最简单的形式是一条 grep 断言进证据），不能只靠肉眼扫。
