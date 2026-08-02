<!-- butler-artifact-template: 1.0.0 artifact=concept -->
# CONCEPT — ITER-0105 · Decision Map 到 Milestone / Iteration 的确定性交接

## Current Understanding

- R4 要解决的是“已由用户选定的 Decision slice 如何安全进入交付系统”，不是再次判断需求大小、清晰度或是否应该 Explore。
- Decision Map 在 promotion 前拥有探索状态；promotion 后只作为 `CONCEPT` 的理由、已确认决定和 evidence pointer 来源。Milestone 继续拥有版本路线，Iteration 继续独占 P1→P5、AC 冻结和交付状态。
- 不要求整张 Map 收敛。用户显式选择一个或多个 resolved Decision 作为 slice roots；系统自动展开其传递依赖闭包。闭包全部 resolved 即满足“决策已定”的机械条件，Map 中其他无关 Decision/Fog 可以继续开放。
- eligibility 不是新的生命周期状态，而是 `plan` 时重算的纯谓词：来源 slice 有效、目标容器兼容、当前无 active Iteration、必要的 Milestone route 已存在。模型无权把“看起来够清晰”写成 admission 结果。
- promotion 使用一个共同 request envelope、两个显式 target adapter：
  - `route-reference`：把 slice 引用绑定到一个**已经存在**的 planned Milestone route，只写不可变 promotion receipt；路线的创建、排序和取消仍走 Milestone 工作流。
  - `iteration-start`：把 slice 结晶为 iteration-intake spec，并调用现有 intake 从 P1 开启 Iteration；存在 active Milestone 时必须指定其 planned route，不存在 active Milestone 时才允许 standalone Iteration。
- 两个 adapter 都不得自动互相串联。`route-reference` 不开 Iteration；`iteration-start` 不发明新路线。用户选择目标并显式执行 `apply`，就是唯一 promotion 权限边界。
- 每次 promotion 以稳定 `promotion_id` 和规范 request digest 保证幂等；receipt 固定记录 source slice digest、Map/Decision 引用、目标 ID、结果与时间，不复制三方完整状态，也不反写 Decision Map。
- source slice digest 只覆盖所选 roots 及其依赖闭包，不钉死整张 Map revision；因此无关探索可以继续，而已经 resolved 且不可修改的来源仍保持稳定可验。
- Decision resolution 的 outcome 与 rationale 必须存在；evidence pointer 可以为空，因为有些决定本身是用户取舍而非外部事实。是否需要更强证据由后续 P2 AC 决定，promotion 不冒充证据质量裁判。
- Map 的 close 与 promotion 正交：promotion 不自动关闭、归档或冻结 Map；Map 按 R2 规则在自身全部 Decision/Fog 收口后关闭，receipt 永久保留反向追溯。
- P2 冻结后，新的 Map 结论不能更新或覆盖当前 Iteration。未突破原影响面时走现有 amend→重新 ACK；扩大影响面时进入未来 route/Iteration。promotion 工具本身只创建引用或开启 P1，不提供“更新 active Iteration”动作。

## Scope

- 新增项目内 `decision-promotion` 驻留模块，暴露 `inspect / plan / apply / verify`，封装 source closure、eligibility、target adapter、幂等 receipt 和失败恢复。
- 定义共同 promotion request，以及 `route-reference`、`iteration-start` 两个封闭 target；未知 target fail-closed。
- `route-reference` 只接受当前 active Milestone 中已存在、尚未绑定 Iteration 的 planned route；通过扫描 receipts 派生 route→Decision 引用，不建立第二份可写索引。
- `iteration-start` 复用 `iteration-intake.apply(..., after_write=...)` 的事务边界，在同一回滚域内生成 P1 产物、Milestone/Iteration 台账变化、Source References 与 promotion receipt。
- 对 source slice、active 状态、route 状态、request/plan digest、重复 ID、stale target、部分失败和幂等重试建立测试。
- 更新 lifecycle、milestone/iteration schema、Explore/Decision Map/Decision Work 文档、部署清单、CI 和项目长期知识。
- 不实现路线自动创建、自动选择 target、自动关闭 Map、active Iteration 的内容更新、多 active Iteration、R5 router/dogfood 或外部 tracker。

## Open Questions / Risks

- **待用户确认的 P1 方案**：采用“共同 request + 两个显式 adapter”，并把 route creation 留在 Milestone 所有权内；确认后再进入 P2 编写冻结 AC。
- `route-reference` 只新增 receipt，不修改 `.ai/MILESTONE.md`，所以人读路线图时需要通过 `decision-promotion inspect` 查看来源；本迭代应在文档中明确这一可发现性，不为方便阅读复制可漂移索引。
- `iteration-start` 可以复用现有 intake 的 Python transaction callback；需要用故障注入测试证明 callback 或同步失败时，迭代台账、活产物和 receipt 会一起回滚。
- 同一个 resolved slice 可以被显式引用到多个未来 route；这属于用户可见复用，不应机械禁止。每次绑定都有独立 receipt，重复同一 promotion request 则幂等返回原 receipt。
