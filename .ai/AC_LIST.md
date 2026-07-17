---
状态: ack-frozen
ACK 日期: 2026-07-17
---

# Goal

完成 MILE-0006 R1 的 Codex 兼容地基：让 Codex 原生发现 Butler 仓库规则、按固定顺序恢复 `.ai/` 状态，并建立可供后续 skills/plugin、hooks 和双入口部署复用的宿主适配契约；现有 Claude Code 行为保持不变。

# In Scope

- 在 Butler 仓根增加 Codex 原生 `AGENTS.md`，覆盖仓库定位、编辑约束、冷启动 `.ai/` 读序和完整规则入口。
- 增加目标项目 Codex 入口模板，结构与 `CLAUDE.md.template` 对齐，并继续以 `templates/rule-card.md` 的 `{{RULE_CARD_CONTENT}}` 为强制规则唯一来源。
- 增加双宿主兼容架构说明，明确共同内核、Claude 适配层、Codex 适配层及各自边界。
- 在 README、Coder 入口和人类指南中登记 Codex 当前可用范围与后续路线，明确 hooks 在 R3 前尚未 live 兼容。
- 保持 R1 边界：本迭代只交付规则发现和架构契约；skills/plugin、hook 运行时、完整部署升级接线分别留在 R2–R4。
- 按新增能力发布 v2.12.0，并明确本版对既有部署项目不自动增加 Codex 入口。

# Out of Scope

- 不创建 8 个 Codex skills，不建立最终 plugin 包或 marketplace 条目；归 R2。
- 不创建 `.codex/hooks.json`，不解析 `apply_patch`，不宣称 Codex 机械门禁已生效；归 R3。
- 不改 `scripts/setup.sh`、`mcv-deployment.md`、`butler-upgrade.md` 的完整双宿主安装/升级执行链；归 R4。
- 不改 `.ai/` 目录名、四件套 schema、P1–P5、PRD、危险模式和偏好探针算法。
- 不删除或改名 `CLAUDE.md`、`.claude/commands/`、`.claude/hooks/`。
- 不绕过 Codex sandbox、审批、hook trust 或管理策略。

# Acceptance Checklist

- [ ] **AC1（仓库原生发现）**：仓根存在 `AGENTS.md`；从 Butler 仓根启动 Codex 时无需用户级 fallback 即可发现。文件明确“这是规则仓，不是使用规则开发业务软件”，并列出不破坏分层、产物链、注册读序、模板单一来源与 frontmatter 标注等编辑约束。
- [ ] **AC2（`.ai/` 冷启动恢复）**：`AGENTS.md` 明确固定读序：`.ai/project/00_INDEX.md` → `.ai/MILESTONES.md` / `.ai/ITERATIONS.md` → `.ai/task-state.md` / `.ai/02_SESSION_HANDOFF.md` → 当前四件套 → 按指针钻 `Coder/`；同时明确 `.ai/` 是 Claude Code 与 Codex 共用状态层，不自动全量读取历史归档。
- [ ] **AC3（目标项目模板）**：新增 `templates/AGENTS.md.template`，具备版本戳、`{{RULE_CARD_CONTENT}}`、完整规则指针和 `<!-- user-managed -->` 保护区；强制规则内容不在模板中手写复制，模板占位契约与 `CLAUDE.md.template` 可机械核对。
- [ ] **AC4（双宿主架构契约）**：新增一份 Codex 兼容架构说明，清楚划分共同内核（`Coder/`、`.ai/`、`rule-card.md`、共享 hook 判断模块）、Claude 适配层（`CLAUDE.md` / `.claude/**`）和 Codex 适配层（`AGENTS.md` / skills/plugin / `.codex` hooks）；明确“入口薄壳、算法回共同真源”，禁止双写规则正文。
- [ ] **AC5（阶段边界诚实）**：架构说明和用户文档明确 R1 只完成规则发现；8 skills/plugin、Codex hooks、setup/部署/升级接线分别标为 R2/R3/R4。尤其注明现有 `butler_gate.py` 只识别 `Edit/Write/MultiEdit` 与 `file_path`，在 R3 前不得把 Codex `apply_patch` 宣称为已受机械门禁保护。
- [ ] **AC6（文档注册）**：`README.md`、`Coder/README.md`、`HUMAN_GUIDE.md` 以最小增量登记 Codex 支持现状、双宿主目标和入口路径；不把整份兼容架构重复抄入三处，详细内容统一回指 AC4 的真源文件。
- [ ] **AC7（Claude 非回归）**：`CLAUDE.md`、`.claude/commands/butler/*.md`、现有 Claude hook 配置与 Python 规则算法无行为变化；`templates/CLAUDE.md.template` 只有在修正两模板共同契约确有必要时才改，且须提供前后差异说明。
- [ ] **AC8（结构与内容自检）**：自动检查 `AGENTS.md` 和 `templates/AGENTS.md.template` 的必需章节/占位符/保护区；检查仓库不存在第二份手写规则卡；Markdown 链接与相对路径可解析；`git diff --check` 通过。
- [ ] **AC9（发布与台账）**：按 MINOR 发布 v2.12.0；`VERSION`、`CHANGELOG.md`、`migrations/v2.12.0.md` 和本地 tag 对齐。迁移配方诚实标注 R1 对既有部署项目为 `[no-op]` + `[restamp]`，目标项目双入口的实际部署/升级接线留待 R4，不伪装成本版已完成。

# Verification Method

- **AC1/AC2**：从仓根检查 Codex 指令发现结果；对 `AGENTS.md` 必需语句和冷启动顺序做文本断言。（auto·可靠 + 人读）
- **AC3**：脚本断言模板含版本、规则卡占位符、完整规则指针、双保护区标记；与 `CLAUDE.md.template` 比较共同占位契约。（auto·可靠）
- **AC4/AC5**：逐节核对架构说明的三层映射、单一真源红线、R1–R4 状态和 hook 诚实边界。（人读）
- **AC6**：搜索三份入口文档中的 Codex 注册项及回指；检查没有大段重复。（auto + 人读）
- **AC7**：`git diff -- CLAUDE.md .claude templates/hooks templates/settings.hooks-snippet.json`；若非空，逐行证明无行为变化。（auto·可靠）
- **AC8**：运行新增或现有结构测试、链接/路径检查、`git diff --check`。（auto·可靠）
- **AC9**：`cat VERSION`、CHANGELOG 顶条、migration 文件名/标题、本地 tag 四方核对。（auto·可靠）

# Open Questions / Risks

- **待 ACK 的边界确认**：R1 会新增目标项目 `AGENTS.md` 模板，但不会在本迭代改 setup、首次部署和既有升级执行链；真正让目标项目自动得到双入口在 R4 完成。
- **验证限制**：Codex 是否自动读取仓根 `AGENTS.md` 可在本仓验证；目标项目模板的完整部署行为要到 R4 做端到端验证，本轮只验证模板契约。
- **发布风险**：v2.12.0 是可独立使用的“仓库规则发现”增量，不应在发布说明中写成“Codex 全面兼容”；完整兼容以 MILE-0006 收口为准。
