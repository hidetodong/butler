---
name: butler-ideation
description: Explore and refine a product or engineering idea with Butler outside P1–P5. Use when the user explicitly requests brainstorming or accepts an Explore suggestion; promotion into delivery always restarts at Iteration P1.
---

# Butler Ideation

1. Resolve `BUTLER_PATH`; require `Coder/README.md`, otherwise stop with setup guidance.
2. Read `${BUTLER_PATH}/Coder/50_Extension_Ideation/ideation-engine.md` and follow it as the workflow source.
3. Keep the session outside P1–P5 until the user explicitly chooses to enter execution.
4. Challenge low-value scope, expose trade-offs, and keep the Decision Map limited to confirmed decisions, open questions, and references; candidate acceptance criteria are not frozen.
5. If the user promotes the result into execution, first resolve `PROJECT_ROOT` through `Coder/20_Workflow_Lifecycle/mcv-deployment.md §0.1`; cwd alone never selects the write target.
6. Route confirmed decisions into the normal Butler lifecycle at Iteration P1 under that root; never jump to P2 or let the Decision Map override Milestone or Iteration artifacts.
