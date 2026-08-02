# decision-map

Butler Explore 的本地确定性状态 Module。它把 Decision、Fog、依赖、Frontier 和临时领取封装在四动作 Interface 后面；调用者和未来 helper 不得直接编辑状态文件。

## 边界

- 每张 Map 的唯一可写真源是 `.ai/decision-maps/DMAP-NNNN/state.json`。
- `.ai/.decision-map-locks/` 只保存本地写锁，不是状态或索引。
- Map 列表由目录扫描派生，不建立全局可写索引。
- Frontier 由 `open + depends_on 全 resolved + 无有效 Claim Lease` 计算，不写回 state。
- 工具只协调同一 macOS/Linux 文件系统；不保证跨主机或网络文件系统一致性，Claim token 也不是身份认证。
- Decision Map 只拥有探索状态。它不创建 Milestone、Iteration 或 P1→P5 产物，promotion 后仍只是理由、证据和历史参考。
- 用户显式选择 resolved Decision slice 与目标后的交接由相邻 `tools/decision-promotion/` 负责；本工具不提供 promotion operation，也不反向保存 receipt。

## 四动作 Interface

```bash
python3 "$BUTLER_PATH/tools/decision-map/decision_map.py" inspect \
  --project-root <PROJECT_ROOT> [--map-id DMAP-0001]

python3 "$BUTLER_PATH/tools/decision-map/decision_map.py" plan \
  --project-root <PROJECT_ROOT> --map-id DMAP-0001 --spec operation.json > plan.json

python3 "$BUTLER_PATH/tools/decision-map/decision_map.py" apply \
  --project-root <PROJECT_ROOT> --plan plan.json

python3 "$BUTLER_PATH/tools/decision-map/decision_map.py" verify \
  --project-root <PROJECT_ROOT> [--map-id DMAP-0001]
```

`inspect`、`plan`、`verify` 保证零写。`apply` 获取 Map 级非阻塞文件锁，在锁内重读并校验 base revision/SHA-256，再发布一个完整 revision。stdout 始终是单个 JSON：成功退出 `0`，锁、stale plan 或 operation ID 冲突退出 `1`，坏输入、损坏状态和 I/O 错误退出 `2`。

`plan` 的输出是可保存的 apply 文档，包含 `base_revision`、`base_sha256`、规范 operation、`request_sha256` 和 effect preview。`apply` 不信任 preview，会重算 request digest 和候选状态。相同 operation ID + 相同 request digest 的重试返回首次 receipt，不重复增加 revision；相同 ID + 不同请求拒绝。

## Operation spec v1

顶层只有三个字段：

```json
{
  "schema_version": 1,
  "operation_id": "OP-stable-client-id",
  "operation": {
    "kind": "create_map",
    "title": "选择同步方案",
    "destination": "形成可进入交付的同步策略"
  }
}
```

`operation.kind` 是封闭集合：

| kind | 必要内容 | 结果 |
|---|---|---|
| `create_map` | `title`, `destination` | 创建 revision 1 的 open Map |
| `add_decision` | `decision_id`, `question`, `depends_on` | 新增 open Decision |
| `add_fog` | `fog_id`, `description` | 新增 open Fog |
| `link_dependency` / `unlink_dependency` | `decision_id`, `dependency_id` | 修改同 Map DAG 边 |
| `claim` | `decision_id`, `owner`, `lease_seconds` | 领取 Frontier Decision 并生成 token |
| `renew` | `decision_id`, `owner`, `token`, `lease_seconds` | 延长未过期 lease |
| `release` | `decision_id`, `owner`, `token` | 释放未过期 lease |
| `resolve` | `decision_id`, `outcome`, `rationale`, `evidence`，已领取时再带 `owner`, `token` | 解决可处理 Decision |
| `abandon` | `decision_id`, `reason` | 丢弃无 active claim、无 open dependent 的 Decision |
| `graduate_fog` | `fog_id`, 一个或多个完整 Decision 定义 | 一个事务内结晶 Fog |
| `dismiss_fog` | `fog_id`, `reason` | 关闭不再追踪的 Fog |
| `close_map` | 无 | 在无 open Decision/Fog 时关闭 Map |

Map、Decision、Fog 使用显式规范 ID：`DMAP-NNNN`、`DEC-NNNN`、`FOG-NNNN`，至少四位且不接受多余零填充。工具不自动分号；这避免了没有全局写索引时的跨 Map 分配竞态。

`lease_seconds` 为 `1..86400`。`now >= expires_at` 时 lease 逻辑上已经失效；旧 worker 不能 renew、release 或 resolve，被重新领取后也不能覆盖新 worker。无有效 claim 的 Frontier Decision 允许协调器直接 resolve。

## State v1

state 顶层固定包含：

- `schema_version`, `map_id`, `revision`, `status`
- `title`, `destination`, `created_at`, `updated_at`
- 以 ID 为键的 `decisions` 和 `fog`
- 以 operation ID 为键的 `applied_operations`

Map 状态只有 `open / closed`，Decision 只有 `open / resolved / abandoned`，Fog 只有 `open / graduated / dismissed`。未知字段、未知枚举、重复/悬空/跨 Map 依赖、依赖环、open Decision 依赖 abandoned Decision、非规范 JSON 和 symlink 均 fail-closed。

state 使用 UTF-8 canonical JSON（排序键、两空格缩进、尾换行）。新 Map 先写隐藏 staging 目录再原子 rename；已有 Map 在同目录 fsync 临时文件后 `os.replace`。进程中断时，可见状态只会是旧或新完整版本。发布后响应若丢失，调用方以同 operation ID 重试即可恢复首次结果。

`applied_operations` 为永久幂等保存 receipt，因此会随 Map 操作数增长。v1 不做静默截断或 compaction；需要压缩时必须由后续 schema migration 明确处理。
