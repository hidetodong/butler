# ITER-0063 · 方案准入与反证门

> 迭代交付（小版本） · 2026-07-18 · MILE-0008 R3 · 危险模式自主 ACK / 完整审查

## 本次交付目标

把 P3 从“TECH_PLAN 已存在、模型说可以”升级为有结构化反证、有明确 verdict、未通过就不能写源码的方案准入门。

## 已完成内容

- TECH_PLAN 新增 `draft / pass / revise / blocked` 四态、审查日期/方式与七项 Plan Admission。
- 标准模式与危险模式都只能在没有已知 Must Fix 时置 `pass`；实质改方案退回 `draft` 重审。
- Goal Contract 将 draft/revise 派生为 at-risk，真正 blocked 派生为 blocked。
- Claude/Codex 共用 phase gate；显式非 pass 与未知值拒绝源码写，旧版无字段保留兼容窗口。
- 新增 7 项结构合同测试，扩展共享 hook 与 Codex wrapper 真链路回归。

## 关键变更 / 用户可感知变化

- 用户 ACK 不再能覆盖方案自己已知的问题；`revise` 必须回修，`blocked` 必须停机。
- Codex apply_patch 与 Claude 写工具消费同一个 verdict 算法，不产生双宿主规则漂移。
- 旧项目不会因模板尚未升级而立即被误杀，但新 TECH_PLAN 不得借 legacy 窗口省略状态。

## 验证方式与结果摘要

- 结构合同 7/7、phase gate 21/21；最终完整矩阵检查 968 个 Markdown 文件/43 链接、8 skills/plugin、135 hooks 与统一双宿主矩阵，全部通过。
- 强审修复 1 Must Fix（Codex wrapper 原先只走 legacy allow，没证明新门）；修复后 draft deny → pass allow 真链路 reproduced 通过，最终 Must Fix 0、Should Fix 0。

## 已知剩余风险 / 延后事项

- hook 只能核 verdict，不能证明自然语言方案绝对正确；R5 仍需最终完成裁决。
- legacy 兼容窗口的移除需要后续迁移配方；未执行 fresh-context 独立复核。

## 引用（只引用，不嵌入）

- `.ai/iterations/ITER-0063/`
- `Coder/20_Workflow_Lifecycle/tech-plan-schema.md`
- checkpoint `da3cae0`
