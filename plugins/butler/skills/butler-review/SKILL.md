---
name: butler-review
description: Review code, documents, plans, or current changes with Butler's review protocol. Use for quick self-review, acceptance-criteria verification, full review, or an explicitly requested independent review.
---

# Butler Review

1. Resolve `BUTLER_PATH`; require `Coder/README.md`, otherwise stop with setup guidance.
2. Read `${BUTLER_PATH}/Coder/60_Extension_CodeReview/review-engine.md` and follow its scope, severity, and reporting contract.
3. For an independent review request, also read `Coder/62_Extension_Agents/overview.md` and `independent-review.md`. Use a fresh reviewer only when the current environment and user authorization allow it; otherwise disclose that the review is not independent.
4. Use the current project's frozen `.ai/AC_LIST.md` when present. Do not edit implementation files unless the user also asks for fixes.
5. Return findings first, ordered by severity, with precise paths and evidence.
