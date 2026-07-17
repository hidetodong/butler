---
name: butler-upgrade
description: Upgrade an existing Butler-enabled project using the repository's versioned migration ledger. Use when the user asks to update, migrate, restamp, or check the Butler version gap in a deployed project.
---

# Butler Upgrade

1. Resolve `BUTLER_PATH`; require `VERSION`, `migrations/`, and `Coder/README.md`, otherwise stop with setup guidance.
2. Resolve the upgrade `PROJECT_ROOT` through `${BUTLER_PATH}/Coder/20_Workflow_Lifecycle/mcv-deployment.md §0.1`; user-named targets outrank cwd and ambiguity stops without writes.
3. Read `${BUTLER_PATH}/Coder/20_Workflow_Lifecycle/butler-upgrade.md` and `migration-schema.md` before changing the project.
4. Detect the deployed version under `PROJECT_ROOT`, compute the exact migration interval, and execute typed actions in order. Do not skip versions or infer absent recipes.
5. Preserve user-managed regions and stop on conflicts as the upgrade protocol requires.
6. Verify the final stamp and report every migration recipe applied. Do not upgrade the Butler repository itself unless explicitly asked.
