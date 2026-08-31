---
状态: ack-frozen
ACK 日期: 2026-08-20
修订记录: 2026-08-20 · ① 冻结后发现 `convergence-loop-engine.md §2` 激活清单第三条「Butler 检测到极高复杂度任务，并经用户确认后开启」是 `logic-protocol.md` 那句主动询问在规则真源里的镜像；原 AC3 要求「§2–§8 正文逐字未改」会强制把它留下，与本轮「loop 只在被点名时才动」的意图直接冲突。按 `iteration-schema.md §5.3` 退回 draft：AC3 改为允许 §2 激活清单这一处删除、其余正文仍须逐字未改，AC5 扩为两处镜像一并清除。影响面未变——该文件本就在 In Scope。
---
<!-- butler-artifact-template: 1.0.0 artifact=acceptance -->
# AC_LIST — ITER-0116

## Goal

- 一次迭代做两件独立的清理：把 `upgrade-convergence-engine` 候办撤掉（升级器从没在真实项目上跑过，现在规划三个迭代的重写没有依据），把 `/butler:loop` 的演进冻结（代码路径与行为一字不动，只停投入，去留归 R13）。同时把这次核查暴露的三处问题一并处理：`logic-protocol.md` 里那句主动推销 loop 的话与 registry 的「必须显式」自相矛盾；`dangerous-engine.md` 对 loop 规则文件还有一条纸面依赖；`.ai/debt.md` 里有一条早在 ITER-0110 就还清了的账。

## In Scope

- 删 `.ai/milestone-backlog/upgrade-convergence-engine.md` 与 `.ai/MILESTONES.md` 待办区对应那一行，两侧同批删净。
- 在 `Coder/55_Extension_ConvergenceLoop/convergence-loop-engine.md` 写明冻结状态：冻结含义（保留代码路径与行为、不再接受演进）、冻结起始（ITER-0116 / MILE-0016 R5）、解冻条件（R13 依使用数据最终处置）。
- 删掉模型自己发起 loop 的两处镜像：`Coder/00_System_Prompt/logic-protocol.md` 结尾那句「若检测到任务复杂度极高……应主动询问：是否需要开启收敛闭环模式」，以及 `Coder/55_Extension_ConvergenceLoop/convergence-loop-engine.md §2` 激活清单第三条「Butler 检测到极高复杂度任务，并经用户确认后开启」。两处都不补替代话术；`logic-protocol.md` 里 loop 的模式条目本身保留不动。
- 改 `Coder/65_Extension_Dangerous/dangerous-engine.md §8` 的 RCA 指针，从 `convergence-loop-engine.md §7` 改为直指 `30_Quality_Gate/bounded-convergence.md §3`；dangerous 其余内容不动。
- 删 `.ai/debt.md` 里「危险模式规则真源仍把 P4 与 `/butler:loop` 自动绑定」那一条（已由 ITER-0110 还清），按文件头纪律不留历史。
- 在 `.ai/MILESTONE.md §5.4` 登记三条：①候办与 loop 是名字撞车、路线项措辞把两件事捆在一起，本轮按两件独立清理执行；②debt 那条已假的发现、根因（ITER-0114 整批迁移未复核）与还清出处（`41ad694`）；③冻结的载体选择与「没有机器兜底」这个事实。
- 用 `scripts/sync-project-overview.py --write` 重算 `.ai/OVERVIEW.md`。

## Out of Scope

- **不删 `/butler:loop`**：命令、Codex skill、`.agents/skills/` 软链、`workflows/registry.json` 条目、`docs/workflows.md` 行、`plugin.json` 描述全部原样保留，行为一字不改。
- 不给 `workflows/registry.json` 加「冻结」字段，也不改 `sync-workflow-registry.py` 的字段集校验（理由与代价见 TECH_PLAN；缺口登记进 `.ai/debt.md`）。
- 不给 `milestone-schema.md` 新增 `候办状态` 取值——撤回用「两侧删净 + 台账留痕」表达，不引入第三态。
- 不改 `bounded-convergence.md` 的熔断纪律、`correction-contract.md` 的常驻「诚实停」、`convergence-loop-engine.md` 的 §2–§8 算法正文。
- 不动 `/butler:dangerous` 的激活语义、自审门、审计与回滚护栏。
- 不处置另外 9 份候办，不重新评估它们的暂缓理由。
- 不装使用数据采集（R11）、不做 loop 最终去留判断（R13）、不动升级器动作类型（R14）与迁移配方（R15）。
- 不切版、不发布。

