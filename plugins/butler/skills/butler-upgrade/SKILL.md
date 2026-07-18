---
name: butler-upgrade
description: Upgrade or inspect an existing Butler-enabled project through Butler's deterministic migration executor. Use when the user asks to update, migrate, restamp, or check the Butler version gap.
---

# Butler Upgrade

1. Resolve `BUTLER_PATH`; require `VERSION`, `migrations/manifest.json`, `tools/butler-upgrade/upgrade.py`, and `Coder/README.md`.
2. Resolve and echo `PROJECT_ROOT` through `Coder/20_Workflow_Lifecycle/mcv-deployment.md §0.1`. User-named targets outrank cwd; ambiguity stops without writes. Never target the Butler repository itself.
3. Read `Coder/20_Workflow_Lifecycle/butler-upgrade.md`. Do not parse Markdown recipes to invent or execute file actions.
4. Run the repository executor's `plan --project-root "$PROJECT_ROOT" --json`. Report the exact gap, actions/domains, changes, conflicts, split decision, and external pending work.
5. Standard mode requires user ACK; dangerous mode uses its mandatory self-review gate. Apply only with explicit `apply ... --split defer|now`.
6. Preserve the executor's status and exit semantics. Never delete markers, owner content, journals, or locks to force success.
7. `global-install` is a separate HOME mutation and requires separate explicit confirmation/audit; project apply never runs it.
8. Re-run plan after apply and report run ID, final stamp, idempotence, split state, and external pending actions.
