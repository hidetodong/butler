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

## Explore opt-in boundary

The user's original request is the only input to semantic trigger matching. If that request explicitly asks to brainstorm, explore, compare directions, or says the requirement is not yet clear, routing to the existing `ideation` workflow is an opt-in action.

Explicit Explore language includes the registered `ideation.semantic_triggers` such as Explore / 探索, Decision Map, cross-session decisions, Wayfinder, brainstorming, or an equally direct natural-language request to compare directions before delivery. This vocabulary is an auditable positive corpus, not a clarity or size classifier: absence of one literal phrase does not prove a request is clear, while vague wording alone does not authorize persistent Explore state.

If a Standard workflow later infers that exploration may help, that inference is not a new router input and must not silently reroute. Follow `Coder/20_Workflow_Lifecycle/lifecycle.md §1.1`: state the concrete blocker, suggest Explore, perform zero state writes, and wait for user consent. On consent, route to the same existing `ideation` workflow; never create an `explore` workflow or duplicate the exploration algorithm here.

The routing decision itself is zero-write. Returning `routed` only selects and loads a workflow; any later project write must pass that workflow's own consent, project-root, plan/apply, and lifecycle gates. `workflows/router-examples.json` is the executable representative corpus for this boundary, not another runtime router.

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
