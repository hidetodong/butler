> 分流: 简化 | 命中升级信号: 均未命中（2 文件、纯文档口径补全、零代码/契约变更） | 2026-06-30
> 补领入账: 本迭代内容在开本号前已实现于工作树（handoff-spec §4/§5 + context-persistence §6 引用），现按用户决定正式归档为 ITER-0015。非危险模式，受监督补号。

# 一句话

handoff-spec 之前只规定了 `02_SESSION_HANDOFF.md`「填哪些字段」（§3 必填字段表），却没说它「长什么样」和「怎么一步步蒸馏出来」——AI 有字段清单却没有固定骨架可填、没有生成步骤可循，冷启动 handoff 的结构会因会话而异。这次把这份格式契约补全：加 §4 固定模板骨架（H1 + 6 个 H2）+ §5 五步生成流程 + 反模式，并让 context-persistence §6 指过来。

# Goal

- G1 给 `02_SESSION_HANDOFF.md` 一个固定模板骨架：H1 锁死、6 个 H2 顺序与 §3 字段表一致、带占位注释与模板规则。
- G2 给冷启动蒸馏一个不得跳步的 5 步生成流程（来源确认→字段映射→长度自检→完整性自检→落盘）+ 禁止的产出形态。
- G3 context-persistence §6 指向新增的 §4/§5，把"何时蒸馏"接到"蒸馏成什么样"。

# Current Understanding

- handoff-spec 原本止于 §3 字段表，缺「骨架」与「步骤」，是半截契约；填字段全靠 AI 自由发挥，结构不稳。
- 模板骨架与 §3 字段表一一对应、H2 顺序锁死；生成流程明确来源优先级、长度自检（≤500 tokens）与完整性自检。
- 纯文档口径补全，不碰 hook、不碰四件套字段、不碰 lifecycle 分流。

# Constraints

- 守本仓 CLAUDE.md 五约束。
- 职责不与 context-persistence 重叠：handoff-spec 只管 `02_SESSION_HANDOFF.md` 的结构与生成，触发时机与状态维护仍归 context-persistence。
- 模板骨架是规范正文的内联示例，不是新模板文件，不进 `templates/`。

# Impact Scope

- 改：`Coder/40_Context_Management/handoff-spec.md`（新增 §4 模板骨架 / §5 生成流程）、`context-persistence.md`（§6 引用补全 +1 行）。
- 不影响：四件套字段、hook、lifecycle 分流、迭代 / 里程碑 / 版本机制、对话层规则。

# Project Type / Active Profiles

- 形态：Markdown 规则仓库（butler 自己）。Profiles：无，按通用 SOP + 本仓 CLAUDE.md 编辑约束。

# Open Questions

- 无。
