---
状态: ack-frozen
ACK 日期: 2026-07-08
迭代: ITER-0035
里程碑: 无（独立迭代）
---

# AC_LIST — ITER-0035（补 [split] 升级接线缺口）

> 监督态自驱（用户点选"做A"，非 /dangerous）。验收脊柱贯穿 P4→P5；全为规则文档接线改动，验证=读改后正文确认 + `git grep` 核守恒，确定性可复现（auto·可靠）。

## 块1 · [split] 接进执行器

- **AC1**：`butler-upgrade §5.1` 的 typed 标签枚举**补入 `[split]`**，指向新增的 `§6.5`；与原有 `[regen-claude]`/`[rename]`/`[add-field]`/`[sync-hooks]`/`[restamp]`/`[no-op]` 并列，不遗漏、格式一致。
- **AC2**：`butler-upgrade` 新增 `§6.5 [split] 落地细则`，含四要素——① **起始态校验**（旧单文件 `.ai/PROJECT.md` 存在**且** `.ai/project/00_INDEX.md` 尚未成形才动）；② 拆分动作（按 `project-digest-schema.md §8` 主题集把单文件内容路由进 `00_INDEX` + 主题文件，拆出文件走 `git add`、`git mv` 不适用）；③ **冲突即停**（目标已部分成形 / 旧单文件手工漂移 → 停下报差异、退回用户 ACK、绝不拆丢用户内容）；④ 与 `migration-schema §4` 语义真源的回指（不重述语义定义）。

## 块2 · opt-in 口径定死

- **AC3**：`§6.5` 显式定 `[split]` 为 **opt-in 非自动**——执行器碰到 `[split]` 时**把它抛成一道用户选择**（现在迁 / 继续单文件以后再迁）；选"继续单文件"则**跳过 `[split]`**、单文件分支照常受支持，其余机械步（`[regen-claude]`+`[restamp]`）照跑。显式声明此口径与"两态并存、不强制立即迁"（`project-digest-schema §9` / `migrations/v2.0.0.md`）对齐。
- **AC4**：opt-in 选择闸的定位与既有确认闸（`[add-field]` 草稿值 ACK、漂移即停 ACK）一致——`[split]` 是结构性 / 高风险步骤自带确认闸，不破坏"配方幂等按序执行"模型（迁过不重迁、暂缓则单文件保持）。

## 块3 · 交叉引用 + 验证清单 + 守恒

- **AC5**：`migration-schema §4` 的 `[split]` 定义补一句执行语义交叉引用（指 `butler-upgrade §6.5` 的 opt-in 选择闸），**语义真源仍在 §4**（只加指针、不搬定义、不重述）。
- **AC6**：`butler-upgrade §7` 验证清单加一行——`[split]` 结果二选一如实报告（已迁文件夹态 / 用户选择暂缓继续单文件），无"该停没停 / 暂缓未报告"的静默。
- **AC7**：`migrations/v2.0.0.md` 措辞与新 opt-in 口径自洽（已写"可暂缓"，确认无矛盾；如需微调则同步、不与 `§6.5` 漂移）。
- **AC8**：scope 守恒——改动集限于 `butler-upgrade.md`（§5.1 + 新 §6.5 + §7）+ `migration-schema.md §4`（一句交叉引用）+（若需）`migrations/v2.0.0.md` 微调；**不改** `[split]` 语义定义（拆什么 / 判据 / 冲突即停仍 §4 真源）、**不改**其它 typed 标签执行逻辑、**不改** `mcv-deployment` 部署种子 / `.ai/project/` 结构契约 / hook / `VERSION` / rename、**不真跑** `/butler-upgrade`。
- **AC9（dogfood·说人话）**：本迭代四件套 + 交付按 R7 说人话三条自检（术语先解释 / 比喻要落地 / 别让英文·变量裸奔），收口前逐条扫、命中即改。
