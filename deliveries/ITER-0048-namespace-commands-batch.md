# 批量铺开 `/butler:` 命名空间命令：一次落三个薄壳，验证「范式可复制 + 目录软链自动托管」

> ITER-0048 · MILE-0005 R2（里程碑第二个迭代、里程碑仍进行中）· 收口 2026-07-14 · dogfood butler 自身 · 标准模式（P2 用户 ACK 三默认）· 判 MINOR·聚合切 v2.8.0（目标项目部署面 `[no-op]`+`[restamp]`）

## 本次交付目标

- R1（ITER-0047）打好了 `/butler:` 命名空间地基：新建 `.claude/commands/butler/` 目录、`/butler-prd` 迁成 `/butler:prd`、`setup.sh` 改成软链整个目录、落 `/butler:review` 当范本。但整套 butler 能力大多仍是规则正文里的散文暗号（`/milestone`、`/butler-upgrade`、`/ideation`），补全菜单里看不见。
- 本次照 R1 的**薄壳路由器**范本，**一次批量落三个低风险命令**——`/butler:milestone`、`/butler:upgrade`、`/butler:ideation`，验证两件事：① 薄壳范式能否稳定批量复制（不是一次性手艺）；② R1 的「整目录软链」是否真能让新命令**零分发动作**自动全局可用。同时把从来只是散文触发词、没有真命令文件的旧名 `/butler-upgrade` 顺势迁成 `/butler:upgrade`（首次为它落真命令文件）。

## 已完成内容

- **新落 3 个薄壳命令**（结构与 R1 的 `prd.md`/`review.md` 同构：读对规则进上下文 → 按 `$ARGUMENTS` 分派 → 委托真源不复述算法〔守 DRY 红线〕→ 第 0 步优雅降级）：
  - **`/butler:milestone`** — 委托 `milestone-schema.md`：留空/贴 brief → 里程碑录入（§6.1 启动信号 → §6.4 录入，含「brief 是大 PRD」并进 `prd-split` 切片 → §7.1 开启登记）；`status` → 只读看板（§6.5，只读不改盘）。收口/废弃/演进走语义（§7.3-7.5）不进命令面，已注明。第 0 步无 `.ai/` 台账则提示先部署基地车、不硬建。
  - **`/butler:upgrade`** — 委托 `butler-upgrade.md`：§3 侦察 → §4 首次/§5 常规区间队列（收「目标戳 < vV ≤ 仓库 VERSION」的 `migrations/` 配方按序幂等执行、漂移即停）→ §6 落地 → §7 验证回退。升级对象是**当前项目**、保护区（`<!-- user-managed -->`/`origin/`）不覆盖。第 0 步没接 butler 则指向 `mcv-deployment`（首次部署≠升级）。
  - **`/butler:ideation`** — 委托 `ideation-engine.md §3`：§3.1 意图探测 → §3.2 需求展开 → §3.3 多维压力测试 → §3.4 收敛 AC。第 0 步：没接 butler 也能脑暴，接了则收敛的 AC 顺势接进 P1→P2。不进执行主线、不冻结。
- **旧触发名 `/butler-upgrade` 全仓迁成 `/butler:upgrade`**：`/butler-upgrade` 此前从来只是规则正文里的散文暗号、无对应命令文件；R2 首次为它落真命令文件，并把活文档里的旧名统一迁新（保留「升级 butler / 同步新版」自然语言触发）。
- **文档更新**：`capabilities.md` 命令表把 `/ideation`·`/milestone`·`/butler-upgrade` 三行**转换**为 `/butler:*` 一等入口（真源列改指命令文件），并**删掉** R1 遗留的 `/review` 旧行（并入既有 `/butler:review`，消并列冗余）；`README.md` 的 `butler/` 子树补三命令。
- **迁移配方 + 切版**：`migrations/v2.8.0.md`（部署面 `[no-op]`+`[restamp]`；点明新命令由 R1 目录软链自动托管、**无需**重跑 setup.sh）；VERSION 2.7.0→2.8.0、CHANGELOG 顶条 `[2.8.0]`（判 MINOR）。

## 关键变更 / 用户可感知变化

- **多了三个命令**：`/butler:milestone`（开里程碑 / 看板）、`/butler:upgrade`（升级已部署项目）、`/butler:ideation`（需求脑暴）。
- **`/butler-upgrade` 改敲 `/butler:upgrade`**：路由行为一字未改，只是换了命名空间触发名（与 R1 `/butler-prd`→`/butler:prd` 同类）。
- **无需任何安装动作就能用**：R1 已把整个 `.claude/commands/butler/` 目录软链进全局，这三个新命令**自动**在所有项目可用——这正是 R1 选「整目录软链」而非「逐文件软链」的兑现点。**唯一例外**：若你从没跑过 R1 的 setup.sh，补跑一次即到位。
- **对已部署项目**：`.ai/` 结构零变化（命令是个人工具、不下发、不进 `templates/`）。

