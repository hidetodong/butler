---
title: Session-to-Iteration Intake
audience: claude,codex
scope: crystallize current session and start one Butler iteration
---

# Session-to-Iteration Intake

Use this workflow when the user asks to summarize the current session and start/claim an iteration for the agreed work.

## Intent gate

- Summary-only requests are read-only: return a concise summary and do not invoke `apply`.
- Starting an iteration requires explicit present-tense intent such as “领一个迭代做这个事情”, “start an iteration”, or an explicit host entry whose arguments ask to start.
- Never store the raw transcript. Crystallize only durable facts.

## Crystallization contract

Create a JSON spec matching `tools/iteration-intake/spec.schema.json`. Keep these categories separate:

- `confirmed_decisions`: choices the user explicitly accepted.
- `model_recommendations`: proposals not yet accepted as user decisions.
- `open_questions`: unresolved choices or missing facts.
- `in_scope` and `out_of_scope`: execution boundary.

Do not promote a recommendation into `confirmed_decisions`. Ask the user if that distinction changes the proposed scope materially.

## Deterministic execution

1. Resolve the real project root using `scripts/resolve-project-root.py` when it is not already certain.
2. Run `python3 "$BUTLER_PATH/tools/iteration-intake/intake.py" plan --project-root "$PROJECT_ROOT" --spec "$SPEC"` first. `plan` is always zero-write.
3. If it reports `active-exists`, do not allocate a new ID: in P1 propose merging the summary; in P2+ propose an in-iteration amendment or a later iteration.
4. If it reports `needs-milestone-route`, obtain the active milestone route before applying.
5. Show the crystallized scope and planned ID. Invoke `apply` only after the user has already given clear start intent.
6. `apply` owns ledger allocation, five live artifacts, task state, state index, milestone attribution, and handoff synchronization as one rollback-capable operation.

On success, report the new iteration ID, P1 status, and the next decision. On failure, report the error and leave no half-open iteration.
