# Goal
- 支撑 AC1–AC7：把三处软指令改为硬约束并保持规则自洽，dogfood 收口 ITER-0003

# Files / Modules to Change
- `Coder/20_Workflow_Lifecycle/iteration-schema.md` — §1 加"文档有界"不变量；§5.1 加 overwrite-only 硬约束；§5.5 收口加 CHANGELOG 归档
- `Coder/20_Workflow_Lifecycle/lifecycle.md` — P1 开启段加 overwrite-only；P5 收口三步描述补 CHANGELOG 归档
- `Coder/20_Workflow_Lifecycle/delivery-summary.md` — §4.7 + §6 硬性"引用不嵌入"
- `Coder/20_Workflow_Lifecycle/mcv-deployment.md` — §2 `01_CHANGELOG.md` 标注热数据、归档目录含可选 CHANGELOG.md
- `Coder/20_Workflow_Lifecycle/mcv-update.md` — §5.1 CHANGELOG 改为按迭代自动归档、体积分片退化兜底
- dogfood：`.ai/{CONCEPT,AC_LIST,TECH_PLAN,VERIFY_REPORT}.md`（覆写 ITER-0003）、`.ai/iterations/ITER-0003/`、`.ai/ITERATIONS.md`、`deliveries/ITER-0003-doc-scoping-hardening.md`

# Interface / Contract
- overwrite-only 契约：开新迭代 = 工作区四件套整体替换为本迭代内容，上一迭代内容仅存于 `iterations/ITER-NNNN/`
- CHANGELOG 契约：`01_CHANGELOG.md` 作用域 = 当前活跃迭代；收口时切片归档，全局文件回到只含开放迭代热数据
- delivery 契约：交付总结对 AC_LIST/TECH_PLAN/VERIFY_REPORT 仅引用路径，禁止全文嵌入
- 工作区四件套路径不变 → hook 零改动

# State / Boundary
- 状态边界：三条约束都作用在"迭代开启"与"迭代收口"两个时刻，不新增阶段
- 模块边界：`iteration-schema.md` 定机制，`lifecycle.md` 定阶段接入，`delivery-summary.md` 定交付层，`mcv-*` 定部署/升级层，引用不复制
- 不在范围内：hook、rule-card、README/HUMAN_GUIDE（无结构变化）

# Design Decisions
- overwrite-only 用规则强制而非 hook：hook 无法可靠判断"内容是否携带上一迭代"，强行机制化代价高收益低；规则明文 + 归档兜底已足够
- CHANGELOG 选"按迭代收口自动归档"而非"全局 + 被动体积分片"：让分片随迭代边界自动发生，体积超标分片退化为异常兜底，根治无界增长
- delivery 选"硬禁嵌入"而非"建议引用"：把软约束升级为不得，AI 无解释空间
- 未命中任何 Domain / Stack Profile；仅按通用 SOP 推进

# Execution Steps
- Task 1: 改 `iteration-schema.md`（§1 不变量 + §5.1 overwrite-only + §5.5 CHANGELOG 归档）
- Task 2: 改 `lifecycle.md`（P1 + P5）
- Task 3: 改 `delivery-summary.md`（§4.7 + §6）
- Task 4: 改 `mcv-deployment.md §2`
- Task 5: 改 `mcv-update.md §5.1`
- Task 6: dogfood — 写 VERIFY、归档 ITER-0003、台账加行收口、写交付

# Verification Plan
- AC1–AC6: 逐文件阅读核对；交叉检查 CHANGELOG 三处口径（iteration-schema/mcv-deployment/mcv-update）无矛盾
- AC7: `git diff` 工作区四件套为 ITER-0003；`ls .ai/iterations/ITER-0003/`；`grep -n 'AC_LIST\|TECH_PLAN' deliveries/ITER-0003-*.md` 仅路径

# Risks / Open Questions
- CHANGELOG 口径分散在三文件，改动需同步，否则自相矛盾 → 由 AC6 交叉核对兜底
- 无未决问题
