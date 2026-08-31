---
name: butler-inbox
description: Capture a one-line idea into the Butler inbox, list the inbox and incubation layers read-only, or carry out an already-decided disposition (incubate, done, dropped, promote, iterate, withdraw). Use when the user wants to jot something down for later, review what is pending, or move an item one step along.
---

# Butler Inbox

1. Resolve the Butler repository from `BUTLER_PATH`. If it is unset or does not contain `Coder/README.md`, stop; do not invent Butler rules.
2. Resolve the unique `PROJECT_ROOT` through `${BUTLER_PATH}/Coder/20_Workflow_Lifecycle/mcv-deployment.md §0.1`. Treat every `.ai/` path as relative to it, never to session cwd.
3. Read `${BUTLER_PATH}/Coder/40_Context_Management/intake-schema.md` (data shape and the closed set of legal transitions) and then `intake-workflow.md` (action boundaries) completely.
4. Execute the requested `add`, `list`, or `handle` branch. With no branch, run the read-only `list`.
5. Route every structural write through `${BUTLER_PATH}/tools/intake/intake.py` with `--project-root <PROJECT_ROOT>`: inbox rows, deferred-table index rows, and a draft's header markers and section skeleton are never edited by hand. The one thing you do write with an editor is the draft body — replace the placeholder comments the tool left with real content.
6. The disposition decision is yours to ask about, not the tool's to guess: incubate or drop, which scale tier, why it is deferred or withdrawn. Ask first, then translate into flags. When a Chinese-only note yields no kebab key, ask the user for a short English slug instead of transliterating one.
7. In standard mode, confirm before any `handle` call. In dangerous mode, still stop when the scale tier or the reason is unclear.
8. Report the tool's receipt in plain language: the key, the resulting state, and which files were written. When a `current` pointer blocks an exit, say so and let the user decide; never close an active milestone or iteration to make room.
