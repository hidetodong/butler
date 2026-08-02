---
状态: ack-frozen
ACK 日期: 2026-08-01
---
<!-- butler-artifact-template: 1.0.0 artifact=acceptance -->
# AC_LIST — ITER-0104

## Goal

- 为 Butler 建立一个不依赖 helper 临场改状态的 Decision Work Module：四类决策工作共享严格任务/结果合同，Research 可在显式选定的独立 Frontier 上受控并行，任何候选结论都必须由协调器通过 R2 Module 显式吸收后才能解决 Decision。

## In Scope

- `.ai/decision-work/` 下按 Map / Decision / Attempt 隔离的不可变 `task.json`、可选 `result.json`、canonical identity 与 evidence pointer。
- Task Packet、Result Envelope、四种 work type discriminator、candidate/needs_input/failed/cancelled outcome 与派生 attempt 状态。
- `inspect / plan / apply / verify` 四动作 Interface，以及 prepare、record、absorb 等内部 operation spec。
- Research 显式 batch、`max_parallel` 安全阈值、helper 零项目写权限、协调器串行记录/吸收。
- claim 到期/替换、stale Map revision、重复/乱序/迟到 result、原子发布、幂等与跨会话恢复。
- 帮手名册、Ideation/驻留工具指针、专项测试与完整 CI 接线。

## Out of Scope

- 不实现 R4 的 Milestone 路线引用、Iteration Admission、promotion receipt、P2 冻结后变更分流或 Decision Map 归档。
- 不新增用户入口或 workflow registry ID，不按模型置信度、需求清晰度或体量自动选 Decision、决定并行度、吸收结论。
- 不把 prototype、grilling、task 强制后台化，不替代真实 HITL 对话，也不把 task 扩张为最终交付实现。
- 不实现多 active Iteration、并行 P4、跨主机/网络文件系统调度、外部 tracker 或通用长期 job scheduler。

## Acceptance Checklist

- [ ] AC1: Decision Work 使用 `.ai/decision-work/DMAP-NNNN/DEC-NNNN/ATT-NNNN/` 作为 sidecar；每个 attempt 只有不可变 canonical `task.json` 和至多一个不可变 canonical `result.json`，不修改 R2 state schema、不在 Decision Map 目录写旁文件，也不建立第二份 mutable job status 或全局可写索引。
- [ ] AC2: Module 对调用者仍只暴露 `inspect / plan / apply / verify` 四个动作；`inspect`、`plan`、`verify` 保证零写，prepare/record/absorb 只作为严格 operation spec 进入 plan/apply，未知字段、枚举、schema、ID 或路径均 fail-closed。
- [ ] AC3: Task Packet 必须绑定 Map、Decision、Attempt、work type、Decision question、已确认 context、constraints、expected output、R2 Map base revision/digest、claim operation ID、claim owner/token digest 与到期时间，并可选绑定一个 predecessor attempt；不得保存原始对话、明文 Claim token、项目写权限或宿主专用 agent 指令。
- [ ] AC4: 四种 work type 是封闭枚举且职责可机械区分：research 要求 findings、source/evidence 与 uncertainties；prototype 的 artifact/observations 在缺 human evaluation 时只能返回 needs_input；grilling 缺真实 human answers 或出现 helper 自问自答时只能返回 needs_input/拒绝 candidate；task 只允许记录解除决策阻塞的前置动作/evidence，不得声明最终交付已实现。
- [ ] AC5: Result Envelope 必须绑定原 Task digest 和 Attempt identity，并且只接受 `candidate / needs_input / failed / cancelled`；candidate 按 work type 满足对应字段，needs_input 带明确问题或待评价 artifact，failed 带稳定错误摘要，cancelled 带原因。result 一经原子发布不得覆盖；相同 operation/request 可幂等重试，不同内容复用 ID 或重复提交必须拒绝且字节不变。needs_input 的接续只能新建绑定 predecessor 的 attempt。
- [ ] AC6: 调用方必须从 inspect 返回的 Frontier 显式选择 Decision ID 并逐项通过 R2 claim；prepare 校验对应 claim receipt、Decision 仍 open、依赖全 resolved 且 owner/token digest/有效期与当前 Claim 匹配，不要求已领取 Decision 仍出现在当前 Frontier。不存在“自动取第一张”或基于模型置信度选票；`max_parallel` 合法范围 `1..8`、省略时为 `1`。
- [ ] AC7: 只有 `research` 允许一个 batch 包含多个互不重复、已分别完成上述 claim 的 work-ready Decision；prototype、grilling、task 的 batch size 必须为 1。Research batch 中任一 Decision/Claim/依赖非法时整批 plan/apply 失败且 sidecar 字节不变。
- [ ] AC8: helper 只接收 host-neutral Task Packet，在隔离临时目录工作并返回有界 Result Envelope；它不接收明文 Claim token、不写目标项目或 Decision Map。Host 不支持 fresh-context/并行时必须串行降级并如实标注 execution mode，不能伪称独立或并行。
- [ ] AC9: record 允许合法迟到结果作为不可变参考落盘，但不改变 Map；无 result 且 Claim 到期时 attempt 状态由查询派生为 expired，needs_input/failed/cancelled/late/stale 均不得触发自动 retry、自动 re-claim 或自动 resolve。
- [ ] AC10: absorb 必须由协调器显式请求，并机械校验 task/result 哈希与绑定、result 为 candidate、Decision 仍 open、依赖仍满足、当前 owner/token 有效且 R2 base 未 stale；成功时只通过 R2 Decision Map Module 提交一次 resolve，evidence 使用可重定位的 sidecar path + SHA-256 pointer。
- [ ] AC11: helper 完成、result 落盘或 inspect 显示 absorbable 都不等于 Decision resolved；无 absorb operation 时 R2 state 必须字节不变。absorb 遇到过期/替换 Claim、已解决/废弃 Decision、stale revision、needs_input/失败/取消 result 或 result 被篡改时必须 fail-closed；同一 absorb operation 的合法重试由 R2 receipt 幂等返回。
- [ ] AC12: 新进程只凭 R2 Map 与 Decision Work sidecar 即可恢复 attempt、execution mode、result、timeliness 与 absorbability；verify 能报告 symlink、非 canonical JSON、意外文件、缺失/篡改 task/result、悬空 Map/Decision 和跨绑定错误，且检查本身零写。
- [ ] AC13: 帮手名册和 Explore 权威文档明确“并行的是 Research 求证，不是 Map 写入”，并让四类工作合同回指单一 Module 真源；R1 单入口/opt-in、R2 四动作状态所有权、R4 promotion 边界、Router + 13 workflows 均保持不变。
- [ ] AC14: 自动测试覆盖四类 schema、Research batch/非 Research 单项、显式选择、零写动作、原子/幂等提交、真实并发、失败/取消/迟到/过期/stale/篡改、跨进程恢复和 absorb 对 R2 的唯一写入；专项测试、workflow/registry 合同、Markdown 链接、`git diff --check` 与完整 `scripts/verify-ci.sh` 全部通过。

