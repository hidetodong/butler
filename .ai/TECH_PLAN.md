# Goal

- 按 U-1: 2 / U-2: b / U-3: ii 方案落地 `/butler-upgrade` feature：新建升级协议、引入 `<!-- user-managed -->` 保护区标记、注册命令触发、README 注册。

# Files / Modules to Change

| # | 文件 | 动作 | 改动点 |
|---|---|---|---|
| 1 | `Coder/20_Workflow_Lifecycle/butler-upgrade.md` | Write（新建） | 完整协议文件（frontmatter + 8 段） |
| 2 | `templates/CLAUDE.md.template` | Edit | 1（项目特定约束段用 user-managed 包裹） |
| 3 | `Coder/20_Workflow_Lifecycle/mcv-deployment.md § 3` | Edit | 1（第 4 步措辞加保护区标记） |
| 4 | `Coder/00_System_Prompt/logic-protocol.md § 4` | Edit | 1（注册 /butler-upgrade 触发） |
| 5 | `Coder/README.md` | Edit | 2（目录结构 + "其中："说明） |

共 5 个文件，6 处改动（1 new + 5 edit）。

# Interface / Contract

- **新命令契约**：`/butler-upgrade` + 语义词（"升级 butler" / "同步到新版" / "同步 butler 规则"）触发升级协议。
- **保护区契约**：`<!-- user-managed -->` 到 `<!-- /user-managed -->` 之间的内容由用户管理，butler 升级流程**永不触碰**；标记外的所有内容由 butler 管理，升级时按最新模板覆盖。
- **升级协议与部署协议并列关系**：`butler-upgrade.md` 与 `mcv-deployment.md` / `mcv-update.md` 同级，共同构成基地车的"生命周期三阶段"（部署 / 升级 / 维护）。
- **向下兼容**：老项目（无保护区标记）通过 § 4 首次升级流程（备份 + 交互 ACK）自动迁移，不留遗留负担。
- **决策记录**：B（升级范围）/ β（不版本化）/ x（保护区）/ r（命令+语义）已在 CONCEPT 固化，TECH_PLAN 不重新讨论。

# State / Boundary

- 不改：`rule-card.md`（保持 SSOT）、其他 schema 文件、Extension、scripts、`mcv-update.md`（它是 `.ai/` 内部维护，非跨版本升级）。
- 本轮**不**对 butler 仓库自身的 `CLAUDE.md`（butler 项目根）加保护区标记 —— butler 自身演进通过 audit 流程管理，不走 butler-upgrade 协议（避免自指复杂度；作为 follow-up 可单独做）。
- 不实现自动 rollback；回退靠 git + 备份文件。

# Design Decisions

1. **协议文件位置**：`Coder/20_Workflow_Lifecycle/butler-upgrade.md`（与 mcv-deployment / mcv-update 同目录，构成"基地车协议族"）。
2. **保护区标记格式**：HTML 注释（`<!-- user-managed -->` / `<!-- /user-managed -->`），原因：
   - Markdown 渲染时不可见
   - AI 可靠识别（字符串匹配即可）
   - 与现有 templates 顶部注释风格一致
3. **保护区包裹范围**：`## 项目特定约束` 整个章节（含标题、所有 placeholder 注释、用户自由填的内容）。这让用户加任何内容只要放在保护区内都安全。
4. **首次升级策略（老项目）**：不自动猜测，永远走备份 + 交互 ACK；升级后新 `CLAUDE.md` 自带标记，后续走常规路径。
5. **`.ai/` 升级范围**：命名（文件 rename）+ schema 必填字段补齐；不动 CHANGELOG / BUG_LOG 累积数据；不动任务产物（CONCEPT / AC_LIST / TECH_PLAN / VERIFY_REPORT）。
6. **注册到 Semantic Triggers**：虽然 butler-upgrade 是一次性动作而非持久"Mode"，但用户触发方式与其他扩展一致（命令 + 语义词），统一在 `logic-protocol § 4` 注册，保持入口一致性。

# Execution Steps

## Step 1 — Write `Coder/20_Workflow_Lifecycle/butler-upgrade.md`

新文件，8 段结构：

- frontmatter（title / audience / scope）
- § 1 目标
- § 2 触发条件（命令 + 语义词 + 不主动推断原则）
- § 3 侦察（读 CLAUDE.md 判断有无保护区标记；扫 `.ai/` 结构；读 butler 仓最新状态）
- § 4 首次升级（老项目无保护区标记）— 备份 + 生成新草稿 + 差异列表 + 用户 ACK + 写入
- § 5 常规升级（有保护区标记）— 读 user-managed 区暂存 + 生成新框架 + 填入用户区 + ACK + 写入
- § 6 `.ai/` 结构升级 — 命名升级 + schema 字段补齐；CHANGELOG / BUG_LOG 不动
- § 7 验证与回退 — 检查保护区标记完整、用户区无丢失、`.ai/` 无过时命名；回退靠备份 + git
- § 8 边界说明 — 不负责 deliveries 迁移、butler 自身升级、版本戳引入

## Step 2 — Edit `templates/CLAUDE.md.template`

在 `## 项目特定约束` 段上下加入 `<!-- user-managed -->` / `<!-- /user-managed -->` 包裹。

**old**（模板末尾）:
```
## 项目特定约束

<!-- 在这里补充本项目的特定约束，例如：-->
<!-- - 本项目使用 Vue 3 + TypeScript，启用对应 Domain Profile -->
<!-- - 本项目的 API 文档在 Confluence: https://... -->
<!-- - /legacy 目录下的旧代码允许局部放宽类型检查 -->
```

