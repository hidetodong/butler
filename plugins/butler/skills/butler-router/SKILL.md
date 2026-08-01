---
name: butler-router
description: Route an unqualified natural-language Butler request to exactly one registered workflow while preserving explicit-only safety boundaries.
---

# Butler Router

Resolve the trusted Butler checkout as `BUTLER_PATH`; if it is ambiguous, stop without writing.

1. Read `$BUTLER_PATH/Coder/00_System_Prompt/workflow-router.md` completely.
2. Read `$BUTLER_PATH/workflows/registry.json` and apply its current routing metadata.
3. Produce the shared route result and load only the selected workflow's rule source and Skill.
4. Never implicitly execute a high-risk workflow.
