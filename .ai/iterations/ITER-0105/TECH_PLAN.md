<!-- butler-artifact-template: 1.0.0 artifact=tech_plan -->
# TECH_PLAN — ITER-0105

方案状态: pass

## Design Decisions

- 新增 `tools/decision-promotion/` 深模块：`engine.py` 持有 schema、资格计算、receipt 存储、锁和两个 adapter；`decision_promotion.py` 只负责严格 JSON CLI；`README.md` 是调用与数据合同真源；`tests/` 覆盖引擎、CLI、并发和故障注入。
- 四动作保持与 R2/R3 相同心智模型：
  - `inspect --project-root [--promotion-id|--milestone-id --route-id]` 扫描不可变 receipts 并派生引用；
  - `plan --project-root --spec request.json` 校验 request、source slice 和 target，输出带 source/target digest 的可保存 plan；
  - `apply --project-root --plan plan.json` 在全局 promotion 锁内重新校验并提交；
  - `verify --project-root [--promotion-id]` 校验目录、receipt、source slice 与 target 交接一致性，零写且不自动修复。
- Request v1 使用严格封闭 schema：
  - common：`schema_version: 1`、稳定的 `promotion_id: PROM-NNNN`、`source: {map_id, decision_ids}`；
  - `route-reference` target：`{kind, milestone_id, route_id}`；
  - `iteration-start` target：`{kind, milestone_id, route_id, intake}`，其中 `milestone_id/route_id` 同为字符串或同为 `null`；`intake` 只含 title、summary、model_recommendations、open_questions、in_scope、out_of_scope，confirmed_decisions 由 source closure 的 resolution 投影生成，避免双写冲突。
- Source projector 通过唯一命名的动态 module loader 调用 `tools/decision-map/engine.py::inspect`，复用 R2 的完整状态验证，不复制 Map parser。它对显式 roots 做 DFS/BFS 传递闭包、按 Decision 数字序稳定排序，并以 canonical JSON 计算 `source_slice_sha256`；digest 只覆盖 map_id、roots 与闭包中 question/depends_on/resolution，不覆盖无关 Map 状态。
- Target validator 只读取现有复合台账和 `.ai/MILESTONE.md`：`route-reference` 要求目标是当前 active Milestone 的 `planned / 实际 ITER=—` 路线；`iteration-start` 额外要求没有 active Iteration。active Milestone 存在时 target 必须准确指向该 Milestone 的 planned route；没有 active Milestone 时两个 ID 必须为 `null`，形成 standalone。
- 不增加 Milestone route 写 API。`route-reference` 的交付只是 `.ai/decision-promotions/<PROM-ID>/receipt.json`；路线到 Decision 的视图由 inspect 扫描派生。`iteration-start` 则把 route 交给现有 intake，由 intake 独占路线状态和迭代号写入。
- Receipt v1 固定记录 schema、promotion/request/source digest、roots/closure、observed Map revision、target、result、created_at；不保存完整 Map/Milestone/Iteration 快照。相同 ID+digest 在任何后续状态下返回原 receipt；相同 ID+不同 digest 冲突。
- `route-reference` 在同目录 staging 写 canonical JSON、fsync 后原子 rename。`iteration-start` 通过唯一命名 loader 调用 `iteration-intake/intake.py::apply`，在其 `after_write` callback 中向新 CONCEPT 的 `Current Understanding` 注入单条 Source References，并发布 receipt；callback/sync 异常由 intake 的 `.ai` snapshot 整体回滚。
- 写锁为项目级 `.ai/.decision-promotion.lock`，非阻塞、拒绝 symlink；锁顺序固定为 promotion → iteration-intake，任何路径不得反向获取。全局串行化是为了保护跨 promotion ID 的 single-active-iteration 不变量；零写动作不取锁、不创建目录。
- Plan 同时固定 `request_sha256`、`source_slice_sha256` 与 `target_sha256`。apply 在锁内重算：source/target 真变化即 stale；Map 中 closure 外变化不会使计划失效。已存在同请求 receipt 的幂等恢复优先于重新要求目标仍为 planned。
- `verify` 对 receipt 做 schema/digest/source 复算，并核对目标存在性：route 后续从 planned 演进到 active/closed/abandoned 不使历史 receipt 失效；iteration-start receipt 必须能在复合迭代台账找到目标 ITER。若 active Iteration/CONCEPT 已产生但 receipt 缺失，报告 `incomplete_promotion`，不猜测、不补写、不再开新号。
- 文档只在既有所有权真源增加接线说明；`scripts/verify-dual-host.sh` 增加新单测发现与 compileall，`scripts/test-workflow-registry.py` 增加边界词断言。该模块不是新用户 workflow，不加入 registry 或新增 skill/命令入口。

### Plan Admission

