# 部署种子 + 文件夹化迁移配方（规则层准备）

> ITER-0032 · 迭代交付（小版本）· 收口 2026-07-07 · MILE-0003 R6 · 监督态自驱（用户"继续接下来的迭代"委托，非 /dangerous；P5 起独立复核守质量）

## 本次交付目标

- R2 定了 `.ai/project/` 知识文件夹契约、R5 把冷启动第一读接成两态，但两个上游口子一直空着：**新项目怎么带上这个文件夹**（部署种子）、**老项目单文件 `.ai/PROJECT.md` 怎么升级成文件夹**（迁移配方）。知识文件夹的契约/维护/读序再全，没人把它部署出来、迁移过去，就永远只是纸面。
- R6 补这两块**规则层准备**，让文件夹态"能被部署出来、能被迁移过去"。**边界**：R6 只备规则（部署协议两态化 + `[split]` 标签 + 配方形态），**不切版、不产 `migrations/v2.0.0.md` 实例、不迁 butler 自身**——那些是 R8 的活。

## 已完成内容

- **块1 · 部署种子**（`mcv-deployment §2`）：
  - 项目全貌产物条从单态（仅 `.ai/PROJECT.md`）改写为**两态**——新项目用 `.ai/project/` 知识文件夹、单文件 `.ai/PROJECT.md` 是遗留/暂态形态（R6 前的老项目 + R8 前的 butler 自身）。
  - 部署时创建**空** `.ai/project/` 目录种子（同 `origin/` 空收件箱：建目录、不预置内容）。空目录**标记该项目采用文件夹态**，供收口步④判"折进文件夹还是前滚单文件"。它是**唯一在部署时即建的 `.ai/` 子目录例外**（`references/`/`iterations/`/`milestones/` 仍按需产生），例外理由已记账。
  - `00_INDEX` **不 stub**——首次收口前滚才由更新说明帮手生成（避免部署时写一份"自信的谎"空地图）。
  - line 45 老项目升级补建指针指向 R6 文件夹化迁移配方。
- **块2 · 文件夹化迁移配方**（`migration-schema §4/§6`）：
  - 新增 typed 标签 **`[split]`**：把 `.ai/` 下单文件产物按主题拆成知识文件夹（首例 `PROJECT.md → .ai/project/`），带起始态校验（旧单文件存在且目标文件夹未成形才动）+ 冲突即停（漂移退 ACK、不覆盖、绝不拆丢用户手写内容）。
  - §6 文档化 `PROJECT.md → .ai/project/` 迁移配方**形态**（`[rename]` + `[split]` + `[restamp]` 三步骨架），声明实例 `migrations/v2.0.0.md` 留 R8 切版时产、R6 不预落。
- **指针翻**：`project-digest §9` header `R3/R5`→`R3/R5/R6 已接线` + R6 路线项待→已（明注 `v2.0.0.md` 实例仍 R8）；`README` 部署清单补空 `.ai/project/` 种子。

## 关键变更 / 用户可感知变化

- **新项目部署后生来带 `.ai/project/` 空知识文件夹种子**——R5 定的文件夹态第一读从此有真项目可走（首次收口后 `00_INDEX` 一生即生效）。
- **老项目有了升级路径**：`[split]` 标签让 `PROJECT.md → .ai/project/` 的文件夹化成为可照做的配方步（实际实例待 R8 切版产）。
- **R6/R8 边界严守**：R6 只备"标签 + 形态 + 条件式前向指针"，不预写 `migrations/v2.0.0.md`——那是切版产物（`versioning §6.3 步4`），此刻写＝引用一个未打的 tag、悬空。

## 收口时修复（P5 独立复核 MF-1）

