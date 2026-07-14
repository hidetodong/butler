> ⚠️ 危险模式：本产物由模型自主 ACK（已过 §5.2 P3 自审门），未经用户确认（ITER-0047，2026-07-14）

# Goal
支撑 AC1–AC8：搭 `.claude/commands/butler/` 命名空间地基、`/butler-prd`→`/butler:prd` 破坏性迁移、`setup.sh` 改目录软链、落 `/butler:review` 薄壳范本、出 `[rename]` 迁移配方、切版 MINOR、边界守恒。

# Files / Modules to Change
- `.claude/commands/butler/`（新目录）— 命名空间根 → AC1
- `.claude/commands/butler/prd.md`（`git mv` 自 `butler-prd.md`）— 保留 git 血缘；正文经 grep 确认不自称 `butler-prd`，仅核示例引用 → AC1/AC3
- `.claude/commands/butler-prd.md`（`git mv` 移走即删）→ AC2
- `.claude/commands/butler/review.md`（新建薄壳路由器）→ AC5
- `scripts/setup.sh`（软链段 81–101：逐文件软链 → 目录软链；加旧 `butler-prd.md` 软链清理；echo/注释里 `/butler-prd`→`/butler:prd`）→ AC4/AC2
- `migrations/v2.7.0.md`（新建迁移配方）→ AC6
- `VERSION`（2.6.1→2.7.0）、`CHANGELOG.md`（顶条 `[2.7.0]`）、git tag `v2.7.0`（本地）→ AC7
- 活文档引用更新 `/butler-prd`→`/butler:prd`：`README.md`、`HUMAN_GUIDE.md`、`.ai/project/capabilities.md`、`.ai/project/frontier.md` → AC2

# Interface / Contract
- **命名空间映射**：`.claude/commands/butler/<name>.md` → `/butler:<name>`（Claude Code 子目录＝冒号命名空间，已 claude-code-guide 查证）。
- **setup.sh 软链契约**：`~/.claude/commands/butler` --symlink--> `$BUTLER_DIR/.claude/commands/butler`；幂等 `ln -sfn`（`-n` 防止对已存在目录软链嵌套建链 `butler/butler`）。旧扁平软链 `~/.claude/commands/butler-prd.md` 用 `[ -L ]` 判定后 `rm`（只删软链、不误删真文件）。
- **prd 薄壳**：三分支路由（留空|贴 PRD → 首切 / `update` → 改版 / `status` → 只读看板）语义**一字不改**，仅命令自称/示例 `/butler-prd`→`/butler:prd`。
- **review 薄壳**：`$ARGUMENTS` 空 → 默认同上下文简要自评；`independent` → 独立复核（fresh-context 子 agent）；委托 `60_Extension_CodeReview/review-engine.md`（+ `62_Extension_Agents/independent-review.md`）真源、不复述算法。

# State / Boundary
- 只碰：命令层（`.claude/commands/**`）、`scripts/setup.sh`、发布层（VERSION/CHANGELOG/migrations/tag）、四处活文档引用。
- **不碰**：`Coder/**` 任何规则算法、`templates/**`、四件套 schema、hook 体系、核心 P1–P5 状态机。
- **引用更新边界**：活文档改；历史归档（`.ai/iterations/**`、`deliveries/**`、既有 `migrations/v2.4.0|v2.5.0.md`、`CHANGELOG.md` 既有版本条目）与当前迭代工作区的**迁移叙述**（`.ai/*.md` 里"把 /butler-prd 迁成 /butler:prd"这类语境正确的提及）一律不动。

# Design Decisions
- **DD1（命名空间＝子目录，不迁 skills）**：维持 commands 路线——command `.md` 软链已 ITER-0045 实跑验证可用；`butler/` 子目录自动成 `/butler:` 前缀。→ AC1
- **DD2（prd 用 git mv）**：保留 git 血缘；grep 已证正文不自称 `butler-prd`，故迁移后功能等价、改动近乎零，风险最低。→ AC3
- **DD3（setup.sh 目录软链 + 旧软链清理）**：一条 `ln -sfn` 软链整个 `butler/` 目录，比逐文件更省、butler 仓加命令自动全局生效；`-n` 保幂等不嵌套；加旧软链清理让**所有机器重跑 setup 即自动清残留**（不靠人手删）。→ AC4/AC2
- **DD4（review 薄壳同构 prd）**：四要点范式（第 0 步读契约 + 没接 butler 降级 / `$ARGUMENTS` 分派 / 委托真源不复述 / 两行说人话 frontmatter），作 R2–R4 复制范本。→ AC5
- **DD5（切版 MINOR v2.7.0）**：命名空间是新增能力（当前 VERSION 2.6.1 → 下一 MINOR 2.7.0）；`/butler-prd`→`/butler:prd` 的破坏面局限「个人命令层」，由迁移配方 `[rename]` 承接、目标项目部署面 `[no-op]`。→ AC7
- **DD6（边界守恒 git diff 佐证）**：收口前 `git diff --stat` 确认改动仅落在上述文件集。→ AC8

