<!-- butler-artifact-template: 1.0.0 artifact=tech_plan -->
# TECH_PLAN — ITER-0112

方案状态: pass
方案审查日期: 2026-08-18
方案审查方式: user-ack

## Design Decisions

### 总体取法

按「先删物、再断规则、后拆机器校验、最后去指针」四段推进，每段结束都能通过 `verify-ci.sh`。不采用「一次性大改再统一修 CI」，因为改动散在 34 个文件里，一次性改完出错时无法二分定位。

被放弃的方案：整目录 `rm -rf .ai/project/` 后统一补。放弃原因是 `invariants.md` / `frontier.md` 本轮要留，且部署项目的 `.ai/project/workspaces.md` 是另一套 live 契约（见下），整目录删会误伤。

### 关键发现：`.ai/project/` 里还住着一个不相干的 live 契约

`.ai/project/workspaces.md` 是 workspace-scope 的项目工作区地图，被 PreToolUse hook（`templates/hooks/lib/workspace_scope.py`）、`workspace-scope-schema.md`、`prd-split.md`、`prd-status.md` 与 4 份测试实际消费。它不是知识摘要，只是恰好住在这个目录里；butler 仓自身是单包项目、没有这个文件，所以前几轮盘点没看见它。

决策：**本轮不动 `workspaces.md` 的路径**。理由是目录本轮本来就不消失（`invariants.md` / `frontier.md` 留着），移动一个被 hook 消费的路径属于破坏性变更、要配迁移动作，成本与收益不匹配。R1 只需断掉 `workspace-scope-schema.md` 里那句「遵守 `.ai/project/` 的 current-truth 覆写语义」——它引用的是即将删除的 `project-digest-schema.md`。最终落点由 R3 连同全貌产物的家一起定。

### 改动清单（34 个文件，按段分组）

**段一 · 删物与迁移（10 处）**

| 动作 | 目标 |
|---|---|
| 删 | `.ai/project/00_INDEX.md` · `identity.md` · `constraints.md` · `capabilities.md` · `architecture.md` · `fold-state.json` |
| 删 | `Coder/62_Extension_Agents/knowledge-fold.md` · `drift-check.md` |
| 删 | `Coder/40_Context_Management/project-digest-schema.md` |
| 迁 | `.ai/project/debt.md` → `.ai/debt.md`（`git mv`，正文不改） |
| 留 | `.ai/project/invariants.md` · `frontier.md` 一字不动 |

删 `capabilities.md` 前先出迁出核查表：22 个小节逐条判「别处有真源 / 无真源需迁出 / 判定可弃」，结论写进 `.ai/01_CHANGELOG.md`。这是 AC2 的门，不能跳。

**段二 · 断规则（11 份）**

- `iteration-schema.md` — §5.5 删步④整条，步⑤降为步④；顶部动作描述去掉「第四步前滚项目全貌产物」；步⑤自检从 6 条不变量改 5 条。
- `milestone-schema.md` — §7.4 同样删步④、顶部描述同步；收口后描述里「项目全貌补漏」改为不提。
- `context-persistence.md` — §6 删第 6 条不变量（前 5 条编号不动）；冷启动读序第 1 项去掉两态分支与知识文件夹指针；「互补」段与「指针」段同步。
- `project-digest-schema.md` — 整份删除。
- `handoff-spec.md` · `references-schema.md` · `prd-split.md` · `prd-status.md` · `workspace-scope-schema.md` · `artifact-style.md` · `butler-upgrade.md` — 逐句去指针。
- `mcv-deployment.md` — §2 去掉「部署即建空 `.ai/project/` 种子」这个唯一例外；§73/75 两态段删除。
- `migration-schema.md` — `[split]` 标签**保留但标注退役**（历史配方 v1.6.0–v2.2.0 仍引用它，删了老项目跨版本升级会断），加一句「本标签自 v4.0.0 起不再产生新实例，动作类型改造见 MILE-0016 R14」。
- `overview.md` — 名册 4 个帮手改 2 个（`independent-review` / `decision-work`）。
- `Coder/README.md` — 目录结构删 3 个文件名，读取顺序同步；冷启动段与 §206 / §208 说明改写。
- `domain-model.md` · `domain-glossary.md` — 去指针。

