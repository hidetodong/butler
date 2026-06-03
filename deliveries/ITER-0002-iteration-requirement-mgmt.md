# ITER-0002 · 迭代化需求管理

## 本次交付目标
- 给 butler SOP 加一层"迭代"：增量迭代中每个迭代有确定的单调递增迭代号 `ITER-NNNN`，落下对应文档，并锁定该迭代的需求范围，使每个迭代可追溯、可审计、可复盘。

## 已完成内容
- 新增机制 SSOT `Coder/20_Workflow_Lifecycle/iteration-schema.md`：定义迭代号格式、`.ai/ITERATIONS.md` 台账字段、"工作区 / 归档 / 交付"三层落盘关系，以及开启 / 冻结 / 修订 / 扩张 / 收口 / 废弃六态锁定纪律。
- `lifecycle.md` 五处接入：P1 开启迭代、P2 ACK 即冻结、§4 工作区与归档关系、P5 收口三步、§5 修订 vs 扩张分流。
- `mcv-deployment.md §2`：`ITERATIONS.md` 列入运行态文件，四件套标注为"当前迭代工作区"，`iterations/` 归档目录首次收口时按需产生。
- `delivery-summary.md`：命名口径改为 `deliveries/ITER-NNNN-<slug>.md`，§7、§8.4 与收口三步对齐。
- `README.md` 注册新文件，`templates/rule-card.md` 新增"迭代化需求"精简段（经占位符自动透传到 `CLAUDE.md.template`）。
- dogfood：把原 `chat-recap-style` 四件套归档为 ITER-0001，本次为 ITER-0002，建台账、归档、交付、收口端到端跑通。

## 关键变更 / 用户可感知变化
- 以后每个迭代开头会领一个 `ITER-NNNN` 号写进 `.ai/ITERATIONS.md`；工作区四件套始终代表"当前迭代"，收口时快照进 `.ai/iterations/ITER-NNNN/` 并落一份 `deliveries/` 交付。
- "固定需求"口径：AC 一旦 ACK 即冻结，迭代内只允许小幅修订（重新 ACK + 修订记录），影响面扩大必须开新迭代号。

## 高层影响范围
- 规则层：`Coder/20_Workflow_Lifecycle/`（新增 1 + 改 3）、`Coder/README.md`、`templates/rule-card.md`。
- hook 体系零改动：工作区保持固定路径，`phase_gate` 校验路径不变，`.ai/iterations/` 与 `deliveries/` 仍在 `is_gated` 豁免区。

## 验证方式与结果摘要
- 逐文件阅读核对新增/修改段落与 AC1–AC5 映射：全部命中。
- `git status -- templates/hooks/` 为空 + `lib/io.py` 豁免名单复核：hook 零改动确认（AC6）。
- `.ai/iterations/` 目录树与 `.ai/ITERATIONS.md` 两行、`deliveries/` 文件一一对应，`current: none` 与状态列一致：dogfood 三层自洽（AC7）。
- 结论：AC1–AC7 全绿，迭代闭合。

## 已知剩余风险 / 延后事项
- 迭代纪律目前是规则约束，hook 不校验台账一致性；台账一致性 linter 列为 ITER-0003 候选增量。
- 台账长期增长后需按 `mcv-update.md` 归档冷行；当前仅 2 行，未触发。

## 可选引用
- `.ai/AC_LIST.md` / `.ai/TECH_PLAN.md` / `.ai/VERIFY_REPORT.md`（已快照至 `.ai/iterations/ITER-0002/`）
- `Coder/20_Workflow_Lifecycle/iteration-schema.md`