- **AC Coverage**：source projector→AC1；严格 request/四动作→AC2；只读 route adapter→AC3；intake adapter→AC4；strict validator→AC5；receipt store→AC6；digest+global lock→AC7；atomic publish/intake callback/verify→AC8；文档边界→AC9；部署与 CI 接线→AC10。无未映射 AC。
- **Assumptions**：R2 resolved Decision 不可再编辑，已由 engine invariant 保证；Milestone 路线表保持当前四列结构，解析测试会锁住；iteration-intake 的 `after_write` 和 rollback 是可复用的公开 Python 边界，故障注入将验证这一假设。
- **Alternatives / Trade-offs**：放弃“promotion 自动创建 route 并立刻开 Iteration”，因为它把两个用户决定合并并夺取 Milestone 所有权；放弃把 Decision refs 写回 `.ai/MILESTONE.md`，因为会形成可漂移索引；放弃钉整张 Map revision，因为无关探索会造成伪 stale。选择 receipt 扫描牺牲少量读取成本，换取单写源和局部稳定性。
- **Failure Modes**：坏/缺 source、未收敛闭包、非法 target、active 冲突、receipt ID 冲突、stale plan、并发 apply、symlink、callback/sync 异常、进程强杀留下不完整交接均有显式拒绝或检测路径；无自动修复路径。
- **Impact / Scope Challenge**：MVP 不做 route mutation、不做 active Iteration update、不建索引、不改 R2/R3 schema，也不新增用户入口；实现集中在一个新工具和少量接线文档，是满足 AC 的最小影响面。
- **Verification Blind Spots**：机器测试可以证明文件状态、锁、回滚和契约，不能证明用户选择的业务方向正确；进程在现有 intake 多文件写入中被 SIGKILL 的绝对原子性不在本迭代保证内，只能由 verify 检出不一致并停机。
- **Verdict**：`pass`；2026-08-02 经用户独立 ACK，当前无已知 Must Fix，允许进入 P4。

## Failure Paths

- request JSON 不是对象、重复键、未知字段、ID 非规范、roots 为空/重复：exit 2，零写。
- Map/Decision 不存在、Map 状态损坏或 symlink、闭包中存在非 resolved：exit 1/2 按 conflict/invalid 分流，零写。
- 当前 Milestone/Iteration 与 target 不兼容、路线不存在或非 planned/unbound：plan/apply 拒绝，零写。
- plan digest 被改写、source slice 或 target 在 plan 后变化：`stale_plan`，零写；closure 外 Map 变化不触发。
- promotion lock 已占用：`promotion_busy`，不等待、不写；锁释放后可用同 plan 重试，但仍需重新通过 stale 检查。
- receipt 已存在：相同 request 返回首次 result 并标记 idempotent；不同 request 返回 `promotion_id_conflict`。
- route receipt staging/write/fsync/rename 失败：清理 staging，正式 receipt 不出现；verify 不把临时文件当状态。
- intake callback 或 handoff/state sync 失败：沿现有 intake exception path 恢复整个 `.ai` snapshot，receipt、台账与活产物共同消失。
- 进程强杀形成 active Iteration 但无 receipt：verify 报 `incomplete_promotion`；后续 apply 因 active Iteration 拒绝，禁止静默分配第二个号，交由既有 abandon/recovery 流程处理。

## Test Strategy

- T1：先建立 engine/CLI test harness、严格 request/plan/receipt fixtures 和项目树 hash helper → AC2、AC5、AC6。
- T2：实现 source projector 与 closure digest；覆盖共享/传递依赖、未 resolved、无关 Map 变化、空 evidence → AC1、AC7。
- T3：实现 route parser/validator、receipt 原子发布、inspect/verify；覆盖路线全状态、只写 receipt、幂等与 symlink → AC3、AC5、AC6、AC8。
- T4：实现 iteration adapter 与全局锁；用真实 iteration-intake fixture 覆盖 standalone/milestone、CONCEPT 引用、并发开工、callback/sync rollback 和 incomplete 检测 → AC4、AC7、AC8。
- T5：更新生命周期、schema、Explore/R2/R3、部署、README、项目索引和 CI 接线；增加边界 contract tests → AC9、AC10。
- T6：运行 `python3 -m unittest discover -s tools/decision-promotion/tests`、R2/R3/intake 回归、`scripts/test-workflow-registry.py`、文档/产物检查与 `scripts/verify-ci.sh`；P5 逐 AC 保存 verification-evidence records → AC1–AC10。

## References Compliance

- 外部参考资料：N/A。本迭代是对已确认 `.ai/CONCEPT.md` 与冻结 `.ai/AC_LIST.md` 的项目内实现。
- 内部合同依赖：`tools/decision-map/README.md`、`tools/iteration-intake/intake.py`、`Coder/20_Workflow_Lifecycle/{milestone-schema,iteration-schema,lifecycle}.md`；实现只调用其既有所有权边界，不复制状态真源。
