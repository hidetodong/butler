<!-- butler-artifact-template: 1.0.0 artifact=tech_plan -->
# TECH_PLAN — ITER-0115

方案状态: pass
方案审查日期: 2026-08-20
方案审查方式: user-ack

## Design Decisions

**D1 · 改动边界一次划清：删五处、改两处**

progress 这条链一共七个落点，其中五个是删、两个是**改而不删**——后两个删了反而丢东西：

| 落点 | 动作 | 为什么 |
|---|---|---|
| `.claude/commands/butler/progress.md` | 删 | 命令实体，同时也是 registry 认的规则真源 |
| `plugins/butler/skills/butler-progress/` | 删 | Codex skill 实体（含 `SKILL.md` 与 `agents/openai.yaml`） |
| `.agents/skills/butler-progress` | 删 | 仓库发现用的相对软链 |
| `workflows/registry.json` 的 progress 块 | 删 | 元数据真源 |
| `test_progress_version_does_not_come_from_project_config` | 删 | 整个测试方法只为 progress 而存在 |
| `review` 的 `项目进度` 负向触发词 | **改**（删这一条触发词，保留其余） | 见 D4 |
| `router-examples.json` 的那条样例 | **改**（保留请求、改期望） | 见 D5 |

**D2 · 一律 `git rm`，不用 `rm`**

删除本身是要审计的事实。`git rm` 让 `git log --follow` 能追到「这个命令什么时候、在哪个迭代被删的」；`rm` + `git add -A` 也能记录，但血缘弱。软链同样走 `git rm`——`rm -r` 对软链只删链不跟随目标，但显式用 `git rm` 少一层判断。

**D3 · 生成投影一律重算，人不碰**

两份生成产物各跑一次写模式，不手改一个字：

- `python3 scripts/sync-workflow-registry.py --write` → 重算 `docs/workflows.md`
- `python3 scripts/sync-project-overview.py --write` → 重算 `.ai/OVERVIEW.md`

顺序上**先摘 registry 条目、再删实体文件**。反过来会撞坑：`build_projections()` 遍历 registry 里每个工作流去改写命令与 skill 的 frontmatter，registry 还留着 progress 而文件已经没了，生成器会直接抛路径错。

**D4 · 把生成模板里两个硬编码数字改成从 registry 派生（治本，本轮最有价值的一处）**

`sync-workflow-registry.py` 的文档模板里写死了两个数：安全段的「其余十一项」、分发状态表的「Router + 13 个业务 Skill」。它们本来就该是算出来的——registry 里有 `workflows` 长度、有 `HIGH_RISK` 集合。改成 f-string 派生后，以后再增删任何工作流，`docs/workflows.md` 的计数自动跟上，不用人记得改。

中文数字「十一」换成阿拉伯数字（`其余 10 项`）——中文数字要额外写个转换函数，不值得，而且表格里本来就是阿拉伯数字。

**D5 · `review` 的负向触发词删掉是安全的**

`项目进度` 这条负向触发词存在的唯一理由，是当年 progress 和 review 都可能接「看看现在怎么样」这类请求，需要把它推离 review。progress 一死，这条就指向一个不存在的工作流。删掉之后 review 会不会反过来抢这类请求？不会——review 的正向触发词是 `review`、`代码复核`、`产物复核`、`independent review`，跟「项目进度」没有任何词面重叠，负向触发词在这里本来就是多余的保险。

**D6 · 路由样例改写而不是删除**

`router-examples.json` 是 router 行为的回归 fixture。删掉那条样例，等于把「问进度这类请求该怎么处理」这个回归一起丢了；改成 `not-butler` 则相反——它把 R4 的结果钉成了一条断言：以后谁把 progress 加回来或者让别的工作流去接进度请求，这条样例会红。

**D7 · 计数处置分三档，不搞一刀切**

「13 个业务工作流」这个数散在三类载体里，性质不同，处置也该不同：

| 载体 | 处置 | 理由 |
|---|---|---|
| `docs/workflows.md`（生成投影，2 处） | D4 改成派生，自动跟随 | 生成产物就该零硬编码 |
| `.ai/invariants.md`（不变量，2 条） | **去数字化**，改为指向 `workflows/registry.json` 与 `plugins/butler/skills/` | ITER-0114 刚立的纪律：不变量只写决策与理由、不复述机制形状。个数正是「机制形状」，机制一改它就假 |
| `HUMAN_GUIDE.md`（3 处）、`Coder/README.md`、`docs/codex-compatibility.md` | 改成 12 | 人读手册给具体数字有信息量，去数字化反而变虚。但它下次还会假，所以配 D8 |

**D8 · 散文计数的缺口记一条 debt，不进 CI**

