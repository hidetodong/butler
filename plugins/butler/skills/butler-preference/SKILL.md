---
name: butler-preference
description: Inspect or change Butler's preference-learning controls. Use when the user asks about preference consent, collection, reback, distillation, project suppression, or the status of Butler preference learning.
---

# Butler Preference

1. Resolve `BUTLER_PATH`; require `Coder/README.md`, otherwise stop with setup guidance.
2. Read `${BUTLER_PATH}/Coder/70_Extension_Preference/preference-probe-engine.md` before reading or changing preference state.
3. Route only the supported operations: status when no operation is supplied, `on`, `off`, `reback on|off`, or `distill`.
4. Global consent/data under `BUTLER_PREF` does not require a project root. Before accessing a project suppression switch, resolve `PROJECT_ROOT` through `Coder/20_Workflow_Lifecycle/mcv-deployment.md §0.1`; if it cannot be resolved, report that project suppression is not applicable and do not guess from cwd.
5. Preserve the separation between global consent/data and `PROJECT_ROOT/.ai/local-constraints.md`.
6. Never collect or infer preferences while Butler dangerous mode is active, and never treat model-made choices as human preference evidence.
