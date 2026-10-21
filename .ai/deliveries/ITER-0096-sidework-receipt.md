# ITER-0096 · 旁路工作回执协议

## 本次交付目标

让用户主动发起、脱离主上下文完成的代码与调研成果，可以通过一份短回执稳定钩回主 Agent，而不引入模型审批、自动扫描或第二套主线状态。

## 已完成内容

- 建立旁路工作回执规则真源，明确固定结构、生产/消费流程和现有状态载体的职责边界。
- 提供支持代码、调研、方案、实验和 evidence 混装的 canonical Markdown 模板。
- 在 Coder 规则入口与人类指南中登记触发方式、按需目录和可直接复制的发起/回钩说法。
- 增加标准库静态合同检查并接入完整 CI，锁定模板、入口、用户决策权、非写入授权和并发 create-only 边界。

## 关键变更 / 用户可感知变化

旁路 Agent 收工时可以把最终结论、成果位置、验证事实和续接入口写到 `.ai/sidework/`，用户只需把路径交给主 Agent。主 Agent 不默认扫描目录，也不替用户接受或拒绝成果；发现方向冲突时会把影响摆出来交由用户决定。

## 高层影响范围

上下文治理规则、回执模板、Coder 入口、人类使用指南和完整 CI。没有新增命令、skill、运行时工具、索引、状态机或自动合并能力。

## 验证方式与结果摘要

旁路回执专项最终 9/9、Markdown links、五件套结构、active 状态审计、diff check 和两次宿主环境完整 CI 均通过；Goal 裁决十一项检查为 `eligible`。P5 完整审查修复“回执可能被误读成写入授权”的 Must Fix 后，最终 Must Fix 0、Should Fix 0；证据见归档 Evidence Index。

## 已知剩余风险 / 延后事项

- 回执结构可机械校验，但摘要质量和共享脏工作区的作者归属不能被模板自动证明，主 Agent 仍需核对实际指针与代码。
- 项目关闭了独立复核，本轮只执行同上下文危险模式完整审查，未冒称 fresh-context 独立结论。
- 当前危险模式规则文档仍把 Loop 写成自动绑定，与用户确认语义冲突；该问题不属于本迭代，需另领纠偏迭代。

## 引用

- `.ai/iterations/ITER-0096/CONCEPT.md`
- `.ai/iterations/ITER-0096/AC_LIST.md`
- `.ai/iterations/ITER-0096/TECH_PLAN.md`
- `.ai/iterations/ITER-0096/VERIFY_REPORT.md`
- `.ai/iterations/ITER-0096/CHANGELOG.md`
- `.ai/iterations/ITER-0096/evidence/`
- `Coder/40_Context_Management/sidework-receipt.md`
- `templates/sidework-receipt.md`
