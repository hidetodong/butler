from __future__ import annotations

import importlib.util
import tempfile
from pathlib import Path


TOOL = Path(__file__).resolve().parents[1]
BUTLER = TOOL.parents[1]


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


promotion = load("decision_promotion_tests", TOOL / "engine.py")
decision_map = load("decision_promotion_tests_map", BUTLER / "tools/decision-map/engine.py")


class Harness:
    def __init__(self, *, milestone: bool = True) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="butler-decision-promotion-")
        self.root = Path(self.temp.name) / "project"
        self.ai = self.root / ".ai"
        self.ai.mkdir(parents=True)
        self.map_id = "DMAP-0001"
        self._write_iteration_ledger()
        self.set_milestone(milestone)
        for name in promotion.ITERATION_INTAKE.LIVE:
            (self.ai / name).write_text(f"old {name}\n", encoding="utf-8")
        (self.ai / "task-state.md").write_text("old task state\n", encoding="utf-8")
        self.map_apply("create_map", title="Choose delivery", destination="Resolved delivery slice", operation_id="OP-create")

    def close(self) -> None:
        self.temp.cleanup()

    def _write_iteration_ledger(self) -> None:
        (self.ai / "ITERATIONS.md").write_text(
            "# 迭代台账\n\ncurrent: none\n\n"
            "| 迭代号 | 标题 | 状态 | 开启 | 收口 | 所属 milestone | 交付 |\n"
            "|---|---|---|---|---|---|---|\n"
            "| ITER-0042 | old | closed | 2026-01-01 | 2026-01-01 | — | x |\n",
            encoding="utf-8",
        )

    def set_milestone(self, active: bool = True, *, route_status: str = "planned", iteration: str = "—") -> None:
        if active:
            (self.ai / "MILESTONES.md").write_text(
                "# 里程碑台账\n\ncurrent: MILE-0002\n\n"
                "| 里程碑号 | 标题 | 状态 | 开启 | 收口 | 含迭代 | 交付 |\n"
                "|---|---|---|---|---|---|---|\n"
                "| MILE-0002 | M | active | 2026-01-01 | — | — | — |\n",
                encoding="utf-8",
            )
            (self.ai / "MILESTONE.md").write_text(
                "# MILESTONE\n\n| 路线项 | 主题 / 范围切片 | 实际 ITER | 状态 |\n"
                "|---|---|---|---|\n"
                f"| R1 | Router | {iteration} | {route_status} |\n"
                "| R2 | Future | — | planned |\n",
                encoding="utf-8",
            )
        else:
            (self.ai / "MILESTONES.md").write_text(
                "# 里程碑台账\n\ncurrent: none\n\n"
                "| 里程碑号 | 标题 | 状态 | 开启 | 收口 | 含迭代 | 交付 |\n"
                "|---|---|---|---|---|---|---|\n"
                "| MILE-0001 | old | closed | 2025-01-01 | 2025-01-02 | ITER-0001 | x |\n",
                encoding="utf-8",
            )
            (self.ai / "MILESTONE.md").unlink(missing_ok=True)

    def map_spec(self, kind: str, *, operation_id: str, **fields) -> dict:
        return {"schema_version": 1, "operation_id": operation_id, "operation": {"kind": kind, **fields}}

    def map_apply(self, kind: str, *, operation_id: str, now: str = "2026-08-02T00:00:00Z", **fields) -> dict:
        spec = self.map_spec(kind, operation_id=operation_id, **fields)
        planned = decision_map.plan(self.root, self.map_id, spec, now)
        return decision_map.apply(self.root, planned, now)

    def add_resolved(self, identity: str, *, depends_on: list[str] | None = None, evidence: list[str] | None = None) -> None:
        number = int(identity.split("-")[1])
        self.map_apply("add_decision", operation_id=f"OP-add-{number}", decision_id=identity, question=f"Question {number}", depends_on=depends_on or [])
        self.map_apply(
            "resolve",
            operation_id=f"OP-resolve-{number}",
            decision_id=identity,
            outcome=f"Choose {number}",
            rationale=f"Reason {number}",
            evidence=evidence or [],
        )

    def route_request(self, promotion_id: str = "PROM-0001", roots: list[str] | None = None, route_id: str = "R1") -> dict:
        return {
            "schema_version": 1,
            "promotion_id": promotion_id,
            "source": {"map_id": self.map_id, "decision_ids": roots or ["DEC-0002"]},
            "target": {"kind": "route-reference", "milestone_id": "MILE-0002", "route_id": route_id},
        }

    def iteration_request(self, promotion_id: str = "PROM-0001", *, milestone: bool = True) -> dict:
        return {
            "schema_version": 1,
            "promotion_id": promotion_id,
            "source": {"map_id": self.map_id, "decision_ids": ["DEC-0002"]},
            "target": {
                "kind": "iteration-start",
                "milestone_id": "MILE-0002" if milestone else None,
                "route_id": "R1" if milestone else None,
                "intake": {
                    "title": "Promoted slice",
                    "summary": "Implement the chosen slice.",
                    "model_recommendations": [],
                    "open_questions": [],
                    "in_scope": ["Chosen slice"],
                    "out_of_scope": ["Other map work"],
                },
            },
        }

    def source_chain(self) -> None:
        self.add_resolved("DEC-0001")
        self.add_resolved("DEC-0002", depends_on=["DEC-0001"])

    @staticmethod
    def tree_bytes(root: Path, *, semantic: bool = False) -> dict[str, bytes]:
        values = {}
        for path in sorted(root.rglob("*")):
            if not path.is_file():
                continue
            relative = path.relative_to(root).as_posix()
            if semantic and relative.endswith(".lock"):
                continue
            values[relative] = path.read_bytes()
        return values
