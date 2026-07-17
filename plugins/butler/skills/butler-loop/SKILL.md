---
name: butler-loop
description: Explicitly run Butler's high-intensity convergence loop for a current P4 implementation. Invoke only when the user names $butler-loop or explicitly asks for Butler's convergence loop; never infer this high-cost mode from a routine request.
---

# Butler Convergence Loop

1. State that this is a high-intensity, potentially long-running and costly mode. Do not proceed if the user did not explicitly invoke this skill.
2. Resolve `BUTLER_PATH`; require `Coder/README.md`, otherwise stop with setup guidance.
3. Resolve the P4 `PROJECT_ROOT` through `Coder/20_Workflow_Lifecycle/mcv-deployment.md §0.1`; never infer it from session cwd alone.
4. Read `${BUTLER_PATH}/Coder/55_Extension_ConvergenceLoop/convergence-loop-engine.md` and `Coder/30_Quality_Gate/correction-contract.md`.
5. Run the referenced execute → probe → reflect → correct loop only under that root. Preserve its quantitative fuse and prohibition on fake-green fixes.
6. This mode has no persistent switch and no `off` command; it ends only on verified convergence or the referenced fuse/stop condition.
