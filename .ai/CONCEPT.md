# Goal
- 为 Delivery Summary 触发时刻定义对话层风格约束，让 AI 在对话框内给出 3–6 句人话摘要，`deliveries/` 文件层仍按正式结构产出

# Current Understanding
- 现状：`Coder/20_Workflow_Lifecycle/delivery-summary.md` 仅规定 `deliveries/*.md` 的 7 小节文件结构，未约束对话层表达
- AI 倾向于把文件结构原样复述到对话，输出冗长、官方、缺乏判断
- 预期产出：在 `delivery-summary.md` 新增 §8 定义对话层风格；在 `lifecycle.md` P5 段补引用；同时产出 butler SOP 所需的 `.ai/` 决策记录与 `deliveries/` 交付总结

# Constraints
- 显性约束：
  - 不新增规则文件，不改目录结构与读取顺序
  - 不改 Delivery Summary 触发条件（§2 沿用）
  - 不改文件层最小结构（§4 沿用）
  - 不回溯历史 deliveries
- 隐性约束：
  - 对话层规则必须自包含，仅读 `delivery-summary.md` 就能理解两种表达
  - 反模糊口径必须显式（无风险时不得用"一切顺利"替代）

# Impact Scope
- 影响：`Coder/20_Workflow_Lifecycle/delivery-summary.md`、`Coder/20_Workflow_Lifecycle/lifecycle.md`、`.ai/*.md`、`deliveries/2026-04-20-chat-recap-style.md`
- 不影响：`Coder/README.md`、`templates/rule-card.md`、`Coder/CLAUDE.md`、其他 schema、hook 配置

# Project Type / Active Profiles
- 项目类型：Markdown 规则仓库（butler 自身）
- 未命中任何 `10_Domain_Stack_Profiles/` profile，仅按通用 SOP 推进

# Open Questions
- 无未决问题（需求边界已在 brainstorming 阶段全部澄清）
