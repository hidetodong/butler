# TECH_PLAN — ITER-0032（MILE-0003 R6）

> 监督态自驱（非 `/dangerous`）：本产物由用户"继续接下来的迭代"委托、模型自驱产出，P5 起独立复核守质量（ITER-0032，2026-07-07）。

## 设计决策（DD）

- **DD1 · 空目录种子而非 stub 内容**（AC2/AC3）：部署建**空** `.ai/project/` 目录、不写 `00_INDEX` 占位。理由：R2 已定 `00_INDEX` 三块（一段话/读序地图/主题登记表）须与实际一致，部署时无内容可填，stub 一份空壳＝"自信的谎"（AI 冷启动信一份假地图）。改用**时序**消解——`00_INDEX` 在首次收口前滚由更新说明帮手按 §8 生，与单文件 `PROJECT.md`"首收口前滚生"同构。空目录仅作**采用标记**，不承诺可读。
- **DD2 · 冷启动键控入口文件、非目录存在**（AC3/两态兼容）：两态判据以**入口文件是否存在**为准（`.ai/project/00_INDEX.md` 在→文件夹态读它；否则 `.ai/PROJECT.md` 在→单文件态读它；都无→缺全貌产物、走 `context-persistence §6` "从迭代 delta 倒推"兜底）。空 `.ai/project/` 目录（部署后·首收口前）落到"都无"分支，**不误触**"文件夹态→读 00_INDEX→踩空"。此为 R5 读序的**运营化澄清**，写进 `mcv-deployment` 部署说明即可，**不改** `context-persistence §冷启动读序` 正文（R5 已定，R6 不碰）。
- **DD3 · `[split]` 通用定义、首例 PROJECT.md**（AC4）：`[split]` 定义写成通用（"把 `.ai/` 下单文件产物按主题拆成文件夹"），`PROJECT.md → .ai/project/` 作首例，不写死只服务这一个。守 §4 幂等（起始态校验：旧单文件在且目标文件夹未成形才动）+ §5 漂移即停（冲突退 ACK 不覆盖）。
- **DD4 · R6 只备规则、不产实例**（AC5/AC6）：迁移配方**实例** `migrations/v2.0.0.md` 是切版产物（`versioning-schema §6.3 步4`：定 bump→改 VERSION→加 CHANGELOG→写 `migrations/vX.Y.Z.md`→打 tag），归 R8。R6 写"标签 + 形态 + 条件式前向指针"，前向指针**不硬编 `v2.0.0`**——用"R8 切版时按此形态产出实例"表述，避免断言一个未打的 tag / 未落的文件已存在。
- **DD5 · 部署种子例外显式记账**（AC2）：`.ai/project/` 成为唯一"部署即建"的 `.ai/` 子目录（`references/`/`iterations/`/`milestones/` 仍按需产生）。这是对 §2 现有"子目录按需产生"叙述的**显式例外**，须在 §2 点名理由（全貌产物之家、标记采用，同 `origin/` 空收件箱先建后投），不留隐式漂移。

## 影响面（章节级）

| 文件 | 改动 | AC |
|---|---|---|
| `20_Workflow_Lifecycle/mcv-deployment.md §2` | 全貌产物条两态化 + 部署建空 `.ai/project/`（记账例外）+ 00_INDEX 不 stub·键控入口文件说明；line 45 老项目升级指针指 R6 配方 | AC1/2/3 |
| `20_Workflow_Lifecycle/migration-schema.md §4` | 新增 `[split]` typed 标签（通用定义 + PROJECT.md 首例 + 起始态校验 + 冲突即停）；§5/§6 关系里点"文件夹化配方形态 + 实例留切版" | AC4/5/6 |
| `40_Context_Management/project-digest-schema.md §9 + §150` | R6 路线项待→已（注 `v2.0.0.md` 实例仍 R8）、header `R3/R5`→`R3/R5/R6`、§150 `[split]` 表述对齐 §4 | AC7 |
| `Coder/README.md`（部署目录清单行） | 部署目录集补 `.ai/project/` 空种子 | AC7 |
| `.ai/PROJECT.md`（收口前滚） | 知识文件夹条 R6 指针 待→已（R8 仍待） | AC7 |

**不碰**：`migrations/`（零新增，AC6）、`context-persistence §冷启动读序`（R5 定，DD2 只在 mcv 侧澄清）、`iteration-schema §5.5`/`milestone §7.4`（R3 折叠语义）、`.ai/project/` 结构契约正文（R2）、hook、`VERSION`/`CHANGELOG`、butler 自身 `.ai/PROJECT.md` 实体结构（R8）。

## Execution Steps（可勾选）

- [ ] S1 · `mcv-deployment §2` 全貌产物条两态化 + 部署建空 `.ai/project/`（例外记账）+ 00_INDEX 不 stub·键控入口文件（AC1/2/3）
- [ ] S2 · `mcv-deployment` line 45 老项目升级补建指针指 R6 文件夹化配方（AC3）
- [ ] S3 · `migration-schema §4` 新增 `[split]` 标签（AC4）+ §6 关系点"文件夹化形态 + 实例留切版·不写 v2.0.0.md"（AC5/6）
- [ ] S4 · `project-digest-schema §9` R6 待→已 + header + §150 对齐（AC7）
- [ ] S5 · `Coder/README.md` 部署目录清单补空 `.ai/project/` 种子（AC7）
- [ ] S6 · 自检 6 不变量（butler 单文件态，第 6 条 N/A）+ scope 守恒核对（`git status`：无 `migrations/` 新增、无 VERSION/CHANGELOG、无 rename）（AC8）
- [ ] S7 · P5 独立复核（fresh-context 子 agent，对抗式：无切版/无 v2.0.0.md 实例/无 butler 实体迁移/`[split]` 已定义/前向指针不悬空/两态兼容不砸单文件）
- [ ] S8 · 原子收口 5 步（归档 + 交付 md+html + 翻台账 + `.ai/PROJECT.md` 前滚 R6→已 + 6 不变量自检）

## 验证策略

全 auto·可靠（规则文档）：每 AC 读改后正文确认 + `git diff`/`grep` 核守恒。核心对抗点＝**两态兼容不砸单文件**（DD2 空目录不踩空）+ **R6/R8 边界**（DD4 无 v2.0.0.md 实例、前向指针不悬空）。无人测道残余。
