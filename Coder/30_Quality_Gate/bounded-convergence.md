---
title: 有界 P4 收敛策略
audience: AI / 开发者
scope: 供 opt-in 模式（Convergence Loop 与 Dangerous Mode 的 P4 执行）共享的定量熔断纪律——重试上限、死锁判定、环境阻塞与 RCA 交还。不拥有任何模式的激活状态、入口或用户语义；常驻的定性「诚实停」仍由 correction-contract.md 拥有
---

# 有界 P4 收敛策略

## 1. 定位

本文件是**有界 P4 收敛策略**的单一真源：把「执行 → 探测 → 反思 → 修正」闭环的**定量熔断纪律**集中在这里，供两个 opt-in 模式共享——

- **Convergence Loop（`/butler:loop`）**：在 P4 上显式开启的高强度纠错升档，叠加 `[Loop #N]` 标注与「死磕」语义。
- **Dangerous Mode（`/butler:dangerous`）**：无人值守自治外壳，其 P4 执行复用本策略，但**不开启 Convergence Loop 模式**。

两者**并列**：各自保留显式入口与激活状态，互不读写对方激活状态；共同使用的只是本文件的纪律，不构成包含关系。

本策略**叠在**常驻 `correction-contract.md` 之上：底线层提供定性「诚实停」（不设硬计数器、不强制 RCA），本文件提供定量熔断（硬上限 + RCA），只对显式开启的 opt-in 模式生效。

## 2. 定量熔断纪律

出现以下任一情况，停止自主纠错并交还（不再空磨）：

- **重试上限**：连续闭环达到 5 次仍未通过。
- **死锁判定**：连续 3 次探测反馈本质一致，未真正消除偏差。
- **环境阻塞**：缺少必要命令、依赖、权限或外部条件。

## 3. RCA 输出

触发熔断后输出一份简明 RCA，写入项目 `.ai/03_BUG_LOG.md`，至少包含：

- 当前目标与受影响 AC；
- 已尝试的修复动作；
- 最近一次探测结果；
- 判断为死锁 / 阻塞的依据；
- 需要用户提供的输入或决策。

无人值守（Dangerous Mode）下，RCA 按 `65_Extension_Dangerous/dangerous-engine.md §8` 异步交还；有人场次按 `55_Extension_ConvergenceLoop/convergence-loop-engine.md` 请求介入。

## 4. 与其他规则的关系

- **常驻契约（`correction-contract.md`）**：本策略的底座；未开启任何 opt-in 模式时，P4 仍受其约束，只是用「诚实停」而非定量熔断。
- **Convergence Loop（`55_Extension_ConvergenceLoop/convergence-loop-engine.md`）**：引用本策略并叠加 `[Loop #N]` 标注与「死磕」语义；激活仍由 `/butler:loop` 显式触发。
- **Dangerous Mode（`65_Extension_Dangerous/dangerous-engine.md`）**：引用本策略用于其 P4；激活仍由 `/butler:dangerous` 显式触发，状态由 project-config `dangerous` 承载。
- **探测内容**：由 `30_Quality_Gate/linting.md` / `testing-strategy.md` / `review-standard.md` 定义；本文件只定义「何时熔断、如何交还」。