**段三 · 拆机器校验（7 份）**

- `scripts/audit-project-state.py` — 删 `audit_fold_receipt()`（第 239–271 行）与第 182 行调用点。
- `scripts/test-audit-project-state.py` — 删对应用例。
- `tools/context-budget/context_budget.py` — `DUPLICATE_CANDIDATES` 去掉 `.ai/project/architecture.md`、`.ai/project/debt.md` 改 `.ai/debt.md`、`.ai/project/invariants.md` 保留。
- `tools/context-budget/tests/test_context_budget.py` — 同步夹具。
- `scripts/verify-codex-foundation.sh` — 第 48 行的 `.ai/project/00_INDEX.md` 从必存清单移除。
- `scripts/test-butler-upgrade.py` — `.ai/PROJECT.md` 相关用例调整（`[split]` 标签保留，用例保留但不再断言知识文件夹形态）。
- `tools/mile0009-e2e/tests/test_mile0009_e2e.py` — 第 83 行夹具改为不建知识文件夹。

**workspace-scope 的 4 份测试不动**（它们引用的是 `workspaces.md`，与本轮无关）。

**段四 · 去指针与登记（6 处）**

`AGENTS.md` · `templates/AGENTS.md.template` · `.claude/commands/butler/init.md` · `plugins/butler/skills/butler-init/SKILL.md` · 2 份候办草稿（`state-transition-trust-gate.md` / `upgrade-convergence-engine.md`）；`.ai/MILESTONE.md §5.4` 补 R14 / R15 交接登记。

### AC Coverage

AC1 段一 · AC2 段一（迁出核查表）· AC3 段二（`overview.md` + `Coder/README.md`）· AC4 段二（两处步④）· AC5 段二（`project-digest-schema.md` + §6 不变量）· AC6 段四（全仓检索）· AC7 段三（`verify-ci.sh`）· AC8 段三（audit）· AC9 段四（§5.4）· AC10 收口时写交付。十条全有落点。

### Assumptions

- `[split]` 标签保留不删——历史配方 v1.6.0 / v2.0.0 / v2.1.0 / v2.2.0 引用它，`manifest.json` 校验会核配方与标签集一致。删标签会让老项目跨版本升级链断。**验证方式**：段二改完立刻跑 `verify-ci.sh`，manifest 一致性检查会直接报。
- 删 `audit_fold_receipt` 不影响其余归档校验——它只读 `.ai/project/fold-state.json`，与 `closed 有归档` 那条独立。**验证方式**：段三改完跑 audit，`ITER-*.archive` 系列检查行数不变。
- 不动 `workspaces.md` 不会让 workspace-scope 契约悬空——它的真源是 `workspace-scope-schema.md`，只有第 22 行那句借了 `project-digest-schema.md` 的语义。**验证方式**：4 份 workspace-scope 测试全绿。

### Alternatives / Trade-offs

- **整目录删 vs 选择性删**：选后者。前者更干净，但会误伤本轮要留的两份和部署项目的 `workspaces.md`。代价是 `.ai/project/` 留成一个只剩两三个文件的半拆状态，直到 R3。
- **`[split]` 删除 vs 标注退役**：选后者。删干净更彻底，但破坏历史升级链。代价是死码多留一个版本。
- **`workspaces.md` 现在搬 vs R3 再定**：选后者。现在搬需要配迁移动作和 hook 路径变更，属 R14 能力；本轮搬等于提前借用还不存在的 typed 标签。

### Impact / Scope Challenge

盘点比 P1 时多出两处：`workspaces.md` 这条 live 契约（P1 漏了，因为 butler 仓自身没这个文件），以及 `[split]` 不能删（P1 只说了它会变死码，没算历史配方的引用）。两处都已收进方案，未扩大 AC。

更小可行方案：只删 `fold-state.json` 和两个帮手、保留全部主题文件。放弃——那样折叠机制的写侧没了、读侧还在，比现在更不自洽。

## Failure Paths

