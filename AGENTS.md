# Butler 规则仓库 — Codex 开发约定

## 仓库定位

这是一个 Markdown 规则仓库，定义 AI 辅助工程开发的通用协作 SOP。你正在编辑规则本身，不是在使用这套规则开发业务软件。完整规则入口是 `Coder/README.md`；按任务需要定向读取，不要一次吞下全部历史文档。

## 冷启动：先恢复 `.ai/` 状态

`.ai/` 是 Claude Code 与 Codex 共用的项目状态层。开始任务时按以下顺序恢复，不依赖对话记忆：

1. 读 `.ai/project/00_INDEX.md` 拿项目地图，再按任务钻相关主题。
2. 读 `.ai/MILESTONES.md`，确认当前里程碑。
3. 读 `.ai/ITERATIONS.md`，确认当前迭代和状态。
4. 读 `.ai/task-state.md`，恢复当前阶段。
5. 读 `.ai/02_SESSION_HANDOFF.md`，恢复会话断点。
6. 若存在活跃迭代，按当前阶段依次读取工作区四件套：
   - `.ai/CONCEPT.md`
   - `.ai/AC_LIST.md`
   - `.ai/TECH_PLAN.md`
   - `.ai/VERIFY_REPORT.md`
7. 最后按文件中的指针读取 `Coder/` 真源与相关代码。不要全量读取 `.ai/iterations/`、`.ai/milestones/` 或 `deliveries/` 历史归档。

## 编辑规则时的约束

1. **不破坏分层**：SOP Core（00/20/30/40）、Domain Profiles（10）、Business Extension（99）职责分明。
2. **不破坏产物链**：P1→CONCEPT → P2→AC_LIST → P3→TECH_PLAN → P5→VERIFY，每阶段从上一阶段文件读取。
3. **不引入隐式依赖**：新增规则文件必须在 `Coder/README.md` 的目录结构和读取顺序中注册。
4. **模板单一来源**：强制规则以 `templates/rule-card.md` 为唯一真源；宿主模板只保留 `{{RULE_CARD_CONTENT}}` 占位，不手工复制规则卡。
5. **保留标注**：规则正文文件的 frontmatter 必须标明 `audience` 与 `scope`；宿主入口和生成模板沿用各自既有格式。

## 双宿主边界

- `CLAUDE.md` / `.claude/**` 服务 Claude Code；`AGENTS.md` 服务 Codex。
- 两端共同回指 `Coder/`、`.ai/` 与 `templates/rule-card.md`，不得维护两套规则算法。
- Codex 的 8 skills/plugin、`apply_patch` hooks 与双入口部署已完成；项目级读写前两宿主都必须按 `mcv-deployment.md §0.1` 解析唯一 `PROJECT_ROOT`，不能仅凭会话 cwd。完整边界见 `docs/codex-compatibility.md`。

## 验证

- 修改 Codex 入口或模板后运行：`bash scripts/verify-codex-foundation.sh`。
- 修改 hook 共享逻辑后运行：`python3 -m pytest templates/hooks/tests -q`。
- 交付前运行：`git diff --check`，并确认没有混入无关变更。
