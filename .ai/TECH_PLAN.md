# TECH_PLAN — ITER-0048（MILE-0005 R2 批量补低风险命名空间命令）

> 标准模式，P2 AC_LIST 经用户 ACK（三默认全收：MINOR / `/butler-upgrade` 触发名迁 / capabilities 转换）。无危险横幅。

# Goal

套 R1 `prd.md`/`review.md` 薄壳范本，批量落 3 个纯薄壳命令，各委托既有真源、带优雅降级、不复述算法。验证范式可批量复制 + R1 目录软链自动托管新命令（不动 `setup.sh`）。

# Files

- 新增：`.claude/commands/butler/milestone.md`、`.claude/commands/butler/upgrade.md`、`.claude/commands/butler/ideation.md`
- 改：`Coder/20_Workflow_Lifecycle/butler-upgrade.md`（仅 §2 触发词 `/butler-upgrade`→`/butler:upgrade`）、`.ai/project/capabilities.md`（命令表转换）、`README.md`（目录树补 3 命令）
- 发布层：`VERSION`、`CHANGELOG.md`、`migrations/vX.Y.Z.md`
- 不碰：`setup.sh`、`templates/**`、schema、hook、任何规则算法、`prd.md`/`review.md`

# Interface（三命令的路由设计）

- **`/butler:milestone`** — frontmatter：`description` 里程碑录入/看板说人话、`argument-hint "[status=只读看板 | 贴 brief 或留空=录入/开里程碑]"`。第 0 步优雅降级（没接 butler）。分支：留空/给 brief → 委托 `milestone-schema.md §6.4`（录入 brief，含「brief 是大 PRD」并进 `prd-split` 分支）+ §6.1 启动信号 + §7.1 开启；`status` → 委托 `milestone-schema.md §6.5`（`/milestone status` 只读看板：读 MILESTONES+MILESTONE 报路线项进度，不写文件）。收口/废弃/演进走语义、不命令化（§6.5 已定）。
- **`/butler:upgrade`** — frontmatter：`description` 已部署项目升级说人话、`argument-hint "[留空=把当前项目升级到最新 butler 版]"`。第 0 步优雅降级（当前项目没接 butler / 无 `CLAUDE.md` butler 区）。委托 `butler-upgrade.md`：按 §3 侦察（读保护区标记 + 版本 gap）→ §4 首次升级（老项目）/ §5 常规升级（有戳走 `migrations/` 区间配方队列）→ §7 验证回退。升级对象＝**当前项目**。
- **`/butler:ideation`** — frontmatter：`description` 需求脑暴说人话、`argument-hint "[贴模糊需求或留空=进入脑暴]"`。第 0 步：脑暴是需求打磨、不强依赖 `.ai/`，但若在已接 butler 项目里可衔接 P1；委托 `ideation-engine.md §3`（意图探测→展开→压力测试→AC 收敛）。无子参数。

# State

无运行时状态。命令是静态 Markdown 薄壳；`$ARGUMENTS` 由 Claude Code 注入。新命令随 R1 `~/.claude/commands/butler` 目录软链自动全局可达。

# Design Decisions

- **DD1（严格套范本）**：三命令逐段对齐 `prd.md`/`review.md` 骨架——frontmatter 两行说人话 → 薄壳三件事声明 + DRY 红线 → 跨 cwd 路径约定段 → 第 0 步优雅降级 → `$ARGUMENTS` 路由 → 一句话收尾。→ AC5
- **DD2（真源锚点真实）**：每处委托带具体 section 号（milestone §6.4/§6.5、butler-upgrade §3/§4/§5/§7、ideation §3），写前 grep 核对真源确有该节。→ AC2/3/4/5
- **DD3（触发名迁移最小面）**：`butler-upgrade.md` 只改 §2 一行触发词 `/butler-upgrade`→`/butler:upgrade`，保留「升级 butler / 同步新版」自然语言触发；§8 line 159「butler 仓库自身的升级」不含命令名、不动。→ AC3/AC9
- **DD4（capabilities 转换非并列）**：`/ideation`·`/milestone`·`/butler-upgrade` 三行改成 `/butler:*` 一等入口 + 路径 `.claude/commands/butler/<name>.md`；顺清 R1 遗留 `/review`↔`/butler:review` 冗余（合并为一行 `/butler:review`）。→ AC7
- **DD5（不动 setup.sh）**：R1 目录软链托管全套，仅靠 AC6 隔离 HOME 实跑证明新命令自动可达。→ AC6
- **DD6（MINOR + 迁移配方）**：纯新增命令、无破坏面 → MINOR；配方部署面 `[no-op]`+`[restamp]` + `[global-install]`（重跑 setup 拿新命令，含触发名迁移属本机命令层）。→ AC8

# Execution Steps

- [ ] T1 写 `butler/milestone.md`（两分支：录入 / status 看板）→ AC1/AC2
- [ ] T2 写 `butler/upgrade.md`（侦察→执行→验证回退）→ AC1/AC3
- [ ] T3 写 `butler/ideation.md`（脑暴流程）→ AC1/AC4
- [ ] T4 改 `butler-upgrade.md §2` 触发词 `/butler-upgrade`→`/butler:upgrade` + grep 全仓无残留裸旧名（历史归档除外）→ AC3/AC9
- [ ] T5 capabilities 命令表转换（3 行 → `/butler:*` + 顺清 `/review` 冗余）+ README 目录树补 3 命令 → AC7
- [ ] T6 写 `migrations/vX.Y.Z.md`（`[no-op]`+`[restamp]`+`[global-install]`）→ AC8
- [ ] T7 切版三载体（VERSION bump + CHANGELOG 顶条 MINOR）→ AC8
- [ ] T8 隔离 HOME 实跑 setup.sh，验证 3 新命令经目录软链可达 + 范式一致性人读核 + `git diff --stat` 边界守恒 → AC5/AC6/AC9

# Verification

- 结构核：读三命令核薄壳四要点齐 + 真源 section 锚点回真源逐一核（无捏造）。
- 隔离 HOME 实跑 `setup.sh` → `test -e ~/.claude/commands/butler/{milestone,upgrade,ideation}.md`。
- grep `/butler-upgrade` 活文档无残留（历史归档除外）。
- `git diff --stat` 边界守恒。
- P5 标准复核（自评 + objective 实跑）；低风险机械迭代，独立复核非强制（如发现存疑再升格）。

# Risks

- 命令菜单可见性 headless 不可实敲——沿用 R1 代理验法。
- `/butler:upgrade` 触发名迁移是唯一 Coder 触碰点——限 §2 一行、grep 兜底无遗漏。
