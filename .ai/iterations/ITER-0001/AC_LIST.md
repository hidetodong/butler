# Goal
- 为 Delivery Summary 触发时刻新增对话层风格约束，同时保持文件层正式结构不变

# In Scope
- 在 `Coder/20_Workflow_Lifecycle/delivery-summary.md` 新增 §8 对话内人话摘要
- 在 `Coder/20_Workflow_Lifecycle/lifecycle.md` P5 Verify 段补一句对 §8 的引用
- 按 butler SOP 产出 `.ai/CONCEPT.md` / `.ai/AC_LIST.md` / `.ai/TECH_PLAN.md` / `.ai/VERIFY_REPORT.md`
- 本次交付生成 `deliveries/2026-04-20-chat-recap-style.md`，并按新 §8 给对话摘要（dogfood 首次应用）

# Out of Scope
- 不新建独立规则文件（如 `chat-recap.md`）
- 不改 `Coder/README.md` 目录结构与读取顺序
- 不改 `templates/rule-card.md` 浓缩规则卡
- 不改 `Coder/CLAUDE.md` 协作约定
- 不回溯 / 不迁移历史 `deliveries/*.md`
- 不下沉对话层风格到 P2 ACK / P3 ACK / 阶段 checkpoint

# Acceptance Checklist
- [ ] AC1: `delivery-summary.md` 出现 §8 节，子节覆盖：8.1 触发 / 8.2 形式 / 8.3 内容核心 / 8.4 收尾引用 / 8.5 与 §4 的关系
- [ ] AC2: §8.2 明确包含三条硬约束：3–6 句中文散文、禁止编号小节标题、禁止铺排长 bullet
- [ ] AC3: §8.3 列出三项必覆盖内容（做了什么 / 风险 / 下一步），对"无风险"场景显式写出"本轮无剩余风险"反模糊口径
- [ ] AC4: §8.4 给出固定引用格式 `正式版：deliveries/YYYY-MM-DD-<slug>.md`
- [ ] AC5: `lifecycle.md` P5 Verify 段出现对 `delivery-summary.md § 8` 的显式引用
- [ ] AC6: `Coder/README.md`、`templates/rule-card.md`、`Coder/CLAUDE.md`、目录结构、读取顺序均未改动
- [ ] AC7: 仅阅读 `delivery-summary.md` 单文件即可同时理解文件层（§2–§7）与对话层（§8）两种表达
- [ ] AC8: `.ai/CONCEPT.md` / `.ai/AC_LIST.md` / `.ai/TECH_PLAN.md` / `.ai/VERIFY_REPORT.md` 按对应 schema 全字段回填
- [ ] AC9: `deliveries/2026-04-20-chat-recap-style.md` 存在且结构符合 `delivery-summary.md §4`
- [ ] AC10: 本轮 P5 结束时，对话框内输出的收尾摘要符合新 §8 风格（首次 dogfood 验证）

# Verification Method
- AC1: grep `delivery-summary.md` 中 `## 8.`、`### 8.1`–`### 8.5` 子节标题
- AC2: grep `delivery-summary.md` 中关键词 `3–6 句`、`禁止输出任何编号小节标题`、`禁止铺排长 bullet`
- AC3: grep `delivery-summary.md` 中关键词 `本轮无剩余风险`，并人工确认三项内容核心均存在
- AC4: grep `delivery-summary.md` 中固定格式 `正式版：deliveries/YYYY-MM-DD-<slug>.md`
- AC5: grep `lifecycle.md` 中 `delivery-summary.md § 8`
- AC6: `git diff HEAD~N -- Coder/README.md templates/rule-card.md Coder/CLAUDE.md` 输出为空
- AC7: 人工通读 `delivery-summary.md`，确认自包含
- AC8: 人工对照各 schema §2 必填字段清单
- AC9: 人工对照 `delivery-summary.md §4` 七个小节
- AC10: 人工对照 §8.2 / §8.3 / §8.4 对本次收尾摘要逐项核查

# Open Questions / Risks
- 风险：AI 可能把"讲人话"误解为"可以省略风险声明"。已通过 AC3 反模糊口径兜底
- 风险：`delivery-summary.md` 从 7 节扩到 8 节，文件变长。若未来对话层约束继续增加（≥ 3 条），应评估拆分到独立文件
- 无未决问题
