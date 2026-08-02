from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from common import Harness


CLI = Path(__file__).resolve().parents[1] / "decision_promotion.py"


class DecisionPromotionCliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.h = Harness()
        self.h.source_chain()
        self.docs = tempfile.TemporaryDirectory(prefix="butler-promotion-cli-")
        self.doc_root = Path(self.docs.name)

    def tearDown(self) -> None:
        self.docs.cleanup()
        self.h.close()

    def write(self, name: str, value: dict) -> Path:
        path = self.doc_root / name
        path.write_text(json.dumps(value), encoding="utf-8")
        return path

    def run_cli(self, *args: str, expected: int = 0) -> dict:
        result = subprocess.run(["python3", str(CLI), *args], text=True, capture_output=True, check=False)
        self.assertEqual(expected, result.returncode, result.stderr or result.stdout)
        self.assertEqual("", result.stderr)
        value = json.loads(result.stdout)
        self.assertIsInstance(value, dict)
        return value

    def test_route_reference_cross_process_plan_apply_inspect_verify(self) -> None:
        spec = self.write("request.json", self.h.route_request())
        planned = self.run_cli("plan", "--project-root", str(self.h.root), "--spec", str(spec), "--now", "2026-08-02T01:00:00Z")
        plan_path = self.write("plan.json", planned)
        applied = self.run_cli("apply", "--project-root", str(self.h.root), "--plan", str(plan_path), "--now", "2026-08-02T01:01:00Z")
        self.assertFalse(applied["idempotent"])
        inspected = self.run_cli("inspect", "--project-root", str(self.h.root), "--milestone-id", "MILE-0002", "--route-id", "R1")
        self.assertEqual("PROM-0001", inspected["receipts"][0]["promotion_id"])
        verified = self.run_cli("verify", "--project-root", str(self.h.root))
        self.assertEqual("ok", verified["status"])

    def test_cli_duplicate_json_key_and_bad_filter_return_one_json_error(self) -> None:
        duplicate = self.doc_root / "duplicate.json"
        duplicate.write_text('{"schema_version":1,"schema_version":1}', encoding="utf-8")
        result = self.run_cli("plan", "--project-root", str(self.h.root), "--spec", str(duplicate), expected=2)
        self.assertEqual("invalid_document", result["code"])
        result = self.run_cli("inspect", "--project-root", str(self.h.root), "--milestone-id", "MILE-0002", expected=2)
        self.assertEqual("invalid_filter", result["code"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
