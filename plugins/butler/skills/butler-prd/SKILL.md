---
name: butler-prd
description: Run Butler's multi-PRD workflow for a supplied product document, targeted PRD update, or read-only status request. Use when the user gives a PRD or asks to split, import, update, reconcile, list, or filter independently versioned PRDs by prd_id or workspace.
---

# Butler PRD

1. Resolve the Butler repository from `BUTLER_PATH`. If it is unset or does not contain `Coder/README.md`, stop and explain how to set it; do not invent Butler rules.
2. Resolve `PROJECT_ROOT` through `${BUTLER_PATH}/Coder/20_Workflow_Lifecycle/mcv-deployment.md §0.1`. A user-named repository outranks session cwd; ambiguity means no project writes.
3. Read `${BUTLER_PATH}/Coder/40_Context_Management/references-schema.md` first.
4. Route the request without reproducing the algorithm:
   - New or pasted PRD / `split`: read `prd-split.md`; run the four-state identity gate first. Only `new-requirement` may propose a dated `prd_id`, and the first-seen date needs project evidence or an explicit user value.
   - `update <prd_id> <new material>`: require the explicit registered identity, read `prd-update.md`, complete semantic diff/recognition/impact alignment into a confirmed spec, then invoke `${BUTLER_PATH}/tools/prd-update/prd_update.py plan`; call apply only when `apply_ready`. Never hand-edit live files or invent a receipt in the host adapter.
   - `status [prd_id] [--workspace key]`: read `prd-status.md` and invoke `${BUTLER_PATH}/tools/prd-status/prd_status.py status --project-root "${PROJECT_ROOT}"`, translating supplied filters to `--prd-id <id>` and/or `--workspace <key>`. Preserve its exit code and perform no writes.
5. Treat every `.ai/` path as relative to `PROJECT_ROOT`, not cwd or the Butler repository.
6. Preserve PRD text, independent identity, workspace scope, and versioning rules exactly as the referenced files require.
