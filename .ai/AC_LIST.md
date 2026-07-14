---
状态: ack-frozen
ACK 日期: 2026-07-14
---

# Goal
搭起 `/butler:xxx` 命名空间命令系统的地基：建命名空间目录、把 `/butler-prd` 干净迁成 `/butler:prd`、改 `setup.sh` 让整个命名空间目录随一条软链全局可用、落第一个新命令 `/butler:review` 证明「薄壳路由器」范式可复制。为 R2–R4 批量加命令铺好骨架与迁移范本。

# In Scope
- 新建 `.claude/commands/butler/` 命名空间子目录（Claude Code 里子目录＝命名空间，`butler/<name>.md`→`/butler:<name>`）。
- `/butler-prd`（v2.4.0 发布、连字符）**破坏性迁**为 `/butler:prd`：文件移到 `butler/prd.md`、清旧全局软链、更新活规则/文档引用、出 `[rename]` 迁移配方。
- 改 `scripts/setup.sh` 软链逻辑：从「逐个软链 `.claude/commands/*.md`」改为「软链整个 `butler/` 目录到 `~/.claude/commands/butler`」。
- 落 `/butler:review`（纯薄壳路由器），委托 `60_Extension_CodeReview` / `62_Extension_Agents` 真源。
- 切一版（判 MINOR，见 AC7）。

# Out of Scope
- **不补 R2–R4 的其余命令**（milestone / upgrade / ideation / preference / loop / dangerous 留后续迭代）。
- **不下发目标项目**：命令不进 `templates/`、目标项目部署面零影响（沿用 ITER-0044 边界）。
- **不改真源规则算法**：`Coder/**` 规则正文语义一律不动。
- **不做团队协作者共享**（project 级拷贝那条路另议）。
- **不新造命令能力**：只迁移 + 落一个已有语义的 `review` 命令。

# Acceptance Checklist
- [ ] **AC1（命名空间成立）**：`.claude/commands/butler/` 目录建立，`butler/prd.md` 存在；命名空间语法 `butler/<name>.md`→`/butler:<name>` 结构正确（子目录名即冒号前缀）。
- [ ] **AC2（旧命令干净移除）**：`.claude/commands/butler-prd.md` 已删；旧全局软链 `~/.claude/commands/butler-prd.md` 清除；**活规则 + 面向人文档**（`Coder/**`、`README.md`、`HUMAN_GUIDE.md`、`.ai/project/**` 等）里无残留 `/butler-prd` 引用——**历史归档冻结快照不改**（`deliveries/**`、`.ai/iterations/**`、`CHANGELOG.md` 既有版本条目、`migrations/` 既有配方）。
- [ ] **AC3（prd 功能等价）**：`butler/prd.md` 与原 `butler-prd.md` **功能等价**——薄壳三分支路由（留空/贴 PRD → 首切、`update` → 改版、`status` → 只读看板）语义一字不改；仅命令自称与示例里的命令名从 `/butler-prd` 更新为 `/butler:prd`、`argument-hint`/`description` 保持说人话。
- [ ] **AC4（setup.sh 目录软链）**：`setup.sh` 改为软链整个 `butler/` 目录（`~/.claude/commands/butler` → 仓库 `.claude/commands/butler/`）；**幂等**（重复跑不炸、`ln -sfn` 或等价）；**不接管** `~/.claude/commands/` 根下用户自放的其它命令；实跑一次确认软链指向正确、`/butler:prd` 与 `/butler:review` 两文件经软链在全局可达。
- [ ] **AC5（review 薄壳范本）**：`butler/review.md` ＝纯薄壳路由器——① 委托 `review-engine.md`（+ `independent-review.md`）真源并声明「算法以真源为准、不复述」（守 DRY）；② 含「当前项目没接 butler / 无迭代产物」时的优雅降级提示（不报错）；③ `frontmatter` 两行说人话（`description` + `argument-hint`）、无内部术语；④ 按 `$ARGUMENTS` 区分默认同上下文自评 vs 独立复核（opt-in）。结构与 `prd.md` 同构，可作 R2–R4 复制范本。
- [ ] **AC6（迁移配方）**：`migrations/vX.Y.Z.md` 产出——个人命令层 `[rename]`（`/butler-prd`→`/butler:prd`，含清旧软链 + 重跑 setup.sh 的本机一次性动作）+ 目标项目部署面 `[no-op]`+`[restamp]`（命令不下发、零结构影响）。
- [ ] **AC7（切版三载体对齐）**：判 **MINOR**（命名空间是新增能力；`/butler-prd`→`/butler:prd` 的破坏面局限在「个人命令层」，由迁移配方 `[rename]` 承接，对目标项目部署面是 no-op）。`VERSION` bump、`CHANGELOG.md` 顶条、git tag 三者一致。
- [ ] **AC8（边界守恒）**：`Coder/**` 任何规则算法、`templates/**`、四件套 schema、hook 体系一行未动——`git diff` 佐证改动仅落在 `.claude/commands/butler/**`、`scripts/setup.sh`、`migrations/**`、发布层与 `/butler-prd` 引用更新处。

# Verification Method
- **AC1**：`test -d .claude/commands/butler` + `test -f .claude/commands/butler/prd.md`；核对目录结构符合命名空间映射规则（auto·可靠）。
- **AC2**：`test ! -e .claude/commands/butler-prd.md`；`test ! -e ~/.claude/commands/butler-prd.md`；`grep -rn '/butler-prd' Coder README.md HUMAN_GUIDE.md .ai/project` 零命中（历史归档目录排除）（auto·可靠）。
- **AC3**：diff 对照原 `butler-prd.md`（从 git 历史取）与新 `butler/prd.md`——除命令名/路径引用外语义无变化；三分支路由锚点逐一核对（auto·可靠 + 人读校）。
- **AC4**：隔离 HOME 实跑 `bash scripts/setup.sh` → `readlink ~/.claude/commands/butler` 指向仓库 `butler/` 目录；重复跑一次确认幂等、无报错；`test -e ~/.claude/commands/butler/prd.md && test -e ~/.claude/commands/butler/review.md`（auto·可靠）。
- **AC5**：读 `butler/review.md` 核四要点齐（委托真源 + 不复述声明 / 降级提示 / 两行说人话 frontmatter / `$ARGUMENTS` 分派）；结构与 `prd.md` 同构性人读比对（auto 结构核 + 人读）。
- **AC6**：读 `migrations/vX.Y.Z.md` 核 `[rename]` + `[no-op]`+`[restamp]` + 本机动作齐备（auto·可靠）。
- **AC7**：`cat VERSION` == tag == `CHANGELOG.md` 顶条版本号，三者一致（auto·可靠）。
- **AC8**：`git diff --stat` / `git status` 确认无 `Coder/**`、`templates/**`、`hook` 改动（auto·可靠）。

# Open Questions / Risks
- **命令菜单「可见性」无法在 headless 环境实敲验证**：用「文件/软链存在 + 命名空间结构正确」作可靠代理（命名空间机制已经 claude-code-guide 查证），同 ITER-0044 对 `/butler-prd` 的验法。
- **三个 P1 Open Question 在本清单已定默认**（呈交 ACK 时请一并确认）：① 切版判 **MINOR**（AC7）；② `/butler:review` **吃参数**区分默认自评 / 独立复核（AC5）；③ 引用更新只动**活规则 + 面向人文档、历史归档快照不改**（AC2）。
- **破坏性改名残留风险**：旧逐文件软链留下的 `~/.claude/commands/butler-prd.md` 必须显式清理，否则新旧命令并存——AC2/AC4 已覆盖。
