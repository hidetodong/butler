# Goal

- 支撑 AC1–AC10：新增一份四件套书写口径，并接线进四个 schema、rule-card、README，让四件套内容讲人话、不啰嗦，字段结构不动。

# Files / Modules to Change

- 新增 `Coder/20_Workflow_Lifecycle/artifact-style.md` —— 书写口径正文（核心产物）。
- `Coder/20_Workflow_Lifecycle/concept-schema.md §4` —— 加指针；现有"不记录冗长调查日志"收编为引用。
- `Coder/20_Workflow_Lifecycle/acceptance-schema.md §5` —— 加指针。
- `Coder/20_Workflow_Lifecycle/tech-plan-schema.md §4` —— 加指针；现有"不写流水账"收编为引用。
- `Coder/20_Workflow_Lifecycle/verify-schema.md §4` —— 加指针，并明确 AC 回填用紧凑式。
- `templates/rule-card.md` —— 新增一条紧凑"产物书写"口径。
- `Coder/README.md` —— 目录结构 + 读取顺序 + 规则目录说明三处注册。

# Interface / Contract

- 无代码接口。文件间契约：四个 schema 与 rule-card 通过文件名引用 `artifact-style.md`，口径正文只此一份（单一来源），引用处不重抄细则。

# State / Boundary

- 只约束四件套字段正文怎么写，不碰字段结构、不碰 lifecycle 分流格式、不碰对话层规则。
- 不在本次处理：历史四件套回填、hook 机械校验书写质量（书写质量不做机械门禁，靠规则 + 自检）。

# Design Decisions

- 落点选 20 层独立文件，不塞进某个 schema：四件套是四个 schema 共用的，口径放共用层才不重复；和对话层的 `presentation-protocol.md` 正好对称（那个管对话讲人话，这个管产物讲人话）。
- "讲人话"写成原则 + 点名反面词，不写硬性禁用词清单：清单会漂移、易过时，且 butler 自己的迭代正文绕不开机制名；原则 + before/after 例更柔、更好维护（已与用户敲定）。
- 给一组 before / after 对照例：直接拿本仓 ITER-0011 真实产物的啰嗦片段做反例，改造后做正例，可照抄。
- rule-card 必须同步加一条：四件套书写每个项目都高频用到，不写进这张 AI 最先读到的规则卡，等于没落地。

# Execution Steps

1. 写 `artifact-style.md`（目标 + 讲人话 + 反啰嗦 + before/after + 边界 + 收口自检）。
2. 四个 schema 各加一行指针，收编各自的弱约束。
3. rule-card 加紧凑口径。
4. README 三处注册。
5. P5 逐项验证 + 收口三步。

# Verification Plan

- 按 AC_LIST 的 Verification Method 逐项核对：读新文件 + grep 接线点 + 通读本迭代四件套自证 dogfood + 五约束自检。

# Risks / Open Questions

- 无 hook 强制，靠读取 + 遵守（同 identity / presentation-protocol，可接受）。
- "讲人话 vs 机制名"边界靠语义判断，用 before/after 例兜底。
