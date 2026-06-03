# 修订记录
- 无（本迭代需求一次冻结，无迭代内修订）

# Goal
- 让"每个迭代文档 scoped 有界"成为硬约束，防止文档纵向堆积不可控

# In Scope
- Fix 1 工作区严格 overwrite-only：开新迭代时四件套必须整体覆写，禁止保留/追加上一迭代内容
- Fix 2 CHANGELOG 收口归档：`01_CHANGELOG.md` 只承载当前活跃迭代热数据，收口随迭代归档进 `iterations/ITER-NNNN/CHANGELOG.md`
- Fix 3 deliveries 引用不嵌入：交付总结必须以指针引用 AC_LIST/TECH_PLAN/VERIFY_REPORT，不得全文嵌入
- dogfood：覆写工作区为 ITER-0003、归档、收口

# Out of Scope
- 不改 hook（overwrite-only 是规则强制，非机制强制）
- 不回溯重命名/迁移历史 deliveries 与既有归档
- 不引入台账一致性 linter（顺延到后续候选）

# Acceptance Checklist
- [ ] AC1: `iteration-schema.md` §5.1 明文规定开新迭代时工作区四件套整体覆写、禁止保留或追加上一迭代内容；§1 或 §3 含"文档有界、历史横向归档"不变量
- [ ] AC2: `iteration-schema.md` §5.5 收口动作把当前迭代的 CHANGELOG 切片随四件套快照进 `iterations/ITER-NNNN/`；`01_CHANGELOG.md` 定义为活跃迭代热数据
- [ ] AC3: `delivery-summary.md §4.7`（及编写原则）硬性规定只引用不嵌入 AC_LIST/TECH_PLAN/VERIFY_REPORT 全文
- [ ] AC4: `lifecycle.md` P1 开启段含 overwrite-only 要点、P5 收口段含 CHANGELOG 随迭代归档
- [ ] AC5: `mcv-deployment.md §2` 把 `01_CHANGELOG.md` 标注为当前迭代热数据、`iterations/ITER-NNNN/` 含可选 `CHANGELOG.md`
- [ ] AC6: `mcv-update.md §5.1` 改为"CHANGELOG 按迭代收口自动归档，体积分片退化为兜底"，与新口径自洽
- [ ] AC7: dogfood 自洽——工作区覆写为 ITER-0003（无 ITER-0002 残留）、归档/台账/交付三层一致、交付文件不含四件套全文嵌入

# Verification Method
- AC1-AC6: 阅读各目标文件，核对新增/修改段落与本清单逐项映射，确认规则间无自相矛盾
- AC7: diff 确认工作区四件套为 ITER-0003 内容；列 `.ai/iterations/ITER-0003/`；grep 交付文件确认 AC_LIST/TECH_PLAN 仅以路径出现

# Open Questions / Risks
- 风险：CHANGELOG 改为按迭代归档与 `mcv-update.md` 旧的体积分片口径并存，需确保不矛盾（AC6 兜底）
- 无未决问题
