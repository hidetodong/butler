# TECH_PLAN — ITER-0020

# Goal

- 支撑 AC1-AC11：在 `versioning-schema.md` 就地成文「提交规约」+ 把 §5 切版流程扩到 git 操作层，并同步所有指针与交叉引用。

# Files / Modules to Change

- `Coder/20_Workflow_Lifecycle/versioning-schema.md`（核心）：frontmatter title+scope；新增 §5「提交规约」；原 §5-8 顺移为 §6-9；扩写新 §6 切版流程；修内部 § 交叉引用。
- `Coder/README.md` §139：versioning-schema 一句话描述补"提交规约 + 切版 git 仪式"。
- `CLAUDE.md`：VERSION 行引用描述同步。
- `HUMAN_GUIDE.md`：versioning-schema 注释同步。
- `Coder/20_Workflow_Lifecycle/migration-schema.md`：`§5`→`§6`、`§7`→`§8` 引用修正（顺移后果）。
- `Coder/20_Workflow_Lifecycle/butler-upgrade.md`：`§7`→`§8` 引用修正（×3）。
- `Coder/20_Workflow_Lifecycle/mcv-deployment.md`：`§6`→`§7` 引用修正。
- `templates/rule-card.md`：裁决=不改（记理由）。
- `.ai/PROJECT.md`：收口前滚，现行约束加"提交规约"一句。

# Interface / Contract

- 提交规约格式契约（新增）：`type(scope): 中文描述 (ITER-NNNN)`；发布专用 `chore(release): vX.Y.Z — 聚合 ITER-A~B (级别)`；`Co-Authored-By:` 署名 trailer 为标准尾注（本仓真实历史全部带）。
- 切版仪式契约（扩写）：预检 → 版本级改动（VERSION/CHANGELOG/migration）→ git 序列（add→commit→tag→push）→ 切版后自检；语义 5 步不变，只加操作层。
- 复用契约（不新造）：切版前后一致性核对 = `context-persistence.md` 冷启动一致性自检 5 不变量；里程碑发布 = `milestone-schema.md` 里程碑收口机制。

# State / Boundary

- 只动规则正文与指针，不动 hook 代码、四件套字段 schema、P1-P5 状态机、VERSION 数值、根 CHANGELOG 已有条目、迁移配方格式。
- 提交规约作用域=butler 仓自身提交（versioning-schema 的 scope）；目标项目提交规约的推广不在本次。
- 里程碑收口机制、semver 语义、SSOT、迁移配方格式均只引用既有单一来源，不重写。

# Design Decisions

- DD1（Q1）：「提交规约」作**新 §5**插在 §4 git tag 与原 §5 切版流程之间——日常提交是切版的上位动作，"提交→切版"相邻最合读者动线。代价=原 §5-8 顺移 §6-9 + 修 6 处外部 §引用 + 2 处内部；按本仓"无隐式依赖"约束必须同步，已纳入执行步骤。
- DD2（Q2）：type 允许集借鉴 conventional commits——`feat/fix/docs/refactor/chore/test/style`；scope 取规则模块 / 区域名（如 `hook`、`lifecycle`、`versioning`、`readme`、`release`）；描述用中文。**显式声明"借鉴其格式、非严格遵循全套 conventional 规范"**，避免读者误按英文全规范执行。
- DD3（Q4）：明确"**提交 ≠ 切版**"两路径——日常迭代收口=一次 `feat/docs/…(ITER-NNNN)` commit + push（不切 tag、不改 VERSION）；发布=按需聚合若干已收口迭代走切版仪式。
- DD4：切版预检/后检**复用** context-persistence 一致性自检 5 不变量，不新造校验器。
- DD5：切版仪式若发布里程碑，走 `milestone-schema.md` 引用，不重写里程碑收口。
- DD6：commit message **非 hook 机械门禁**（PreToolUse 管不到 git commit，且 butler 不跑自身 hook），SOP 内显式声明靠纪律 + 收口自检兜底；`Co-Authored-By:` 署名 trailer 记为标准尾注（本仓历史全带）。
- DD7（Q3）：rule-card **不收录**提交规约——它非产物链硬门、非封闭枚举、不进 hook `phase_gate`，属纪律类；rule-card 只承载强制产物集与机械约束，收录会稀释其定位。记理由于交付。

# Execution Steps

- [ ] T1 改 `versioning-schema.md` frontmatter title→「提交与版本治理协议」、scope 补提交规约 + 切版仪式 → AC8
- [ ] T2 插入新 §5「提交规约」：格式 / type 集 / scope 口径 / 中文描述 / `(ITER-NNNN)` 尾注（可多迭代）/ 发布形态 / 何时提交 / 一次装什么 / body 引用不复述 / 非门禁声明 / 署名 trailer → AC1, AC2, AC3
- [ ] T3 原 §5-8 顺移 §6-9，修内部 § 引用（第15行"发布流程（§5）"→§6、第63行"（§5 在切版时已产出）"→§6）→ AC11
- [ ] T4 扩写新 §6 切版流程：切版前预检（复用一致性自检 5 不变量 + 区间迭代均 closed / 无悬挂 active）+ git 精确序列（add→`chore(release)` commit→`git tag vX.Y.Z`→push+push tag）+ 切版后自检（VERSION==tag==CHANGELOG 顶条）+ 里程碑发布引用 milestone-schema → AC5, AC7
- [ ] T5 新 §6 加"提交 ≠ 切版"两路径段 → AC6
- [ ] T6 修外部 § 引用：`migration-schema`（§5→§6、§7→§8）、`butler-upgrade`（§7→§8 ×3）、`mcv-deployment`（§6→§7）→ AC11
- [ ] T7 同步指针：README §139、CLAUDE.md VERSION 行、HUMAN_GUIDE versioning 注释 → AC9
- [ ] T8 rule-card 裁决记录（不改，DD7 理由）→ AC10
- [ ] T9 抽查 git 历史 5-8 条逐条对照规约（AC4 验证动作）→ AC4
- [ ] T10 P5：git diff 核对不变量文件未动 + 逐 AC 回填 VERIFY_REPORT → AC11
- [ ] T11 收口前滚 `PROJECT.md` 现行约束加"提交规约"一句 → AC10

# Verification Plan

- AC1/2/3/5/6/7：读改后 versioning-schema §5/§6，核对格式 / 两路径 / git 序列 / 预检后检 / 里程碑引用齐备。
- AC4：`git log` 抽样逐条套规约。
- AC8/9：读 frontmatter + grep versioning-schema 在 README/CLAUDE/HUMAN_GUIDE 描述。
- AC10：rule-card 裁决记录 + PROJECT.md diff。
- AC11：`git diff --stat` 确认 semver 段/SSOT 段/迁移格式/四件套 schema/hook/VERSION/根 CHANGELOG 未动；grep `§[0-9]` 确认无断引用。

# Risks / Open Questions

- 顺移后 § 引用断裂风险 → 缓解：T6 后全仓 grep `versioning-schema.md §` + 文件内 grep `§[0-9]` 复核。
- conventional commits 误读风险 → 缓解：DD2 显式"借鉴非全套"声明。
- Open Questions Q1-Q4 均已在 DD1-DD3/DD7 定案，无遗留。
