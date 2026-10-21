# 项目知识文件夹升级 + 帮手名册 + 说人话（MILE-0003）

> MILE-0003 · 里程碑交付（大版本）· 收口 2026-07-08 · 随 v2.0.0 发布（**MAJOR·破坏性**）· 含迭代 ITER-0026 / ITER-0028 / ITER-0029 / ITER-0030 / ITER-0031 / ITER-0032 / ITER-0033 / ITER-0034（另含正交独立迭代 ITER-0027）

## 本次交付目标

- 三条线并行，攻 butler 冷启动认知的三处系统性短板：① **知识文件夹（主体）**——旧的单文件 `.ai/PROJECT.md` 是一份千余字的薄索引（几个关键词 + "细节看代码"），AI 冷启动读完并不真知道"项目里有什么"，容易沦为"报几个关键词假装体系有用"；② **帮手名册（子项一）**——butler 派出去干活的临时子 agent 一直只有"复核"一个、说明还摊在 5 个文件各写一遍，没有名册；③ **说人话（子项二）**——butler 面向人的输出容易堆术语黑话，看着专业其实难懂（"简短"≠"好懂"）。
- 大版本目标：把冷启动"整体"产物从薄索引升级为**随迭代越补越全、AI 读完真懂"项目里有什么"的实体知识库**，靠"强制 + 可验证的收口折叠"保证不腐；把帮手从 1 个立成名册化 3 个 + 通用规矩唯一真源；把"说人话"从模糊建议收敛成可自检的三条硬标准。因重写了冷启动核心产物契约，按 semver 属 **MAJOR**，收口切 **v2.0.0**。

## 已完成内容

- 八个路线项（R1~R8）分三条线闭环，逐项见下方回填表。主体线 R2/R3/R5/R6/R8 走"契约 → 维护回路 → 读序 → 部署迁移 → 自身 dogfood"五段，子项一 R1/R4（帮手名册骨架 + 补齐），子项二 R7（说人话）。收尾 R8 让 butler 拿自己当第一个真实用户，验证了整套知识文件夹设计第一次真实落地。

## 关键变更 / 用户可感知变化

- **冷启动全貌产物：单文件薄索引 → `.ai/project/` 知识文件夹**（破坏性）：`00_INDEX` 入口 + 按主题分文件（identity/architecture/capabilities/invariants/constraints/debt/frontier）+ digest-and-point 密度（名 + 干什么 + 指针，已有真源不逐字抄）。维护哲学反转：从"按需微调、避免膨胀"改为"每次收口按主题强制折叠 delta、overwrite 禁历史层"。
- **冷启动怎么读也变了**：第一读两态——采用文件夹的项目先读 `00_INDEX` 拿地图、再按需钻相关主题（不 slurp 整个文件夹）；仍单文件的老项目读 `.ai/PROJECT.md`。butler 自己已迁文件夹态。
- **帮手成名册**：`62_Extension_Agents/` 立起——复核（`independent-review`，接 P5）/ 更新说明（`knowledge-fold`，收尾把 delta 折进知识文件夹）/ 查过时（`drift-check`，抽查说明过时）三帮手 + 通用规矩 G1–G4 唯一真源；帮手 = 定义资料用时读、临时起干净子 agent、不下发到项目。
- **说人话成硬纪律**：三条硬标准（术语先解释 / 比喻要落地 / 别让英文·变量裸奔）定义只写一次（`artifact-style §2`）、对话层与文档层同守、发长文前逐条自检。
- **老项目怎么升**：按 `migrations/v2.0.0.md`——`[split]`（想迁时把单文件文件夹化，两态并存不强制立即迁）+ `[regen-claude]`（重生成 CLAUDE.md 规则卡）+ `[restamp]`。

## 高层影响范围

- 新增：`Coder/62_Extension_Agents/`（overview + 三帮手定义）、`Coder/30_Quality_Gate/implementation-discipline.md`（ITER-0027 正交）、`.ai/project/`（butler 自身知识文件夹 8 文件）、`migrations/v2.0.0.md`。
- 改写 / 升级：`40_Context_Management/project-digest-schema.md`（单文件→文件夹契约）、`context-persistence.md §6`（读序两态 + 第 6 漂移不变量）、`iteration-schema §5.5` / `milestone-schema §7.4`（收口步④两态折叠）、`mcv-deployment §2`（部署种子）、`migration-schema §4`（`[split]` 标签）、`artifact-style` + `presentation-protocol`（说人话三条）、`review-engine` G2 单源化 + `dangerous §7.3` / `verify-schema §4` 引用改指、`templates/rule-card.md` + `Coder/README`（同步注册）。
- 删除：`.ai/PROJECT.md`（butler 自身迁走）。
- 未动：P1–P5 阶段状态机、四件套字段结构、AC 验收脊柱、迭代/里程碑双层、`templates/hooks/`（无 hook 变更——本 MAJOR 耦合面小于看起来，因 `PROJECT.md` 本不受 hook 门禁）。

