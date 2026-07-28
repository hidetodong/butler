# 迭代台账

> ⚠️ 危险模式自治：MILE-0013 将项目级 Butler 机器配置从 `.ai/local-constraints.md` 拆到顶层扁平的 `.ai/butler.config.json`，完成兼容迁移和全链路切换。

## 危险模式自治路线图

ITER-0095 归属 MILE-0013 R3：全消费端统一接线、当前仓迁移、3.3.0 版本链与完整发布验证。

current: none

| 迭代号 | 标题 | 状态 | 开启 | 收口 | 所属 milestone | 交付 |
|---|---|---|---|---|---|---|
| ITER-0095 | Butler 配置全链路接线与 3.3.0 发布准备（MILE-0013 R3·危险模式） | closed | 2026-07-28 | 2026-07-28 | MILE-0013 | deliveries/ITER-0095-project-config-consumers.md |
| ITER-0094 | Butler 配置部署与 legacy 迁移（MILE-0013 R2·危险模式） | closed | 2026-07-28 | 2026-07-28 | MILE-0013 | deliveries/ITER-0094-project-config-migration.md |
| ITER-0093 | Butler 项目配置合同与统一读写内核（MILE-0013 R1·危险模式） | closed | 2026-07-28 | 2026-07-28 | MILE-0013 | deliveries/ITER-0093-project-config-core.md |
| ITER-0092 | TDD 配对收口接线与 pytest dogfood（MILE-0012 R2·危险模式） | closed | 2026-07-26 | 2026-07-26 | MILE-0012 | deliveries/ITER-0092-tdd-goal-gate-dogfood.md |
| ITER-0091 | 轻量 TDD 配对合同与检查器（MILE-0012 R1·危险模式）：cycle 声明、稳定 evidence ID、顺序/outcome/argv/cwd 校验与负向 fixture | closed | 2026-07-25 | 2026-07-25 | MILE-0012 | deliveries/ITER-0091-lightweight-tdd-pair-checker.md |
| ITER-0090 | /butler:setup 机器级安装命令：双宿主入口、显式确认、setup.sh 复用与 registry 分发 | closed | 2026-07-23 | 2026-07-23 | — | deliveries/ITER-0090-butler-setup-command.md |
| ITER-0089 | 五件套兼容迁移与非回归：正文保留、legacy、幂等 fixture 与真实仓 dogfood（MILE-0011 R4） | closed | 2026-07-23 | 2026-07-23 | MILE-0011 | deliveries/ITER-0089-artifact-migration-dogfood.md |
| ITER-0088 | 五件套校验与门禁：零写检查器、hook、状态审计、CI 与双宿主接线（MILE-0011 R3） | closed | 2026-07-23 | 2026-07-23 | MILE-0011 | deliveries/ITER-0088-artifact-structure-gates.md |
| ITER-0087 | 五件套阶段生成器：按阶段生成/重置骨架并保护已有正文与边界（MILE-0011 R2） | closed | 2026-07-23 | 2026-07-23 | MILE-0011 | deliveries/ITER-0087-artifact-stage-generator.md |
| ITER-0086 | 五件套结构合同：机器真源、模板版本、固定字段/段落/顺序与 N/A 规则（MILE-0011 R1） | closed | 2026-07-23 | 2026-07-23 | MILE-0011 | deliveries/ITER-0086-artifact-structure-contract.md |
| ITER-0085 | 真正的 ITER/MILE 区间分片纠偏（MILE-0010 后续）：固定范围冷分片、索引导航、定向读取、跨分片审计与兼容迁移 | closed | 2026-07-23 | 2026-07-23 | — | deliveries/ITER-0085-fixed-range-state-ledger-shards.md |
| ITER-0084 | 长编号、双台账热冷分层与规模迁移（MILE-0010 R2–R4·危险模式）：数值身份、机器索引、有界热表、冷历史、幂等迁移与万级验证 | closed | 2026-07-22 | 2026-07-22 | MILE-0010 | deliveries/ITER-0084-scalable-state-ledgers.md |
| ITER-0083 | handoff 确定性可信闭环（MILE-0010 R1·危险模式）：状态快照读取层、固定生成、触发/检查、来源指纹、陈旧拒绝与重建 | closed | 2026-07-22 | 2026-07-22 | MILE-0010 | deliveries/ITER-0083-trusted-handoff.md |
| ITER-0082 | 工作区范围发现、计划/改动门禁与端到端验证（MILE-0009 R8·危险模式）：稳定地图发现、TECH_PLAN 对账、实际改动/hook 拦截、真实 apps 只读样本迁移回归 | closed | 2026-07-22 | 2026-07-22 | MILE-0009 | deliveries/ITER-0082-workspace-scope-gate-e2e.md |
| ITER-0081 | 确定性 PRD 改版执行与回执（MILE-0009 R7·危险模式）：显式 prd_id/spec、先冻后更事务、模块认亲、三态影响与处置、verify/rollback/幂等 | closed | 2026-07-22 | 2026-07-22 | MILE-0009 | deliveries/ITER-0081-prd-update-transaction.md |
| ITER-0080 | 首切、状态与命令适配（MILE-0009 R6·危险模式）：身份四态先于写盘、按 prd_id/date 目录首切、只读 status 与 workspace 下钻、双宿主薄路由 | closed | 2026-07-22 | 2026-07-22 | MILE-0009 | deliveries/ITER-0080-prd-split-status.md |
| ITER-0079 | 多 PRD 引用、兼容迁移与人类指南（MILE-0009 R5·危险模式）：多需求钉版、legacy 显式迁移/回滚、历史引用解析与独立操作指南 | closed | 2026-07-22 | 2026-07-22 | MILE-0009 | deliveries/ITER-0079-multi-prd-migration.md |
| ITER-0078 | /butler:inbox 命令与分类路由（MILE-0009 R4·危险模式）：确定性扫描、幂等 INBOX 写入、双宿主入口、确认路由与活工作区保护 | closed | 2026-07-22 | 2026-07-22 | MILE-0009 | deliveries/ITER-0078-butler-inbox-workflow.md |
| ITER-0077 | 收件箱数据契约（MILE-0009 R3·危险模式）：origin 只读边界、INBOX 来源身份/指纹/状态、派生关系与幂等变更检测 | closed | 2026-07-22 | 2026-07-22 | MILE-0009 | deliveries/ITER-0077-inbox-data-contract.md |
| ITER-0076 | Monorepo 工作区地图与需求级范围契约（MILE-0009 R2·危险模式）：稳定工作区键、路径映射、四类范围与越界扩张纪律 | closed | 2026-07-22 | 2026-07-22 | MILE-0009 | deliveries/ITER-0076-workspace-scope-contract.md |

> 备注：ITER-0001 是迭代机制上线前完成的任务，回溯补号；其交付文件沿用上线前的日期命名，不回溯重命名。迭代机制自 ITER-0002 起正式生效。
