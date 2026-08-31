<!-- butler-artifact-template: 1.0.0 artifact=changelog -->
# ITER-0115 变更流

> 砍 `/butler:progress` 全链（MILE-0016 R4） · active · 2026-08-20

## ADD

- `.ai/iterations/ITER-0115/ac11-ac12-sweep.py`：本轮唯一新写的脚本，一次扫描守两组模式——A 组是 progress 链的活引用（`/butler:` + `progress`、`$butler-` + `progress`、`butler-` + `progress`、`commands/butler/` + `progress`），B 组是散文里会变假的计数表述（`Router + 13`、`13 个业务`、`13 workflow skills`、`其余十一项`）。模式串一律用变量拼接而不写字面量，脚本因此不会命中自己（TECH_PLAN Failure Path 7）。命中即非零退出并逐条打印文件与行号，不只报总数。**按 D8 有意不接 `verify-ci.sh`** → AC11、AC12
- `.ai/debt.md`：追加一条——`HUMAN_GUIDE.md`、`Coder/README.md`、`docs/codex-compatibility.md` 三处散文里的工作流个数没有机器兜底，下次增删照样会漏改；条目里写明「不加 CI 扫描是有意的」与自然消解路径（R12 的 usage 报告落地时本来就要重做工作流呈现层）。这条是登记不是实现，性质同 AC13，**在 AC 覆盖之外**（TECH_PLAN D8 已预告） → 无对应 AC
- `.ai/MILESTONE.md §5.4`：追加两条登记——①路线图给 R4 点名的「规则真源」与「rule-card 引用」两个落点在 progress 上根本不存在（registry 的 `rule_source` 指回命令文件自身，`templates/rule-card.md` 全文未提 progress），如实记为不适用而非假装完成；②Claude 侧是软链、删文件即全局生效，Codex 个人安装是拷贝、用户机器上的副本要重跑 `scripts/setup.sh` 才清得掉，该要求登记给 R15 的 `migrations/v4.0.0.md`，并确认本轮**不触发** `[regen-entrypoints]` → AC13
- `.ai/iterations/ITER-0115/` 另六份证据脚本（`ac1-ac2-entities.sh` / `ac3-ac4-registry.sh` / `ac5-router-example.sh` / `ac6-ac7-assertions.sh` / `ac8-ac9-docs.sh` / `ac10-overview.sh`）：分别断言实体消失与软链不断链、`EXPECTED_IDS` 与 `--check`、路由样例三字段、三处机器断言加 plugin.json、四份人读文档与不变量、全貌产物重算结果 → AC1–AC10

## EDIT

- `workflows/registry.json` 的 `review` 块：`routing.negative_triggers` 由 `["project status", "项目进度"]` 清空为 `[]`。两条都删——它们存在的唯一理由是把「看看现在怎么样」这类请求推离 review、推向 progress，progress 一死就都指向不存在的目标；review 的正向触发词（`review`、`代码复核`、`产物复核`、`independent review`）与「项目进度」无任何词面重叠，这层保险本来就多余（TECH_PLAN D5）→ AC2
- `workflows/router-examples.json`：`现在项目进度怎么样` 这条请求文字**保留**，期望结果改为 `expected_status: "not-butler"` / `expected_primary: null` / `expected_state_writes: false`。删样例等于把「问进度该怎么处理」这个回归一起丢了；改期望反而把 R4 的结果钉成断言——以后谁把 progress 加回来、或让别的工作流去接进度请求，这条会红（D6）→ AC5
- `scripts/sync-workflow-registry.py` 三处：`EXPECTED_IDS` 去掉 `progress` 剩 12 项；长度校验由写死的 `!= 13` 改为 `!= len(EXPECTED_IDS)`；`docs_table()` 里两个硬编码数字改成从 registry 派生（`total = len(data["workflows"])`、`implicit = sum(... allow_implicit_invocation)`），模板文案相应改为 `其余 {implicit} 项` 与 `Router + {total} 个业务 Skill`。**这是本轮最有价值的一处**——以后再增删工作流，生成投影的计数自动跟上（D4）→ AC3、AC4
- `docs/workflows.md`：由 `--write` 重算，恰好三行变化（progress 表格行消失、「其余十一项」→「其余 10 项」、分发状态表「Router + 13 个业务 Skill」→「Router + 12 个业务 Skill」），无非语义 diff → AC4
- `scripts/verify-codex-workflows.sh`：两处名单去掉 `progress`，两处数量断言 `14` → `13`，结尾文案改为 `(Router + 12 workflow skills)` → AC6
- `scripts/test-workflow-registry.py`：工作流数量断言 `13` → `12` → AC6
- `scripts/test-goal-host-wiring.py:49`：工作流数量断言 `13` → `12`。**这处是跑完整 CI 才发现的**——它写的是裸数字，本轮设计的四组扫描模式都匹配不到 → AC6
- `tools/codex-validators/test_vendored_validators.py:80`：skill 目录数断言 `14` → `13`（Router + 12 业务）。同上，也是靠 CI 报错才暴露 → AC6/AC7
- `tools/project-config/tests/test_consumers.py`：净删 14 行——`READERS` 元组 2 条、`test_commands_surface_source_conflicts_and_legacy_write_boundary` 里的路径 1 条，外加整个 `test_progress_version_does_not_come_from_project_config` 方法（其中含 2 条路径）。TECH_PLAN D9 已预告 In Scope 那句「摘 3 处」是描述性计数写少了，实际 4 个编辑点，影响面与 AC6 绑定条件不变 → AC6
- `plugins/butler/.codex-plugin/plugin.json`：`longDescription` 的枚举由 `ideation, preference, progress, convergence` 改为 `ideation, preference, convergence`，其余字段未动 → AC7
- `HUMAN_GUIDE.md`（3 处）、`Coder/README.md`（1 处）、`docs/codex-compatibility.md`（1 处）：「13 个业务」全部收敛为「12 个业务」。人读手册给具体数字有信息量，这一档不去数字化（D7 第三档），代价记在 `.ai/debt.md` → AC8
- `.ai/invariants.md` 两条（Codex skill 单一实体源、工作流元数据单一注册源）：**不是把 13 改成 12，而是把个数整个拿掉**——改为「Router 与全部业务 skill（名单以 `workflows/registry.json` 为准）」「Router 元入口与全部业务工作流」。个数正是 ITER-0114 立的写作纪律所说的「机制形状」，机制一改它就假。条目总数仍 47，正文改动恰好 2 行删 2 行增，其余条目未碰（D7 第二档）→ AC9
- `.ai/OVERVIEW.md`：由 `sync-project-overview.py --write` 重算，工作流清单少 progress 一行，另外两行是台账推进的正常跟随（active 迭代 ITER-0115、MILE-0016 含迭代数 3→4）→ AC10
- `.ai/ITERATIONS.md` / `.ai/MILESTONE.md`：`current` 置 ITER-0115，R4 路线行置 active 并绑本迭代 → 无对应 AC（台账维护）

