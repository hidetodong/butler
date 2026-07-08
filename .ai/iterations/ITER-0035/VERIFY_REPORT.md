# VERIFY_REPORT — ITER-0035（补 [split] 升级接线缺口）

> 监督态自驱（用户点选"做A"，非 `/dangerous`）· 全为规则文档接线改动，验证=读改后正文核契约 + `git grep` 核守恒，确定性可复现（**auto·可靠**）· 无人测道残余（纯规则、无运行时）。

## 验收结果（逐 AC · auto·可靠）

- [x] **AC1 ✓** `butler-upgrade §5.1`（line 74）typed 标签枚举补 `[split]`：见 §6.5，与 `[rename]`/`[add-field]`/`[sync-hooks]` 并列、格式一致、不遗漏。
- [x] **AC2 ✓** 新增 `§6.5`（line 121–131）四要素齐：① 起始态校验（旧 `.ai/PROJECT.md` 在**且** `00_INDEX.md` 未成形才动，line 128）；② 拆分动作（`project-digest-schema §3` 主题集路由 + `git add`、`git mv` 不适用 + 删旧单文件，line 129）；③ 冲突即停（漂移不覆盖、退 ACK、绝不拆丢，line 130）；④ 回指 `migration-schema §4` 语义真源（line 123）。
- [x] **AC3 ✓** opt-in 非自动口径显式（§6.5 line 125–127 + §5.1 blockquote line 78）：执行器不静默自动拆、先呈"现在迁 / 继续单文件"选择；选后者跳过本步、单文件分支继续支持、机械步照跑，明写与"两态并存不强制立即迁"（`project-digest-schema §9` / `v2.0.0.md`）对齐。
- [x] **AC4 ✓** opt-in 闸不破坏幂等：§6.5 line 131「迁过则跳过、暂缓则单文件保持下次仍问」；§5.1 blockquote「两类都幂等、都先校验起始态」。结构性步骤自带确认闸的定位（类比 `[add-field]` 草稿 ACK / 漂移 ACK）记于 CONCEPT DD1 + 关键约束，rule 正文只承载"幂等 + opt-in"事实。
- [x] **AC5 ✓** `migration-schema §4` `[split]` 条（line 37）补一句「升级执行语义……opt-in、非自动……见 `butler-upgrade §6.5`；本条只定标签语义，执行落地不在此重述」——**语义真源仍 §4**，只加指针、未搬定义。
- [x] **AC6 ✓** `§7` 验证清单（line 143）加行：`[split]` 结果二选一如实报告（已迁文件夹态 / 用户选择暂缓），禁"该停没停 / 暂缓未报告 / 拆丢用户内容"静默。
- [x] **AC7 ✓** `migrations/v2.0.0.md` 与新口径自洽：原 line 5（两态并存·非必须马上迁）+ line 22（可暂缓）无矛盾；「迁移步骤」新增 opt-in 注（步骤 1 非机械自动、执行器先问、选继续单文件跳过只跑 2–3、指 §6.5），配方本身闭环。
- [x] **AC8 ✓（scope 守恒）** `git status` 源文件改动集 = `butler-upgrade.md`（§5.1 + 新 §6.5 + §7，+17 行）+ `migration-schema.md §4`（1 句）+ `v2.0.0.md`（opt-in 注 +2 行）；余为四件套 / 台账过程件。**不改** `[split]` 语义定义（§4 真源）/ 其它 typed 标签逻辑 / `mcv-deployment` / `.ai/project/` 契约 / hook / `VERSION` / rename / README。未真跑 `/butler-upgrade`。
- [x] **AC9 ✓（dogfood 说人话）** 三条自检命中即改：裸英文 `surfacing`（AC/CONCEPT/TECH 3 处）改「抛成一道用户选择」、`sync`（CONCEPT 1 处）改「同步」；`opt-in`/`幂等` 首现均有一句话释义（CONCEPT 一句话 line 7「opt-in（问一句再迁）非自动」、§6.5 line 131「迁过则跳过」）；文件名英文带中文上下文，非裸奔。

## 独立复核

- **初评 APPROVE-with-nits**（干净上下文子 agent、验证者≠实现者、只读、对抗式）。四对抗重点：A 两态 opt-in 真守（选继续单文件跳过本步、单文件三回退全落地、与 §9/v2.0.0 口径一致）过；C 起始态校验 + 冲突即停齐、无静默覆盖出口 过；D 枚举无遗漏、§7 无静默出口 过；B 语义单一来源基本成立但 §6.5 部分复述 §4。
- **三处已修复**：① **Must Fix**——§6.5 line 130 悬空指针 `§5.2`（本文件 §5 是有序列表无 §5.2 子节），改指「§5 步骤 2」；② **Should Fix**——§6.5 line 130 判据/冲突即停近逐字复述 §4，收敛为「同 `migration-schema.md §4`」指针 + 保留「绝不拆丢用户内容」红线，消除双写（守 DD2 语义真源不搬家）；③ **Nit**——§6.5 line 129 主题集真源 `§8 模板骨架`→ 改指 `§3 推荐主题集`。修复后无 Must/Should 残留，复核转 **APPROVE**。

## Remaining Risks

- 本轮只接**执行器路径**，仍未真跑 `/butler-upgrade`（既存 dogfood 债，见 `debt.md`）——`[split]` opt-in 闸在真实老项目端到端首验仍悬。
- opt-in 选择闸是"AI 执行时问用户"，靠规则文字约束、非代码强制；真实升级时是否严格先问、暂缓是否如实报告，取决于执行体遵从（同 `[add-field]`/漂移 ACK 的既有信任模型）。
