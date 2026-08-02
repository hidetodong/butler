# decision-work

Butler Explore 的决策工作 Module。它把一次受控求证保存为不可变 Task Packet / Result Envelope，并把“helper 已返回候选”与“Decision 已被解决”严格分开。helper 不能写 Decision Map；只有协调器显式 `absorb_result` 才会通过 [`../decision-map/`](../decision-map/) 提交 resolve。

## 边界

- sidecar 固定为 `.ai/decision-work/DMAP-NNNN/DEC-NNNN/ATT-NNNN/{task.json,result.json}`；`task.json` 不可变，`result.json` 可缺省且至多发布一次。
- `.ai/.decision-work-locks/` 只有 Map 级本地写锁；Attempt 列表由目录扫描派生，没有 mutable status 或全局可写索引。
- Module 不启动 agent、不判断需求大小/清晰度、不自动选择 Decision、不自动 retry/re-claim/resolve，也不创建 Milestone、Iteration 或 promotion 产物。
- helper 完成、record 成功或 Result absorbable 都不会触发交付；协调器显式 absorb 形成 resolved Decision 后，才可由相邻 `tools/decision-promotion/` 消费用户选择的 slice。本模块不拥有该交接。
- Task Packet 不含明文 Claim token、原始对话、绝对项目写路径或宿主 prompt。helper 在隔离临时目录工作，不得写目标项目或 `.ai/`。
- 只有 `research` 可组成多项 batch，`max_parallel` 为 `1..8`、默认 `1`。宿主不能提供 fresh-context/并行时必须串行降级并如实回传实际模式。
- 本工具只保证同一 macOS/Linux 本地文件系统上的进程协调；不提供身份认证、跨主机调度或长期队列。

## 四动作 Interface

```bash
python3 "$BUTLER_PATH/tools/decision-work/decision_work.py" inspect \
  --project-root <PROJECT_ROOT> [--map-id DMAP-0001] \
  [--decision-id DEC-0001] [--attempt-id ATT-0001]

python3 "$BUTLER_PATH/tools/decision-work/decision_work.py" plan \
  --project-root <PROJECT_ROOT> --map-id DMAP-0001 --spec operation.json > plan.json

python3 "$BUTLER_PATH/tools/decision-work/decision_work.py" apply \
  --project-root <PROJECT_ROOT> --plan plan.json

python3 "$BUTLER_PATH/tools/decision-work/decision_work.py" verify \
  --project-root <PROJECT_ROOT> [--map-id DMAP-0001]
```

`inspect`、`plan`、`verify` 零写。`apply` 在 Map 级 work lock 下重读 sidecar 与 Decision Map，再提交不可变文件或嵌套 R2 operation。stdout 始终为一个 JSON 对象：成功退出 `0`；锁竞争、stale plan、身份冲突或不可吸收退出 `1`；坏 schema、损坏文件、unsafe path 与 I/O 错误退出 `2`。

## 调用顺序

1. 用 Decision Map `inspect` 读取 Frontier，由用户/协调器显式选择 Decision ID。
2. 对每个所选 Decision 调用 Decision Map `claim`，保留 claim receipt、owner 与 token。
3. 用本工具 `prepare_attempts` 生成不可变 `task.json`。prepare 会校验 Decision open、依赖已解决、当前 Claim 与 receipt 完整匹配；已领取 Decision 此时不必仍在 Frontier。
4. 宿主把 Task Packet 交给合适 worker/HITL 会话；worker 只返回有界 Result Envelope。
5. 用 `record_result` 原子保存 `result.json`。迟到、失败、取消或 needs-input 结果可保存，但不会改 Map。
6. 用 `inspect` 审阅派生状态。只有 `candidate + relation=current` 才是 absorbable。
7. 协调器明确接受候选后，以当前 owner/token 调用 `absorb_result`。Module 当刻创建新的 Decision Map resolve plan，并追加相对路径 + SHA-256 证据指针。

helper 完成、record 成功和 `absorbable=true` 都不等于 Decision resolved。跳过第 7 步时，R2 state 字节不变。

