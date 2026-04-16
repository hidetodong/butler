# Goal

- 修复 Butler Should Fix Bucket C（Mode 术语双关消歧）1 条问题：`logic-protocol.md § 4` 的 Standard/Ideation/Loop/Review "Mode"（扩展模块激活状态）与 `mode-switch.md` 的 Architect/Coder/Reviewer "Mode"（同一执行者的职责切换）共用"Mode"一词，读者难以区分。

# Current Understanding

- 本任务是 Butler 规则仓维护的第五轮。Bucket B 已随 commit `b25c1b7` 落地。
- 两类 Mode 的语义不同：
  - logic-protocol 的 Mode 是**运行时能力**（是否激活 Ideation/Loop/Review 引擎），与 `/xxx` 指令强绑定，不宜改动（术语已深入）。
  - mode-switch 的 Mode 是**同一执行者的职责切换**（P1-P3 用 Architect 帽子、P4 用 Coder 帽子、P5 用 Reviewer 帽子），与角色/职责概念更贴近。
- 审计报告建议：改 mode-switch 这一侧的术语为 Role/Hat/Persona，保留 Mode 给扩展模块。
- 本轮存在一个主要设计取舍（术语选型 + 是否重命名文件）需要用户拍板。

# Constraints

- 显性约束：
  - 不破坏 `logic-protocol.md § 4 模块激活感知` 中 Standard/Ideation/Loop/Review 的语义与命令绑定。
  - 不修改 lifecycle.md 的 P1/P2/P3/P4/P5 阶段定义。
  - 若重命名文件，必须同步更新所有引用点，避免 broken link。
- 隐性约束：
  - 术语应清晰、中性、可中英对照（中文为主体）。
  - 选定术语应能与产物链中的现有词汇（如 `mcv-update.md` 中的"热/冷数据"）风格一致，不过度术语化。

# Impact Scope

预计修改文件（取决于方案选型）：
- `Coder/40_Context_Management/mode-switch.md`（内部 6 次 "Mode" 术语 + 标题）
- `Coder/40_Context_Management/context-persistence.md:124`（引用）
- `Coder/README.md:62`（目录结构引用）
- 若重命名：新文件名 + 上述引用同步

不影响：`logic-protocol.md § 4 模块激活感知`（保留 Mode 术语）、`lifecycle.md` P 阶段定义、其他规则文件、templates、scripts。

# Project Type / Active Profiles

- 项目类型：Markdown 规则仓库。
- 未命中任何 Domain Profile。

# Open Questions

- **C-1** 术语选型与是否重命名文件需要用户拍板（见 AC_LIST 的方案列表）。
