from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).parents[1] / "handoff.py"
SPEC = importlib.util.spec_from_file_location("handoff_tool", MODULE_PATH)
assert SPEC and SPEC.loader
handoff = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(handoff)


class HandoffTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        ai = self.root / ".ai"
        ai.mkdir()
        (ai / "task-state.md").write_text(
            "# Task State\n\n- 当前迭代：ITER-0083\n- 当前里程碑：MILE-0010\n- 阶段：P3 Design → P4 Execute\n- 状态：active\n- 下一动作：实现工具。\n\n# Goal Calibration\n\nN/A\n",
            encoding="utf-8",
        )
        (ai / "ITERATIONS.md").write_text("current: ITER-0083\n| ITER-0083 | x | active | now | — | MILE-0010 | — |\n", encoding="utf-8")
        (ai / "MILESTONES.md").write_text("current: MILE-0010\n| MILE-0010 | x | active | now | — | ITER-0083 | — |\n", encoding="utf-8")
        (ai / "MILESTONE.md").write_text("# milestone\n", encoding="utf-8")
        (ai / "CONCEPT.md").write_text("# Current Understanding\n- 派生视图。\n# Open Questions\n- 无\n", encoding="utf-8")
        (ai / "AC_LIST.md").write_text("# Goal\n- x\n", encoding="utf-8")
        (ai / "TECH_PLAN.md").write_text("# Design Decisions\n- 使用 sidecar。\n# Risks / Open Questions\n- stop hook 不统一。\n", encoding="utf-8")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_sync_check_and_idempotence(self) -> None:
        first = handoff.sync(self.root)
        self.assertTrue(first["changed"])
        before = (self.root / ".ai/02_SESSION_HANDOFF.md").read_bytes()
        second = handoff.sync(self.root)
        self.assertFalse(second["changed"])
        self.assertEqual(before, (self.root / ".ai/02_SESSION_HANDOFF.md").read_bytes())
        code, result = handoff.check(self.root)
        self.assertEqual((code, result["status"]), (0, "fresh"))
        text = before.decode()
        self.assertEqual(text.count("## "), 6)
        self.assertIn("使用 sidecar", text)

    def test_source_change_and_tamper_are_stale(self) -> None:
        handoff.sync(self.root)
        task = self.root / ".ai/task-state.md"
        task.write_text(task.read_text().replace("实现工具", "继续测试"), encoding="utf-8")
        code, result = handoff.check(self.root)
        self.assertEqual(code, 1)
        self.assertIn("sources-changed", result["reasons"])
        handoff.sync(self.root)
        target = self.root / ".ai/02_SESSION_HANDOFF.md"
        target.write_text(target.read_text() + "tamper\n", encoding="utf-8")
        code, result = handoff.check(self.root)
        self.assertEqual(code, 1)
        self.assertIn("handoff-tampered", result["reasons"])

    def test_missing_and_invalid_receipt(self) -> None:
        code, result = handoff.check(self.root)
        self.assertEqual(code, 1)
        self.assertEqual(result["reasons"], ["handoff-missing", "receipt-missing"])
        handoff.sync(self.root)
        (self.root / ".ai/handoff-state.json").write_text("{", encoding="utf-8")
        code, result = handoff.check(self.root)
        self.assertEqual(code, 1)
        self.assertIn("receipt-invalid", result["reasons"])

    def test_no_active_and_no_milestone_ledger(self) -> None:
        ai = self.root / ".ai"
        (ai / "task-state.md").write_text(
            "- 当前迭代：无 active\n- 当前里程碑：none\n- 阶段：—\n- 状态：idle\n- 下一动作：等待。\n",
            encoding="utf-8",
        )
        (ai / "ITERATIONS.md").write_text("current: none\n", encoding="utf-8")
        (ai / "MILESTONES.md").unlink()
        result = handoff.sync(self.root)
        self.assertEqual(result["status"], "fresh")
        receipt = json.loads((ai / "handoff-state.json").read_text())
        self.assertEqual(receipt["snapshot"]["iteration"], "none")

    def test_task_ledger_mismatch_and_symlink_fail(self) -> None:
        (self.root / ".ai/ITERATIONS.md").write_text("current: none\n", encoding="utf-8")
        with self.assertRaises(handoff.HandoffError):
            handoff.inspect(self.root)

    def test_second_write_failure_rolls_back_pair(self) -> None:
        handoff.sync(self.root)
        ai = self.root / ".ai"
        old_handoff = (ai / "02_SESSION_HANDOFF.md").read_bytes()
        old_receipt = (ai / "handoff-state.json").read_bytes()
        task = ai / "task-state.md"
        task.write_text(task.read_text().replace("实现工具", "改变状态"), encoding="utf-8")
        original = handoff.atomic_write
        calls = 0

        def fail_second(path, data):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("injected")
            return original(path, data)

        handoff.atomic_write = fail_second
        try:
            with self.assertRaises(OSError):
                handoff.sync(self.root)
        finally:
            handoff.atomic_write = original
        self.assertEqual(old_handoff, (ai / "02_SESSION_HANDOFF.md").read_bytes())
        self.assertEqual(old_receipt, (ai / "handoff-state.json").read_bytes())
        (self.root / ".ai/ITERATIONS.md").unlink()
        (self.root / ".ai/ITERATIONS.md").symlink_to("task-state.md")
        with self.assertRaises(handoff.HandoffError):
            handoff.inspect(self.root)


if __name__ == "__main__":
    unittest.main()
