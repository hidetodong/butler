---
name: butler-milestone
description: Create, split, defer, promote, or inspect Butler milestones from a product brief or roadmap. Use for multi-iteration planning, multiple unnumbered backlog directions, one-direction-per-file storage, start, withdrawal-before-work, or status requests.
---

# Butler Milestone

1. Resolve `BUTLER_PATH`; require `Coder/README.md`, otherwise stop with setup guidance.
2. Resolve `PROJECT_ROOT` through `${BUTLER_PATH}/Coder/20_Workflow_Lifecycle/mcv-deployment.md §0.1`; user-named paths outrank cwd, and ambiguity must stop without writes.
3. Read `${BUTLER_PATH}/Coder/20_Workflow_Lifecycle/milestone-schema.md` and execute its intake, backlog promotion, or status branch.
4. Before synthesizing a milestone from a structured product document, apply the schema's PRD classification gate. If it is a PRD, also read `Coder/40_Context_Management/prd-split.md` and split before routing.
5. Treat discussion and start as separate decisions. If deferred input contains multiple directions that can be started independently, split them into peer backlog blocks first. Store exactly one direction per `.ai/milestone-backlog/<slug>.md`, with its own key and ledger row; do not combine independent directions in one draft. Keep route items of the same milestone together.
6. Index every deferred block separately in the unnumbered backlog section of `.ai/MILESTONES.md`, and do not change `current` or allocate `MILE-NNNN`.
7. Allocate the next formal milestone number only when starting or promoting a backlog draft (`start <候办键>`). Never pre-allocate milestone or future iteration numbers.
8. Reclaim an accidentally opened number only through schema §7.6: it must be the latest number with no linked iteration, archive, or delivery. Otherwise preserve the number and close or abandon it.
9. Keep milestone direction separate from iteration-level frozen acceptance criteria; unnumbered backlog drafts do not project a Goal or own iterations.