## 高层影响范围

- 新增（命令层）：`.claude/commands/butler/milestone.md` + `upgrade.md` + `ideation.md`。
- 改（活文档·触发名）：`Coder/20_Workflow_Lifecycle/butler-upgrade.md`（§2 触发词）、`Coder/00_System_Prompt/logic-protocol.md`、`Coder/20_Workflow_Lifecycle/migration-schema.md`、`HUMAN_GUIDE.md`、`.ai/project/architecture.md`、`.ai/project/debt.md`。
- 改（活文档·命令表/目录树）：`.ai/project/capabilities.md`（三行转换 + 删 `/review` 冗余）、`README.md`（子树补三命令）。
- 发布层（独立 chore(release) 提交）：`VERSION` 2.7.0→2.8.0、`CHANGELOG.md` 顶条、`migrations/v2.8.0.md`。
- 没碰（守最小影响面 / AC9 边界守恒）：任何 `Coder/**` 规则**算法**与状态机、`templates/**`、四件套 schema、`templates/hooks/**`、**`setup.sh`（R1 目录软链已托管，本迭代一行未动）**——`git diff --stat` 核清。

## 验证方式与结果摘要

- **9 项验收（AC1–AC9）全过**，`auto·可靠`为主 + 结构核/人读：
  - **隔离假 HOME 实跑 `setup.sh` ×2（首装 + 幂等）5/5 命令经目录软链可达**：三新命令 + R1 的 prd/review 全部 `test -e` 通过、`~/.claude/commands/butler` 目录软链指向仓库命名空间目录、无 `butler/butler` 套娃、**`setup.sh` 未改一行**——坐实 R1 目录软链红利（AC1/AC6）。
  - 三命令薄壳四要点齐（薄壳声明 + DRY / 跨 cwd 路径约定段 / 第 0 步降级 / frontmatter 说人话），委托的真源 section 锚点回真源**逐一真实存在**、零捏造（AC2/AC3/AC4/AC5）。
  - `/butler-upgrade` 全仓残留普查**零裸旧名**（新名带旧名注 / 文件名引用 / 本迭代规划稿讨论迁移本身 / 历史归档 均合法）（AC3）；capabilities 三行已转换 + `/review` 行已删、README 子树五命令齐（AC7）；VERSION/CHANGELOG/migration 三载体一致（AC8）；`git diff --stat` 无越界（AC9）。
- **标准模式复核**：低风险纯机械（薄壳复制 R1 已验范式 + 触发名字符串迁移 + 文档 + 幂等切版），P5 自评 + 客观隔离 HOME 实跑无 shaky 处，未升格强制独立复核（区别于 R1 危险模式）。

## 已知剩余风险 / 延后事项

- **计划-实际差异 1 处（已记 VERIFY_REPORT）**：TECH_PLAN DD3 字面「`butler-upgrade.md` 只改 §2 一行」，实际按 AC3「全仓无残留」迁了 6 处命令名——6 处全是触发名、非算法，DD3 原则不破，差异为计划低估了触发名在活文档的分布面。
- **命令菜单「可见性」headless 不可实敲**：沿用 R1 代理验法（文件存在 + 命名空间结构正确 + 经目录软链可达）。真正菜单可见需在**主检出**跑过 R1 的 setup.sh。
- **`/butler:upgrade` 升级协议仍从未真跑**：本迭代只给它换触发名 + 落命令文件，历史欠债（见 `debt.md`）未消。
- **MILE-0005 仍进行中**：R3（`preference` 多子命令）、R4（`loop`/`dangerous` 加风险闸）待后续迭代，设计未锁、不擅自连跑。

## 引用（只引用路径，不嵌全文）

- 归档四件套 + 变更流：`.ai/iterations/ITER-0048/CONCEPT.md` / `AC_LIST.md` / `TECH_PLAN.md` / `VERIFY_REPORT.md` / `CHANGELOG.md`
- 命令（新）：`.claude/commands/butler/milestone.md` / `upgrade.md` / `ideation.md`
- 触发名迁移：`Coder/20_Workflow_Lifecycle/butler-upgrade.md`（§2）、`Coder/00_System_Prompt/logic-protocol.md`、`Coder/20_Workflow_Lifecycle/migration-schema.md`、`HUMAN_GUIDE.md`、`.ai/project/architecture.md` / `debt.md`
- 文档：`.ai/project/capabilities.md`（命令表）、`README.md`（`butler/` 子树）
- 发布元数据：`VERSION`、`CHANGELOG.md`（`## [2.8.0]`）、`migrations/v2.8.0.md`
- 里程碑：`.ai/MILESTONE.md`（MILE-0005 §5.3 路线图 R2）
