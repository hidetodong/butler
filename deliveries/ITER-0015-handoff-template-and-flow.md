# handoff 格式契约补全：模板骨架 + 蒸馏生成流程

> ITER-0015 · 迭代交付（小版本） · 收口 2026-06-30

## 本次交付目标

- `handoff-spec.md` 原本只规定了 `02_SESSION_HANDOFF.md`「填哪些字段」（§3），却没说它「长什么样」「怎么一步步蒸馏」——AI 有字段却没有固定骨架可填、没有步骤可循，冷启动交接的结构因会话而异。
- 这次把这份半截契约补全：加固定模板骨架 + 不得跳步的生成流程。
- 补领说明：本迭代内容在建号前已落地于工作树，受用户监督决定正式归档入账（非危险模式）。

## 已完成内容

- `handoff-spec.md` 新增 §4 模板骨架：H1 锁死为 `# Session Handoff`，6 个 H2（任务断点 / 关键决策摘要 / 环境脏点 / 已知风险 / 唤醒指令 / 状态指针）顺序与 §3 字段表一致，每个 H2 带占位注释，并附三条模板规则（H1 不得改写 / H2 顺序固定不得增删 / 占位注释落盘须替换）。
- `handoff-spec.md` 新增 §5 生成流程：5 个不得跳步的步骤——来源确认（task-state > 产物链 > 对话）、字段映射、长度自检（≤500 tokens）、完整性自检、覆盖式落盘；外加 4 条反模式（禁写思考过程 / 禁复制大段日志 / 禁罗列已完成清单 / 禁写成对人交付总结）。
- `context-persistence.md` §6 蒸馏规则补一行指针，指向 handoff-spec §4 骨架与 §5 步骤。

## 关键变更 / 用户可感知变化

- 以后冷启动写 `02_SESSION_HANDOFF.md` 有固定骨架可照填、有步骤序列可照走，跨会话交接的结构不再因人而异。
- 职责边界更清晰：handoff-spec 管「长什么样 + 怎么生成」，context-persistence 仍管「何时蒸馏 + 维护什么状态」。
- 向后兼容：纯文档口径补全，没动任何字段语义、没碰 hook，老 handoff 不受影响。

## 高层影响范围

- 规则层：改 `Coder/40_Context_Management/handoff-spec.md`（§4/§5 新增）、`context-persistence.md`（§6 一行）。
- 没碰：§3 必填字段表、四件套字段、hook、lifecycle 分流、迭代 / 里程碑 / 版本机制、对话层规则。

## 验证方式与结果摘要

- 5 条验收项全部满足：§4 骨架（H1 + 6 H2 + 模板规则）、§5 流程（5 步 + 反模式）齐全；H2 顺序对齐 §3、长度上限对齐 §2、状态指针可省对齐 context-persistence §6；§6 指针在位。
- git diff 确认改动仅 handoff-spec(+55) 与 context-persistence(+1)，§3 字段表与 frontmatter 未动。
- 本仓 CLAUDE.md 五约束自检通过。

## 已知剩余风险 / 延后事项

- 模板骨架与生成流程靠 AI 读取遵守、无 hook 机械强制（同 artifact-style 既有取舍，可接受）。
- 本轮不切版，累积到下次发布。

## 引用

- `.ai/iterations/ITER-0015/CONCEPT.md`
- `.ai/iterations/ITER-0015/AC_LIST.md`
- `.ai/iterations/ITER-0015/TECH_PLAN.md`
- `.ai/iterations/ITER-0015/VERIFY_REPORT.md`
- 改动规则：`Coder/40_Context_Management/handoff-spec.md`（§4/§5 新增）、`Coder/40_Context_Management/context-persistence.md`（§6）
