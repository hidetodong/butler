---
状态: ack-frozen
ACK 日期: 2026-07-22
---

> ⚠️ 危险模式：模型已过验收自审门并自主冻结（ITER-0078，2026-07-22）。

# Goal

- 交付真实可用且不越权的 `/butler:inbox` 扫描与分类路由工作流。

# In Scope

- 标准库 scanner 的 plan/apply/status、canonical INBOX 管理块和 JSON 输出。
- origin 文件递归发现、原始字节 hash、source_id、幂等/变化/缺失/符号链接边界。
- 模型分类、批量确认、路由矩阵、危险模式自审与活工作区保护。
- Claude/Codex 入口、registry 第 11 项、生成投影和人读表。
- 隔离 fixture、完整 CI 和文档计数。

# Out of Scope

- 不让 scanner 自动判断新需求/新版，不在 CLI 内创建 PRD/里程碑/ideation。
- 不写、移动、删除 origin 文件，不跟随 origin 内符号链接。
- 不实现 R5 多 PRD 引用迁移或 R7 update receipt。

# Acceptance Checklist

- [ ] AC1：`inbox.py scan` 默认只输出计划且零写入，`--apply` 只原子更新 `.ai/INBOX.md` 管理块，保留管理块外内容。
- [ ] AC2：递归扫描 origin regular files、按原始字节 SHA-256；符号链接/逃逸拒绝，origin 缺失按空收件箱处理且不创建它。
- [ ] AC3：同 locator+hash 幂等、同 locator 变更保留 source_id 并置 source-changed、已消失来源保留历史且不删除关系。
- [ ] AC4：工具输出稳定 JSON，包含 added/changed/unchanged/missing/rejected 和待处理来源；异常退出码与零部分写入明确。
- [ ] AC5：workflow 对待处理来源逐项语义分类，呈交分类/理由/路线；standard 模式确认前不路由，dangerous 模式自审后才放行并写审计。
- [ ] AC6：分类准确路由到 PRD 首切、PRD update、supplemental、ideation、milestone backlog 或 record-only；ambiguous/duplicate 等待确认，不静默合并。
- [ ] AC7：批量路由不得覆盖活 MILESTONE/迭代四件套/IDEATION；冲突项保持 awaiting-confirmation，其余无依赖项继续。
- [ ] AC8：Claude `/butler:inbox`、Codex `$butler-inbox`、repo discovery、registry/docs/plugin 投影一致；workflow 集合从 10 升 11。
- [ ] AC9：隔离 fixture 覆盖 plan/apply 幂等、内容变化、缺失、symlink、原文零写入、管理块外保留和 registry 完整性；完整 CI 通过。

# Verification Method

- AC1–AC4/AC9：标准库 unittest 临时项目 fixture + CLI subprocess + 文件 hash 前后对账。
- AC5–AC8：结构合同、registry sync --check、命令/skill 逐分支审查。
- 全量：`bash scripts/verify-ci.sh`、diff check、Goal/state audit。

# Open Questions / Risks

- 模型语义分类无法由 scanner 单测证明，结构测试只证明路由协议；R8 端到端会用代表性 fixture 再验证。
