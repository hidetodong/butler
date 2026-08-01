---
title: Butler Workflow Router
audience: claude,codex
scope: host-neutral semantic routing
---

# Butler Workflow Router

This file is the single source of truth for routing an unqualified Butler request. Host adapters must remain thin and must not maintain their own intent tables.

## Entry and bypass

1. An explicit workflow entry such as `/butler:review` or `$butler-review` bypasses this router.
2. `/butler <natural language>` and implicit `$butler-router` invocation enter this router.
3. Load `workflows/registry.json`; never route to the top-level `router` object itself.

## Candidate selection

1. Compare the request with each workflow's description and `semantic_triggers`.
2. Remove candidates matched by a `negative_triggers` phrase or with unsatisfied `prerequisites`.
3. Use `conflicts_with` and `priority` only to resolve otherwise comparable candidates. Meaning wins over keyword count.
4. Select at most one primary workflow. Put sequential possibilities in `followups`; reassess them after the primary workflow completes.
5. If confidence is insufficient or two candidates remain materially tied, ask one concise disambiguating question and return `ambiguous`.
6. If the request does not concern Butler project/product workflow, return `not-butler`.

## Safety boundary

Any workflow with `allow_implicit_invocation: false`, including `loop` and `dangerous`, may only return `explicit-required`. State the canonical explicit entry and do not execute it.

## Result contract

Return this logical object before loading the selected workflow:

```json
{
  "status": "routed | ambiguous | explicit-required | not-butler",
  "primary_workflow": "workflow id or null",
  "followups": [],
  "reason": "short user-facing reason",
  "risk": "normal | high | none",
  "host_entry": "canonical entry or null",
  "requires_confirmation": false
}
```

For `routed`, load the selected workflow's `rule_source` and current host adapter, then follow that workflow exactly. Do not duplicate its lifecycle rules here.
