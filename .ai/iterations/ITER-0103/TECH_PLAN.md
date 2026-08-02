<!-- butler-artifact-template: 1.0.0 artifact=tech_plan -->
# TECH_PLAN — ITER-0103

方案状态: pass
方案审查日期: 2026-08-01
方案审查方式: user-ack

## Design Decisions

### Goal

- 通过一个本地优先、严格校验的 Decision Map Module 覆盖 AC1–AC11：调用者只需理解 `inspect / plan / apply / verify` Interface，依赖 DAG、Frontier、lease、幂等、锁和原子恢复均由 Module 的 Implementation 吸收。

### Files / Modules to Change

- `tools/decision-map/engine.py` — **Decision Map 深 Module**；唯一拥有路径解析、严格 state 合同、纯状态 reducer、Frontier 计算、lease 语义、operation receipt、锁和原子发布。对 Python 调用者只暴露 `inspect / plan / apply / verify`。
- `tools/decision-map/decision_map.py` — **CLI Adapter**；把四个同名动作、显式 `--project-root`、Map ID 和 JSON 文件转换为 Module Interface 调用，stdout 始终输出一个 JSON 对象，不复制状态算法。
- `tools/decision-map/README.md` — **工具合同真源**；说明目录、state v1、operation spec、四动作、退出码、并发保证和非保证项。
- `tools/decision-map/tests/test_engine.py` — 通过四动作 Interface 验证状态生命周期、严格校验、Frontier、lease、Fog、幂等与冷启动。
- `tools/decision-map/tests/test_storage.py` — 用临时项目、并发子进程和故障注入验证锁、stale revision、原子发布、symlink/path 防护与失败零半状态。
- `tools/decision-map/tests/test_cli.py` — 以 subprocess 验证四动作 JSON Interface、退出码、plan 零写与跨进程恢复。
- `Coder/50_Extension_Ideation/ideation-engine.md` — 把新 Map 的结构化持久状态指向 Decision Map 工具，同时保留一个 Explore 入口、用户 opt-in 和 promotion 后参考地位；不在规则文档复制 state schema。
- `Coder/20_Workflow_Lifecycle/mcv-deployment.md`、`Coder/README.md`、`README.md` — 注册 Decision Map 为 Butler 驻留工具并给出真源指针，不把工具拷进目标项目。
- `scripts/test-workflow-registry.py` — 在 R1 现有 Explore 合同测试中增加“仍无 Explore workflow、结构化状态只指向驻留工具、不得自动 promotion”的静态断言。
- `scripts/verify-dual-host.sh` — 把新工具的三组测试和 Python compileall 纳入现有双宿主/完整 CI 链，不新建平行验证入口。
- `.ai/01_CHANGELOG.md` 与项目知识 topic — P4/P5 记录并折叠本迭代真实 delta；`CONTEXT.md` 已在 P2 固定领域词汇，不承载实现合同。

### Interface / Contract

- CLI 只有四个动作：
  - `inspect --project-root <root> [--map-id DMAP-NNNN]`：列出 Map 或返回指定 Map 的持久状态、有效 claim 和派生 Frontier，全程零写。
  - `plan --project-root <root> --map-id DMAP-NNNN --spec <operation.json>`：严格读取当前状态，规范化一个 operation，返回 base revision、base SHA-256、request SHA-256 与 effect preview，全程零写。
  - `apply --project-root <root> --plan <plan.json>`：在 Map 锁内重新验证 plan 与当前状态，提交至多一次 revision；成功、冲突和坏状态均返回机器码。
  - `verify --project-root <root> [--map-id DMAP-NNNN]`：校验目录、规范 JSON、state 合同、DAG、receipt 与派生不变量，全程零写。
