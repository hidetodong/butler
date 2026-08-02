#!/usr/bin/env python3
"""Run a deterministic end-to-end Butler Explore dogfood scenario."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


TOOL_ROOT = Path(__file__).resolve().parent
BUTLER_ROOT = TOOL_ROOT.parents[1]
MAP_TOOL = BUTLER_ROOT / "tools/decision-map"
WORK_TOOL = BUTLER_ROOT / "tools/decision-work"
PROMOTION_TOOL = BUTLER_ROOT / "tools/decision-promotion"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


decision_map = _load("explore_dogfood_decision_map", MAP_TOOL / "engine.py")
decision_work = _load("explore_dogfood_decision_work", WORK_TOOL / "engine.py")
decision_promotion = _load("explore_dogfood_decision_promotion", PROMOTION_TOOL / "engine.py")


def _sha256(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def _snapshot(paths: list[Path]) -> dict[str, str]:
    snapshot: dict[str, str] = {}
    for path in paths:
        if path.is_dir():
            candidates = sorted(item for item in path.rglob("*") if item.is_file())
        else:
            candidates = [path] if path.is_file() else []
        for candidate in candidates:
            snapshot[str(candidate)] = _sha256(candidate.read_bytes())
    return snapshot


class Scenario:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.ai = root / ".ai"
        self.ai.mkdir(parents=True)
        self.map_id = "DMAP-0001"
        self.map_operations = 0
        self.work_operations = 0
        self._write_delivery_state()

    def _write_delivery_state(self) -> None:
        (self.ai / "ITERATIONS.md").write_text(
            "# 迭代台账\n\ncurrent: none\n\n"
            "| 迭代号 | 标题 | 状态 | 开启 | 收口 | 所属 milestone | 交付 |\n"
            "|---|---|---|---|---|---|---|\n"
            "| ITER-0001 | previous | closed | 2026-08-01 | 2026-08-01 | — | deliveries/previous.md |\n",
            encoding="utf-8",
        )
        (self.ai / "MILESTONES.md").write_text(
            "# 里程碑台账\n\ncurrent: MILE-0001\n\n"
            "| 里程碑号 | 标题 | 状态 | 开启 | 收口 | 含迭代 | 交付 |\n"
            "|---|---|---|---|---|---|---|\n"
            "| MILE-0001 | Structured questions | active | 2026-08-01 | — | — | — |\n",
            encoding="utf-8",
        )
        (self.ai / "MILESTONE.md").write_text(
            "# MILESTONE\n\n"
            "| 路线项 | 主题 / 范围切片 | 实际 ITER | 状态 |\n"
            "|---|---|---|---|\n"
            "| R1 | Host capability contract | — | planned |\n",
            encoding="utf-8",
        )

    def map_apply(self, kind: str, fields: dict[str, Any], operation_id: str, now: str) -> dict[str, Any]:
        request = {
            "schema_version": 1,
            "operation_id": operation_id,
            "operation": {"kind": kind, **fields},
        }
        planned = decision_map.plan(self.root, self.map_id, request, now)
        applied = decision_map.apply(self.root, planned, now)
        self.map_operations += 1
        return applied

    def work_apply(self, kind: str, fields: dict[str, Any], operation_id: str, now: str) -> dict[str, Any]:
        request = {
            "schema_version": 1,
            "operation_id": operation_id,
            "operation": {"kind": kind, "map_id": self.map_id, **fields},
        }
        planned = decision_work.plan(self.root, self.map_id, request, now)
        applied = decision_work.apply(self.root, planned, now)
        self.work_operations += 1
        return applied

    def initialize_map(self) -> dict[str, dict[str, Any]]:
        self.map_apply(
            "create_map",
            {
                "title": "Structured question card boundary",
                "destination": "Decide where native cards help without replacing text fallback or lifecycle gates",
            },
            "OP-dogfood-create",
            "2026-08-02T01:00:00Z",
        )
        self.map_apply(
            "add_fog",
            {"fog_id": "FOG-0001", "description": "Real cross-host time savings have not yet been observed"},
            "OP-dogfood-fog",
            "2026-08-02T01:01:00Z",
        )
        questions = {
            "DEC-0001": ("Which confirmations fit native cards versus text or HITL?", []),
            "DEC-0002": ("What host capability boundary can Butler honestly promise?", []),
            "DEC-0003": ("What evidence would justify a custom UI or external coordination layer?", ["DEC-0001", "DEC-0002"]),
        }
        for index, (decision_id, (question, dependencies)) in enumerate(questions.items(), 2):
            self.map_apply(
                "add_decision",
                {"decision_id": decision_id, "question": question, "depends_on": dependencies},
                f"OP-dogfood-add-{index - 1}",
                f"2026-08-02T01:0{index}:00Z",
            )
        initial = decision_map.inspect(self.root, self.map_id, "2026-08-02T01:06:00Z")
        claims: dict[str, dict[str, Any]] = {}
        for index, decision_id in enumerate(("DEC-0001", "DEC-0002"), 1):
            claims[decision_id] = self.map_apply(
                "claim",
                {"decision_id": decision_id, "owner": "r5-coordinator", "lease_seconds": 3600},
                f"OP-dogfood-claim-{index}",
                "2026-08-02T01:07:00Z",
            )
            claims[decision_id]["operation_id"] = f"OP-dogfood-claim-{index}"
        return {"initial": initial, "claims": claims}

    def research_and_absorb(self, claims: dict[str, dict[str, Any]]) -> dict[str, Any]:
        attempts = []
        for index, decision_id in enumerate(("DEC-0001", "DEC-0002"), 1):
            claim = claims[decision_id]
            attempts.append(
                {
                    "decision_id": decision_id,
                    "attempt_id": f"ATT-{index:04d}",
                    "confirmed_context": ["Use current Butler repository contracts as primary evidence"],
                    "constraints": ["No target-project writes by helper", "Do not invent unavailable host capabilities"],
                    "expected_output": ["Bounded recommendation", "Evidence pointers", "Uncertainties"],
                    "claim_operation_id": claim["operation_id"],
                    "claim_owner": claim["owner"],
                    "claim_token": claim["token"],
                    "requested_execution_mode": "parallel",
                }
            )
        self.work_apply(
            "prepare_attempts",
            {"work_type": "research", "max_parallel": 2, "attempts": attempts},
            "OP-dogfood-prepare-batch",
            "2026-08-02T01:08:00Z",
        )

        outcomes = {
            "DEC-0001": (
                "Use native cards only for bounded mutually exclusive confirmations; preserve text/HITL fallback",
                ["Coder/20_Workflow_Lifecycle/acceptance-schema.md", "Coder/20_Workflow_Lifecycle/tech-plan-schema.md"],
            ),
            "DEC-0002": (
                "Describe host capabilities, not internal tool names; Pi currently has gates but no semantic Router entry",
                ["plugins/butler/skills/butler-router/SKILL.md", "plugins/butler-pi/index.ts"],
            ),
        }
        before_absorb_revision = decision_map.inspect(self.root, self.map_id)["state"]["revision"]
        absorbable_before: list[bool] = []
        actual_modes: list[str] = []
        invalid_digest_probe: dict[str, Any] | None = None
        for index, decision_id in enumerate(("DEC-0001", "DEC-0002"), 1):
            attempt_id = f"ATT-{index:04d}"
            task_path = self.ai / "decision-work" / self.map_id / decision_id / attempt_id / "task.json"
            outcome, sources = outcomes[decision_id]
            result = {
                "status": "candidate",
                "actual_execution_mode": "serial",
                "fresh_context": False,
                "outcome": outcome,
                "rationale": "The repository contracts support this bounded conclusion",
                "evidence": [f"repo:{source}" for source in sources],
                "payload": {
                    "findings": [outcome],
                    "sources": sources,
                    "uncertainties": ["No cross-host elapsed-time study was run"],
                },
            }
            if index == 1:
                protected = [
                    self.ai / "decision-maps" / self.map_id,
                    self.ai / "decision-work" / self.map_id,
                ]
                before_invalid = _snapshot(protected)
                invalid_request = {
                    "schema_version": 1,
                    "operation_id": "OP-dogfood-invalid-digest-probe",
                    "operation": {
                        "kind": "record_result",
                        "map_id": self.map_id,
                        "decision_id": decision_id,
                        "attempt_id": attempt_id,
                        "task_sha256": "missing-prefix",
                        "result": result,
                    },
                }
                try:
                    decision_work.plan(self.root, self.map_id, invalid_request, "2026-08-02T01:08:30Z")
                except decision_work.DecisionWorkError as error:
                    invalid_digest_probe = {
                        "code": error.code,
                        "exit_code": error.exit_code,
                        "zero_writes": before_invalid == _snapshot(protected),
                    }
                else:  # pragma: no cover - fail loudly if the safety gate regresses
                    raise AssertionError("invalid task digest unexpectedly planned")
            self.work_apply(
                "record_result",
                {
                    "decision_id": decision_id,
                    "attempt_id": attempt_id,
                    "task_sha256": _sha256(task_path.read_bytes()),
                    "result": result,
                },
                f"OP-dogfood-record-{index}",
                "2026-08-02T01:09:00Z",
            )
            view = decision_work.inspect(self.root, self.map_id, decision_id, attempt_id, "2026-08-02T01:10:00Z")
            absorbable_before.append(view["attempts"][0]["derived"]["absorbable"])
            actual_modes.append(view["attempts"][0]["result"]["actual_execution_mode"])

        revision_after_record = decision_map.inspect(self.root, self.map_id)["state"]["revision"]
        for index, decision_id in enumerate(("DEC-0001", "DEC-0002"), 1):
            claim = claims[decision_id]
            self.work_apply(
                "absorb_result",
                {
                    "decision_id": decision_id,
                    "attempt_id": f"ATT-{index:04d}",
                    "owner": claim["owner"],
                    "token": claim["token"],
                    "resolve_operation_id": f"OP-dogfood-absorb-map-{index}",
                },
                f"OP-dogfood-absorb-{index}",
                "2026-08-02T01:11:00Z",
            )
        self.map_apply(
            "resolve",
            {
                "decision_id": "DEC-0003",
                "outcome": "Require observed multi-machine, multi-writer, query/notification, or scale blockers before building an external layer",
                "rationale": "The local workflow must first demonstrate a concrete limitation; theoretical future need is not enough",
                "evidence": ["decision:DEC-0001", "decision:DEC-0002"],
            },
            "OP-dogfood-resolve-3",
            "2026-08-02T01:12:00Z",
        )
        return {
            "requested_mode": "parallel",
            "actual_modes": actual_modes,
            "fresh_context": [False, False],
            "absorbable_before_absorb": absorbable_before,
            "record_changed_map": revision_after_record != before_absorb_revision,
            "invalid_digest_probe": invalid_digest_probe,
        }

    def recover_in_fresh_processes(self) -> dict[str, Any]:
        command = [
            sys.executable,
            str(TOOL_ROOT / "scenario.py"),
            "--inspect-project-root",
            str(self.root),
            "--map-id",
            self.map_id,
        ]
        completed = subprocess.run(command, check=True, capture_output=True, text=True)
        recovered = json.loads(completed.stdout)
        return {"command_count": 1, "transcript_reads": 0, **recovered}

    def promote(self) -> dict[str, Any]:
        request = {
            "schema_version": 1,
            "promotion_id": "PROM-0001",
            "source": {"map_id": self.map_id, "decision_ids": ["DEC-0003"]},
            "target": {"kind": "route-reference", "milestone_id": "MILE-0001", "route_id": "R1"},
        }
        planned = decision_promotion.plan(self.root, request, "2026-08-02T01:13:00Z")
        first = decision_promotion.apply(self.root, planned, "2026-08-02T01:14:00Z")
        second = decision_promotion.apply(self.root, planned, "2026-08-02T01:15:00Z")
        verified = decision_promotion.verify(self.root, "PROM-0001", "2026-08-02T01:16:00Z")
        return {
            "promotion_id": "PROM-0001",
            "first_idempotent": first["idempotent"],
            "replay_idempotent": second["idempotent"],
            "verify_status": verified["status"],
            "receipt_count": len(verified["checked"]),
        }

    def run(self) -> dict[str, Any]:
        initialized = self.initialize_map()
        work = self.research_and_absorb(initialized["claims"])
        recovery = self.recover_in_fresh_processes()
        promotion = self.promote()
        map_view = decision_map.inspect(self.root, self.map_id, "2026-08-02T01:17:00Z")
        map_verify = decision_map.verify(self.root, self.map_id, "2026-08-02T01:17:00Z")
        work_verify = decision_work.verify(self.root, self.map_id, "2026-08-02T01:17:00Z")
        state_roots = (self.ai / "decision-maps", self.ai / "decision-work", self.ai / "decision-promotions")
        persistent_json = [path for base in state_roots if base.exists() for path in base.rglob("*.json")]
        return {
            "schema_version": 1,
            "status": "ok",
            "map": {
                "map_id": self.map_id,
                "initial_frontier": initialized["initial"]["frontier"],
                "final_frontier": map_view["frontier"],
                "decision_count": len(map_view["state"]["decisions"]),
                "fog_count": len(map_view["state"]["fog"]),
                "map_operations": self.map_operations,
                "verify_status": map_verify["status"],
            },
            "work": {**work, "work_operations": self.work_operations, "verify_status": work_verify["status"]},
            "recovery": recovery,
            "promotion": promotion,
            "maintenance": {
                "persistent_json_files": len(persistent_json),
                "coordinator_apply_actions": self.map_operations + self.work_operations + 1,
            },
        }


def run_scenario() -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="butler-explore-dogfood-") as directory:
        return Scenario(Path(directory) / "project").run()


def inspect_persisted(project_root: str | Path, map_id: str) -> dict[str, Any]:
    root = Path(project_root).resolve()
    map_view = decision_map.inspect(root, map_id)
    work_view = decision_work.inspect(root, map_id)
    absorbable = [
        item for item in work_view["attempts"] if item["derived"]["absorbable"]
    ]
    if absorbable:
        next_action = "review and explicitly absorb the current candidate results"
    elif map_view["frontier"]:
        next_action = "select and claim a Decision from the current Frontier"
    elif any(item["status"] == "open" for item in map_view["state"]["fog"].values()):
        next_action = "collect evidence for the open Fog, or explicitly dismiss it; promotion remains optional"
    else:
        next_action = "explicitly choose whether to promote a resolved slice or close the Map"
    return {
        "destination": map_view["state"]["destination"],
        "frontier": map_view["frontier"],
        "decision_statuses": {
            identity: value["status"] for identity, value in map_view["state"]["decisions"].items()
        },
        "attempt_count": len(work_view["attempts"]),
        "attempt_relations": {
            f"{item['decision_id']}/{item['attempt_id']}": item["derived"]["relation"]
            for item in work_view["attempts"]
        },
        "next_action": next_action,
        "read_objects": [
            f".ai/decision-maps/{map_id}/state.json",
            f".ai/decision-work/{map_id}/**/task.json",
            f".ai/decision-work/{map_id}/**/result.json",
        ],
    }


def verify_persisted(
    project_root: str | Path,
    map_id: str,
    milestone_id: str,
    route_id: str,
) -> dict[str, Any]:
    """Verify the live R5 dogfood state and a fail-closed promotion preflight without writes."""
    root = Path(project_root).resolve()
    ai = root / ".ai"
    errors: list[str] = []
    map_report = decision_map.verify(root, map_id, "2026-08-02T06:12:00Z")
    work_report = decision_work.verify(root, map_id, "2026-08-02T06:12:00Z")
    view = inspect_persisted(root, map_id)
    map_view = decision_map.inspect(root, map_id, "2026-08-02T06:12:00Z")
    work_view = decision_work.inspect(root, map_id, now="2026-08-02T06:12:00Z")

    if map_report["status"] != "ok":
        errors.append("decision-map verify failed")
    if work_report["status"] != "ok":
        errors.append("decision-work verify failed")
    if set(view["decision_statuses"].values()) != {"resolved"} or len(view["decision_statuses"]) != 3:
        errors.append("expected exactly three resolved decisions")
    open_fog = [item for item in map_view["state"]["fog"].values() if item["status"] == "open"]
    if len(open_fog) != 1:
        errors.append("expected exactly one open Fog")
    if view["attempt_count"] != 2 or set(view["attempt_relations"].values()) != {"absorbed"}:
        errors.append("expected exactly two absorbed attempts")
    actual_modes = [item["result"]["actual_execution_mode"] for item in work_view["attempts"]]
    fresh_context = [item["result"]["fresh_context"] for item in work_view["attempts"]]
    if actual_modes != ["serial", "serial"] or fresh_context != [False, False]:
        errors.append("live execution mode is not the recorded serial/non-fresh result")

    backlog = ai / "milestone-backlog" / "codex-structured-question-cards.md"
    if not backlog.is_file() or "候办状态: deferred" not in backlog.read_text(encoding="utf-8"):
        errors.append("dogfood source backlog is not deferred")
    milestone = ai / "MILESTONE.md"
    route_line = f"| {route_id} |"
    milestone_text = milestone.read_text(encoding="utf-8") if milestone.is_file() else ""
    matching_routes = [line for line in milestone_text.splitlines() if line.startswith(route_line)]
    if len(matching_routes) != 1 or "| active |" not in matching_routes[0] or "ITER-0106" not in matching_routes[0]:
        errors.append(f"{milestone_id}/{route_id} is not the active ITER-0106 route")

    receipt = ai / "decision-promotions" / "PROM-0001" / "receipt.json"
    protected = [
        ai / "decision-maps" / map_id,
        ai / "decision-work" / map_id,
        ai / "decision-promotions",
        ai / "ITERATIONS.md",
        ai / "MILESTONES.md",
        ai / "MILESTONE.md",
        backlog,
    ]
    before = _snapshot(protected)
    refusal: dict[str, Any]
    request = {
        "schema_version": 1,
        "promotion_id": "PROM-0001",
        "source": {"map_id": map_id, "decision_ids": ["DEC-0003"]},
        "target": {"kind": "route-reference", "milestone_id": milestone_id, "route_id": route_id},
    }
    try:
        decision_promotion.plan(root, request, "2026-08-02T06:12:00Z")
    except decision_promotion.DecisionPromotionError as error:
        refusal = {"code": error.code, "exit_code": error.exit_code}
        if error.code != "route_unavailable" or error.exit_code != 1:
            errors.append(f"unexpected promotion refusal: {error.code}/{error.exit_code}")
    else:
        refusal = {"code": "not-refused", "exit_code": 0}
        errors.append("live promotion unexpectedly planned")
    after = _snapshot(protected)
    zero_semantic_writes = before == after and not receipt.exists()
    if not zero_semantic_writes:
        errors.append("promotion preflight changed protected state or created a receipt")

    return {
        "schema_version": 1,
        "status": "ok" if not errors else "error",
        "errors": errors,
        "map_verify": map_report["status"],
        "work_verify": work_report["status"],
        "recovery": view,
        "actual_modes": actual_modes,
        "fresh_context": fresh_context,
        "backlog_deferred": "候办状态: deferred" in backlog.read_text(encoding="utf-8") if backlog.is_file() else False,
        "promotion_refusal": refusal,
        "zero_semantic_writes": zero_semantic_writes,
        "promotion_receipt_exists": receipt.exists(),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inspect-project-root")
    parser.add_argument("--verify-project-root")
    parser.add_argument("--map-id")
    parser.add_argument("--milestone-id")
    parser.add_argument("--route-id")
    args = parser.parse_args(argv)
    try:
        if args.inspect_project_root and args.verify_project_root:
            parser.error("choose only one of --inspect-project-root and --verify-project-root")
        if args.inspect_project_root:
            if not args.map_id or args.milestone_id or args.route_id:
                parser.error("inspect requires --map-id and no delivery target")
            report = inspect_persisted(args.inspect_project_root, args.map_id)
        elif args.verify_project_root:
            if not all((args.map_id, args.milestone_id, args.route_id)):
                parser.error("verify requires --map-id, --milestone-id, and --route-id")
            report = verify_persisted(
                args.verify_project_root,
                args.map_id,
                args.milestone_id,
                args.route_id,
            )
        else:
            if any((args.map_id, args.milestone_id, args.route_id)):
                parser.error("map and delivery target arguments require inspect or verify mode")
            report = run_scenario()
    except Exception as error:  # pragma: no cover - CLI safety envelope
        print(json.dumps({"schema_version": 1, "status": "error", "error": str(error)}, ensure_ascii=False, sort_keys=True))
        return 1
    print(json.dumps(report, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0 if report.get("status", "ok") == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
