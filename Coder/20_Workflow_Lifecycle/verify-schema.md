---
title: 验证报告模板
audience: AI / 开发者
scope: P5 Verify 阶段的验证结果、风险说明与验收回填模板
---

# Verify Schema

## 1. 目标

用于在交付前明确说明：哪些 AC 已满足、如何验证、还剩哪些风险。

## 2. 交付约定

- 必须产出：`.ai/VERIFY_REPORT.md`
- 必填字段：`Verification Summary`、`AC Status`、`Verification Results`、`Gate Coverage`、`Remaining Risks`、`Handoff / Next Step`

## 3. 标准模板

```md
# Verification Summary
- 本次验证覆盖范围
- 总体验收结论

# AC Status
- [x] AC1: 已满足 / 未满足
- [x] AC2: 已满足 / 未满足
- [ ] AC3: 未满足原因

# Verification Results
- AC1: 使用了什么验证方式，结果如何
- AC2: 使用了什么验证方式，结果如何
- AC3: 为什么尚未关闭

# Gate Coverage
- 通用质量门禁：已验证项
- Active Profiles：已验证项（仅命中时填，未命中可省略）
- Tech Plan Alignment：TECH_PLAN 中 Design Decisions 的兑现情况
- References Compliance：.ai/references/ 下已处理参考资料的规格遵守情况（无参考资料时标注 N/A）

# Independent Review（可选，仅当本迭代跑过独立复核时填）
- 复核方式：fresh-context 子 agent / 手动 /review / 未执行（环境不支持）
- 逐 AC 裁决：confirm N 项 / refute M 项；refute 项列出与处置
- 结论：通过 / 阻断（Must Fix 待修，见 .ai/references/insight-independent-review.md）

# Remaining Risks
- 当前未关闭风险
- 尚未覆盖的边界情况

# Handoff / Next Step
- 若任务未完全闭合，下一步从哪里继续
```

## 4. 编写规则

- 必须按 AC 回填，不得只给笼统结论。
- 验证方式应尽量具体到命令、检查动作或人工确认口径。
- `Gate Coverage` 分四类回填：通用质量门禁（始终）、Active Profiles（仅命中时）、Tech Plan Alignment（逐项对照 `TECH_PLAN.md` 中的 Design Decisions 说明是否兑现）、References Compliance（逐项对照 `.ai/references/` 下的参考资料说明规格是否被遵守；本轮无参考资料时标注 N/A）。
- 若仍有未关闭风险，必须显式暴露，不能用总结性措辞掩盖。
- 字段正文必须讲人话、不啰嗦，口径以 `artifact-style.md` 为准（单一来源，不在此重复）；AC 回填用紧凑式 `[x] ACn ✓ 一句话证据`，不重抄 AC 原文。
- `Independent Review` 为可选字段：仅当本迭代跑过独立复核（手动 `/review` 或项目 `Review Policy: independent_review: on`）时回填；未跑则可整段省略。环境不支持 fresh-context 子 agent 而未能独立复核时，须按 `60_Extension_CodeReview/review-engine.md` §6.4 如实标注"未执行"并落到 `Remaining Risks`，不得冒称已独立复核。

## 5. 与执行流程的关系

- P5 阶段必须产出 `.ai/VERIFY_REPORT.md`，按 `.ai/AC_LIST.md` 逐项回填验证结果。
- 若任务已闭合，可作为最终交付摘要的一部分。
- 若任务未闭合，可继续衔接 checkpoint 或 `02_SESSION_HANDOFF.md`。
- 简化路径下可简要验证，不强制产出此文件。