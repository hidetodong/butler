# Dangerous Mode Run Log

- 2026-07-29 | close | ITER-0096 | dangerous-ack | Goal 十一项检查全绿；12 份 evidence、五件套/CHANGELOG、双格式交付完成归档，旁路回执规则/模板/入口/CI 闭环。危险模式与 Loop 的存量规则耦合保持明示，未扩张进本迭代。
- 2026-07-29 | P5-review | ITER-0096 | dangerous-ack | 安全修订后专项 9/9、Markdown links、diff check 与宿主环境完整 CI reproduced 通过；最终 Must Fix=0、Should Fix=0。项目 `independent_review=false`，且本轮未获委派授权，未执行 fresh-context 独立复核并如实披露。
- 2026-07-29 | P5-review | ITER-0096 | dangerous-ack | 完整安全审查发现 1 个 Must Fix：回执协议若不明确“非代码写入授权”，可能让旁路 Agent 借当前迭代四件套包装范围外源码改动；另发现并发同名需 create-only 兜底。已补禁止绕过、隔离路径和竞争重试规则并加结构回归，范围仍为原 AC4。
- 2026-07-29 | P3-reentry | ITER-0096 | user-corrected | 用户明确危险模式与 Loop 不绑定；撤销 P4 自动 Loop 假设，TECH_PLAN 改回常驻纠错收口契约并重审保持 pass。先前 `[Loop #1]` 仅为对话误标，不作为运行状态；规则真源中的存量耦合另行处理，不扩张本迭代。
- 2026-07-29 | P3 | ITER-0096 | dangerous-ack | Plan Admission=pass；采用独立 `.ai/sidework/` 的一任务一回执、规则真源 + 可复制模板、用户显式路径回钩和标准库结构检查，否决 handoff/references 混用、状态机、索引、自动扫描及新命令。AC 全覆盖、Must Fix=0，自主进入 P4。
- 2026-07-29 | P2 | ITER-0096 | dangerous-ack | AC1–AC6 覆盖协议定位、混合成果模板、生产/消费边界、命名与共享工作区可信度、入口接线和完整验证；每项均可机械或证据验证，无模型审批权、自动扫描或隐藏范围扩张，自主冻结。
- 2026-07-29 | route | ITER-0096 | dangerous-ack | 用户把已收敛构思提升为独立迭代；授权上限冻结为 `/Users/cyborgno2/Documents/WorkCode.nosync/butler`。范围锁定为旁路工作短回执的协议真源、模板、入口与验证，不建设审批状态、索引、自动扫描、命令/skill 或调度器。
- 2026-07-28 | route | ITER-0095 | dangerous-ack | 自动开启 MILE-0013 R3；范围锁定为统一 `resolve/set` 消费语义、当前仓 dogfood 迁移、双宿主文档接线与 3.3.0 迁移/发布验证，不推断 commit、tag 或 push 授权。
- 2026-07-28 | P2 | ITER-0095 | dangerous-ack | AC1–AC8 覆盖统一读写、source/冲突可见性、本仓保值迁移、活文档清零、真实升级链、版本一致性和完整关闭态验证；自审无不可验证项后自主冻结。
- 2026-07-28 | P3 | ITER-0095 | dangerous-ack | Plan Admission=pass；采用 `resolve` 唯一读、`set` JSON-only 写、consumer matrix 结构测试、保值 dogfood 和先迁移链后关闭/切版本的顺序，Must Fix=0，自主进入 P4。
- 2026-07-28 | P2-reentry | ITER-0095 | dangerous-ack | P5 收口顺序审查发现 AC7 不能把“Goal eligible 后才允许生成”的 delivery 实体反向设为完成资格前置；保持原发布范围，只把验收点收窄为 UNRELEASED 元数据与既定路径对齐，实体由关闭态审计核对。
- 2026-07-28 | P5-review | ITER-0095 | dangerous-ack | 完整强审发现 1 个 Must Fix：直接修改 preference command frontmatter 绕过 workflow registry 投影真源；已改为更新 registry 并重生成。复跑配置专项 32/32、upgrader 19/19、完整 CI exit 0，最终 Must Fix 0、Should Fix 0；独立复核关闭。
- 2026-07-28 | close | ITER-0095 / MILE-0013 | dangerous-ack | Goal 十一项检查全绿，证据与五件套归档、迭代/里程碑双格式交付生成，R1–R3 全部 closed；v3.3.0 仅为 UNRELEASED 候选，未提交、未打 tag、未推送。

