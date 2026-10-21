from __future__ import annotations

import json
import os
import stat
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
USAGE = ROOT / "tools" / "usage" / "usage.py"
sys.path.insert(0, str(ROOT / "tools" / "usage"))
import usage as usage_mod  # noqa: E402


class UsageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmpdir = self._tmp()
        (self.tmpdir / ".ai").mkdir()

    def _tmp(self) -> Path:
        import tempfile
        path = Path(tempfile.mkdtemp(prefix="butler-usage-"))
        self.addCleanup(lambda: __import__("shutil").rmtree(path, ignore_errors=True))
        return path

    def invoke(self, *args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(USAGE), *args],
            cwd=str(cwd or self.tmpdir),
            text=True,
            capture_output=True,
        )

    def test_record_and_show_roundtrip(self) -> None:
        first = self.invoke("record", "--project-root", str(self.tmpdir), "--id", "tool:intake")
        self.assertEqual(first.returncode, 0, first.stderr)
        payload = json.loads((self.tmpdir / ".ai/.usage.json").read_text(encoding="utf-8"))
        self.assertEqual(payload["schema_version"], 1)
        self.assertRegex(payload["entries"]["tool:intake"]["last_used"], usage_mod.TIMESTAMP_RE)
        self.assertEqual(set(payload["entries"]["tool:intake"]), {"last_used"})
        second = self.invoke("record", "--project-root", str(self.tmpdir), "--id", "tool:intake")
        self.assertEqual(second.returncode, 0, second.stderr)
        updated = json.loads((self.tmpdir / ".ai/.usage.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(
            updated["entries"]["tool:intake"]["last_used"],
            payload["entries"]["tool:intake"]["last_used"],
        )
        shown = self.invoke("show", "--project-root", str(self.tmpdir))
        self.assertEqual(json.loads(shown.stdout)["entries"]["tool:intake"]["last_used"], updated["entries"]["tool:intake"]["last_used"])

    def test_unknown_id_refuses_write(self) -> None:
        result = self.invoke("record", "--project-root", str(self.tmpdir), "--id", "tool:not-a-tool")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.tmpdir / ".ai/.usage.json").exists())

    def test_catalog_covers_registry_and_product_tools(self) -> None:
        allowed = usage_mod.allowed_ids()
        registry = json.loads((ROOT / "workflows/registry.json").read_text(encoding="utf-8"))
        for item in registry["workflows"]:
            self.assertIn(f"workflow:{item['id']}", allowed)
        self.assertIn("workflow:router", allowed)
        for name in usage_mod.PRODUCT_TOOLS:
            self.assertIn(f"tool:{name}", allowed)
        present = usage_mod.tool_dirs(ROOT / "tools")
        self.assertEqual(present, usage_mod.PRODUCT_TOOLS | usage_mod.SKIP_TOOLS)

    def test_skip_without_ai_directory(self) -> None:
        empty = self._tmp()
        result = self.invoke("record", "--project-root", str(empty), "--id", "tool:intake")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((empty / ".usage.json").exists())
        self.assertFalse((empty / ".ai").exists())

    def test_write_failure_is_fail_open(self) -> None:
        ai = self.tmpdir / ".ai"
        os.chmod(ai, stat.S_IREAD | stat.S_IEXEC)
        try:
            result = self.invoke("record", "--project-root", str(self.tmpdir), "--id", "tool:intake")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse((ai / ".usage.json").exists())
        finally:
            os.chmod(ai, stat.S_IRWXU)

    def test_gitignore_lists_usage_file(self) -> None:
        text = (ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn(".ai/.usage.json", text)

    def test_real_clis_stamp(self) -> None:
        commands = [
            ([sys.executable, str(ROOT / "tools/intake/intake.py"), "list", "--project-root", str(self.tmpdir)], "tool:intake"),
            ([sys.executable, str(ROOT / "tools/handoff/handoff.py"), "check", "--project-root", str(self.tmpdir)], "tool:handoff"),
            ([sys.executable, str(ROOT / "tools/goal-assurance/goal.py"), "evaluate", "--project-root", str(self.tmpdir)], "tool:goal-assurance"),
        ]
        (self.tmpdir / ".ai/ITERATIONS.md").write_text("current: none\n", encoding="utf-8")
        for command, entry in commands:
            result = subprocess.run(command, text=True, capture_output=True)
            self.assertTrue((self.tmpdir / ".ai/.usage.json").exists(), result.stderr)
            payload = json.loads((self.tmpdir / ".ai/.usage.json").read_text(encoding="utf-8"))
            self.assertIn(entry, payload["entries"], f"{entry} missing after {command}: {result.stderr}")

    def test_workflow_shells_mention_record(self) -> None:
        registry = json.loads((ROOT / "workflows/registry.json").read_text(encoding="utf-8"))
        expected = {item["id"] for item in registry["workflows"]} | {"router"}
        commands = ROOT / ".claude/commands"
        skills = ROOT / "plugins/butler/skills"
        found: set[str] = set()
        files = [commands / "butler.md", *sorted((commands / "butler").glob("*.md"))]
        files.extend(sorted(skills.glob("*/SKILL.md")))
        for path in files:
            text = path.read_text(encoding="utf-8")
            self.assertIn("usage.py record", text, path)
            for workflow in expected:
                token = f"workflow:{workflow}"
                if token in text:
                    found.add(workflow)
        self.assertEqual(found, expected)


if __name__ == "__main__":
    unittest.main()
