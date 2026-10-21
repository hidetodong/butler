from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TOOL = ROOT / "tools" / "preference-experiment" / "experiment.py"
sys.path.insert(0, str(TOOL.parent))
import experiment  # noqa: E402


def run(root: Path, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(TOOL), "--project-root", str(root)],
        text=True,
        capture_output=True,
        check=False,
        env=env,
    )


class ExperimentTests(unittest.TestCase):
    def test_two_runs_match_and_report_no_change(self) -> None:
        first = run(ROOT)
        second = run(ROOT)
        self.assertEqual(0, first.returncode, first.stderr)
        self.assertEqual(first.stdout, second.stdout)
        payload = json.loads(first.stdout)
        fixture = experiment.load_fixture()
        preference = fixture["general_preference"]
        self.assertLess(preference.index("保持冻结"), preference.index("删除"))
        self.assertEqual(["删除", "保持冻结"], fixture["options"])
        self.assertEqual(fixture["options"], payload["order_off"])
        self.assertEqual(payload["order_off"], payload["order_on"])
        self.assertIs(False, payload["ranking_changed"])

    def test_ranker_is_refused_instead_of_true(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "proj"
            package = root / "pkg"
            package.mkdir(parents=True)
            (package / "rank.py").write_text(
                "def reorder_options(options, profile):\n    return list(reversed(options))\n",
                encoding="utf-8",
            )
            result = run(root)
        self.assertEqual(2, result.returncode)
        self.assertNotIn("ranking_changed", result.stdout)
        self.assertIn("ranker present", result.stderr)

    def test_does_not_create_external_preference_dir(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            pref = Path(temp) / "prefs"
            env = os.environ.copy()
            env["BUTLER_PREF"] = str(pref)
            result = run(ROOT, env)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertFalse(pref.exists())

    def test_true_result_keeps_files(self) -> None:
        decision = experiment.disposition({"ranking_changed": True, "order_off": ["a"], "order_on": ["b"]})
        self.assertEqual("keep", decision["action"])
        self.assertIn("反哺开、有监督、只参考通识层、排序变化", decision["required_text"])
        self.assertTrue((ROOT / "workflows" / "registry.json").is_file())

    def test_false_result_retires_preference_entry(self) -> None:
        registry = json.loads((ROOT / "workflows" / "registry.json").read_text(encoding="utf-8"))
        ids = {item["id"] for item in registry["workflows"]}
        self.assertNotIn("preference", ids)
        self.assertIn("loop", ids)
        for relative in (
            "Coder/70_Extension_Preference/preference-probe-engine.md",
            ".claude/commands/butler/preference.md",
            "plugins/butler/skills/butler-preference/SKILL.md",
            ".agents/skills/butler-preference",
        ):
            self.assertFalse((ROOT / relative).exists(), relative)
        self.assertTrue(TOOL.is_file())
        self.assertEqual("retire", experiment.disposition(json.loads(run(ROOT).stdout))["action"])

    def test_prose_counts_match_registry(self) -> None:
        registry = json.loads((ROOT / "workflows" / "registry.json").read_text(encoding="utf-8"))
        count = len(registry["workflows"])
        needle = f"{count} 个业务"
        for relative in (
            "HUMAN_GUIDE.md",
            "Coder/README.md",
            "docs/codex-compatibility.md",
        ):
            text = (ROOT / relative).read_text(encoding="utf-8")
            self.assertIn(needle, text, relative)

    def test_loop_stays_frozen_and_debt_is_closed(self) -> None:
        text = (ROOT / "Coder/55_Extension_ConvergenceLoop/convergence-loop-engine.md").read_text(encoding="utf-8")
        self.assertIn("最终处置是保持冻结", text)
        self.assertIn("没有最后调用时间", text)
        self.assertIn("不能当成已经证实没人用", text)
        self.assertNotIn("等 R13", text)
        debt = (ROOT / ".ai" / "debt.md").read_text(encoding="utf-8")
        self.assertNotIn("随 MILE-0016 R13 对 loop 做最终处置", debt)


if __name__ == "__main__":
    unittest.main()
