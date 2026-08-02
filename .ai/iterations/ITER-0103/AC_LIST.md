---
状态: ack-frozen
ACK 日期: 2026-08-01
---
<!-- butler-artifact-template: 1.0.0 artifact=acceptance -->
# AC_LIST — ITER-0103

## Goal

- 为 Butler 建立一个不依赖模型临场判断的本地 Decision Map 状态 Module：探索决策、依赖、Frontier 与协作领取均由封闭合同和确定性转换管理，并能在进程退出后从磁盘完整恢复。

## In Scope

- 每张 Map 的单一原子 `state.json` 真源、schema 版本、revision 与目录扫描发现。
- Map、Decision、Fog、Dependency、Claim Lease 与派生 Frontier 的数据合同和合法转换。
- `inspect / plan / apply / verify` 外部 Interface，以及 create、link、claim、renew、release、resolve、graduate、dismiss、abandon、close 等 operation spec。
- 同一文件系统内的并发冲突、幂等重试、失效 lease 回收、失败零半状态和跨会话恢复。
- 面向合同的自动测试、命令帮助与 Butler 权威文档接线。

## Out of Scope

- 不新增 Explore 用户入口，不改变 R1 已冻结的 opt-in / suggest-only 边界，也不实现清晰度或需求大小分类器。
- 不实现研究 helper 或多 agent 调度（MILE-0014 R3）。
- 不把 Decision Map promotion 接入 Milestone / Iteration admission（R4），不让 Decision Map 覆盖交付期真源。
- 不实现 Standard Router dogfood（R5）、远端数据库、跨主机分布式锁或云端同步。

## Acceptance Checklist

- [x] AC1: 每张 Map 只以 `.ai/decision-maps/DMAP-NNNN/state.json` 作为可写真源，含显式 schema version、map identity、revision、Map 状态及 Decision/Fog 集合；Map 列表由目录扫描派生，不存在第二份全局可写索引。
- [x] AC2: 数据合同只接受 Map `open / closed`、Decision `open / resolved / abandoned`、Fog `open / graduated / dismissed`；ID 重复、跨 Map 引用、悬空依赖、环、非法枚举及“open Decision 依赖 abandoned Decision”均 fail-closed 且不改文件。
- [x] AC3: Frontier 不落盘，查询时严格派生为“Decision 为 open、全部 `depends_on` 已 resolved、当前无有效 Claim”；过期 Claim 在所有查询和转换中逻辑上等于不存在，相同磁盘状态与相同时钟必得相同结果。
- [x] AC4: Claim 只能领取 Frontier Decision，并返回 owner、不可伪造的 token 与 UTC 到期时间；renew/release/已领取 Decision 的 resolve 均校验 owner + token，过期或被重新领取后的旧 token 不能续租、释放或完成。未领取的 Frontier Decision 允许协调器直接 resolve。
- [x] AC5: Dependency 仅存同 Map `depends_on` 单向边并保持 DAG；存在 open dependent 时不能把其前置 Decision abandon。Map 只有在不存在 open Decision 和 open Fog 时才能 close，关闭后除 inspect/verify 外的状态转换全部拒绝。
- [x] AC6: Fog graduation 能在一个事务中把一个 open Fog 标为 graduated 并创建一个或多个合法 Decision；任一新 Decision、依赖或状态不合法时整次操作失败且 Map 字节不变。dismiss 与重复 graduation 等非法转换同样 fail-closed。
- [x] AC7: Module 对调用者只暴露 `inspect / plan / apply / verify` 四个动作；`plan` 零写并返回规范化 operation spec、base revision 与 digest，`inspect`/`verify` 零写，具体状态转换不扩张为一组浅层外部命令。
- [x] AC8: `apply` 在 Map 文件锁内校验 schema、base revision/digest 和 operation ID，再以原子替换提交一次 revision；冲突或中途失败不留下临时/半写状态，同一 operation ID 的相同请求可幂等重试并返回既有结果，不同请求复用 ID 必须拒绝。
- [x] AC9: 新进程只凭 Map 目录中的持久状态即可恢复 Map、有效 Claim、依赖与相同时钟下的 Frontier；verify 能以机器可读结果报告合同错误，状态判断不读取 prompt、对话记忆或模型置信度。
- [x] AC10: R1 的唯一自然语言入口、opt-in、suggest 零写、显式 promotion 与交付期真源优先级保持不变；R2 的工具和文档不得创建 Milestone/Iteration、写 P1→P5 四件套或引入自动清晰度/大小分流。
- [x] AC11: 自动测试覆盖正常生命周期、DAG/非法引用、lease 到期与 stale token、revision 冲突、operation 幂等、Fog 原子 graduation、关闭只读、跨会话恢复及故障注入；专项测试、权威文档合同检查、Markdown 链接检查、`git diff --check` 与完整 `scripts/verify-ci.sh` 全部通过。

## Verification Method

- AC1: 使用临时项目创建至少两张 Map，检查目录、schema 和 revision；删除进程内缓存后目录扫描结果仍准确，并静态确认无全局可写索引。
- AC2: 参数化合同测试逐项提交合法/非法枚举、重复 ID、跨 Map/悬空/成环依赖和 abandoned dependency，比较失败前后文件哈希。
- AC3: 用可注入时钟覆盖依赖未完成、已完成、有效 claim、恰好到期与过期场景；断言 state 文件不含 Frontier 投影且重复计算一致。
- AC4: 双 worker 测试领取冲突、续租、释放、过期重领、stale token 完成拒绝及未领取协调器直解。
- AC5: DAG 转换测试验证 open dependent 对 abandon 的阻断；分别以未收敛/已收敛 Map 测试 close，并检查 closed Map 的所有写 operation 拒绝。
- AC6: Fog 生成单个/多个 Decision 的成功测试与非法依赖故障注入测试，检查状态、revision 和文件哈希的原子性。
- AC7: Interface 合同测试枚举仅四个外部动作；对 inspect/plan/verify 前后做目录快照，确认零写并检查 plan 输出字段完整。
- AC8: 并发进程与故障注入测试覆盖 stale revision、digest 不符、相同/冲突 operation ID、锁内竞争、替换失败及残留临时文件。
- AC9: 进程 A 写入含依赖和 claim 的 Map，进程 B 冷启动读取并在同一 clock 下比较规范化 inspect/Frontier；向损坏文件运行 verify 并检查非零退出与机器结果。
- AC10: 扩展 R1 静态合同测试，断言 R2 无新 Explore ID/入口、无自动 routing/promotion 写入，并检查 Milestone/Iteration/四件套路径字节不被 Decision Map operation 改动。
- AC11: 归档专项测试、合同测试及完整 CI 的机器证据，运行链接检查、registry 检查和 `git diff --check`，逐项映射 AC1–AC10。

## External References

- N/A

## Open Questions / Risks

- AC4 的“不可伪造 token”按高熵随机、不可预测且精确匹配验收，不把本地 lease 提升为安全认证机制。
- R2 只承诺同一文件系统内的协调；网络文件系统锁语义与跨主机一致性明确不在本轮保证范围。
