# decision-promotion

Butler Explore 到交付系统的确定性交接 Module。它只消费用户显式选择的 resolved Decision slice，不判断需求是否清晰、大小或应进入哪个目标，也不创建 Milestone route。

## 所有权边界

- Decision Map 继续拥有探索决定；promotion receipt 只保存稳定引用和交接结果。
- Milestone 继续拥有路线的创建、排序、状态和取消；`route-reference` 只引用一个已经存在的 planned route。
- Iteration intake 继续拥有迭代号、P1 活产物和台账写入；`iteration-start` 只把已确认 slice 结晶为 intake spec。
- promotion 不关闭 Map、不直接进入 P2、不更新 active Iteration，也不写 Decision Work。

## 四动作 Interface

```bash
python3 "$BUTLER_PATH/tools/decision-promotion/decision_promotion.py" inspect \
  --project-root <PROJECT_ROOT> [--promotion-id PROM-0001] \
  [--milestone-id MILE-0001 --route-id R2]

python3 "$BUTLER_PATH/tools/decision-promotion/decision_promotion.py" plan \
  --project-root <PROJECT_ROOT> --spec promotion.json > promotion-plan.json

python3 "$BUTLER_PATH/tools/decision-promotion/decision_promotion.py" apply \
  --project-root <PROJECT_ROOT> --plan promotion-plan.json

python3 "$BUTLER_PATH/tools/decision-promotion/decision_promotion.py" verify \
  --project-root <PROJECT_ROOT> [--promotion-id PROM-0001]
```

`inspect`、`plan`、`verify` 零写；`apply` 是唯一写动作。stdout 始终为单个 JSON。成功为 exit `0`，锁/状态冲突/stale 为 `1`，坏输入、损坏状态或 verify 失败为 `2`。

## Request v1

共同 envelope：

```json
{
  "schema_version": 1,
  "promotion_id": "PROM-0001",
  "source": {
    "map_id": "DMAP-0001",
    "decision_ids": ["DEC-0004"]
  },
  "target": {}
}
```

`decision_ids` 是用户选择的 slice roots。工具自动展开传递依赖闭包；闭包必须全部 resolved，但 Map 中其他 Decision/Fog 可以开放。source digest 只覆盖 roots 与闭包的 question/dependency/resolution，所以无关探索不会制造伪 stale。resolution 的 outcome/rationale 必须存在，evidence 列表可以为空。

### route-reference

```json
{
  "kind": "route-reference",
  "milestone_id": "MILE-0001",
  "route_id": "R2"
}
```

目标必须是当前 active Milestone 中已经存在、尚未绑定 ITER 的 `planned` route。apply 只发布 `.ai/decision-promotions/PROM-0001/receipt.json`；不修改路线表、Map 或迭代台账。route→Decision 视图由 `inspect --milestone-id ... --route-id ...` 扫描 receipts 派生。

### iteration-start

```json
{
  "kind": "iteration-start",
  "milestone_id": "MILE-0001",
  "route_id": "R2",
  "intake": {
    "title": "实现同步策略",
    "summary": "把已确认策略交付为一个迭代。",
    "model_recommendations": [],
    "open_questions": [],
    "in_scope": ["同步策略"],
    "out_of_scope": ["其他探索方向"]
  }
}
```

存在 active Milestone 时，两个 ID 必须指向它的可用 planned route；没有 active Milestone 时，两者必须同时为 `null`，表示 standalone Iteration。必须没有 active Iteration。confirmed decisions 由 source closure 投影，调用方不能另写一份；apply 复用 iteration-intake，从 P1 开启并在 `CONCEPT.md` 写 Promotion Source 指针，绝不跳入 P2。

## Plan、receipt 与恢复

plan 固定规范 request digest、source slice digest 和相关 target digest。apply 在项目根目录 inode 外层 guard 与 `.ai/.decision-promotion.lock` 双层非阻塞锁内重算；即使 intake rollback 替换整个 `.ai`，外层 guard 仍保持锁连续性。真实变化返回 `stale_plan`；closure 外 Map 变化不影响计划。

receipt 是 canonical JSON，记录 `promotion_id`、request/source digest、roots/closure、观察到的 Map revision、target、result 和 UTC 时间，不复制三方完整状态。相同 ID + 相同 request 返回首次结果并标记 idempotent；相同 ID + 不同 request 拒绝。

`route-reference` 使用 staging + fsync + atomic rename。`iteration-start` 进入 intake 前先在 `.ai/.decision-promotion-pending/` 发布临时意图，随后在 iteration-intake 的 rollback callback 内共同写 Source References 与 receipt；正常完成或可捕获异常会删除 pending，进程强杀则留下它。callback 或同步异常时 `.ai` 整体恢复。现有 intake 不承诺被 SIGKILL 时的跨多文件强原子性；`verify` 会把残留 pending，或 CONCEPT 已含 Promotion Source 但 receipt 缺失，报告为 `incomplete_promotion`，不会猜测、补写或再开一个迭代。

同一 resolved slice 可以由用户用不同 `promotion_id` 显式引用到多个 route。Map close 与 promotion 正交；P2 冻结后的新结论继续按 Iteration 的 amend/re-ACK 或扩张到未来 route/Iteration 处理。
