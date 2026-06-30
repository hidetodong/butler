---
状态: ack-frozen
ACK 日期: 2026-06-30
---

# Goal

- 给四件套补"分层 / 渐进展开"写法（重点 CONCEPT），让同一份文档对人和 AI 同时友好；不推翻 ITER-0012。

# In Scope

- `artifact-style.md` 加一节"渐进展开 / 分层"原则 + 一个分层骨架样例。
- `concept-schema.md` 模板顶部加"一句话"gist 块，列入必填字段 + 编写规则（完整路径必填、简化路径可选、legacy 容忍）。
- `templates/rule-card.md` 产物书写节补 gist-first / 一行一意 / 不串层。
- `Coder/README.md` 更新 artifact-style 描述行，反映分层 / 渐进展开。

# Out of Scope

- 不改其它三件套字段结构（TECH_PLAN 的 gist 留将来）。
- 不改 lifecycle、对话层规则（presentation-protocol、delivery-summary §8）、hook 体系。
- 不回填 / 重写历史产物。
- 本轮不切版，累积到下次发布（预计 MINOR）。

# Acceptance Checklist

- [ ] AC1: `artifact-style.md` 新增"渐进展开 / 分层"节，含五要点：①顶部一句话 gist（意图先行）②一行一个意思、拆箭头链（多步列成步骤）③承重引用首次出现给一句话解释（含项目领域符号 / 文件 / 表，不止 butler 黑话）④不串层（散文层不夹密集符号、精度层用干净引用列表）⑤"不啰嗦 ≠ 极限压缩"。
- [ ] AC2: 该节给一个分层 CONCEPT 骨架样例（一句话 → 结构化目标 → 精确引用 三层），可照抄。
- [ ] AC3: `concept-schema.md` §3 模板顶部加"一句话"块；§2 必填字段纳入；§4 编写规则加一行（2-3 句白话、写清干嘛 + 为什么、与 Goal 分工：一句话是散文意图速览、Goal 是结构化目标项）。
- [ ] AC4: AC3 的"一句话"块写明完整路径必填、简化路径可选、老 CONCEPT 无此块按 legacy 放行（向后兼容）。
- [ ] AC5: `templates/rule-card.md` 产物书写节补充 gist-first / 一行一意 / 不串层，与新文件正文口径一致。
- [ ] AC6: `Coder/README.md` 中 `artifact-style.md` 描述行更新，反映分层 / 渐进展开。
- [ ] AC7: 与 ITER-0012 无冲突——新内容是叠加扩展、不推翻 §2 / §3；"不啰嗦 ≠ 极限压缩"已显式化解潜在误读（grep 确认该句在位）。
- [ ] AC8: 本迭代 CONCEPT 自己按新结构写（顶部有"一句话"、分层、一行一意），作为 dogfood 证据。
- [ ] AC9: 本仓 CLAUDE.md 五约束自检通过。

# Verification Method

- AC1 / AC2: 读 `artifact-style.md` 核对新节五要点齐全 + 骨架样例在位。
- AC3 / AC4: 读 `concept-schema.md` 核对模板加块、必填字段、编写规则、legacy 说明。
- AC5: grep `rule-card.md` 命中新口径；比对措辞一致。
- AC6: grep `Coder/README.md` artifact-style 描述行含分层 / 渐进展开。
- AC7: grep "不啰嗦"/"极限压缩"在 `artifact-style.md` 命中；通读确认未删改 §2 / §3。
- AC8: 通读本迭代 CONCEPT，确认顶部"一句话"+ 分层 + 一行一意。
- AC9: 对照本仓 CLAUDE.md 五条逐项自检，写进 VERIFY 的 Gate Coverage。

# Open Questions / Risks

- 风险：分层 / gist 靠会话起始读取 + 遵守，无 hook 强制——同 ITER-0012，可接受。
- 风险："一句话"与 Goal 可能被写重——用"散文意图速览 vs 结构化目标项"的分工说明区分。
