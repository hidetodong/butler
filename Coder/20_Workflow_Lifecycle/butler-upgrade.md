---
title: butler 主动升级协议
audience: AI / 开发者
scope: 已部署 butler 的项目升级到当前 butler 仓库最新版的流程与保护区契约
---

# butler-upgrade (Active Upgrade)

## 1. 目标

当 butler 仓库本身发生显著演进（模板重构、schema 新增、文件重命名等）后，已部署的目标项目需要把自己的 `CLAUDE.md` 与 `.ai/` 结构同步到最新版本，同时保护项目特有内容不被覆盖。

本规则定义升级的触发条件、侦察动作、执行步骤与验证口径。与 `mcv-deployment.md`（初次部署）和 `mcv-update.md`（`.ai/` 内部维护）并列，构成基地车的生命周期三阶段。

## 2. 触发条件

满足以下任一条件时启动升级：

- 用户显式输入 `/butler-upgrade`
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

4. **计算版本 gap**：读取目标 `CLAUDE.md` 中的 `butler v…` 版本戳与 `$BUTLER_PATH/VERSION`，比较并汇报版本差（如 "v1.0.0 → v1.2.0"）。目标无版本戳=视为前版本化项目（早于版本概念引入），按 § 4 首次升级路径处理。版本 gap 仅作辅助提示，是否升级仍以文件内容差异为准绳（见 `versioning-schema.md §7`）。

5. 生成升级清单草稿，进入 § 4 或 § 5 呈报给用户。

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

本次升级完成后，新 `CLAUDE.md` 自带保护区标记，下次升级自动走 § 5 路径。

## 5. 常规升级（新契约项目，有保护区标记）

项目 `CLAUDE.md` 含 `<!-- user-managed -->` 保护区标记的正常升级流程：

1. **读取用户区**：提取 `<!-- user-managed -->` 到 `<!-- /user-managed -->` 之间的内容，暂存。
2. **生成新框架**：按最新 `templates/CLAUDE.md.template` + `rule-card.md` 构造新 `CLAUDE.md` 骨架（保护区结构在新模板中保留），并把 `{{BUTLER_VERSION}}` 重戳为 `$BUTLER_PATH/VERSION` 当前版本。
3. **填入用户区**：将暂存的用户区内容原样填入新骨架的保护区位置。
4. **呈报升级清单给用户**：
   - **版本 gap**：旧戳 → 新版本（如 "v1.0.0 → v1.2.0"）。
   - butler 区变化项逐条列出（如 "rule-card 新增了 X 条执行纪律"、"深度阅读指针路径数量变化"）。
   - 用户区：原样保留，无变化。
5. **用户 ACK 后写入** `CLAUDE.md`。
6. **继续处理 `.ai/`**：进入 § 6。

## 6. `.ai/` 结构升级

按方案 ii（命名 + schema 字段补齐）执行：

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

## 7. 验证与回退

升级完成后，AI 应回顾并向用户报告：

- `CLAUDE.md` 含 `<!-- user-managed -->` / `<!-- /user-managed -->` 保护区标记完整；用户区内容逐字保留。
- `CLAUDE.md` 版本戳已更新到当前 butler 版本（与 `$BUTLER_PATH/VERSION` 一致）。
- `.ai/` 下无过时命名的文件。
- `local-constraints.md` 必填字段齐全（按最新 schema）。

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
- **版本号为辅、内容差异为主**：升级以文件内容差异为准绳；版本 gap（目标戳 vs 仓库 `VERSION`）仅作辅助提示与升级后重戳的依据，**不单凭版本号判定是否需要升级**——目标内容可能已手工漂移，版本号无法反映（见 `versioning-schema.md §7`）。
