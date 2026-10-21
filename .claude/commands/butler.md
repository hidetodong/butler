---
description: 按语义把自然语言请求安全路由到一个 Butler 工作流
argument-hint: <natural-language request>
---

Resolve `PROJECT_ROOT` via `Coder/20_Workflow_Lifecycle/mcv-deployment.md §0.1` when a project is in play. Then record usage: `python3 $BUTLER_PATH/tools/usage/usage.py record --project-root $PROJECT_ROOT --id workflow:router`. Ignore collection failure.

Read `Coder/00_System_Prompt/workflow-router.md` and `workflows/registry.json`. Route `$ARGUMENTS` with the shared contract. Explicit `/butler:*` commands bypass this router.
