---
title: butler 主动升级协议
audience: AI / 开发者
scope: 已部署 butler 的项目升级到当前 butler 仓库最新版的流程与保护区契约
---

# butler-upgrade (Active Upgrade)

## 1. 目标

当 butler 仓库本身发生显著演进（模板重构、schema 新增、文件重命名等）后，已部署的目标项目需要把自己的 `CLAUDE.md` 与 `.ai/` 结构同步到最新版本，同时保护项目特有内容不被覆盖。

本规则定义升级的触发条件、侦察动作、执行步骤与验证口径。与 `mcv-deployment.md`（初次部署）和 `mcv-update.md`（`.ai/` 内部维护）并列，构成基地车的生命周期三阶段。

**升级以迁移配方为主干**：butler 每次切版都产出一份 `migrations/vX.Y.Z.md`（格式见 `migration-schema.md`），逐条列出该版部署项目要做的幂等步骤。本协议据目标版本戳收集"目标戳 < vV ≤ 仓库 `VERSION`"区间的配方、按版本号升序执行，**不再每次现场推导差异**；内容 diff 降为每步的起始态校验与冲突兜底（漂移即停、退回 ACK）。无版本戳的前版本化老项目没有配方链起点，回退到 §4 全量首次升级。

## 2. 触发条件

满足以下任一条件时启动升级：

- 用户显式输入 `/butler:upgrade`（旧名 `/butler-upgrade`，MILE-0005 R2 迁入命名空间）
- 用户提到"升级 butler"、"同步到新版"、"同步 butler 规则"

不主动推断 —— 仅在触发信号出现时执行，避免在稳定状态下破坏已部署结构。

## 3. 侦察 (Scouting)

AI 必须依次完成以下动作并简要汇报：

1. 读取目标项目根目录 `CLAUDE.md`，判断是否含 `<!-- user-managed -->` 保护区标记：
   - **有标记**（新契约项目）：进入 § 5 常规升级。
   - **无标记**（老项目）：进入 § 4 首次升级。
   - **标记格式异常**（如 `<!--user-managed-->` 无空格、或标记被部分破坏）：AI 应容错识别（忽略空白 / 大小写），但若完全无法识别，退化为 § 4 首次升级。

2. 扫描 `.ai/` 目录结构：
   - 识别命名过时的文件（例如旧 `SESSION_HANDOFF.md` 无前缀，当前规范为 `02_SESSION_HANDOFF.md`）。
   - 识别缺失的 schema 必填字段（例如 `local-constraints.md` 缺 `Project Type` 或 `Active Profiles`）。
   - 识别 butler 仓当前存在但项目未有的 schema 或产物位置。

3. 读取当前 butler 仓库的最新状态：
   - `$BUTLER_PATH/templates/CLAUDE.md.template`
   - `$BUTLER_PATH/templates/rule-card.md`
   - `$BUTLER_PATH/Coder/20_Workflow_Lifecycle/` 下相关 schema

4. **计算版本 gap**：读取目标 `CLAUDE.md` 中的 `butler v…` 版本戳与 `$BUTLER_PATH/VERSION`，比较并汇报版本差（如 "v1.0.0 → v1.2.0"）。目标无版本戳=视为前版本化项目（早于版本概念引入），按 § 4 首次升级路径处理。版本 gap 仅作辅助提示，是否升级仍以文件内容差异为准绳（见 `versioning-schema.md §8`）。

5. **收集迁移配方**：取 `$BUTLER_PATH/migrations/` 下所有满足"目标戳 < vV ≤ 仓库 `VERSION`"的 `vV.md`，按版本号升序排成执行队列（格式见 `migration-schema.md`）。目标无版本戳=无配方链起点，转 §4 全量首次升级。

6. 生成升级清单草稿（=配方队列汇总：覆盖哪些版本、每版关键步骤），进入 §4（无戳老项目）或 §5（有戳常规升级，按队列执行）呈报给用户。

## 4. 首次升级（老项目，无保护区标记）

老项目的 `CLAUDE.md` 没有保护区标记。首次升级按以下流程：

1. **备份旧文件**：
   - `cp CLAUDE.md CLAUDE.md.backup-YYYYMMDD`
   - 备份 `.ai/` 下将被重命名的文件到 `.ai/backup-YYYYMMDD/`
2. **生成新版草稿**：按最新 `templates/CLAUDE.md.template` + `rule-card.md` 构造新 CLAUDE.md 骨架（含 `<!-- user-managed -->` 保护区），并把 `{{BUTLER_VERSION}}` 戳为 `$BUTLER_PATH/VERSION` 当前版本（老项目原无版本戳，此为首次戳入），但不直接写入文件。
3. **对比差异**：将旧 CLAUDE.md 与新草稿逐段对比，分类：
   - 自动可迁移：旧文件中的 butler 区内容（会被新版替换，用户无需关心）。
   - 需 ACK 的段落：旧文件中 butler 不认识的内容，判定为用户加的。