# Execution Steps
- [ ] T1 建 `.claude/commands/butler/` + `git mv butler-prd.md butler/prd.md` → AC1
- [ ] T2 核 `butler/prd.md`：grep 确认无 `/butler-prd` 自称残留、示例引用若有则改 `/butler:prd`，三分支路由语义不动 → AC3
- [ ] T3 [P] 读 `review-engine.md` + `independent-review.md` 真源，写 `butler/review.md` 薄壳（四要点 + `$ARGUMENTS` 分派 default/independent + 降级）→ AC5
- [ ] T4 改 `scripts/setup.sh`：软链段改目录软链 + 旧 `butler-prd.md` 软链清理 + echo/注释更新 → AC4/AC2
- [ ] T5 更新活文档引用 `/butler-prd`→`/butler:prd`（README / HUMAN_GUIDE / capabilities / frontier）→ AC2
- [ ] T6 写 `migrations/v2.7.0.md`（`[rename]` 个人命令层 + `[no-op]`+`[restamp]` 部署面 + 本机一次性动作）→ AC6
- [ ] T7 切版：`VERSION` 2.7.0 + `CHANGELOG.md` 顶条 `[2.7.0]` → AC7
- [ ] T8 实跑验证（隔离 HOME 跑 `setup.sh` 两次核幂等 + `readlink` 软链指向 + `test -e` 经软链可达 + grep 无残留 + `git diff --stat` 边界）→ AC1/AC2/AC4/AC8

# Verification Plan
- **AC1**：`test -d .claude/commands/butler && test -f .claude/commands/butler/prd.md`；命名空间结构核对（auto·可靠）。
- **AC2**：`test ! -e .claude/commands/butler-prd.md`；隔离 HOME 跑 setup 后 `test ! -e ~/.claude/commands/butler-prd.md`；`grep -rn '/butler-prd' README.md HUMAN_GUIDE.md .ai/project` 零命中（auto·可靠）。
- **AC3**：`git show HEAD:.claude/commands/butler-prd.md` 与新 `butler/prd.md` diff——除命令名/示例外三分支路由锚点逐一等价（auto diff + 人读）。
- **AC4**：隔离 HOME `bash scripts/setup.sh` ×2 → `readlink ~/.claude/commands/butler` 指向仓库 `butler/`、无 `butler/butler` 嵌套、无报错；`test -e ~/.claude/commands/butler/prd.md && test -e ~/.claude/commands/butler/review.md`（auto·可靠）。
- **AC5**：读 `butler/review.md` 核四要点齐 + 与 `prd.md` 同构；`$ARGUMENTS` 分派 default/independent 明确（auto 结构核 + 人读）。
- **AC6**：读 `migrations/v2.7.0.md` 核 `[rename]`+`[no-op]`+`[restamp]`+本机动作齐（auto·可靠）。
- **AC7**：`cat VERSION` == tag == `CHANGELOG.md` 顶条，三者一致（auto·可靠）。
- **AC8**：`git diff --stat` / `git status` 确认无 `Coder/**`、`templates/**`、hook 改动（auto·可靠）。
- **P5**：升格独立复核（fresh-context 子 agent，验证者≠实现者），逐 AC 裁决 + 边界守恒对抗探测。

# Risks / Open Questions
- **setup.sh 幂等嵌套陷阱**：`ln -sfn` 对已存在目录软链须带 `-n`（现有代码已用，沿用）；隔离 HOME 复跑两次显式验证无 `butler/butler`。
- **命令可见性无法 headless 实敲**：用「软链存在 + 命名空间结构正确」作可靠代理（机制已查证），同 ITER-0044 验法。
- **prd.md 内部引用遗漏**：T2 grep 兜底（已初判正文无自称，低风险）。
- 三 P1 Open Question 已在 P2/P3 定死（MINOR / review 吃参数 / 引用只改活文档），无遗留未决。
