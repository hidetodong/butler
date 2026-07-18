# Dangerous Mode Run Log

- 2026-07-18 · activation · ITER-0059 · `dangerous-ack`：用户明确要求开启危险模式并完成 MILE-0007；项目开关已置 on，北极星锁定为连续完成 R4/R5 后收口里程碑。
- 2026-07-18 · P2 · ITER-0059 · `dangerous-ack`：通过验收自审门并自主冻结 AC1–AC9。结论：每条 AC 均有明确负向/正向验证，覆盖功能、结构、事务安全与证据质量；In/Out 边界明确，split/global-install 未决风险如实暴露，无范围膨胀或不可验证项。
- 2026-07-18 · P3 · ITER-0059 · `dangerous-ack`：通过设计自审门并自主锁定中心 JSON manifest、标准库 CLI、项目内 preflight/transaction/journal 与三执行域方案。结论：AC1–AC9 均有模块和验证映射；未引入通用脚本语言或自动语义 split，影响面未越过 R4。
- 2026-07-18 · P5-review · ITER-0059 · `dangerous-ack`：首次状态 evidence 发现 1 项 Must Fix——通用 plugin cachebuster helper 改了仓内源 manifest，违反 VERSION 精确对账；已保留失败 record，恢复源版本，cachebuster 只留安装副本，待定点复查。
- 2026-07-18 · P5-review · ITER-0059 · `dangerous-ack`：完整多维审查又发现 manifest preconditions/protected path、current drift 与事务准备失败三处合同缺口；修复后最终升级专项 16/16、完整唯一入口、两组 reproduced 风险复核和状态审计通过。最终 Must Fix 0、Should Fix 0；未执行 fresh-context 独立复核且已如实披露。
- 2026-07-18 · close · ITER-0059 · `dangerous-ack`：证据整包归档、四件套/CHANGELOG 快照、MD/HTML 交付和项目知识折叠完成；R4/ITER-0059 置 closed，自治路线推进 R5。
- 2026-07-18 · route · ITER-0060 · `dangerous-ack`：按北极星自动开启 R5，锁定单一 workflow registry、窄投影生成/校验、风险门与分发三态边界。
- 2026-07-18 · P2 · ITER-0060 · `dangerous-ack`：AC1–AC8 通过自审并自主冻结；每项可由 registry fixture/投影/分发/完整矩阵验证，范围不包含业务算法或远端团队配置。
- 2026-07-18 · P3 · ITER-0060 · `dangerous-ack`：设计自审通过；JSON + 标准库、全量 plan 后原子 write、零写入 check、窄 frontmatter/YAML/docs/symlink 投影逐 AC 映射，无影响面扩张。
2026-07-18 | ITER-0060 | P5 strong review | Should Fix: hook command validation matched suffix only; tightened to exact type/command object and added regression. Final Must Fix 0 / Should Fix 0; no independent fresh-context review.
2026-07-18 | ITER-0060 | Evidence | 11 records archived; direct system-Python validator failure retained (missing PyYAML), pinned uv full matrix reproduced passed. Registry closure tests 8/8.
2026-07-18 | ITER-0060 / MILE-0007 | Close | R5 closed, project knowledge folded, milestone routes R1–R5 all closed. Dangerous remains ON; release/push not inferred.
- 2026-07-18 · route · ITER-0061 · `dangerous-ack`：用户 ACK MILE-0008 方向并确认危险模式；开启 R1，限定只做目标载体盘点、层级边界和假完成失败模型，不提前实现 Goal Contract。
- 2026-07-18 · P2 · ITER-0061 · `dangerous-ack`：AC1–AC6 通过验收自审并自主冻结；每项均有表格、严格 JSON、真源对照或完整验证动作，覆盖功能/结构/质量，Out of Scope 明确隔离 R2–R6，无不可验证项或隐藏范围扩张。
- 2026-07-18 · P3 · ITER-0061 · `dangerous-ack`：设计自审通过；采用人读基线 + 负向 JSON oracle，不新增运行 schema/脚本，不修改共同规则算法；AC1–AC6 均有落点和验证，宿主未知能力保持 unknown，未把当前会话观察误升为长期合同。
- 2026-07-18 · P5-review · ITER-0061 · `dangerous-ack`：完整强审发现 1 个 Should Fix——基线把危险模式北极星合并进普通 ITERATIONS 索引行，角色边界不够清楚；已拆为独立载体项，明确它只指导跨迭代自治、不能裁决完成。其余宿主来源等级、R1/R2 边界和 8 个负向 oracle 未发现 Must Fix。
- 2026-07-18 · P5-review · ITER-0061 · `dangerous-ack`：强审修复后合同与完整矩阵 reproduced 通过；最终 Must Fix 0、Should Fix 0。未执行 fresh-context 独立复核并已如实披露；R1 只证明问题模型，未宣称 Goal 已受新门禁保护。
- 2026-07-18 · close · ITER-0061 · `dangerous-ack`：9 个 evidence 整包归档、四件套/CHANGELOG 快照、MD/HTML 交付和 frontier 折叠完成；R1 closed，危险模式按 MILE-0008 路线推进 R2。
- 2026-07-18 · route · ITER-0062 · `dangerous-ack`：自动开启 R2；依据 R1 边界选择派生 Goal 视图，不新增 `.ai/GOAL.md` 第二台账。
- 2026-07-18 · P2 · ITER-0062 · `dangerous-ack`：AC1–AC6 自审通过并冻结；状态、真源、宿主投影和结构测试均可验证，后续路线边界明确。
- 2026-07-18 · P3 · ITER-0062 · `dangerous-ack`：设计自审通过；单一 `goal-contract.md` + 窄指针 + unittest，complete 只由收口事实派生，不提前实现 R3–R6。
- 2026-07-18 · P5-review · ITER-0062 · `dangerous-ack`：强审发现 1 个 Must Fix（新规则漏登 Coder 目录树）和 1 个 Should Fix（milestone completion-candidate 未单独消歧）；已补目录登记、里程碑候选语义与结构回归。
- 2026-07-18 · P5-review · ITER-0062 · `dangerous-ack`：修复后专项 7/7 与完整矩阵 reproduced 通过；最终 Must Fix 0、Should Fix 0，未执行 fresh-context 独立复核并如实披露。
- 2026-07-18 · close · ITER-0062 · `dangerous-ack`：8 个 evidence 归档、四件套/CHANGELOG、双格式交付完成；R2 closed，继续 R3。
- 2026-07-18 · route · ITER-0063 · `dangerous-ack`：自动开启 R3；选择 TECH_PLAN frontmatter 为 verdict 单一真源，共享 phase gate 机械拒绝显式非 pass，同时保留旧版无字段兼容。
- 2026-07-18 · P2 · ITER-0063 · `dangerous-ack`：AC1–AC7 通过自审并自主冻结；状态机、反证维度、标准/危险 ACK、hook 正负态、Goal 映射、接线与机器证据均可验证，R4–R6 边界明确。
- 2026-07-18 · P3 · ITER-0063 · `dangerous-ack`：结构化 Plan Admission verdict=`pass`；AC 全覆盖，替代方案、失败模式、影响面与验证盲区已挑战，未发现 Must Fix，准许进入 P4。
- 2026-07-18 · P5-review · ITER-0063 · `dangerous-ack`：首轮强审发现 1 个 Must Fix——单元测试覆盖状态门，但 Codex wrapper 真链路仍只走 legacy 无字段 allow，无法证明新 P3 门在真实适配器生效；已改为先以 draft 断言 deny、再置 pass 断言 allow，并补 subprocess integration 与 smoke 新合同 fixture。
- 2026-07-18 · P5-review · ITER-0063 · `dangerous-ack`：修复后结构合同 7/7、共享 hooks 135 项与完整固定矩阵 reproduced 通过；最终 Must Fix 0、Should Fix 0。未执行 fresh-context 独立复核并如实披露。
- 2026-07-18 · close · ITER-0063 · `dangerous-ack`：7 个 evidence 整包归档、四件套/CHANGELOG、双格式交付和项目知识折叠完成；R3 closed，继续 R4。
- 2026-07-18 · route · ITER-0064 · `dangerous-ack`：自动开启 R4；选择 task-state 活跃校准投影 + 既有阶段真源回写，不新增问题台账。
- 2026-07-18 · P2 · ITER-0064 · `dangerous-ack`：AC1–AC7 自审通过并冻结；六类信号、投影、P1–P5 路由、Goal 影响、重审纪律与证据均可验证，R5–R6 边界明确。
- 2026-07-18 · P3 · ITER-0064 · `dangerous-ack`：Plan Admission verdict=`pass`；否决独立 issue ledger 和“一律回 P4”，按事实性质路由，未发现 Must Fix。
- 2026-07-18 · P5-review · ITER-0064 · `dangerous-ack`：首轮强审发现 1 Must Fix——task-state 用自然语言占位行冒充封闭 Signal/Status 数据；另有 1 Should Fix——VERIFY 的 review 引用误写不存在的 §71。已改为空表 + 表外 N/A、增加 dogfood 断言，并把引用修正到 §4。
- 2026-07-18 · P5-review · ITER-0064 · `dangerous-ack`：修复后结构合同 8/8、完整固定矩阵 reproduced 通过；最终 Must Fix 0、Should Fix 0。未执行 fresh-context 独立复核并如实披露。
- 2026-07-18 · close · ITER-0064 · `dangerous-ack`：6 个 evidence 整包归档、四件套/CHANGELOG、双格式交付与知识折叠完成；R4 closed，继续 R5。
- 2026-07-18 · route · ITER-0065 · `dangerous-ack`：自动开启 R5；选择只读标准库 CLI 聚合完成资格，不自动 close。
- 2026-07-18 · P2 · ITER-0065 · `dangerous-ack`：AC1–AC7 自审通过并冻结；覆盖 AC/plan/calibration/evidence/review/blocker/ledger 与八类负向 oracle。
- 2026-07-18 · P3 · ITER-0065 · `dangerous-ack`：Plan Admission pass；稳定 JSON + 0/1/2 退出码，全量 checks 汇总，不信 host/tasks，不抢跑 R6。
- 2026-07-18 · P5-review · ITER-0065 · `dangerous-ack`：首轮强审发现 1 Must Fix——测试 fixture 自造 `streams` 包装层，与真实 evidence v1 顶层 stdout/stderr 漂移，导致工具会误拒真实 record；已对齐真实 schema 并增加 shape/schema/id 回归。
- 2026-07-18 · P5-review · ITER-0065 · `dangerous-ack`：修复后 13/13 adjudicator tests 与完整矩阵 reproduced 通过；最终 Must Fix 0、Should Fix 0，未执行 fresh-context 独立复核。
- 2026-07-18 · close · ITER-0065 · `dangerous-ack`：completion adjudicator 对本仓 active 状态十项 checks 全绿、verdict=eligible；6 evidence 归档、双格式交付和知识折叠完成，R5 closed，继续 R6。
- 2026-07-18 · route · ITER-0066 · `dangerous-ack`：自动开启 R6；共同 rule-card + 驻留 CLI 薄接线，host 只投影，缺能力 `.ai/` 降级。
- 2026-07-18 · P2/P3 · ITER-0066 · `dangerous-ack`：AC1–AC7 冻结、Plan Admission pass；不新增 workflow/daemon，不切版，不假报外部旧项目已升级。
- 2026-07-18 · P5-review · ITER-0066 · `dangerous-ack`：首轮强审发现 1 Must Fix——渲染进目标项目的规则卡使用相对 `tools/goal-assurance`，外部项目实际不可达；已改为 `$BUTLER_PATH` 驻留路径，并升级双入口端到端断言。
- 2026-07-18 · P5-review · ITER-0066 · `dangerous-ack`：修复后 host wiring 7/7 与完整矩阵 reproduced 通过；最终 Must Fix 0、Should Fix 0，未执行 fresh-context 独立复核。
- 2026-07-18 · close · ITER-0066 / MILE-0008 · `dangerous-ack`：adjudicator 十项 checks 全绿、6 evidence 归档、双格式迭代/里程碑交付与知识折叠完成；R1–R6 全 closed，危险模式自治正常终止。
