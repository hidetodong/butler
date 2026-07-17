---
name: butler-ideation
description: Explore and refine an unclear product or engineering idea with Butler without entering the execution lifecycle. Use for brainstorming, requirement discovery, trade-off analysis, MVP reduction, or shaping a vague request before implementation.
---

# Butler Ideation

1. Resolve `BUTLER_PATH`; require `Coder/README.md`, otherwise stop with setup guidance.
2. Read `${BUTLER_PATH}/Coder/50_Extension_Ideation/ideation-engine.md` and follow it as the workflow source.
3. Keep the session outside P1–P5 until the user explicitly chooses to enter execution.
4. Challenge low-value scope, expose trade-offs, and distinguish confirmed decisions from open ideas.
5. If the user promotes the result into execution, first resolve `PROJECT_ROOT` through `Coder/20_Workflow_Lifecycle/mcv-deployment.md §0.1`; cwd alone never selects the write target.
6. Route confirmed decisions into the normal Butler lifecycle under that root; do not treat brainstorm output as frozen acceptance criteria.
