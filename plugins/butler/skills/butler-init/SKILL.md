---
name: butler-init
description: Deploy Butler base infrastructure into a new project. Use when the user asks to initialize Butler, set up Butler in a project, deploy the base car, or bootstrap a project with Butler.
---

# Butler Init

1. Resolve `BUTLER_PATH` through `Coder/20_Workflow_Lifecycle/mcv-deployment.md §0`; require `VERSION`, `scripts/render-project-entrypoints.py`, and `Coder/README.md`.
2. Resolve and echo `PROJECT_ROOT` through `Coder/20_Workflow_Lifecycle/mcv-deployment.md §0.1`.
3. Check for `.ai/` at `$PROJECT_ROOT`:
   - **Exists** → report "already deployed" and stop.
   - **Absent** → continue.
4. Read and execute `Coder/20_Workflow_Lifecycle/mcv-deployment.md` in full, section order:
   - **§1 Scout**: identify tech stack, project structure, matching profiles.
   - **§2 Scaffold**: create `.ai/` and `deliveries/`.
   - **§3 Rule injection**: run `render-project-entrypoints.py` to generate `CLAUDE.md` + `AGENTS.md`.
   - **§4 Local adaptation**: generate human-readable `.ai/local-constraints.md` plus safe-default `.ai/butler.config.json` through the resident project-config tool; store profiles only in JSON.
   - **§5 Hook injection**: copy hooks from `templates/hooks/` and configure `.claude/settings.json`.
5. Offer `$butler-setup` for machine-level command/extension installation and follow `Coder/20_Workflow_Lifecycle/butler-setup.md`; do not duplicate setup steps here. Execute only with the setup workflow's explicit confirmation.
6. Report: project root, tech stack/profiles, created directories, entrypoints, hooks status, global install result.