- **删 `capabilities.md` 时误判「别处有真源」**：22 个小节里若有条目实际无真源却被判可弃，信息永久丢失（虽可从 git 捞回，但无人知道要捞）。缓解：核查表逐条写明真源文件名，判定可弃的必须给出具体文件与小节，不接受「散在 `Coder/` 里」这种描述。
- **删步④后步骤编号断裂**：`iteration-schema.md` 步⑤改步④，但正文别处若有「第五步自检」的交叉引用会指错。缓解：改完全文检索「第五步」「步⑤」「步5」。
- **`verify-ci.sh` 局部绿**：五处机器校验分散，容易改一半。缓解：段三每改一个文件跑一次全量 CI，不攒着一起跑。
- **`context-budget` 的重复真源检查误报**：`DUPLICATE_CANDIDATES` 少了 `architecture.md` 后，原本被这条拦住的领域概念重复可能不再被发现。缓解：改完确认 `context_budget.py check` 仍报 0 个重复，并在交付里说明这条检查的覆盖面缩小了。
- **半拆状态被误当终态**：R1 收口后 `.ai/project/` 只剩两个孤立文件、读序在过渡措辞上。缓解：`.ai/task-state.md` 与交付里都写明这是过渡态、R2/R3 承接，不写成「已完成」。
- **回滚路径**：任何一段出错，`git checkout -- <段内文件>` 即可退回段起点；整迭代回滚是一次 `git revert`。删除文件用 `git rm`，历史完整保留。

## Test Strategy

- **AC1**：`ls .ai/project/` 恰为 `invariants.md` / `frontier.md` 两项；`git diff --quiet HEAD -- .ai/project/invariants.md .ai/project/frontier.md` 返回 0；`.ai/debt.md` 与 `git show HEAD:.ai/project/debt.md` diff 仅标题行差异。
- **AC2**：人读 `.ai/01_CHANGELOG.md` 的 22 条核查表，抽查 5 条被判可弃的条目在指定真源文件中确实存在。
- **AC3**：`ls Coder/62_Extension_Agents/` 计数 3；`grep 'knowledge-fold\|drift-check' Coder/62_Extension_Agents/overview.md Coder/README.md` 零命中。
- **AC4 / AC5**：`grep '折叠\|knowledge-fold\|project-digest' Coder/20_Workflow_Lifecycle/iteration-schema.md Coder/20_Workflow_Lifecycle/milestone-schema.md` 零命中；`test ! -f Coder/40_Context_Management/project-digest-schema.md`；人读 `context-persistence.md §6` 确认 5 条编号连续；全文检索「第五步」无错指。
- **AC6**：`grep -rEl 'project-digest|knowledge-fold|drift-check|fold-state' --include='*.md' --include='*.py' --include='*.sh' --include='*.json' --include='*.template' .` 按归档白名单过滤后为空；剩余的 `.ai/project` 路径字样逐条人读，确认只指向 `invariants.md` / `frontier.md` / `workspaces.md` 三个实际存在的目标。
- **AC7**：`bash scripts/verify-ci.sh` exit 0，输出进 `tools/verification-evidence/`。段三期间每改一个文件跑一次，不只在最后跑。
- **AC8**：`python3 scripts/audit-project-state.py --project-root .` 除 `release.worktree` / `release.tag` 外全 OK，输出中无 `fold_receipt` 字样。
- **AC9 / AC10**：人读 `.ai/MILESTONE.md §5.4` 与交付总结对应段落。
- **机器验证盲区**：CI 能证明「没有指向已删文件的引用」和「测试没垮」，不能证明「删掉的内容确实无价值」。AC2 的迁出核查是人判，`capabilities.md` 那 22 条的判定质量没有机器兜底——这是本轮最大的验证盲区，必须在交付里明说。另外冷启动质量下降与否本轮无法测量，要等 R11 的使用监视器。

## References Compliance

- 本迭代无 `.ai/references/` 外部参考资料，`External References` 为 N/A。
- AC_LIST 无 `prd_refs`，故不产出 `Workspace Write Plan`；本迭代改动全在 butler 仓单包内，无跨 workspace 写入。
- 未命中任何 Domain / Stack Profile，按通用 SOP 与 `Coder/30_Quality_Gate/` 的常驻底线（`implementation-discipline` 最小实现纪律、`correction-contract` 纠错契约）执行。
