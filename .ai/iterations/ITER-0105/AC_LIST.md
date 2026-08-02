---
状态: ack-frozen
ACK 日期: 2026-08-01
---
<!-- butler-artifact-template: 1.0.0 artifact=acceptance -->
# AC_LIST — ITER-0105

## Goal

- 为已由用户选定的 Decision slice 提供一个确定性、显式、可预演、可审计且幂等的 promotion 边界，使其能够引用到既有 Milestone planned route，或通过现有 iteration-intake 从 P1 开启 Iteration；整个过程不引入自动清晰度/体量判断，也不产生新的交付真源。

## In Scope

- 项目内 `decision-promotion` 模块及 `inspect / plan / apply / verify` 四动作 CLI。
- resolved Decision roots、传递依赖闭包、source slice digest 与 evidence pointer 投影。
- `route-reference` 与 `iteration-start` 两个显式 target adapter。
- 不可变 promotion receipt、幂等重试、并发/陈旧计划拒绝、故障检测与回滚。
- 与 Decision Map、Decision Work、Milestone、Iteration intake、P2 冻结变更分流的文档和 CI 接线。

## Out of Scope

- 自动判断需求清晰度、体量、是否启用 Explore 或选择 promotion target。
- 自动创建、排序或取消 Milestone route；自动关闭/归档 Decision Map。
- 把 promotion 直接送入 P2、更新 active Iteration、绕过 ACK 或替代现有 P1→P5。
- 多 active Iteration、并行 P4、R5 router/dogfood、外部 tracker。
- 为既有 iteration-intake 增加超出其当前保证的跨进程强原子事务。

## Acceptance Checklist

- [ ] AC1: Source slice：request 显式给出规范 `map_id` 与至少一个 root Decision；工具从 Map 真源确定性展开去重、稳定排序的传递依赖闭包。只有闭包内全部 Decision 为 `resolved` 且带 outcome/rationale 时才 eligible；Map 其余开放 Decision/Fog 不阻塞，resolution evidence 允许为空。
- [ ] AC2: 单入口显式目标：promotion request 只有共同 envelope 与 `route-reference`、`iteration-start` 两个封闭 target；工具不推断清晰度、体量或目标，不自动串联两个 adapter。`inspect`、`plan`、`verify` 零写，只有用户显式提交保存的 plan 给 `apply` 才能写入。
- [ ] AC3: Route reference：`route-reference` 只接受当前 active Milestone 中已存在、状态为 `planned` 且尚未绑定 ITER 的路线；成功后只新增不可变 receipt，不修改 Decision Map、Decision Work、Milestone 路线表或 Iteration 台账。`inspect` 通过扫描 receipts 派生 route→Decision 引用。
- [ ] AC4: Iteration start：`iteration-start` 在没有 active Iteration 时调用现有 iteration-intake，从 P1 创建完整活产物和台账。存在 active Milestone 时必须指向其中一个可用 planned route；无 active Milestone 时才允许 standalone。它不得创建路线、不得直接进入 P2，并须把 promotion source/receipt 引用写入新 `CONCEPT.md`。
- [ ] AC5: Admission 拒绝：不存在/损坏/符号链接 Map、未知或未 resolved Decision、空 roots、错误 Milestone/route 状态、已有 active Iteration、active Milestone 下请求 standalone、未知字段/枚举或不规范 ID 均 fail-closed，且失败前后项目状态字节不变。
- [ ] AC6: Receipt 与幂等：receipt 以稳定 `promotion_id` 保存规范 request digest、roots/closure、source slice digest、观察到的 Map revision、target、result 与时间。相同 ID+相同 request 重试返回原结果且不重复写入；相同 ID+不同 request 拒绝；receipt 不复制三方完整状态、不反写 Map。
- [ ] AC7: Stale 与并发：plan 绑定 source slice digest 和相关 target 状态摘要；所选 slice 或目标状态变化后 apply 拒绝，无部分写入。并发 apply 至多一个提交成功；对无关 Map 内容的变化不误判 source slice stale。
- [ ] AC8: 事务与恢复：`route-reference` 的单 receipt 发布使用 staging/atomic rename；`iteration-start` 复用 iteration-intake 的回滚边界并在 callback 内写 Source References/receipt。故障注入证明 callback 或同步失败时 `.ai` 整体恢复；无法保证的进程强杀窗口被 `verify` 检出并给出确定性错误，不静默创建第二个 Iteration。
- [ ] AC9: 生命周期所有权：promotion 不关闭、归档或冻结 Map，不更新 active Iteration。文档明确 Map close 与 promotion 正交；P2 冻结后的新结论按既有 amend→重新 ACK 或扩张→未来 route/Iteration 分流，Decision Map 始终只是理由、证据与历史参考。
- [ ] AC10: 集成与零回归：部署清单、生命周期/里程碑/迭代/Explore/Decision Map/Decision Work 文档、Butler README/能力索引和 CI 均能发现新模块；新测试与仓库完整 CI 通过，R1–R3 的边界、状态机和 helper 合同保持不变。

## Verification Method

- AC1：fixture 覆盖单 root、多 root、共享依赖、传递依赖、闭包未 resolved、无关开放项与空 evidence；断言 closure/source digest。
- AC2：CLI contract 测试四动作写集、未知 target/字段和 plan→apply 门；对零写动作执行前后目录树 hash 对比。
- AC3：active milestone fixture 覆盖有效 planned route、缺失/active/closed/abandoned/已绑定路线；成功后对 Map、Milestone、Iteration 文件做 hash 不变检查，并用 inspect 查询反向引用。
- AC4：分别验证 milestone route 与 standalone fixture；断言 iteration-intake 产物、P1 状态、route 绑定、CONCEPT Source References 和 receipt，并验证非法组合拒绝。
- AC5：参数化负例测试断言错误码/错误类型及项目树 hash 不变；symlink、损坏 JSON 与未知字段单独覆盖。
- AC6：同请求重放、ID 冲突、receipt schema/内容与只读校验；断言只有一个 receipt 且无 Map 回写。
- AC7：保存 plan 后分别改变 source/target，验证 stale 拒绝；并发进程竞争断言单一提交；仅改变非 closure Decision 时验证仍可 apply。
- AC8：在 callback、receipt 发布和 state sync 位置注入异常，验证 rollback/atomic publish；构造 receipt/iteration 不一致状态，验证 `verify` fail-closed 且不自动修复。
- AC9：文档契约审查与回归测试，确认不存在 close-map、active-iteration update 或跳 P1 的写路径，并与 iteration-schema 的 amend/escalate 规则交叉核对。
- AC10：运行新模块测试、R2/R3 回归、workflow/部署契约测试、文档链接检查和仓库完整 CI；保存 P5 evidence records。

## External References

- N/A

## Open Questions / Risks

- 进程被强制终止时，iteration-intake 本身不承诺跨多文件 crash atomicity；本迭代只要求检测不一致并安全停机，不在 R4 内重写整个 intake 事务引擎。
- 同一个 source slice 可被用户显式引用到多个 route；这是允许的复用，每次绑定使用不同 `promotion_id`，而不是由系统自动去重成唯一归属。
