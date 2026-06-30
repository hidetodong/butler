# 四件套讲人话 + 反啰嗦：新增产物书写口径

> ITER-0012 · 迭代交付（小版本） · 收口 2026-06-30

## 本次交付目标

- 四件套（CONCEPT / AC_LIST / TECH_PLAN / VERIFY_REPORT）写出来的内容太像内部机器日志：堆满只有 butler 自己懂的黑话，还经常把一件事重述好几遍。
- 这次给它们补一条"内容怎么写"的纪律——讲人话、不啰嗦——但**字段结构一字不动**。

## 已完成内容

- 新增一份书写口径 `Coder/20_Workflow_Lifecycle/artifact-style.md`，定两条原则：
  - **讲人话**：字段正文要让不懂 butler 内部机制的人也读得懂；能用大白话就别用黑话；真要指某个机制（如 schema、ack-frozen）就点名再加一句解释，不让读者自己猜。
  - **不啰嗦**：一律 bullet、嵌套不超 2 层、不复述模板提示语和上一阶段已写过的内容、没有的字段就写"无"；升级信号只列名不加括号小作文；验证报告用 `[x] ACn ✓ 一句话证据` 不重抄原文。
  - 附了两组取自真实历史产物的 before / after 对照，可直接照抄。
- 把这条口径接到了四个 schema（各加一行指针引用，单一来源不重复）、浓缩规则卡 `rule-card.md`（AI 最先读到的地方）、以及 `Coder/README.md`（注册新文件）。

## 关键变更 / 用户可感知变化

- 从此以后新产出的四件套会明显更像人话、更短，读起来不再像内部日志。
- 字段名、AC 编号、文件路径等结构锚点保持不变，产物链逐阶段读取不受影响；老项目不升级也能照常用（向后兼容）。
- 本迭代自己的四件套就是按新口径写的，可直接当样板对照。

## 高层影响范围

- 规则层：新增 1 个文件，改动四个 schema 的"编写规则"段、rule-card、README。
- 没碰：四件套字段结构、lifecycle 的分流行格式、对话层规则（presentation-protocol、delivery-summary §8）、hook 体系、迭代 / 里程碑 / 版本机制、历史已归档产物。

## 验证方式与结果摘要

- 10 条验收项全部满足：新文件六节齐全、四个 schema 与 rule-card、README 接线点 grep 全中。
- dogfood 核对：本迭代四件套已无黑话 filler、无整段重述（反面词只出现在"举例说明它们"的地方）。
- 本仓 CLAUDE.md 五条编辑约束逐项自检通过。
- 详见验证报告与四件套（见下方引用）。

## 已知剩余风险 / 延后事项

- 这条口径靠 AI 会话起始读取并遵守，没有 hook 机械强制——和 identity、presentation-protocol 一样，可接受。
- "讲人话"和"必要的机制名"之间的边界靠语义判断，有一定模型自由度，用 before / after 例子兜底。
- 本轮不切版，ITER-0012 累积到下次发布，预计是 MINOR（新增可选规则、向后兼容）。

## 引用

- `.ai/iterations/ITER-0012/CONCEPT.md`
- `.ai/iterations/ITER-0012/AC_LIST.md`
- `.ai/iterations/ITER-0012/TECH_PLAN.md`
- `.ai/iterations/ITER-0012/VERIFY_REPORT.md`
- 新增规则：`Coder/20_Workflow_Lifecycle/artifact-style.md`
