<!-- butler-artifact-template: 1.0.0 artifact=tech_plan -->
# TECH_PLAN — ITER-0100

方案状态: pass

方案审查日期: 2026-07-31
方案审查方式: user-ack

## Design Decisions

**Goal**：支撑 AC1–AC8，把 R1 混装在一份文件中的“初始路由、上下文地图、术语审计、冲突证据”拆成 L0–L3，并用静态预算门和运行期扇出升级回执共同约束渐进加载；不改变 Butler 的状态、权限、命令或生命周期行为。

**Files / Modules to Change**

| 文件 / 模块 | 改动性质 | 服务 AC |
|---|---|---|
| `Coder/README.md` | 增加唯一带标记的 L0 路由块；更新入口、目录和按需读法 | AC1、AC5、AC6 |
| `Coder/domain-model.md` | 收敛为 L1 五上下文地图、四路径路由与分批升级合同 | AC2、AC4、AC5 |
| `Coder/domain-glossary.md` | 新增 L2 查询表，迁入 R1 的 20 项高风险术语 | AC3、AC5 |
| `Coder/architecture-overview.md` | 只更新 L1/L2 分工和导航，不复制地图或术语定义 | AC6 |
| `tools/context-budget/context_budget.py` | 新增标准库确定性预算检查 CLI | AC1–AC7 |
| `tools/context-budget/README.md` | 记录命令、稳定代理、退出码与非能力边界 | AC7 |
| `tools/context-budget/tests/test_context_budget.py` | 覆盖绿色基线和预算/结构负例 | AC5、AC7 |
| `scripts/verify-ci.sh` | 接入 context-budget 单元测试与项目基线检查 | AC7、AC8 |

`.ai/project/architecture.md`、`.ai/project/invariants.md` 与 `.ai/project/debt.md` 在 P4 只做只读重复审计；需要更新的当前事实由收口知识折叠统一写入，避免执行阶段绕过 knowledge-fold 边界。迭代状态、evidence、交付与归档按生命周期更新，不计入规则功能面。P2 的 Archify 临时图只作设计辅助；本轮不把特定渲染器或生成 HTML 引入运行合同。

**Layer Contract**

| 层 | 权威载体 | 触发 | 预算 / 停止 |
|---|---|---|---|
| L0 初始内核 | `Coder/README.md` 标记块 | 每次从 Coder 入口建立规则上下文 | ≤1,600 UTF-8 bytes、≤18 非空行、≤4 文档指针；普通单模块问题到此停止 |
| L1 上下文地图 | `Coder/domain-model.md` | 跨模块所有权、同名状态消歧、真源冲突或新增核心领域术语 | 全文 ≤7,000 bytes、≤70 行、≤15 文档指针；定位上下文和下一层后停止 |
| L2 术语查询 | `Coder/domain-glossary.md` | 已知待查术语或 L1 指向的相关术语 | 只读取相关行，不默认整表植入；20 项审计完整保留 |
| L3 完整审计 | ITER-0099 归档、交付、evidence 与 `.ai/project/debt.md` | 用户显式要求完整领域审查、历史追溯或冲突取证 | 分段读取；不把历史正文复制回 L0–L2 |

**Progressive Read Contract**

- 普通冷启动：L0 → 目标专项规则；不读取 L1、L2、L3。
- 单术语消歧：L0 → L2 对应行 → 首批最多 3 份直接真源；证据足够即停。
- 跨上下文设计：L0 → L1 → 必要 L2 行 → 首批最多 3 份直接真源；证据足够即停。
- 完整领域审查：L0 → L1/L2 建立索引 → 显式进入 L3；仍按主题分段，不递归追链接或整目录读取。

“3 份”是每批预算，不是总上限。进入下一批前必须产出扇出升级回执，固定包含“当前问题、已知结论、缺失证据、已读来源、下一批来源、选择理由”六项，并先压缩前批事实。短任务把回执写进用户可见的进度更新；跨会话 Butler 任务同时同步 `.ai/task-state.md`。下一批仍最多 3 份，循环到问题解决、显式升级 L3，或因外部条件不足诚实阻塞。

**Static Budget Contract**

- `context_budget.py check --project-root <root>` 只依赖 Python 标准库，成功返回 0，合同失败返回 1，输入/布局错误返回 2。
- L0 由唯一 begin/end 标记定位；检查 bytes、非空行、仓库 Markdown 指针数和三条必备路由语义。
- L1 检查全文预算、恰好五个上下文、固定上下文字段、指针数、四路径与六字段升级回执合同，并拒绝统一语言审计表、真实冲突案例正文和递归/整目录读取指令。
- L2 检查恰好 20 行、固定必填列、概念唯一、所有者为单一上下文、仓库内定义真源存在；机器只证明结构与路径，不建立 R3 才负责的术语 registry。
- 测试从仓库基线构造临时 fixture，分别制造 L0/L1 超预算、上下文缺失、术语缺失、空列、过量指针、允许递归和缺升级字段，确认 fail-closed。

**Plan Admission**

