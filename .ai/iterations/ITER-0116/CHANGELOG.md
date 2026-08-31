<!-- butler-artifact-template: 1.0.0 artifact=changelog -->
# ITER-0116 变更流

> /butler:loop 降级与候办清理（MILE-0016 R5） · closed · 2026-08-20

## ADD

- `Coder/55_Extension_ConvergenceLoop/convergence-loop-engine.md`：H1 之后、`## 1. 身份` 之前新增冻结声明块（引用块，9 行）。三要素齐备——冻结含义（正文原样保留并照常生效、`/butler:loop` 依然可用，冻结的是**演进**）、冻结起始（ITER-0116 / MILE-0016 R5）、解冻条件（R13 依真实使用数据做最终处置）；末段明写「靠声明和评审自觉、没有任何机器检查会拦住违反它的改动」。→ AC3
- `.ai/debt.md`：新增一条「`/butler:loop` 的演进冻结没有机器兜底」，写明缺口、有意不加检查的理由（registry 加字段要连带改 12 个工作流对象与严格字段校验、生成投影和测试）与自然消解路径（随 R13 的最终处置作废）。→ AC8
- `.ai/MILESTONE.md §5.4`：追加三条 R5 登记——①候办与 loop 只是名字撞车、路线项措辞把两件事捆在一起，本轮按两件独立清理执行，含撤候办的真实理由与重启条件、并澄清 R14 / R15 未覆盖其范围；②debt 那条已假的发现、根因（ITER-0114 整批迁移只搬字面未复核）与还清出处 `41ad694`；③冻结的载体选择（否掉 registry 加字段、否掉写进 frontmatter）、由此产生的无兜底事实，以及按 `migration-schema.md §5` 判定本轮不触发 `[regen-entrypoints]`。→ AC2
- `.ai/iterations/ITER-0116/loop-entities.baseline`：P4 开工前录下 loop 六处实体的内容哈希。`workflows/registry.json` 与 `docs/workflows.md` 带着 ITER-0115 的未提交改动，对 HEAD 做 `git diff` 会假红，故这六处一律用内容哈希做零改动基线。
- `.ai/iterations/ITER-0116/ac4-ac10-sweep.py`：两组扫描器。A 组查残留（主动询问原句、激活清单第三条、已撤候办的键、「检测到 + 复杂度 + 收敛闭环」等价组合），B 组查在场（六处实体哈希、软链可解析、registry 仍 12 且 loop 的 `allow_implicit_invocation` 仍 false、冻结声明三要素与落点、§2 激活恰 2 条、§3–§8 章节齐全、模式清单仍 8 条、dangerous 三项、候办两侧集合一致、debt 一删一增、§5.4 三条登记）。不接 `verify-ci.sh`。→ AC4 / AC10
- `.ai/iterations/ITER-0116/` 下 6 份 AC 证据脚本：`ac1-backlog.sh`、`ac2-registration.sh`、`ac3-ac5-freeze.sh`、`ac6-dangerous.sh`、`ac7-ac8-debt.sh`、`ac9-overview.sh`、`ac11-ci-audit.sh`。
- `.ai/verification-evidence/` 新增 8 条记录，覆盖 AC1–AC11 全部十一项。

## EDIT

- `Coder/55_Extension_ConvergenceLoop/convergence-loop-engine.md §2`：激活清单第三条「Butler 检测到极高复杂度任务，并经用户确认后开启」删除，激活条件由 3 条减为 2 条（显式命令 `/butler:loop`、显式语义「死磕 / 必须变绿 / 不准报错 / 严格校验」）；新末条的句末 `；` 随之改为 `。`。§3–§8 算法正文零改动。→ AC5 / AC3
- `Coder/65_Extension_Dangerous/dangerous-engine.md §8`：熔断交还那段的 RCA 指针由 `convergence-loop-engine.md §7` 改为直指 `30_Quality_Gate/bounded-convergence.md §3`，解除 dangerous 对 loop 规则文件的最后一条纸面依赖。改动恰为 1 增 1 删；§9「与收敛闭环 (`/butler:loop`)」的并列陈述保留不动（它陈述关系事实，不是依赖）。→ AC6
- `.ai/OVERVIEW.md`：由 `scripts/sync-project-overview.py --write` 重算，8798 字节。相对 P4 前只有台账跟随行变化（MILE-0016 含迭代数随 ITER-0116 开启递增）；工作流清单仍 12 行、loop 行在场且字段未动。→ AC9
- `.ai/ITERATIONS.md` / `.ai/MILESTONE.md` / `.ai/MILESTONES.md` / `.ai/state-index.json` / `.ai/task-state.md` / `.ai/02_SESSION_HANDOFF.md` / `.ai/handoff-state.json`：迭代与里程碑台账随 ITER-0116 推进更新，状态索引与 handoff 重新同步至 fresh。
- `.ai/CONCEPT.md` / `.ai/AC_LIST.md` / `.ai/TECH_PLAN.md`：本迭代四件套。`AC_LIST.md` 按 `iteration-schema.md §5.3` 退回 draft 修订一次后重新 ACK（`ack-frozen`，2026-08-20），修订记录写在 frontmatter 单行。

## DELETE

- `.ai/milestone-backlog/upgrade-convergence-engine.md`（7775 字节）与 `.ai/MILESTONES.md` 待办区对应那一行：候办撤回，两侧同批删净。候办文件数与索引行数由 10 同步减为 9，`audit-project-state.py` 的 `milestones.backlog_set` 集合一致性检查为 OK。→ AC1
- `Coder/00_System_Prompt/logic-protocol.md` 结尾整段（连同其后的空行共 2 行）：「若检测到任务复杂度极高（如核心算法、大规模重构），应主动询问：检测到逻辑复杂，是否需要开启收敛闭环模式进行高强度迭代验证？」删除，零新增行。模式清单仍 8 条、顺序未变，「收敛闭环模式 (`/butler:loop`)」那条正文未改。→ AC5
- `.ai/debt.md`「危险模式规则真源仍把 P4 与 `/butler:loop` 自动绑定」一条：ITER-0110（`41ad694`）已还清，按文件头纪律「还掉的删除、不留历史」清除，不留「已还清」墓碑。条目数一删一增后仍为 10。→ AC7

**覆盖面变化**：`/butler:loop` 的触发面由「显式命令 + 显式语义 + 模型自判复杂度后兜售」收敛为「显式命令 + 显式语义」两条，与 `workflows/registry.json` 的 `allow_implicit_invocation: false` 对齐。命令行为本身一字未改。

**未删的部分**：`/butler:loop` 的命令、Codex skill、`.agents/skills/` 软链、registry 条目、`docs/workflows.md` 的行、`plugins/butler/.codex-plugin/plugin.json` 全部逐字节保留（哈希比对为证）；`logic-protocol.md` 里 loop 的模式条目、`dangerous-engine.md §9` 的并列陈述、`bounded-convergence.md` 全文均未动。删不删归 R13。
