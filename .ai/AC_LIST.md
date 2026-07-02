---
状态: ack-frozen
ACK 日期: 2026-07-02
---

> ITER-0020（独立迭代，所属 milestone `—`；MILE-0001 虽仍 active，但本 SOP 不在其范围，故不吸附）。分流与背景见 CONCEPT，不重述。

# Goal

- 把 butler 的"日常提交规约 + 切版 git 仪式"补成一份可照做的 SOP，就地扩写进 `versioning-schema.md`：提交约定从隐性实践固结成文，切版从语义 5 步落到 git 操作层。

# In Scope

- `versioning-schema.md` 新增「提交规约」节。
- `versioning-schema.md §5` 扩写为含 git 操作层 + 切版前后自检的仪式。
- versioning-schema title/scope 更新 + README / CLAUDE / HUMAN_GUIDE 指针同步。
- rule-card / PROJECT.md 裁决与按需前滚。

# Out of Scope

- 不新建规则文件。
- 不改 semver 语义 / SSOT / 迁移配方格式 / 里程碑收口机制（均引用既有单一来源）。
- 不做 git commit 的 hook 机械门禁。
- 不实际发布 MILE-0001 或切任何版本（本迭代只写 SOP）。
- 不动 hook Python 代码、四件套字段、P1-P5 状态机。

# Acceptance Checklist

- [ ] AC1: `versioning-schema.md` 新增「提交规约」节，明确 commit message 格式 `type(scope): 中文描述 (ITER-NNNN)`——列出允许的 type 集、scope 取值口径（规则模块名）、描述语言（中文）、迭代号尾注规则（可引用多个 ITER）。
- [ ] AC2: 提交规约节写明发布专用提交形态 `chore(release): vX.Y.Z — 聚合 ITER-NNNN~NNNN (级别)`，并与日常迭代提交区分。
- [ ] AC3: 提交规约节写明"何时提交 / 一次提交装什么 / commit body 引用 `deliveries/` 与 `ITERATIONS.md` 而不复述"，并显式声明 commit message 非 hook 机械门禁、靠纪律 + 收口自检兜底。
- [ ] AC4: 提交规约与本仓真实 git 历史自洽——抽查近若干条历史提交（`chore(release): v1.5.0 …`、`feat(hook): … (ITER-0019)` 等）均能被规约覆盖，无冲突。
- [ ] AC5: `versioning-schema §5` 扩写为含 git 操作层的完整切版仪式，在保留原语义 5 步（定 bump / 改 VERSION / 加 CHANGELOG / 写 migration / 打 tag）基础上补：①切版前预检（复用 `context-persistence.md` 一致性自检 5 不变量 + 待聚合迭代均 `closed`、无悬挂 active）②git 精确序列（add 哪些 → `chore(release)` commit → `git tag vX.Y.Z` → push + push tag）③切版后自检（VERSION 数值 == tag 数字 == CHANGELOG 顶条版本，三者对齐）。
- [ ] AC6: §5 明确"提交 ≠ 切版"两条路径——日常迭代收口的 commit+push（不切 tag）与聚合发布的切版仪式分开；切版是按需聚合动作、非每迭代触发。
- [ ] AC7: §5 切版仪式中若本次发布的是一个里程碑，引用 `milestone-schema.md` 的里程碑收口机制处理里程碑台账 / 归档 / 版本级交付，不在 versioning-schema 内重写该机制。
- [ ] AC8: versioning-schema.md frontmatter `title` 与 `scope` 更新，反映其现在也承载提交规约与切版仪式（不止版本治理）。
- [ ] AC9: 指针同步——`Coder/README.md §139` versioning-schema 一句话描述、`CLAUDE.md` VERSION 行引用、`HUMAN_GUIDE.md` versioning-schema 注释均更新，与新范围一致；守"无隐式依赖"。
- [ ] AC10: rule-card 裁决（提交规约是否进强制卡）并记理由；`.ai/PROJECT.md` 现行约束段按需补"提交规约"一句（收口前滚）。
- [ ] AC11: 不破坏不变量——semver 语义 §2 / SSOT §1 / 迁移配方格式 / 四件套字段 schema / hook 代码 / P1-P5 状态机 / VERSION 数值 / 根 CHANGELOG 已有条目 均未改；本仓五约束自检。

# Verification Method

- AC1/2/3: 读改后 versioning-schema 提交规约节，核对格式 / type 集 / scope / release 形态 / 何时提交 / 非门禁声明。
- AC4: 抽 5-8 条 `git log` 历史提交逐条对照规约，确认无冲突。
- AC5/6/7: 读改后 §5，核对预检 / git 序列 / 切版后自检三段齐备、两路径分开、里程碑走引用。
- AC8/9: 读 frontmatter + grep versioning-schema 在 README / CLAUDE / HUMAN_GUIDE 的描述，确认同步。
- AC10: 看 rule-card 裁决记录 + PROJECT.md diff。
- AC11: git diff 确认未碰不变量文件 / 段落。

# Open Questions / Risks

- 见 CONCEPT Open Questions（提交规约成节位置 / type 允许集 / rule-card 裁决 / 是否补"仅提交"路径），P3 定。
- 风险：与 conventional commits 的关系——采用其格式但用中文描述，须在 SOP 内说明"借鉴其格式、非严格全套遵循"，避免读者误按英文 conventional 全规范执行。
- 风险：规约作用域——写在 versioning-schema（scope=butler 仓自身版本治理），默认只约束 butler 仓提交；是否推广到目标项目留 Out of Scope / 后续。