## Acceptance Checklist

- [ ] AC1: `.ai/milestone-backlog/upgrade-convergence-engine.md` 不存在，`.ai/MILESTONES.md` 待办区不再有 `upgrade-convergence-engine` 行且剩余 9 行内容逐字未动；`audit-project-state.py` 的 `milestones.backlog_set` 为 OK（索引集合与实际文件集合仍相等），其余 9 个候办的 `backlog.<slug>.*` 全部保持 OK。
- [ ] AC2: `.ai/MILESTONE.md §5.4` 追加三条登记且各自写到位——①点明候办与 loop 只是名字都含「收敛」、路线项 In Scope 的措辞把两件事捆在一起，本轮按两件独立清理执行，并写明撤候办的真实理由是「升级器从没在真实已部署项目上跑过」而不是「loop 降级」；②写明 debt 那条已假、根因是 ITER-0114 从 `frontier.md` 整批迁移时未复核、还清出处是 commit `41ad694`（ITER-0110）；③写明冻结落在规则真源、没有机器兜底、解冻条件是 R13。
- [ ] AC3: `Coder/55_Extension_ConvergenceLoop/convergence-loop-engine.md` 含冻结声明，三要素齐备——冻结含义写明「代码路径与行为保留、不再接受演进」、冻结起始标明 ITER-0116（MILE-0016 R5）、解冻条件指向 R13 且写明依据是使用数据。除新增声明段与 §2 激活清单删掉的那一条外，§2–§8 正文逐字未改：`git diff` 的删除行恰为 1 行（即那条第三激活条件），无其他正文行改动；§3–§8 的算法正文零改动。
- [ ] AC4: `/butler:loop` 实体与元数据零改动——`.claude/commands/butler/loop.md`、`plugins/butler/skills/butler-loop/SKILL.md` 与 `agents/openai.yaml`、`.agents/skills/butler-loop` 软链、`docs/workflows.md` 的 loop 行、`plugins/butler/.codex-plugin/plugin.json` 全部与本轮开工前逐字节相同；`workflows/registry.json` 的 loop 块逐字段相同，`workflows` 长度仍 12。
- [ ] AC5: 模型自己发起 loop 的两处镜像全部清除——`Coder/00_System_Prompt/logic-protocol.md` 全文不再出现「是否需要开启收敛闭环模式」这句主动询问，`Coder/55_Extension_ConvergenceLoop/convergence-loop-engine.md §2` 激活清单不再含「Butler 检测到极高复杂度任务」这一条，激活条件由 3 条减为 2 条（显式命令、显式语义），两处都不补等价替代话术（全仓不出现「检测到」+「复杂度」+「收敛闭环」的组合）。`logic-protocol.md` 里「收敛闭环模式 (`/butler:loop`)」那条模式说明仍在且正文未改；模式清单仍是 8 条、顺序未变，其余 7 条（Standard / Explore·Ideation / Review / Butler Upgrade / Butler Setup / Dangerous / Preference）逐条未动。
- [ ] AC6: `Coder/65_Extension_Dangerous/dangerous-engine.md` 全文不再引用 `convergence-loop-engine.md`，§8 的 RCA 指针改为 `30_Quality_Gate/bounded-convergence.md §3`；§9「与收敛闭环」那条保留（它陈述的是两者并列关系，不是依赖）；除这一处指针外 `git diff` 无其他正文改动。
- [ ] AC7: `.ai/debt.md` 条目数由 10 减为 9，删掉的恰是「危险模式规则真源仍把 P4 与 `/butler:loop` 自动绑定」那条，其余 9 条逐字未动；文件头「还掉的删除、不留历史」纪律未被违反（不留任何「已还清」的墓碑条目）。
- [ ] AC8: `.ai/debt.md` 新增一条登记冻结无机器兜底的欠账，写明缺口（没有任何检查能拦住有人后来又改 loop）、有意不加检查的理由、以及自然消解路径（R13 决定去留时这条自动作废）；净效果条目数回到 10。
- [ ] AC9: `.ai/OVERVIEW.md` 由 `--write` 重算且 `--check` 退出码 0，工作流清单仍 12 行且 loop 行在场，体量仍在 12000 字节上限内。
- [ ] AC10: 可重跑扫描断言两组均零命中——A 组查 loop 冻结的反面证据（`dangerous-engine.md` 指向 `convergence-loop-engine`、logic-protocol 的主动询问话术、`upgrade-convergence-engine` 在活跃文件中的残留引用）；B 组查 loop 实体是否被误伤（命令 / skill / 软链 / registry 条目缺任一即红）。扫描面排除历史归档（`.ai/iterations/`、`.ai/history/`、`deliveries/`）、已发布迁移配方（`migrations/`）、第三方依赖（`.venv/`、`.git/`）与本迭代工作区产物及台账。
- [ ] AC11: `bash scripts/verify-ci.sh` 退出码 0；`python3 scripts/audit-project-state.py --project-root . --allow-unreleased` 退出码 0，非 OK 行只剩 `UNRELEASED` 发布态亮牌与历史迭代的 `INFO` 诊断留存行。

