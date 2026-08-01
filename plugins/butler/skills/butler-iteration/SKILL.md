---
name: butler-iteration
description: Summarize the durable decisions from the current session and start one auditable Butler iteration. Use when the user asks to recap the discussion and claim or start an iteration for it; keep summary-only requests read-only.
---

# Butler Iteration

Resolve the trusted Butler checkout as `BUTLER_PATH` and the target project as `PROJECT_ROOT`; ambiguity is zero-write.

1. Read `$BUTLER_PATH/Coder/20_Workflow_Lifecycle/iteration-intake.md` completely.
2. Separate confirmed user decisions, model recommendations, open questions, in-scope work, and out-of-scope work.
3. Use the resident `$BUTLER_PATH/tools/iteration-intake/intake.py` plan/apply flow; never edit iteration state ad hoc.
4. Preserve the summary-only zero-write rule and the single-active-iteration invariant.
