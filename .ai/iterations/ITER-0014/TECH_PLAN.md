> ⚠️ 危险模式：本产物由模型过 dangerous-engine §5.2 自审门后自主 ACK，未经用户确认（ITER-0014，2026-06-30）。

# Goal

- 支撑 AC1–AC11：新增迁移配方规范与台账、把 `butler-upgrade` 改成配方执行器、把"切版记配方"写进版本治理，并落实危险模式护栏。

# Files / Modules to Change

- 新增 `Coder/20_Workflow_Lifecycle/migration-schema.md` —— 配方格式 + 台账位置 + 标签集 + 幂等/漂移契约的单一来源（AC1 / AC2）。
- 新增 `migrations/v1.1.0.md` / `v1.2.0.md` / `v1.3.0.md` —— 三份回填配方（AC3）。
- 改 `Coder/20_Workflow_Lifecycle/butler-upgrade.md` —— §3 侦察收集配方、§4/§5/§6 改执行器、新增 hook 副本同步、保留无戳兜底（AC4 / AC5）。
- 改 `Coder/20_Workflow_Lifecycle/versioning-schema.md` —— §5 加"记录迁移配方"步 + 指针（AC6）。
- 改 `Coder/README.md` —— 注册 migration-schema（AC7）。
- 已落：`.ai/RUN_LOG.md`、`.ai/ITERATIONS.md`（北极星 + ITER-0014）、四件套横幅（AC11）。

# Interface / Contract

- **配方文件契约**：路径 `migrations/vX.Y.Z.md`；版本号 = 该配方所属发布版；语义 = "从上一发布版升级到本版，部署项目要做的幂等步骤"。
- **执行器输入 / 输出**：输入 = 目标 `CLAUDE.md` 版本戳 `S` + 仓库 `VERSION` `C`；动作 = 取所有满足 `S < V ≤ C` 的 `migrations/vV.md`，按版本号升序逐条应用；输出 = 升级后的 `CLAUDE.md` / `.ai/` / `.claude/hooks/` + 重戳为 `C`。
- **标签集（typed 步骤）**：`[rename]`（改名）/ `[add-field]`（补 schema 必填字段）/ `[regen-claude]`（重生成 CLAUDE.md 内联段，保 user-managed 区）/ `[sync-hooks]`（同步 `.claude/hooks/` 副本）/ `[restamp]`（重戳版本）/ `[no-op]`（本版对部署项目无影响）。
- 文件间契约不变：`VERSION` 仍是版本号唯一真源；配方引用版本号、不另立版本数字。

# State / Boundary

- 配方"幂等"= 每步先校验起始态（"若旧名存在才改"/"若字段缺失才补"），重复执行不重复改；与 `mcv-deployment.md §5.2` settings 幂等合并同源思路。
- "冲突退回真人 ACK"= 起始态与配方预期不符（目标已手工漂移）时，执行器停下、报告差异、等用户决定，不强行套用。
- 边界：本迭代只改"升级 / 版本治理"两条规则 + 新增一个 schema + 配方数据；不碰 hook 代码、四件套字段、lifecycle 分流。

# Design Decisions

- **配方为主干、diff 为兜底**：把现状"diff 主驱动"翻转为"配方主驱动 + diff 校验冲突"。这与 `versioning-schema.md §7`"版本号为辅、内容差异为主"不矛盾——§7 防的是"盲目按版本号判定是否需要升级"，而配方每步都先校验起始态、漂移即退回 ACK，正是用 diff 守住每一步，不是抛弃 diff。
- **`migrations/` 放仓库根**：它是 butler 发布元数据（和 `deliveries/`、`CHANGELOG.md`、`VERSION` 同级），不是给目标项目的模板，故不放 `templates/`。
- **纯 Markdown + typed 标签**：人能读、AI 能照做，不引入 YAML/JSON 解析依赖，与 hook"零三方依赖"风格一致。
- **补 hook 副本同步**：`mcv-deployment.md §5.4` 已点明升级需同步 `.claude/hooks/` 副本却一直没落地；执行器化顺带用 `[sync-hooks]` 标签补上。
- **无戳老项目走全量兜底**：前版本化项目没有配方链起点，保留原 §4 首次升级的全量对账，不被新执行器卡死（AC5）。
- **本迭代不切版**：切版（改 VERSION / CHANGELOG / 打 tag）是用户门控的聚合动作；收口后建议把本迭代发为下一版并按新规则写 `migrations/` 配方做 dogfood。

# Execution Steps

1. 写 `migration-schema.md`（格式 / 标签 / 契约）。
2. 建 `migrations/` 并写三份回填配方。
3. 改 `butler-upgrade.md` 为执行器 + hook 同步 + 兜底。
4. 改 `versioning-schema.md §5` + 指针。
5. 注册进 `Coder/README.md`。
6. P5：独立复核（另起不读本会话的子 agent 对照 AC + CHANGELOG 核）→ 写 VERIFY → 收口三步。

# Verification Plan

- 按 `AC_LIST.md` 的 Verification Method 逐项核对：读新文件 + 读三份配方对照 CHANGELOG + grep README 注册 + VERIFY 写"配方/diff 不冲突"论证 + 五约束自检 + 危险护栏清单核对。

# Risks / Open Questions

- 配方靠"切版记录"规则纪律维持、无 hook 强制——`[no-op]` 兜底 + §5 必做步降低漏记，但不根除。
- 回填配方可能漏项——P5 独立复核交叉对照 `CHANGELOG`。