- Python Interface 同样只有 `inspect(project_root, map_id, now)`、`plan(project_root, map_id, spec, now)`、`apply(project_root, planned, now)`、`verify(project_root, map_id, now)` 四个入口；CLI 是一个 Adapter，测试与未来 R3 coordinator 复用同一 seam。
- operation spec 顶层固定为 `schema_version`、`operation_id`、`operation`。`operation.kind` 的 v1 封闭集合为：`create_map`、`add_decision`、`add_fog`、`link_dependency`、`unlink_dependency`、`claim`、`renew`、`release`、`resolve`、`abandon`、`graduate_fog`、`dismiss_fog`、`close_map`。未知字段和未知 kind 一律拒绝。
- `create_map` 必须提供显式规范 `DMAP-NNNN`、非空 title 和 destination；Decision/Fog 也使用显式 `DEC-NNNN` / `FOG-NNNN`。R2 不自动分配身份，因此无需全局写索引，也不会把“下一号”交给模型猜测。
- `resolve` 写入 outcome、rationale 和可选 evidence references；`abandon` / `dismiss_fog` 写入 reason；`graduate_fog` 一次携带一个或多个完整 Decision 定义。R1 的决定、开放问题和参考依据均有落点，但这些内容不是 P2 AC。
- plan payload 是可保存、可审计的 JSON；`apply` 不信任其内容，必须重新规范化 operation、重算 request digest，并在锁内校验 base revision/digest。CLI 成功退出 `0`，安全冲突退出 `1`，坏输入、损坏状态或 I/O 失败退出 `2`。

### State / Boundary

- 每张 Map 唯一可写真源是 `.ai/decision-maps/DMAP-NNNN/state.json`。state v1 顶层含 schema version、map identity、revision、status、title、destination、UTC created/updated、以 ID 为键的 decisions/fog，以及 `applied_operations` receipt 集合。
- revision 在 create 成功后为 `1`，以后每个首次成功的 operation 恰好 `+1`。state 使用 UTF-8、排序键、固定缩进和尾换行的 canonical JSON；verify 拒绝语义相同但非规范的手改文件，避免 digest 双义。
- Decision 保存 question、`open / resolved / abandoned`、`depends_on`、claim 与 resolution/abandon 记录；Fog 保存 description、`open / graduated / dismissed` 和 graduation/dismiss 记录。Map 只取 `open / closed`。
- Frontier 永不写入 state：`open Decision ∩ dependencies all resolved ∩ no effective claim`。`now >= expires_at` 即 lease 已过期；过期 claim 可保留为审计字节，但在 inspect、Frontier 和全部转换中按不存在处理，新 claim 可原子覆盖它。
- claim 只接受 Frontier Decision，使用调用方 owner、Module 在 apply 时生成的高熵 token、claimed_at 和 expires_at；`lease_seconds` 为 `1..86400`。renew 必须 owner/token 匹配且未过期，新到期时间从 `max(now, old expires_at)` 延长；release 和已领取 resolve 同样要求匹配。无有效 claim 的 Frontier Decision 可直接 resolve。
- active claim 下不能 abandon；先 release 或等待到期。存在 open dependent 时不能 abandon dependency。link/unlink 只修改 open Decision 的同 Map 边，并在候选状态上重跑无环、悬空和 abandoned dependency 校验。
- Fog 只有 open 时可 graduate/dismiss；graduation 在同一次 reducer 中先构造全部新 Decision 与依赖，再整图验证，通过后一次提交。Map 仅在没有 open Decision/Fog 时可 close；closed 后所有写 operation 拒绝。
- `applied_operations[operation_id]` 保存 request digest、committed revision 与调用方重试所需的 result（含 claim token）。锁内先查 receipt：digest 相同则返回原结果且不增 revision，digest 不同则冲突；因此“replace 已成功但输出丢失”仍可安全重试。
- Map 写锁位于 `.ai/.decision-map-locks/DMAP-NNNN.lock`，是协调物而非状态真源；使用 macOS/Linux 的 `fcntl.flock(LOCK_EX|LOCK_NB)`。读取依靠单文件/目录原子发布看到旧或新完整版本，不获取写锁。
- 新 Map 先在 `.ai/decision-maps/` 下隐藏 staging 目录写入并 fsync，再原子 rename 为规范 Map 目录；已有 Map 在同目录写临时 state、fsync、`os.replace`、再 fsync 目录。失败清理本次 staging/temp；verify 报告非规范目录、残留和 symlink，不跟随路径逃逸。
- 未来 R3 helper 只提交 operation spec，R4 promotion 只读取 Map 输出；两者不能绕过本 Module 直接写 state。R2 不修改 workflow registry、宿主入口、Milestone/Iteration 或四件套 admission。

### Alternatives / Trade-offs