## DELETE

- `.claude/commands/butler/progress.md`（122 行）：Claude 侧命令实体，同时也是 registry 认的规则真源。走 `git rm` 而非 `rm`，让 `git log --follow` 追得到「哪个迭代删的」（D2）→ AC1
- `plugins/butler/skills/butler-progress/`：Codex skill 实体整目录，含 `SKILL.md`（26 行）与 `agents/openai.yaml`（6 行）→ AC1
- `.agents/skills/butler-progress`：仓库发现用的相对软链。删后 `.agents/skills/` 剩 13 条（Router + 12 业务），逐条 `test -e "$link/SKILL.md"` 无断链 → AC1
- `workflows/registry.json` 的整个 progress 工作流块（43 行 diff 中的绝大部分）：元数据真源。删后 `workflows` 长度 12、无 `id == "progress"`，其余 12 块逐字段未动 → AC2
- `README.md` 能力表「想看当前 Milestone、Iteration、验收和风险 / 进度总览 / `/butler:progress` · `$butler-progress`」一行：纯删不补替代（+0/-1 的 diff）。补替代等于把砍掉的能力用文字续命，而且 `/butler:milestone status` 只报里程碑、覆盖不了验收和风险，写上去反而误导。问进度现在就是普通对话——直接读 `.ai/task-state.md` 与双台账 → AC8
- `tools/project-config/tests/test_consumers.py` 的 `test_progress_version_does_not_come_from_project_config`：整个测试方法只为 progress 而存在，随之删除；剩余用例仍覆盖 dangerous / preference / review 三个消费者 → AC6
- **覆盖面变化（不是等价替换）**：progress 曾经做的事是把 `.ai/task-state.md`、双台账、`AC_LIST.md`、`VERIFY_REPORT.md` 聚合成一份进度总览。这些文件每一份都已在冷启动读序里，转述层自己不带任何校验——聚合得对不对没有机器能判。砍掉之后没有替代品，问进度就是 AI 直接读台账回答。**这次砍是靠审计判断，不是靠使用数据**：没有「过去 90 天被调用几次」这类数据可依，装监视器是 R11/R12 的事。如果以后发现真需要，得重开一条链而不是复活旧的 → 见 AC_LIST「Open Questions / Risks」
- **未删的部分（有意保留）**：历史归档（`.ai/iterations/`、`.ai/history/`、`deliveries/`）与已发布迁移配方（`migrations/`）里对 progress 的提及一律不动——那是既成事实记录，不是活引用；用户机器上 Codex 个人安装的 `butler-progress` 拷贝本轮删不到，归 R15（已在 §5.4 登记）→ AC11 排除面 / AC13
