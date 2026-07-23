import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).parents[1] / "state_ledger.py"
SPEC = importlib.util.spec_from_file_location("state_ledger", MODULE_PATH)
sl = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(sl)


class StateLedgerTests(unittest.TestCase):
    def seed(self, iterations=125, milestones=3):
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        (root / ".ai").mkdir()
        iteration_lines = [
            "# 迭代台账",
            "",
            f"current: ITER-{iterations:04d}",
            "",
            "| 迭代号 | 标题 | 状态 | 开启 | 收口 | 所属 milestone | 交付 |",
            "|---|---|---|---|---|---|---|",
        ]
        for value in range(iterations, 0, -1):
            state = "active" if value == iterations else "closed"
            iteration_lines.append(
                f"| ITER-{value:04d} | item {value} | {state} | d | "
                f"{'—' if state == 'active' else 'd'} | MILE-{milestones:04d} | "
                f"{'—' if state == 'active' else f'deliveries/ITER-{value:04d}.md'} |"
            )
        milestone_lines = [
            "# 里程碑台账",
            "",
            f"current: MILE-{milestones:04d}",
            "",
            "| 里程碑号 | 标题 | 状态 | 开启 | 收口 | 含迭代 | 交付 |",
            "|---|---|---|---|---|---|---|",
        ]
        for value in range(milestones, 0, -1):
            state = "active" if value == milestones else "closed"
            milestone_lines.append(
                f"| MILE-{value:04d} | mile {value} | {state} | d | "
                f"{'—' if state == 'active' else 'd'} | ITER-{iterations:04d} | "
                f"{'—' if state == 'active' else f'deliveries/MILE-{value:04d}.md'} |"
            )
        (root / ".ai/ITERATIONS.md").write_text("\n".join(iteration_lines) + "\n", encoding="utf-8")
        (root / ".ai/MILESTONES.md").write_text("\n".join(milestone_lines) + "\n", encoding="utf-8")
        return temporary, root

    @staticmethod
    def tree_bytes(root):
        return {
            str(path.relative_to(root)): path.read_bytes()
            for path in sorted((root / ".ai").rglob("*"))
            if path.is_file()
        }

    def test_fixed_ranges_create_multiple_bounded_shards(self):
        temporary, root = self.seed(iterations=125)
        index = sl.migrate(root, hot_limit=20, shard_size=50)
        ledger = index["ledgers"]["iterations"]
        self.assertEqual((ledger["shard_count"], ledger["cold_count"]), (3, 105))
        shards = sorted((root / ".ai/history/iterations").glob("*.md"))
        self.assertEqual([path.name for path in shards], [
            "ITER-000001-000050.md",
            "ITER-000051-000100.md",
            "ITER-000101-000150.md",
        ])
        for path in shards:
            rows = sl.parse_rows(path.read_text(), "ITER", 7)
            self.assertLessEqual(len(rows), 50)
            receipt = json.loads(path.with_suffix(".json").read_text())
            self.assertEqual(receipt["count"], len(rows))
            self.assertEqual(receipt["sha256"], sl.digest(path.read_bytes()))
        self.assertEqual(len(sl.parse_rows((root / ".ai/ITERATIONS.md").read_text(), "ITER", 7)), 20)
        temporary.cleanup()

    def test_migrate_check_and_bytes_are_idempotent(self):
        temporary, root = self.seed()
        first = sl.migrate(root, 20, 50)
        before = self.tree_bytes(root)
        second = sl.migrate(root, 20, 50)
        self.assertEqual(first, second)
        self.assertEqual(before, self.tree_bytes(root))
        self.assertEqual(sl.check(root), first)
        temporary.cleanup()

    def test_lookup_reads_hot_or_one_cold_shard(self):
        temporary, root = self.seed()
        sl.migrate(root, 20, 50)
        code, cold = sl.lookup(root, "ITER-0042")
        self.assertEqual(code, 0)
        self.assertEqual(cold["source"], ".ai/history/iterations/ITER-000001-000050.md")
        code, hot = sl.lookup(root, "ITER-0125")
        self.assertEqual(code, 0)
        self.assertEqual(hot["source"], ".ai/ITERATIONS.md")
        code, missing = sl.lookup(root, "ITER-9999")
        self.assertEqual(code, 1)
        self.assertEqual(missing["status"], "not_found")
        temporary.cleanup()

    def test_lookup_rejects_hot_ledger_drift(self):
        temporary, root = self.seed()
        sl.migrate(root, 20, 50)
        hot = root / ".ai/ITERATIONS.md"
        hot.write_text(hot.read_text().replace("item 125", "tampered"), encoding="utf-8")
        with self.assertRaises(sl.Error):
            sl.lookup(root, "ITER-0125")
        temporary.cleanup()

    def test_long_identity_uses_numeric_order(self):
        temporary, root = self.seed(iterations=3)
        path = root / ".ai/ITERATIONS.md"
        path.write_text(path.read_text().replace("ITER-0003", "ITER-10000"), encoding="utf-8")
        index = sl.migrate(root, 2, 50)
        self.assertEqual(index["ledgers"]["iterations"]["max_used"], 10000)
        temporary.cleanup()

    def test_zero_and_overpadded_identity_are_rejected(self):
        for invalid in ("ITER-0000", "ITER-00001"):
            temporary, root = self.seed(iterations=3)
            path = root / ".ai/ITERATIONS.md"
            path.write_text(path.read_text().replace("ITER-0003", invalid), encoding="utf-8")
            with self.assertRaises(sl.Error):
                sl.migrate(root, 2, 50)
            temporary.cleanup()

    def test_ten_thousand_rows_have_bounded_shards_and_lookup(self):
        temporary, root = self.seed(iterations=10000)
        index = sl.migrate(root, 20, 50)
        self.assertEqual(index["ledgers"]["iterations"]["row_count"], 10000)
        self.assertEqual(index["ledgers"]["iterations"]["shard_count"], 200)
        self.assertEqual(len(list((root / ".ai/history/iterations").glob("*.md"))), 200)
        self.assertEqual(len(list((root / ".ai/history/iterations").glob("*.json"))), 200)
        self.assertLess(len((root / ".ai/state-index.json").read_bytes()), 4096)
        code, result = sl.lookup(root, "ITER-0001")
        self.assertEqual(code, 0)
        self.assertLess(result["bytes_read"], 65536)
        self.assertEqual(len(sl.parse_rows((root / ".ai/ITERATIONS.md").read_text(), "ITER", 7)), 20)
        temporary.cleanup()

    def test_v1_single_cold_file_is_removed(self):
        temporary, root = self.seed(iterations=80)
        hot_path = root / ".ai/ITERATIONS.md"
        text = hot_path.read_text(encoding="utf-8")
        parsed = sl.parse_rows(text, "ITER", 7)
        hot = parsed[:20]
        cold = parsed[20:]
        hot_path.write_text(sl.render_hot(text, "iterations", hot), encoding="utf-8")
        legacy = root / ".ai/history/ITERATIONS.cold.md"
        legacy.parent.mkdir()
        legacy.write_text(
            "# ITER cold ledger\n\n| 迭代号 | 标题 | 状态 | 开启 | 收口 | 所属 milestone | 交付 |\n"
            "|---|---|---|---|---|---|---|\n"
            + "\n".join(sl.row_line(row) for row in cold) + "\n",
            encoding="utf-8",
        )
        sl.migrate(root, 20, 50)
        self.assertFalse(legacy.exists())
        self.assertEqual(len(list((root / ".ai/history/iterations").glob("*.md"))), 2)
        temporary.cleanup()

    def test_duplicate_across_hot_and_shard_is_rejected(self):
        temporary, root = self.seed()
        sl.migrate(root, 20, 50)
        shard = root / ".ai/history/iterations/ITER-000101-000150.md"
        shard.write_text(shard.read_text() + "| ITER-0125 | duplicate | closed | d | d | MILE-0003 | d.md |\n", encoding="utf-8")
        with self.assertRaises(sl.Error):
            sl.check(root)
        temporary.cleanup()

    def test_corrupt_hash_and_orphan_are_rejected(self):
        temporary, root = self.seed()
        sl.migrate(root, 20, 50)
        shard = root / ".ai/history/iterations/ITER-000001-000050.md"
        shard.write_text(shard.read_text().replace("item 1", "tampered"), encoding="utf-8")
        with self.assertRaises(sl.Error):
            sl.check(root)
        sl.migrate(root, 20, 50)
        receipt = shard.with_suffix(".json")
        receipt.write_text(receipt.read_text().replace('"count": 50', '"count": 49'), encoding="utf-8")
        with self.assertRaises(sl.Error):
            sl.lookup(root, "ITER-0001")
        sl.migrate(root, 20, 50)
        orphan = root / ".ai/history/iterations/note.md"
        orphan.write_text("not managed\n", encoding="utf-8")
        with self.assertRaises(sl.Error):
            sl.check(root)
        temporary.cleanup()

    def test_milestones_use_same_sharding_algorithm(self):
        temporary, root = self.seed(iterations=10, milestones=130)
        index = sl.migrate(root, 20, 50)
        self.assertEqual(index["ledgers"]["milestones"]["shard_count"], 3)
        code, result = sl.lookup(root, "MILE-0001")
        self.assertEqual(code, 0)
        self.assertIn("/milestones/", result["source"])
        temporary.cleanup()

    def test_atomic_update_rolls_back_writes_and_deletes(self):
        temporary, root = self.seed(iterations=3)
        a = root / ".ai/a.txt"
        b = root / ".ai/b.txt"
        c = root / ".ai/c.txt"
        a.write_text("old-a")
        b.write_text("old-b")
        c.write_text("old-c")
        calls = 0

        def fail_second(source, target):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("injected")
            os.replace(source, target)

        with self.assertRaises(OSError):
            sl.atomic_update(
                root,
                {".ai/a.txt": "new-a", ".ai/b.txt": "new-b"},
                {".ai/c.txt"},
                replace=fail_second,
            )
        self.assertEqual(a.read_text(), "old-a")
        self.assertEqual(b.read_text(), "old-b")
        self.assertEqual(c.read_text(), "old-c")
        temporary.cleanup()


if __name__ == "__main__":
    unittest.main()