## Operation spec v1

顶层固定为 `schema_version / operation_id / operation`。operation kind 是封闭集合：

| kind | 必要内容 | 唯一副作用 |
|---|---|---|
| `prepare_attempts` | `map_id`, `work_type`, 可选 `max_parallel`, `attempts[]` | 发布一个或一批 `task.json` |
| `record_result` | `map_id`, `decision_id`, `attempt_id`, `task_sha256`, `result` | 发布一个 `result.json` |
| `absorb_result` | `map_id`, `decision_id`, `attempt_id`, `owner`, `token`, `resolve_operation_id` | 通过 Decision Map Module resolve |

单项 prepare 示例：

```json
{
  "schema_version": 1,
  "operation_id": "OP-prepare-sync-research",
  "operation": {
    "kind": "prepare_attempts",
    "map_id": "DMAP-0001",
    "work_type": "research",
    "max_parallel": 1,
    "attempts": [{
      "decision_id": "DEC-0001",
      "attempt_id": "ATT-0001",
      "confirmed_context": ["需要离线可用"],
      "constraints": ["只使用公开一手资料"],
      "expected_output": ["推荐方案及反证"],
      "claim_operation_id": "OP-claim-sync",
      "claim_owner": "coordinator",
      "claim_token": "<R2 claim token>",
      "requested_execution_mode": "serial"
    }]
  }
}
```

明文 token 只存在调用方的 operation/plan 中，用于在提交时校验；发布后的 Task Packet 只保存 token SHA-256 和 observed expiry。

## Task / Result v1

Task 绑定 Map、Decision、Attempt、work type、原问题、确认上下文、约束、预期输出、可选 predecessor、prepare/batch identity、R2 revision/digest 与 Claim receipt/digest/expiry。Attempt ID 由调用方显式分配；同一个 `needs_input` predecessor 只能接一个新 Attempt。

Result status 只有：

- `candidate`：有 outcome、rationale、evidence 及对应 work-type payload，可进入显式吸收审查。
- `needs_input`：有问题或 artifact pointer；终结当前 Attempt，只能新建 predecessor Attempt 接续。
- `failed`：有稳定 error code/summary；不自动 retry。
- `cancelled`：有原因；不自动 re-claim。

work type 只有：

| type | candidate 的专属内容 | 执行限制 |
|---|---|---|
| `research` | findings, sources, uncertainties | 唯一允许多项 parallel batch；可串行降级 |
| `prototype` | artifacts, observations, human_evaluation | 缺真人评价不能 candidate；单项 serial/HITL |
| `grilling` | questions, human_answers, assumptions, tradeoffs | 禁止 self-answer；单项 HITL |
| `task` | action, evidence, unblocked | 只解除决策前置阻塞，不得声称完成最终交付 |

Result 还回传 `actual_execution_mode=parallel|serial|hitl` 与 `fresh_context`。它们是执行事实回声，不是 Module 对宿主能力的推断。

## 派生状态与恢复

`inspect` 分开返回：持久 `result_status`，派生 `lifecycle=pending|expired|recorded`、`timeliness=on_time|late|N/A`、`relation=current|stale|absorbed`，以及 `absorbable`/原因码。状态不写回文件，因此新进程只凭 R2 Map 与 sidecar 就能恢复。

record 不要求 Claim 仍有效，合法迟到结果仍可作为参考保存；但 Claim 到期/替换、Decision terminal、非 candidate 或被篡改都不可 absorb。每次 absorb 都在当刻生成新 R2 plan，因此同一 Research batch 的多个结果不会因前一个 resolve 自动污染后一个的旧 base。相同 operation/request 的 prepare/record 和相同 R2 resolve receipt 可幂等恢复；不同内容复用 identity 会 fail-closed。

`verify` 检查目录、symlink、canonical JSON、task↔Decision/claim receipt、result↔task digest、batch/predecessor 和 R2 evidence pointer。若已吸收的 result 后来缺失或摘要改变，也会报告错误。检查本身零写。
