# Butler Upgrade Executor

`upgrade.py` 是已部署项目升级的可执行真源。它读取 `migrations/manifest.json`，不解析 Markdown 配方决定动作。

## Commands

```bash
python3 "$BUTLER_PATH/tools/butler-upgrade/upgrade.py" inspect --project-root "$PROJECT_ROOT"
python3 "$BUTLER_PATH/tools/butler-upgrade/upgrade.py" plan --project-root "$PROJECT_ROOT" --split defer
python3 "$BUTLER_PATH/tools/butler-upgrade/upgrade.py" apply --project-root "$PROJECT_ROOT" --split defer
```

加 `--json` 可获得稳定字段：`status`、版本区间、逐 action、文件变化、冲突、机器级待办和 run ID。`inspect` 与 `plan` 零写入；`apply` 才修改项目。

`[split]` 跨版本时：

- 不传决定：返回 `needs-decision`，零写入。
- `--split defer`：保留 `.ai/PROJECT.md`，继续机械升级。
- `--split now`：真实单文件待拆时返回 `manual-split`，交给有人语义迁移，零写入。

机器级安装不属于项目事务。只有显式执行下列命令才会修改 HOME：

```bash
python3 "$BUTLER_PATH/tools/butler-upgrade/upgrade.py" global-install \
  --project-root "$PROJECT_ROOT" --confirm
```

## Exit Codes

| Code | Meaning |
|---|---|
| 0 | ready/applied/already-current；机器级待办会另列，不冒充已执行 |
| 2 | 输入、版本、marker、路径、所有权或漂移冲突 |
| 3 | 需要 split/bootstrap/global confirmation |
| 4 | apply lock 存在，禁止并发或覆盖未决运行 |
| 5 | apply 失败，项目文件已恢复；journal 保留诊断 |
| 6 | 独立 global install 失败 |

## Transaction State

成功 preflight 后，apply 在目标项目创建：

```text
.ai/butler-upgrade/
├── apply.lock
└── runs/<run-id>/
    ├── journal.json
    ├── restore.json
    └── backup/<project-relative-path>
```

冲突发生在运行区创建前。执行会在每次写入前再次核 plan 的 before hash；失败只从本次 backup 恢复已触及文件，不调用 `git reset`/`checkout`，不覆盖其他用户改动。异常终止遗留 lock 时禁止新计划；先审阅对应 journal/backup，再人工恢复或移除锁。

## Manifest Contract

`migrations/manifest.json` 为执行数据真源。每个发布区间有严格连续的 source/target、人读 recipe 指针和有限 action；action ID 全局唯一，domain 只能由类型决定：

- `project`：入口、hook/settings、rename/add-field、restamp/no-op。
- `decision`：`split`。
- `machine`：`global_install`。

校验器要求所有 `migrations/v*.md` 与 manifest 一一对应。人读配方解释意图；程序绝不从其散文或标签正则生成写操作。
