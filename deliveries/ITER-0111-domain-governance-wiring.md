# ITER-0111 · 领域治理接线与真实 dogfood（MILE-0015 R5）

- 交付级别：迭代交付（小版本）
- 收口日期：2026-08-17
- 所属里程碑：MILE-0015（Butler 领域模型治理）

## 本次交付目标

前四轮把领域模型建起来了，但它只在 butler 仓自己的一条路径上生效：改了领域定义没人拦，Codex 入口和部署项目根本不知道有这套渐进读取规则，发布时也没说部署项目要不要跟。这一轮把这三处接线补上，再用本迭代自身量一次成本，回答「这套治理值不值得继续」。

## 已完成内容

- 评审多了一维「领域变更」：命中领域文件时必须显式声明唯一所有者、兼容影响、迁移路径、负向样例，缺一条按 Must Fix 处理。口径归 `review-standard.md §5` 独占，`review-engine.md` 只登记名字和指针。
- 领域合同检查器加了条目覆盖门：登记了却没有任何断言或关系能抓住它变坏，直接判失败并指名条目。
- L0 渐进读取内核从只存在于 `Coder/README.md`，变成三处字节一致——加上 Codex 入口 `AGENTS.md` 和部署项目用的 `templates/rule-card.md`，任一处被单独改动都会被 CI 抓住并指出是哪一份不一致。
- 迁移配方规范补了「领域变更的升级处置」判据：哪类改动对部署项目无影响、哪类必须重新生成宿主入口，无影响也要显式写进「不需要动作」。
- 新增 9 条 fixture 与 5 条常驻断言，全部接进完整 CI。

## 关键变更 / 用户可感知变化

- **部署项目冷启动会多读一段约 234 token 的读取纪律**（占规则卡全文 3.8%）：撞上领域术语时按分层读，而不是全量吞。
- **覆盖门一开就抓到两条真缺口**：`four-state-machine-code`（四态机器码 pass/fail/defer/skip）和 `bridge-manifest-results-json`（人测桥输入输出契约）此前完全没有任何断言或关系锚住。已补真断言，不是放宽判定。
- **下个发布版必须含 `[regen-entrypoints]`**：因为改了 `templates/rule-card.md`，已部署项目不重新生成入口就拿不到新的 L0，不得记 `[no-op]`。

## 高层影响范围

- 新增章节：`review-standard.md §5`、`migration-schema.md §5`（原 §5/§6 顺延为 §6/§7）。
- 修改工具：`tools/domain-contract/`（覆盖门 + 5 条断言 + 6 例 fixture）、`tools/context-budget/`（三处一致校验 + 3 例 fixture）。
- 修改入口：`Coder/README.md`、`AGENTS.md`、`templates/rule-card.md` 各含一份同源 L0 块。
- 顺延修正：`project-digest-schema.md` 两处 `migration-schema.md §6` 改为 `§7`（全仓唯一受影响的活引用）。
- 未触碰 MILE-0014 的 Decision Map / Work / Promotion 状态机，未改任何命令、路径与状态值。

## 验证方式与结果摘要

- 9/9 AC 全绿（auto·可靠），7 条 evidence record 全部 passed，完整 `verify-ci.sh` 退出码 0，`git diff --check` 干净，Goal 裁决 `eligible`。
- 过程中 Goal 门先判过一次 `ineligible`——AC1 与 AC6 只有规则正文、没有机器证据，被拒绝按口头结论打绿。处理方式不是补一次性 grep，而是把三份文件的结构锚点注册成常驻断言，进 CI 每次跑。
- 三层导航实测体量：L0 656 字节 / L1 3966 字节 / L2 术语表 5456 字节 / L2 转换合同 6163 字节。token 数为换算值（中文约 0.9 token/字符），非 tokenizer 实测。

## 已知剩余风险 / 延后事项

- **证明不了宿主真的按 L0 分层读了**。能证明三处字节一致、能证明 L0 进了部署入口，但没有任何运行时观测能说明某个宿主在真实会话里确实照它分层读取。这是 R5 定义里「衡量歧义减少」最实的那一半，本轮拿不到，已划给 `butler-slim-down` 候办的 usage instrumentation。
- **机器只能查声明在不在，查不出想没想对**。四项声明里「兼容影响」和「迁移路径」写得对不对、有没有漏掉依赖方，机器判不了，执行仍靠自觉。
- **覆盖门是文件级粒度**。将来若有条目蹭同文件的无关断言，门会误判为已覆盖。
- **dogfood 样本只有一个迭代**，不构成普遍结论。

## 引用

- `.ai/iterations/ITER-0111/CONCEPT.md`
- `.ai/iterations/ITER-0111/AC_LIST.md`
- `.ai/iterations/ITER-0111/TECH_PLAN.md`
- `.ai/iterations/ITER-0111/VERIFY_REPORT.md`
- `.ai/iterations/ITER-0111/evidence/`
