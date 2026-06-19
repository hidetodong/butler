> 分流: 完整 | 命中升级信号: 多文件改动(≥3) / 反转既有规则(ITER-0006「preference 不纳入项目配置」) / 契约语义(三态生效条件 + 真源归属) / 跨模块影响(local-constraints-schema·preference-engine·logic-protocol·部署·rule-card·人类文档·Coder README) / 设计取舍(per-project 抑制 vs 跨项目真源 双源消歧) | 2026-06-19

# Goal
- 把 preference（偏好探针）**接入项目级配置** `.ai/local-constraints.md`「Butler 功能开关」段，新增 `preference: on|off`（默认 on）作为**本项目抑制开关**——让它与 `dangerous`/`independent_review` 在同一处统一可见、可读、可控（用户要求）。
- 同时**不破坏 preference 的跨项目本质**：consent / signals / profile 的真源仍在外置 `$PREF`，本开关只管"这个项目要不要采集"，不双写外置状态。

# Background / 为什么做 + 冲突挑明
- 用户问"preference 会自动开启吗"，确认其机制（一次同意后默认常驻、反哺 opt-in），随后要求"preference 也应写进配置里"。
- **这反转了 ITER-0006 的一条特意决策**：当时把 dangerous/independent_review 写进 local-constraints 时，**特意排除了 preference**，理由是"preference 跨项目、外置存储，不是项目级配置"（写在 local-constraints-schema §4.1、rule-card、HUMAN_GUIDE、Coder/README 四处）。
- 我已向用户挑明此冲突并给出三种语义（per-project 抑制 / 只读镜像 / 全量接管），**用户选定 A：per-project 抑制开关**。本轮据此反转排除条，但用"抑制层"而非"全量接管"来调和——保住跨项目真源不被破坏、不引入双真源。

# 语义（已与用户锁定）
- **本项目是否运行探针** = 全局未 `/preference off` **且** 外置 `$PREF` `consent: granted` **且** 本项目 `preference ≠ off`；三者全真才在本项目采集/蒸馏/反哺。
- `preference: off`（项目级）**只抑制本项目**，不改全局 consent、不动 `$PREF` 数据、不影响其他项目。
- 缺字段（legacy/旧部署）= 视为 `on`（不抑制），行为同旧版（仅受全局同意约束）。
- 外置 `$PREF` 仍是 consent/signals/profile 的**跨项目唯一真源**；本开关不双写它（不是镜像、不是第二真源，而是"本项目采集闸"）。

# Scope
## In
1. **schema**：`local-constraints-schema.md` §2 必填字段 + §3 模板「Butler 功能开关」段增 `preference: on`；§4.1 把"preference 不纳入"反转为"per-project 抑制开关"口径（含三态生效条件与真源归属，作为该语义 SSOT）。
2. **引擎**：`preference-probe-engine.md` 增项目级抑制开关（新 §2.5）+ 在 §2.1 默认常驻处标注"受项目级抑制"；明确生效优先级（全局 off > 全局 consent > 项目开关）。
3. **接线**：`logic-protocol.md` §1.3 会话起始读取增 `preference` 项；§4 Preference Mode 补"per-project 抑制开关落 local-constraints"。
4. **部署默认**：`mcv-deployment.md §4` 生成「Butler 功能开关」段时含 `preference: on`（默认 on，安全——实际采集仍需全局同意）。
5. **传播**：`rule-card.md`（项目级功能开关节，反转排除句）、`HUMAN_GUIDE.md`（开关表加 preference 行 + 更新"偏好探针不在这里"注）、`Coder/README.md`（local-constraints-schema 描述反转"偏好不纳入"）。

## Out（非本轮）
- 不把 consent / reback / signals / profile 搬进 local-constraints（选项 C 已否决：破坏跨项目本质 + 双真源）。
- 不为 preference 开关加 hook 校验（与 dangerous/independent_review 同等，靠规则纪律）。
- 不改采集/蒸馏/反哺算法、外置存储契约、§3 安全底线、与 /dangerous 的完全隔离。
- 不切新版本（按需聚合；ITER-0009 累积到下次切版，预计 MINOR——新增项目级开关能力）。

# Key Design Decisions
1. **抑制层而非接管**：项目开关是"本项目采集闸"，与外置全局 consent 分管不同层面——故不构成双真源（governs 不同的东西）。
2. **默认 on 是安全的**：`preference: on` 不等于"强制采集"——实际采集仍要全局 consent=granted；未同意时 on 也不会偷采。安全默认。
3. **真源不变**：外置 `$PREF` 仍是 consent/data 跨项目真源；schema/engine 反复申明，避免被误读成"项目级真源"。
4. **与 dangerous 区别对待**：preference 是只读观察者、低风险，**不需要 announce-on-read**（dangerous 才需要）；会话起始读到即遵循即可。
5. **反转要彻底**：四处"排除"措辞全部改写，避免规则自相矛盾。

# Risks / Open Questions
- 反转既有决策需保证四处措辞一致改写，否则规则内部打架——以"逐处 grep 校验旧排除句消失"兜底。
- "默认 on 但需全局同意"可能被误读为"装了就采集"——文案须显式写"on≠强制采集，仍需全局同意"。
- 项目开关靠规则纪律（会话起始读 + 遵循），无 hook 强制——与现有 dangerous/independent_review 同源同险。

# 影响文件（预估）
- 改：`Coder/20_Workflow_Lifecycle/local-constraints-schema.md`、`Coder/70_Extension_Preference/preference-probe-engine.md`、`Coder/00_System_Prompt/logic-protocol.md`、`Coder/20_Workflow_Lifecycle/mcv-deployment.md`、`templates/rule-card.md`、`HUMAN_GUIDE.md`、`Coder/README.md`。
- 零改动护栏：preference 采集/蒸馏/反哺算法（§5/§6/§7）、外置存储契约（§4）、§3 安全底线、与 /dangerous 隔离（§9）、ledger_status hook、产物链四 schema、versioning-schema。
