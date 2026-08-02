<!-- butler-artifact-template: 1.0.0 artifact=concept -->
> 分流: 完整 | 命中升级信号: 契约变更、多文件改动、跨模块影响、设计取舍 | 2026-08-01

# CONCEPT — ITER-0103 · Decision Map 本地合同与确定性状态机（MILE-0014 R2）

## Current Understanding

- 在 R1 已冻结的 opt-in 与真源边界上，为 Decision Map 建立本地优先、可校验、可跨会话恢复的最小数据合同和确定性状态转换；本迭代只建设探索状态底座，不接 Milestone/Iteration promotion。
- 已确认：MILE-0014 R1 已关闭，下一条承接路线是 R2。
- 已确认：Decision Map 只拥有探索期决策状态，仍位于 P1→P5 之外；普通任务快路径和 suggest-only 入口边界不变。
- 已确认：R2 覆盖地图/决策文件、依赖 DAG、Frontier、claim lease、resolve、Fog graduation、校验与跨会话恢复。
- 已确认：每张 Map 使用 `.ai/decision-maps/DMAP-NNNN/state.json` 作为唯一可写真源；不建全局可写索引，列表由目录扫描派生。单文件状态用锁 + revision + 原子替换保证一次转换不留下多文件半状态，目录为后续证据或投影保留扩展位。
- 已确认：Map 只设 `open / closed`；Decision 只设 `open / resolved / abandoned`；Fog 只设 `open / graduated / dismissed`。Claim 是带 owner、token、UTC 到期时间的 lease，不是 Decision 状态；Frontier 永远由“open + 依赖全 resolved + 无有效 claim”计算，不持久化。
- 已确认：Fog graduation 可在一次原子操作中生成一个或多个 Decision；Dependency 只存 `depends_on` 单向边，最终状态必须同 Map 引用、无环，且 open Decision 不得依赖 abandoned Decision。
- 已确认：工具只暴露 `inspect / plan / apply / verify` 四个外部动作；具体 create、link、claim、renew、release、resolve、graduate、abandon 等作为 plan spec 内部 operation。`plan` 零写并返回 base revision / digest，`apply` 在文件锁内校验 revision 和 operation id 后原子提交，重复 operation id 幂等返回既有结果。
- 已确认：lease 使用可注入的 UTC clock；过期 claim 逻辑上等于不存在，续租必须 owner + token 匹配且未过期，旧 worker 在过期或被重新领取后不能 resolve。未被 claim 的 Frontier Decision 允许协调器直接 resolve；存在有效 claim 时必须持匹配 token。

## Scope

- 定义 Decision Map、Decision/Fog、依赖边、Frontier 与 claim lease 的本地数据合同。
- 实现确定性的创建、校验、claim、resolve、Fog graduation、过期恢复和只读状态查询。
- 验证依赖 DAG 无环、Frontier 可重建、非法转换 fail-closed、写入幂等且失败不留半状态。
- 提供跨会话恢复所需的最小索引、摘要和可审计状态。

## Open Questions / Risks

- P1 已于 2026-08-01 获用户 ACK，无遗留开放问题。
- 风险：本地文件锁只解决同一文件系统内的并发写入，不把 R2 表述为跨主机分布式协调能力。