- 采用“每 Map 单 state + operation receipt”，不采用“每 Decision 一文件 + 全局索引”：前者让一次 Fog graduation、DAG 校验和 lease 转换只有一个提交点，代价是同 Map 写入串行且 receipt 随历史增长；R2 优先正确性与可恢复性，不提前做 compaction。
- 采用四动作深 Module，不为 13 种 operation 各建 CLI 命令：operation 仍是封闭、可验证的数据，但调用者只学习一套 plan/apply 冲突语义，未来新增内部转换不扩大外部 Interface。
- 采用显式 Map/Decision/Fog ID，不做扫描后自动 `+1`：牺牲一点手工便利，避免无全局索引条件下的跨 Map 分号竞态；友好分号可由 R3 coordinator 先 inspect 再生成候选 ID，但最终仍由 create 锁和“目标不存在”校验裁决。
- 采用本地 `fcntl` lease 协调，不引入数据库或 GitHub assignee：符合 R2 本地优先与仓库 macOS/Linux 支持矩阵；跨主机和网络文件系统一致性留在范围外。
- 采用 Python 标准库严格校验，不新增运行时依赖或独立 JSON Schema validator：减少部署面；README + Implementation 是合同真源，行为测试从 Interface 验证，不维护会漂移的第二套校验算法。

### Execution Steps

- [ ] T1 建立 Decision Map Module 骨架、严格路径/ID/canonical JSON/state v1 校验和只读 inspect/verify → AC1、AC2、AC7、AC9
- [ ] T2 实现纯 reducer、DAG/Frontier、Decision/Fog 生命周期和 Map close 规则 → AC2、AC3、AC5、AC6
- [ ] T3 实现 claim/renew/release/resolve 的 UTC lease、token 和过期/stale worker 语义 → AC3、AC4
- [ ] T4 实现 plan payload、request/base digest、operation receipt 与幂等冲突裁决 → AC7、AC8
- [ ] T5 实现非阻塞文件锁、新 Map 目录发布、既有 state 原子替换、fsync/symlink 防护与故障清理 → AC1、AC8、AC9
- [ ] T6 实现四动作 CLI Adapter 和工具 README，通过 subprocess 固定 JSON/退出码/零写合同 → AC7、AC9
- [ ] T7 更新 Ideation、驻留工具与 Coder/root README 指针，扩展 R1 workflow 合同断言但不改变 registry/宿主入口 → AC10
- [ ] T8 将专项测试与 compileall 接入 `verify-dual-host.sh`，运行专项、registry、链接、diff 和完整 CI 并采集证据 → AC11

### Plan Admission

- **AC Coverage**：AC1 由 state v1、目录扫描和 atomic create 覆盖；AC2/AC5 由严格 validator + reducer + 全图 DAG 校验覆盖；AC3 由纯 Frontier 函数与注入 UTC 时钟覆盖；AC4 由 lease reducer 与 token receipt 覆盖；AC6 由单 reducer/单提交 graduation 覆盖；AC7 由四动作 Module/CLI seam 覆盖；AC8 由锁内 receipt-first、base 校验与 atomic replace 覆盖；AC9 由磁盘冷启动、canonical state 和 verify 覆盖；AC10 由只改规则指针和既有 registry 合同测试覆盖；AC11 由三组专项测试接入完整 CI 覆盖。
- **Assumptions**：Butler 当前支持矩阵是 macOS/Linux，可使用 `fcntl`、同文件系统 rename 与目录 fsync；用两平台 CI 验证。目标项目已有真实 `.ai/` 目录；路径 resolver 与 symlink 测试 fail-closed。UTC wall clock 可能被系统校时改变，本合同只以每次动作观察到的 UTC 判定，不声称提供跨主机单调时钟。
- **Alternatives / Trade-offs**：已比较单 state/多文件、四动作/多命令、显式 ID/自动分号、本地锁/远端协调；选择均直接服务原子性、Interface 深度和 R2 范围，没有新增未使用 Adapter。
- **Failure Modes**：坏 JSON、非 canonical state、未知字段、路径逃逸、symlink、孤立/环依赖、stale plan、锁竞争、operation ID 冲突、token 失效、replace/fsync 异常、create staging 残留和提交后 stdout 丢失都有明确拒绝或幂等恢复路径；任何错误下可见 state 始终是旧或新完整版本。
- **Impact / Scope Challenge**：最小完整落点是一个 Module、一个 CLI Adapter、三组测试和四处文档/CI 接线；不新增 workflow/skill/command，不触碰 promotion/admission，也不把 R3/R4/R5 偷塞进 R2。
- **Verification Blind Spots**：单机测试不能证明所有网络文件系统都正确实现 `flock`/rename，也不能把高熵 token提升为身份认证；这两项已明确 Out of Scope。长生命周期 receipt 的磁盘增长可测量但 R2 不做 compaction，避免破坏永久幂等。
- **Verdict**：`pass` — 冻结 AC 均有 Interface、Implementation 与验证映射，无已知 Must Fix；用户已完成 P3 ACK，可进入 P4。