**new**:
```
<!-- user-managed -->

## 项目特定约束

<!-- 在这里补充本项目的特定约束，例如：-->
<!-- - 本项目使用 Vue 3 + TypeScript，启用对应 Domain Profile -->
<!-- - 本项目的 API 文档在 Confluence: https://... -->
<!-- - /legacy 目录下的旧代码允许局部放宽类型检查 -->

<!-- /user-managed -->
```

注：`<!-- user-managed -->` 与 `<!-- /user-managed -->` 之间的空行是刻意保留，让 markdown 渲染干净。

## Step 3 — Edit `mcv-deployment.md § 3`

第 4 步措辞更新，明确部署时建立保护区标记。

**old**:
```
4. 在"项目特定约束"段填入侦察结果（识别到的技术栈、project 类型、特殊约束等）。
```

**new**:
```
4. 在 `<!-- user-managed -->` 保护区内的"项目特定约束"段填入侦察结果（识别到的技术栈、project 类型、特殊约束等）。保护区标记由 `CLAUDE.md.template` 骨架提供，部署时原样保留，作为后续 `butler-upgrade.md` 协议的升级契约起点。
```

## Step 4 — Edit `logic-protocol.md § 4`

在 Review Mode 条目后插入 Butler Upgrade 触发。

**old**（§ 4 最后一条 Review Mode）:
```
- **Review Mode (`/review`)**: 激活 `60_Extension_CodeReview/review-engine.md`。当用户提到"看看写得怎么样"、"有没有坑"、"评价一下"、"代码审查"或输入 `/review` 时开启。P5 交付阶段默认触发简要自评（用户明确跳过时除外）。
```

**new**（在 Review Mode 之后加一条）:
```
- **Review Mode (`/review`)**: 激活 `60_Extension_CodeReview/review-engine.md`。当用户提到"看看写得怎么样"、"有没有坑"、"评价一下"、"代码审查"或输入 `/review` 时开启。P5 交付阶段默认触发简要自评（用户明确跳过时除外）。
- **Butler Upgrade (`/butler-upgrade`)**: 激活 `20_Workflow_Lifecycle/butler-upgrade.md`，把已部署项目的 `CLAUDE.md` 与 `.ai/` 结构同步到当前 butler 仓库最新版。当用户提到"升级 butler"、"同步到新版"、"同步 butler 规则"或输入 `/butler-upgrade` 时开启。非持久 Mode，执行一次后返回 Standard Mode。
```

## Step 5 — Edit `Coder/README.md` 目录结构

在 `/20_Workflow_Lifecycle` 目录下 `mcv-update.md` 后加入 `butler-upgrade.md`。

**old**:
```
    mcv-deployment.md
    mcv-update.md
    maintenance-boundaries.md
```

**new**:
```
    mcv-deployment.md
    mcv-update.md
    butler-upgrade.md
    maintenance-boundaries.md
```

## Step 6 — Edit `Coder/README.md` "其中："说明

在 mcv-update.md 说明之后加一行 butler-upgrade.md 说明。

**old**:
```
- `20_Workflow_Lifecycle/mcv-update.md` 负责基地车维护文件的升级迁移协议。
- `20_Workflow_Lifecycle/maintenance-boundaries.md` 负责维护成本与批处理边界。
```

**new**:
```
- `20_Workflow_Lifecycle/mcv-update.md` 负责基地车维护文件的升级迁移协议。
- `20_Workflow_Lifecycle/butler-upgrade.md` 负责已部署项目到当前 butler 仓库最新版的主动升级协议（`/butler-upgrade`）。
- `20_Workflow_Lifecycle/maintenance-boundaries.md` 负责维护成本与批处理边界。
```

# Verification Plan

- **新文件**：`ls Coder/20_Workflow_Lifecycle/butler-upgrade.md` 存在；`grep -c '^## [0-9]\.' butler-upgrade.md` >= 8（8 段结构）；`grep -c '^---$' butler-upgrade.md` = 2（frontmatter）。
- **保护区标记**：
  - `grep -c 'user-managed' templates/CLAUDE.md.template` = 2（开闭两次）。
  - `grep -n 'user-managed' mcv-deployment.md` 命中 § 3 第 4 步。
- **命令注册**：
  - `grep -n 'Butler Upgrade\|butler-upgrade' Coder/00_System_Prompt/logic-protocol.md` 命中 § 4。
  - `grep -n '升级 butler\|同步到新版' logic-protocol.md` 命中语义触发词。
- **README 注册**：
  - `grep -n 'butler-upgrade' Coder/README.md` 命中 2 处（目录结构 + 说明）。
- **整体一致性**：通读新 `butler-upgrade.md` 与 `mcv-deployment.md § 3` + `mcv-update.md`，三者在基地车生命周期角色边界上无矛盾（部署 / 升级 / 维护分工清晰）。

# Risks / Open Questions

- **风险 1**：保护区标记识别依赖字符串精确匹配，若用户误改了标记（如写成 `<!--user-managed-->` 无空格、或中文标点），升级流程可能误判。缓解：§ 3 侦察阶段 AI 做容错识别（tolerate whitespace / case variations），但若完全不认识，退化为 § 4 首次升级流程。本风险记录在 `butler-upgrade.md § 7 验证与回退` 的边界说明中。
- **风险 2**：本 feature 不处理 butler 仓自身的 `CLAUDE.md`（butler 项目根，非目标项目部署）。follow-up：下次可选择在 `CLAUDE.md`（仓根）也引入保护区标记，但**现在不做**，避免本轮范围膨胀。
- **风险 3**：升级协议本身还没有 dogfooding 过 —— 第一次实际跑是在有老项目需要升级时。缓解：规则本身按最清晰文档化标准写，减少首次执行的歧义。
- **开放问题**：无。
