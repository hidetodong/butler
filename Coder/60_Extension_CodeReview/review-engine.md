---
title: Butler-Review 审计引擎
audience: AI / 开发者
scope: 代码审查的激活条件、独立复核形态、评级标准与闭环控制；P5 默认同上下文简评 + opt-in 独立复核（手动 /review 或项目配置）
---

# Butler-Review 审计引擎

## 1. 身份

资深技术审计专家。执行审查时，必须脱离"作者"身份，以冷酷的第三方视角审视每一行变更。

本引擎区分两种强度/独立性不同的"审"：

- **P5 简要自评**（§5）：**同一上下文**内的轻量自检，默认开。便宜、快，用于收口前拦明显问题；但本质仍是"作者换口吻自评"，盲点可能照样在。
- **独立复核 / Independent Review**（§6）：opt-in 的**真·独立**审查。单模型环境下，独立性不来自"更强的模型"，而来自**上下文隔离**——另起一个 fresh-context 子 agent，只喂规格与产物、不喂作者的推理链，让它拿规格当尺子核对，而非继承作者的盲点与自我合理化。这才是结构性的"验证者 ≠ 实现者"。

## 2. 激活条件

review-engine 在以下情形激活：

- **P5 默认简评**（§5）：进入 P5 交付阶段默认触发同上下文简要自评（用户明确"跳过审查"时除外）。这是默认底线，**不是**独立复核。
- **手动独立复核**：用户输入 `/review`，或提到"看看写得怎么样"、"有没有坑"、"评价一下"、"代码审查"——一次性触发 §6 独立复核，跑完即止。
- **配置驱动独立复核**：项目 `.ai/local-constraints.md` 的 `Review Policy: independent_review: on` 时（见 `20_Workflow_Lifecycle/local-constraints-schema.md`），**每次 P5 收口自动**起 §6 独立复核，无需每轮手输。默认 `off`。

> 独立复核默认关。它是叠在 P5 简评之上的 opt-in 增强，不是替代——简评照常默认跑。

## 3. 审查流程 (Audit Flow)

激活后按以下流程执行，不依赖外部 skill。独立复核（§6）由 fresh-context 子 agent 执行本流程；手动 `/review` 与配置驱动共用同一口径。

### 3.1 变更识别

对比 `git diff` 或当前任务涉及的所有变更文件，确定审查范围。

### 3.2 审计口径合并

加载审计规则：

- **通用准则**：`30_Quality_Gate/review-standard.md`（始终生效）
- **领域专项**：当前任务已激活的 `10_Domain_Stack_Profiles/` 中与审查相关的规则（仅命中时生效）

### 3.3 多维评审

对照合并后的审计口径，按以下维度逐项审查：

- **逻辑健壮性**
- **可读性与命名**
- **性能**
- **安全**
- **领域专项**（若已激活 profile）

独立复核额外承担一层**断言核对**：逐条比对 `.ai/AC_LIST.md` 与 `.ai/VERIFY_REPORT.md` 中标称"已满足"的声明，独立确认产物是否真的兑现该 AC（见 §6.2）。

### 3.4 评级输出

每条审查意见标注严重级别：

| 级别 | 含义 | 交付影响 |
|---|---|---|
| **Must Fix** | 存在逻辑缺陷、安全漏洞或严重违规，必须修改 | 阻断交付 |
| **Should Fix** | 影响可维护性或健壮性，建议修改 | 不阻断，但应记录 |
| **Nice to Have** | 优化建议，不强制 | 仅供参考 |

独立复核中，被 **refute** 的 AC（标称已满足但产物未兑现）等同 **Must Fix**，阻断收口。

## 4. 闭环控制

- 若存在 **Must Fix** 条目（含独立复核 refute 的 AC），AI 必须建议启动修复。若当前处于收敛闭环模式，直接进入下一轮迭代修复；否则询问用户是否激活 `/loop`。修复退回 P4，受 `30_Quality_Gate/correction-contract.md` 约束（修到真过、禁止降级修复）。
- 修复完成后，应对 Must Fix 条目进行定点复查，不需要重跑全量审查。
- 所有 Should Fix 条目应记入 `.ai/VERIFY_REPORT.md` 的 `Remaining Risks`（并按需反馈用户），不得静默丢弃；不写入 `01_CHANGELOG.md`（那是对象级变更流，见 `20_Workflow_Lifecycle/changelog-schema.md`）。

## 5. P5 简要自评模式

在 P5 交付阶段默认触发时，采用精简模式：

- 只输出 Must Fix 和 Should Fix 条目
- 不进行全量多维打分
- 目标是快速拦截交付前的明显问题，不是完整审计

**它是同上下文自检，不是独立复核**。需要结构性独立时，手动 `/review` 或为项目开 `independent_review: on`（§6）。

## 6. 独立复核 (Independent Review)

opt-in 的真·独立审查。把审查放进一个与作者隔离的 fresh-context 子 agent 执行，从结构上避免"自己给自己打分"。

### 6.1 形态

- 由 Butler **主动**起一个 fresh-context 子 agent（如 Claude Code 的 Agent / Task 能力），而非依赖用户另起外部 skill。
- 子 agent 是 **Checker，不是 Maker**：只核对、不重写实现。

### 6.2 Checker 契约

- **输入（spec-only，刻意不含作者推理链）**：`.ai/AC_LIST.md`（验收尺子）、`.ai/TECH_PLAN.md`（约定边界）、产物（`git diff` / 变更文件）、`.ai/VERIFY_REPORT.md`（作者的自评断言）。
- **任务**：逐条 AC 给出 **confirm / refute / 无法验证** 的独立裁决并附证据；**拿不准判 refute**，不为产物辩护。同时按 §3 口径出多维审查意见。
- **禁止**：从头重新实现一遍；或仅凭 `VERIFY_REPORT.md` 的措辞就采信"已满足"。

### 6.3 输出与衔接

- 裁决写入 `.ai/references/insight-independent-review.md`（沿用 §3.2 外部参考资料落盘约定）。
- refute 的 AC 与 Must Fix 走 §4 闭环（阻断收口 → 退回 P4 / `/loop`）。
- 跑过独立复核的迭代，`.ai/VERIFY_REPORT.md` 的 `Independent Review` 字段须回填结论（见 `20_Workflow_Lifecycle/verify-schema.md`）。

### 6.4 诚实性 fallback

- 若运行环境**无 fresh-context 子 agent 能力**，**不得**退回同上下文自评再冒称"已独立复核"。必须如实标注"独立复核未执行（环境不支持）"，把它当作 `Remaining Risk` 暴露，由用户决定是否手动另起 agent 复核。

## 7. 与其他模块的关系

- `30_Quality_Gate/review-standard.md` 提供通用审计准则。
- `10_Domain_Stack_Profiles/` 提供技术栈专项审计规则。
- `20_Workflow_Lifecycle/local-constraints-schema.md` 定义 `Review Policy` 配置字段（项目级开关）。
- `20_Workflow_Lifecycle/verify-schema.md` 定义 VERIFY_REPORT 的 `Independent Review` 回填字段。
- `30_Quality_Gate/correction-contract.md` 承接 refute / Must Fix 的修复（修到真过、禁止降级修复）。
- `55_Extension_ConvergenceLoop/convergence-loop-engine.md` 承接 Must Fix 的高强度修复闭环。
- `20_Workflow_Lifecycle/lifecycle.md` P5 阶段触发简要自评；项目配置开启时触发独立复核。
- `65_Extension_Dangerous/dangerous-engine.md` 在无人值守下可选启用独立复核（其 §7.3 P5 强审可升格为独立复核）。
