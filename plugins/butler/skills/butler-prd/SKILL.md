---
name: butler-prd
description: Run Butler's PRD-first workflow for a supplied product document, PRD update, or PRD status request. Use when the user gives a PRD or asks to split, import, update, reconcile, or inspect versioned PRD references.
---

# Butler PRD

1. Resolve the Butler repository from `BUTLER_PATH`. If it is unset or does not contain `Coder/README.md`, stop and explain how to set it; do not invent Butler rules.
2. Read `${BUTLER_PATH}/Coder/40_Context_Management/references-schema.md` first.
3. Route the request without reproducing the algorithm:
   - New or pasted PRD: read and execute `prd-split.md`.
   - `update`: read and execute `prd-update.md` update flow.
   - `status`: read and execute `prd-update.md` status flow without writes.
4. Treat `.ai/` paths as relative to the user's current project, not the Butler repository.
5. Preserve PRD text and versioning rules exactly as the referenced files require.
