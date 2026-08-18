---
状态: ack-frozen
ACK 日期: 2026-08-18
---
<!-- butler-artifact-template: 1.0.0 artifact=acceptance -->
# AC_LIST — ITER-0112

## Goal

- 让 `.ai/project/` 里被证明维护不住的六份、支撑折叠的 `project-digest-schema.md` 契约与 `knowledge-fold` / `drift-check` 两个帮手从 Butler 消失，同批解除迭代与里程碑收口仪式对折叠的强制，并把因删除而失效的指针全部改到自洽——本迭代收口时仓库不留任何指向已删文件的活引用。被证明有效的 `invariants.md` 与 `frontier.md` 原位保留、内容不动，交给 R3 的替代品设计。

## In Scope

- 删除 `.ai/project/` 下 6 个文件（`00_INDEX.md` / `identity.md` / `constraints.md` / `capabilities.md` / `architecture.md` / `fold-state.json`）；删 `capabilities.md` 前逐条核，凡本仓别处无真源的判断先迁出。
- `invariants.md` 与 `frontier.md` 原位保留；`frontier.md` 一字不动，`invariants.md` 只修订因本轮删除而变假的三条不变量，理由层完整保留。目录留这两份 + 迁走 `debt.md` 后不再有其他内容。
- `debt.md` 迁到 `.ai/debt.md`，内容原样保留。
- 删除 `Coder/62_Extension_Agents/knowledge-fold.md` 与 `drift-check.md`，从名册 `overview.md` 与 `Coder/README.md` 注销。
- 重写 `iteration-schema.md §5.5 步④` 与 `milestone-schema.md §7.4 步④`，去掉折叠必做项及其两态分支。
- 删除 `Coder/40_Context_Management/project-digest-schema.md` 并从 `Coder/README.md` 注销；单文件 `.ai/PROJECT.md` legacy 形态一并停支持。
- 删除 `context-persistence.md §6` 的「知识文件夹漂移自检」不变量。
- 拆除机器侧校验与夹具：`scripts/audit-project-state.py`（含 `test-audit-project-state.py`）、`tools/context-budget/`、`templates/hooks/` 三份测试、`tools/workspace-scope/tests/`、`tools/mile0009-e2e/tests/`、`scripts/verify-codex-foundation.sh`、`scripts/test-butler-upgrade.py`。
- 最小去指针：`AGENTS.md`、`templates/AGENTS.md.template`、`Coder/README.md`、`.claude/commands/butler/init.md`、`plugins/butler/skills/butler-init/SKILL.md`、`mcv-deployment.md`、`handoff-spec.md`、`references-schema.md`、`prd-split.md`、`prd-status.md`、`workspace-scope-schema.md`、`artifact-style.md`、`butler-upgrade.md`、`migration-schema.md`、`domain-model.md`、`domain-glossary.md`、2 份候办草稿。
- 在 `.ai/MILESTONE.md §5.4` 登记交接给 R14 / R15 的确定输入：`[split]` 标签、`upgrade.py` 的 `--split` 必填参数与 `project-knowledge-shape-valid` 前置、`mcv-deployment.md §2` 的空种子例外。

## Out of Scope

- 不定义新冷启动读序的正面内容，不改两份入口模板的读序段落（R2）。
- 不改 `upgrade.py` 的动作类型表、路径校验与 CLI 参数，不新增删除 / 移动两类 typed 标签（R14）；不写 `migrations/v4.0.0.md`（R15）。
- 不动 `/butler:progress`（R4）、`/butler:loop`（R5）、旧 inbox 全链与 `origin/`（R8）、根布局改名与迁位（R9）。
- 不设计新的全貌产物——生成部分的派生源与手写部分的落点归 R3。
- 不改双台账结构与状态值，不改 `.ai/references/` 与 PRD 子系统自身契约。
- 不切版、不发布。

## Acceptance Checklist

- [ ] AC1: `.ai/project/` 下只剩 `invariants.md` 与 `frontier.md` 两个文件；`frontier.md` 与本迭代开工前逐字节相同；`invariants.md` 仅允许修订三条因本轮删除而变假的不变量（冷启动读序第一读、一致性自检条数、全貌产物形态），其余条目与 38 条 `*为什么*` 理由一字不动；`.ai/debt.md` 存在且内容与迁移前 `.ai/project/debt.md` 逐字节相同（除新增迁出条目外无实质改写）。
- [ ] AC2: 删 `capabilities.md` 前的迁出核查有留痕——22 个小节逐条过一遍后，本仓别处无真源的判断已迁到明确归属文件，判定为可弃的条目在 `.ai/01_CHANGELOG.md` 列明；不接受整文件直接删除。
- [ ] AC3: `Coder/62_Extension_Agents/` 只剩 `overview.md` / `independent-review.md` / `decision-work.md` 三个文件；`overview.md` 名册为两个帮手，`Coder/README.md` 的目录结构与读取顺序同步注销两份。
- [ ] AC4: `iteration-schema.md §5.5 步④` 与 `milestone-schema.md §7.4 步④` 不再出现知识文件夹折叠的必做要求与两态分支，且两处步骤编号与上下文仍连贯。
- [ ] AC5: `Coder/40_Context_Management/project-digest-schema.md` 已删除并从 `Coder/README.md` 注销；`context-persistence.md §6` 的漂移自检不变量已删除，其余不变量编号连续。
- [ ] AC6: 全仓检索 `\.ai/project|project-digest|knowledge-fold|drift-check|fold-state` 在活跃文件中零命中；历史归档（`.ai/iterations/`、`.ai/milestones/`、`.ai/history/`、`deliveries/`、`migrations/v1.6.0`–`v2.2.0`、`CHANGELOG.md`、`docs/research/`）允许保留，不回溯改写。
- [ ] AC7: `scripts/verify-ci.sh` 一次跑完全绿，无跳过、无单点豁免。
- [ ] AC8: `scripts/audit-project-state.py --project-root .` 除 `release.worktree` / `release.tag` 两项发布态 DRIFT 外全 OK，不再输出任何 fold receipt 或知识文件夹相关校验行。
- [ ] AC9: `.ai/MILESTONE.md §5.4` 含 R14 / R15 交接登记，三处（`[split]` 标签、`--split` 参数与前置、空种子例外）逐项写明现状与归属路线项。
- [ ] AC10: 交付总结如实记录两项信息损失——`fold-state.json` 的折叠回执历史不可再机器验证，以及本轮论证的是「无证据被消费」而非「已证明从未被消费」，确定性数据要等 R11。

