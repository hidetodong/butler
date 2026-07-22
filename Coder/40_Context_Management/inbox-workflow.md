---
title: 需求收件箱动作协议
audience: AI / 开发者
scope: /butler:inbox 与 $butler-inbox 的扫描、语义分类、确认、自审、委托路由和处理回执；不复制 PRD、ideation、milestone 的内部算法
---

# inbox-workflow（需求收件箱动作协议）

本协议把不确定的需求材料变成可审计的路由决定。`tools/inbox/inbox.py` 只登记可证明的来源事实；AI 负责语义分类；真正的派生动作必须委托既有规则真源。任何一步失败都不得伪造成功关系。

## 0. 前置门

1. 按 `Coder/20_Workflow_Lifecycle/mcv-deployment.md §0.1` 解析唯一 `PROJECT_ROOT`；歧义时零写入。
2. 读取 `inbox-schema.md`，恢复 `.ai/INBOX.md` 的状态、指纹与关系合同。
3. 读取 `.ai/MILESTONE.md`、`.ai/ITERATIONS.md`、`.ai/task-state.md`、`.ai/02_SESSION_HANDOFF.md`；存在活跃迭代时再读四件套，建立当前工作区保护集。
4. `origin/` 永远只读。不得因“处理收件箱”而移动、改名、格式化或删除来源。

## 1. 动作分支

| 参数 | 行为 | 写入 |
|---|---|---|
| `status` | 调 `inbox.py status`，汇总来源、状态和待处理数 | 无 |
| `scan` 或留空 | 先调 `inbox.py scan` 取得 plan；呈交新增/变化/拒绝/待处理摘要 | 无 |
| `apply` | 先 plan，再调 `inbox.py scan --apply` 登记来源事实，然后进入分析 | 只允许工具原子更新 INBOX 管理块 |
| `route` | 读取已登记的待处理来源，分析并走 §2–§5 | 仅在各门通过后 |

仓库内执行方式：

```bash
python3 "$BUTLER_PATH/tools/inbox/inbox.py" scan --project-root "$PROJECT_ROOT"
python3 "$BUTLER_PATH/tools/inbox/inbox.py" scan --project-root "$PROJECT_ROOT" --apply
```

默认 `scan` 是零写 plan。工作流不得用手写 Markdown 模拟 scanner，也不得把拒绝项当成待路由来源。

## 2. 逐项分析合同

只分析 `unprocessed`、`source-changed` 或 `failed` 的来源。读取原文时遵守 locator 边界，输出每项四元组：

| 字段 | 要求 |
|---|---|
| `source_id` | 沿用 ledger 身份 |
| `classification` | 只能取 `inbox-schema.md §5` 枚举 |
| `reason` | 一句可核查理由，不复制长原文 |
| `proposed_route` | 明确目标动作；缺目标身份时标出待确认问题 |

空内容、无法读取、认证失败或路径边界失败置 `failed`，不得推进 `processed_sha256`。不同 locator 内容相同只能分类为 `duplicate-candidate`，不得自动认亲。

## 3. 路由矩阵

| classification | 委托动作 | 成功关系 |
|---|---|---|
| `new-requirement` | 读取 `references-schema.md` 与 `prd-split.md`，创建新的 `prd_id` 后执行首切 | `prd / <prd_id> / created` |
| `existing-requirement-version` | 必须先确定目标 `prd_id`，再读取 `prd-update.md` 执行 update | `prd / <prd_id>@<version> / updated` |
| `supplemental-material` | 绑定已确认的 PRD/里程碑/项目 reference，不改写权威 PRD 原文 | `reference / <relative-ref> / supports` |
| `fuzzy-idea` | 委托 `Coder/50_Extension_Ideation/ideation-engine.md`；不得覆盖已有 `.ai/IDEATION.md` | `ideation / <relative-ref> / created` |
| `milestone-direction` | 按 `milestone-schema.md` 写一方向一文件的未编号 milestone backlog；不抢占编号 | `milestone-backlog / <draft-key> / created` |
| `record-only` | 明确记录忽略理由，不创建工程产物 | `record-only / <reason-key> / ignored-as` |
| `duplicate-candidate` | 呈交候选身份，等待确认；确认后才可写 `duplicate-of` | 不自动写 |
| `ambiguous` | 列出最小澄清问题，保持等待确认 | 不写 |

本文件只负责选择并委托，不复制上述规则的切片、改版、脑暴或里程碑算法。

## 4. 确认与危险模式自审

### standard

先把全部四元组与批量路由计划呈交用户。用户确认前，只能把已分析项记为 `awaiting-confirmation`；不得执行派生动作、写 `actual_route` 或 Derivations。

### dangerous

用户已显式开启危险模式时可以免逐项 ACK，但每批必须先完成自审并写 `.ai/RUN_LOG.md`：

- 分类与原文事实是否吻合；
- 目标 `prd_id` / artifact 身份是否唯一；
- 是否触碰 §5 活工作区保护；
- 派生动作是否有独立验证与可恢复路径。

任一项不确定，退回 `awaiting-confirmation`。危险模式不是猜测许可。

## 5. 活工作区保护与批量隔离

以下是保护集：活跃 `.ai/MILESTONE.md`、当前 `.ai/ITERATIONS.md` 指向的迭代、当前四件套、未归档 `.ai/IDEATION.md`，以及它们声明的唯一身份。

- 路由若会覆盖、重置、换绑或并行占用保护集，冲突项保持 `awaiting-confirmation`，note 写明冲突对象。
- `existing-requirement-version` 影响当前活跃工作时，必须按 `prd-update.md` 的三态影响面亮牌，不得静默改当前 AC/TECH_PLAN。
- 每个 source_id 是独立事务边界。一个冲突或失败项不能阻塞无依赖 sibling；已成功 sibling 也不得因后项失败而回写成失败。
- 需要多个来源共同确认一个 artifact 时，先建立显式依赖组；组内全成或全不执行，不能留下半个派生事实。

## 6. 成功回执与失败回执

派生动作完成且其自身验证通过后，才原子更新对应 Sources 行并幂等追加 Derivations：

1. 写 `actual_route`；
2. 将 `processed_sha256 = observed_sha256`；
3. 置 `routed`，或对 record-only 置 `ignored`；
4. 以 `source_id + artifact_kind + artifact_ref + relation` 去重追加关系；
5. 写 `recorded_at` 与一条 RUN_LOG 路由回执。

失败时只置 `failed` 并写脱敏原因；不得推进 processed hash、不得留下成功关系。更新 ledger 必须复用 scanner 的 parser/renderer/atomic writer，不能用模糊文本替换。

## 7. 收尾输出

汇报 `added / changed / unchanged / missing / rejected`，并按 `routed / ignored / awaiting-confirmation / failed` 列 source_id。明确指出哪些项因活工作区冲突未执行；`status` 分支始终只读。
