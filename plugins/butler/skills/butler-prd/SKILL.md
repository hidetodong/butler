---
name: butler-prd
description: Run Butler's PRD-first workflow for a supplied product document, PRD update, or PRD status request. Use when the user gives a PRD or asks to split, import, update, reconcile, or inspect versioned PRD references.
---

# Butler PRD

1. Resolve the Butler repository from `BUTLER_PATH`. If it is unset or does not contain `Coder/README.md`, stop and explain how to set it; do not invent Butler rules.
2. Resolve `PROJECT_ROOT` through `${BUTLER_PATH}/Coder/20_Workflow_Lifecycle/mcv-deployment.md §0.1`. A user-named repository outranks session cwd; ambiguity means no project writes.
3. Read `${BUTLER_PATH}/Coder/40_Context_Management/references-schema.md` first.
4. Route the request without reproducing the algorithm:
   - New or pasted PRD: read and execute `prd-split.md`.
   - `update`: read and execute `prd-update.md` update flow.
   - `status`: read and execute `prd-update.md` status flow without writes.
5. Treat every `.ai/` path as relative to `PROJECT_ROOT`, not cwd or the Butler repository.
6. Preserve PRD text and versioning rules exactly as the referenced files require.