- P5 对抗式复核揪出一个 Must Fix：R6 新引入的"空 `.ai/project/` 种子"暂态（目录在、`00_INDEX` 未生）会诱导冷启动踩空——`context-persistence §6` 两态判据措辞"采用 `.ai/project/` 的项目→读 `00_INDEX`"，加上 mcv §2 自述"空目录=采用标记"，字面读者会去读一个不存在的 `00_INDEX`；而救回它的"键控入口文件"澄清只写在 mcv §2（部署协议），**没落进冷启动读者实读的 context-persistence §6**。
- **修复**：给 `context-persistence §6` line 124 文件夹分支补一句**入口文件 `00_INDEX.md` 存在性判据守卫**（空种子暂态→按"缺全貌产物"倒推、不读空 `00_INDEX`）+ line 130 兜底句点名空种子。修后 mcv §2 ↔ context-persistence §6 双向自洽，冷启动读者本地闭合。
- **边界校正透明记账**：冻结的 AC8 列"无 R5 读序第一读改动"，本轮 touch 了 `context-persistence §冷启动读序`——但此改是为 R6 **自身新引入的空种子暂态**补冷启动安全守卫（R5 没预见的第三态），**不改 R5 两态第一读语义**，是"把部署种子做安全"这个 R6 交付物的内在部分，非重开 R5。记为 P5 驱动的合理边界校正，非静默越界。

## 高层影响范围

- 改（章节级，5 规则文件）：`20_Workflow_Lifecycle/mcv-deployment.md §2`、`migration-schema.md §4/§6`、`40_Context_Management/context-persistence.md §6`（MF-1 守卫）、`project-digest-schema.md §9`、`Coder/README.md`。
- 收口前滚（本迭代自身，butler 单文件态）：`.ai/PROJECT.md` 知识文件夹条 R6 指针 待→已（R8 仍待）。
- 没碰（R6 边界）：`migrations/v2.0.0.md` 实例（R8 切版产）、butler 自身 `.ai/PROJECT.md → .ai/project/` 实体迁移 + `VERSION` 切版（R8）、R3 折叠必做/第 6 不变量语义、R5 两态第一读语义（仅补空种子守卫）、`.ai/project/` 结构契约（R2，§1–§8）、hook、`presentation-protocol`/`artifact-style`（R7）。

## 验证方式与结果摘要

- **8/8 AC 通过**（AC3 经 MF-1 修复后翻过），全 **auto·可靠**（规则文档：读正文确认 + `git`/`grep` 核守恒，确定性可复现）；无人测道残余。
- P5 **独立复核**（fresh-context 子 agent，验证者≠实现者）：初判 REQUEST-CHANGES（1 Must Fix，MF-1 空种子踩空），修复后逐 AC 复核 8 过。**对抗点全过**：`migrations/` 无 `v2.0.0.md`、4 处 `v2.0.0.md` 引用均"留 R8 产"不悬空、前向指针 `versioning §6.3 步4` 真实、`[split]` 幂等+漂移即停自洽、单文件分支显式含 butler、`project-digest §9` 明注实例仍 R8 不虚报。
- 守恒核对：`git status` 改动集=5 改规则文件 + `.ai/` 台账 + PROJECT.md 前滚；无 `migrations/v2.0.0.md` 新增、无 `VERSION`/`CHANGELOG` 切版、无 rename（`^R`=0）、无 hook 改动。

## 已知剩余风险 / 延后事项

- **文件夹态仍无真实项目验证**（承 R5）：R6 只备"能种、能迁"的规则层；真跑要到有新项目部署（走空种子）或 R8 butler 自身迁移后。此前含 butler 在内所有项目仍走单文件态。
- **迁移配方实例 `migrations/v2.0.0.md` 未产**（R6 边界，非欠债）：配方在切版时产（`versioning §6.3 步4`），R8 切 v2.0.0 时落。
- 本轮按惯例收口即提交，**未推送、未切版**；MILE-0003 仍 active，剩 R7（说人话）/ R8（butler dogfood + 切 v2.0.0），待用户指令。

## 引用（只引用路径，不嵌全文）

- 归档四件套 + 切片：`.ai/iterations/ITER-0032/CONCEPT.md` / `AC_LIST.md` / `TECH_PLAN.md` / `VERIFY_REPORT.md` / `CHANGELOG.md`
- 改动：`Coder/20_Workflow_Lifecycle/mcv-deployment.md`、`migration-schema.md`、`Coder/40_Context_Management/context-persistence.md`、`project-digest-schema.md`、`Coder/README.md`
- 相关契约：`migration-schema.md §4`（`[split]` typed 标签）/`§6`（切版产配方）、`versioning-schema.md §6.3`（切版步骤）、`project-digest-schema.md §8`（00_INDEX 模板）
