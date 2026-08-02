<!-- butler-artifact-template: 1.0.0 artifact=tech_plan -->
# TECH_PLAN — ITER-0104

方案状态: pass
方案审查日期: 2026-08-01
方案审查方式: user-ack

## Design Decisions

### Goal

- 以一个深的 Decision Work Module 覆盖 AC1–AC14：调用者只学习 `inspect / plan / apply / verify` Interface，Task/Result schema、不可变发布、Research batch、HITL 接续、迟到/失败恢复和显式 absorb 都由 Implementation 吸收。
- helper 的 seam 停在 host-neutral Task Packet / Result Envelope；宿主负责如何启动 worker，核心 Module 不绑定 Codex、Claude 或 Pi 的子 agent 调用方式。

### Files / Modules to Change

- `tools/decision-work/engine.py` — **Decision Work 深 Module**；唯一拥有 sidecar 路径、严格 task/result/plan 合同、派生 attempt 状态、batch 校验、原子发布、幂等和 absorb 编排。Python 调用者只使用四动作 Interface。
- `tools/decision-work/decision_work.py` — **CLI Adapter**；将四个动作和 JSON 文档转给 Module，stdout 固定单 JSON，退出 `0/1/2`，不复制合同算法。
- `tools/decision-work/README.md` — **R3 工具合同真源**；定义 sidecar v1、work/result 类型、操作、证据 pointer、并发/HITL/迟到语义及非保证项。
- `tools/decision-work/tests/test_engine.py` — 从 Interface 验证 schema、四类 work、predecessor、派生状态与 absorb 规则。
- `tools/decision-work/tests/test_storage.py` — 验证 canonical bytes、Map 级 work lock、batch 预检、原子 publish、幂等、真实竞争、symlink/path 与故障恢复。
- `tools/decision-work/tests/test_cli.py` — subprocess 验证四动作、退出码、零写、跨进程 prepare/record/absorb/verify。
- `Coder/62_Extension_Agents/decision-work.md`、`overview.md` — 新增一个 Decision Work Helper 定义，四类 work 是同一 helper Interface 的模式，不建立四套 agent 生命周期；明确权限、隔离、HITL 和串行降级。
- `Coder/50_Extension_Ideation/ideation-engine.md` — 在 R2 Map 指针之后接 R3 work packet/result/absorb 指针，强调 helper 不写 Map、Research 求证并行而 Map 单写。
- `Coder/20_Workflow_Lifecycle/mcv-deployment.md`、`Coder/README.md`、`README.md` — 注册第二个驻留工具与唯一合同指针，不复制 sidecar schema、不增加项目部署副本。
- `CONTEXT.md` — 增补 Attempt、Task Packet、Result Envelope、Needs Input、Absorb 的统一领域词义。
- `scripts/test-workflow-registry.py`、`scripts/verify-dual-host.sh` — 扩展静态边界断言并把三组专项测试/compileall 接入完整 CI；不修改 `workflows/registry.json` 的 13 workflow 集合。
- `.ai/01_CHANGELOG.md` 与收口知识 topic — P4/P5 记录实际 delta，收口时按主题折叠；不在 P3 预写完成结论。

### External Interface

- CLI 与 Python 都只暴露四个动作：
  - `inspect(project_root, map_id?, decision_id?, attempt_id?, now?)`：扫描 sidecar 并结合 R2 当前状态，分别返回持久 `result_status`、派生 `lifecycle/timeliness/relation` 与 absorbability，避免把 late、stale、candidate 等正交维度揉成一个互斥枚举；零写。
  - `plan(project_root, map_id, spec, now?)`：严格规范化一个 `prepare_attempts / record_result / absorb_result` operation，返回 work base digest、相关 R2 revision/digest、request digest 与 effect preview；零写。
  - `apply(project_root, planned, now?)`：在 Map 级 work lock 下重读 sidecar/R2、重算候选并提交一个 operation；prepare/record 只发布不可变文件，absorb 只调用 R2 Module。
  - `verify(project_root, map_id?, now?)`：校验 sidecar tree、canonical JSON、绑定/predecessor/batch 不变量与 R2 悬空引用；零写。
