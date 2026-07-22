from contextlib import redirect_stdout
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from tools.inbox import inbox


NOW = "2026-07-22T10:00:00+08:00"


class InboxScannerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / ".ai").mkdir()
        (self.root / "origin").mkdir()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def run_cli(self, *args: str) -> tuple[int, dict]:
        output = io.StringIO()
        with redirect_stdout(output):
            code = inbox.main(list(args))
        return code, json.loads(output.getvalue())

    def scan(self, apply: bool = False) -> tuple[int, dict]:
        args = ["scan", "--project-root", str(self.root), "--now", NOW]
        if apply:
            args.append("--apply")
        return self.run_cli(*args)

    def test_plan_is_zero_write_and_apply_is_idempotent(self) -> None:
        source = self.root / "origin/需求.md"
        source.write_bytes(b"hello\r\n")
        before = hashlib.sha256(source.read_bytes()).hexdigest()
        code, plan = self.scan()
        self.assertEqual(0, code)
        self.assertEqual(1, plan["counts"]["added"])
        self.assertFalse((self.root / ".ai/INBOX.md").exists())
        code, applied = self.scan(True)
        self.assertEqual(0, code)
        self.assertTrue(applied["changed"])
        first = (self.root / ".ai/INBOX.md").read_bytes()
        code, repeated = self.scan(True)
        self.assertEqual(0, code)
        self.assertFalse(repeated["changed"])
        self.assertEqual(first, (self.root / ".ai/INBOX.md").read_bytes())
        self.assertEqual(before, hashlib.sha256(source.read_bytes()).hexdigest())

    def test_content_change_keeps_source_id(self) -> None:
        source = self.root / "origin/a.txt"
        source.write_text("v1", encoding="utf-8")
        self.scan(True)
        path = self.root / ".ai/INBOX.md"
        ledger = inbox.read_ledger(path)
        processed = "sha256:" + "0" * 64
        ledger.sources[0]["processed_sha256"] = processed
        ledger.sources[0]["status"] = "routed"
        path.write_text(inbox.render(ledger), encoding="utf-8")
        source.write_text("v2", encoding="utf-8")
        code, result = self.scan(True)
        self.assertEqual(0, code)
        self.assertEqual(1, result["counts"]["changed"])
        ledger = inbox.read_ledger(path)
        self.assertEqual("SRC-0001", ledger.sources[0]["source_id"])
        self.assertEqual("source-changed", ledger.sources[0]["status"])
        self.assertEqual(processed, ledger.sources[0]["processed_sha256"])

    def test_missing_source_is_preserved(self) -> None:
        source = self.root / "origin/a.txt"
        source.write_text("v1", encoding="utf-8")
        self.scan(True)
        source.unlink()
        code, result = self.scan(True)
        self.assertEqual(0, code)
        self.assertEqual(1, result["counts"]["missing"])
        ledger = inbox.read_ledger(self.root / ".ai/INBOX.md")
        self.assertEqual("SRC-0001", ledger.sources[0]["source_id"])
        self.assertIn("unavailable", ledger.sources[0]["note"])

    def test_symlink_is_rejected_and_not_followed(self) -> None:
        outside = self.root / "outside.txt"
        outside.write_text("secret", encoding="utf-8")
        (self.root / "origin/link.txt").symlink_to(outside)
        code, result = self.scan(True)
        self.assertEqual(0, code)
        self.assertEqual(1, result["counts"]["rejected"])
        self.assertEqual([], result["pending"])

    def test_control_character_locator_is_rejected(self) -> None:
        (self.root / "origin/bad\nname.md").write_text("secret", encoding="utf-8")
        code, result = self.scan(True)
        self.assertEqual(0, code)
        self.assertEqual(1, result["counts"]["rejected"])
        self.assertEqual("<control-character-path>", result["rejected"][0]["locator"])

    def test_subprocess_json_and_status_are_read_only(self) -> None:
        source = self.root / "origin/a.txt"
        source.write_bytes(b"raw\r\nbytes")
        before = hashlib.sha256(source.read_bytes()).hexdigest()
        command = [
            sys.executable, str(Path(inbox.__file__)), "scan", "--project-root", str(self.root),
            "--apply", "--now", NOW,
        ]
        result = subprocess.run(command, text=True, capture_output=True, check=False)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(1, json.loads(result.stdout)["counts"]["added"])
        ledger_before = (self.root / ".ai/INBOX.md").read_bytes()
        code, status = self.run_cli("status", "--project-root", str(self.root))
        self.assertEqual(0, code)
        self.assertFalse(status["changed"])
        self.assertEqual(ledger_before, (self.root / ".ai/INBOX.md").read_bytes())
        self.assertEqual(before, hashlib.sha256(source.read_bytes()).hexdigest())

    def test_content_outside_managed_block_is_preserved(self) -> None:
        path = self.root / ".ai/INBOX.md"
        original = "# My Notes\n\nkeep me  \n\t"
        path.write_text(original, encoding="utf-8")
        (self.root / "origin/a.txt").write_text("a", encoding="utf-8")
        self.scan(True)
        content = path.read_text(encoding="utf-8")
        self.assertTrue(content.startswith(original))
        ledger = inbox.read_ledger(path)
        ledger.suffix = "suffix-without-leading-newline"
        path.write_text(inbox.render(ledger), encoding="utf-8")
        self.scan(True)
        self.assertTrue(path.read_text(encoding="utf-8").endswith("suffix-without-leading-newline"))

    def test_broken_markers_fail_without_writing(self) -> None:
        path = self.root / ".ai/INBOX.md"
        original = "notes\n" + inbox.START + "\n"
        path.write_text(original, encoding="utf-8")
        code, result = self.scan(True)
        self.assertEqual(2, code)
        self.assertIn("markers", result["error"])
        self.assertEqual(original, path.read_text(encoding="utf-8"))

    def test_missing_origin_is_empty_and_not_created(self) -> None:
        (self.root / "origin").rmdir()
        code, result = self.scan(True)
        self.assertEqual(0, code)
        self.assertEqual(0, result["counts"]["added"])
        self.assertFalse((self.root / "origin").exists())

    def test_broken_origin_symlink_is_rejected(self) -> None:
        (self.root / "origin").rmdir()
        (self.root / "origin").symlink_to(self.root / "does-not-exist", target_is_directory=True)
        code, result = self.scan(True)
        self.assertEqual(0, code)
        self.assertEqual(1, result["counts"]["rejected"])

    def test_corrupt_source_id_fails_as_stable_json(self) -> None:
        (self.root / "origin/a.txt").write_text("a", encoding="utf-8")
        self.scan(True)
        path = self.root / ".ai/INBOX.md"
        original = path.read_text(encoding="utf-8").replace("SRC-0001", "BAD-ID", 1)
        path.write_text(original, encoding="utf-8")
        code, result = self.scan(True)
        self.assertEqual(2, code)
        self.assertIn("source_id", result["error"])
        self.assertEqual(original, path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
