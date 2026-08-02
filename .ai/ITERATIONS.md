# 迭代台账

> Butler 统一语义 Router 与会话转迭代入口：共享路由真源，为 Claude 与 Codex / ChatGPT 提供薄适配，并把「总结当前 session 后领取迭代」收敛为标准 Butler 工作流。

## 最近迭代

ITER-0100 为独立迭代：收敛 Claude 与 Codex / ChatGPT 的 Butler 统一语义路由，新增会话转迭代工作流；不改现有业务算法，不将 loop / dangerous 放开为隐式调用。

current: none
| 迭代号 | 标题 | 状态 | 开启 | 收口 | 所属 milestone | 交付 |
|---|---|---|---|---|---|---|
| ITER-0106 | Explore Router 接线与 Butler 自身 dogfood（MILE-0014 R5） | closed | 2026-08-02 | 2026-08-02 | MILE-0014 | deliveries/ITER-0106-explore-router-dogfood.md |
| ITER-0105 | Decision Map 到 Milestone / Iteration 的确定性交接 | closed | 2026-08-01 | 2026-08-02 | MILE-0014 | deliveries/ITER-0105-decision-promotion-bridge.md |
| ITER-0104 | Decision Map 决策工作 helper 与单写者吸收合同（MILE-0014 R3） | closed | 2026-08-01 | 2026-08-01 | MILE-0014 | deliveries/ITER-0104-decision-work-helper-contract.md |
| ITER-0103 | Decision Map 本地合同与确定性状态机（MILE-0014 R2） | closed | 2026-08-01 | 2026-08-01 | MILE-0014 | deliveries/ITER-0103-decision-map-local-state-machine.md |
| ITER-0102 | Explore 与 Decision Map 边界合同（MILE-0014 R1） | closed | 2026-08-01 | 2026-08-01 | MILE-0014 | deliveries/ITER-0102-explore-decision-map-boundary.md |
| ITER-0101 | 修复 Butler 插件刷新运行时与错误码回声 | closed | 2026-08-01 | 2026-08-01 | — | deliveries/ITER-0101-plugin-refresh-runtime-fix.md |
| ITER-0100 | Butler 统一语义 Router 与会话转迭代入口 | closed | 2026-08-01 | 2026-08-01 | — | deliveries/ITER-0100-semantic-router-session-intake.md |
| ITER-0099 | 升级器 hook 树摘要与部署文件集对齐：修复 sync_hooks 失配 | closed | 2026-08-01 | 2026-08-01 | — | deliveries/ITER-0099-hook-tree-digest-alignment.md |
| ITER-0098 | 开源就绪：README、许可证与社区协作入口 | closed | 2026-07-31 | 2026-07-31 | — | deliveries/ITER-0098-open-source-readiness.md |
| ITER-0097 | 沟通风格正本瘦身：砍冗余留例子，守 artifact-style 四条对齐 | closed | 2026-07-30 | 2026-07-30 | — | deliveries/ITER-0097-communication-style-slim.md |
| ITER-0096 | 旁路工作回执协议（危险模式） | closed | 2026-07-29 | 2026-07-29 | — | deliveries/ITER-0096-sidework-receipt.md |
| ITER-0095 | Butler 配置全链路接线与 3.3.0 发布准备（MILE-0013 R3·危险模式） | closed | 2026-07-28 | 2026-07-28 | MILE-0013 | deliveries/ITER-0095-project-config-consumers.md |
| ITER-0094 | Butler 配置部署与 legacy 迁移（MILE-0013 R2·危险模式） | closed | 2026-07-28 | 2026-07-28 | MILE-0013 | deliveries/ITER-0094-project-config-migration.md |
| ITER-0093 | Butler 项目配置合同与统一读写内核（MILE-0013 R1·危险模式） | closed | 2026-07-28 | 2026-07-28 | MILE-0013 | deliveries/ITER-0093-project-config-core.md |
| ITER-0092 | TDD 配对收口接线与 pytest dogfood（MILE-0012 R2·危险模式） | closed | 2026-07-26 | 2026-07-26 | MILE-0012 | deliveries/ITER-0092-tdd-goal-gate-dogfood.md |
| ITER-0091 | 轻量 TDD 配对合同与检查器（MILE-0012 R1·危险模式）：cycle 声明、稳定 evidence ID、顺序/outcome/argv/cwd 校验与负向 fixture | closed | 2026-07-25 | 2026-07-25 | MILE-0012 | deliveries/ITER-0091-lightweight-tdd-pair-checker.md |
| ITER-0090 | /butler:setup 机器级安装命令：双宿主入口、显式确认、setup.sh 复用与 registry 分发 | closed | 2026-07-23 | 2026-07-23 | — | deliveries/ITER-0090-butler-setup-command.md |
| ITER-0089 | 五件套兼容迁移与非回归：正文保留、legacy、幂等 fixture 与真实仓 dogfood（MILE-0011 R4） | closed | 2026-07-23 | 2026-07-23 | MILE-0011 | deliveries/ITER-0089-artifact-migration-dogfood.md |
| ITER-0088 | 五件套校验与门禁：零写检查器、hook、状态审计、CI 与双宿主接线（MILE-0011 R3） | closed | 2026-07-23 | 2026-07-23 | MILE-0011 | deliveries/ITER-0088-artifact-structure-gates.md |
| ITER-0087 | 五件套阶段生成器：按阶段生成/重置骨架并保护已有正文与边界（MILE-0011 R2） | closed | 2026-07-23 | 2026-07-23 | MILE-0011 | deliveries/ITER-0087-artifact-stage-generator.md |

> 备注：ITER-0001 是迭代机制上线前完成的任务，回溯补号；其交付文件沿用上线前的日期命名，不回溯重命名。迭代机制自 ITER-0002 起正式生效。
