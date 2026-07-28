---
name: butler-review
description: Review code, documents, plans, or current changes with Butler's review protocol. Use for quick self-review, acceptance-criteria verification, full review, or an explicitly requested independent review.
---

# Butler Review

1. Resolve `BUTLER_PATH`; require `Coder/README.md`, otherwise stop with setup guidance.
2. Resolve the review `PROJECT_ROOT` through `Coder/20_Workflow_Lifecycle/mcv-deployment.md §0.1`; cwd alone is not review scope.
3. Read `${BUTLER_PATH}/Coder/60_Extension_CodeReview/review-engine.md` and follow its scope, severity, and reporting contract.
4. For an independent review request, also read `Coder/62_Extension_Agents/overview.md` and `independent-review.md`. Use a fresh reviewer only when the current environment and user authorization allow it; otherwise disclose that the review is not independent.
5. Use `PROJECT_ROOT/.ai/AC_LIST.md` when present. Do not edit implementation files unless the user also asks for fixes.
6. For configuration-driven review, call project-config `resolve`; trigger only on `independent_review=true`, fail closed on read errors, and surface conflicts. Persist a project-level choice only with `set independent_review true|false` when `source=config`; legacy/missing requires upgrade/init.
7. Return findings first, ordered by severity, with precise paths and evidence.