4. **交互 ACK**：对每个需 ACK 的段落，AI 向用户提问："这段内容 butler 不识别，建议移入新文件的 `<!-- user-managed -->` 保护区。接受 / 拒绝 / 修改？"
5. **写入新文件**：用户 ACK 后写入新 `CLAUDE.md`。备份文件保留。
6. **继续处理 `.ai/`**：进入 § 6 `.ai/` 结构升级。

本次升级完成后，新 `CLAUDE.md` 自带保护区标记**并戳入当前版本号**，于是有了配方链起点；下次升级自动走 §5 配方队列路径。

## 5. 常规升级（有保护区标记 + 有版本戳：执行迁移配方队列）

目标 `CLAUDE.md` 含 `<!-- user-managed -->` 保护区标记、且有版本戳时，按 §3 收集的配方队列**按序逐条执行**。每步按其 typed 标签（定义见 `migration-schema.md §4`）落地，全部幂等、先校验起始态：

1. **逐版逐步执行**：对队列中每个 `migrations/vV.md`，按其 `## 迁移步骤` 顺序处理标签：
   - `[regen-claude]`：提取目标 user-managed 区暂存 → 按最新 `templates/CLAUDE.md.template` + `rule-card.md` 重建 butler 管理区骨架 → 原样填回 user-managed 区。
   - `[rename]`：见 §6.1。`[add-field]`：见 §6.2。`[sync-hooks]`：见 §6.4。`[split]`：见 §6.5。
   - `[restamp]`：把 `{{BUTLER_VERSION}}` 戳重戳为该步目标版本。
   - `[no-op]`：本版无结构影响，跳到 restamp。

   > 步骤性质分两类：**机械步**（`[regen-claude]` / `[rename]` / `[add-field]` / `[sync-hooks]` / `[restamp]`）起始态符合即静默自动落地；**结构迁移步 `[split]`** 是哲学级形态迁移（单文件 → 知识文件夹），**opt-in、非自动**——执行器碰到它时先问用户迁不迁，见 §6.5。两类都幂等、都先校验起始态。
2. **起始态校验与冲突**：每步执行前校验起始态是否符合配方预期。**符合**才动；**不符合**（目标已手工漂移）则停下、报告差异、退回用户 ACK，**不**强行套用（守 `versioning-schema.md §8`"内容差异为主"）。
3. **呈报升级清单给用户**：版本 gap（旧戳 → 仓库当前版本）、队列覆盖的配方版本、每版关键步骤；user-managed 区原样保留、无变化。
4. **用户 ACK 后写入**：写 `CLAUDE.md` 及改动的 `.ai/` / `.claude/hooks/`；末尾 `[restamp]` 到仓库当前 `VERSION`。

配方步骤里 `.ai/` 与 `.claude/hooks/` 的具体落地动作见 §6——`[rename]` / `[add-field]` / `[sync-hooks]` 即调用其中对应小节。

## 6. `.ai/` 与 hook 副本的落地动作（配方步骤执行细则）

§5 配方队列里的 `[rename]` / `[add-field]` / `[sync-hooks]` 步骤，按本节对应小节执行（命名 + schema 字段补齐 + hook 副本同步）：

### 6.1 命名升级

- 识别旧命名文件并重命名到新规范：
  - 若项目用 git：`git mv <old> <new>`，保留历史血缘。
  - 若未用 git：`mv <old> <new>` 并提示用户补 commit。
- 已知重命名场景（随 butler 演进，清单自动扩展）：
  - `SESSION_HANDOFF.md` → `02_SESSION_HANDOFF.md`
  - `mode-switch.md`（若存在本地副本）→ `role-switch.md`
- **不动**：`CHANGELOG` / `BUG_LOG` 等累积型文件内容（仅在文件名过时才重命名）。

### 6.2 schema 字段补齐

- 读取项目 `.ai/local-constraints.md` 与 butler 仓的 `local-constraints-schema.md`。
- 对**缺失的必填字段**（`Project Type` / `Active Profiles`），AI 基于项目侦察结果生成草稿值，交用户 ACK。
- **可选字段**缺失不强制补齐。
- 若旧文件字段格式与新 schema 差异过大（如字段名完全不匹配），退化为交互确认模式，逐字段确认。

### 6.3 不纳入升级范围

以下产物不由升级协议处理：

- `.ai/CONCEPT.md` / `AC_LIST.md` / `TECH_PLAN.md` / `VERIFY_REPORT.md`（任务产物，按当前任务阶段决定）。
- `.ai/references/`（外部参考资料，独立生命周期）。
- `deliveries/`（人类可读交付总结归档，历史不动）。

### 6.4 hook 副本同步（`[sync-hooks]`）

- 比对目标 `.claude/hooks/` 与 `$BUTLER_PATH/templates/hooks/`（除 `tests/`）。
- 不一致则按 `mcv-deployment.md §5.1` 以 butler 版本为准覆盖（目标 hooks 是 butler 拷贝副本，不得本地改动；本地化需求回流 butler 仓）。
- 同步后按 `mcv-deployment.md §5.3` 跑一次 hook 自检命令确认可用。
- 本小节补齐 `mcv-deployment.md §5.4` 指出、但此前未落地的"hook 副本随升级同步"缺口。

