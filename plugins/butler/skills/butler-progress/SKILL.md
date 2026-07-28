---
name: butler-progress
description: Show structured progress for the current Butler-enabled project — milestone, iteration, goal, acceptance, execution, verification, risks. Use when the user asks for project progress, status overview, current state, or how things are going in a Butler project.
---

# Butler Progress

Read-only aggregation of the current project's Butler state into a fixed-format structured progress report.

1. Resolve `BUTLER_PATH`; require `Coder/README.md`, otherwise stop with setup guidance.
2. Resolve `PROJECT_ROOT` through `Coder/20_Workflow_Lifecycle/mcv-deployment.md §0.1`; cwd alone is not the project.
3. Check `$PROJECT_ROOT/.ai/` exists. If not, tell the user the project has no Butler deployment and suggest `/butler:init`. Do not proceed.
4. If arguments start with `brief`: read `.ai/task-state.md` only, output one line: `<project> │ <iteration or "none"> │ <phase or "—"> │ <status>`. Stop.
5. Otherwise run project-config `resolve` once and reuse its JSON result. Surface source, three switches, profiles, and `legacy_conflicts`; on failure mark project configuration fail-closed but continue read-only aggregation of other ledgers.
6. Produce the full 9-section report by reading these files (mark missing data as "无", never fabricate):
   - **§1 Project overview**: git remote name (or directory name), Butler version from managed `CLAUDE.md`/`AGENTS.md` stamps or `VERSION`, deployment status, resolved project configuration.
   - **§2 Milestone**: read `.ai/MILESTONES.md` — current pointer, title, status, route item count, backlog count.
   - **§3 Current iteration**: read `.ai/task-state.md` — iteration ID, milestone, phase (P1–P5), status, next action.
   - **§4 Goal state**: read Goal Calibration table from `.ai/task-state.md` — list open signals; derive Goal state per `goal-contract.md §3` priority chain.
   - **§5 Acceptance progress**: read `.ai/AC_LIST.md` — total count, confirmed/pending/failed breakdown, frozen status.
   - **§6 Execution progress**: read `.ai/TECH_PLAN.md` — plan verdict, steps done/total from `[x]`/`[ ]` counts.
   - **§7 Verification status**: read `.ai/VERIFY_REPORT.md` — auto/manual lane status, confidence level.
   - **§8 Risks & blockers**: aggregate open calibration signals, non-pass plan verdicts, failed verification items.
   - **§ Recent changes**: last 5 entries from `.ai/01_CHANGELOG.md`.
7. Output format: fixed section order §1–§9, tables for quantifiable data, consistent emoji (✅ done ⏳ pending ❌ failed ⚠️ risk — N/A). Start with a one-line summary: `<project> │ <iteration> │ <phase> │ <goal state>`.
8. Do NOT write any files. This command is strictly read-only.