## Verification Method

- AC1: 在临时项目准备多个 attempt，检查 sidecar 目录与 canonical bytes；对 R2 Map 目录和 state schema 做前后快照，静态/动态确认无旁文件、全局索引或 mutable status。
- AC2: Interface 合同测试枚举仅四动作；对 inspect/plan/verify 前后做完整树 digest，并参数化提交未知字段、枚举、schema、identity 与 symlink 路径。
- AC3: 生成 Task Packet 并逐字段断言绑定、base、claim digest/expiry 与上下文；扫描 JSON 确认不含原始 transcript、明文 token、绝对项目写路径或宿主 prompt。
- AC4: 为四个 discriminator 各跑合法/非法 fixture；特别验证 prototype 缺 human evaluation、grilling 缺 human answers 或声称 self-answered 时只能 needs_input/不能 candidate，task 声称最终实现时拒绝。
- AC5: 参数化 candidate/needs_input/failed/cancelled 及 predecessor 接续，比较首次 record、相同请求重试、不同内容重复和故障注入前后的 result bytes 与目录残留。
- AC6: 用显式 Frontier→claim→prepare 链覆盖 claim receipt 缺失、非 Frontier claim 被 R2 拒绝、prepare 时依赖变化、过期/替换 claim、默认并行度及 `0/1/8/9` 边界，断言已 Claim Decision 不需仍出现在 Frontier，且不存在隐式选票输出。
- AC7: 分别准备 2–8 个合法 Research attempt，以及多项 prototype/grilling/task 和含单一坏项的 Research batch；比较失败前后全树 digest。
- AC8: 用 fake host Adapter 记录 helper 输入、cwd 与 execution mode；断言输入无 token、工作目录隔离、无项目写入，并覆盖 parallel capability false 的串行诚实回声。
- AC9: 用可注入 UTC clock 覆盖 pending、expired、on-time、late、needs_input、failed、cancelled；逐场景比较 R2 state revision/bytes，确认 record/inspect 不触发 lifecycle 写入。
- AC10: 对合法 candidate 执行 absorb，检查 R2 resolution evidence pointer 的相对路径与 digest、revision 只增一次，并以 spy/fake 断言唯一写 seam 是 Decision Map Module。
- AC11: 在无 absorb、claim 过期/替换、Decision terminal、Map stale、needs_input/坏 result 与重复 absorb 场景比较 Map bytes/revision/receipt，确认成功幂等、失败零写。
- AC12: 进程 A prepare/record，进程 B 冷启动 inspect/verify/absorb；再注入 symlink、非 canonical、意外文件、缺失/篡改与跨绑定 fixture，检查稳定机器错误码和零写。
- AC13: 扩展 workflow/驻留工具合同测试，断言无新增 registry ID/入口、Router 仍为 13 workflows、Ideation/Agents 文档只回指单一合同且 promotion 仍归 R4。
- AC14: 用 verification evidence runner 归档专项、合同和完整 CI 记录，逐项映射 AC1–AC13，并运行 artifact contract、state audit、链接检查和 `git diff --check`。

## External References

- N/A：本轮继承 MILE-0014 R1/R2 的仓内权威合同；前期 Wayfinder 调研只作为设计背景，不作为逐字外部规格。

## Open Questions / Risks

- `max_parallel=8` 是资源安全硬上限，不表示系统已能判断需求大小；实际批次仍由调用方显式选择，默认 1。
- Claim token digest 只用于绑定与泄漏规避，不是权限认证；R2 的本地协调安全口径保持不变。
- 不可变 sidecar 会随 attempt 数增长；R3 不删除或压缩，R4 再定义随 Map promotion/归档的生命周期。
- Host Adapter 的真实并行与 fresh-context 能力无法由核心 Module 创造；降级路径必须可观察、可验证。
