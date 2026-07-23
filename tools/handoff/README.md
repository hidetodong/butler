# Handoff Tool

从 Butler 项目的权威状态生成和校验 `.ai/02_SESSION_HANDOFF.md`。

```bash
python3 tools/handoff/handoff.py inspect --project-root /path/to/project
python3 tools/handoff/handoff.py sync --project-root /path/to/project
python3 tools/handoff/handoff.py check --project-root /path/to/project
```

`inspect` 与 `check` 零写入。`check` 返回 0=fresh、1=stale、2=输入或状态非法；`sync` 原子更新 handoff 和 `.ai/handoff-state.json`。handoff 与 receipt 都是派生产物，人工决定必须先写入 task-state、阶段产物或台账。
