# Butler Explore 决策地图接入

## 本次交付目标

把 Wayfinder 值得借鉴的“决策问题、依赖图、当前 Frontier、跨会话恢复”能力接入 Butler，同时守住单一入口、显式 opt-in 和原有 Milestone / Iteration 交付生命周期。

## 已完成内容

- R1 冻结 Explore / Decision Map 的边界：它是既有 Ideation 的可选持久化深度，不是新入口或 P1 前置阶段。
- R2 交付本地 Decision Map 状态机，覆盖 DAG、Frontier、Fog、Claim Lease、幂等、并发和跨进程恢复。
- R3 交付不可变 Decision Work sidecar，允许独立 Research 受控并行，但所有结果必须由协调器显式 absorb。
- R4 交付 Decision Promotion，以 `route-reference` / `iteration-start` 把 resolved slice 显式接回既有路线或 Iteration P1。
- R5 完成 Router 接线与 Butler 真实 dogfood，保留快路径，验证恢复、错误路线、Research 执行事实与维护开销。

## 关键变更 / 用户可感知变化

- Butler 仍只有一个自然语言入口；Explore 只在用户主动要求，或用户接受带具体 blocker 的零写建议后启用。
- Decision Map 只拥有探索期决策状态。Milestone 继续拥有版本范围与路线，Iteration 继续独占 P1→P5、冻结 AC、实现和验收。
- Map 不必整体结束才可交付；用户可以显式选择已解决且依赖闭合的 slice，引用到既有 planned route，或从 P1 开一个 Iteration。
- 系统不根据模型给出的清晰度、大小或置信度静默建 Map、Milestone、Iteration，也没有新增 Wayfinder / Explore workflow ID。
- 真实 dogfood 证明了单机跨会话恢复和 fail-closed 交接，但没有观察到实际 Research 并行提速，因此外部 tracker 继续延后。

## 高层影响范围

- Explore / Ideation、Router、Milestone、Iteration 与 P1→P5 之间的领域边界。
- `tools/decision-map/`、`tools/decision-work/`、`tools/decision-promotion/` 三个确定性 Module。
- Claude、Codex、Pi 薄适配与共享 registry / CI 合同。
- Butler 自身的真实 Decision Map、dogfood 报告、验证证据与项目知识文件夹。

## 拆分路线图回填

| 路线 | 交付切片 | 承接迭代 | 结果 |
|---|---|---|---|
| R1 | Explore / Decision Map 边界合同 | [ITER-0102](../ITER-0102-explore-decision-map-boundary.md) | closed |
| R2 | Decision Map 本地合同与确定性状态机 | [ITER-0103](../ITER-0103-decision-map-local-state-machine.md) | closed |
| R3 | Decision Work helper 与单写者吸收合同 | [ITER-0104](../ITER-0104-decision-work-helper-contract.md) | closed |
| R4 | Decision Map 到 Milestone / Iteration 的确定性交接 | [ITER-0105](../ITER-0105-decision-promotion-bridge.md) | closed |
| R5 | Router 接线与 Butler 真实 dogfood | [ITER-0106](../ITER-0106-explore-router-dogfood.md) | closed |

## 验证方式与结果摘要

- 五个承接迭代全部 closed，各自有四件套/变更流归档、Markdown + HTML 交付、机器 evidence 与 fold receipt。
- 三个 Decision Module 共 53 项专项测试，Router 13 项、dogfood 4 项以及双宿主/三宿主完整矩阵通过。
- live `DMAP-0001` 的三个 Decision 均 resolved，两个 Attempt absorbed，一个 Fog 保留；新进程可一条命令恢复。
- live promotion 对已绑定 R5 返回 `route_unavailable`，无 receipt、零语义写；隔离 fixture 的合法 apply/replay/verify 通过。
- ITER-0106 P5 同上下文简评 Must Fix 0、Should Fix 0；关闭态项目审计与路线/台账对账通过。

## 已知剩余风险 / 延后事项

- 任意自然语言路由仍由宿主模型理解；显式 trigger 和代表 corpus 不能等同于生产误路由率。
- Research dogfood 实际为 serial、非 fresh-context，没有证明并行带来时间收益。
- 尚无跨机器、多人写入、查询通知或长期规模的实证阻塞，外部 tracker 裁决保持 `defer`。
- `FOG-0001` 与 deferred 结构化提问卡片候办保留为未来参考，不自动开启新的 Milestone / Iteration。
- 项目配置未启用独立复核；各迭代使用同上下文简评与机器复现证据收口。

## 引用

- `.ai/milestones/MILE-0014/MILESTONE.md`
- `deliveries/ITER-0102-explore-decision-map-boundary.md`
- `deliveries/ITER-0103-decision-map-local-state-machine.md`
- `deliveries/ITER-0104-decision-work-helper-contract.md`
- `deliveries/ITER-0105-decision-promotion-bridge.md`
- `deliveries/ITER-0106-explore-router-dogfood.md`
- `docs/explore-dogfood-r5.md`
