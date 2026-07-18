---
title: 复核帮手定义
audience: AI / 开发者
scope: 复核帮手（independent review）的中立定义——角色/输入/输出/禁止/隔离/权限 + 触发/断言核对/输出衔接；共享审查流程回指 60_Extension_CodeReview，通用规矩回指 overview
---

# 复核帮手（Independent Review）

> 帮手名册的一员，通用规矩见 `overview.md` §3（G1–G4）。本文件是复核帮手的完整定义；它执行的**共享审查流程**（多维评审 / 评级 / 闭环）不归它私有，仍以 `60_Extension_CodeReview/review-engine.md` 为真源，本文件只定"把那套流程放进隔离上下文跑"的复核专有部分。

## 1. 一句话

复核 = 把审查放进一个与作者隔离的干净子 agent 里跑，拿验收标准挨条核对产物写得对不对、挑出错就拦住收工——从结构上避免"自己给自己打分"。

## 2. 中立定义（角色 / 输入 / 输出 / 禁止 / 隔离 / 权限）

| 项 | 内容 |
|---|---|
| **角色** | Checker（核对者），**不是** Maker（实现者）：只核对、不重写实现。以资深技术审计的第三方视角执行，脱离作者身份。 |
| **输入**（spec-only，刻意不含作者推理链） | `.ai/AC_LIST.md`（验收尺子）、`.ai/TECH_PLAN.md`（约定边界）、产物（`git diff` / 变更文件）、`.ai/VERIFY_REPORT.md`（作者的自评断言）及其 Evidence Index 指向的机器 record。 |
| **输出** | 逐条 AC 的 **confirm / refute / 无法验证** 裁决 + 证据强度（reported/captured/reproduced）；加按共享流程出的多维审查意见（含严重级别 Must / Should / Nice）。 |
| **禁止** | ① 从头重新实现一遍；② 仅凭 `VERIFY_REPORT.md` 的措辞就采信"已满足"；③ 为产物辩护。**拿不准一律判 refute。** |
| **隔离** | 必须 fresh-context 子 agent（通用规矩 G1）；起不了就按 G2 如实标注"未执行"、不冒称已独立。 |
| **权限** | **实现/规格只读**（读 + 搜），不改代码和四件套；唯一写权限是调用 verification evidence runner 在证据热区生成 `review-*` record，由主线校验/归档。 |

## 3. 触发

- **手动**：用户输入 `/review`，或提到"看看写得怎么样""有没有坑""评价一下""代码审查"——一次性触发，跑完即止。
- **配置驱动**：项目 `.ai/local-constraints.md`「Butler 功能开关」`independent_review: on` 时，每次 P5 收口自动起，无需每轮手输（默认 off）。
- **危险模式**：`/butler:dangerous` 下 P5 强制完整审查建议升格为独立复核（见 `65_Extension_Dangerous/dangerous-engine.md §7.3`）。

> 独立复核是叠在 P5 简评之上的 opt-in 增强、不替代简评（`60_Extension_CodeReview/review-engine.md §5` 的同上下文简评照常默认跑）。

## 4. 执行：断言核对（复核专有的那一层）

复核跑 `60_Extension_CodeReview/review-engine.md §3` 的**共享审查流程**（变更识别 / 口径合并 / 多维评审 / 评级），并**额外承担一层断言核对**：

- 逐条比对 `.ai/AC_LIST.md` 与 `.ai/VERIFY_REPORT.md` 中标称"已满足"的声明，独立确认产物是否真兑现该 AC。
- 先校验 Evidence Index 与 record；风险相关命令由复核者抽样重跑并产生独立 `review-*` evidence ID。只读限制是“不改实现/规格”，不妨碍在隔离临时环境执行验证并把 record 交回主线归档。
- 未重跑的结论只能标 `captured`，不得因为身处 fresh-context 就把作者证据写成 `reproduced`。
- 被 **refute** 的 AC（标称已满足但产物未兑现）等同 **Must Fix**，阻断收口。

## 5. 输出衔接

- 裁决写入 `.ai/references/insight-independent-review.md`（落进 `.ai/references/` 外部参考资料目录）。
- refute 的 AC 与 Must Fix 走 `60_Extension_CodeReview/review-engine.md §4` 闭环（阻断收口 → 退回 P4 / `/butler:loop`）。
- 跑过独立复核的迭代，`.ai/VERIFY_REPORT.md` 的 `Independent Review` 字段须回填结论（见 `20_Workflow_Lifecycle/verify-schema.md`）。

## 6. 诚实兜底

- 环境无 fresh-context 子 agent 能力时，按 `overview.md` §3 通用规矩 **G2** 处理：如实标注"独立复核未执行（环境不支持）"、当 `Remaining Risk` 暴露，**不得**退回同上下文自评再冒称"已独立复核"。