## 拆分路线图回填

| 路线项 | 主题 | 实际 ITER | 状态 | 落点 |
|---|---|---|---|---|
| R1 | 帮手名册骨架 + 复核三拆 + 通用规矩单源化 | ITER-0026 | ✅ closed | `deliveries/ITER-0026-agent-roster-review-split.md` |
| R2 | 知识文件夹 schema：`PROJECT.md` 解构为 `.ai/project/` 契约 | ITER-0028 | ✅ closed | `deliveries/ITER-0028-knowledge-folder-schema.md` |
| R3 | 维护回路：收口强制按主题折叠 + 知识文件夹漂移自检不变量 | ITER-0029 | ✅ closed | `deliveries/ITER-0029-maintenance-loop-wiring.md` |
| R4 | 更新说明 + 查过时两帮手定义成型 + 接线 | ITER-0030 | ✅ closed | `deliveries/ITER-0030-fold-drift-helpers.md` |
| R5 | 冷启动读序切换 + digest-and-point 读纪律 | ITER-0031 | ✅ closed | `deliveries/ITER-0031-coldstart-read-order-switch.md` |
| R6 | 部署种子 + 文件夹化迁移配方（规则层准备） | ITER-0032 | ✅ closed | `deliveries/ITER-0032-deploy-seed-and-folder-migration.md` |
| R7 | 说人话三条硬标准 + 发长文前自检 | ITER-0033 | ✅ closed | `deliveries/ITER-0033-plain-language-standards.md` |
| R8 | butler 自身 dogfood 迁 `.ai/project/` + 对齐现实 + 切 v2.0.0 | ITER-0034 | ✅ closed | `deliveries/ITER-0034-dogfood-knowledge-folder-migration.md` |

- 八路线项全部达成。执行顺序 R1 → R2 → R3 → R4 → R5 → R6 → R7 → R8（先立名册骨架预演"总述+分文件+登记"模式，再定知识文件夹契约、接维护回路、补帮手、切读序、备部署迁移、立说人话，末位 butler 自身 dogfood + 切版收尾）。另含正交独立迭代 ITER-0027（最小实现纪律，不属本里程碑三条线）。

## 验证方式与结果摘要

- 八路线项其下迭代各自 P1–P5 闭环、各自收口交付（见上表链接），多数经 P5 独立复核（干净上下文子 agent、验证者≠实现者、对抗式）；R6/R7 初判 REQUEST-CHANGES→修 Must Fix→全过，R8 段A APPROVE、0 Must Fix。
- 里程碑收口前确认拆分路线图 8 项全 closed、一致性自检 6 不变量全绿（含新增第 6 条知识文件夹漂移，对已迁文件夹态的 butler 自身适用且当轮不漂移）。
- **dogfood（R8 · ITER-0034）**：butler 自身单文件 `.ai/PROJECT.md` 迁成 `.ai/project/`、旧 6 段无遗漏、`architecture` 只摘全貌指 README 不抄目录树、单文件分支逻辑保留给老项目、指针不踩空——知识文件夹设计第一次真实落地验证通过。
- 本里程碑随 v2.0.0 聚合发布（聚合 ITER-0026~0034），迁移配方 `migrations/v2.0.0.md`（`[split]`+`[regen-claude]`+`[restamp]`；无 `[sync-hooks]`/`[add-field]`）。

## 已知剩余风险 / 延后事项

- **`/butler-upgrade` 仍未在真实老项目实跑**（跨里程碑历史 dogfood 债）：本版 `migrations/v2.0.0.md` 的 `[split]` 是首个真实文件夹化配方，真实老项目端到端升级验证仍悬着，风险最高的一步待未来一次真实升级兜底。
- 说人话落规则层、可自检，但"输出真的更好懂"靠后续每次迭代照做 + 收口自检兜底——书写质量不做机器门禁（非机械可判真假的封闭项）。
- 帮手权限靠约定 + G2 诚实兜底（起不了子 agent 则主线自做并如实标注）；"工具层硬拦"留后续增强。

## 引用

- 里程碑产物快照：`.ai/milestones/MILE-0003/MILESTONE.md`
- 其下迭代交付：见上方回填表 8 条 `deliveries/ITER-00NN-*.md` + 正交 `deliveries/ITER-0027-implementation-discipline.md`
- 发布：`CHANGELOG.md` [2.0.0]、`migrations/v2.0.0.md`、`.ai/ITERATIONS.md`、`.ai/MILESTONES.md`
