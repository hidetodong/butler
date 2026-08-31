<!-- butler-artifact-template: 1.0.0 artifact=tech_plan -->
# TECH_PLAN — ITER-0116

方案状态: pass
方案审查日期: 2026-08-20
方案审查方式: 用户审阅（P3 方案与 §5.3 修订后的验收标准一并 ACK）

## Design Decisions

**D1 · 撤候办用「两侧删净」表达，不引入 `候办状态` 第三态**

`milestone-schema.md` 只定义了 `候办状态: deferred` 一个取值，`audit-project-state.py` 的 `backlog.<slug>.markers` 也按这一个值硬断言。加一个 `withdrawn` 要同时改规则、审计断言与测试，换来的是一份没人会再读的墓碑文件。

选「删文件 + 删索引行」，理由与撤回本身自洽：撤回的意思是这个方向现在不成立，不是它变成了另一种状态。理由不会丢——它落在 `.ai/MILESTONE.md §5.4`、本迭代变更流与交付总结三处，都是本来就要写的地方。

这一处有**现成的机器兜底**，不用自己造：`audit-project-state.py` 的 `milestones.backlog_set` 断言「索引行集合 == 实际文件集合」，只删一边立刻红。这是本轮唯一一处删除动作能被既有 CI 直接卡住的地方。

**D2 · 冻结声明落在规则真源正文顶部，不进 frontmatter、不进 registry**

三个候选落点，选第二个：

| 落点 | 判断 |
|---|---|
| `workflows/registry.json` 加 `frozen` 字段 | ❌ `sync-workflow-registry.py` 用 `exact_keys` 严格校验，加字段要改 12 个工作流对象 + 校验常量 + 生成投影 + 测试。为一条一次性的流程承诺改全局 schema，代价与收益不成比例 |
| `convergence-loop-engine.md` H1 之后、`## 1. 身份` 之前加一个引用块 | ✅ 任何模型加载这份规则都会读到顶部；不动章节编号，AC3「§2–§8 正文逐字未改」不受影响 |
| frontmatter 加 `status:` 键 | ❌ 规则 frontmatter 没有任何机器校验，加了既不被检查也容易被读取时剥掉，等于写在没人看的地方 |

声明写三要素，缺一不可：**冻结含义**（代码路径与行为全部保留、不再接受演进）、**冻结起始**（ITER-0116 / MILE-0016 R5）、**解冻条件**（R13 依使用数据最终处置）。不写「已废弃」「不推荐使用」这类话——冻结不是弃用，行为一字没改，命令照常能用。

**D3 · 模型自己发起 loop 的两处镜像一起删，都不补替代话术**

这是本轮最实的一处改动，也是 §5.3 amend 的由来。两处写的是同一件事：

- `logic-protocol.md` 结尾：「若检测到任务复杂度极高……应主动询问：是否需要开启收敛闭环模式」。
- `convergence-loop-engine.md §2` 激活清单第三条：「Butler 检测到极高复杂度任务，并经用户确认后开启」。

**口径要说清楚**：第三条写的是「经用户确认后开启」，字面上不违反 registry 的 `allow_implicit_invocation: false`，删它的理由不是「它违规」。理由是**发起权在模型**——由模型判断复杂度再兜售，制造的正是 R13 要拿来判 loop 生死的那份使用数据。冻结一个命令的同时留着自动推销它的话术，冻结就是空的。

删完 §2 激活条件由 3 条减为 2 条：显式命令 `/butler:loop`、显式语义（「死磕」「必须变绿」等）。两处都不补「用户明确要求时才开启」这类替代句——那话已经写在 registry 的 `allow_implicit_invocation: false` 和命令正文的「郑重触发、不是随手一敲的默认」里，再写一遍是第三、第四个真源，撞 DRY 红线。

**D4 · 拆掉 dangerous 对 loop 规则文件的最后一条纸面依赖**

`dangerous-engine.md §8` 熔断交还那段把 RCA 格式指向 `convergence-loop-engine.md §7`，而 §7 自己又转指 `bounded-convergence.md §3`。多绕一跳，不影响正确性——但 loop 已被冻结、R13 可能删它，这一跳留着就会在删除时断链。改成直指 `bounded-convergence.md §3`。

**§9「与收敛闭环 (`/butler:loop`)」那条保留**，不删。它陈述的是「两者并列、互不激活」这个关系事实，是 ITER-0110 解耦的成果记录，不是依赖。删了反而会让人以为两者关系没定义过。

**D5 · `.ai/debt.md` 一删一增，净额仍是 10 条**