- operation spec 顶层固定为 `schema_version / operation_id / operation`，kind 封闭为：
  - `prepare_attempts`：`map_id`、`work_type`、`max_parallel`（可省略，默认 1）、一个或多个完整 attempt request。
  - `record_result`：`map_id / decision_id / attempt_id / task_sha256 / result`。
  - `absorb_result`：`map_id / decision_id / attempt_id / owner / token / resolve_operation_id`；不允许调用者重写 candidate outcome/rationale/evidence。
- CLI 成功退出 `0`；锁竞争、stale plan、已存在不同字节、不可 absorb 等安全冲突退出 `1`；坏 schema、损坏 sidecar、unsafe path 或 I/O 错误退出 `2`。

### Task Packet / Result Envelope v1

- identity 均显式给出且 canonical：`DMAP-NNNN / DEC-NNNN / ATT-NNNN`，Module 不自动分号。每个 Decision 下 Attempt ID 唯一；predecessor 必须是同 Decision 已存在且 result=`needs_input` 的 attempt，并且只允许一个直接 successor，避免 HITL 分叉。
- `task.json` 顶层固定保存：schema、identities、work_type、question、confirmed_context、constraints、expected_output、可选 predecessor、prepare operation ID、R2 `map_revision/map_sha256`、claim operation ID/owner/token SHA-256/observed expiry、requested execution mode、batch ID、完整 batch member identities 和 created_at。member 清单让 verify 能在没有全局索引时识别硬崩后的不完整批次。
- Task Packet 不含明文 token、原始对话、绝对项目写路径或宿主 prompt。`requested_execution_mode` 只有 `parallel / serial / hitl`：多项 Research 为 parallel；单项 Research 可 serial；prototype/grilling/task 必须 hitl 或 serial。
- `result.json` 公共字段固定为 schema、identities、task_sha256、record operation ID、status、actual_execution_mode、fresh_context、submitted_at 与 type payload。真实执行模式是可审计回声，不把布尔声明冒充宿主能力证明。
- status 封闭为：
  - `candidate`：含不可空 outcome/rationale/evidence 及 work-type payload，可进入显式 absorb 校验。
  - `needs_input`：含 questions 或 artifact pointers；终结本 attempt，只能通过新 predecessor attempt 接续。
  - `failed`：含稳定 error code/summary；不自动 retry。
  - `cancelled`：含 reason；不自动 re-claim。
- work-type payload：research 固定 findings/sources/uncertainties；prototype 固定 artifacts/observations/human_evaluation，缺最后一项不能 candidate；grilling 固定 questions/human_answers/assumptions/tradeoffs 且 `human_answers` 不能为空，不接受 self-answered 标志；task 固定 action/evidence/unblocked，`unblocked` 只说明前置障碍，不允许 `delivery_completed` 字段。

### State / Boundary

