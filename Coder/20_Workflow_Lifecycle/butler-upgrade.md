---
title: butler 主动升级协议
audience: AI / 开发者
scope: 已部署项目通过仓库升级器安全同步到当前 Butler 版本
---

# butler-upgrade (Executable Upgrade)

## 1. 目标与真源

已部署项目升级由 `$BUTLER_PATH/tools/butler-upgrade/upgrade.py` 确定执行。程序读取 `migrations/manifest.json`；`migrations/vX.Y.Z.md` 是人读发布说明，不再由模型解析散文决定写操作。

三层真源各司其职：

- `migrations/manifest.json`：版本链、action ID、类型、执行域和参数。
- `tools/butler-upgrade/upgrade.py`：preflight、计划、事务执行、恢复、退出状态。
- 本文：触发、交互路由、人工边界和完成口径。

## 2. 触发与项目根

用户显式输入 `/butler:upgrade`、`$butler-upgrade`，或明确要求升级/同步 Butler 时触发；不主动推断。

任何侦察前先按 `mcv-deployment.md §0.1` 解析并回声唯一 `$PROJECT_ROOT`。用户点名优先；歧义时停止且零写入。升级器还会拒绝：

- Butler 规则仓自身或其内部目录；
- 不存在、不可写、缺 `.ai/` 的目标；
- 路径穿越、外指 symlink 和非受管路径。

## 3. 先计划，后执行

先运行只读计划：

```bash
python3 "$BUTLER_PATH/tools/butler-upgrade/upgrade.py" plan \
  --project-root "$PROJECT_ROOT" --json
```

计划输出版本 gap、逐 action、执行域、预计文件变化、冲突和机器级待办。`inspect`/`plan` 对项目、Butler 仓与 HOME 都零写入。

按状态路由：

- `ready` / `ready-with-external-pending`：呈报清单，标准模式等 ACK；危险模式按自审门决定。
- `already-current`：无项目动作，回报当前版。
- `needs-decision`：队列经过 `[split]`，进入 §4。
- `manual-bootstrap`：无版本戳，不能确定配方链起点；走 `mcv-deployment.md` 首次部署/有人迁移，不默认覆盖。
- `conflict` / `locked`：停机，报告诊断；不得删除 marker、用户文件或锁来换绿。

## 4. `[split]` 人工决定

`.ai/PROJECT.md → .ai/project/` 是语义重组，继续保持 opt-in：

- **暂缓**：执行 `apply ... --split defer`。原单文件逐字保留，其余机械动作继续。
- **现在迁**：先运行 `plan ... --split now`。真实待拆时程序返回 `manual-split` 且零写入。**该路径自 ITER-0112 起已无目标形态**——知识文件夹机制已退役，`--split now` 只应出现在跨旧版本的历史升级链里；新项目遇到此状态应选 `defer`。

目标文件夹部分成形、旧单文件与 `00_INDEX.md` 同时存在都属于冲突，程序不猜测、不覆盖。

## 5. 项目内 apply

用户或危险模式自审放行后显式执行：

```bash
python3 "$BUTLER_PATH/tools/butler-upgrade/upgrade.py" apply \
  --project-root "$PROJECT_ROOT" --split defer --json
```

程序按以下顺序工作：

1. 校验 manifest 全链、recipe 一一覆盖、版本/marker/所有权与全部动作前置条件。
2. 在内存生成最终文件图；冲突在任何运行区/目标写入前返回。
3. apply 前复核 before SHA-256，拒绝计划后发生的并发修改。
4. 排他创建 `.ai/butler-upgrade/apply.lock`，写 run backup/restore/journal。
5. 原子替换登记文件。失败只恢复本次已触及文件，不调用 `git reset`/`checkout`，不覆盖其他工作树改动。

项目 action 有限且 schema 化：双入口重生成/重戳、hook + settings 同步、显式 rename/add-field、项目配置迁移 `migrate_config`、no-op。`migrate_config` 复用 `tools/project-config/` 的纯迁移计划，并由本升级器把 JSON 创建和 Markdown 收窄纳入同一 backup/restore/journal。历史 `[regen-claude]` 归一为双入口动作。未知 action/字段/domain 立即失败。

入口外原文和 CLAUDE.md/AGENTS.md 各自 `<!-- user-managed -->` 区逐字保留；`.ai/references/`（含用户原件 `raw/`）、`deliveries/`、历史 `.ai/iterations/` / `.ai/milestones/` 不在可写集合。

## 6. 机器级动作分域

`[global-install]` 修改 HOME，不属于项目事务。项目 plan 只列为 `external_pending`，apply 永不暗中执行。确需刷新机器能力时另行显式运行：

```bash
python3 "$BUTLER_PATH/tools/butler-upgrade/upgrade.py" global-install \
  --project-root "$PROJECT_ROOT" --confirm --json
```

该命令只报告安装器自身结果；失败不得把项目报告为 fully-complete。标准模式先取得用户确认；危险模式也必须把 HOME 边界写入审计，不因自治默认扩大权限。

## 7. 状态、恢复与验证

退出码与运行区完整契约见 `tools/butler-upgrade/README.md`。关键状态：0 成功/当前版、2 冲突、3 需决定、4 锁、5 失败已恢复、6 外部安装失败。

异常终止可能留下 lock。下次 plan 会 fail-closed；先检查：

```text
.ai/butler-upgrade/runs/<run-id>/journal.json
.ai/butler-upgrade/runs/<run-id>/restore.json
.ai/butler-upgrade/runs/<run-id>/backup/
```

不得不看 journal 就删除锁。确认文件已恢复或人工按 restore manifest 处理后，才可移除锁并重跑。

完成报告至少包含：

- 旧戳 → 当前 `VERSION`、队列范围和项目 action；
- apply status/run ID、两入口同戳、user-managed 保留；
- hook/settings 最终态和 rerun `already-current`；
- split 是已迁/暂缓/人工待办；
- `external_pending` 是否另行完成。

测试/复核结论必须引用 verification evidence record；不能只说“升级测试好了”。

## 8. 边界

- 不改 `.ai/references/`、`deliveries/`、任务四件套、历史归档或 CHANGELOG/BUG_LOG 内容。
- 不自动理解任意知识文本，不提供通用 shell action。
- Butler 仓自身的发布仍走 `versioning-schema.md`，不走本升级器。
- 版本 gap 决定迁移区间，内容/hash/marker/所有权校验决定是否安全写入；版本号不替代漂移检查。
