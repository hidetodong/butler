---
name: butler-dangerous
description: Explicitly control Butler's experimental unattended autonomy mode. Invoke only when the user names $butler-dangerous or clearly requests Butler dangerous mode; never infer autonomous authority from an ordinary request.
---

# Butler Dangerous Mode

1. Warn that this experimental mode grants long-running autonomous authority and is safest on an isolated, reversible branch or worktree. Do not enable it without explicit invocation.
2. Resolve `BUTLER_PATH`; require `Coder/README.md`, otherwise stop with setup guidance.
3. Before reading or writing the project switch, resolve `PROJECT_ROOT` through `Coder/20_Workflow_Lifecycle/mcv-deployment.md §0.1`. The session cwd alone never selects the project.
4. Read `${BUTLER_PATH}/Coder/65_Extension_Dangerous/dangerous-engine.md` and `Coder/20_Workflow_Lifecycle/local-constraints-schema.md` before changing state.
5. Route `status` as read-only, `off` as explicit shutdown, and empty/on as activation through the engine's risk gate. Persist state only under the resolved project root where the schema defines a project switch.
6. When active, preserve self-review ACK gates, audit logging, rollback anchors, P5 full review, residual-test admission rules, and stop conditions exactly as the engine defines them.
