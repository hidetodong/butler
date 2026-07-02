# CONCEPT — ITER-0020

> 分流：完整路径 | 命中升级信号：新增契约（提交/切版规约）、多文件接线、跨阶段影响（收口↔发布） | 2026-07-02

## 一句话

butler 每次提交都在遵循一套约定（`type(scope): 中文描述 (ITER-NNNN)`、发布用 `chore(release)`），但这套约定**全靠隐性模仿、零成文**；而切版流程 `versioning-schema §5` 只写到"改 VERSION / 加 CHANGELOG / 写迁移 / 打 tag"的语义层，**没落到 git 操作层**（stage 什么、commit message 长什么样、push 与 tag 的先后、切版前后怎么自检）。本迭代把"日常提交规约 + 切版 git 仪式"补成一份可照做的 SOP，就地扩写进 `versioning-schema.md`。

## 背景与判断

- 用户诉求：在仓库内做一份"提交切版"的 SOP。
- 现状扫描：全仓 grep `commit message / 提交规约 / conventional` 零命中——提交约定有实践、无规则；但 git 历史近 40 条前缀分布高度一致（`feat(scope)` / `docs` / `chore(release)` + 尾部 `(ITER-NNNN)`），是稳定的隐性契约，值得固结成文。
- 切版侧 `versioning-schema §5` 已有 5 步语义骨架，缺的是 git 操作层与切版前后自检——不是从零造，是补齐"最后一公里"。
- 落点已定（用户三选）：就地扩写 `versioning-schema.md`（不新建文件）、提交规约 + 切版仪式都做、按 ITER-0020 正式迭代走。
- 复用而非另造：切版前/后的一致性核对**复用** ITER-0019 已定义的冷启动一致性自检 5 不变量（`context-persistence.md`），不新造一套校验。
- 归属：本 SOP 不在 MILE-0001（冷启动全貌 + 收口门槛，R1/R2/R3 已封口）范围内，故 ITER-0020 作**独立迭代**（所属 milestone `—`），不吸附进仍 active 但已达成的 MILE-0001。

## 目标（Goal）

- G1：在 `versioning-schema.md` 新增「提交规约」——固化 commit message 格式（type/scope/中文描述 + `(ITER-NNNN)` 尾注）、发布专用 `chore(release): vX.Y.Z — 聚合 …` 形态、何时提交、一次提交装什么、body 引用而不复述。
- G2：把 `versioning-schema §5` 切版流程从语义 5 步扩成含 git 操作层的可照做仪式：切版前预检（复用一致性自检）→ 版本级改动（VERSION / CHANGELOG / migration）→ git add/commit/tag/push 精确序列 → 切版后自检（VERSION 数值 == tag == CHANGELOG 顶条版本）。
- G3：接线与指针同步——更新 versioning-schema 的 title/scope、`Coder/README §139` 一句话描述、`CLAUDE.md` 与 `HUMAN_GUIDE.md` 对 versioning-schema 的引用；按需前滚 `PROJECT.md` 现行约束。
- G4：dogfood 自洽——SOP 里的切版仪式与本仓真实 git 历史（`chore(release)` 形态、tag `vX.Y.Z`）对得上；rule-card 裁决（提交规约是否进强制卡，倾向不进）。

## 约束（Constraints）

- 就地扩写，不新建规则文件（用户选定）。
- 不改 semver 语义（§2）、SSOT（§1）、迁移配方格式（`migration-schema.md` 主管，只引用）。
- git commit message 不做 hook 机械门禁——PreToolUse hook 管不到 git commit，且 butler 自身不跑 hook；提交规约靠纪律 + 收口自检兜底，须在 SOP 内写明"非机械门禁"。
- 切版仪式里"里程碑收口"部分只引用 `milestone-schema §里程碑收口`，不重写里程碑收口机制（单一来源）。
- 守本仓五约束（分层 / 产物链 / 无隐式依赖 / 模板单一来源 / audience 标注）。

## 影响范围（Impact Scope）

- 改（核心）：`Coder/20_Workflow_Lifecycle/versioning-schema.md`——frontmatter scope + 新增提交规约节 + 扩写 §5。
- 改（接线）：`Coder/README.md §139`（versioning-schema 一句话描述）、`CLAUDE.md`（VERSION 行引用描述）、`HUMAN_GUIDE.md`（versioning-schema 注释）。
- 按需：`.ai/PROJECT.md`（现行约束段补"提交规约"一句，收口时前滚）；`templates/rule-card.md`（裁决，倾向不改）。
- 不影响：四件套字段 schema、P1-P5 状态机、hook 体系代码、迁移配方格式、根 CHANGELOG 已有条目、VERSION 数值、里程碑收口机制。

## 项目类型与 Profiles

Markdown 规则仓。本迭代纯规则正文，不动 hook Python，无代码 profile 命中；按通用 SOP 推进。

## 待澄清（Open Questions）

- Q1：提交规约放 `versioning-schema.md` 内**独立一节**（现有 §5 之前），还是并进现有节？倾向新增独立节——提交是切版的上位日常动作，值得显式成节。（P3 定）
- Q2：type 允许集固定为哪些？倾向借鉴 conventional commits 常用类（feat/fix/docs/refactor/chore/test/style）+ 说明 scope 取规则模块名。（P3 定）
- Q3：rule-card 是否收录提交规约？倾向否（提交非产物链硬门、非封闭枚举，属纪律类），记理由。（P3 定）
- Q4：是否补一段"仅提交不切版"的日常路径（本仓常见：迭代收口只 commit+push、不切 tag）？倾向补，明确"提交 ≠ 切版"两条路径。（P3 定）
