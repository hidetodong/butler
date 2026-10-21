---
description: 总结当前会话的已确认内容，并安全领取一个可审计迭代
argument-hint: [scope or constraints]
---

After `PROJECT_ROOT` is known, record usage with `python3 $BUTLER_PATH/tools/usage/usage.py record --project-root $PROJECT_ROOT --id workflow:iteration`. Ignore collection failure; do not invent a different id.

Read `Coder/20_Workflow_Lifecycle/iteration-intake.md` and follow it exactly. Treat `$ARGUMENTS` as additional scope, not as a raw transcript to persist.
