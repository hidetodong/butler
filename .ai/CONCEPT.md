> 分流: 完整 | 命中升级信号: 多文件改动、跨模块影响、宿主契约变更、设计取舍 | 2026-07-17

# 一句话

为 Butler 增加 Codex 兼容地基：先让 Codex 原生发现规则、正确恢复 `.ai/` 状态，并定死双宿主共享真源与适配层边界，为后续 skills/plugin 和 hooks 改造铺路。

# Goal

承接 MILE-0006 R1，在不破坏现有 Claude Code 使用方式的前提下，让 Codex 打开 Butler 仓或已部署项目时能自动获得正确入口：知道 `.ai/` 是状态层、按固定顺序恢复当前任务、按需读取 `Coder/` 真源；同时把后续 command→skill、Claude hook→Codex hook 的适配边界写清，避免两套规则正文。

# Current Understanding

- `.ai/` 本身没有 Claude Code 专属协议：它是普通 Markdown 状态目录，Codex 可以直接读写，现有四件套、迭代归档、里程碑、知识文件夹和 handoff 均可复用。
- 当前自动注入链只覆盖 Claude Code：仓根和目标项目生成的是 `CLAUDE.md`，全局 setup 写 `~/.claude/CLAUDE.md`；Codex 默认入口是 `AGENTS.md`。
- 直接把 `CLAUDE.md` 加进 Codex fallback 可以临时工作，但属于用户机器配置，不能保证团队或新环境开箱即用；仓库应提供原生 `AGENTS.md`。
- `templates/rule-card.md` 是浓缩强制规则唯一真源。新增 Codex 模板时也必须从它生成/引用，不能手工复制一份规则卡长期维护。
- Codex 工作流更适合 skills/plugin，而不是照搬 `.claude/commands/`。这属于后续 R2，本迭代只立契约和入口，不一次性吞掉分发改造。
- Codex hooks 的事件结构与 Claude 接近，但 discovery 路径、trust 流程和写文件工具输入不同。现有 gate 对 Codex `apply_patch` 会静默放行的风险属于 R3，本迭代登记但不假装已修。

# Constraints

- 保留 `CLAUDE.md` 与 `.claude/**`，不做单向迁移或破坏性改名。
- `Coder/`、`.ai/`、`templates/rule-card.md` 继续是共同真源；Codex 入口只能路由和解释宿主差异。
- `AGENTS.md` 保持短小，关键规则内联到高注意力入口，但完整算法通过相对路径按需读取，避免超过 Codex 默认项目指令预算。
- 不在 R1 落公共 plugin、不发布 marketplace、不改现有 hook Python 判断算法。
- 不声称 hooks 已兼容；在 R3 端到端验证前，文档必须明确当前机械门禁只对 Claude Code live。
- 当前基线已从本地 v2.10.0 快进到 `github/main` v2.11.0；后续改动基于独立分支 `feat/mile-0006-codex-compatibility`。

# Impact Scope

- **R1 预计新增**：根 `AGENTS.md`、Codex 兼容架构/维护说明，以及目标项目 `AGENTS.md` 模板或生成约定（具体文件名在 P2/P3 冻结）。
- **R1 预计更新**：`README.md`、`Coder/README.md`、`HUMAN_GUIDE.md`、部署/升级规则中关于规则入口与双宿主边界的最小说明；`.ai/project/` 长期知识在收口时前滚。
- **后续迭代而非 R1**：`.agents/skills` 或 plugin 目录、`.codex/hooks.json`、`apply_patch` 解析器、setup 安装逻辑、迁移配方与完整 E2E。
- **明确不碰**：P1–P5 算法、四件套字段、PRD 版本化、危险模式算法、业务扩展和技术栈 profile。

# Project Type / Active Profiles

Markdown 规则仓库 + Python hook 测试 + Shell 安装脚本。无前端技术栈 profile；采用通用 SOP、文档规则、hook 测试与跨宿主配置验证。

# Open Questions

- 无。2026-07-17 用户已确认四项默认：plugin 为最终分发面、四迭代拆分、目标项目最终双入口、一迭代一版。

# Confirmed Decisions

1. Codex plugin 是最终全局安装面；repo skills 是开发态源码和 fallback。
2. MILE-0006 按 R1–R4 四迭代推进，R1 不提前实现 skills/plugin 与 hooks。
3. R4 完成后，新部署项目同时生成 `CLAUDE.md` 与 `AGENTS.md`，两者共同引用 `rule-card.md` 真源；R1 先建立模板和契约，不提前改完整部署链。
4. 延续一迭代一版；R1 按新增 Codex 原生发现能力发布 v2.12.0。
