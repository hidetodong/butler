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
- 条件字段：`人测道小结`（仅当存在人测道 AC 时必填，见 §3 模板与 §4 分道回填要求）

## 3. 标准模板

```md
# Verification Summary
- 本次验证覆盖范围
- 总体验收结论

# AC Status（道 + 置信档合并标记，见 §4）
- [x] AC1 (auto·可靠): 已满足 ✓
- [x] AC2 (auto·弱): 已满足 ✓（代理验证：截图对基线 diff）
- [ ] AC3 (human·待人): 待人测 — 归 <类目>

# 人测道小结（仅当存在 human·待人 档 AC 时；无则整段省略）
- AC3：<归入类目：主观审美 / 物理设备 / 真人感知 / 外部人工闸> — 状态：待人测 / 结论摘要

# Verification Results
- AC1: 使用了什么验证方式，结果如何
- AC2: 使用了什么验证方式，结果如何
- AC3: 为什么尚未关闭

# Gate Coverage
- 通用质量门禁：已验证项
- Active Profiles：已验证项（仅命中时填，未命中可省略）
- Tech Plan Alignment：TECH_PLAN 中 Design Decisions 的兑现情况
- References Compliance：.ai/references/ 下已处理参考资料的规格遵守情况（PRD 切片对 AC 钉住的 prd_version 核；无参考资料时标注 N/A）

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
- **分道回填**：每条 AC 必须标所属道 + 置信档，合并记为 `(auto·可靠)` / `(auto·弱)` / `(human·待人)`（道口径见 `30_Quality_Gate/testing-strategy.md §3`，置信档见下条）。自动道 AC 须给可复现的自动验证证据（命令 / 断言 / 脚本 / 代理验证）；人测道 AC 须在「人测道小结」说明归入哪个类目、为何机器不可测，并记其待测 / 结论状态。默认归自动道，说不出人测类目即应回自动道。
- **分级置信**：道标记内叠三档置信，如实记录、不虚高——
  - `可靠`：确定性、可复现的机器断言（单测 / 类型检查 / 构建 / 精确视觉断言等），自动道默认档。
  - `弱`：代理验证产出的弱但真实信号（截图对基线 diff / VLM 判读截图 / 启发式断言，见 `30_Quality_Gate/testing-strategy.md §3.1`）；仍属自动道，但**不冒充 `可靠`**。
  - `待人`：机器（含代理验证）都测不了、只能人判定的残余，即人测道；须在「人测道小结」记类目与状态。
  - 红线：`弱` 不标 `可靠`、`待人` 不标已验——`/butler:dangerous` 无人值守下尤须如实（残余处置见 `65_Extension_Dangerous/dangerous-engine.md §7.4`）。
- **人测道回传闭环**：`(human·待人)` 档残余不止于"标记待人"——有人场次须经**交付自测桥**回传结论并按四态路由回填（触发 / 后台起桥 / 阻塞等待 / 读回 / 四态路由流程见 `human-test-bridge.md`）：`pass` 计入收口 / `fail` 进纠错（`correction-contract.md`）/ `defer` 记 `Remaining Risks` 不阻塞 / `skip` 记 N/A；无人值守（`/butler:dangerous`）不起桥、改走 `65_Extension_Dangerous/dangerous-engine.md §7.4` 准入闸。
- 验证方式应尽量具体到命令、检查动作或人工确认口径。
- `Gate Coverage` 分四类回填：通用质量门禁（始终）、Active Profiles（仅命中时）、Tech Plan Alignment（逐项对照 `TECH_PLAN.md` 中的 Design Decisions 说明是否兑现）、References Compliance（逐项对照 `.ai/references/` 下的参考资料说明规格是否被遵守；本轮无参考资料时标注 N/A）。**PRD 切片专项**：对着 `AC_LIST.md` frontmatter 钉住的 `prd_version` 核、**非对 live 最新核**——同一迭代内 live 即钉住版（读 live 即可），仅回溯复核历史迭代（PRD 此后已改版）才按 `prd_version` 读 `.archive/vN/<slug>.md`（钉住版语义见 `acceptance-schema.md §4`、读侧纪律回指 `40_Context_Management/references-schema.md §5 步骤 2`）。
- 若仍有未关闭风险，必须显式暴露，不能用总结性措辞掩盖。
- `Remaining Risks` 也是 Review / P5 自评产出的 **Should Fix（不阻断项）** 的落点（不得写入 `01_CHANGELOG.md`）；见 `60_Extension_CodeReview/review-engine.md §71`。
- 字段正文必须讲人话、不啰嗦，口径以 `artifact-style.md` 为准（单一来源，不在此重复）；AC 回填用紧凑式 `[x] ACn ✓ 一句话证据`，不重抄 AC 原文。
- `Independent Review` 为可选字段：仅当本迭代跑过独立复核（手动 `/review` 或项目 `Review Policy: independent_review: on`）时回填；未跑则可整段省略。环境不支持 fresh-context 子 agent 而未能独立复核时，须按 `62_Extension_Agents/overview.md §3` 通用规矩 **G2** 如实标注"未执行"并落到 `Remaining Risks`，不得冒称已独立复核。

## 5. 与执行流程的关系

- P5 阶段必须产出 `.ai/VERIFY_REPORT.md`，按 `.ai/AC_LIST.md` 逐项回填验证结果。
- 若任务已闭合，可作为最终交付摘要的一部分。
- 若任务未闭合，可继续衔接 checkpoint 或 `02_SESSION_HANDOFF.md`。
- 简化路径下可简要验证，不强制产出此文件。