## Verification Method

- AC1: `ls .ai/project/` 输出恰为两项；`git diff --quiet HEAD -- .ai/project/frontier.md` 返回 0；`git diff --stat -- .ai/project/invariants.md` 恰为 3 行改动且人读确认只动那三条；`grep -c '为什么' .ai/project/invariants.md` 不小于 38；`test -f .ai/debt.md` 且与 `git show HEAD:.ai/project/debt.md` `diff` 比对正文。
- AC2: 人读核对 `.ai/01_CHANGELOG.md` 的迁出/可弃清单共 22 条，逐条抽查被判可弃的条目在指定真源文件中确实存在。
- AC3: `ls Coder/62_Extension_Agents/` 计数为 3；`grep -c 'knowledge-fold\|drift-check' Coder/62_Extension_Agents/overview.md Coder/README.md` 为 0。
- AC4: 人读两处步骤全文；`grep -n '折叠\|knowledge-fold\|project-digest' Coder/20_Workflow_Lifecycle/iteration-schema.md Coder/20_Workflow_Lifecycle/milestone-schema.md` 零命中。
- AC5: `test ! -f Coder/40_Context_Management/project-digest-schema.md`；`grep -n 'project-digest' Coder/README.md` 零命中；人读 `context-persistence.md §6` 确认编号连续。
- AC6: `grep -rEl 'project-digest|knowledge-fold|drift-check|fold-state' --include='*.md' --include='*.py' --include='*.sh' --include='*.json' --include='*.template' .` 后按归档白名单过滤，结果为空；`.ai/project` 路径字样允许保留在仍指向 `invariants.md` / `frontier.md` 的引用上，需逐条人读确认指得到实际文件。
- AC7: `bash scripts/verify-ci.sh`，exit 0，输出留证。
- AC8: `python3 scripts/audit-project-state.py --project-root .`，人读输出行。
- AC9: 人读 `.ai/MILESTONE.md §5.4` 末三条演进记录。
- AC10: 人读 `deliveries/ITER-0112-*.md` 对应段落。

## External References

- N/A（本迭代无 `.ai/references/` 外部参考资料）。

## Open Questions / Risks

- **风险 · 删 `capabilities.md` 会连带删掉唯一真源**：27KB、22 个小节，按里程碑卷起来的能力总览别处没有。AC2 就是为此设的门，逐条过是本轮最耗时也最不能省的一步。`invariants.md` 这轮不删，风险不涉及它。
- **风险 · 机器门禁改一半**：audit、context-budget、hook 测试、workspace-scope 测试、codex 基线脚本五处都拿 `.ai/project` 当夹具或断言，容易出现局部绿局部红。AC7 要求 `verify-ci.sh` 一次全绿，不接受单点跑过。
- **风险 · 删了才发现有人在读**：回滚成本是一次 `git revert` 加一轮读序回退，可接受；但验证阶段要诚实记录冷启动体感，不能因为删了就写成没影响。真正的确定性数据要等 R11 的使用监视器。
- **待定 · R1 收口后到 R3 之间的过渡态**：本轮只把旧指针改到不悬空，`context-persistence.md §6` 第一读会短暂处在「不再指知识文件夹、但新读序尚未正式定义」的过渡措辞上，`.ai/project/` 也会暂时只剩两个孤立文件。这是有意的——R2 定读序、R3 定全貌产物落点；但若 R2/R3 迟迟不开，这个半拆状态会变成事实上的常态，比拆干净或不拆都糟。
- **amend 记录（2026-08-18）**：P4 执行时发现 AC1「`invariants.md` 一字不动」与 AC6「活文件无断指针」直接冲突——该文件里有三条不变量（冷启动读序第一读两态、一致性自检 6 条、全貌产物 = 知识文件夹）在本轮删除后成为假陈述，留着正是本里程碑要消灭的「陈旧的完整」。按 `iteration-schema.md §5.3` amend：AC1 收窄为「只允许改这三条」，其余与理由层仍受字节约束。
