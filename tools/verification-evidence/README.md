# Verification Evidence

Butler 驻留的 P5 自动道证据工具。它执行明确的验证命令，把真实 argv、退出码、stdout/stderr 和摘要封存为可校验 record；`VERIFY_REPORT.md` 只解释并引用这些事实，不能反向手填 record。

## 调用

```bash
python3 "$BUTLER/tools/verification-evidence/evidence.py" run \
  --project-root "$PROJECT_ROOT" --iteration ITER-0001 \
  --id unit-tests --ac AC1,AC2 -- python3 -m pytest

python3 "$BUTLER/tools/verification-evidence/evidence.py" verify \
  --project-root "$PROJECT_ROOT" --iteration ITER-0001

python3 "$BUTLER/tools/verification-evidence/evidence.py" check-tdd \
  --project-root "$PROJECT_ROOT" --iteration ITER-0001

# 迭代置 closed、current 已为 none 后补捕获最终状态审计时，必须显式亮牌：
python3 "$BUTLER/tools/verification-evidence/evidence.py" run \
  --project-root "$PROJECT_ROOT" --iteration ITER-0001 --allow-closed \
  --id state-audit-closed --ac AC8 -- python3 scripts/audit-project-state.py --project-root .
```

`run` 后的命令按 argv 直接执行，不经过 shell。默认 timeout 900 秒、stdout/stderr 各最多持久化 1 MiB；任一输出截断会记 `incomplete`，不得作为通过证据。

## 轻量 TDD 配对

任务只有在 `TECH_PLAN.md` 的 `Test Strategy` 段显式声明 cycle 时才启用配对检查。未声明时 `check-tdd` 输出 N/A、零写返回成功。

```md
<!-- butler-tdd-cycles: v1 -->
| Cycle | AC | argv_json | cwd |
|---|---|---|---|
| parser | AC1,AC2 | `["python3","-m","pytest","tests/test_parser.py","-q"]` | `.` |
```

- cycle 名只用小写字母、数字和单连字符。
- Red evidence ID 固定为 `tdd-<cycle>-red`，必须是 `failed`。
- Green evidence ID 固定为 `tdd-<cycle>-green`，必须是 `passed`。
- 两条 record 的 argv、cwd、AC 必须与声明完全一致，且 Red 完整结束后才能开始 Green。
- record 继续使用 schema v1 固定三文件格式；不增加 sidecar、第二台账或新日志。

`--source archive` 会优先读取迭代归档内的 `TECH_PLAN.md` 和 evidence，供关闭态复核；归档计划不存在时兼容读取 live `TECH_PLAN.md`。本检查只证明 Butler 记录到同一命令先失败、后通过，不证明生产代码一定在 Red 后修改，也不判断失败原因是否有效。

## Record schema v1

每个 evidence ID 独占 `.ai/verification-evidence/<id>/`，目录内固定为 `record.json`、`stdout.log`、`stderr.log`。record 保存：

- evidence ID、迭代号、关联 AC；
- argv、项目相对 cwd、UTC 起止时间与 duration；
- 子进程退出码与 outcome；
- stdout/stderr 的原始字节数、保存字节数、SHA-256 和截断状态。

ID append-only，重复调用不会覆盖。工具不记录环境变量值，也不做可能漏秘密的启发式脱敏；只运行输出适合入仓的验证命令。可能包含 token、密钥或用户数据时，改用安全的机器摘要，不能直接捕获原始输出。

默认只允许给 `current` 迭代写/移动 evidence。`--allow-closed` 只在台账 `current: none` 且指定迭代行确为 `closed` 时放行，用于收口后的最终状态审计；它不会放宽任意历史或 active 指针不一致。

## Outcome / 退出码

| outcome | CLI exit | 含义 |
|---|---:|---|
| `passed` | 0 | 子进程 exit 0，双流完整 |
| `failed` | 1 | 子进程非零，失败证据已封存 |
| `launch_error` | 2 | 命令无法启动；错误证据已封存 |
| `incomplete` | 3 | 输出被截断，不得打绿 |
| `timeout` | 124 | 超时并终止进程组，超时证据已封存 |

参数、路径、schema 或重复 ID 错误同样退出 2，但不会伪造 record。

## 收口

P5 先 `verify --source hot`，再运行 `archive` 把整棵热区原子移动到 `.ai/iterations/ITER-NNNN/evidence/`，随后 `verify --source archive`。需要退回 P4 时用 `reopen` 整包移回；任何时刻不得同时保留 hot/archive 两份真源。
