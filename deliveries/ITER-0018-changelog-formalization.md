# 每迭代 changelog 正式化：01_CHANGELOG 重定义为严格 ADD/EDIT/DELETE 变更流

> ITER-0018 · 迭代交付（小版本）· 收口 2026-06-30 · 所属 MILE-0001（R3）

## 本次交付目标

- butler 一直没有"每迭代精确改了什么"的结构化记录：`01_CHANGELOG.md` 只是个没 schema、从没产出过的影子（取向还是"决策日志"），真实变更只活在 deliveries 散文里。
- 本迭代把它正式化为**严格 ADD/EDIT/DELETE 的每迭代对象级变更流**，给真 schema、收编半成品，并把搭便车在它上面的 Should-Fix 留痕迁出。

## 已完成内容

- 新增 `Coder/20_Workflow_Lifecycle/changelog-schema.md`：锁定格式（顶部元信息 + 三段 `## ADD`/`## EDIT`/`## DELETE` + 每条 `` `对象 §章节` — 语义 → ACn ``）、粒度（文件+章节级、rename=DELETE+ADD）、噪声地板、四产物分工、产出/归档时机、写作口径。
- 重定义 `01_CHANGELOG.md` 语义并同步 5 处引用：mcv-deployment §43、maintenance-boundaries §15、iteration-schema §4.4·§5.5、lifecycle §165、mcv-update §5.1。
- Should-Fix 迁新家：review-engine §71 + dangerous-engine §121 改记入 `VERIFY_REPORT.md` 的 `Remaining Risks`；maintenance §15 删除其作为 CHANGELOG 输入；verify-schema §4 收端补口径，契约双向闭合。
- 收口接线：完整路径迭代收口**必产** `01_CHANGELOG.md` 并归档 `iterations/ITER-NNNN/CHANGELOG.md`（简化路径可省）。
- README 注册新 schema；dogfood：产出 ITER-0018 自身 changelog + 回填 ITER-0017 范例。

## 关键变更 / 用户可感知变化

- 以后每个完整路径迭代收口都产一份严格 ADD/EDIT/DELETE 的精确变更流，绑 AC、可追溯——不再靠翻 deliveries 散文倒推改了什么。
- 不双重记账：delivery 写高层人话、changelog 写细粒度对象级、git 是机械全量真源，三者分工写进 schema。
- Should-Fix 从"塞进 changelog"改为"落 VERIFY_REPORT 的 Remaining Risks"——评审产出归评审产物，变更流只记对象级改动。
- 向后兼容：纯 markdown 契约 + 接线，未动四件套字段、AC 脊柱、状态机、hook、根 CHANGELOG。

## 高层影响范围

- 新增：`Coder/20_Workflow_Lifecycle/changelog-schema.md`；`.ai/01_CHANGELOG.md`、`.ai/iterations/ITER-0017/CHANGELOG.md`（dogfood）。
- 改（20 层）：mcv-deployment、maintenance-boundaries、iteration-schema、lifecycle、mcv-update、verify-schema、delivery-summary、README；（60/65）：review-engine、dangerous-engine。
- 没碰：四件套字段 schema、hook、rule-card、P1-P5 状态机、版本机制、根 `CHANGELOG.md`。

## 验证方式与结果摘要

- 10 条 AC 全部满足（逐项见 VERIFY_REPORT）：格式锁定、粒度/噪声地板、语义重定义、Should-Fix 三处全迁、收口必产/归档、README 注册、dogfood、四产物分工、rule-card 裁决、不变量。
- grep 兜底：旧"决策/增量日志"语义零残留；"Should Fix→01_CHANGELOG"零残留（剩余命中均为新增的"不写入"声明）。
- 不变量 git 核对：concept/acceptance/tech-plan schema、hooks、根 CHANGELOG、VERSION 未出现在改动名单。

## 已知剩余风险 / 延后事项

- `mcv-update §5.1` 自动化命令仍含"决策快照"措辞，属老项目（迭代机制上线前）legacy 兜底语境，已加指针澄清，不重写 legacy。
- changelog 必产靠收口纪律、无机械门禁（butler 自身不跑 hook）——R2 / ITER-0019 的执行门禁 + 一致性探针拟覆盖。
- 本轮不切版；MILE-0001 待 R2 收口后聚合发布。

## 引用

- 归档四件套 + 切片：`.ai/iterations/ITER-0018/CONCEPT.md` / `AC_LIST.md` / `TECH_PLAN.md` / `VERIFY_REPORT.md` / `CHANGELOG.md`
- 新增规则：`Coder/20_Workflow_Lifecycle/changelog-schema.md`
- 改动规则：`mcv-deployment.md`、`maintenance-boundaries.md`、`iteration-schema.md`、`lifecycle.md`、`mcv-update.md`、`verify-schema.md`、`delivery-summary.md`、`Coder/README.md`、`review-engine.md`、`dangerous-engine.md`
- dogfood 范例：`.ai/iterations/ITER-0017/CHANGELOG.md` · 里程碑：`.ai/MILESTONE.md`（MILE-0001 R3）