### 6.5 单文件文件夹化（`[split]`）

把老项目的单文件全貌产物 `.ai/PROJECT.md` 拆成 `.ai/project/` 知识文件夹。标签**语义定义**（拆什么、判据、冲突即停）以 `migration-schema.md §4` 为真源，本小节只定"升级执行器怎么落地它"。

- **性质：opt-in、非自动**。与其它机械步不同，`[split]` 是形态迁移（薄索引 → 知识文件夹），执行器**不静默自动拆**，而是先向用户呈一个选择：
  - **现在迁**：执行下面的拆分动作。
  - **继续单文件、以后再迁**：**跳过本步**，`.ai/PROJECT.md` 原样保留、单文件分支继续受支持（冷启动第一读 / 收口前滚 / 第 6 漂移不变量都有单文件回退，见 `context-persistence.md §6`）；其余机械步（`[regen-claude]` / `[restamp]`）照常执行。这与"两态并存、不强制立即迁"（`project-digest-schema.md §9`、`migrations/v2.0.0.md`）对齐。
- **起始态校验（符合才动）**：旧 `.ai/PROJECT.md` 存在**且** `.ai/project/00_INDEX.md` 尚未成形。二者不满足则本步无操作（已迁过则幂等跳过；无单文件可拆的更老项目走 `mcv-deployment.md §2` 空种子 + 首次收口生成路径，不在本步）。
- **拆分动作**（用户选"现在迁"后）：按 `project-digest-schema.md §3` 主题集，把单文件内容路由进 `00_INDEX.md`（入口三块）+ 各主题文件（`identity` / `architecture` / `capabilities` / `invariants` / `constraints` / `debt` / `frontier`，项目暂无内容的主题不建）。拆出的新文件走 `git add`（内容重组非纯改名，`git mv` 不适用，血缘靠本次 commit 说明追溯）；删除旧 `.ai/PROJECT.md`。
- **冲突即停**：判据与冲突处理**同 `migration-schema.md §4`**（＝ §5 步骤 2 的漂移即停纪律）——目标文件夹已部分成形、或旧单文件被手工改得与预期不符（目标项目漂移），则**不覆盖**、停下报差异、退回用户 ACK，**绝不把用户手写内容拆丢**。
- **幂等**：迁过（`00_INDEX` 已成形）则本步跳过；用户选暂缓则单文件保持、下次升级仍会再问。

## 7. 验证与回退

升级完成后，AI 应回顾并向用户报告：

- `CLAUDE.md` 含 `<!-- user-managed -->` / `<!-- /user-managed -->` 保护区标记完整；用户区内容逐字保留。
- `CLAUDE.md` 版本戳已更新到当前 butler 版本（与 `$BUTLER_PATH/VERSION` 一致）。
- `.ai/` 下无过时命名的文件。
- `local-constraints.md` 必填字段齐全（按最新 schema）。
- 配方队列每一版均已应用（无遗漏、无因漂移而中途搁置未报告的步骤）。
- `.claude/hooks/` 副本与仓库 `templates/hooks/` 一致（`[sync-hooks]` 已执行且自检通过）。
- 若队列含 `[split]`：结果二选一如实报告——**已迁文件夹态**（`.ai/project/00_INDEX.md` 成形、旧 `.ai/PROJECT.md` 已删）/ **用户选择暂缓**（单文件保留、继续两态支持）；不得有"该停没停 / 暂缓未报告 / 拆丢用户内容"的静默。

如果用户对升级结果不满意，回退路径：

- **`CLAUDE.md`**：从备份恢复 `cp CLAUDE.md.backup-YYYYMMDD CLAUDE.md`。
- **`.ai/` 重命名**：若已 git commit，用 `git revert` 或 `git reset` 回滚；若未 commit，从备份目录 `cp -r .ai/backup-YYYYMMDD/* .ai/` 恢复。
- **schema 补齐**：直接删除新增字段即可（无破坏性副作用）。

本规则不提供自动 rollback 能力；回退机制靠 git + 备份文件。

## 8. 边界说明

本规则不负责：

- **`deliveries/` 历史迁移**：人类可读交付总结归档，升级协议不改动。
- **`CHANGELOG` / `BUG_LOG` 内容改写**：累积型维护文件内容属项目历史。
- **butler 仓库自身的升级**：butler 仓（作为规则源）自身的版本与发布由 `versioning-schema.md` 的切版流程管理（VERSION / CHANGELOG / git tag），不走 butler-upgrade（后者面向"目标项目"而非 butler 本身）。
- **版本号为辅、内容差异为主**：升级以文件内容差异为准绳；版本 gap（目标戳 vs 仓库 `VERSION`）仅作辅助提示与升级后重戳的依据，**不单凭版本号判定是否需要升级**——目标内容可能已手工漂移，版本号无法反映（见 `versioning-schema.md §8`）。