## Verification Method

- AC1: `test -e` 断言候办文件不存在；`grep -c 'upgrade-convergence-engine' .ai/MILESTONES.md` 为 0，待办区行数由 10 变 9 且 `git diff` 只有一行删除；跑 `audit-project-state.py` 取 `milestones.backlog_set` 与全部 `backlog.*` 行的状态。
- AC2 / AC3: 逐条 `grep -qF` 断言关键措辞在场；`git diff` 人读确认 `convergence-loop-engine.md` 只有新增段、无正文行改动。
- AC4: 对 loop 的六个落点逐个 `git diff --quiet` 断言零改动；`python3 -c` 读 registry 断言 loop 块字段与长度。
- AC5 / AC6: `grep -c` 断言旧话术与旧指针零命中、新指针在场、保留项仍在；`git diff` 断言改动行数（logic-protocol 应为纯删、dangerous 应为 1 增 1 删）。
- AC7 / AC8: `grep -c '^- \*\*'` 断言条目数变化；`git diff .ai/debt.md` 人读确认删的是哪条、加的是哪条。
- AC9: `--write` 后 `--check` 取退出码；`wc -c` 实测；`grep -c '| loop |' .ai/OVERVIEW.md` 为 1。
- AC10: 新增 `.ai/iterations/ITER-0116/` 下一条扫描脚本，两组模式各自跑并在命中时非零退出、打印文件与行号；模式串用变量拼接避免自命中；命令与输出整份进 evidence。
- AC11: 两条命令各取退出码并留存完整输出。

## External References

- N/A（本迭代无 `.ai/references/` 外部参考资料）。

## Open Questions / Risks

- **风险 · 撤候办是判断不是数据**。依据是「升级器从没在真实已部署项目上跑过，给没被真实用过的工具规划三个迭代的重写属于过度设计」。这个判断本身也没有使用数据支撑——装监视器是 R11。如果 R15 的真实回归暴露升级器确实卡得很死，要开一份**新**候办承接，不是复活这份 2026-08-04 的范围评估；交付总结要写明依据性质。
- **风险 · 冻结靠自觉，没有机器能拦**。真正的强制只有删除，而删除正是本轮明确不做的。冻结声明写在规则真源里，任何人（含未来的 AI 会话）都可能视而不见。AC8 把这个缺口如实记进 `.ai/debt.md`，不假装它被守住了。
- **已定 · 不给 registry 加冻结字段**。`sync-workflow-registry.py` 用 `exact_keys` 严格校验，加一个字段要同时改 12 个工作流对象、校验常量、生成投影与相关测试——为一条一次性的流程承诺改动全局 schema，代价与收益不成比例。口径与 ITER-0115 处置散文计数一致：能治本的治本，治不了的如实登记。
- **已定 · 撤回不引入 `候办状态` 第三态**。`milestone-schema.md` 只定义 `deferred` 一个取值，`audit-project-state.py` 也按这一个值断言。撤回用「文件与索引行两侧删净 + 理由留在 §5.4 与交付总结」表达，与 butler 处理退役的一贯口径（删除、不留墓碑）一致。
- **已定 · 两处镜像删了都不补替代**。补一句「用户明确要求时才开启」等于把已经写在 registry（`allow_implicit_invocation: false`）和命令正文（「郑重触发、不是随手一敲的默认」）里的话第三、第四次复述，属于 DRY 红线内的重复真源。
- **口径说明 · 那条第三激活条件不算「隐式调用」，但仍要删**。它写的是「经用户确认后开启」，字面上不违反 `allow_implicit_invocation: false`。删它的理由是另一条：**发起权在模型**。冻结的核心含义是「只在被点名时才动」，由模型判断复杂度再兜售，制造的正是 R13 要拿来判 loop 生死的那份使用数据。
