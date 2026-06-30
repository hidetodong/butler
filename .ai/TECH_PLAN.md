# Goal

- 支撑 AC1–AC9：给 `artifact-style.md` 加"渐进展开 / 分层"原则，给 `concept-schema` 加"一句话"顶部块，并同步 rule-card / README，让 CONCEPT 对人和 AI 同时友好。

# Files / Modules to Change

- `Coder/20_Workflow_Lifecycle/artifact-style.md` —— 新增一节"渐进展开 / 分层"（五要点 + 分层骨架样例）。
- `Coder/20_Workflow_Lifecycle/concept-schema.md` —— §2 必填字段加"一句话"；§3 模板顶部加"一句话"块；§4 编写规则加一行（含与 Goal 分工、legacy 容忍）。
- `templates/rule-card.md` —— 产物书写节补 gist-first / 一行一意 / 不串层。
- `Coder/README.md` —— 更新 `artifact-style.md` 逐文件说明行，反映分层 / 渐进展开。

# Interface / Contract

- 无代码接口。文件间契约不变：四个 schema 仍指针引用 `artifact-style.md`（单一来源），本轮只扩充该单一来源的内容 + 给 CONCEPT 模板加一个向后兼容的新块。

# State / Boundary

- 只扩书写口径 + CONCEPT 模板的"一句话"块；不碰其它三件套字段、lifecycle 分流格式、对话层规则、hook。
- "一句话"是新增块、向后兼容：老 CONCEPT 无此块按 legacy 放行；hook 不看 CONCEPT 内部结构，无影响。

# Design Decisions

- 通用原则放 `artifact-style.md`（跨四件套都适用），CONCEPT 专属的"一句话"块放 `concept-schema`（它是 CONCEPT 的结构）——各归各层。
- "一句话"与 `Goal` 分工写清：一句话 = 散文意图速览（干嘛 + 为什么，给冷读者和 fresh-context AI 锚意图），Goal = 结构化目标项。防两者写重。
- 用"分层"吸收"人 vs AI"的唯一偏差：精度（路径 / 符号 / payload）单独成层，人不看也懂意图、AI 要用直接拿；不靠删精度来讨好人。
- 显式写"不啰嗦 ≠ 极限压缩"：上一轮的"反啰嗦"针对填充 / 重述，本轮要防它被误读成"再压一点"而加重"太挤"那种病。
- 分层骨架样例直接用 ultra-learning ITER-0016 的真实痛点（箭头链 G6、无 gist）做对照，可照抄。

# Execution Steps

1. 扩 `artifact-style.md`：加"渐进展开 / 分层"节 + 分层骨架样例。
2. 改 `concept-schema.md`：必填字段 + 模板块 + 编写规则。
3. 补 `rule-card.md` 产物书写节。
4. 更新 `README.md` 描述行。
5. P5 逐项验证 + 收口三步。

# Verification Plan

- 按 AC_LIST 的 Verification Method 逐项核对：读两份规则文件 + grep 接线点 + 通读本迭代 CONCEPT 自证 dogfood + 五约束自检。

# Risks / Open Questions

- 无 hook 强制，靠读取 + 遵守（同 ITER-0012，可接受）。
- "一句话" vs Goal 写重风险——用分工说明 + 样例兜底。
