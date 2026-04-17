# Butler 规则仓库 — 开发约定

## 仓库定位

这是一个 Markdown 规则仓库，定义 AI 辅助工程开发的通用协作 SOP。你正在编辑规则本身，不是在用规则开发软件。

## 目录结构与职责

- `Coder/` — 工程开发与 AI 协作规则体系（核心）
- `Learner/` — 学习事务管理
- `Composer/` — 杂项事务
- `HUMAN_GUIDE.md` — 面向人类用户的操作手册
- `templates/` — 目标项目使用的 CLAUDE.md 模板、浓缩规则卡与 hook 体系（`hooks/`、`settings.hooks-snippet.json`）

## 编辑规则时的约束

1. **不破坏分层**：SOP Core（00/20/30/40）、Domain Profiles（10）、Business Extension（99）三层职责分明，不要把某一层的内容混入另一层。
2. **不破坏产物链**：P1→CONCEPT.md → P2→AC_LIST.md → P3→TECH_PLAN.md → P5→VERIFY_REPORT.md，每个阶段从上一阶段的文件读取，不依赖对话记忆。
3. **不引入隐式依赖**：新增规则文件时必须在 `Coder/README.md` 的目录结构和读取顺序中注册。
4. **模板单一来源**：浓缩规则的 SSOT 是 `templates/rule-card.md`；`templates/CLAUDE.md.template` 通过 `{{RULE_CARD_CONTENT}}` 占位符引用 rule-card，无需手工双写。修改强制约束只需更新 `templates/rule-card.md`。
5. **audience 标注**：每个规则文件的 frontmatter 必须标明 audience（AI / 开发者）和 scope。

## 写作风格

- 规则面向 AI 执行，措辞用"必须"/"不得"/"应"，避免模糊的"建议"/"可以考虑"。
- 中文说明，标识符和文件名用英文。
- 规则之间通过文件名互相引用，不写绝对路径。
