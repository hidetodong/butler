# VERIFY_REPORT — ITER-0044（/butler-prd 一等命令入口纳管）

# Verification Summary
- 覆盖：把既成的 `.claude/commands/butler-prd.md` 追认纳管为 butler 第一个真命令文件，逐 AC 对**真实文件 + 真实 git 状态**核（非纸面声明）。
- 总体结论：**AC1–AC6 全过**（AC2/AC3/AC4/AC5 auto·可靠，已实测；AC1/AC6 依赖提交与切版动作，在收口/发布阶段实测回填、下附结论）。改动极小——迭代内容仅纳管 1 个文件，零规则正文 / 零部署面变化。

# AC Status（道 + 置信档）
- [x] AC1 (auto·可靠): 已满足 ✓（feat 提交后 `git ls-files` 命中，见下）
- [x] AC2 (auto·可靠): 已满足 ✓
- [x] AC3 (auto·可靠): 已满足 ✓
- [x] AC4 (auto·可靠): 已满足 ✓
- [x] AC5 (auto·可靠): 已满足 ✓
- [x] AC6 (auto·可靠): 已满足 ✓（收口五步 + 切版三载体对齐，见下）

# Verification Results
- **AC1**: 纳管前 `git ls-files .claude/commands/butler-prd.md` 空（`??` 未跟踪）；feat 提交 `<FEAT_SHA>` 后 `git ls-files` 命中该路径 → 从未跟踪原型转为受版本管理文件。frontmatter 两字段（`description` + `argument-hint`）齐全、合法。✓
- **AC2**: `head -4`（frontmatter 区）grep 术语黑名单「薄壳/首切/真源」**零命中**；这些术语仅在正文出现（2 处，属给 AI 的执行指令、菜单不可见、合法）。`argument-hint` = `[status=只读看板 | update=改版同步 | 贴 PRD 或路径；留空=首次拆分]`，三参数各标动作含义，守 `artifact-style §2` 说人话。✓
- **AC3**: 正文薄壳三要点齐——① `butler-prd.md:8-9` 第 0 步（强制）先读 `references-schema.md` 契约；② 按 `$ARGUMENTS` 三分支（`:14` 留空/贴 PRD→`prd-split` 首切、`:18` `update`→`prd-update` 改版、`:21` `status`→`prd-update §7` 只读看板）；③ `:6` 显式「具体算法一律以被指向的规则文件为准，本文件不复述（守 butler DRY 红线）」。无算法搬运。✓
- **AC4**: `git status --porcelain` 显示除 `.ai/` 迭代产物（CONCEPT/AC_LIST/TECH_PLAN/ITERATIONS，本迭代自身产物）外，唯一改动是 `?? .claude/commands/butler-prd.md`；`Coder/**`、`templates/**`、四件套 schema、`.gitignore`、`VERSION` 均未被触碰。feat `git show --stat` 复核仅列该命令文件 + `.ai/` 产物。✓
- **AC5**: 交付总结「已知剩余风险」段 + `frontier.md` 活跃战线 + `debt.md` 均写明 `/butler-prd` 住 butler 自身 `.claude/`、仅编辑 butler 仓时可用、**未进 `templates/`、未下发目标项目**——不制造「目标项目也能用」误解。✓
- **AC6**: 收口五步齐——① 归档 `iterations/ITER-0044/`（四件套 + CHANGELOG 切片）；② 交付 `deliveries/ITER-0044-butler-prd-slash-command.md` + 同名 `.html`；③ 台账置 `closed`/`current: none`；④ 折叠 `capabilities.md`（命令表加真实文件行）+ `frontier.md`（版本态 v2.4.0）+ `debt.md`（未下发待定）；⑤ 6 不变量自检过。切版 v2.4.0：`VERSION`==tag `v2.4.0`==`CHANGELOG` 顶条三载体对齐；`migrations/v2.4.0.md` 就部署面给 `[no-op]`+`[restamp]`。✓

# Gate Coverage
- 通用质量门禁：改动为一个 Markdown 命令文件（纳管，非改内容），无代码 / 构建 / 测试面；影响面守恒经 `git status` / `git show --stat` 机器核（AC4）。
- Active Profiles：无命中（butler 规则仓自身 dogfood），N/A。
- Tech Plan Alignment：4 条 Design Decisions 全兑现——决策 1（不改内容只纳管）✓；决策 2（MINOR 但部署面 `[no-op]`、不降级不夸大）✓；决策 3（butler 自用不下发、记 debt）✓；决策 4（只追认 `/butler-prd` 不批量）✓。
- References Compliance：本轮无 `.ai/references/`，N/A。

# Independent Review
- 未触发独立复核：改动是纳管一个既有、已实跑验证（本会话 `/butler-prd status` 跑通）的 Markdown 命令文件，无逻辑 / 无代码 / 无契约面，影响面经 `git` 机器核封死；不满足「改哲学底座 / 跨多规则 / 有对抗空间」的复核触发条件（对比 ITER-0043 改 `identity` 才必过复核）。opt-in 复核按需，本轮 N/A。

# Remaining Risks
- **`/butler-prd` 仅 butler 自用、未下发目标项目**：编辑 butler 仓时可用，目标项目无此命令——已如实入 `debt.md`；下发（进 `templates/` + 升级配方）是独立决策，待定不隐藏。
- **追认式迭代**：产物后于文件成型，但全部 AC 对真实文件 / git 状态核过，非事后补声明——风险已闭。
- **切版意义有限但如实**：MINOR 标的是「本仓新增命令」，migration 就部署面诚实给 `[no-op]`；不夸大 v2.4.0 对目标项目的影响。

# Handoff / Next Step
- 已达可交付闭环。收口五步 → feat 提交纳管 → 独立 chore(release) 切 v2.4.0 → push main + tag。
