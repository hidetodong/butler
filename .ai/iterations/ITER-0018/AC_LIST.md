---
状态: ack-frozen
ACK 日期: 2026-06-30
---

> ITER-0018（MILE-0001 R3）。P2 经用户"按你的来"授权 ACK 冻结（2026-06-30），验收范围锁定，进入 P3。背景见 CONCEPT，不重述。

# Goal

- 把 `01_CHANGELOG.md` 正式化为严格 ADD/EDIT/DELETE 的每迭代精确变更流 + 真 schema + 收编半成品 + Should-Fix 迁新家 + dogfood。

# In Scope

- 新增 `changelog-schema.md`（格式 / 粒度 / 噪声地板 / 与 git·delivery 分工 / 何时写）。
- 重定义 `01_CHANGELOG.md` 语义 + 同步所有引用一致。
- Should-Fix 迁新家（review-engine / dangerous-engine → VERIFY_REPORT）。
- 收口接线（产出 + 归档）+ 与 delivery 分工。
- dogfood + 回填 ITER-0017 范例。

# Out of Scope

- 收口执行门禁 / hook 规则 / 一致性探针（R2 / ITER-0019）。
- 不改四件套字段结构、AC 脊柱、P1-P5 状态机、hook 代码。
- 根 `CHANGELOG.md`（发布史）不动。

# Acceptance Checklist

- [ ] AC1: 新增 `Coder/20_Workflow_Lifecycle/changelog-schema.md`，定义每迭代 changelog 格式——三段 `## ADD` / `## EDIT` / `## DELETE`（严格三类、无内容写"无"不省段）、每条 `` `对象 §章节` — 一句话语义 → ACn ``、顶部 `> <标题> · <active|closed> · <收口日期>`（与 MILE-0001 定调一致）。
- [ ] AC2: schema 明确粒度（文件 + 章节级、不逐行）+ 噪声地板（跳纯排版 / typo，沿用 `maintenance-boundaries §15`）+ 与 git（机械真源）/ delivery（人读散文）分工；写作口径指针引用 `artifact-style.md`。
- [ ] AC3: `01_CHANGELOG.md` 语义重定义为"严格 ADD/EDIT/DELETE 变更流"，并同步所有引用到一致语义、无残留"决策日志"旧义：`mcv-deployment`、`iteration-schema §5.1/§5.5`、`lifecycle §165`、`maintenance-boundaries §15`。
- [ ] AC4: Should-Fix 迁新家——`review-engine §71` + `dangerous-engine §121` 不再写 `01_CHANGELOG.md`，改落 VERIFY_REPORT（口径明确、不静默丢弃）。
- [ ] AC5: 收口接线——`iteration-schema §5.5` 明确完整路径收口产出 `01_CHANGELOG.md` 并归档 `iterations/ITER-NNNN/CHANGELOG.md`（简化路径可省）。
- [ ] AC6: `README.md` 目录结构注册新 schema（消除隐式依赖）。
- [ ] AC7: dogfood——ITER-0018 自身 `.ai/01_CHANGELOG.md` 按新格式产出；并回填 `.ai/iterations/ITER-0017/CHANGELOG.md` 作具体范例（验证格式可用、非空）。
- [ ] AC8: 不双重记账自证——changelog / delivery / ITERATIONS / PROJECT 四者职责边界在 schema 写清；schema 明确 delivery「已完成内容」与 changelog 分工（delivery 高层、changelog 细粒度），无重复记账。
- [ ] AC9: rule-card 联动裁决——判定 changelog 是否进强制产物集并落实结论（进则补、不进记录理由），与"不做存在性硬门禁"一致。
- [ ] AC10: 不破坏不变量——四件套字段 / AC 脊柱 / 状态机 / hook 代码未动；根 `CHANGELOG.md` 发布史未动；本仓五约束自检通过。

# Verification Method

- AC1 / AC2 / AC8: 读新 schema，核对格式定义、粒度 / 噪声地板 / git·delivery 分工、四产物边界。
- AC3: grep `01_CHANGELOG`，确认各引用语义一致、无"决策日志"残留。
- AC4: 读 review-engine §71 / dangerous-engine §121，确认 Should-Fix 改落 VERIFY_REPORT。
- AC5: 读 iteration-schema §5.5，确认收口产出 + 归档步。
- AC6: 读 README 目录结构，确认新 schema 已注册。
- AC7: 查 `.ai/01_CHANGELOG.md` + `iterations/ITER-0017/CHANGELOG.md` 存在、非空、合格式。
- AC9: grep rule-card，确认联动结论已落实。
- AC10: git diff 确认未碰四件套字段 / hook / 状态机 / 根 CHANGELOG；本仓五约束自检。

# Open Questions / Risks

- 见 CONCEPT Open Questions（必产口径 / Should-Fix 落点 / 硬门禁 / 与 delivery 分工），P3 定。
- 风险：与 delivery 重复记账 → 靠 AC8 分工边界（delivery 高层散文、changelog 细粒度操作）化解。
- 风险：Should-Fix 迁移遗漏其他引用点 → AC4 用 grep 全量核对 `01_CHANGELOG` 引用。