- 2026-07-22 · activation · MILE-0009 · `dangerous-ack`：用户明确要求开启危险模式并开始当前里程碑；确认 MILE-0009 已 active、尚无承接迭代。本次写入上限冻结为 `/Users/cyborgno2/Documents/WorkCode.nosync/butler`，北极星锁定为连续完成 R1–R8 后收口里程碑。
- 2026-07-22 · route · ITER-0075 · `dangerous-ack`：领取 MILE-0009 R1；限定为需求集合、日期化稳定身份、单需求目录和新需求/新版身份判定契约，不提前实现 monorepo 范围、inbox、多 PRD AC 钉版、命令、迁移或门禁。
- 2026-07-22 · P2 · ITER-0075 · `dangerous-ack`：AC1–AC7 通过验收自审并自主冻结；项目级索引、`prd_id` 语法与稳定性、单需求目录、身份判定、歧义停机、旧结构兼容边界和文档/测试均有可验证判据，范围未越过 R1。
- 2026-07-22 · P3 · ITER-0075 · `dangerous-ack`：Plan Admission verdict=`pass`；选择在 `references-schema.md` 原位升级声明式契约并用标准库结构测试守字段，否决新增第二份 schema 与提前改动作层。AC 全覆盖，无已知 Must Fix。
- 2026-07-22 · P4-correction · ITER-0075 · `dangerous-ack`：完整 CI 首轮暴露根 `README.md` 缺 `docs/workflows.md` 路由，导致 workflow registry 8 项中 6 项连锁失败；该缺口不在 R1 初始 diff，但阻断 AC7。按最小根因修复补回单一人读入口，保留首轮失败结论后重跑。
- 2026-07-22 · P4-correction · ITER-0075 · `dangerous-ack`：完整 CI 第二轮通过 153 项 hooks 后在 Goal Calibration dogfood 发现 1 个失败：task-state 用自然语言描述“无信号”却漏掉机器契约要求的精确空态行。已恢复 `当前无未闭合运行时信号（N/A）`，不伪造信号表行，待专项与完整矩阵复核。
- 2026-07-22 · P5-review · ITER-0075 · `dangerous-ack`：完整强审发现 1 个 Must Fix——重排后的 references §4/§6 仍能被旧动作层链接命中，但已分别从“模块 slug 身份 / 无损红线”漂成“仅 prd_id / 读纪律”，形成静默错指。已将 §4 收敛为两层稳定身份、§6 恢复无损真源并保留新集合读序；不修改 legacy 动作算法。
- 2026-07-22 · P5-review · ITER-0075 · `dangerous-ack`：修复后专项 6/6、完整 CI reproduced exit 0、diff check 与 5 份 evidence integrity 通过；最终 Must Fix 0、Should Fix 0。两份沙箱环境失败 record 保留，绿色 AC 由后续 `reproduced-full-ci` 覆盖；未执行 fresh-context 独立复核并如实披露。
- 2026-07-22 · close · ITER-0075 · `dangerous-ack`：Goal adjudicator 十项全绿、证据整包归档、四件套/CHANGELOG 快照、MD/HTML 交付与 invariants/frontier 折叠完成；R1 closed，继续 R2。
- 2026-07-22 · route · ITER-0076 · `dangerous-ack`：自动开启 R2；选择项目知识层稳定 workspace map + 单需求四类范围，不按包复制 PRD、不提前实现 R8 门禁。
- 2026-07-22 · P2 · ITER-0076 · `dangerous-ack`：AC1–AC7 自审通过并冻结；地图字段、稳定键、四类集合、默认拒绝、模块子集、扩张审查和单包退化均可验证，范围未越过 R2。
- 2026-07-22 · P3 · ITER-0076 · `dangerous-ack`：Plan Admission=pass；采用独立 workspace-scope schema，references 只接指针，否决路径直写每份 PRD与提前接 hook。无已知 Must Fix。
- 2026-07-22 · P5-review · ITER-0076 · `dangerous-ack`：完整强审发现 1 个 Must Fix——地图 status 曾含 `moved`，却又规定目录移动只改 path，导致同一稳定键移动后会被“只允许 active 引用”拒绝；另补模块四类互斥与完整声明，封住省略字段默认放行。现已明确移动后保持 active、只更新 path/evidence，并加回归断言。
- 2026-07-22 · P5-review · ITER-0076 · `dangerous-ack`：修复后专项 7/7、完整 CI reproduced exit 0、160 hooks 与 diff check 通过；最终 Must Fix 0、Should Fix 0，未执行 fresh-context 独立复核。
- 2026-07-22 · close · ITER-0076 · `dangerous-ack`：Goal adjudicator 十项全绿、证据与四件套归档、双格式交付、知识折叠完成；R2 closed，继续 R3。
- 2026-07-22 · route · ITER-0077 · `dangerous-ack`：自动开启 R3；选择稳定 source_id + observed/processed 双指纹 + 独立派生关系表，origin 保持用户自管零写入，不提前实现 R4 命令。
- 2026-07-22 · P2 · ITER-0077 · `dangerous-ack`：AC1–AC7 自审通过并冻结；来源、指纹、封闭状态、幂等、变化、重复候选、多对多和隐私边界均可验证。
- 2026-07-22 · P3 · ITER-0077 · `dangerous-ack`：Plan Admission=pass；否决 hash 主键和原文复制，采用 inbox schema 单一真源 + 三处薄接线。无已知 Must Fix。
- 2026-07-22 · P5-review · ITER-0077 · `dangerous-ack`：完整强审发现 1 个 Must Fix——外部文档 revision 曾被建议写入 locator/evidence，会让每次改版改变稳定 locator，破坏同源变化检测。已新增独立可变 `source_revision` 字段，稳定文档 ID/URL 留 locator，hash 继续裁决内容，并补回归断言。
- 2026-07-22 · P5-review · ITER-0077 · `dangerous-ack`：修复后专项 7/7、完整 CI reproduced exit 0、167 hooks 与 diff check 通过；最终 Must Fix 0、Should Fix 0，未执行 fresh-context 独立复核。
- 2026-07-22 · close · ITER-0077 · `dangerous-ack`：Goal adjudicator 十项全绿、证据/四件套归档、双格式交付和知识折叠完成；R3 closed，继续 R4。
- 2026-07-22 · route · ITER-0078 · `dangerous-ack`：自动开启 R4；选择标准库 scanner 管机械事实、双宿主薄入口管语义分类/确认/委托路由，registry 扩为 11，不在 CLI 内复制 PRD 算法。
- 2026-07-22 · P2 · ITER-0078 · `dangerous-ack`：AC1–AC9 自审通过并冻结；plan/apply、幂等/变化/symlink、路由确认、活工作区保护、双宿主注册和 fixture 均可验证。
- 2026-07-22 · P3 · ITER-0078 · `dangerous-ack`：Plan Admission=pass；采用 Markdown managed block 单一真源与原子替换，否决纯模型写 ledger 和 JSON sidecar。无已知 Must Fix。
- 2026-07-22 · P5-review · ITER-0078 · `dangerous-ack`：完整强审先后修复 3 个 Must Fix——表格 parser 空行假设、首次接管时块外尾随内容损失/断链 origin symlink 漏拒绝、registry 重复 ID fixture 依赖旧顺序；均补负向回归。
- 2026-07-22 · P5-review · ITER-0078 · `dangerous-ack`：scanner 11/11、registry 8/8、协议结构 5/5、完整 CI reproduced exit 0、170 hooks 与 diff check 通过；最终 Must Fix 0、Should Fix 0，未执行 fresh-context 独立复核。
- 2026-07-22 · close · ITER-0078 · `dangerous-ack`：Goal adjudicator 十项全绿、5 个 evidence（含 1 条已复现纠正的失败诊断）归档、四件套/CHANGELOG、双格式交付与知识折叠完成；R4 closed，继续 R5。
- 2026-07-22 · route · ITER-0079 · `dangerous-ack`：自动开启 R5；选择 `prd_refs` 多值钉版 + 标准库 resolver/事务迁移 + receipt/backup，不回写 frozen/closed 历史，不提前实现 R6/R7。
- 2026-07-22 · P2 · ITER-0079 · `dangerous-ack`：AC1–AC9 自审通过并冻结；多引用、legacy 解析、plan/apply/verify/rollback、影响面、指南与负向 fixture 均可验证。
- 2026-07-22 · P3 · ITER-0079 · `dangerous-ack`：Plan Admission=pass；采用窄 YAML 列表、同父目录事务切换和机器 receipt，否决猜日期/原地 move/回写 closed AC。真实 apps dogfood留 R8。
- 2026-07-22 · P5-review · ITER-0079 · `dangerous-ack`：完整强审发现 3 个 Must Fix——receipt/backup/mapping 路径可被篡改诱导越界、切换后 verify 失败未自动恢复、影响面漏扫 MILESTONE 的 `→ prd: slug` 指针；已加根约束/ID 校验、失败反切换和路线 slug 扫描及回归。
- 2026-07-22 · P5-review · ITER-0079 · `dangerous-ack`：另发现完整 CI 未直接执行 scanner/migration 行为测试；已把两组标准库 unittest 纳入 `verify-ci.sh`。最终 targeted 11+11、完整 CI 175 hooks + 两组行为测试均通过；继续采集证据。
- 2026-07-22 · close · ITER-0079 · `dangerous-ack`：Goal adjudicator 十项全绿、4 个 evidence 与四件套/CHANGELOG 归档、双格式交付和知识折叠完成；R5 closed，继续 R6。

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
- 2026-07-18 · route · ITER-0067 · `dangerous-ack`：用户确认项目外授权交宿主；本次危险任务授权上限冻结为 `/Users/cyborgno2/Documents/WorkCode.nosync/butler`，范围内动态施工；开启独立完整迭代，不切版。
- 2026-07-18 · P2 · ITER-0067 · `dangerous-ack`：AC1–AC7 自审通过并冻结；外部目标退出判定、坏输入 fail-closed、多项目逐根门禁和危险模式授权上限均可机器验证。
- 2026-07-18 · P3 · ITER-0067 · `dangerous-ack`：Plan Admission=`pass`；否决 AI 自签授权文件与正常路径 bypass，采用 Butler 流程门禁和宿主文件权限分层。
- 2026-07-18 · P5-review · ITER-0067 · `dangerous-ack`：完整强审发现 2 个 Must Fix——项目子目录写兄弟目录会被误判项目外、无 Git 的既有 Butler 项目会失去阶段门/advisor；已统一目标项目根并增加仅 `.ai/` 项目的有界 cwd fallback。
- 2026-07-18 · P5-review · ITER-0067 · `dangerous-ack`：修复后最终 hook 147 项、Codex wrapper 与完整 CI captured 通过；最终 Must Fix 0、Should Fix 0，未触发 opt-in 独立复核。
- 2026-07-18 · close · ITER-0067 · `dangerous-ack`：Goal adjudicator 十项全绿、6 evidence 整包归档、四件套/CHANGELOG 快照与双格式交付完成；项目知识折叠后关闭迭代，危险模式保持 ON。
- 2026-07-19 · route · ITER-0068 · `dangerous-ack`：用户要求讨论后暂缓的里程碑不占正式号；开启独立完整迭代，将候办草稿与正式里程碑拆层。
- 2026-07-19 · P2 · ITER-0068 · `dangerous-ack`：AC1–AC8 自审通过并冻结；候办落盘、提升领号、安全退回、历史不回收和状态审计均有可验证判据。
- 2026-07-19 · P3 · ITER-0068 · `dangerous-ack`：Plan Admission=`pass`；采用台账候办索引 + 独立草稿，否决 `paused` 占号与台账内堆详情，退回条件限定为最新号且零历史引用。
- 2026-07-19 · P5-review · ITER-0068 · `dangerous-ack`：完整强审发现 2 个 Must Fix——brief 章节仍把 `.ai/MILESTONE.md` 写成候办期真源，以及审计器遇畸形正式号可能抛异常；已切换为随阶段唯一真源，并增加稳定 ID 漂移报告与回归。
- 2026-07-19 · P5-review · ITER-0068 · `dangerous-ack`：修复后状态审计 18/18、workflow registry、Markdown 链接、147 hooks 与完整 CI 均通过；最终 Must Fix 0、Should Fix 0，未触发 opt-in 独立复核。
- 2026-07-19 · P3-reentry · ITER-0068 · `dangerous-ack`：Goal adjudicator 暴露与 verify-schema 的存量契约冲突，错把已被后续通过证据覆盖的失败诊断当成当前失败；方案退回并重审为“全记录校验完整性，只 passed 记录覆盖 AC”，Plan Admission 再次 pass。
# ITER-0069

