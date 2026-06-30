> 补领入账：实现先于建号，本方案为已落地改动的回填记录（ITER-0015，受监督）。

# Goal

- 支撑 AC1–AC5：把 handoff 格式契约补全为「字段 + 骨架 + 生成流程」。

# Files / Modules to Change

- 改 `Coder/40_Context_Management/handoff-spec.md`——在 §3 字段表后新增 §4 模板骨架、§5 生成流程（AC1/AC2/AC3/AC5）。
- 改 `Coder/40_Context_Management/context-persistence.md`——§6 蒸馏规则一行补指针，指向 handoff-spec §4/§5（AC4）。

# Interface / Contract

- `02_SESSION_HANDOFF.md` 结构契约：H1 = `# Session Handoff`（锁死）；6 个 H2 顺序 = §3 必填字段表顺序；「状态指针」简单任务可省，其余 5 项必填。
- 生成流程契约：来源优先级 task-state > P1–P3 产物链 > 对话上下文；落盘覆盖式、不留历史版本。
- 不新增字段、不改 §3 字段语义——§4 是 §3 的「形」、§5 是 §3 的「序」。

# State / Boundary

- handoff-spec 管「结构与生成」，context-persistence 管「触发与状态维护」，边界不重叠。
- 不碰 hook、四件套字段、lifecycle 分流。

# Design Decisions

- 模板骨架内联进规范正文，不另立 `templates/` 文件——它是 handoff-spec 的示例锚点、随规范走，避免又一个会漂的副本（同 rule-card 占位符继承纪律的取向）。
- §4/§5 紧接 §3 之后，保持「字段→骨架→流程」的自然阅读序。

# Execution Steps

1. handoff-spec 加 §4 模板骨架 + 模板规则。
2. handoff-spec 加 §5 生成流程 + 反模式。
3. context-persistence §6 补一行指针。
4. 自检 H2 顺序 / 长度上限 / 状态指针可省三处对齐。

（注：步骤已先行落地，本记录为补领回填。）

# Verification Plan

- 按 `AC_LIST.md` 的 Verification Method 逐项核对；git diff 确认改动面仅限两文件、§3 字段表与 frontmatter 未动。

# Risks / Open Questions

- 无遗留。模板骨架靠 AI 读取遵守、无 hook 机械强制（同 artifact-style，可接受）。
