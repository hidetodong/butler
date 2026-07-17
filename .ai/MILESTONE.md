# MILESTONE — MILE-0006 · Codex 双宿主兼容层

> 方向性产物（非冻结、不走 ACK）。目标不是把 Butler 从 Claude Code 迁走，而是在保持现有 Claude Code 能力的同时，增加一套 Codex 原生入口；`.ai/` 与 `Coder/` 继续作为两端共同的状态层和规则真源。

## 5.1 范围评估

**In Scope（版本级）**

- **规则自动注入**：增加 Codex 原生 `AGENTS.md` 入口，明确冷启动读序、`.ai/` 状态恢复和深度规则指针；保留现有 `CLAUDE.md`。
- **命令工作流迁移**：把现有 8 个 `/butler:*` 薄壳命令映射为 Codex skills，并评估以 Codex plugin 作为全局分发单位，避免使用已弃用的 custom prompts。
- **Hook 机械门禁**：增加 `.codex/hooks.json` / plugin hook 入口；适配 Codex `apply_patch` 的工具名与 patch 输入，同时复用现有 Python 规则模块。
- **部署与升级双宿主化**：让新项目部署、既有项目升级和全局 setup 能分别生成/维护 Claude Code 与 Codex 所需入口，不复制 `Coder/` 规则正文。
- **兼容性验证**：建立 Claude Code / Codex 两列验证矩阵，覆盖规则发现、`.ai/` 恢复、8 个工作流、PreToolUse 拒绝、PostToolUse 提醒与子 agent 独立复核。

**Out of Scope（版本级）**

- 不重写 P1–P5、迭代、里程碑、PRD、危险模式等规则算法。
- 不改 `.ai/` 目录名和既有产物 schema；`.ai/` 是宿主无关的共同状态层。
- 不让 Butler 文本规则绕过 Codex 的 sandbox、审批、hook trust 或企业策略。
- 不删除 Claude Code 的 `CLAUDE.md`、`.claude/commands/`、`.claude/hooks/` 支持。
- 首版不发布公共 marketplace，不承诺 Codex Cloud、IDE、桌面端以外所有宿主的完全一致行为。

**关键交付目标**

- 同一份 Butler 规则仓可在 Claude Code 与 Codex 中自动发现并恢复 `.ai/` 状态。
- 8 个 Butler 工作流在 Codex 中可显式/语义触发，规则正文仍以 `Coder/` 为真源。
- Codex 写文件时，阶段门禁和提醒不再因 `apply_patch` 输入差异而静默失效。
- 双宿主安装、升级、验证步骤有机器可执行的检查和人类可读说明。

## 5.2 理解阐释

- **核心问题**：Butler 的业务规则本身是 Markdown，宿主无关；真正绑定 Claude Code 的是自动发现、slash command、hook 输入协议、权限配置和安装路径。若只让 Codex“能读 Markdown”，规则看似兼容，但自动注入、机械门禁和全局命令都会缺失。
- **兼容策略**：保留共同内核，增加宿主适配层。共同内核包括 `Coder/`、`.ai/`、`templates/rule-card.md` 与 Python 规则判断；Claude 适配层继续放 `.claude/`，Codex 适配层使用 `AGENTS.md`、skills/plugin、`.codex/`。
- **最大风险**：出现两套规则正文并逐渐漂移。因此 Codex 文件只能做入口、路由和协议适配，不能复制规则算法；双宿主共用的逻辑应下沉到现有真源或共享 Python 模块。
- **已确认事实**：Codex 当前支持 `AGENTS.md`、repo skills、plugins、PreToolUse/PostToolUse hooks 与多 agent；matcher 可用 `Edit|Write` 命中 `apply_patch`，但现有 gate 内部仍只接受 `Edit/Write/MultiEdit` 和 `file_path`，必须显式适配。

## 5.3 拆分路线图

预计跨度：ITER-0051 ~ ITER-0054（方向性，真实编号以台账为准）

| 路线项 | 主题 / 范围切片 | 实际 ITER | 状态 |
|---|---|---|---|
| R1 | **兼容地基**：双宿主边界、`AGENTS.md` 自动注入入口、`.ai/` 共同状态层与单一真源约束 | ITER-0051 | closed |
| R2 | **Codex 工作流入口**：把 8 个薄壳命令迁为 skills，落本地 plugin 骨架与全局安装路径 | ITER-0052 | closed |
| R3 | **Codex hooks**：`.codex`/plugin hook 配置、`apply_patch` 输入适配、拒绝与提醒端到端测试 | ITER-0053 | closed |
| R4 | **部署升级与收官**：setup / MCV / migrations / HUMAN_GUIDE 双宿主化，跑 Claude+Codex 回归矩阵并收里程碑 | — | planned |

## 5.4 范围演进记录

- 2026-07-17：用户要求从现有 Butler 台账继续，改造为 Codex 可用；确认无活跃里程碑/迭代后开启 MILE-0006，并以双宿主兼容而非替换 Claude Code 为方向。
- 2026-07-17：用户确认四项默认——plugin 为最终分发面、按 R1–R4 四迭代推进、目标项目最终双入口、继续一迭代一版。R1 收紧为规则发现 + 模板/架构契约；完整部署升级接线仍归 R4。
- 2026-07-17：R1 / ITER-0051 收口并发布 v2.12.0。仓库已可被 Codex 原生发现；目标项目自动部署、skills/plugin 与 hooks 仍按 R2–R4 继续，MILE-0006 保持 active。
- 2026-07-17：用户开启危险模式并要求继续；R2 绑定 ITER-0052，按会话级自治推进 8 skills、plugin 骨架和本地安装验证，R3/R4 边界不变。
- 2026-07-17：R2 / ITER-0052 自治收口并发布 v2.13.0；个人 `butler@personal` 已真实安装，8 skills 可用。危险模式继续推进 R3。
- 2026-07-17：危险模式自动开启 R3 / ITER-0053；以 plugin 默认 hooks 发现 + 共享 Python dispatcher 适配为主线，R4 边界不变。
- 2026-07-17：R3 / ITER-0053 完整强审 0 Must Fix；124 tests 与真实 Codex phase/protected deny、allow、advisor 全通过，发布 v2.14.0。危险模式继续进入 R4。
