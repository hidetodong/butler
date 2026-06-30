---
状态: ack-frozen
ACK 日期: 2026-06-30
---

> 补领入账：本迭代内容已先行实现于工作树，受用户监督决定正式归档为 ITER-0015；ACK 由用户「补领正式入账」指令授予，非危险模式自审。

# Goal

- 把 handoff 格式契约从「只有字段」补全到「字段 + 骨架 + 生成流程」，让 `02_SESSION_HANDOFF.md` 结构可复现、蒸馏可照做。

# Constraints

- 不改 §3 必填字段表语义、不改四件套字段、不碰 hook、frontmatter scope 不变。
- 不与 context-persistence 的「何时写 / 写什么 / 写到哪」职责重叠。

# Acceptance Checklist

- [x] AC1: handoff-spec 新增 §4 模板骨架——H1 固定 `# Session Handoff` + 6 个 H2（任务断点 / 关键决策摘要 / 环境脏点 / 已知风险 / 唤醒指令 / 状态指针），顺序与 §3 字段表一致，含占位注释与「H1 不得改写 / H2 顺序固定 / 占位注释落盘须替换」三条模板规则。
- [x] AC2: handoff-spec 新增 §5 生成流程——5 个不得跳步的步骤（来源确认 / 字段映射 / 长度自检 / 完整性自检 / 落盘）+ 反模式清单（禁写思考过程、禁复制大段日志、禁罗列已完成清单、禁写成对人交付总结）。
- [x] AC3: §4/§5 与既有约束自洽——H2 顺序对齐 §3；§5 长度自检 ≤500 tokens 对齐 §2；「状态指针」简单任务可省对齐 context-persistence §6。
- [x] AC4: context-persistence §6 蒸馏规则指向新增段——明确「模板骨架见 handoff-spec §4、生成步骤见 §5」。
- [x] AC5: 不越界——未改 §3 字段表语义、未改四件套字段、未碰 hook、handoff-spec frontmatter scope 不变。

# Verification Method

- AC1/AC2: 读 handoff-spec §4/§5，核对骨架字段齐全、H2 顺序、模板规则、5 步序列与反模式。
- AC3: 交叉比对 §4 H2 顺序 vs §3 字段表、§5 长度上限 vs §2、状态指针可省 vs context-persistence §6。
- AC4: 读 context-persistence §6，确认指针句存在。
- AC5: git diff 确认仅 §4/§5 新增 + §6 一行；grep 确认 §3 字段表与 frontmatter 未变。
