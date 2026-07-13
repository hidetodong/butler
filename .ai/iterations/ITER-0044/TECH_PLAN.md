# TECH_PLAN — ITER-0044（/butler-prd 一等命令入口纳管）

# Goal
- 支撑 AC1–AC6：把既成的 `.claude/commands/butler-prd.md` 追认纳管、逐 AC 对真实文件与 git 状态核验，再走收口 + 独立切 MINOR v2.4.0。

# Files / Modules to Change
- **纳管（迭代内容）**：`.claude/commands/butler-prd.md` — 已存在、内容已定型（前序会话说人话化过），本迭代不改其内容，只 `git add` 纳管。支撑 AC1–AC3。
- **折叠（收口 step 4）**：`.ai/project/capabilities.md`（命令表加 `/butler-prd` 真实文件行）+ `.ai/project/frontier.md`（版本态刷新 v2.4.0）+ `.ai/project/debt.md`（记「命令未下发目标项目」为待定）。支撑 AC5、AC6。
- **发布层（独立 chore(release) 提交）**：`VERSION`（2.3.0→2.4.0）、`CHANGELOG.md`（顶条 v2.4.0）、`migrations/v2.4.0.md`（`[no-op]`+`[restamp]`）。支撑 AC6。
- **不改**：任何 `Coder/**` 规则、`templates/**`、schema、hook、`.gitignore`。

# Interface / Contract
- 命令文件遵循 Claude Code 命令契约：frontmatter `description` + `argument-hint`（菜单可见）、正文为发给 AI 的执行指令（菜单不可见）、`$ARGUMENTS` 承接用户参数。无 butler 侧新契约、无字段/hook/schema 变更。

# State / Boundary
- 迭代内容提交与发布提交**分离**（守 `versioning-schema §5.2/§6.1`）：feat 提交只装 `.claude/commands/butler-prd.md` + `.ai/` 收口产物；release 提交单独装 VERSION/CHANGELOG/migration + 打 tag。
- 命令是 butler 仓内部工具，不进 `templates/`、不下发——边界写进交付与 debt。

# Design Decisions
- **决策 1：本迭代不改命令文件内容，只纳管**。理由：前序会话已把 frontmatter 说人话化、正文薄壳已成型且经本会话 `/butler-prd status` 实跑验证可用；再改即无谓扰动。AC2/AC3 是**验收既有文件达标**，非重写。
- **决策 2：判 MINOR（新增命令能力），不因「不下发」降级为 PATCH**。理由：`versioning-schema §2` MINOR = 新增命令；`/butler-prd` 是 butler 仓新增的一等命令入口（对在 butler 仓工作的使用者是新能力）。但 migration 就**部署面**如实给 `[no-op]`——命令不在 `templates/`、目标项目零变化，版本意义不夸大。两者不矛盾：能力对本仓新增（MINOR），对部署项目无影响（`[no-op]`）。
- **决策 3：命令 butler 自用、不下发（关 Open Question 1）**。理由：先验证一等命令文件形态在 butler 自身跑顺，下发是独立决策（涉及 `templates/` 部署面、升级配方），本轮不扩张；记入 `debt`/`frontier` 待定。
- **决策 4：只追认 `/butler-prd`，不批量落其他命令（关 Open Question 2）**。理由：守最小实现，避免范围膨胀；成体系铺开另开方向。

# Execution Steps
- [ ] T1 开 ITER-0044：`.ai/ITERATIONS.md` 领号、置 active、`current` 指向 → 已随四件套开启
- [ ] T2 验收既有命令文件（不改内容）：读 frontmatter 核说人话（AC2）、读正文核薄壳三要点（AC3）→ 写入 VERIFY
- [ ] T3 影响面核验：`git status` 确认唯一未跟踪是该文件；规划 feat 提交只装它（AC4）
- [ ] T4 收口五步：归档 `iterations/ITER-0044/` → 交付 `.md`+`.html` → 台账 closed/current:none → 折叠 `capabilities`+`frontier`+`debt`（AC5）→ 6 不变量自检（AC6）
- [ ] T5 feat 提交纳管命令 + `.ai/` 收口产物；提交后实测 AC1（`git ls-files` 命中）、AC4（`git show --stat` 仅该文件）回填 VERIFY
- [ ] T6 独立切 v2.4.0：改 VERSION / 加 CHANGELOG / 写 migration → `chore(release)` 提交 + tag `v2.4.0` → 切版后三载体对齐自检（AC6）
- [ ] T7 push main + tag

# Verification Plan
- AC1：提交后 `git ls-files .claude/commands/butler-prd.md` 有输出；frontmatter 两字段齐。
- AC2：frontmatter 两行无「薄壳/首切/真源」；`argument-hint` 三参数各标动作。
- AC3：正文含第 0 步契约读 + 三分支路由 + 「不复述」声明。
- AC4：feat `git show --stat` 仅 `.claude/commands/butler-prd.md`（+`.ai/` 产物）；`Coder/**`/`templates/**`/schema/`.gitignore`/`VERSION` 未在 feat 提交动。
- AC5：交付 + `frontier`/`debt` 有「butler 自用、未下发」边界句。
- AC6：收口 6 不变量过；`git tag --points-at HEAD` 含 `v2.4.0`；`VERSION`==tag==CHANGELOG 顶条；migration 为 `[no-op]`+`[restamp]`。

# Risks / Open Questions
- 两个 Open Question 已在本阶段关闭（决策 3、4）。
- 追认式风险（产物事后补）已由「ACn 对真实文件/真实 git 状态核」缓解（AC_LIST 已记）。
- 残余：`/butler-prd` 只 butler 自用未下发——如实入 `debt`，不当欠债隐藏。
