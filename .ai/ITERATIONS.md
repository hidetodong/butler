# 迭代台账

> ⚠️ 危险模式纠偏：补齐 MILE-0010 遗漏的真正区间分片；保留旧交付事实，不把单冷文件误称为分片。

## 危险模式自治路线图

ITER-0085 独立纠偏：固定区间冷分片、索引导航、定向读取、跨分片审计与迁移。

current: none

| 迭代号 | 标题 | 状态 | 开启 | 收口 | 所属 milestone | 交付 |
|---|---|---|---|---|---|---|
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
| ITER-0075 | 需求集合与日期化身份契约（MILE-0009 R1·危险模式）：项目级 PRD 总索引、稳定 prd_id、单需求内部结构与新需求/新版身份边界 | closed | 2026-07-22 | 2026-07-22 | MILE-0009 | deliveries/ITER-0075-prd-collection-identity-contract.md |
| ITER-0074 | 仓库卫生清理：清过期 worktree 残留 + 堆积分支 + 空壳目录 + P0 审计修复（test 计数 8→10 / frontier 版本同步） | closed | 2026-07-21 | 2026-07-21 | — | deliveries/ITER-0074-repo-cleanup.md |
| ITER-0073 | /butler:progress 命令：只读聚合当前项目的结构化进度报告——里程碑、迭代、Goal、验收、执行、验证、风险一页看完 | closed | 2026-07-21 | 2026-07-21 | — | deliveries/ITER-0073-butler-progress-command.md |
| ITER-0072 | /butler:init 命令：新项目基地车一键部署 + Codex skill + registry + 同步脚本适配 | closed | 2026-07-20 | 2026-07-20 | — | deliveries/ITER-0072-butler-init-command.md |
| ITER-0071 | 说人话补「自造缩写」标准并让产物范例常驻：artifact-style §2 标准一收编掐短词/自造缩写、§6 加对照，rule-card 产物书写段加 3 组现场 ❌→✅ 范例，说准四条 SSOT 作用域 | closed | 2026-07-20 | 2026-07-20 | — | deliveries/ITER-0071-tone-plainlang-coinage.md |
| ITER-0070 | Pi 宿主适配器：TypeScript 扩展拦截 write/edit 调 Python 判断模块做流程门禁，setup.sh 安装，文档多宿主化 | closed | 2026-07-19 | 2026-07-20 | — | deliveries/ITER-0070-pi-host-adapter.md |
| ITER-0069 | 多方向候办拆分：一方向一候办键、一索引块、一草稿文件，禁止多个方向混装；状态审计 20 项与完整 CI 通过 | closed | 2026-07-19 | 2026-07-19 | — | deliveries/ITER-0069-multi-direction-backlog-splitting.md |
| ITER-0068 | 里程碑候办区与延迟编号：讨论稿不占号，开工才领号，未绑迭代的误开项可退回候办；状态审计 18 项、Goal 16 项与完整 CI 通过 | closed | 2026-07-19 | 2026-07-19 | — | deliveries/ITER-0068-milestone-backlog-numbering.md |
| ITER-0067 | 项目外写入授权边界：外部目标交宿主、坏输入 fail-closed、多项目逐根门禁；危险模式冻结授权上限，强审修复 2 Must Fix，147 hooks/完整 CI 通过 | closed | 2026-07-18 | 2026-07-18 | — | deliveries/ITER-0067-external-write-authorization-boundary.md |
| ITER-0066 | Goal 双宿主接线与端到端验证（MILE-0008 R6·危险模式）：共同单向投影、capability 降级、冷启动与驻留 CLI；强审修复外部路径，7 tests/完整矩阵通过 | closed | 2026-07-18 | 2026-07-18 | MILE-0008 | deliveries/ITER-0066-goal-dual-host-wiring.md |

> 备注：ITER-0001 是迭代机制上线前完成的任务，回溯补号；其交付文件沿用上线前的日期命名，不回溯重命名。迭代机制自 ITER-0002 起正式生效。
