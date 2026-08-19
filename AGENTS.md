# Butler 规则仓库 — Codex 开发约定

## 仓库定位

这是一个 Markdown 规则仓库，定义 AI 辅助工程开发的通用协作 SOP。你正在编辑规则本身，不是在使用这套规则开发业务软件。完整规则入口是 `Coder/README.md`；按任务需要定向读取，不要一次吞下全部历史文档。

## 冷启动：先恢复 `.ai/` 状态

`.ai/` 是 Claude Code 与 Codex 共用的项目状态层。下面这段是 `Coder/40_Context_Management/context-persistence.md §6` 的字节投影，改它要改真源：

<!-- butler-context-order:begin -->
冷启动 / clean-slate 重启时按下列五步恢复上下文，不依赖对话记忆；每步读完即停，不顺着引用递归展开。

1. **欠债与边界** —— 读 `.ai/debt.md`：还悬着什么账、哪些边界不能碰。
2. **时间线** —— 只读 `.ai/MILESTONES.md` 与 `.ai/ITERATIONS.md` 的热表；需要旧身份时先跑 state-ledger `check`，再沿 `.ai/state-index.json` 用 `lookup` 定向读命中的那一个冷分片，禁止默认读取整个 `.ai/history/`。
3. **断点** —— 先跑 `$BUTLER_PATH/tools/handoff/handoff.py check`：`fresh` 才读 `.ai/02_SESSION_HANDOFF.md`，`stale` 先 `sync` 重建后再读，`error` 先修权威状态；handoff 的性质与 sync 时机见规则卡「强制工作流」。
4. **Goal 状态** —— 读 `.ai/task-state.md` 的 Goal Calibration、当前 `.ai/TECH_PLAN.md` 的方案状态与 `.ai/VERIFY_REPORT.md` 的 Completion Inputs，重算 state / reason / next；宿主原生 Goal 只是可重建投影。
5. **产物与代码** —— 按前四步给出的指针钻取工作区四件套、`Coder/` 真源与代码；不全量读取 `.ai/iterations/`、`.ai/milestones/` 或 `deliveries/` 历史归档。
<!-- butler-context-order:end -->

### 核心概念渐进读取（L0）

<!-- butler-context-l0:begin -->
- 普通单模块任务：停在本入口，直接读取目标专项规则；不得默认加载领域地图。
- 已知术语需要消歧：只查 `domain-glossary.md` 的相关行，再读取首批最多 3 份直接真源。
- 涉及跨模块所有权、同名状态、真源冲突或新增核心术语：先读 `domain-model.md` 定位上下文，再按需查术语和真源。
- 3 份是每批预算而非总上限；续批前先压缩已知结论，并公开记录问题、缺口、已读来源、下一批来源与选择理由。
- 只有显式完整领域审查才进入历史证据层；任何路径都不得递归追随引用或整目录读取。
<!-- butler-context-l0:end -->

## 编辑规则时的约束

1. **不破坏分层**：SOP Core（00/20/30/40）、Domain Profiles（10）、Business Extension（99）职责分明。
2. **不破坏产物链**：P1→CONCEPT → P2→AC_LIST → P3→TECH_PLAN → P5→VERIFY，每阶段从上一阶段文件读取。
3. **不引入隐式依赖**：新增规则文件必须在 `Coder/README.md` 的目录结构和读取顺序中注册。
4. **模板单一来源**：强制规则以 `templates/rule-card.md` 为唯一真源；宿主模板只保留 `{{RULE_CARD_CONTENT}}` 占位，不手工复制规则卡。
5. **保留标注**：规则正文文件的 frontmatter 必须标明 `audience` 与 `scope`；宿主入口和生成模板沿用各自既有格式。

## 双宿主边界

- `CLAUDE.md` / `.claude/**` 服务 Claude Code；`AGENTS.md` 服务 Codex。
- 两端共同回指 `Coder/`、`.ai/` 与 `templates/rule-card.md`，不得维护两套规则算法。
- Codex 的 11 skills/plugin、`apply_patch` hooks 与双入口部署已完成；项目级读写前两宿主都必须按 `mcv-deployment.md §0.1` 解析唯一 `PROJECT_ROOT`，不能仅凭会话 cwd。完整边界见 `docs/codex-compatibility.md`。

## 验证

- 交付前完整验证统一运行：`bash scripts/verify-ci.sh`。
- 修改 Codex 入口或模板后运行：`bash scripts/verify-codex-foundation.sh`。
- 修改 hook 共享逻辑后运行：`python3 -m pytest templates/hooks/tests -q`。
- 交付前运行：`git diff --check`，并确认没有混入无关变更。
