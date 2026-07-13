---
状态: ack-frozen
ACK 日期: 2026-07-13
prd_version: —
---

# Goal
- 把 `.claude/commands/butler-prd.md` 正式纳入版本管理，使 `/butler-prd` 成为 butler 仓一等命令入口；确认其菜单说人话、正文薄壳守 DRY、影响面守恒、butler 自用不下发的边界如实记录。

# In Scope
- 纳管 `.claude/commands/butler-prd.md` 一个文件（迭代内容提交）。
- 独立发布提交切 MINOR v2.4.0（VERSION / CHANGELOG / migration）。

# Out of Scope
- 不改任何 `Coder/**` 规则正文、不动 `templates/`、不改四件套 schema / hook / `.gitignore`。
- 不把命令下发给目标项目（不进 `templates/`）。
- 不把 `/milestone` / `/prd` 等其他散文命令一并落文件（本轮只追认 `/butler-prd`）。

# Acceptance Checklist
- [ ] AC1: `.claude/commands/butler-prd.md` 作为真实文件被纳入版本管理（提交后 `git ls-files` 命中、不再是 `??` 未跟踪），且含合法 Claude Code 命令 frontmatter（`description` + `argument-hint` 两字段齐全）。
- [ ] AC2: 菜单可见字段说人话——`description` / `argument-hint` 中**无**「薄壳 / 首切 / 真源规则」等内部实现术语；每个参数（`status` / `update` / 留空）在 `argument-hint` 里标注了对应动作含义，守 `artifact-style §2` 说人话三条。
- [ ] AC3: 命令正文是薄壳路由器——① 有「第 0 步强制读 `references-schema` 契约」；② 按 `$ARGUMENTS` 三分支路由（留空/贴 PRD→`prd-split` 首切、`update`→`prd-update` 改版、`status`→`prd-update §7` 只读看板）；③ 正文显式声明「算法以被指向规则为准、本文件不复述」，不搬运任何真源算法（守 DRY）。
- [ ] AC4: 影响面守恒——迭代内容提交（feat）**只**含 `.claude/commands/butler-prd.md`；`git diff` 核 `Coder/**`、`templates/**`、四件套 schema、`.gitignore`、`VERSION` 均未被该提交触碰（`VERSION` 变更只出现在独立 release 提交）。
- [ ] AC5: 边界如实记录——交付总结与 `frontier`/`debt` 明确写清 `/butler-prd` 住 butler 自身 `.claude/`、只在编辑 butler 仓时可用、**未下发目标项目**，不制造「目标项目也能用」的误解（no 假绿）。
- [ ] AC6: 收口 + 切版一致性——四件套说人话、ITER-0044 收口五步齐（归档 / 交付 .md+.html / 台账 closed·current:none / 折叠 `capabilities`+`frontier` / 6 不变量自检）；v2.4.0 三处版本载体对齐（`VERSION` == tag `v2.4.0` == `CHANGELOG` 顶条），`migrations/v2.4.0.md` 就部署面如实给 `[no-op]`+`[restamp]`。

# Verification Method
- AC1: `git ls-files .claude/commands/butler-prd.md` 提交后有输出；读文件头核 frontmatter 两字段。
- AC2: 读 frontmatter 两行 + grep 术语黑名单（薄壳/首切/真源）应只在正文出现、不在 frontmatter。
- AC3: 读正文核第 0 步 + 三分支 + 「不复述」声明；确认无算法搬运。
- AC4: `git show --stat`（feat 提交）应仅列 `.claude/commands/butler-prd.md`；`git diff` 核边界文件。
- AC5: 读 `deliveries/ITER-0044-*.md` 与 `frontier.md`/`debt.md` 核边界句存在。
- AC6: 收口后跑 6 不变量自检；切版后 `git tag --points-at HEAD` + 三载体比对。

# Open Questions / Risks
- 追认式迭代（文件先于产物存在）：风险是产物沦为「事后补作业」。缓解——ACn 全部对着真实文件与真实 git 状态核，非纸面声明；AC4/AC1 依赖提交后状态、在收口验证阶段实测回填。
- 「切版是否值得」已在决策阶段与用户确认走规范路径（Option C）；本迭代如实按 MINOR 记，migration 就部署面零影响给 `[no-op]`，不夸大版本意义。