- sidecar 只落在 `.ai/decision-work/DMAP-NNNN/DEC-NNNN/ATT-NNNN/{task.json,result.json}`。`task.json` 一经发布不可变，`result.json` 至多发布一次；不写 status 文件。inspect 将正交事实分开：`result_status=none/candidate/needs_input/failed/cancelled`，无结果时 `lifecycle=pending/expired`，`timeliness=on_time/late/N/A`，`relation=current/stale/absorbed`，再给 `absorbable` 与原因码。
- `.ai/.decision-work-locks/DMAP-NNNN.lock` 只用于本地 Map 级提交串行化，不是状态。Map/Decision/Attempt 列表由目录扫描派生，不建全局可写索引。
- prepare 的正确顺序固定为：调用方读取 R2 Frontier → 显式选择 ID → 逐项使用 R2 claim → 以 claim receipt 和当前 Map 创建 Task Packet。prepare 时 Decision 因有效 Claim 已不在 Frontier；Module 校验的是 open、依赖全 resolved、claim receipt 存在且当前 owner/token digest/expiry 匹配。
- `max_parallel` 为 `1..8`，省略按 1；只有 research 可 batch size >1。apply 获取 work lock 后先对整批重读并校验，任一坏项在任何发布前拒绝；合法项在隐藏 staging 中写完/fsync，再逐目录发布。I/O 失败回滚本次新增目录；进程硬崩后的合法子集可由同 operation 幂等补齐，verify 通过 task 内 batch identity/size 报告不完整批次。
- prepare/record 幂等不另建 receipt：目标文件不存在则原子发布，已存在且 canonical bytes/request identity 相同则返回原结果，不同则冲突。这样没有为不可变文件再引入 mutable receipt 真源。
- record 不要求 Claim 仍有效，因此迟到/替换 Claim 的合法 helper 输出仍可保存；它绝不修改 R2。`now >= current claim expires_at`、token digest 不同或 Decision 已 terminal 时，inspect 把 result 派生为 late/stale/不可 absorb。
- absorb 读取不可变 candidate，使用调用方当前 owner/token 在当刻生成一个新的 R2 resolve plan；task 创建时的旧 Map revision 只作 provenance，不因同 Map 其他并行 Decision 已提交就误判 stale。真正 stale 检查作用于 absorb 当刻生成的嵌套 R2 plan。
- absorb 的 R2 resolution outcome/rationale 逐字取 candidate，evidence 至少追加 canonical pointer：`decision-work:.ai/decision-work/<map>/<decision>/<attempt>/result.json#sha256:<hex>`。调用方不能在 absorb 时改写结论；不同结论必须新 attempt。
- DecisionMap Adapter 是 Implementation 内部 seam：生产 Adapter 动态加载并调用现有 `tools/decision-map/engine.py` 四动作 Interface；测试 Adapter 记录 plan/apply 调用并模拟冲突。它不扩大 Decision Work 的外部 Interface，也不复制 R2 reducer。
- helper 执行不进入 Python Module：Butler coordinator 根据 Task Packet 调用当前宿主已有的 worker 能力。Research 可 fresh-context parallel；宿主不支持则 actual mode 必须 serial。Prototype/Grilling 的人类输入留在协调器会话，Task 不获得项目源码写权限。
- R3 不创建/修改 Milestone、Iteration、四件套或 promotion receipt；不新增 workflow/skill/command。R4 只可读取 sidecar pointer 与 resolved Decision，后续归档不得反向改变 R3 v1 语义。

### Alternatives / Trade-offs

- **采用不可变 sidecar，不扩 R2 state**：避免把 helper/transcript/job 生命周期塞进探索决策真源，也使 record 迟到结果无需修改 Map；代价是 R4 需定义长期归档，R3 暂不压缩。
- **采用一个四模式 helper Interface，不建四个 helper lifecycle**：公共 packet/result/失败/吸收规则只维护一份，类型差异用严格 discriminator；避免四套浅 Module 漂移。
- **采用 host-neutral packet，不在工具里 spawn agent**：Claude/Codex/Pi 的 worker 能力真实不同，核心只承诺可验证输入输出；代价是 R5 前由 coordinator 按文档接线，不能把“工具已实现”说成“所有宿主已自动并行”。
- **采用显式 absorb，不在 record 后自动 resolve**：多一步调用换取人/协调器审阅和可审计意图，直接消除“helper 输出即决策”的模型依赖。
- **采用不可变 needs_input 链，不更新 result**：跨会话能保留每轮真实输入缺口与人类回答来源；代价是多一个 attempt，但避免 mutable conversation state 和覆盖历史。
- **采用内部 DecisionMap Adapter，不经 subprocess**：保留 R2 同一验证/receipt/原子语义，同时可注入 fake 测试；不搬运或复制 R2 Implementation。动态 loader 集中在一个内部 Adapter，CLI 路径不泄露给调用者。

### Execution Steps

- [x] T1 建立 Decision Work Module 骨架、路径/ID/canonical JSON、task/result/plan strict schema 与四动作只读路径 → AC1–AC5、AC12
- [x] T2 实现 sidecar 扫描、predecessor/batch 绑定和 UTC 派生 attempt 状态/absorbability → AC1、AC5、AC9、AC12
- [x] T3 实现 prepare plan/apply、R2 claim receipt 校验、Research batch `1..8`、staging/lock/幂等/回滚 → AC3、AC6、AC7
- [x] T4 实现 record plan/apply、四类 payload、needs_input/失败/取消/迟到与不可变冲突 → AC4、AC5、AC8、AC9
- [x] T5 实现内部 DecisionMap Adapter 与 absorb plan/apply、fresh base、canonical evidence pointer 和 R2 receipt 重试 → AC10、AC11
- [x] T6 实现 CLI Adapter、README 与跨进程/机器错误码合同 → AC2、AC12
- [x] T7 新增 Decision Work Helper 定义并更新 Agents/Ideation/驻留工具/CONTEXT 指针，保持 registry 与 R4 边界 → AC8、AC13
- [x] T8 编写 Interface、storage/concurrency、CLI 测试并扩展 workflow 静态合同 → AC1–AC13
- [x] T9 接入 `verify-dual-host.sh`，运行专项、artifact/registry/state/link/diff/完整 CI 并采集 P5 evidence → AC14

