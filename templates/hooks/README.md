---
title: Butler Hook Gate — 贡献者说明
audience: 开发者
scope: templates/hooks/ 的结构、运行机制、测试与应急流程
---

# Butler Hook Gate

`templates/hooks/` 是 butler 的 Claude Code PreToolUse hook SSOT。`mcv-deployment.md` 协议在部署目标项目时，把这里除 `tests/` 外的内容拷到目标 `.claude/hooks/`，并把 `../settings.hooks-snippet.json` 合并进目标 `.claude/settings.json`。

## 目录结构

```txt
butler_gate.py           # PreToolUse 入口
rules/
  protected_paths.py     # 拦 99_Business_Extension/
  phase_gate.py          # 拦源码路径在 P1/P2/P3 产物缺失时
  artifact_chain.py      # 占位，未来承载 AC-ID linkage 等规则
lib/
  io.py                  # Context, Decision, parse_stdin, resolve_target, is_gated, GATED_BLACKLIST
  bypass.py              # BUTLER_BYPASS 评估 + RUN_LOG 追加
tests/                   # 本目录的测试（不分发到目标项目）
```

## 运行机制

1. Claude Code 在 `Edit` / `Write` / `MultiEdit` 前通过 PreToolUse 调用 `python3 .claude/hooks/butler_gate.py`，stdin 传入 JSON。
2. Dispatcher 顺序执行 `RULE_MODULES`（`protected_paths → phase_gate → artifact_chain`），任一 `deny` 即终止。
3. `deny` 后走 `lib/bypass.py`：若 `BUTLER_BYPASS=1` 且 `.ai/bypass-reason.md` 非空，追加 `.ai/RUN_LOG.md` 后放行；否则 `exit 2` + stderr 给 AI 可读的违规摘要。
4. 任何未捕获异常由 dispatcher 顶层 catch，`exit 2`（**fail-closed**）。

## 退出码契约

| exit | 含义 |
|---|---|
| 0 | 放行（允许工具执行） |
| 2 | 拒绝（含规则 deny 与 internal error） |

## Bypass 流程

```bash
# 在目标项目根
echo "hotfix: XYZ in prod, will supplement AC after" > .ai/bypass-reason.md
BUTLER_BYPASS=1 claude ...     # 或直接在该 shell 里用 Claude Code
```

- `bypass-reason.md` **不会**被 hook 自动清理；同一会话内多次 bypass 会复用同一 reason 并在 `RUN_LOG.md` 留多条记录。
- 绕过 **会被 git 看见**（RUN_LOG 是追加历史），review 时可追问。

## Fail-closed 与应急流程

若 hook 自身有 bug 把你锁死（所有 Edit/Write 都 `exit 2`）：

1. 写 `.ai/bypass-reason.md`（非空）并设 `BUTLER_BYPASS=1` 绕过。
2. 在 butler 仓库提 issue，贴 stderr 里的 `internal error` 回溯。

## 本地测试

改 hook 后必须跑：

```bash
cd templates/hooks
python3 -m pytest tests/         # Tier 1 + Tier 2
bash tests/smoke.sh              # Tier 3（可选，不入 CI）
```

## 已测试的 Claude Code 版本

- 待补（首次部署后验证过的版本号写在这里）

## 平台支持

- macOS、Linux
- Windows 不在本 phase 范围
