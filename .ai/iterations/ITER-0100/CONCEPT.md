<!-- butler-artifact-template: 1.0.0 artifact=concept -->
# CONCEPT — ITER-0100 · 上下文预算与渐进注入（MILE-0014 R2）

分流: 完整 | 命中升级信号: 多文件改动、契约变更、跨模块影响、设计取舍 | 2026-07-31

## Current Understanding

- **一句话**：R1 的完整领域地图适合审计，但不适合每次冷启动整份植入。R2 要把“让模型知道何时查什么”与“保存完整审计细节”拆开，让初始上下文只承担高密度路由，详细定义继续按需回到真源。
- **Goal**：建立可执行的上下文预算与渐进加载合同，使普通工程冷启动只植入最小语义内核；命中 Butler 核心概念歧义时，能够按上下文、术语和少量真源逐层下钻，而不会完整加载领域审计或递归展开全部引用。
- 当前 `Coder/domain-model.md` 为 85 行、12,395 bytes，估算完整读取约 3.7k–4.5k tokens；其中 22 个真源指针若被全部展开，关联文件约 254 KB，最坏可能消耗约 70k–90k tokens。
- 当前文档混合了四种用途：初始语义植入、五上下文路由、20 项术语审计、R1 冲突反证。用途混装是主要成本来源，不是“领域模型”概念本身必然昂贵。
- 重复主要分布在 `Coder/README.md`、`Coder/architecture-overview.md`、`.ai/project/architecture.md`、`.ai/project/invariants.md`、`.ai/project/debt.md` 与各概念 schema；需要区分必要的一句路由复述和会漂移的定义重写。
- 项目是 Markdown 规则仓库，附带验证工具；本轮未命中 Domain / Stack Profile，仅按通用 SOP、产物合同与上下文治理规则推进。

## Scope

- **In Scope**：定义 L0 初始植入、L1 上下文路由、L2 术语查询、L3 完整审计四级加载模型，并为每级规定触发条件、允许内容和体量预算。
- **In Scope**：收窄 `domain-model` 触发语义，只治理 Butler 协作协议核心概念；普通业务术语和单模块实现不得误触完整领域读取。
- **In Scope**：规定一次查询只跟随与当前问题相关的少量真源，禁止批量或递归展开全部指针；为体量、术语数量和真源扇出建立确定性回归检查。
- **In Scope**：审计并消除与 README、architecture、project knowledge、debt 和各 schema 的无效重复；保留必要导航和历史可追溯性。
- **In Scope**：验证普通冷启动、单术语消歧、跨上下文设计、完整领域审查四种读取路径，各自只加载预期层级。
- **Out of Scope**：不在本轮建设 R3 的 PRD→AC→Plan→Evidence→Goal→Handoff 转换合同；不实现 R4 的机器术语 registry、dangerous/loop 修复或人测容器修复。
- **Out of Scope**：不删除 ITER-0099 归档和 evidence，不通过弱化 P1→P5、Goal、权限或验证门禁来节约上下文，不改变公开命令和运行状态语义。

## Open Questions / Risks

- **建议方向**：让 `Coder/README.md` 承担约 100–200 tokens 的 L0 路由内核；把 `Coder/domain-model.md` 收敛为约 600–1,000 tokens 的 L1 五上下文地图；20 项术语审计作为 L2 按需查询资料；R1 冲突反证回到归档与 `.ai/project/debt.md`。
- **待 P2 冻结**：20 项术语审计应拆成独立长期查询文档，还是只保留 ITER-0099 归档并让新任务直接查各 schema。前者查询方便但增加维护面，后者最省上下文但失去集中索引。
- **预算口径风险**：仓库当前没有固定 tokenizer，不能把模型相关 token 估算当机器合同。建议 CI 使用 bytes、行数、术语行数和真源指针数作为稳定代理，token 只做人读解释。
- **过度瘦身风险**：若 L0 只剩文件路径而没有“何时触发、不得全展开、同名词需限定”三条判断，模型虽然省了上下文，却无法正确路由，属于无效植入。
- **兼容风险**：`domain-model.md` 已被 README、架构摘要和交付引用；若拆分或改名，必须保持可读入口与相对链接有效，历史归档不追溯改写。
