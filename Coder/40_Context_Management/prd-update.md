---
title: PRD 确定性改版与回执
audience: AI / 开发者
scope: 指定 prd_id 的新版 PRD 经变更对账、模块认亲和三态处置确认后，生成 update spec，由标准库工具零写 plan、先冻后更事务 apply、持久 receipt、verify/rollback；不做首切或代码范围门禁
---

# prd-update（PRD 确定性改版与回执）

本文件是已有需求的改版动作真源。结构/身份以 `references-schema.md` 为准，首切走 `prd-split.md`，查询走 `prd-status.md`。机械执行唯一入口是 `$BUTLER_PATH/tools/prd-update/prd_update.py`；宿主命令不得手工模拟事务。

## 1. 身份闸与变更对账（先不写盘）

调用必须显式给出已登记 `prd_id`，并按 `references-schema §5` 证明输入是该需求的 `new-version`。省略、duplicate、ambiguous、指向 legacy 或来源关系冲突都停止；改版不领取新 ID。

语义层先完成：

1. 用户修改清单优先，旧 live 与新版原文逐字 diff 兜底；两者不一致必须亮出。
2. 按 `prd-split` 的自然边界重新派生最终 active 模块原文，不让 CLI 猜章节。
3. 认亲先判保留/新增/消失，再提改名/拆分/合并候选。改名保留 slug；新 slug 的 origins 必须指向旧 active slug；拿不准退回独立新增+移除。
4. 扫描 changed slug 对 `.ai/MILESTONE.md#R<n>`、当前 AC 和 ledger=closed 的 archived AC 的 future/active/closed 影响；同一 milestone 文件按每条路线实际状态分别分类，不改这些文件。
5. 一次 soft 对齐 old/new version、最终模块/source、origins/removed、三态影响和每项处置。标准模式用户确认；危险模式完整自审可代 ACK。

## 2. Update Spec v1

确认结果写成 JSON spec；字段精确、未知字段拒绝：

```json
{
  "schema_version": 1,
  "prd_id": "2026-07-22-login",
  "expected_old_version": "v1.0",
  "new_version": "v1.1",
  "confirmed": true,
  "confirmation": {"mode": "user-ack", "at": "2026-07-22T10:00:00+08:00"},
  "active_modules": [
    {"module_slug": "login-flow", "title": "登录流程", "source": "sources/login-flow.md", "origins": ["login-flow"]}
  ],
  "removed_slugs": [],
  "dispositions": [
    {"path": ".ai/iterations/ITER-0001/AC_LIST.md", "decision": "keep-pinned-history", "note": "历史继续按 v1.0"}
  ]
}
```

- `source` 相对 spec 文件解析，必须是非 symlink 的 UTF-8 普通文件；bytes 原样写 live 并记 hash。两个模块不得复用同一 source 文件。
- retained slug 的 `origins=[自身]`；纯新增为空；split/merge 显式列旧 origins。removed slug 不得复活；一对一改名换 slug 拒绝。
- `new_version` 必须严格大于现场 old version；现有 archive 冲突拒绝。
- plan 阶段可用 `confirmed:false + pending`，但 apply 必须 `user-ack` 或 `dangerous-self-review` 的 ISO 时间。

## 3. 三态 disposition

plan 对每个影响 path 要求且只允许一项处置：

| state | 允许 decision | 边界 |
|---|---|---|
| `future` | `use-new-on-start` / `defer` / `not-applicable` | 不自动改 milestone |
| `active` | `amend-and-refreeze` / `keep-pinned` / `defer` | 不自动改/重冻当前 AC |
| `closed` | `keep-pinned-history` / `open-follow-up` / `defer` | closed 绝不回写 |

缺项、重复 path、越出当前 impact 或 state/decision 不匹配时 apply 拒绝。receipt 只记录决定；真正 amend/新迭代仍走既有生命周期。

## 4. 零写 plan

```bash
python3 "$BUTLER_PATH/tools/prd-update/prd_update.py" plan --project-root "$PROJECT_ROOT" --spec "$SPEC"
```

plan 复用 `prd-status` parser 对账项目总索引、目标索引/模块和 workspace map，读取 source bytes/hash，返回 module changes、三态 impact、dispositions、missing 与 `apply_ready`。它不建 lock/cache/stage/receipt。0=有更新且 ready，1=合法但未确认/缺处置/无实质变化，2=输入或现场错误。

## 5. 事务 apply：stage 中先冻，整 collection 切换

```bash
python3 "$BUTLER_PATH/tools/prd-update/prd_update.py" apply --project-root "$PROJECT_ROOT" --spec "$SPEC"
```

apply 获取 `.ai/references/.prd-update.lock` 后重算 plan/source/现场 hash：

1. 同父 stage 完整复制当前 `references/prd/`。
2. 在 stage 的目标 `<prd_id>/.archive/<old_version>/` 复制旧 `00_INDEX` + 全部登记模块，形成自包含快照；不得含其他 PRD 或嵌套 archive。
3. 才把确认过的 source bytes 写目标 live，removed 模块保留文件并置表状态；更新单需求 identity/模块表和项目总索引目标行，其他需求不动。
4. 用共享 status parser 验证 stage，写 `<prd_id>/.butler-updates/<update_id>.json`，再对 receipt 之外的 post tree hash 复核。
5. 将旧 PRD root rename 到 `.ai/references/.prd-update-backups/<update_id>`，再将 stage rename 为 live；live verify 失败立即反切换。

stage/backup 与 live 同文件系统；任一预检或 stage 点失败只清本次临时物。两次 rename 任一点失败必须恢复 exact pre tree、移除 lock/stage。成功 backup 保留到用户明确 rollback/清理。

## 6. Receipt、幂等、verify 与 rollback

receipt 是持久更新回执，含 `update_id/prd_id/applied_at`、old/new version、spec/source/pre/post/archive hashes、backup/archive 安全路径、module changes/origins、impact、dispositions、confirmation 与排除自身 hash 字段后的 `receipt_payload_sha256`。它不是 PRD 内容真源。

- 同一已确认 spec + source bytes 重复 apply：找到唯一 matching receipt、verify 通过后返回 `changed:false`，不再建 archive/bump。
- `verify --prd-id ID [--update-id UPD-…]`：零写，对账 current post、archive、backup、目标版本和 receipt path/schema。
- `rollback`：只允许 receipt 指向的当前 collection 仍等于 post hash、backup 等于 pre hash。任何后续 PRD 更新、人工漂移或路径篡改都拒绝，避免整树恢复覆盖新工作。
- receipt/backup/archive/update ID 绝对路径、`..`、symlink、错根或身份漂移全部 fail-closed。

## 7. status 与非回归

`prd-status` 只读投影每份需求的 `latest_update`（版本、module changes、impact、dispositions）；没有 receipt 为 `null`，畸形 receipt 拒绝。status 不因此获得写能力。

- update 工具只写 PRD collection、managed backup 和短命 lock/stage；MILESTONE、AC、iteration archive、origin 零写。
- 不使用 PRD 的项目、扁平 references、其他 `prd_id` 内容保持不变。
- workspace 自动发现、实际 git diff 与 hook 写范围门禁由 `workspace-scope-schema.md` 与 `tools/workspace-scope/` 消费更新后的钉版范围；本动作不复制其算法。
