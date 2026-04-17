# Goal

- 为 butler 新增**主动升级命令**：让已部署过 butler 的老项目能通过一条指令，把自己的 `CLAUDE.md` 与 `.ai/` 结构同步到当前 butler 仓库的最新模板与规则，同时保护项目特定内容不被覆盖。

# Current Understanding

- 本任务是 Butler 规则仓第九轮维护 —— 但性质是**新增 feature**（不在 audit 清单中），非 bug 修复。
- 用户痛点：butler 仓经过 v0.0.3 → v0.0.10 的大量变更，模板结构（CLAUDE.md.template 占位符）、`.ai/` 文件命名（02_SESSION_HANDOFF）、schema 新增（local-constraints-schema）等都与老部署项目脱节。手工同步成本高且易漏。
- 已定的 4 个核心决策：
  - **B**：升级范围 = `CLAUDE.md` + `.ai/` 结构（不涉及 `deliveries/` 历史）
  - **β**：不引入 butler 版本戳，靠差异检测
  - **x**：保护区标记（用户内容与 butler 内容用 HTML 注释边界分隔）
  - **r**：命令触发 = 显式 slash `/butler-upgrade` + 语义词（"升级 butler" / "同步到新版"）

# Constraints

- 显性约束：
  - 不破坏三层架构（SOP Core / Domain Profiles / Business Extension）。
  - 不破坏现行 `mcv-deployment.md` 的初次部署语义 —— 升级协议与部署协议并列而非替代。
  - 新规则文件必须在 `Coder/README.md` 注册；必须含 frontmatter（audience / scope）。
  - 保护用户项目特定约束内容，不被覆盖式升级吞掉。
- 隐性约束：
  - 升级过程应**可审阅、可 ACK**（列出变更清单给用户确认后再动），不得直接静默覆盖。
  - 老项目（无保护区标记）也要能升级，不能假设所有项目都是新规范。

# Impact Scope

预计新建/修改 5 个文件：
- **新建** `Coder/20_Workflow_Lifecycle/butler-upgrade.md`（升级协议，与 `mcv-deployment.md` / `mcv-update.md` 并列）
- **修改** `templates/CLAUDE.md.template`（引入 `<!-- butler-managed -->` / `<!-- /butler-managed -->` 保护区边界）
- **修改** `Coder/20_Workflow_Lifecycle/mcv-deployment.md § 3`（部署时生成保护区标记，建立升级契约的起点）
- **修改** `Coder/00_System_Prompt/logic-protocol.md § 4 Semantic Triggers`（注册 `/butler-upgrade` 命令与语义触发词）
- **修改** `Coder/README.md`（注册新文件 + 目录结构 + "其中："说明）

不影响：其他 schema、Extension、Domain Profiles、scripts、templates/rule-card.md（保持 SSOT 不动）。

# Project Type / Active Profiles

- 项目类型：Markdown 规则仓库。
- 未命中任何 Domain Profile。

# Open Questions

3 个细节设计需用户拍板（见 AC_LIST）：
- **U-1** 保护区标记的"覆盖方向"（butler 区显式标 vs 用户区显式标）
- **U-2** 老项目（无保护区标记）的首次升级策略
- **U-3** `.ai/` 结构升级的范围粒度
