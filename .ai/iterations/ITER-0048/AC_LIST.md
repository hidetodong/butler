---
状态: ack-frozen
ACK 日期: 2026-07-14
---

# Goal

MILE-0005 R2：套 R1 薄壳路由器范本，批量落 3 个低风险纯薄壳命令 `/butler:milestone`（+`status`）、`/butler:upgrade`、`/butler:ideation`，各委托既有真源、不复述算法、带优雅降级；验证「范式可批量复制 + R1 目录软链自动托管新命令」。

# In Scope

- 新建 3 个薄壳命令文件：`.claude/commands/butler/milestone.md`、`upgrade.md`、`ideation.md`，结构与 `prd.md`/`review.md` 同构。
- `/butler:milestone` 吃 `status` 参数（留空/给 brief=录入 · `status`=只读看板），委托 `milestone-schema.md`。
- `/butler:upgrade` 委托 `butler-upgrade.md`；**一并把真源 §2 触发词 `/butler-upgrade`→`/butler:upgrade`**（默认 Q2，触发名更新非算法，与 R1 `/butler-prd` 迁移一致）+ 更新 capabilities 对应行。
- `/butler:ideation` 委托 `ideation-engine.md`。
- capabilities 命令表：把 `/ideation`·`/milestone`·`/butler-upgrade` 三行**转换**为 `/butler:*` 一等入口（散文触发降为语义 fallback 注明）+ 顺清 R1 遗留的 `/review`↔`/butler:review` 并列冗余（默认 Q3）；README 目录树补 3 个命令。
- 切一版（默认判 MINOR，见 AC8）。

# Out of Scope

- **不动 `setup.sh`**：R1 目录软链已托管全套，新命令自动全局可用。
- **不改真源规则算法**：三命令委托的 `Coder/**` 规则正文语义一律不动（`/butler:upgrade` 仅改 §2 触发**名**，非算法）。
- **不补 R3/R4**：`preference`（子命令最多）、`loop`/`dangerous`（加风险闸）留后续迭代。
- **不下发目标项目**：命令不进 `templates/`、部署面零影响。
- **不新造命令能力**：只迁既有散文触发词、不发明新命令、不扩语义。

# Acceptance Checklist

- [ ] **AC1（三命令成立·可达）**：`.claude/commands/butler/` 下 `milestone.md`+`upgrade.md`+`ideation.md` 三文件建立；命名空间映射 `butler/<name>.md`→`/butler:<name>` 结构正确。
- [ ] **AC2（`/butler:milestone` 薄壳）**：委托 `milestone-schema.md` 真源；`$ARGUMENTS` 分派——留空/给 brief → 里程碑录入（含「brief 是大 PRD」并进 `prd-split` 的分支指向）、`status` → 只读看板；第 0 步「没接 butler / 无 `.ai/`」优雅降级不报错；薄壳只路由不复述算法；frontmatter 两行说人话；跨 cwd 路径约定段在。
- [ ] **AC3（`/butler:upgrade` 薄壳 + 触发名迁移）**：委托 `butler-upgrade.md` 真源；升级对象是**当前项目**、第 0 步优雅降级；薄壳不复述区间配方算法；**`butler-upgrade.md §2` 触发词 `/butler-upgrade`→`/butler:upgrade`**（保留「升级 butler / 同步新版」自然语言触发），全仓无残留裸 `/butler-upgrade`（历史归档冻结快照除外）。
- [ ] **AC4（`/butler:ideation` 薄壳）**：委托 `ideation-engine.md` 真源；第 0 步降级；薄壳不复述脑暴流程；frontmatter 两行说人话；跨 cwd 路径约定段在。
- [ ] **AC5（范式一致性）**：三命令与 `prd.md`/`review.md` 同构——① 薄壳三件事声明 + DRY 不复述红线；② 跨 cwd 路径约定段；③ 第 0 步优雅降级；④ frontmatter 说人话无术语；⑤ `$ARGUMENTS` 路由（milestone 有 status 分支，另两个可无参数但结构一致）；⑥ 委托的真源 section 锚点真实存在（读真源核对，无捏造路径）。
- [ ] **AC6（目录软链自动托管·实跑）**：隔离 HOME 实跑 `setup.sh`，确认 3 个新命令经 `~/.claude/commands/butler` 目录软链全部可达（`test -e`）、无需改 `setup.sh`——验证 R1 目录软链红利。
- [ ] **AC7（文档更新）**：`.ai/project/capabilities.md` 命令表按「转换为 `/butler:*` 一等入口 + 顺清 `/review` 冗余」更新；`README.md` 目录树 `butler/` 子树补 milestone/upgrade/ideation 三命令。
- [ ] **AC8（切版三载体对齐）**：判 **MINOR**（纯新增 3 命令、无破坏面）；`VERSION` bump、`CHANGELOG.md` 顶条、git tag 三者一致；`migrations/vX.Y.Z.md` 为目标项目部署面 `[no-op]`+`[restamp]` + `[global-install]` 机器动作（重跑 setup 拿新命令）。
- [ ] **AC9（边界守恒）**：除 `butler-upgrade.md §2` 触发名一行外，任何 `Coder/**` 规则算法、`templates/**`、四件套 schema、hook、`setup.sh` 一行未动；`git diff` 佐证改动仅落 `.claude/commands/butler/**`、`butler-upgrade.md`(§2 触发名)、`capabilities.md`/`README.md`、发布层。

# Verification Method

- **AC1**：`test -f` 三命令文件 + 命名空间结构核（auto·可靠）。
- **AC2/AC3/AC4**：读命令文件核薄壳四要点齐 + 委托真源 section 锚点逐一回真源核（auto 结构核 + 人读）。
- **AC3 触发名**：`grep -rn '/butler-upgrade' Coder README.md .ai/project`（历史归档除外）应仅剩合法处或零（auto·可靠）。
- **AC5**：三命令与 `prd.md`/`review.md` 结构逐要点对照（人读同构核）。
- **AC6**：隔离 HOME `bash scripts/setup.sh` → `test -e ~/.claude/commands/butler/{milestone,upgrade,ideation}.md`（auto·可靠）。
- **AC7**：读 capabilities/README 核更新到位、说人话（auto + 人读）。
- **AC8**：`cat VERSION` == tag == CHANGELOG 顶条（auto·可靠）。
- **AC9**：`git diff --stat` 确认无越界（auto·可靠）。

# Open Questions / Risks（呈 ACK 时请一并确认三默认）

1. **切版号**：默认 **MINOR**（纯新增命令能力，与 R1 同类）。
2. **`/butler-upgrade` 触发名一并迁 `/butler:upgrade`**（AC3）：默认**迁**（改 `butler-upgrade.md §2` 触发词 + capabilities，触发名非算法、与 R1 一致；保留自然语言触发）。若你想保守「只加命令、不碰任何 Coder 真源」，可否掉此项、`/butler-upgrade` 散文名与 `/butler:upgrade` 命令并存。
3. **capabilities 整理方式**（AC7）：默认**转换**旧行为 `/butler:*` 一等入口 + 顺清 R1 遗留 `/review` 冗余。若想最小改动，可只加 3 新行、不动旧行（但表会更冗余）。
- **风险**：命令菜单「可见性」headless 不可实敲，沿用 R1 代理验法（文件/软链存在 + 结构正确 + 经软链可达）。
