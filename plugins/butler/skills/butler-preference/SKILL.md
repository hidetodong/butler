---
name: butler-preference
description: Inspect or change Butler's preference-learning controls. Use when the user asks about preference consent, collection, reback, distillation, project suppression, or the status of Butler preference learning.
---

# Butler Preference

1. Resolve `BUTLER_PATH`; require `Coder/README.md`, otherwise stop with setup guidance.
2. Read `${BUTLER_PATH}/Coder/70_Extension_Preference/preference-probe-engine.md` before reading or changing preference state.
3. Route only the supported operations: status when no operation is supplied, global `on|off`, project suppression `project on|off`, `reback on|off`, or `distill`.
4. Global consent/data under `BUTLER_PREF` does not require a project root. Before accessing a project suppression switch, resolve `PROJECT_ROOT` through `Coder/20_Workflow_Lifecycle/mcv-deployment.md §0.1`; if it cannot be resolved, report that project suppression is not applicable and do not guess from cwd.
5. For status or project suppression, call project-config `resolve`. Surface source/conflicts and fail closed on error. Persist project suppression only with `set preference true|false` when `source=config`; require upgrade/init for legacy/missing and never edit legacy Markdown.
6. Preserve the separation between global consent/data under `BUTLER_PREF` and the project switch in `PROJECT_ROOT/.ai/butler.config.json`.
7. Never collect or infer preferences while Butler dangerous mode is active, and never treat model-made choices as human preference evidence.
