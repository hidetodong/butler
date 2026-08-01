---
状态: ack-frozen
ACK 日期: 2026-08-01
---
<!-- butler-artifact-template: 1.0.0 artifact=acceptance -->
# AC_LIST — ITER-0100

## Goal

- 让 Claude 与 Codex / ChatGPT 使用同一套 Butler 语义路由规则，并把「总结当前会话后领取一个迭代」变成可重复、可审计的标准工作流。

## In Scope

- 宿主无关的 Router 规则、结果状态和消歧行为。
- `workflows/registry.json` 中的 Router 元入口、工作流消歧元数据和新 `iteration` 工作流。
- Claude `/butler` 与 `/butler:iteration`，以及 Codex / ChatGPT `butler-router` 与 `butler-iteration` 薄适配器。
- registry 同步器、生成的人读文档、安装分发和双宿主回归测试。

## Out of Scope

- 不新增 Pi Router 入口。
- 不引入向量库、独立分类服务或用户行为学习。
- 不改宿主平台本身的 `@`、slash 或 `$` 交互机制。
- 不修改现有 12 个工作流的业务算法，不把原始会话全文持久化到 `.ai/`。

## Acceptance Checklist

- [ ] AC1: Router 的语义分类和安全规则只有一份宿主无关真源；Claude Command 与 Codex Skill 只做发现、路由和输入输出转换，不复制这套算法。
- [ ] AC2: registry 能表达不参与候选的 Router 元入口，以及业务工作流的优先级、排除词、冲突项和前置条件；未知字段、自路由和宿主投影缺失都会校验失败。
- [ ] AC3: Claude 可通过 `/butler <自然语言>` 进入 Router，且根命令与现有 `/butler:progress` 等命名空间命令能同时发现；直接调用具体命令时不经 Router。
- [ ] AC4: Codex / ChatGPT 可通过允许隐式调用的 `butler-router` Skill 进入同一 Router；直接调用 `$butler-progress` 等具体 Skill 时不经 Router。
- [ ] AC5: 一组双宿主共用的语义样例能覆盖 13 个业务工作流的代表性输入；两端对同一输入选出相同的主工作流，需要串联时一次只选一个主路由。
- [ ] AC6: `loop` 与 `dangerous` 在两端都不能被 Router 隐式开启；普通语义只返回 `explicit-required` 和各宿主的显式入口，只有用户直接调用该入口才能进入。
- [ ] AC7: Router 统一返回 `routed`、`ambiguous`、`explicit-required` 或 `not-butler`；多候选无法稳定消歧时必须请用户选择，不属于 Butler 的请求不强行路由。
- [ ] AC8: registry 新增 `iteration` 业务工作流，并生成 Claude `/butler:iteration` 与 Codex `$butler-iteration` 薄入口；「总结当前 session 并领取 / 开启迭代」等语义可被 Router 稳定分发到它。
- [ ] AC9: `butler-iteration` 只将用户已确认的决定写成当前理解，把模型建议和待澄清项分开标明；不保存原始会话全文，单纯「总结一下」保持只读且项目字节不变。
- [ ] AC10: 无 active 迭代时，`butler-iteration` 依次解析唯一项目根、判断分流和里程碑归属、从复合台账分配下一号、整体重置五件套、写入 P1 CONCEPT、更新 task-state 并重建 handoff；任一确定性检查失败时不留半开启状态。
- [ ] AC11: 已有 active 迭代时，`butler-iteration` 不分配新号；P1 未冻结时只建议将新结论并入当前 CONCEPT，P2 后按迭代内修订或影响面扩张规则处理，机械测试确认不会出现两个 active。
- [ ] AC12: registry 同步器可幂等生成新入口、Skill 元数据、人读能力表和仓内发现链接；专项回归、官方 Codex Skill 校验、`git diff --check` 与完整 `bash scripts/verify-ci.sh` 全部通过。

## Verification Method

- AC1: 扫描 Router 规则与两端适配器的引用关系，用重复算法负向样例锁定单一真源。
- AC2: 运行 registry schema 正向、未知字段、自路由、投影缺失和路径越界样例。
- AC3: 在 Claude 命令发现 fixture 中同时检查 `/butler` 与 `/butler:xxx`，并验证直接命令优先。
- AC4: 运行 Codex Skill 结构校验和隐式调用元数据断言，验证直接 Skill 优先。
- AC5: 对共用样例表分别运行 Claude / Codex 投影校验，比较主工作流与串联顺序。
- AC6: 用「一直做到底」、「无人值守」等输入跑双端负向测试，再分别验证显式入口仍可用。
- AC7: 对单候选、多候选、高风险候选和非 Butler 请求逐类断言返回状态与下一动作。
- AC8: 运行 registry 同步后检查两端 `iteration` 入口与语义触发投影。
- AC9: 用混合「用户决定 / 模型建议 / 待澄清」的会话 fixture 验证 CONCEPT 投影，并对只读总结执行前后项目哈希对比。
- AC10: 在临时 Butler 项目跑完整开启路径与每个故障注入点，对账台账、五件套、task-state、handoff 和零半状态。
- AC11: 分别构造 P1 active、P2 已冻结和影响面扩张 fixture，检查路由结果与 active 数量。
- AC12: 连续两次运行 registry 同步并比较字节，再运行专项测试、Codex Skill 校验、`git diff --check` 和完整 CI。

## External References

- N/A

## Open Questions / Risks

- ChatGPT App 的真实 `@Butler` 交互受平台能力影响；仓内验收只能保证 Plugin / Skill 元数据、隐式调用政策和安全退路，不冒充真实界面端到端证据。
- Claude `/butler` 与 `/butler:xxx` 的共存需要实际发现测试；如果宿主不支持同名根文件与目录，P3 必须退回可验证的显式备选名称，不能伪造支持。
