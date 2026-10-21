from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
REPORT = ROOT / "tools" / "usage-report" / "usage_report.py"
sys.path.insert(0, str(ROOT / "tools" / "usage-report"))
sys.path.insert(0, str(ROOT / "tools" / "usage"))
import usage as usage_mod  # noqa: E402
import usage_report as report_mod  # noqa: E402

NOW = "2026-09-14T00:00:00Z"
ALLOWED = {"tool:intake", "tool:handoff", "tool:usage"}


class UsageReportTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmpdir = Path(tempfile.mkdtemp(prefix="butler-usage-report-"))
        self.addCleanup(lambda: __import__("shutil").rmtree(self.tmpdir, ignore_errors=True))
        (self.tmpdir / ".ai").mkdir()

    def invoke(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(REPORT), *args],
            cwd=str(self.tmpdir),
            text=True,
            capture_output=True,
        )

    def write_usage(self, entries: dict) -> None:
        payload = {"schema_version": 1, "entries": entries}
        path = self.tmpdir / ".ai" / ".usage.json"
        path.write_text(json.dumps(payload), encoding="utf-8")

    def test_cli_defaults_to_90_day_json(self) -> None:
        result = self.invoke("report", "--project-root", str(self.tmpdir))
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["since_days"], 90)
        self.assertRegex(payload["generated_at"], usage_mod.TIMESTAMP_RE)
        self.assertEqual(set(payload["buckets"]), set(report_mod.BUCKETS))

    def test_four_buckets_and_exact_cutoff(self) -> None:
        self.write_usage({
            "tool:intake": {"last_used": "2026-09-01T00:00:00Z"},
            "tool:handoff": {"last_used": "2026-01-01T00:00:00Z"},
            "workflow:retired": {"last_used": "2026-08-01T00:00:00Z"},
            "tool:broken": {"last_used": "yesterday"},
        })
        payload = report_mod.build_report(self.tmpdir, 90, NOW, allowed=ALLOWED)
        self.assertEqual(
            [item["id"] for item in payload["buckets"]["A"]],
            ["tool:intake"],
        )
        self.assertEqual(payload["buckets"]["A"][0]["last_used"], "2026-09-01T00:00:00Z")
        self.assertEqual(
            [item["id"] for item in payload["buckets"]["B"]],
            ["tool:handoff"],
        )
        self.assertEqual(
            [item["id"] for item in payload["buckets"]["C"]],
            ["tool:usage"],
        )
        self.assertIsNone(payload["buckets"]["C"][0]["last_used"])
        self.assertEqual(
            [item["id"] for item in payload["buckets"]["D"]],
            ["tool:broken", "workflow:retired"],
        )
        broken = next(item for item in payload["buckets"]["D"] if item["id"] == "tool:broken")
        self.assertIsNone(broken["last_used"])
        edge = report_mod.cutoff_stamp(NOW, 90)
        self.write_usage({"tool:intake": {"last_used": edge}})
        on_edge = report_mod.build_report(self.tmpdir, 90, NOW, allowed={"tool:intake"})
        self.assertEqual(on_edge["buckets"]["A"][0]["id"], "tool:intake")

    def test_since_7d_changes_boundary_and_illegal_values_fail(self) -> None:
        self.write_usage({"tool:intake": {"last_used": "2026-09-06T00:00:00Z"}})
        week = report_mod.build_report(self.tmpdir, 7, NOW, allowed={"tool:intake"})
        quarter = report_mod.build_report(self.tmpdir, 90, NOW, allowed={"tool:intake"})
        self.assertEqual(week["buckets"]["B"][0]["bucket"], "B")
        self.assertEqual(quarter["buckets"]["A"][0]["bucket"], "A")
        changed = self.invoke("report", "--project-root", str(self.tmpdir), "--since", "7d")
        self.assertEqual(changed.returncode, 0, changed.stderr)
        self.assertEqual(json.loads(changed.stdout)["since_days"], 7)
        for value in ("0d", "1h", "90"):
            refused = self.invoke("report", "--project-root", str(self.tmpdir), "--since", value)
            self.assertNotEqual(refused.returncode, 0, value)
            self.assertNotIn("since_days", refused.stdout)
            self.assertNotIn("buckets", refused.stdout)

    def test_missing_or_corrupt_file_lists_catalog_as_c(self) -> None:
        missing = self.invoke("report", "--project-root", str(self.tmpdir))
        self.assertEqual(missing.returncode, 0, missing.stderr)
        missing_payload = json.loads(missing.stdout)
        allowed = usage_mod.allowed_ids()
        self.assertEqual(self._ids(missing_payload, "C"), allowed)
        self.assertEqual(missing_payload["buckets"]["D"], [])
        path = self.tmpdir / ".ai" / ".usage.json"
        original = b'{"schema_version": 1, "entries": []}'
        path.write_bytes(original)
        corrupt = self.invoke("report", "--project-root", str(self.tmpdir))
        self.assertEqual(corrupt.returncode, 0, corrupt.stderr)
        corrupt_payload = json.loads(corrupt.stdout)
        self.assertEqual(self._ids(corrupt_payload, "C"), allowed)
        self.assertEqual(corrupt_payload["buckets"]["D"], [])
        self.assertEqual(path.read_bytes(), original)

    def test_report_covers_allowed_ids_exactly_once(self) -> None:
        self.write_usage({
            "tool:intake": {"last_used": "2026-09-01T00:00:00Z"},
            "workflow:retired": {"last_used": "2026-08-01T00:00:00Z"},
        })
        payload = report_mod.build_report(self.tmpdir, 90, NOW)
        allowed = usage_mod.allowed_ids()
        seen: list[str] = []
        for name in report_mod.BUCKETS:
            for item in payload["buckets"][name]:
                self.assertEqual(item["bucket"], name)
                seen.append(item["id"])
        self.assertEqual(len(seen), len(set(seen)))
        self.assertTrue(allowed.isdisjoint(self._ids(payload, "D")))
        self.assertEqual(self._ids(payload, "A") | self._ids(payload, "B") | self._ids(payload, "C"), allowed)
        self.assertEqual(self._ids(payload, "D"), {"workflow:retired"})

    def test_stamp_happens_after_the_snapshot(self) -> None:
        result = self.invoke("report", "--project-root", str(self.tmpdir))
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertIn("tool:usage-report", self._ids(payload, "C"))
        stored = json.loads((self.tmpdir / ".ai" / ".usage.json").read_text(encoding="utf-8"))
        self.assertRegex(stored["entries"]["tool:usage-report"]["last_used"], usage_mod.TIMESTAMP_RE)
        self.assertIn("usage-report", usage_mod.PRODUCT_TOOLS)

    def _ids(self, payload: dict, bucket: str) -> set[str]:
        return {item["id"] for item in payload["buckets"][bucket]}