- 删「危险模式规则真源仍把 P4 与 `/butler:loop` 自动绑定」——ITER-0110（`41ad694`）已还清。按文件头纪律「还掉的删除、不留历史」，不留「已还清」的墓碑；出处留在 §5.4 与交付总结。
- 增「loop 冻结无机器兜底」——本轮新欠的账，写明缺口、有意不加检查的理由、自然消解路径（R13 决定去留时这条自动作废）。

两笔分开记，不合并成一条「换了个欠账」。它们性质不同：前者是发现旧账已假，后者是新做的取舍。

**D6 · 扫描脚本这轮要守两个方向，不是一个**

ITER-0115 是纯删除，扫描只需查「不该有的还在不在」。**本轮是改而不删，最大的风险反过来——误伤**。所以扫描分两组：

- **A 组·不该有的**：`dangerous-engine.md` 里出现 `convergence-loop-engine`、两处主动发起话术的残留、活跃文件里出现 `upgrade-convergence-engine`。
- **B 组·该留的必须在**：`.claude/commands/butler/loop.md` 在、`plugins/butler/skills/butler-loop/SKILL.md` 在、`.agents/skills/butler-loop` 软链在且不断链、registry 里 loop 块在且 `workflows` 长度仍 12、`docs/workflows.md` 的 loop 行在。**任一缺失即红**。

B 组是这轮的主要保险。模式串同样用变量拼接避免自命中。脚本落在 `.ai/iterations/ITER-0116/`，**不接 `verify-ci.sh`**（同 ITER-0115 D8 的口径）。

**D7 · 本轮不触发 `[regen-entrypoints]`**

改的是 `Coder/` 下的规则文件。两份入口模板（`templates/CLAUDE.md.template`、`templates/AGENTS.md.template`）只**引用 `logic-protocol.md` 的路径**，不嵌它的内容；`templates/rule-card.md` 全文未提收敛闭环。按 `migration-schema.md §5` 的判据，改动没有流进目标项目的 `CLAUDE.md` / `AGENTS.md`，故不触发。这一条要在 §5.4 写明，与 ITER-0115 的结论并列。

**D8 · 台账推进会让 `.ai/OVERVIEW.md` 出现跟随行，预期之内**

本轮改了双台账（新开 ITER-0116、MILE-0016 含迭代数 4 → 5），`--write` 重算后 OVERVIEW 的「版本与当前状态」和「里程碑时间线」两节会跟着变。工作流清单节应当**零变化**（loop 行必须还在）。若工作流节也变了，说明误伤了 registry，停下核对。

**执行顺序**：
- [ ] T1 删候办文件 + 删 `.ai/MILESTONES.md` 待办区那一行 → AC1
- [ ] T2 `convergence-loop-engine.md`：H1 后加冻结声明块 + 删 §2 激活第三条 → AC3、AC5（半）
- [ ] T3 删 `logic-protocol.md` 那句主动询问 → AC5（半）
- [ ] T4 改 `dangerous-engine.md §8` 的 RCA 指针 → AC6
- [ ] T5 `.ai/debt.md` 一删一增 → AC7、AC8
- [ ] T6 `.ai/MILESTONE.md §5.4` 登记三条 → AC2
- [ ] T7 跑 `sync-project-overview.py --write` 重算 `.ai/OVERVIEW.md` → AC9
- [ ] T8 写两组扫描脚本并跑；完整 CI + 状态审计 + 全量 evidence 捕获 → AC4、AC10、AC11

## Failure Paths

1. **误伤 loop 实体是本轮头号风险**。上一轮的肌肉记忆是「看见 progress 就删」，这轮 loop 长得很像但必须原样留下。对策：D6 的 B 组在场断言 + AC4 的六处 `git diff --quiet` 逐个断言零改动。任何一处 loop 实体出现在 `git status` 里就是错的。
2. **候办只删一边**。删了文件忘删索引行（或反过来），`audit-project-state.py` 的 `milestones.backlog_set` 会红并打印两个集合的差。这是唯一一处不用自己造检查的删除动作，跑审计即可。
3. **删 §2 第三条时误伤同段其他行**。§2 激活清单三条格式相同，删错一条会让 loop 失去一条合法激活方式。对策：删后立刻断言激活清单恰为 2 条、且分别含 `/butler:loop` 与「死磕」；`git diff` 的删除行数必须恰为 1。
4. **`.ai/debt.md` 删错条目**。10 条里删一条、加一条，净额不变，光看条目数看不出删对没删对。对策：断言删掉的那条的关键字（「自动绑定」）零命中，且另外 9 条的首句逐条仍在。
5. **扫描脚本自己命中自己**。A 组模式串里写着 `convergence-loop-engine` 这些字样，跑全仓扫描会命中脚本自身。对策：模式串用变量拼接，且排除面显式含脚本自身路径（两道都上，B 组的在场断言不受影响）。
6. **冻结声明插错位置打乱章节**。声明块必须落在 H1 之后、`## 1. 身份` 之前。若插进 §1 内部或改了任何 `## N` 行，AC3 的「§3–§8 零改动」会红。对策：`git diff` 逐行确认新增块的上下文行是 H1 与 `## 1. 身份`。
7. **OVERVIEW 的工作流节被连带改动**。台账两节变是预期的，工作流节变不是。若出现，说明 registry 被误动，回到 Failure Path 1 排查。
8. **§5.4 三条登记写成流水账**。三条各有具体内容要点（名字撞车的事实与真实撤回理由 / debt 已假的根因与还清出处 commit / 冻结载体选择与无兜底），不能写成「登记了三件事」。对策：AC2 的证据脚本对每条的关键措辞逐个 `grep -qF`。

