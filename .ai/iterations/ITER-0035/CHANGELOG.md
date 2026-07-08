> ITER-0035 · 补 [split] 升级接线缺口 · 收口即归档

本文件是**当前活跃迭代**的对象级变更流（ADD/EDIT/DELETE）。收口时归档至 `iterations/ITER-0035/CHANGELOG.md`。

## ADD

- `Coder/20_Workflow_Lifecycle/butler-upgrade.md` 新增 `§6.5 单文件文件夹化（[split]）`：升级执行器落地 `[split]` 的四要素——① 起始态校验（旧 `.ai/PROJECT.md` 在**且** `.ai/project/00_INDEX.md` 未成形才动）；② opt-in 选择闸（现在迁 / 继续单文件以后再迁，选后者跳过本步、两态并存）；③ 拆分动作（按 `project-digest-schema §8` 主题集路由 + `git add` + 删旧单文件）；④ 冲突即停（漂移不覆盖、退 ACK、绝不拆丢用户内容）+ 幂等；语义真源回指 `migration-schema §4`。

## EDIT

- `Coder/20_Workflow_Lifecycle/butler-upgrade.md §5.1`：typed 标签枚举补 `[split]`（指 §6.5）；加一段性质分类——**机械步**（`[regen-claude]`/`[rename]`/`[add-field]`/`[sync-hooks]`/`[restamp]`）静默自动，**结构迁移步 `[split]`** opt-in、非自动。
- `Coder/20_Workflow_Lifecycle/butler-upgrade.md §7`：验证清单加一行——`[split]` 结果二选一如实报告（已迁文件夹态 / 用户选择暂缓），无"该停没停 / 暂缓未报告 / 拆丢内容"的静默。
- `Coder/20_Workflow_Lifecycle/migration-schema.md §4`（`[split]` 条）：补一句升级执行语义交叉引用（`/butler-upgrade` 里为 opt-in 非自动，落地见 `butler-upgrade §6.5`）；**语义真源仍在 §4**，只加指针不搬定义。
- `migrations/v2.0.0.md`「迁移步骤」：加 opt-in 注——`[split]`（步骤 1）非机械自动、执行器先问，选继续单文件则跳过步骤 1 只跑 2–3，指 `butler-upgrade §6.5`。

## DELETE

- 无