- **AC Coverage**：AC1 由 L0 标记与预算检查覆盖；AC2 由 L1 收敛和五上下文解析覆盖；AC3 由独立 L2 表和路径检查覆盖；AC4 由 L3 只读导航与历史不改断言覆盖；AC5 由四路径、分批回执和场景走读覆盖；AC6 由职责对账、允许内容与知识折叠边界覆盖；AC7 由 context-budget CLI、负向测试和 CI 接线覆盖；AC8 由完整证据链、完整 CI 和 P5 审查覆盖。
- **Assumptions**：① 当前五个上下文与 20 项术语来自已收口 ITER-0099，可作为迁移输入；② L2 默认不进冷启动读序，因此独立文档不会增加初始注入；③ bytes/行数/指针数比 tokenizer 结果更适合作为跨模型机器合同；④ 运行时读文件行为无法仅靠静态脚本完全证明，必须保留可见升级回执和 P5 场景走读。
- **Alternatives / Trade-offs**：继续把 20 项术语留在 L1 最省文件数但每次跨域定位都支付全部成本，否决；只把术语留在历史归档最省常驻维护但失去集中查询入口，否决；现在建设 JSON registry 能强制精确术语身份，但会提前进入 R3 并制造迁移/兼容成本，否决；把 3 设为总硬顶会损害复杂问题正确性，采用“每批 3 份 + 有回执续批”。
- **Failure Modes**：见下节。
- **Impact / Scope Challenge**：核心改动收敛在四份 Coder 文档、一个小型标准库工具、其测试和一行 CI 接线；不新增运行服务、模型 tokenizer、状态枚举或宿主 hook。项目知识只在既有收口折叠更新，不于 P4 建立第二维护路径。
- **Verification Blind Spots**：静态检查不能证明上下文划分永远正确、模型实际读取量或术语迁移语义完全等价；P5 必须比较迁移前后 20 项名称、人工走读四路径，并将运行时约束结论标为语义审查而非机器事实。
- **Verdict**：`pass` — AC 全覆盖，文件边界和失败路径明确，没有已知 Must Fix；用户已于 2026-07-31 ACK，允许进入 P4。

**Execution Steps**

- [ ] T1 抽取并记录 R1 的五上下文、20 项术语与当前尺寸基线，作为迁移对账输入 → AC2、AC3、AC4
- [ ] T2 收敛 README 的 L0 标记块，并将 `domain-model.md` 改为预算内 L1 地图 → AC1、AC2、AC5
- [ ] T3 新增 L2 glossary，逐项迁移 20 项术语并对账真源 → AC3、AC6
- [ ] T4 更新 architecture-overview 的薄导航，完成五份重复候选文档的职责审计 → AC4、AC6
- [ ] T5 实现 context-budget CLI 与绿色/负向 fixture 测试，接入完整 CI → AC1–AC7
- [ ] T6 运行四路径语义走读、预算合同、artifact、链接、diff、状态审计和完整 CI，捕获 evidence → AC1–AC8

## Failure Paths

- **L0 太薄只剩路径**：模型不知道何时触发 L1，也不知道禁止全展开。预算检查除尺寸外还要求“触发、普通任务停止、禁止递归/批量”三类语义。
- **L1 又长回审计报告**：术语表、冲突案例或历史说明重新混入会让成本反弹。静态检查拒绝对应结构，详细内容只留 L2/L3。
- **L2 成为第二执行真源**：glossary 只能保存白话定义、所有者、非职责和指针；枚举、字段与算法仍由原 schema/manifest/规则拥有。
- **分批预算变成调查上限**：3 份不足时若直接停止会损害正确性。合同要求六字段升级回执后继续下一批或进入 L3，不允许把预算不足写成已解决。
- **回执流于隐藏思考**：只在模型内部推理无法审计。短任务必须通过进度更新可见；跨会话任务还要同步 task-state。
- **检查器绑定中文排版过紧**：工具只钉住机器必要的标记、固定表头和预算，不对普通措辞做整段字符串比较；语义走读承担可读性判断。
- **术语迁移丢项或改义**：机器计数 20 仍可能换掉一个概念。P4 先捕获迁移前名称集合，P5 做集合对账并抽查定义/真源语义。
- **知识文件夹双写**：P4 不直接修改 `.ai/project/` 当前全貌；收口折叠根据已验证 delta 更新，fold receipt 负责漂移检查。

## Test Strategy

- **预算基线**：运行 `python3 tools/context-budget/context_budget.py check --project-root .`，输出 L0/L1 bytes、非空行、指针数、上下文数和 L2 术语数。
- **负向合同**：运行 `python3 -m unittest discover -s tools/context-budget/tests`；fixture 分别验证超预算、缺标记、缺上下文、19/21 术语、空必填列、坏真源、过量指针、允许递归和缺升级字段均返回非零。
- **迁移完整性**：在改写前提取当前 20 项概念名称；改写后与 L2 名称集合做等值比较，并抽查 `active`、`pass`、Dangerous Mode、Convergence Loop、Handoff 的限定语义和真源。
- **四路径走读**：用普通单模块、单术语、跨上下文设计、完整领域审查四个场景记录期望层级；增加“首批 3 份仍不足”场景，确认产生六字段回执后才续批。
- **重复与历史边界**：扫描 README、architecture-overview、project knowledge、debt，确认没有复制五上下文表/20 项术语表；核对 ITER-0099 归档、交付和 evidence 未被改写或删除。
- **仓库门禁**：运行 artifact contract、`python3 scripts/check-markdown-links.py --root .`、`git diff --check`、状态审计和 `bash scripts/verify-ci.sh`，由 verification-evidence 捕获 P5 证据。
- 本迭代不声明 TDD cycle，`TDD Pair Status` 写 N/A。

## References Compliance

- `.ai/references/domain-driven-design-fowler.md` 只支撑“领域地图负责边界与统一语言导航，不夺取执行真源”的战略设计原则；不复制来源大段正文，不引入 DDD 战术对象模式。
- `.ai/iterations/ITER-0099/AC_LIST.md` 是五上下文、20 项术语和冲突证据的冻结迁移来源；R2 只重组读取层级，不追溯改写该归档。