### Plan Admission

- **AC Coverage**：AC1–AC5 由 immutable sidecar、strict schemas 与 derived state 覆盖；AC6–AC7 由显式 R2 claim receipt + research-only batch 覆盖；AC8 由 host-neutral packet、helper definition 和 execution mode 回声覆盖；AC9 由 record/map 分离与注入 UTC 覆盖；AC10–AC11 由 fresh nested R2 plan、显式 absorb 和 receipt 幂等覆盖；AC12 由扫描/verify/跨进程覆盖；AC13 由规则指针与 registry 不变量覆盖；AC14 由三组专项、静态合同和完整 CI 覆盖。
- **Assumptions**：R2 Python 四动作 Interface 是本轮可复用 seam；用 production/fake 两个内部 Adapter 验证。Butler 支持 macOS/Linux 本地文件系统，沿用 `fcntl`/rename/fsync 假设。宿主是否实际支持 parallel/fresh-context 只能由 Adapter 回声和端到端 dogfood 证明，核心不能推断。
- **Alternatives / Trade-offs**：已比较扩 R2 state、可变 job store、四套 helper、工具内 spawn、自动 absorb 与可变 HITL result；选择不可变 sidecar + 单 helper合同 + 显式 absorb 是满足冻结 AC 的最小深 Module。
- **Failure Modes**：坏/非规范 JSON、路径逃逸/symlink、attempt 冲突、predecessor 分叉、batch 坏项、claim receipt 缺失/替换/过期、stale plan、同 ID 异内容、record 迟到、result 篡改、R2 apply 冲突、发布中断与宿主能力降级均有拒绝、派生状态或幂等恢复路径。
- **Impact / Scope Challenge**：最小完整落点是一个 Module、一个 CLI Adapter、三组测试、一个中立 helper 定义与现有文档/CI 指针；不需要 registry 新 workflow、R2 schema migration、通用 scheduler 或 R4 promotion。
- **Verification Blind Spots**：机器能验证 packet 没有 token/写路径、声明的 execution mode 和 fake Adapter 行为，不能证明真实第三方宿主确实创建 fresh-context worker；R5 dogfood 前必须把该项作为可观察非保证。硬崩发生在多目录 batch 发布中间时，恢复依赖同 operation 重试/verify，不声称文件系统提供多目录原子事务。
- **Verdict**：`pass` — AC 全部有明确 Interface、Implementation 与验证映射，关键并发/并行矛盾已消除，无已知 Must Fix；用户已完成 P3 ACK，可进入 P4。

## Failure Paths

