---
title: 验证报告模板
audience: AI / 开发者
scope: P5 Verify 阶段的验证结果、风险说明与验收回填模板
---

# Verify Schema

> 结构机器真源：`tools/artifact-pipeline/artifacts.v1.json` + `templates/VERIFY_REPORT.md`。本文件解释验证语义；新 live 产物的 H2、Evidence 表头和条件段由 manifest 固定，N/A 不删段，legacy 归档不追溯改写。

## 1. 目标

用于在交付前明确说明：哪些 AC 已满足、如何验证、还剩哪些风险。

## 2. 交付约定

- 必须产出：`.ai/VERIFY_REPORT.md`
- 必填字段：`Verification Summary`、`AC Status`、`Evidence Index`、`Verification Results`、`TDD Pair Status`、`Goal Calibration`、`Completion Inputs`、`Gate Coverage`、`Remaining Risks`、`Handoff / Next Step`
- 条件字段：`人测道小结`（段位置与空值口径由 `tools/artifact-pipeline/artifacts.v1.json` + `templates/VERIFY_REPORT.md` 固定，缺省 N/A 不删段；存在 human·待人 档 AC 时必填，见 §3 模板与 §4 分道回填要求）

## 3. 标准模板

```md
# Verification Summary
- 本次验证覆盖范围
- 总体验收结论

# AC Status（道 + 置信档合并标记，见 §4）
- [x] AC1 (auto·可靠): 已满足 ✓
- [x] AC2 (auto·弱): 已满足 ✓（代理验证：截图对基线 diff）
- [ ] AC3 (human·待人): 待人测 — 归 <类目>

# 人测道小结（段位置由 manifest/template 固定；无 human·待人 档 AC 时整段保留 N/A）
- AC3：<归入类目：主观审美 / 物理设备 / 真人感知 / 外部人工闸> — 状态：待人测 / 结论摘要

# Evidence Index
| Evidence ID | AC | 强度 | Outcome | Record |
|---|---|---|---|---|
| unit-tests | AC1, AC2 | captured | passed | `.ai/iterations/ITER-NNNN/evidence/unit-tests/record.json` |

# Verification Results
- AC1: 使用了什么验证方式，结果如何
- AC2: 使用了什么验证方式，结果如何
- AC3: 为什么尚未关闭

# TDD Pair Status
- TECH_PLAN 未声明 TDD cycle 时写 N/A
- 已声明时逐 cycle 写 `check-tdd` 的 `[OK]` 或失败诊断，并在 Evidence Index 引用 Red/Green record

# Goal Calibration
- CAL-001：<signal> → <route> → resolved（依据：<新 evidence / 重审 verdict>）
- 本轮无 calibration signal 时写 N/A

# Completion Inputs
- Review Verdict: pass
- Completion Blockers: none

# Gate Coverage
- 通用质量门禁：已验证项
- Workspace Scope：`check-plan` 与 `check-diff` 的 evidence ID（无 `prd_refs` 时标 N/A）
- Active Profiles：已验证项（仅命中时填，未命中可省略）
- Tech Plan Alignment：TECH_PLAN 中 Design Decisions 的兑现情况
- References Compliance：.ai/references/ 下已处理参考资料的规格遵守情况（需求集合逐项对 AC 钉住的 prd_refs 核；legacy 旧迭代按 prd_version + migration receipt 解析；无参考资料时标注 N/A）

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
- **Evidence Index 硬门**：完整路径迭代每条已通过的自动道 AC 必须引用机器生成的 evidence ID，record 最终路径固定在 `.ai/iterations/ITER-NNNN/evidence/<id>/record.json`；只有命令文本、测试数量、截图描述或“passed”措辞一律只是 `reported`，不得勾选。record schema 与校验命令以 `tools/verification-evidence/README.md` 为真源。
- 失败/超时/截断记录同样保留并列入 Evidence Index，作为纠错轨迹；它们不能覆盖绿色 AC。修复后用新 evidence ID 重跑，只有 outcome=`passed` 的记录可为已勾选自动道 AC 提供覆盖。
- **TDD 配对投影**：TECH_PLAN 在 `Test Strategy` 声明 cycle 时，P5 必须先运行 `verification-evidence check-tdd`，把逐 cycle 结果写入 `TDD Pair Status`，并把 Red/Green 两条 record 都列入 Evidence Index。任一 cycle 未通过时 `Completion Blockers` 必须为 `present`；未声明时写 N/A，不新增收口义务。
- **证据强度诚实**：`reported`=仅声称、不能关 AC；`captured`=证据包已校验但未重跑；`reproduced`=复核者重新执行并产生独立 evidence ID。未重跑不得写成“复现”。
- **分道回填**：每条 AC 必须标所属道 + 置信档，合并记为 `(auto·可靠)` / `(auto·弱)` / `(human·待人)`（道口径见 `30_Quality_Gate/testing-strategy.md §3`，置信档见下条）。自动道 AC 须给可复现的自动验证证据（命令 / 断言 / 脚本 / 代理验证）；人测道 AC 须在「人测道小结」说明归入哪个类目、为何机器不可测，并记其待测 / 结论状态。默认归自动道，说不出人测类目即应回自动道。
- **分级置信**：道标记内叠三档置信，如实记录、不虚高——
  - `可靠`：确定性、可复现的机器断言（单测 / 类型检查 / 构建 / 精确视觉断言等），自动道默认档。
  - `弱`：代理验证产出的弱但真实信号（截图对基线 diff / VLM 判读截图 / 启发式断言，见 `30_Quality_Gate/testing-strategy.md §3.1`）；仍属自动道，但**不冒充 `可靠`**。
  - `待人`：机器（含代理验证）都测不了、只能人判定的残余，即人测道；须在「人测道小结」记类目与状态。
  - 红线：`弱` 不标 `可靠`、`待人` 不标已验——`/butler:dangerous` 无人值守下尤须如实（残余处置见 `65_Extension_Dangerous/dangerous-engine.md §7.4`）。
- **人测道回传闭环**：`(human·待人)` 档残余不止于"标记待人"——有人场次须经**交付自测桥**回传结论并按四态路由回填（触发 / 后台起桥 / 阻塞等待 / 读回 / 四态路由流程见 `human-test-bridge.md`）：`pass` 计入收口 / `fail` 进纠错（`correction-contract.md`）/ `defer` 记 `Remaining Risks` 不阻塞 / `skip` 记 N/A；无人值守（`/butler:dangerous`）不起桥、改走 `65_Extension_Dangerous/dangerous-engine.md §7.4` 准入闸。
- 验证方式应具体到 evidence ID、检查动作或人工确认口径；命令 argv/退出码/日志摘要由 record 承载，VERIFY 不手抄伪造第二份。
- `Gate Coverage` 分四类回填：通用质量门禁（始终）、Active Profiles（仅命中时）、Tech Plan Alignment（逐项对照 `TECH_PLAN.md` 中的 Design Decisions 说明是否兑现）、References Compliance（逐项对照 `.ai/references/` 下的参考资料说明规格是否被遵守；本轮无参考资料时标注 N/A）。**需求集合专项**：遍历 `AC_LIST.md` 的每个 `prd_refs` 项，逐个 `prd_id / prd_version / module_slug` 核钉住版而非 live 最新；live 版本不符即读该需求自己的 `.archive/<prd_version>/`，不得跨需求借同名模块。legacy 旧迭代用 `prd_version` 加 migration receipt 解析隐式身份。语义见 `acceptance-schema.md §4/§5`，确定性解析见 `references-schema.md §8`。
- AC 含 `prd_refs` 时，P5 必须把 `check-plan` 和 `check-diff` 作为 Workspace Scope 证据归档；`check-diff` 覆盖删除、重命名、复制与未跟踪路径，任一越界均阻断完成。无 `prd_refs` 时明确记 N/A；legacy `prd_version` 未迁移时不得把范围检查写成通过。
- 若仍有未关闭风险，必须显式暴露，不能用总结性措辞掩盖。
- `Goal Calibration` 按 `goal-calibration.md` 回填本轮 completion-blocking signal、route 与 resolved 依据；仍 open/blocked 时不得勾绿受影响 AC 或收口。Remaining Risks 不能作为绕过该门的垃圾桶。
- `Completion Inputs` 是完成裁决器的机读输入：`Review Verdict` 只允许 `pass / must-fix / not-run`，`Completion Blockers` 只允许 `none / present`；未知/缺失 fail-closed。完整路径收口前运行 `tools/goal-assurance/goal.py evaluate`，只有 exit 0 / `eligible` 可进入收口仪式。裁决器会独立重查 TECH_PLAN 声明的 TDD 配对，不信任 `TDD Pair Status` 文字本身。
- `Remaining Risks` 也是 Review / P5 自评产出的 **Should Fix（不阻断项）** 的落点（不得写入 `01_CHANGELOG.md`）；见 `60_Extension_CodeReview/review-engine.md §4`。
- 字段正文必须讲人话、不啰嗦，口径以 `artifact-style.md` 为准（单一来源，不在此重复）；AC 回填用紧凑式 `[x] ACn ✓ 一句话证据`，不重抄 AC 原文。
- `Independent Review` 为可选字段：仅当本迭代跑过独立复核（手动 `/review` 或 project-config `resolve` 返回 `independent_review=true`）时回填；未跑则可整段省略。环境不支持 fresh-context 子 agent 而未能独立复核时，须按 `62_Extension_Agents/overview.md §3` 通用规矩 **G2** 如实标注"未执行"并落到 `Remaining Risks`，不得冒称已独立复核。

## 5. 与执行流程的关系

- P5 阶段必须产出 `.ai/VERIFY_REPORT.md`，按 `.ai/AC_LIST.md` 逐项回填验证结果。
- 完整路径 P5 在最终回填前必须校验并归档 evidence 热区；归档/重开协议见 `iteration-schema.md §5.5` 与工具 README。
- completion adjudicator 在 evidence 尚处热区时运行；它只判 active iteration 的 close eligibility，不替代归档后的 state audit。
- 若任务已闭合，可作为最终交付摘要的一部分。
- 若任务未闭合，可继续衔接 checkpoint 或 `02_SESSION_HANDOFF.md`。
- 简化路径下可简要验证，不强制产出此文件。
