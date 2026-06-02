# Goal
- 为 butler SOP 引入"迭代化需求管理"：增量迭代中每个迭代有确定的单调递增迭代号 `ITER-NNNN`，落下对应文档，并锁定该迭代的需求范围（"固定需求"）

# Current Understanding
- 现状：`.ai/` 下只有单套阶段产物（`CONCEPT.md` / `AC_LIST.md` / `TECH_PLAN.md` / `VERIFY_REPORT.md`），每个新任务覆盖上一套，缺少"某次迭代固定了哪些需求、产出了哪套文档"的稳定身份
- 增量历史只能靠 `01_CHANGELOG.md` 流水 + `deliveries/` 日期命名，无法按迭代号回溯
- 预期产出：新增 `iteration-schema.md` 机制 SSOT；在 `lifecycle.md` / `mcv-deployment.md` / `delivery-summary.md` / `README.md` / `templates/rule-card.md` 中接入迭代号、台账、归档与收口纪律；并在 butler 自身 dogfood 验证

# Constraints
- 显性约束：
  - hook 不改：工作区四件套保持固定路径，`phase_gate` 校验的 `.ai/CONCEPT.md` 等路径不动
  - 不破坏三层分层（SOP Core / Domain Profiles / Business Extension）与产物链
  - 新增规则文件必须注册进 `Coder/README.md`（项目约束 #3）
  - 浓缩规则 SSOT 是 `templates/rule-card.md`，不双写（项目约束 #4）
  - 不回溯重命名历史 `deliveries/` 文件
- 隐性约束：
  - 归档目录在 `.ai/` 与 `deliveries/` 豁免区内，`is_gated` 不拦
  - 迭代号单调不复用，同一时刻至多一个 active 迭代

# Impact Scope
- 影响（规则层）：新增 `Coder/20_Workflow_Lifecycle/iteration-schema.md`；改 `lifecycle.md` / `mcv-deployment.md` / `delivery-summary.md` / `Coder/README.md` / `templates/rule-card.md`
- 影响（dogfood）：新增 `.ai/ITERATIONS.md`、`.ai/iterations/ITER-0001..0002/`、`deliveries/ITER-0002-*.md`
- 不影响：hook 体系（`templates/hooks/`）、其他 schema、`CLAUDE.md.template` 骨架（经占位符自动透传 rule-card）

# Project Type / Active Profiles
- 项目类型：Markdown 规则仓库（butler 自身）
- 未命中任何 `10_Domain_Stack_Profiles/` profile，仅按通用 SOP 推进

# Open Questions
- 无未决问题。三个核心设计决策已由用户拍板：落盘结构=工作区+收口归档；编号=递增零填充序号；锁定纪律=允许修订、扩张才开新迭代
