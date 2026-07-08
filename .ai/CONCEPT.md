# 补 [split] 升级接线缺口

> 独立迭代 · ITER-0035 · 监督态自驱（用户点选"做A"接力，非 /dangerous）· 不切版

## 一句话

`[split]`（把老项目单文件 `.ai/PROJECT.md` 拆成 `.ai/project/` 知识文件夹）这个标签在 R6 加进 `migration-schema`、R8 产了第一个实例 `migrations/v2.0.0.md`，但**升级执行器 `butler-upgrade.md` 从没同步接线**——`§5/§6` 只会执行 `[regen-claude]`/`[rename]`/`[add-field]`/`[sync-hooks]`/`[restamp]`/`[no-op]`，碰到 `[split]` 没有路由；本轮把它接上，并定死 `[split]` 是 **opt-in（问一句再迁）非自动**，与"两态并存、不强制立即迁"对齐。

## 背景（这缺口怎么来的）

- R6（ITER-0032）只在 `migration-schema §4` 定义了 `[split]` 标签**语义**（拆什么、判据、冲突即停），没碰升级执行器。
- R8（ITER-0034）产了 `migrations/v2.0.0.md` 实例、其步骤 1 就是 `[split]`。
- 但 `/butler-upgrade` 的执行器 `butler-upgrade §5.1` 逐条枚举它认得的标签时**漏了 `[split]`**、`§6` 落地细则也没有 `[split]` 小节。结果：真跑 `/butler-upgrade` 到 `[split]` 那步，AI 没有明确执行路径，只能临时回退去读 `migration-schema §4` 的语义定义拼——不是设计好的自动路径。
- 附带一个未定的口径：typed 步骤默认自动跑，但规则又说"不强制立即迁"。`[split]` 到底自动拆还是问一句？没定死（`v2.0.0.md` 写了"可暂缓"、和"它是配方里的一步"打架）。

## 做什么

- **DD1 · `[split]` 是 opt-in 结构迁移、非机械自动步**：机械标签（`[regen-claude]`/`[restamp]`）升级时静默自动跑；`[split]` 不同——它是哲学级形态迁移，执行器碰到它时**把它抛成一道用户选择**："本版可把你的单文件 `PROJECT.md` 迁成知识文件夹——现在迁 / 继续单文件、以后再迁？"。选"继续单文件"则跳过 `[split]`、单文件分支照常受支持（守两态并存），其余机械步（`[regen-claude]`+`[restamp]`）照跑。
- **A1**：`butler-upgrade §5.1` 标签枚举补 `[split]`（指向新 `§6.5`）。
- **A2**：`butler-upgrade` 新增 `§6.5 [split] 落地细则`——起始态校验（旧单文件在**且** `.ai/project/00_INDEX.md` 未成形才动）+ **opt-in 迁移选择闸**（迁 / 暂缓）+ 拆分动作（按 `project-digest-schema §8` 主题集路由进 `00_INDEX` + 主题文件、拆出文件走 `git add`）+ **冲突即停**（目标已部分成形 / 旧单文件手工漂移 → 停下报差异退 ACK、绝不拆丢用户内容）+ 暂缓分支（跳过但如实报告、单文件继续支持）。
- **A3**：`migration-schema §4` 的 `[split]` 定义补一句执行语义交叉引用（"升级时的 opt-in 选择闸见 `butler-upgrade §6.5`"），语义真源仍在 §4。
- **A4**：`butler-upgrade §7` 验证清单加一行（`[split]` 结果二选一如实报告：已迁文件夹态 / 用户选择暂缓继续单文件）。
- **A5**：核 `migrations/v2.0.0.md` 措辞与新口径自洽（已写"可暂缓"，确认不需改或微调）。

## 边界（不做）

- 不改 `[split]` 的**语义定义**（拆什么、判据、冲突即停仍以 `migration-schema §4` 为真源）——只接**执行器**。
- 不改其它 typed 标签的执行逻辑、不改 `mcv-deployment` 部署种子、不改 `.ai/project/` 结构契约。
- 不真跑 `/butler-upgrade`（那是 dogfood 债、需真实老项目，非本轮范围）。
- 不切版（纯规则接线补齐、向后兼容，属独立迭代；是否随下个版本发布另论）。

## 关键设计约束

- **opt-in 不破坏"配方幂等按序执行"模型**：`[split]` 的用户选择闸类比已有的 `[add-field]` 草稿值 ACK、漂移即停 ACK——结构性 / 高风险步骤本就带确认闸，不是纯机械同步。执行器逐步处理时，`[split]` 这步内含一次 opt-in 分叉，仍是幂等的（迁过了不重迁、暂缓则单文件保持）。
- **语义真源不搬家**：`[split]` 定义仍在 `migration-schema §4`，`butler-upgrade §6.5` 只写"执行器怎么落地它"（起始态校验调用 + opt-in 闸 + git 动作），回指 §4 不重述语义（守单一来源）。