## Test Strategy

本迭代**不新增单元测试**。改的全是规则散文与台账，没有新增可执行逻辑；既有机器断言里真正管用的是 `audit-project-state.py` 的 backlog 一致性检查（D1）与 `sync-project-overview.py --check`（D8）。为规则文本新写单测等于给「我改对了没」再套一层自己写的判断。

**新增的唯一脚本**是 D6 的两组扫描器 `.ai/iterations/ITER-0116/ac4-ac10-sweep.py`：A 组查残留、B 组查在场，任一组有问题即非零退出并打印文件与行号。它不进 CI。

**证据捕获**（`tools/verification-evidence/evidence.py run`）：

- `ac1-backlog` (AC1)：候办文件不存在 + 索引行消失 + 剩余 9 行逐字未动 + `milestones.backlog_set` 与全部 `backlog.*` 审计行为 OK
- `ac2-registration` (AC2)：§5.4 三条登记的关键措辞逐条断言
- `ac3-ac5-freeze` (AC3,AC5)：冻结声明三要素 + 声明块位置 + §2 激活清单降为 2 条 + 两处镜像零命中 + `logic-protocol.md` 模式清单仍 8 条 + §3–§8 零改动
- `ac6-dangerous` (AC6)：`dangerous-engine.md` 全文零 `convergence-loop-engine` + §8 新指针在场 + §9 并列陈述保留 + diff 恰为 1 增 1 删
- `ac7-ac8-debt` (AC7,AC8)：删的是哪条、加的是哪条、净额 10、其余 9 条首句逐条仍在
- `ac9-overview` (AC9)：`--check` 退出码 + 体量 + 工作流清单 12 行且 loop 行在场
- `ac4-ac10-sweep` (AC4,AC10)：两组扫描器本体，含 loop 六处实体的零改动断言
- `ac11-ci-audit` (AC11)：`verify-ci.sh` + `audit-project-state.py --allow-unreleased`

**置信档**：AC1、AC4、AC9、AC10、AC11 为 auto·可靠（确定性断言，且 AC1 有既有审计兜底、AC4 是 `git diff --quiet` 这类不含判断的断言）；AC2、AC3、AC5、AC6、AC7、AC8 为 auto·弱档——机器只查得出字样在不在、行数对不对，判不了写得对不对，那部分靠人读 `git diff`。无 human·待人 档。

## References Compliance

- 本迭代无 `.ai/references/` 外部参考资料，无外部引用合规项。
- **分层不破**：动的是 SOP Core 的 `00_System_Prompt/logic-protocol.md`、Domain 扩展层的 `55_Extension_ConvergenceLoop/` 与 `65_Extension_Dangerous/`，各自只改本层自己的内容；没有把某层的职责挪进另一层。`bounded-convergence.md` 作为两个模式共用的熔断真源（ITER-0110 立的分工）本轮不动，D4 的指针改动方向正是让它更符合那次分工。
- **产物链不破**：每条设计决策都能追到 AC。AC 之外的动作只有 §5.4 的三条登记（登记性质，AC2 已覆盖）与 `.ai/debt.md` 的一删一增（AC7 / AC8 已覆盖），本轮没有 AC 覆盖不到的附带动作。
- **DRY 红线**：D3 两处镜像都删且不补替代，正是为了不制造第三、第四个「什么时候开 loop」的真源；D4 把指针改成直指真源，减少一跳转述。
- **模板 SSOT 不破**：`templates/rule-card.md` 与两份入口模板本轮未动，模板只引用 `logic-protocol.md` 的路径而不嵌内容，故**不触发 `[regen-entrypoints]`**（D7）。
- **升级处置**：本轮改的全是 butler 仓内的规则文件与台账，目标项目侧无任何受管文件形态变化，不需要新增迁移动作。无 `[global-install]`、无 `[restamp]`。
