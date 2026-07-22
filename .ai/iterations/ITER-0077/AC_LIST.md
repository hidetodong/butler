---
状态: ack-frozen
ACK 日期: 2026-07-22
---

> ⚠️ 危险模式：本产物由模型自主 ACK（已过验收自审门），未经用户逐项确认（ITER-0077，2026-07-22）。

# Goal

- 建立来源可追踪、变化可检测、派生可回溯且不碰用户原稿的收件箱数据合同。

# In Scope

- `origin/` 可选收件箱与严格只读边界。
- `.ai/INBOX.md` 来源表、关系表和稳定 `source_id`。
- 文件/对话/外部文档 locator、SHA-256 双指纹和状态机。
- 幂等、来源变化、重复候选、多对多派生与敏感信息边界。
- 部署/README/HUMAN_GUIDE 接线和结构测试。

# Out of Scope

- 不实现 `/butler:inbox` 扫描、分类、确认、路由或命令注册。
- 不写 `origin/`，不自动生成 PRD/里程碑/脑暴产物。
- 不把 INBOX 变成原文快照、版本仓库或通用事件日志。

# Acceptance Checklist

- [ ] AC1：schema 定义 `.ai/INBOX.md` 来源表和派生关系表，字段能回答来源是谁、当前内容、上次处理、状态、建议/实际去向。
- [ ] AC2：`source_id` 单调分配且不复用；kind/locator 改变与内容改变的身份边界明确，不能用 hash 充当来源身份。
- [ ] AC3：文件 SHA-256 对原始字节计算；对话/外部文档有确定性规范化与稳定 locator，保存 observed/processed 双指纹。
- [ ] AC4：状态为封闭枚举并给出转移：unprocessed/analyzed/awaiting-confirmation/routed/ignored/source-changed/failed；失败与忽略不伪装 routed。
- [ ] AC5：同 locator + 同 hash 幂等不新增来源；同 locator hash 变化保持 source_id 并置 source-changed；同 hash 不同 locator 只标重复候选、不自动合并。
- [ ] AC6：一源多产物、多源一产物由独立关系表表达；ledger 不复制完整原文、凭据或敏感内容，origin 永远只读。
- [ ] AC7：部署/README/HUMAN_GUIDE 接线与结构测试完整，非 inbox 快速路径不回归，完整 CI 通过。

# Verification Method

- AC1–AC7：标准库 unittest 检查字段、指纹、状态、转移、幂等、关系与只读红线。
- AC7：专项测试、Markdown、完整 CI、diff check 与状态审计。

# Open Questions / Risks

- 对话文本规范化必须避免不同语义被过度归一；R3 采用最小换行规范化，不做语义清洗。
- 外部文档若无法取得稳定 revision，只能用 URL + 抓取内容 hash，状态仍可检测变化但来源系统版本号可能未知。
