# 迭代台账

> MILE-0015 已收口并随 v3.6.0 发布；当前 active 里程碑为 MILE-0016（Butler 瘦身与重造）。
> ITER-0107～ITER-0109 是 2026-08-04 跨设备汇合后的正式编号；开启/收口日期保留实际完成时间 2026-07-31。

## 最近迭代

ITER-0117 已收口：新建 `Coder/40_Context_Management/intake-schema.md`，把「随手记一句 → 想清楚值不值得做 → 真的开工」三层的数据形态定死——闪念口一张表加日期化闪念键（不用递增号池、不做内容指纹认亲），状态四态封闭、转移穷举四条、终态不回头；孵化区草稿头部加 `规模` 三档并按档定段落，`undecided` 必须点名「卡在哪」；执行分流三条封闭出口、两侧原子。只定数据形态不写命令（归 R7）。新旧两份契约共占 `.ai/INBOX.md`，靠新契约顶部一段生效时点声明单向分工，旧链 13 份文件逐字节未动。P3 撤回了一条已 ACK 的验收标准（待办区索引不加规模列，避免造出第二个真源），按 §5.3 走了正式修订。

current: none
| 迭代号 | 标题 | 状态 | 开启 | 收口 | 所属 milestone | 交付 |
|---|---|---|---|---|---|---|
| ITER-0119 | 退役旧 inbox 全链（MILE-0016 R8） | closed | 2026-08-21 | 2026-08-21 | MILE-0016 | deliveries/ITER-0119-retire-old-inbox-chain.md |
| ITER-0118 | /butler:inbox 命令与工具实现（MILE-0016 R7） | closed | 2026-08-20 | 2026-08-20 | MILE-0016 | deliveries/ITER-0118-inbox-command-and-tool.md |
| ITER-0117 | inbox 三层数据契约与真源（MILE-0016 R6） | closed | 2026-08-20 | 2026-08-20 | MILE-0016 | deliveries/ITER-0117-intake-three-layer-contract.md |
| ITER-0116 | /butler:loop 降级与候办清理（MILE-0016 R5） | closed | 2026-08-20 | 2026-08-20 | MILE-0016 | deliveries/ITER-0116-loop-freeze-backlog-withdrawal.md |
| ITER-0115 | 砍 /butler:progress 全链（MILE-0016 R4） | closed | 2026-08-20 | 2026-08-20 | MILE-0016 | deliveries/ITER-0115-retire-butler-progress.md |
| ITER-0114 | 项目全貌产物重建（MILE-0016 R3） | closed | 2026-08-19 | 2026-08-20 | MILE-0016 | deliveries/ITER-0114-project-overview-rebuild.md |
| ITER-0113 | 冷启动读序正式定义与四载体对齐（MILE-0016 R2） | closed | 2026-08-18 | 2026-08-19 | MILE-0016 | deliveries/ITER-0113-cold-start-read-order.md |
| ITER-0112 | 退役项目知识文件夹与折叠机制（MILE-0016 R1） | closed | 2026-08-18 | 2026-08-18 | MILE-0016 | deliveries/ITER-0112-retire-project-knowledge-folder.md |
| ITER-0111 | 领域治理接线与真实 dogfood（MILE-0015 R5） | closed | 2026-08-17 | 2026-08-17 | MILE-0015 | deliveries/ITER-0111-domain-governance-wiring.md |
| ITER-0110 | 最小可执行领域合同与双冲突试点（MILE-0015 R4） | closed | 2026-08-05 | 2026-08-13 | MILE-0015 | deliveries/ITER-0110-minimal-domain-contract.md |
| ITER-0109 | 上下文映射与主链转换合同（MILE-0015 R3） | closed | 2026-07-31 | 2026-07-31 | MILE-0015 | deliveries/ITER-0109-main-chain-context-map.md |
| ITER-0108 | 上下文预算与渐进注入（MILE-0015 R2） | closed | 2026-07-31 | 2026-07-31 | MILE-0015 | deliveries/ITER-0108-progressive-context-loading.md |
| ITER-0107 | 领域地图与语言审计（MILE-0015 R1·危险模式） | closed | 2026-07-31 | 2026-07-31 | MILE-0015 | deliveries/ITER-0107-domain-model-boundaries.md |
| ITER-0106 | Explore Router 接线与 Butler 自身 dogfood（MILE-0014 R5） | closed | 2026-08-02 | 2026-08-02 | MILE-0014 | deliveries/ITER-0106-explore-router-dogfood.md |
| ITER-0105 | Decision Map 到 Milestone / Iteration 的确定性交接 | closed | 2026-08-01 | 2026-08-02 | MILE-0014 | deliveries/ITER-0105-decision-promotion-bridge.md |
| ITER-0104 | Decision Map 决策工作 helper 与单写者吸收合同（MILE-0014 R3） | closed | 2026-08-01 | 2026-08-01 | MILE-0014 | deliveries/ITER-0104-decision-work-helper-contract.md |
| ITER-0103 | Decision Map 本地合同与确定性状态机（MILE-0014 R2） | closed | 2026-08-01 | 2026-08-01 | MILE-0014 | deliveries/ITER-0103-decision-map-local-state-machine.md |
| ITER-0102 | Explore 与 Decision Map 边界合同（MILE-0014 R1） | closed | 2026-08-01 | 2026-08-01 | MILE-0014 | deliveries/ITER-0102-explore-decision-map-boundary.md |
| ITER-0101 | 修复 Butler 插件刷新运行时与错误码回声 | closed | 2026-08-01 | 2026-08-01 | — | deliveries/ITER-0101-plugin-refresh-runtime-fix.md |
| ITER-0100 | Butler 统一语义 Router 与会话转迭代入口 | closed | 2026-08-01 | 2026-08-01 | — | deliveries/ITER-0100-semantic-router-session-intake.md |

> 备注：ITER-0001 是迭代机制上线前完成的任务，回溯补号；其交付文件沿用上线前的日期命名，不回溯重命名。迭代机制自 ITER-0002 起正式生效。