D7 第三档留了个真缺口：这三份人读文档里的数字没有任何机器兜底，下次增删工作流照样会漏改。往 CI 里塞一条扫描能堵住，但那正是 MILE-0016 在砍的那类积累——为一次性清理留一条永久检查。所以：本轮的扫描脚本落在迭代证据目录（`.ai/iterations/ITER-0115/ac11-ac12-sweep.sh`），由 `evidence.py run` 捕获，**不接 `verify-ci.sh`**；同时往 `.ai/debt.md` 追加一条，写明这个缺口与它的自然消解路径（R12 的 usage 报告落地后，工作流清单本来就要重做一遍呈现层）。

追加这一行 debt 严格说在 AC 之外——它是登记不是实现，性质与 AC13 的 §5.4 登记相同。P5 会如实标注这是 AC 覆盖之外的附带登记。

**D9 · 一处 AC 措辞与实测不符，先在此说明**

AC In Scope 写的是 `tools/project-config/tests/test_consumers.py`「摘 3 处 progress 路径」。实测编辑点是 4 个：`READERS` 元组 2 条、`test_commands_surface_source_conflicts_and_legacy_write_boundary` 的路径元组 1 条、外加整个 `test_progress_version_does_not_come_from_project_config` 方法（其中还含 2 条路径）。影响面没变（同一个文件、同一个意图），AC6 的绑定条件写的是「不再含任何 progress 路径」也仍然精确——变的只是我在 In Scope 里那句描述性计数写少了。按 `iteration-schema.md §5.3`，这不构成需求变化，故不退回 draft 重 ACK；但记在这里，P5 如实回填。

**执行顺序**：
- [ ] T1 摘 `workflows/registry.json` 的 progress 块 + 删 `review` 的 `项目进度` 负向触发词 → AC2
- [ ] T2 改 `router-examples.json` 那条样例为 `not-butler` → AC5
- [ ] T3 `git rm` 三个实体（命令 / skill 目录 / 软链）→ AC1
- [ ] T4 改 `sync-workflow-registry.py`：`EXPECTED_IDS` 去 progress + D4 两处数字改派生；跑 `--write` → AC3、AC4
- [ ] T5 改三处机器断言 + `plugin.json` longDescription → AC6、AC7
- [ ] T6 改四份人读文档 + `.ai/invariants.md` 两条去数字化 → AC8、AC9
- [ ] T7 跑 `sync-project-overview.py --write` 重算 `.ai/OVERVIEW.md` → AC10
- [ ] T8 写扫描脚本跑两组模式；追加 `.ai/debt.md` 一条；`.ai/MILESTONE.md §5.4` 登记两条 → AC11、AC12、AC13
- [ ] T9 完整 CI + 状态审计 + 全量 evidence 捕获 → AC14

## Failure Paths

1. **中间态必然红，别把它当结论**。T1 删了 registry 条目但 T4 还没改 `EXPECTED_IDS`，`--check` 就会报 ID 集合对不上；T3 删了实体但 T5 还没改数量断言，`verify-codex-workflows.sh` 就会报 14 != 13。对策：T1–T8 一次做完再跑 CI，中途的红是预期的，不作为判断依据；只有 T9 的结果算数。
2. **软链残留不会被生成器抓到**。`build_projections()` 只保证「registry 里有的都投影出来」，不检查「投影里有没有多余的」——删了 registry 条目却忘删 `.agents/skills/butler-progress`，`sync-workflow-registry.py --check` 照样绿。真正兜住这一漏的是 `verify-codex-workflows.sh` 里那两条数量断言（plugin skills 目录数、软链数）。所以 T5 必须把 14 改成 13，改错方向（比如只改一处）会让这个漏洞继续存在。
3. **`test_consumers.py` 删一半留一半**。那个 progress 专属测试方法删掉后，要确认剩下的用例仍然覆盖 dangerous / preference / review 三个消费者，不能因为共用元组而误删。对策：改完先单跑 `pytest tools/project-config/tests -q`，用例数应从原有减少 1 个方法而不是整类消失。
4. **`--write` 产生非语义 diff**。D4 改模板文案后，`docs/workflows.md` 应该只有三行变化（progress 那行消失、「其余十一项」变「其余 10 项」、分发表那行数字变）。若 diff 里出现别的行，说明 f-string 改动碰到了不该碰的地方，停下核对再继续。
5. **`invariants.md` 去数字化改过头**。这两条不变量的正文里除了个数还有别的机制描述（`.agents/skills/` 必须保持相对软链、registry 维护哪些字段）。本轮只拿掉个数，不顺手重写整条——重写会让 `git diff` 变大、也超出 AC9「除这两条外正文未改」的口径。改完用 `git diff` 逐字确认。
6. **`.ai/OVERVIEW.md` 的其他节被连带改动**。工作流清单少一行是预期的，但如果生成结果里规则目录、驻留工具那几节也变了，说明期间有别的东西动过（比如 T4 改脚本时误碰了 `Coder/README.md`）。对策：`git diff .ai/OVERVIEW.md` 应只有工作流表少一行。
7. **扫描脚本自己命中自己**。脚本正文里写着 `butler-progress` 这些模式串，跑全仓 `grep` 时会命中自身，造成假红。对策：排除面显式包含脚本自身路径，或用变量拼接模式串避免字面量出现；两种都行，选后者更干净。
8. **已部署的 Codex 侧继续能触发**。用户机器上 `~/.codex` 里的 plugin 是拷贝，本轮删不到；在 Codex 里 `$butler-progress` 仍会被发现，而它 SKILL.md 里指的规则文件已经不存在。这是有意接受的窗口，归 R15，本轮只在 §5.4 登记，**不做兼容降级、不留 deprecated 桩**。

