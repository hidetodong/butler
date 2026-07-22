---
name: butler-inbox
description: Scan Butler requirement sources, classify pending items, and safely route them to PRD, ideation, milestone backlog, references, or record-only outcomes. Use when the user asks to inspect, import, classify, or process an origin/ requirement inbox.
---

# Butler Inbox

1. Resolve the Butler repository from `BUTLER_PATH`. If it is unset or does not contain `Coder/README.md`, stop; do not invent Butler rules.
2. Resolve the unique `PROJECT_ROOT` through `${BUTLER_PATH}/Coder/20_Workflow_Lifecycle/mcv-deployment.md §0.1`. Treat every `.ai/` path as relative to it, never to session cwd.
3. Read `${BUTLER_PATH}/Coder/40_Context_Management/inbox-schema.md` and then `inbox-workflow.md` completely.
4. Execute the requested `status`, `scan`, `apply`, or `route` branch. With no branch, use the zero-write scan plan.
5. Keep `origin/` read-only. Let the deterministic scanner own source facts and the referenced Butler workflows own derived artifacts.
6. In standard mode, wait for route confirmation. In dangerous mode, apply the workflow's self-review and audit gate; ambiguity still waits.
7. Report outcomes by source ID and distinguish completed, ignored, waiting, and failed items.
