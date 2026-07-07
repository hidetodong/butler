# TECH_PLAN — ITER-0030（MILE-0003 R4）

> 监督态自驱（非 `/dangerous`）：本产物由用户"继续吧"委托、模型自驱产出，P5 起独立复核守质量（ITER-0030，2026-07-07）。

# Goal

- 支撑 AC1–AC8：补齐更新说明 `knowledge-fold` + 查过时 `drift-check` 两帮手完整定义 + 名册登记 + 最小回指接线 + README 注册，接到 R3 回路且不改其强制语义。

# Files / Modules to Change

**新增（2 帮手定义文件，镜像 `independent-review.md` 结构）**

1. `Coder/62_Extension_Agents/knowledge-fold.md` — 更新说明帮手。frontmatter（title/audience/scope）+ §1 一句话 + §2 中立定义表（角色=折叠者 / 输入=本迭代 `01_CHANGELOG.md` delta + 当前 `.ai/project/` / 输出=更新后 topic 文件 / 禁止=改说明以外的东西·凭空编 / 隔离=fresh-context G1 / **权限=只准写 `.ai/project/`**）+ §3 触发（每次收工且动了结构；接 `iteration-schema §5.5 步④` 文件夹态）+ §4 执行（按主题路由 delta 折进对应 topic、overwrite 禁历史层、成本∝改动量，承 `project-digest-schema §6`）+ §5 输出衔接（更新后的 `.ai/project/` + 收口自检第 6 条核）+ §6 诚实兜底（回指 `overview §3` G2）。→ AC1/AC5/AC6
2. `Coder/62_Extension_Agents/drift-check.md` — 查过时帮手。同款结构；§2（角色=查过时者 / 输入=`.ai/project/` 说明 + 真实代码 / 输出=漂移清单"哪几处对不上" / 禁止=改任何文件 / 隔离=fresh-context / **权限=只读**）+ §3 触发（冷启动 / 收口抽查，接 `context-persistence 第 6 不变量`）+ §4 执行（对照 topic 文件 vs 代码 / 近期 CHANGELOG，标脱节项）+ §5 输出衔接（落 `.ai/references/insight-drift-check.md`，喂回主线决定补折）+ §6 诚实兜底（G2）。→ AC2/AC5/AC6

**改（章节级）**

3. `Coder/62_Extension_Agents/overview.md §2` — 名册表两行状态 🔜 R4 → ✅ 本轮立；删占位说明句（co-edit）。→ AC3
4. `Coder/20_Workflow_Lifecycle/iteration-schema.md §5.5 步④` — 文件夹态折叠句末加"（可唤 `62_Extension_Agents/knowledge-fold.md` 帮手 fresh-context 执行）"。→ AC4
5. `Coder/40_Context_Management/context-persistence.md 第 6 不变量` — 句末加"（可唤 `62_Extension_Agents/drift-check.md` 帮手抽查）"。→ AC4
6. `Coder/README.md` — 目录树 `/62_Extension_Agents` 补两文件 + 分文件说明补两行。→ AC8

# Design Decisions

- **DD1 opt-in 措辞硬纪律**：接线一律"可唤 / 推荐唤"，绝不"必须唤"。折叠必做（R3）指"折这件事必做"，"谁做"可主线可帮手——起不了子 agent 时主线做（G2），不卡收口。（对 AC4/AC5/AC7）
- **DD2 两帮手镜像 independent-review 六段式**：格式统一（§1 一句话 + §2 六项中立定义表 + §3 触发 + §4 执行 + §5 衔接 + §6 兜底），降低阅读成本、名册风格一致。（对 AC1/AC2）
- **DD3 G1–G4 单源不重写**：两定义只在 §隔离/§兜底回指 `overview §3`，不抄 G1–G4 正文（承 R1 单源化）。（对 AC6）
- **DD4 权限声明与名册表对账**：knowledge-fold「只写 `.ai/project/`」/ drift-check「只读」写进 §2 权限行，且与 overview §2"只准碰"列逐字对齐；overview §5 名册自检兜底。（对 AC6/AC8）
- **DD5 接线只加可发现性回指、不重复帮手正文**：schema 侧（iteration/context-persistence）各加一句括注，触发/执行细节留帮手 §3/§4，不双写。milestone §7.4 步④ 不单独加（knowledge-fold §3 触发"每次收工"已覆盖里程碑收口）。（对 AC4，最小实现纪律）
- **DD6 不动 R3 强制条**：iteration §5.5 步④"必做"、context-persistence 第 6 条不变量的强制性一字不改，只在句末追加"可唤帮手"括注。（对 AC7）

# Execution Steps（镜像到 task-state）

- [ ] T1 新建 `knowledge-fold.md`（六段式，权限只写 `.ai/project/`）→ AC1/AC5/AC6
- [ ] T2 新建 `drift-check.md`（六段式，权限只读）→ AC2/AC5/AC6
- [ ] T3 改 `overview.md §2` 名册表两行 ✅ + 去占位（co-edit）→ AC3
- [ ] T4 接线：`iteration §5.5 步④` + `context-persistence 第 6 条` 各加一句可唤括注 → AC4
- [ ] T5 `Coder/README.md` 注册两文件 → AC8
- [ ] T6 自检：名册 3 帮手↔3 定义↔权限一致 + grep G1–G4 未重写 + git status 未越 R5/R6/R8 + R3 强制语义未改 → AC6/AC7/AC8
- [ ] T7 P5 独立复核子 agent

# Test / Verify Strategy

- 全 AC 属文档类：读两新定义 + 改动处正文确认要素齐 + `git`/`grep` 核守恒（`auto·可靠`）。
- 关键对抗核：接线处 grep"可唤/推荐"确认非"必须"；模拟起不了子 agent 环境走 G2（主线折叠 + 如实标注）不卡收口。
- `git status --short` 证明改动集=2 新增 + 4 改（overview/iteration/context-persistence/README）+ `.ai/` 台账，无 rename、未触 mcv/migrations/VERSION、读序第一读未改。

# Risks / Rollback

- 风险：接线误写"必须唤" → T4/DD1 + AC5 专项核。
- 风险：权限声明漂移 → DD4 + overview §5 名册自检。
- 回滚：两文件为纯新增（`git rm`），四处改为文本增量（`git checkout --`）可逐一回退；未切版、未动 hook。