## Test Strategy

本迭代不新增单元测试——改的是既有断言的期望值（13→12、14→13、名单去一项），新写测试等于给「我改对了没」再套一层自己写的判断。真正的验证力来自三处**既有**机器断言：`sync-workflow-registry.py --check`（registry 与全部投影对账）、`verify-codex-workflows.sh`（实体数量 + 官方固定版 validator）、`test-workflow-registry.py` 与 `test_consumers.py`（数量与消费者契约）。

**新增的唯一脚本**是 AC11/AC12 的扫描器 `.ai/iterations/ITER-0115/ac11-ac12-sweep.sh`：两组模式各跑一遍 `grep -rn`，命中即非零退出并打印文件与行号；排除面按 AC11 写死（`.ai/iterations/`、`.ai/history/`、`deliveries/`、`migrations/`、`.venv/`、`.git/` 与本迭代工作区产物）。它不进 CI（D8）。

**证据捕获**（`tools/verification-evidence/evidence.py run`）：

- `ac1-ac2-entities` (AC1,AC2)：三个实体不存在 + 软链数 13 且不断链 + registry 长度 12 与 review 触发词断言
- `ac3-ac4-registry` (AC3,AC4)：`EXPECTED_IDS` 断言 + `--check` 退出码 + `docs/workflows.md` 三处文案与行数
- `ac5-router-example` (AC5)：样例三字段断言 + 覆盖校验退出码
- `ac6-ac7-assertions` (AC6,AC7)：`verify-codex-workflows.sh` + `test-workflow-registry.py` + `pytest tools/project-config/tests` + plugin.json 断言，四条各自退出码
- `ac8-ac9-docs` (AC8,AC9)：四份人读文档旧表述零命中 + `invariants.md` 47 条不变、两条无个数
- `ac10-overview` (AC10)：`sync-project-overview.py --check` 退出码 + 体量 + 工作流表行数
- `ac11-ac12-sweep` (AC11,AC12)：扫描脚本本体
- `ac13-ac14-ci-audit` (AC13,AC14)：`verify-ci.sh` + `audit-project-state.py --allow-unreleased` + §5.4 登记在场的弱档代理

**置信档**：AC1–AC7、AC10–AC12、AC14 为 auto·可靠（确定性断言，且大部分是既有 CI 断言而非本轮自造）；AC8、AC9、AC13 为 auto·弱——机器只查得出「旧表述没了、新表述在」，判不了改后的话写得对不对，那部分靠人读 `git diff`。无 human·待人 档。

## References Compliance

- 本迭代无 `.ai/references/` 外部参考资料，无外部引用合规项。
- **分层不破**：本轮不动 SOP Core（00/20/30/40）任何规则文件的算法，只动仓根的入口实体、注册表、生成投影与人读文档；`Coder/README.md` 的改动仅是一处计数，不改结构与职责分工。
- **产物链不破**：每条设计决策都能追到 AC；唯二 AC 之外的动作是 D8 的一行 debt 追加（登记性质）与 D9 的措辞澄清（不改影响面），两者都已在正文写明，P5 如实回填。
- **模板 SSOT 不破**：`templates/rule-card.md` 全文未提 progress，本轮不动它，也不动两份入口模板。故**本轮不触发 `[regen-entrypoints]`**——按 `migration-schema.md §5` 的判据，改动没有流进目标项目的 `CLAUDE.md` / `AGENTS.md`。
- **升级处置登记**：Claude 侧全局命令是软链到本仓目录（`scripts/setup.sh` 装的），删文件即全局生效，不需要迁移动作；Codex 侧个人 plugin 是拷贝，需要 `[global-install]`（重跑 `scripts/setup.sh`）才能清掉用户机器上的 `butler-progress` 副本。这条要求登记给 R15 的 `migrations/v4.0.0.md`，本轮只在 `.ai/MILESTONE.md §5.4` 记明，不单独开配方。