- 2026-07-19：用户补充多个候办方向必须拆块并分文件；按已关闭需求扩张规则开启独立 ITER-0069。
- 2026-07-19：危险模式自审 P2/P3，冻结 AC1–AC5，方案 verdict=pass。
- 2026-07-19：同上下文强审完成，Must Fix 0、Should Fix 0；20 项状态审计与完整 CI 通过。
- 2026-07-22 · route · ITER-0080 · `dangerous-ack`：自动开启 MILE-0009 R6；身份四态先于写盘，采用独立标准库只读 status、`prd_id#module_slug` 指针和双宿主薄路由，不提前实现 R7/R8。
- 2026-07-22 · P2 · ITER-0080 · `dangerous-ack`：AC1–AC9 自审通过并冻结；日期证据、双层索引、workspace soft 对齐、零写 status、legacy/坏输入和 host 投影均可验证。
- 2026-07-22 · P3 · ITER-0080 · `dangerous-ack`：Plan Admission=pass；采用 project index 发现真源 + 目录交叉核验 + 窄 Markdown parser，否决散文看板、迁移工具耦合与 R7 写动作。无已知 Must Fix。
- 2026-07-22 · P5-review · ITER-0080 · `dangerous-ack`：完整强审修复 3 个 Must Fix——workspace key 未与 active 地图对账、祖先 symlink 可越出项目根、argparse 坏参数未保持 JSON；均补负向回归。
- 2026-07-22 · P5-review · ITER-0080 · `dangerous-ack`：首次完整 CI 暴露新迭代 task-state 仍残留 R5 resolved 投影；已整体覆写为当前 N/A，第二次完整 CI 通过。
- 2026-07-22 · close · ITER-0080 · `dangerous-ack`：Goal adjudicator 十项全绿、6 个 evidence（含 1 条已纠正 launch error）与四件套/CHANGELOG 归档、双格式交付和知识折叠完成；R6 closed，继续 R7。
- 2026-07-22 · route · ITER-0081 · `dangerous-ack`：自动开启 MILE-0009 R7；语义确认产 JSON spec，机械层用整 PRD root staging/backup/rename、持久 receipt 与 hash-gated rollback，不提前实现 R8。
- 2026-07-22 · P2 · ITER-0081 · `dangerous-ack`：AC1–AC9 自审通过并冻结；spec、零写 plan、先冻后更、影响处置、幂等/恢复/篡改和 status 接线均可验证。
- 2026-07-22 · P3 · ITER-0081 · `dangerous-ack`：Plan Admission=pass；采用已确认 spec + 共享 status parser + 整 collection 事务交换，否决模型启发式 CLI、逐文件半事务和自动改工作产物。无已知 Must Fix。
- 2026-07-22 · P5-review · ITER-0081 · `dangerous-ack`：两轮强审修复逐路线影响误分类、receipt 自身篡改缺口与共享 status 缺失 hash 依赖；补混合路线、payload 篡改、非法时间和 rollback 中途故障回归，最终 Must Fix 0、Should Fix 0。
- 2026-07-22 · P5-verify · ITER-0081 · `dangerous-ack`：事务行为 12/12、结构合同 7/7、完整 CI 189 hooks + 行为组、diff check 与 Goal adjudicator 十项全绿；4 个 evidence 完整归档。
- 2026-07-22 · close · ITER-0081 · `dangerous-ack`：四件套/CHANGELOG 快照、双格式交付和项目知识折叠完成；R7 closed。按用户要求停在 `current: none` 的 compact 边界，不自动开启 R8。
- 2026-07-22 · close-audit · ITER-0081 · `dangerous-ack`：收口态完整 CI 首轮发现无 active 时 task-state 不应保留 resolved 信号行；历史留 VERIFY/RUN_LOG、活投影恢复 N/A 后，完整 CI 189 hooks + 全行为组、state audit 与 diff check 最终通过。
- 2026-07-22 · route · ITER-0082 · `dangerous-ack`：compact 后自动开启 MILE-0009 R8；施工授权上限仍为 Butler 仓，真实 apps 只读取证并在临时副本 dogfood，不提前把仓外可读等同可写。
- 2026-07-22 · P2 · ITER-0082 · `dangerous-ack`：AC1–AC10 自审通过并冻结；覆盖发现/地图/钉版范围/计划/diff/hook/扩张纪律、版本级 e2e、apps 零写 dogfood 与完整收口，明确 shell 与旧 queued 状态边界。
- 2026-07-22 · P3 · ITER-0082 · `dangerous-ack`：Plan Admission=pass；采用 hook 自包含共享内核 + 驻留 CLI + 写计划三重交集 + P5 diff，apps 走真实只读源和临时副本。无已知 Must Fix。
- 2026-07-22 · P4-calibration · ITER-0082 · `dangerous-ack`：共享内核/CLI 与 10 项专项通过；新 hook 首次自举因 `_root` 未把 `ctx.cwd: str` 转成 Path 而 fail-closed。危险模式禁止模型自行 bypass，登记 CAL-001 并请求一次受控 gate-repair 授权。
- 2026-07-22 · P4-dogfood · ITER-0082 · `dangerous-ack`：无写读取 apps：legacy inspect 成功识别 12 live 模块 + v20 archive，Git status hash 前后均为 `71c52a…b75`；真实 npm glob 暴露无 manifest 目录应跳过的 CAL-002。源码门禁仍等待用户显式授权一次受控修复。
- 2026-07-22 · P4-bypass · ITER-0082 · `user-authorized`：用户明确允许一次受控 bypass；先落非空审计理由，仅修 `_root` 的 str→Path 归一化与 npm glob 跳过无 manifest 普通目录，随即删除理由。后续普通源码 patch 成功，门禁恢复；CAL-001/CAL-002 resolved。
- 2026-07-22 · P4-e2e · ITER-0082 · `dangerous-ack`：单一临时工程贯通 inbox 幂等、legacy migration/resolver、update receipt、两 PRD 同名模块、多版本钉住与跨包 scope；真实 apps 临时副本进一步发现 `v28` doc-revision 与产品版 `V1.1.0` 并存，补“源”行 doc version 优先和无点 `vN` 兼容后，plan/apply/verify/resolve/rollback 全绿。
- 2026-07-22 · P4-dogfood · ITER-0082 · `dangerous-ack`：apps 原仓 Git status hash 前后同为 `fb7c0b…97a`；临时副本 rollback 后 legacy PRD 树 hash 恢复 `sha256:91cc34…05fb4`。真实仓未写入，非标准 queued 里程碑未被静默规范化。
- 2026-07-22 · P5-verify · ITER-0082 · `dangerous-ack`：首轮完整 CI 的实现/宿主/hook 195 项均通过，唯一失败为 task-state 仍投影已 resolved CAL 行；按 Goal Calibration 活投影合同清空为 N/A，保留历史于本日志，待重跑。
- 2026-07-22 · P5-review · ITER-0082 · `dangerous-ack`：同上下文完整强审发现 glob symlink 与精确 workspace 无 manifest 两个边界缺口；修复并加负向回归后最终 Must Fix 0、Should Fix 0。环境规则禁止委派，未执行 fresh-context 独立复核并如实披露。
- 2026-07-22 · P5-verify · ITER-0082 · `dangerous-ack`：六份 evidence 校验归档；workspace 10/10、hook/合同 13/13、组合 e2e、真实 apps dogfood、完整 CI 与 diff check 通过，Goal adjudicator 十项全绿、verdict=eligible。
- 2026-07-22 · close · ITER-0082 / MILE-0009 · `dangerous-ack`：R8 置 closed，迭代/里程碑四件套与双格式交付完成，项目知识折叠；MILE-0009 八条路线全部 closed。未提交、未切版、未推送，等待 closed 状态审计后 compact。
- 2026-07-22 · close-audit · ITER-0082 / MILE-0009 · `dangerous-ack`：evidence 重新归档后 closed 状态审计 exit 0，ITER/MILE 台账、路线、交付、归档、evidence 与 fold receipt 全部一致，仅保留 `UNRELEASED` 亮牌；收口态完整 CI 与 diff check 再次通过。当前无 active，进入 compact 边界。
- 2026-07-22 · release · MILE-0009 · `user-requested`：按 MAJOR 级别切版 v3.0.0，聚合 ITER-0075–ITER-0082；迭代内容与发布元数据保持独立提交，升级配方登记 global-install、sync-hooks、restamp，旧 PRD 内容继续要求显式迁移。
- 2026-07-22 · route · ITER-0083 / MILE-0010 · `dangerous-ack`：用户明确启动长期规模治理；独立落盘五件套固定化候办后，把 handoff 高频痛点前移为 R1。确认 handoff 是工具生成的派生视图，先落权威状态、再生成/签指纹，陈旧内容不得被冷启动当真。
- 2026-07-22 · P2/P3 · ITER-0083 · `dangerous-ack`：冻结 AC1–AC9；方案采用标准库派生工具 + sidecar receipt + 写后 advisory + 冷启动 check/sync，不依赖 stop hook，不声称恢复未落盘聊天。Plan Admission=pass。
- 2026-07-22 · P5-review · ITER-0083 · `dangerous-ack`：完整审查发现成对写缺失败回滚、current 未核前缀/active 两个 Must Fix；回 P4 增加事务恢复与故障注入/坏状态回归，最终专项 6/6、hook 197 项、审计 21 项与完整 CI 通过。
- 2026-07-22 · close · ITER-0083 · `dangerous-ack`：可信 handoff 的五组 evidence、四件套/CHANGELOG、双格式交付和知识折叠完成；R1 closed。未实际使用 bypass。
- 2026-07-22 · route · ITER-0084 · `dangerous-ack`：R2–R4 因共享同一状态迁移边界合并收官；冻结至少四位身份、有界双台账、机器索引、幂等迁移与万级验证，外部项目无具体根授权故保持 N/A。
- 2026-07-22 · P5-review · ITER-0084 · `dangerous-ack`：万行 fixture、当前仓迁移和首次审计/CI 暴露 cold backlog 误读、fold receipt 缺失/locale 污染、task-state 固定句缺失；失败证据保留，逐项修复后 Goal 十项全绿。
- 2026-07-22 · close · ITER-0084 / MILE-0010 · `dangerous-ack`：84 条迭代拆成 20 热 + 64 冷，state index/check 通过；两个迭代与里程碑归档、双格式交付、fold receipt 完成。用户授权 bypass 但本里程碑未使用；明确不切板、不 tag、不推送。
- 2026-07-23 · correction · ITER-0085 · `user-triggered`：用户指出单个 `ITERATIONS.cold.md` 不是分片。确认 MILE-0010 已归档不可重开/回挂，开启独立纠偏迭代；旧交付保留事实，新迭代补固定区间多分片与定向读取 proof。
- 2026-07-23 · release · MILE-0010 / MILE-0011 · `user-requested`：按 MINOR 级别切版 v3.1.0，聚合 ITER-0083–ITER-0089；发布可信 handoff、固定区间状态分片和确定性五件套产物链，升级配方登记 global-install、sync-hooks、regen-entrypoints、restamp，既有项目的数据迁移保持显式执行。
- 2026-07-23 · route · ITER-0090 · `dangerous-ack`：用户提出把 setup 做进命令；开启独立迭代，采用 `/butler:setup` / `$butler-setup` 薄入口 + `scripts/setup.sh` 机械单一真源，不混入项目 init/upgrade。
- 2026-07-23 · P5-verify · ITER-0090 · `dangerous-ack`：setup 双宿主/临时 HOME 矩阵、skill/plugin validator、registry 9 项、200 hooks 与完整 CI captured 通过；Goal 十项全绿、verdict=eligible。
- 2026-07-23 · close · ITER-0090 · `dangerous-ack`：两份 evidence、五件套/CHANGELOG、双格式交付与项目知识折叠完成；未提交、未切版、未推送。
- 2026-07-25 · route · ITER-0091 / MILE-0012 · `dangerous-ack`：用户明确开启危险模式并启动 MILE-0012；授权上限冻结为 Butler 仓，P4 代码回滚锚点为 `1aa6533c86ac448d80e4a0330148f5f3a953ea2e`，既有脏点仅含里程碑规划/状态产物。R1 采用现有 evidence v1 + 稳定 ID 配对，不建设 sidecar、baseline、adapter 或第二台账。
- 2026-07-25 · P2 · ITER-0091 · `dangerous-ack`：AC1–AC7 经反证、自洽性、可验证性审查后冻结；明确无声明零行为，声明后缺边、outcome、顺序、argv/cwd/AC 漂移均 fail-closed，生命周期完成门留给 R2。
- 2026-07-25 · P3 · ITER-0091 · `dangerous-ack`：Plan Admission=pass；在 `evidence.py` 增加只读 `check-tdd`，TECH_PLAN 用版本化 marker + 固定表声明 cycle，配对 ID 由名称派生。无已知 Must Fix，进入 P4。
- 2026-07-25 · P5-review · ITER-0091 · `dangerous-ack`：完整强审先后修复 marker 未限定 Test Strategy、超长 cycle 生成非法 evidence ID、正文引用 marker 误触发、缺边时诊断不完整四项；最终 Must Fix 0、Should Fix 0。未执行 fresh-context 独立复核并如实披露。
- 2026-07-25 · P5-verify · ITER-0091 · `dangerous-ack`：专项 21/21；首次完整 CI 因沙箱拒绝用户级 uv cache 失败并保留 record，宿主授权后同命令 reproduced exit 0，200 hooks 与全部行为组通过；Goal Calibration 无开放信号。
- 2026-07-25 · close · ITER-0091 · `dangerous-ack`：Goal adjudicator 十项全绿；三份 evidence、五件套/CHANGELOG、双格式交付和项目知识折叠完成，R1 closed。未提交、未切版、未推送；继续 R2。

