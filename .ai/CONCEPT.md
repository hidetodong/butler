> 分流: 完整 | 命中升级信号: 需求有歧义、多文件改动、契约变更、跨模块影响、设计取舍 | 2026-07-18

# 一句话

- Butler 已经能定义验收、方案和验证，却没有把它们串成统一的 Goal 完成资格。R1 先画清现状和失败样本，证明问题落在哪一层，再由后续迭代设计契约，避免边审计边发明答案。

# Goal

- 产出一份可审计的目标体系基线：说明 Butler 与当前宿主各自把“目标、计划、进度、完成”放在哪里，哪些状态只是推进投影，哪些事实才有资格参与最终完成判断。
- 把“任务做完但 Goal 不该完成”的典型情形固化为结构化反例，供 R2–R6 设计和回归测试复用。

# Current Understanding

- Butler 当前以 milestone 承载版本方向，以 iteration 承载单轮范围，以 `CONCEPT/AC_LIST/TECH_PLAN/VERIFY_REPORT` 承载目标理解、完成定义、方案和证据，以 `task-state` 承载运行进度；这些载体各自有纪律，但没有一份规则明确规定 Goal 完成状态必须由哪些下游事实共同裁决。
- `AC_LIST.md §6` 已给出任务完成最低口径，P5 也要求 evidence 和 review；然而宿主原生 goal/task 工具可以单独显示 complete，Butler 尚未明确它只是状态投影、不得覆盖 AC / evidence / review 的真相。
- 当前会话可观察到的 Codex Goal 能力提供 objective 与 active/complete/blocked 生命周期，并要求只有目标真正达成且无剩余必做工作时才能 complete；但它不替 Butler 自动审查方案、AC 或证据，也不能假定所有 Codex 版本或 Claude Code 有相同 API。
- 用户说的“方案没有百分之百通过”应落成离散可审计判定，而不是虚构置信百分比：方案要么通过、要么需修订、要么被阻塞；未通过就不能用任务完成状态掩盖。

# Constraints

- R1 只审计并冻结问题模型，不修改 P1–P5、Goal 状态机、宿主适配或完成门算法；这些属于 R2–R6。
- 不新增第二份运行台账，不把 Goal 与 milestone、AC、plan、task-state 重复记账。
- 宿主能力结论必须区分“当前会话可观察合同”和“Butler 可长期依赖合同”；未知处如实标注，不推断 Claude/Codex 对称。
- 失败样本必须包含输入事实、错误完成声明、预期处置和未来责任路线，能被后续机械裁决器转成 fixture。
- 危险模式自主 P2/P3 仍须留下横幅、RUN_LOG、checkpoint 和回滚锚点；没有 fresh-context 复核时不得冒称独立。

# Impact Scope

- 本迭代新增 `docs/research/` 下的目标体系基线与机器可读失败样本，更新本迭代 `.ai/` 运行态、归档与交付。
- 只读盘点 `Coder/00`、`20`、`30`、`40`、`60`、`65`、Claude commands、Codex skills/plugin、模板与状态审计器。
- 不修改共同内核规则正文、hook、plugin manifest、工作流 registry、目标项目部署模板或版本号。

# Project Type / Active Profiles

- Markdown 规则仓 + Python/Bash 工具 + Claude/Codex 双宿主适配。
- 未命中领域 profile，仅按通用 SOP；危险模式 ON。

# Open Questions

- “Goal”最终应是独立持久对象，还是从现有 milestone/iteration/AC 状态推导出的逻辑视图，留给 R2 依据本轮边界矩阵裁决。
- Codex Goal 与 Claude task 的具体接线和降级策略留给 R6；R1 只记录当前可观察能力与依赖禁区。
