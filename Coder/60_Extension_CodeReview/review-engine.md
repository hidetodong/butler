---
title: Butler-Review 审计引擎
audience: AI / 开发者
scope: 代码审查的激活条件、评级标准与闭环控制（共享审查流程真源）；P5 默认同上下文简评。复核帮手（独立复核）的完整定义见 62_Extension_Agents/independent-review.md
---

# Butler-Review 审计引擎

> 本文件是**共享审查流程**的真源（多维评审 / 评级 / 闭环 / P5 简评）。复核帮手（把这套流程放进隔离上下文跑的"独立复核"）的完整定义已迁至 `62_Extension_Agents/independent-review.md`；所有帮手的通用规矩（干净上下文 G1 / 诚实兜底 G2）见 `62_Extension_Agents/overview.md §3`。

## 1. 身份

资深技术审计专家。执行审查时，必须脱离"作者"身份，以冷酷的第三方视角审视每一行变更。

本引擎区分两种强度 / 独立性不同的"审"：

- **P5 简要自评**（§5）：**同一上下文**内的轻量自检，默认开。便宜、快，用于收口前拦明显问题；但本质仍是"作者换口吻自评"，盲点可能照样在。
- **独立复核 / Independent Review**：opt-in 的**真·独立**审查，靠**上下文隔离**（另起 fresh-context 子 agent、只喂规格与产物、不喂作者推理链）实现结构性的"验证者 ≠ 实现者"。其独立性原理见 `62_Extension_Agents/overview.md §3` 通用规矩 **G1**，完整定义（触发 / 契约 / 断言核对 / 衔接）见 `62_Extension_Agents/independent-review.md`。

## 2. 激活条件

- **P5 默认简评**（§5）：进入 P5 交付阶段默认触发同上下文简要自评（用户明确"跳过审查"时除外）。这是默认底线，**不是**独立复核。
- **独立复核触发**（手动 `/review` / 配置驱动 `independent_review: on` / 危险模式升格）：见 `62_Extension_Agents/independent-review.md §3`。

> 独立复核默认关。它是叠在 P5 简评之上的 opt-in 增强，不是替代——简评照常默认跑。

## 3. 审查流程 (Audit Flow)

激活后按以下流程执行，不依赖外部 skill。独立复核由 fresh-context 子 agent 执行本流程（见 `62_Extension_Agents/independent-review.md`）；手动 `/review` 与配置驱动共用同一口径。

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

> 独立复核在多维评审之外额外承担一层**断言核对**（逐条独立核对 `AC_LIST` 声明是否真兑现），属复核专有，见 `62_Extension_Agents/independent-review.md §4`。

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

**它是同上下文自检，不是独立复核**。需要结构性独立时，手动 `/review` 或为项目开 `independent_review: on`（触发与契约见 `62_Extension_Agents/independent-review.md`）。

## 6. 独立复核（定义已迁出）

独立复核（opt-in 的真·独立审查）的完整定义——中立契约（角色 / 输入 / 输出 / 禁止 / 隔离 / 权限）、触发、断言核对、输出衔接、诚实兜底——已迁至 `62_Extension_Agents/independent-review.md`。本节只保留它与共享流程的接口：

- 它跑的多维审查流程 = 本文件 §3；Must Fix / refute 闭环 = 本文件 §4。
- 环境无 fresh-context 子 agent 能力时的诚实兜底，按 `62_Extension_Agents/overview.md §3` 通用规矩 **G2**（如实标注"未执行"、当风险暴露，不冒称已独立）。

## 7. 与其他模块的关系

- `62_Extension_Agents/overview.md`：帮手通用规矩唯一真源（G1 独立性=上下文隔离 / G2 诚实兜底）；`62_Extension_Agents/independent-review.md`：复核帮手完整定义。
- `30_Quality_Gate/review-standard.md` 提供通用审计准则。
- `10_Domain_Stack_Profiles/` 提供技术栈专项审计规则。
- `20_Workflow_Lifecycle/local-constraints-schema.md` 定义 `Review Policy` 配置字段（项目级开关）。
- `20_Workflow_Lifecycle/verify-schema.md` 定义 VERIFY_REPORT 的 `Independent Review` 回填字段。
- `30_Quality_Gate/correction-contract.md` 承接 refute / Must Fix 的修复（修到真过、禁止降级修复）。
- `55_Extension_ConvergenceLoop/convergence-loop-engine.md` 承接 Must Fix 的高强度修复闭环。
- `20_Workflow_Lifecycle/lifecycle.md` P5 阶段触发简要自评；项目配置开启时触发独立复核。
- `65_Extension_Dangerous/dangerous-engine.md` 在无人值守下可选启用独立复核（其 §7.3 P5 强审可升格为独立复核）。