- **把已 Claim Decision 仍判作 Frontier**：会让所有合法 prepare 自相矛盾；prepare 改验 open + resolved dependencies + live matching Claim，并核 claim receipt。
- **并行结果互相制造 stale**：若 absorb 强绑 task 创建时 Map revision，先吸收一个就会阻断同批其它结果；旧 base 仅作 provenance，每次 absorb 重新生成 R2 plan。
- **helper 泄露写权/明文 token**：Task Packet schema 无这些字段，严格未知字段拒绝，测试扫描 packet；Claim 只留 token digest。
- **HITL 覆盖旧结果**：prototype/grilling 需要人输入却改写 result 会丢历史；needs_input 终结 attempt，新 attempt 显式 predecessor 且不分叉。
- **坏 Research 项造成半批**：plan/apply 均整批预检后才发布；I/O 失败回滚，硬崩合法子集通过 operation 重试补齐并由 verify 报不完整批次。
- **迟到 worker 覆盖新决定**：record 可保存但不写 Map；absorb 重新检查当前 claim、Decision 状态和 result hash，旧 token/terminal Decision 拒绝。
- **record 被误当 resolve**：所有 prepare/record/inspect 前后断言 R2 bytes/revision 不变，只有 absorb 的内部 Adapter 可以调用 R2 apply。
- **候选在 absorb 时被模型改写**：absorb spec 不接受 outcome/rationale/evidence 覆盖，resolution 从 result 逐字生成并追加 canonical pointer。
- **宿主不支持并行却冒称 parallel**：helper definition 要求 actual execution mode/fresh-context 回声；不支持时串行，不阻断正确性但不能报告并行收益。
- **sidecar 路径逃逸或手改**：只由 canonical IDs 拼路径，逐层拒绝 symlink/意外文件，canonical JSON + SHA-256 绑定，verify 零写报告。
- **动态加载 R2 漂移**：production Adapter 启动时验证四动作存在，所有行为仍由 R2 tests + Decision Work integration tests覆盖；不复制 reducer。

### Risks / Open Questions

- 不可变 attempt 会增长；R3 按 Map/Decision 定向扫描并设置输入/输出大小上限，归档和压缩留给 R4，不静默删除。
- `max_parallel=8` 只限制批次规模，不限制主机总资源；coordinator 仍应依据宿主能力选择较小显式值，默认 1。
- actual execution mode 是宿主 Adapter 的审计声明，不是密码学证明；R5 必须用真实 dogfood 评估并行收益。
- 当前无阻断 P4 的设计开放问题；P3 已获用户 ACK。

## Test Strategy

- `python3 -m unittest discover -s tools/decision-work/tests`：从四动作 Interface 覆盖 task/result 四类型、needs_input predecessor、prepare/record/absorb、derived state、strict/canonical/path、幂等、并发与故障注入（AC1–AC12、AC14）。
- R2 integration：在临时项目通过真实 Decision Map create/add/claim 建立 work-ready Decision，验证非 Frontier claim 由 R2 拒绝、prepare 核 receipt/current claim、record 零 Map 写、并行结果依次 fresh absorb 且 R2 receipt 重试一致（AC6、AC7、AC9–AC11）。
- Research batch：覆盖 size `1/2/8`、默认 1、0/9、非 research 多项、重复 ID、一个坏 claim/依赖和多目录竞争；坏批次前后 tree digest 相同，硬崩模拟后可重试补齐或由 verify 亮牌（AC6、AC7、AC12）。
- HITL/type fixtures：prototype 缺 human evaluation、grilling 缺 human answers/self-answered、task 越权声明 delivery complete、research 缺 source/uncertainty 均不能 candidate；needs_input→predecessor candidate 链可恢复（AC4、AC5）。
- UTC/乱序矩阵：pending/expired/on-time/late、claim renew/replace、record before/after expiry、Decision terminal、result tamper、stale absorb plan，逐场景比较 R2/sidecar bytes（AC9–AC12）。
- CLI subprocess：进程 A prepare、隔离 fake worker 产出、进程 B record、进程 C inspect/absorb/verify；断言 stdout 单 JSON、exit `0/1/2` 和零写动作（AC2、AC8、AC12）。
- `python3 scripts/test-workflow-registry.py` 与 `python3 scripts/sync-workflow-registry.py --check`：断言仍为 Router + 13 workflows，无新入口、无自动 promotion，Agents/Ideation 只回指 Decision Work 真源（AC13）。
- `python3 scripts/check-markdown-links.py --root .`、artifact contract、state audit、`git diff --check`、`bash scripts/verify-ci.sh`：完整回归并由 verification-evidence runner 生成 AC 映射 record（AC14）。
- 不声明 TDD cycle；P5 的 `TDD Pair Status` 写 N/A，以专项测试、真实 R2 integration 和完整 CI 的 captured evidence为准。

## References Compliance

- N/A：AC 无 `prd_refs`，没有外部权威规格或 Workspace Write Plan；Wayfinder 调研仅是背景，冻结合同以 `.ai/CONCEPT.md`、`.ai/AC_LIST.md`、R1/R2 归档和仓内现行规则为准。
