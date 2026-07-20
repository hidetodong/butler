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
   - **§2 Scaffold**: create `.ai/`, `deliveries/`, `origin/`, and `.ai/project/` seed.
   - **§3 Rule injection**: run `render-project-entrypoints.py` to generate `CLAUDE.md` + `AGENTS.md`.
   - **§4 Local adaptation**: generate `.ai/local-constraints.md` with safe defaults.
   - **§5 Hook injection**: copy hooks from `templates/hooks/` and configure `.claude/settings.json`.
5. Offer to run `bash "$BUTLER_PATH/scripts/setup.sh"` for global command/extension installation. Execute only with explicit user confirmation.
6. Report: project root, tech stack/profiles, created directories, entrypoints, hooks status, global install result.
