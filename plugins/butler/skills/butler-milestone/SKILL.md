---
name: butler-milestone
description: Create or inspect a Butler milestone from a product brief, roadmap, or large requirement. Use when the user asks to open, plan, split, route, or show status for a multi-iteration milestone.
---

# Butler Milestone

1. Resolve `BUTLER_PATH`; require `Coder/README.md`, otherwise stop with setup guidance.
2. Resolve `PROJECT_ROOT` through `${BUTLER_PATH}/Coder/20_Workflow_Lifecycle/mcv-deployment.md §0.1`; user-named paths outrank cwd, and ambiguity must stop without writes.
3. Read `${BUTLER_PATH}/Coder/20_Workflow_Lifecycle/milestone-schema.md` and execute its intake or status branch.
4. Before synthesizing a milestone from a structured product document, apply the schema's PRD classification gate. If it is a PRD, also read `Coder/40_Context_Management/prd-split.md` and split before routing.
5. Write state only under `PROJECT_ROOT`. Never pre-allocate future iteration numbers.
6. Keep milestone direction separate from iteration-level frozen acceptance criteria.
