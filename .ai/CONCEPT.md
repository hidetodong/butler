# Goal
- 把"每个迭代的文档保持 scoped、有界"从软指令变成硬约束，堵死增量迭代中文档纵向堆积、越来越长不可控的风险

# Current Understanding
- 现状（ITER-0002 引入迭代机制后）：分迭代隔离目前靠 AI 自觉"覆写"，无机制兜底；存在三处无界增长口子
  1. 工作区四件套"覆写"是软指令，未明文禁止保留/追加上一迭代内容
  2. `01_CHANGELOG.md` 是 append-only 全局日志，只靠 `mcv-update.md` 体积超标被动分片
  3. `delivery-summary §4.7` 只写"可选引用"，未硬性禁止把 AC_LIST/TECH_PLAN 全文嵌入交付
- 预期产出：在 `iteration-schema.md` / `lifecycle.md` / `delivery-summary.md` / `mcv-deployment.md` / `mcv-update.md` 把这三处改成硬约束，并 dogfood 收口 ITER-0003

# Constraints
- 显性约束：
  - 不破坏既有产物链与三层分层；hook 不改
  - 工作区四件套固定路径不变（仍保证 phase_gate 零改动）
  - 历史靠 `iterations/ITER-NNNN/` 横向铺开，不纵向堆进单文件
- 隐性约束：
  - 改动须自洽：CHANGELOG 改为按迭代归档后，`mcv-update §5.1` 的体积分片要退化为兜底而非主路径
  - overwrite-only 是规则强制，非 hook 强制（hook 难以判断"是否携带上一迭代内容"）

# Impact Scope
- 影响（规则层）：`iteration-schema.md`、`lifecycle.md`、`delivery-summary.md`、`mcv-deployment.md`、`mcv-update.md`
- 影响（dogfood）：覆写 `.ai/` 四件套为 ITER-0003、归档 `.ai/iterations/ITER-0003/`、台账加行、`deliveries/ITER-0003-*.md`
- 不影响：hook 体系、其他 schema、`templates/rule-card.md`（卡片已含迭代约束，本轮不动）、`README.md` / `HUMAN_GUIDE.md`（无目录结构新增）

# Project Type / Active Profiles
- 项目类型：Markdown 规则仓库（butler 自身）
- 未命中任何 Domain / Stack Profile，仅按通用 SOP 推进

# Open Questions
- 无未决问题。用户已确认"就这么落地"，三条硬约束方向已对齐