- 2026-07-26 | 路线图变更 | ITER-0092 | dangerous-ack | 自审结论：MILE-0012 R2 范围已在里程碑中明确且无外部阻塞；自决摘要：绑定 ITER-0092 并开启 P1。
- 2026-07-26 | P2 | ITER-0092 | dangerous-ack | 自审结论：AC1–AC7 均可机械验证，功能/结构/质量与关闭态兼容覆盖完整，无隐藏未决项；自决摘要：自主冻结 AC 并进入 P3。
- 2026-07-26 | P3 | ITER-0092 | dangerous-ack | 自审结论：Plan Admission=pass；AC 全覆盖，无新契约/模块扩张，跨根寻址、stdout JSON 和关闭态失败路径已明确，Must Fix=0；自决摘要：复用 evidence CLI 单一算法并进入 P4。
- 2026-07-26 | P5-review | ITER-0092 | dangerous-ack | 自审结论：逻辑健壮性/可读性/性能/安全与 AC1–AC7 断言核对通过，Must Fix=0、Should Fix=0；独立复核未启用（项目开关 off，本任务也未获子 agent 委派授权）；自决摘要：允许进入 Goal 完成资格裁决。
- 2026-07-28 | route | ITER-0093 | dangerous-ack | 授权上限冻结为 `/Users/cyborgno2/Documents/WorkCode.nosync/butler`；MILE-0013 R1 绑定 ITER-0093，先建立扁平 JSON 配置合同与统一读写内核，不提前切换消费端。
- 2026-07-28 | P2 | ITER-0093 | dangerous-ack | 自审结论：AC1–AC7 覆盖结构、行为、安全和质量，均有机器验证方法，无隐藏未决项；自主冻结 AC。
- 2026-07-28 | P3 | ITER-0093 | dangerous-ack | Plan Admission=pass；选择标准库单内核、显式项目根、严格完整配置与原子替换，配置缺失和配置损坏分流清楚，Must Fix=0；自主进入 P4。
- 2026-07-28 | P5-review | ITER-0093 | dangerous-ack | 完整强审发现 1 个 Must Fix：原子替换后目录同步若失败会出现“命令报错但配置已改变”；已把全部可失败步骤前移到发布前，并补故障注入及路径/字段负向回归。
- 2026-07-28 | P5-review | ITER-0093 | dangerous-ack | 修复后配置专项 18/18、完整 CI reproduced 与 diff check 通过；最终 Must Fix 0、Should Fix 0。项目 `independent_review` 为 off，未执行 fresh-context 独立复核并如实披露。
- 2026-07-28 | close | ITER-0093 | dangerous-ack | Goal 十一项检查全绿、9 份 evidence 整包归档，五件套、双格式交付与 4 个知识主题折叠完成；R1 closed，继续 MILE-0013 R2。
- 2026-07-28 | route | ITER-0094 | dangerous-ack | 自动开启 MILE-0013 R2；以 project-config 纯迁移计划 + upgrader 既有事务承接双文件变更，不提前切消费端或登记未发布版本 action。
- 2026-07-28 | P2 | ITER-0094 | dangerous-ack | AC1–AC7 覆盖 legacy 解析、JSON 优先、冲突、正文保真、升级事务、新部署和完整回归，均有机械验证方法；自主冻结。
- 2026-07-28 | P3 | ITER-0094 | dangerous-ack | Plan Admission=pass；采用纯 parser/plan + upgrade transaction 单一 journal，模糊 Markdown fail-closed，Must Fix=0；自主进入 P4。
- 2026-07-28 | P2-reentry | ITER-0094 | dangerous-ack | 实现核对发现 AC3 未点名 legacy `Review Policy` 清理；在原迁移影响面内补明并重新自审冻结，不新增消费端或版本链范围。
- 2026-07-28 | P5-review | ITER-0094 | dangerous-ack | 完整强审发现 1 个 Must Fix：未来版本含 `migrate_config` 后，已在当前版本的项目若配置被删会被 `already-current` 隐藏；已按 released action 增加 current-version config drift 检查和回归。
- 2026-07-28 | P5-review | ITER-0094 | dangerous-ack | 修复后 project-config 27/27、upgrader 18/18、完整 CI reproduced 与 diff check 通过；最终 Must Fix 0、Should Fix 0。独立复核未启用并如实披露。
- 2026-07-28 | close | ITER-0094 | dangerous-ack | Goal 十一项检查全绿、9 份 evidence 整包归档，五件套、双格式交付和 4 个知识主题折叠完成；R2 closed，继续 MILE-0013 R3。
- 2026-07-31 | route | ITER-0107 | dangerous-ack | 用户要求危险模式做完 MILE-0015 R1；配置解析为 `dangerous=true`、source=config、零 legacy 冲突。授权上限冻结为 Butler 仓；既有工作树非干净，P4 回滚锚点采用进入危险任务时的 diff SHA-256 `0dec6e81b7972e34602e9885886cce4846eece17cc9c3334889119124a3d0a6e`，不自动提交或覆盖用户改动。
- 2026-07-31 | P2 | ITER-0107 | dangerous-ack | AC1–AC7 自审通过并自主冻结：每条均有确定性结构检查或基于真实冲突的语义审查，覆盖领域边界、术语所有权、真源防双写、冲突反证、入口注册、行为非回归与外部参考合规；范围上限 15–20 个概念，无隐藏行为改动或未决阻断项。
- 2026-07-31 | P3 | ITER-0107 | dangerous-ack | Plan Admission=pass：采用独立 `Coder/domain-model.md` + README/architecture 两处薄接线，20 行人读审计只存所有权与真源指针；否决把内容塞进规则分层总览、提前建设 JSON registry 和重排目录。AC1–AC7 全覆盖，Must Fix=0，进入 P4。
- 2026-07-31 | P4 | ITER-0107 | execute | 新增五上下文领域地图、20 项统一语言审计与双冲突反证；只接线 `Coder/README.md`、`Coder/architecture-overview.md`，未改冲突真源或运行行为。结构合同、链接、diff 检查均通过；完整 CI 首次因沙箱拒绝 uv 缓存失败，保留 `full-ci` 记录，获准环境用 `reproduced-full-ci` 原命令重跑通过，进入 P5。
- 2026-07-31 | P5 | ITER-0107 | dangerous-review | 完整多维审查 verdict=pass，Must Fix=0、Should Fix=0；风险相关领域合同以 `review-domain-model-contract` 重跑通过。`independent_review=false` 且当前未授权子 agent，故未执行 fresh-context 独立复核并在 VERIFY_REPORT 明示。AC1–AC7 均有 passed evidence，进入 Goal 完成资格裁决。
- 2026-07-31 | close | ITER-0107 | closed | Goal Assurance verdict=`eligible`；evidence 热区校验后整包归档，四件套/CHANGELOG 快照与 `deliveries/ITER-0107-domain-model-boundaries.{md,html}` 落地；MILE-0015 R1 置 closed，项目知识折叠到 architecture/invariants/frontier，迭代台账 current 置 none。
- 2026-07-31 | milestone-evolve | MILE-0015 | route-added | 根据上下文成本审计新增 planned R2“上下文预算与渐进注入”：初始只植入语义路由内核，领域路由/术语查询/完整审计分层加载，限制真源扇出并建立体量门禁；原 R2–R4 顺延为 R3–R5，未预占 ITER 号。
- 2026-07-31 | route | ITER-0108 | full | 用户明确启动领域模型治理 R2；原分支当时基于 `max_used=99` 领取了后来发生冲突的本地编号，2026-08-04 汇合后正式校正为 ITER-0108 / MILE-0015。分流命中多文件、契约、跨模块与设计取舍，进入 P1；危险模式配置仍为 ON，但本次启动指令只推进到 P1，不自动全程收口。
2026-07-31 | P1→P2 | ITER-0108 | user-ack | 用户确认上下文预算与渐进注入的 P1 方向；P2 选择独立 L2 术语查询文档，AC 保持 draft 等待逐项冻结。
2026-07-31 | P2-amend | ITER-0108 | user-challenge | 用户指出“最多 3 份真源”可能妨碍复杂问题取证；修订为每批 3 份的默认预算，超额须先记录证据缺口、压缩前批结论并说明下一批理由，可连续分批或显式升级 L3，不设牺牲正确性的总数硬顶。
2026-07-31 | P2→P3 | ITER-0108 | user-ack | 用户确认 AC1–AC8；AC_LIST 置 ack-frozen。P3 采用 L0 README + L1 domain-model + L2 domain-glossary + L3 历史审计分层，并以静态预算门和六字段运行期升级回执共同约束渐进加载；TECH_PLAN 保持 draft 等待方案 ACK。
2026-07-31 | P3→P4 | ITER-0108 | user-ack | 用户确认技术方案，Plan Admission=pass，进入 P4。工作树已有 R1/里程碑状态改动，不自动提交或覆盖；执行前 `git diff --binary` SHA-256=`3bbba51c69b6c5acf9c1421f96d31aaf9fde3326819b774f62f962a1fb59c34d`。迁移前术语集合已核对为 20 项。
2026-07-31 | P4→P5 | ITER-0108 | execute | 完成 L0 README、L1 domain-model、L2 domain-glossary、L3 历史审计分层；新增标准库 context-budget CLI、5 组负向测试并接入完整 CI。基线 L0=694 bytes/6 非空行/2 指针，L1=3894 bytes/55 行/11 指针，contexts=5、terms=20、routes=4；Markdown、artifact、state audit、diff 与完整 CI 通过。
2026-07-31 | P5-review | ITER-0108 | self-review | 同上下文简评发现定义真源 symlink 可逃逸仓库根，判 Must Fix 并退回 P4 修复；共享校验增加 resolved path 必须位于 PROJECT_ROOT 的约束和负例。`review-context-budget-tests`、`review-context-budget-contract`、`review-full-ci` 复现通过；最终 Must Fix=0、Should Fix=0，独立复核配置为 false。
2026-07-31 | route | ITER-0109 | full | 用户确认继续领域模型治理；原分支当时基于 `max_used=100` 领取了后来发生冲突的本地编号，2026-08-04 汇合后正式校正为 ITER-0109 / MILE-0015 并绑定 R3。按 L0/L1 渐进读取首批只展开 milestone、iteration、concept 三份直接真源；P1 将范围锁在五段主链转换合同与既有真源对账，不提前吞并 R4 机器合同和冲突试点。
2026-07-31 | P1→P2 | ITER-0109 | user-ack | 用户确认 P1；第二批读取 references/acceptance/tech-plan，确认 PRD 钉版三元组与 Plan 逐 AC 继承；第三批读取 verify/goal/handoff，确认 evidence 证明、Goal 聚合裁决和 handoff 单向派生。证据覆盖五段后停止下钻，起草 AC1–AC8，保持 draft 等待冻结。
2026-07-31 | P2→P3 | ITER-0109 | user-ack | 用户确认 AC1–AC8；AC_LIST 置 `ack-frozen`。P3 聚焦独立按需主链合同、薄导航和静态负向检查，不复制 schema 字段全集、不改现有运行算法、不提前吞并 R4 试点。
2026-07-31 | P3 | ITER-0109 | plan-draft | 方案采用按需 `Coder/context-map.md` + L1 薄指针，并扩展现有 context-budget parser/test/CI；否决膨胀 domain-model、新增 JSON registry 和第二 checker。AC1–AC8 覆盖完整，预审 Must Fix=0，方案保持 draft 等待用户 ACK。
2026-07-31 | P3→P4 | ITER-0109 | user-ack | 用户确认技术方案，Plan Admission=pass。进入 P4 前工作树已有 R1/R2 与当前状态改动，不自动覆盖或提交；`git diff --binary` SHA-256=`25d9b55bbc21c1a9f1b0a9f2a2ded0b04eb24ef94a32a0557868eb54f73913e4`。
2026-07-31 | P4 | ITER-0109 | execute | 新增 `Coder/context-map.md` 四类事实层级和五段九字段合同；README/L1/architecture 薄接线，扩展现有 context-budget checker 与 3 组负例。首次专项暴露“权威事实→权威事实”被误判为分类不足，已修正为箭头两侧分别命中合法分类；最终专项 9/9、合同基线、链接与 diff check 通过。
2026-07-31 | P4→P5 | ITER-0109 | execute | 沙箱外完整 `scripts/verify-ci.sh` exit 0；context-map 指标为 6172 bytes/90 行/20 指针、四类事实、五段转换，R2 L0/L1/20 术语基线保持通过。进入 P5 evidence 与同上下文审查。
2026-07-31 | P5-review | ITER-0109 | self-review | 同上下文审查发现 1 个 Must Fix：权威方向只检查合法分类子串，`未知事实 + 受控投影` 可混入；退回 P4 改为箭头两侧严格 token 集，并补未知分类与导航重复块负例。`review-context-map-*` 与 `review-full-ci` reproduced 通过，最终 Must Fix=0、Should Fix=0；`independent_review=false` 未执行独立复核。
2026-07-31 | close | ITER-0109 | closed | Goal Assurance 首次因 Evidence Index 使用热区路径无法识别，校准为规范归档路径后 verdict=`eligible`；13 份 evidence、五件套和双格式交付归档，R3 置 closed，知识折叠到 architecture/invariants/frontier，MILE-0015 继续 R4。
2026-07-31 | close-audit | ITER-0109 | passed | 关闭态 state ledger、handoff freshness、artifact contract、context-map 合同、归档 evidence、项目状态审计与 `git diff --check` 全绿；最终完整 CI exit 0（Pi tsc 仅存既有模块解析跳过提示），未提交、未切版、未推送。
2026-08-04 | history-reconcile | MILE-0015 | renumbered | 跨设备汇合发现已发布 `main` 已占用 MILE-0014 与 ITER-0099～ITER-0106；发布历史保持不动，领域模型治理整体改号为 MILE-0015，R1～R3 改号为 ITER-0107～ITER-0109，并同步归档目录、交付文件、证据回执、复合台账与知识折叠 receipt。