## Failure Paths

- **双真源**：另写全局 index、Markdown 状态或 helper 直改 JSON会造成漂移；实现和文档只允许 state.json 写状态，测试扫描受管目录并拒绝第二投影。
- **读后写竞态**：plan 后状态已变化；apply 必须在锁内重读，除相同 receipt 的幂等重试外，base revision/digest 不同即 exit 1。
- **operation ID 复用**：相同 ID 不同 spec 若被当重试会返回错误结果；receipt 比 request digest，不同即冲突。
- **过期 worker 覆盖新结果**：旧 token 在 lease 到期并被重领后尝试 resolve；owner/token/expiry 三项任一不匹配即拒绝。
- **依赖漂移**：局部 link 或 abandon 使图成环/悬空/依赖 abandoned；每个候选状态提交前全图验证，不做局部乐观放行。
- **Fog 半毕业**：生成多个 Decision 时中途失败；纯 reducer 先构造候选，完整验证后才交给单文件发布。
- **create 半目录**：进程在 state 可见前失败；使用隐藏 staging + rename，普通扫描不会观察规范 DMAP 半目录，verify 对残留亮牌。
- **replace 后响应丢失**：调用方不知道是否成功；相同 operation ID 重试先命中 receipt 并返回原 result，不重复 token、expiry 或 revision。
- **手工/恶意路径**：伪造 ID、symlink 或非规范目录可能越界；路径只由 canonical ID 拼接，逐层拒绝 symlink/非普通文件，不接受调用方直接 state path。
- **范围回归**：文档接线被误写成自动选择 Explore/Map 或直接 promotion；R1 静态合同继续断言单入口、用户 opt-in、suggest 零写和 Iteration P1。

### Risks / Open Questions

- `applied_operations` 为永久幂等保留完整 receipt，会随 Map 操作数增长；这是 R2 有意选择。只有出现实测规模问题时再以带迁移的后续迭代设计 compaction，不能静默截断历史。
- `lease_seconds` v1 上限建议固定 86400 秒，避免“临时领取”被写成近似永久所有权；该上限属于本方案设计，随 P3 ACK 一并冻结。
- 当前没有阻断实现的开放问题；P3 已获用户 ACK。

## Test Strategy

- `python3 -m unittest discover -s tools/decision-map/tests`：覆盖 create/add/link/unlink、DAG、Frontier、claim/renew/release/resolve、stale token、Fog 原子 graduation、abandon/close、canonical/symlink、receipt 幂等、并发与故障注入（AC1–AC9、AC11）。
- CLI subprocess 场景：进程 A `plan/apply` 后进程 B `inspect/verify`，比较 state、有效 claim 和同 clock Frontier；逐项断言 exit `0/1/2` 和 stdout 单 JSON（AC7–AC9）。
- 目录/文件快照：对 inspect/plan/verify、所有拒绝路径和注入失败比较前后 tree bytes；create/update 成功分别检查 atomic directory/file 结果且无 staging/temp 残留（AC1、AC2、AC6–AC9）。
- 并发场景：两个进程使用同 base 操作不同 operation，只允许一个提交；同 operation 同 digest 的并发/串行重试返回相同 receipt；过期重领后旧 token 永不完成（AC4、AC8）。
- `python3 scripts/test-workflow-registry.py` 与 `python3 scripts/sync-workflow-registry.py --check`：确认无新 Explore workflow/宿主入口，无自动 promotion，规则只指向驻留工具（AC10）。
- `python3 scripts/check-markdown-links.py --root .`、`git diff --check`、`bash scripts/verify-ci.sh`：验证文档指针、格式与两平台既有完整回归；P5 通过 verification-evidence runner 归档机器 record（AC11）。
- 不声明 TDD cycle；P5 无需伪造 Red/Green 对，仍以专项测试和完整 CI 的 captured evidence 为准。

## References Compliance

- N/A：冻结 AC 无 `prd_refs`，本迭代没有需要钉版的 `.ai/references/` 外部资料；R1 已确认的 Explore 合同通过归档产物与现行 `ideation-engine.md` 继承，不另立版本或 Workspace Write Plan。
