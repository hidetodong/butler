"""tools/intake 的契约测试。

覆盖 Coder/40_Context_Management/intake-schema.md 的三层：闪念口、孵化区、执行分流。
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from tools.intake import intake  # noqa: E402
from tools.intake.tests.helpers import make_root, snapshot  # noqa: E402

ENTRY = REPO_ROOT / "tools" / "intake" / "intake.py"
INBOX_HEADER = "| 闪念键 | 记于 | 一句话 | 状态 | 去向 |"
PLACEHOLDER = "<!-- TODO(intake):"


def run(root, *args):
    """直接调 main()，返回 (退出码, 解析后的 JSON 或原始文本)。"""
    import io
    import contextlib

    buf, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(err):
        code = intake.main([args[0], "--project-root", str(root), *args[1:]])
    text = buf.getvalue().strip()
    try:
        payload = json.loads(text) if text else {}
    except json.JSONDecodeError:
        payload = text
    return code, payload, err.getvalue().strip()


def digest(path):
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()


class TempRootCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp = self._tmp.name


# --------------------------------------------------------------------------
# AC2 · add
# --------------------------------------------------------------------------
class TestAdd(TempRootCase):
    def test_creates_inbox_with_contract_header(self):
        root = make_root(self.tmp)
        code, out, _ = run(root, "add", "--text", "fix the renderer", "--date", "2026-08-20")
        self.assertEqual(code, 0)
        self.assertEqual(out["state"], "new")
        self.assertEqual(out["key"], "2026-08-20-fix-the-renderer")
        body = (root / ".ai" / "INBOX.md").read_text(encoding="utf-8")
        self.assertIn("## 闪念", body)
        self.assertIn(INBOX_HEADER, body)
        self.assertIn("| 2026-08-20-fix-the-renderer | 2026-08-20 | fix the renderer | new | — |", body)

    def test_slug_collision_backs_off_with_numeric_suffix(self):
        root = make_root(self.tmp)
        keys = []
        for _ in range(3):
            code, out, _ = run(root, "add", "--text", "same idea", "--date", "2026-08-20")
            self.assertEqual(code, 0)
            keys.append(out["key"])
        self.assertEqual(
            keys,
            ["2026-08-20-same-idea", "2026-08-20-same-idea-2", "2026-08-20-same-idea-3"],
        )

    def test_append_only_leaves_earlier_rows_byte_identical(self):
        root = make_root(self.tmp)
        run(root, "add", "--text", "first one", "--date", "2026-08-20")
        before = (root / ".ai" / "INBOX.md").read_bytes()
        run(root, "add", "--text", "second one", "--date", "2026-08-21")
        after = (root / ".ai" / "INBOX.md").read_bytes()
        self.assertTrue(after.startswith(before.rstrip(b"\n")))

    def test_explicit_slug_is_required_for_non_ascii_text(self):
        root = make_root(self.tmp)
        code, out, _ = run(root, "add", "--text", "把渲染器搬进仓库", "--date", "2026-08-20")
        self.assertNotEqual(code, 0)
        self.assertIn("--slug", json.dumps(out, ensure_ascii=False))
        self.assertFalse((root / ".ai" / "INBOX.md").exists())

        code, out, _ = run(
            root, "add", "--text", "把渲染器搬进仓库", "--slug", "ship-renderer", "--date", "2026-08-20"
        )
        self.assertEqual(code, 0)
        self.assertEqual(out["key"], "2026-08-20-ship-renderer")

    def test_pipe_and_newline_in_text_are_rejected_without_writing(self):
        root = make_root(self.tmp)
        code, _, _ = run(root, "add", "--text", "a | b", "--slug", "ab", "--date", "2026-08-20")
        self.assertNotEqual(code, 0)
        self.assertFalse((root / ".ai" / "INBOX.md").exists())


# --------------------------------------------------------------------------
# AC3 · list
# --------------------------------------------------------------------------
class TestList(TempRootCase):
    def _seed(self):
        root = make_root(self.tmp)
        run(root, "add", "--text", "alpha idea", "--date", "2026-08-20")
        run(root, "add", "--text", "beta idea", "--date", "2026-08-20")
        run(
            root, "handle", "--inbox", "2026-08-20-alpha-idea", "--to", "incubated",
            "--slug", "alpha", "--scale", "iteration", "--title", "Alpha 方向",
            "--reason", "先记着", "--date", "2026-08-20",
        )
        return root

    def test_list_is_read_only(self):
        root = self._seed()
        before = snapshot(root)
        code, out, _ = run(root, "list")
        self.assertEqual(code, 0)
        self.assertEqual(snapshot(root), before)
        self.assertEqual(len(out["inbox"]), 2)
        self.assertEqual(len(out["backlog"]), 1)

    def test_filters_by_state_and_scale(self):
        root = self._seed()
        _, out, _ = run(root, "list", "--state", "new")
        self.assertEqual([e["key"] for e in out["inbox"]], ["2026-08-20-beta-idea"])
        self.assertEqual(out["backlog"], [])

        _, out, _ = run(root, "list", "--layer", "backlog", "--scale", "milestone")
        self.assertEqual(out["backlog"], [])
        _, out, _ = run(root, "list", "--layer", "backlog", "--scale", "iteration")
        self.assertEqual([e["key"] for e in out["backlog"]], ["alpha"])

    def test_flags_draft_that_still_holds_placeholder(self):
        root = self._seed()
        _, out, _ = run(root, "list", "--layer", "backlog")
        self.assertTrue(out["backlog"][0]["incomplete"])

        draft = root / ".ai" / "milestone-backlog" / "alpha.md"
        filled = "\n".join(
            line for line in draft.read_text(encoding="utf-8").splitlines()
            if PLACEHOLDER not in line
        )
        draft.write_text(filled + "\n", encoding="utf-8")
        _, out, _ = run(root, "list", "--layer", "backlog")
        self.assertFalse(out["backlog"][0]["incomplete"])


# --------------------------------------------------------------------------
# AC4 · 转移合法性
# --------------------------------------------------------------------------
class TestTransitions(TempRootCase):
    def _seed(self):
        root = make_root(self.tmp)
        run(root, "add", "--text", "one idea", "--date", "2026-08-20")
        return root

    def test_three_inbox_transitions_all_pass(self):
        # 第四条合法转移 incubated → dropped 只走 withdraw 出口，见 TestExits。
        for text, target, extra in [
            ("t one", "incubated", ["--slug", "s1", "--scale", "undecided", "--title", "T1", "--reason", "R1"]),
            ("t two", "done", ["--note", "顺手改掉了"]),
            ("t three", "dropped", ["--note", "不做了"]),
        ]:
            with tempfile.TemporaryDirectory() as tmp:
                root = make_root(tmp)
                _, out, _ = run(root, "add", "--text", text, "--date", "2026-08-20")
                code, res, _ = run(
                    root, "handle", "--inbox", out["key"], "--to", target,
                    "--date", "2026-08-20", *extra,
                )
                self.assertEqual(code, 0, f"{target} 应当合法：{res}")
                self.assertEqual(res["state"], target)

    def test_terminal_states_do_not_move(self):
        root = self._seed()
        run(root, "handle", "--inbox", "2026-08-20-one-idea", "--to", "done",
            "--note", "做掉了", "--date", "2026-08-20")
        before = snapshot(root)
        for target in ("dropped", "incubated", "new"):
            code, out, _ = run(
                root, "handle", "--inbox", "2026-08-20-one-idea", "--to", target,
                "--date", "2026-08-20", "--note", "x", "--slug", "s", "--scale",
                "undecided", "--title", "T", "--reason", "R",
            )
            self.assertNotEqual(code, 0, f"done → {target} 必须被拒")
        self.assertEqual(snapshot(root), before)

    def test_incubated_to_done_is_rejected(self):
        root = self._seed()
        run(root, "handle", "--inbox", "2026-08-20-one-idea", "--to", "incubated",
            "--slug", "s", "--scale", "undecided", "--title", "T", "--reason", "R",
            "--date", "2026-08-20")
        before = snapshot(root)
        code, _, _ = run(root, "handle", "--inbox", "2026-08-20-one-idea", "--to", "done",
                         "--note", "x", "--date", "2026-08-20")
        self.assertNotEqual(code, 0)
        self.assertEqual(snapshot(root), before)

    def test_incubated_to_dropped_must_go_through_withdraw(self):
        root = self._seed()
        run(root, "handle", "--inbox", "2026-08-20-one-idea", "--to", "incubated",
            "--slug", "s", "--scale", "undecided", "--title", "T", "--reason", "R",
            "--date", "2026-08-20")
        before = snapshot(root)
        code, out, _ = run(root, "handle", "--inbox", "2026-08-20-one-idea", "--to", "dropped",
                           "--note", "x", "--date", "2026-08-20")
        self.assertNotEqual(code, 0)
        self.assertIn("withdraw", json.dumps(out, ensure_ascii=False))
        self.assertEqual(snapshot(root), before)

    def test_unknown_key_is_rejected(self):
        root = self._seed()
        before = snapshot(root)
        code, _, _ = run(root, "handle", "--inbox", "2026-08-20-nope", "--to", "done",
                         "--note", "x", "--date", "2026-08-20")
        self.assertNotEqual(code, 0)
        self.assertEqual(snapshot(root), before)


# --------------------------------------------------------------------------
# AC5 · 三处联动、两侧原子
# --------------------------------------------------------------------------
class TestIncubateWritesThreePlaces(TempRootCase):
    def _seed(self):
        root = make_root(self.tmp)
        run(root, "add", "--text", "ship the renderer", "--date", "2026-08-20")
        return root

    def test_three_places_written_together(self):
        root = self._seed()
        code, out, _ = run(
            root, "handle", "--inbox", "2026-08-20-ship-the-renderer", "--to", "incubated",
            "--slug", "ship-renderer", "--scale", "iteration", "--title", "把渲染器搬进仓库",
            "--reason", "当前 active 占着，先入孵化区", "--date", "2026-08-20",
        )
        self.assertEqual(code, 0)
        self.assertEqual(sorted(out["written"]), sorted([
            ".ai/INBOX.md",
            ".ai/MILESTONES.md",
            ".ai/milestone-backlog/ship-renderer.md",
        ]))

        inbox = (root / ".ai" / "INBOX.md").read_text(encoding="utf-8")
        self.assertIn("| incubated | .ai/milestone-backlog/ship-renderer.md |", inbox)

        draft = (root / ".ai" / "milestone-backlog" / "ship-renderer.md").read_text(encoding="utf-8")
        self.assertIn("候办键: ship-renderer", draft)
        self.assertIn("候办状态: deferred", draft)
        self.assertIn("规模: iteration", draft)
        self.assertIn("## 要解决什么", draft)
        self.assertIn("## 暂缓原因", draft)
        self.assertNotIn("## 拆分路线图", draft)

        ledger = (root / ".ai" / "MILESTONES.md").read_text(encoding="utf-8")
        self.assertIn(
            "| ship-renderer | 把渲染器搬进仓库 | 2026-08-20 | "
            ".ai/milestone-backlog/ship-renderer.md | 当前 active 占着，先入孵化区 |",
            ledger,
        )

    def test_milestone_tier_gets_four_sections(self):
        root = self._seed()
        run(root, "handle", "--inbox", "2026-08-20-ship-the-renderer", "--to", "incubated",
            "--slug", "big", "--scale", "milestone", "--title", "大方向", "--reason", "R",
            "--date", "2026-08-20")
        draft = (root / ".ai" / "milestone-backlog" / "big.md").read_text(encoding="utf-8")
        for section in ("## 范围评估", "## 理解阐释", "## 拆分路线图", "## 范围演进记录"):
            self.assertIn(section, draft)

    def test_undecided_tier_names_the_blocker_section(self):
        root = self._seed()
        run(root, "handle", "--inbox", "2026-08-20-ship-the-renderer", "--to", "incubated",
            "--slug", "maybe", "--scale", "undecided", "--title", "还不确定", "--reason", "R",
            "--date", "2026-08-20")
        draft = (root / ".ai" / "milestone-backlog" / "maybe.md").read_text(encoding="utf-8")
        self.assertIn("## 想做什么", draft)
        self.assertIn("## 卡在哪", draft)

    def test_duplicate_backlog_key_is_rejected_without_writing(self):
        root = self._seed()
        run(root, "add", "--text", "another idea", "--date", "2026-08-20")
        run(root, "handle", "--inbox", "2026-08-20-ship-the-renderer", "--to", "incubated",
            "--slug", "dup", "--scale", "undecided", "--title", "T", "--reason", "R",
            "--date", "2026-08-20")
        before = snapshot(root)
        code, _, _ = run(root, "handle", "--inbox", "2026-08-20-another-idea", "--to", "incubated",
                         "--slug", "dup", "--scale", "undecided", "--title", "T2", "--reason", "R2",
                         "--date", "2026-08-20")
        self.assertNotEqual(code, 0)
        self.assertEqual(snapshot(root), before)


class TestRollback(TempRootCase):
    def _seed(self):
        root = make_root(self.tmp)
        run(root, "add", "--text", "rollback probe", "--date", "2026-08-20")
        return root

    def _incubate(self, root):
        return run(
            root, "handle", "--inbox", "2026-08-20-rollback-probe", "--to", "incubated",
            "--slug", "probe", "--scale", "iteration", "--title", "探针", "--reason", "R",
            "--date", "2026-08-20",
        )

    def _fail_on_nth_write(self, n):
        original = intake._write_file
        state = {"count": 0}

        def patched(path, data):
            state["count"] += 1
            if state["count"] == n:
                raise OSError("注入的写盘失败")
            return original(path, data)

        return patched, original

    def test_failure_on_second_write_rolls_everything_back(self):
        root = self._seed()
        before = snapshot(root)
        patched, original = self._fail_on_nth_write(2)
        intake._write_file = patched
        try:
            code, out, _ = self._incubate(root)
        finally:
            intake._write_file = original
        self.assertNotEqual(code, 0)
        self.assertEqual(snapshot(root), before)
        self.assertFalse((root / ".ai" / "milestone-backlog" / "probe.md").exists())

    def test_failure_on_third_write_rolls_everything_back(self):
        root = self._seed()
        before = snapshot(root)
        patched, original = self._fail_on_nth_write(3)
        intake._write_file = patched
        try:
            code, _, _ = self._incubate(root)
        finally:
            intake._write_file = original
        self.assertNotEqual(code, 0)
        self.assertEqual(snapshot(root), before)


# --------------------------------------------------------------------------
# 执行分流三条出口
# --------------------------------------------------------------------------
class TestExits(TempRootCase):
    def _root_with_draft(self, scale, *, milestones_current="none", iterations_current="none"):
        row = (
            "| d1 | 夹具方向 | 2026-08-20 | .ai/milestone-backlog/d1.md | 先缓着 |"
        )
        root = make_root(
            self.tmp,
            milestones_current=milestones_current,
            iterations_current=iterations_current,
            formal_rows=[
                "| MILE-0001 | 老里程碑 | closed | 2026-01-01 | 2026-01-02 | ITER-0001 | — |",
            ],
            backlog_rows=[row],
            iteration_rows=[
                "| ITER-0001 | 老迭代 | closed | 2026-01-01 | 2026-01-02 | MILE-0001 | — |",
            ],
        )
        sections = {
            "milestone": "## 范围评估\n\n真内容。\n\n## 理解阐释\n\n真内容。\n\n"
                         "## 拆分路线图\n\n真内容。\n\n## 范围演进记录\n\n真内容。\n",
            "iteration": "## 要解决什么\n\n真内容。\n\n## 暂缓原因\n\n真内容。\n",
        }[scale]
        (root / ".ai" / "milestone-backlog" / "d1.md").write_text(
            f"# 夹具方向\n\n候办键: d1\n候办状态: deferred\n规模: {scale}\n\n{sections}",
            encoding="utf-8",
        )
        inbox = (
            "# INBOX — 闪念口\n\n## 闪念\n\n"
            f"{INBOX_HEADER}\n|---|---|---|---|---|\n"
            "| 2026-08-01-seed | 2026-08-01 | 种子闪念 | incubated | .ai/milestone-backlog/d1.md |\n"
        )
        (root / ".ai" / "INBOX.md").write_text(inbox, encoding="utf-8")
        return root

    def test_promote_requires_no_active_milestone(self):
        root = self._root_with_draft("milestone", milestones_current="MILE-0001")
        before = snapshot(root)
        code, out, _ = run(root, "handle", "--backlog", "d1", "--exit", "promote", "--date", "2026-08-20")
        self.assertNotEqual(code, 0)
        self.assertIn("current", json.dumps(out, ensure_ascii=False))
        self.assertEqual(snapshot(root), before)

    def test_promote_allocates_number_and_clears_both_sides(self):
        root = self._root_with_draft("milestone")
        code, out, _ = run(root, "handle", "--backlog", "d1", "--exit", "promote", "--date", "2026-08-20")
        self.assertEqual(code, 0)
        self.assertEqual(out["id"], "MILE-0002")
        ledger = (root / ".ai" / "MILESTONES.md").read_text(encoding="utf-8")
        self.assertIn("current: MILE-0002", ledger)
        self.assertIn("| MILE-0002 | 夹具方向 | active | 2026-08-20 | — | — | — |", ledger)
        self.assertNotIn("| d1 |", ledger)
        self.assertFalse((root / ".ai" / "milestone-backlog" / "d1.md").exists())
        body = (root / ".ai" / "MILESTONE.md").read_text(encoding="utf-8")
        self.assertIn("## 5.3 拆分路线图", body)

    def test_promote_rejects_non_milestone_scale(self):
        root = self._root_with_draft("iteration")
        before = snapshot(root)
        code, _, _ = run(root, "handle", "--backlog", "d1", "--exit", "promote", "--date", "2026-08-20")
        self.assertNotEqual(code, 0)
        self.assertEqual(snapshot(root), before)

    def test_iterate_allocates_number_and_clears_both_sides(self):
        root = self._root_with_draft("iteration")
        code, out, _ = run(root, "handle", "--backlog", "d1", "--exit", "iterate", "--date", "2026-08-20")
        self.assertEqual(code, 0)
        self.assertEqual(out["id"], "ITER-0002")
        self.assertIn("next_step", out)
        ledger = (root / ".ai" / "ITERATIONS.md").read_text(encoding="utf-8")
        self.assertIn("current: ITER-0002", ledger)
        self.assertIn("| ITER-0002 | 夹具方向 | active | 2026-08-20 | — |", ledger)
        self.assertNotIn("| d1 |", (root / ".ai" / "MILESTONES.md").read_text(encoding="utf-8"))
        self.assertFalse((root / ".ai" / "milestone-backlog" / "d1.md").exists())

    def test_iterate_requires_no_active_iteration(self):
        root = self._root_with_draft("iteration", iterations_current="ITER-0001")
        before = snapshot(root)
        code, _, _ = run(root, "handle", "--backlog", "d1", "--exit", "iterate", "--date", "2026-08-20")
        self.assertNotEqual(code, 0)
        self.assertEqual(snapshot(root), before)

    def test_withdraw_clears_both_sides_and_writes_back_inbox_row(self):
        root = self._root_with_draft("iteration")
        code, out, _ = run(root, "handle", "--backlog", "d1", "--exit", "withdraw",
                           "--reason", "想清楚了不值得做", "--date", "2026-08-20")
        self.assertEqual(code, 0)
        self.assertFalse((root / ".ai" / "milestone-backlog" / "d1.md").exists())
        self.assertNotIn("| d1 |", (root / ".ai" / "MILESTONES.md").read_text(encoding="utf-8"))
        inbox = (root / ".ai" / "INBOX.md").read_text(encoding="utf-8")
        self.assertIn("| 2026-08-01-seed | 2026-08-01 | 种子闪念 | dropped |", inbox)
        body = (root / ".ai" / "MILESTONE.md").read_text(encoding="utf-8")
        self.assertIn("想清楚了不值得做", body)
        self.assertIn(".ai/MILESTONE.md", out["written"])


# --------------------------------------------------------------------------
# AC1 · 命令行本身接线正确
# --------------------------------------------------------------------------
class TestCli(TempRootCase):
    def test_end_to_end_through_real_process(self):
        root = make_root(self.tmp)
        proc = subprocess.run(
            [sys.executable, str(ENTRY), "add", "--project-root", str(root),
             "--text", "cli probe", "--date", "2026-08-20"],
            capture_output=True, text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        key = json.loads(proc.stdout)["key"]
        self.assertEqual(key, "2026-08-20-cli-probe")

        proc = subprocess.run(
            [sys.executable, str(ENTRY), "list", "--project-root", str(root)],
            capture_output=True, text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(json.loads(proc.stdout)["inbox"][0]["key"], key)

    def test_missing_project_root_exits_non_zero(self):
        proc = subprocess.run(
            [sys.executable, str(ENTRY), "list"], capture_output=True, text=True
        )
        self.assertNotEqual(proc.returncode, 0)

    def test_unwritable_contract_violation_exits_non_zero_without_writing(self):
        root = make_root(self.tmp)
        proc = subprocess.run(
            [sys.executable, str(ENTRY), "handle", "--project-root", str(root),
             "--inbox", "2026-08-20-nothing", "--to", "done", "--note", "x"],
            capture_output=True, text=True,
        )
        self.assertNotEqual(proc.returncode, 0)
        self.assertFalse((root / ".ai" / "INBOX.md").exists())



# --------------------------------------------------------------------------
# AC11 · 旧格式 `.ai/INBOX.md` 的回归防线
#
# MILE-0016 R8 删掉上一代收件箱契约与 `tools/inbox/` 之后，仓里再没有任何工具
# 认识旧格式。已部署项目硬盘上那份旧文件也没人搬（升级器没有删除/移动动作，
# 归 R14）。所以这里锁死唯一能守的行为：三个子命令碰到旧格式一律拒绝退出，
# 且**一个字节都不许写**——宁可停下让人处理，也不能把用户的旧回执改坏。
# --------------------------------------------------------------------------
LEGACY_INBOX = """# 收件箱

<!-- butler-inbox:managed:start -->

## Sources

| source_id | kind | locator | source_revision | observed_sha256 | processed_sha256 | observed_at | status | classification | proposed_route | actual_route | summary | note |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SRC-0001 | origin-file | origin/login.md | — | sha256:%s | — | 2026-08-01T09:00:00+08:00 | pending | — | — | — | 登录需求原稿 | — |

## Derivations

| source_id | artifact_kind | artifact_ref | derived_at | note |
|---|---|---|---|---|
| SRC-0001 | prd | 2026-08-01-login | 2026-08-01T09:10:00+08:00 | — |

<!-- butler-inbox:managed:end -->
""" % ("0" * 64)


class TestLegacyInboxIsRefusedNotRewritten(TempRootCase):
    def _root_with_legacy(self):
        root = make_root(self.tmp)
        (root / ".ai" / "INBOX.md").write_text(LEGACY_INBOX, encoding="utf-8")
        return root

    def test_add_refuses_and_writes_nothing(self):
        root = self._root_with_legacy()
        before = snapshot(root)
        code, _, err = run(root, "add", "--text", "new thought", "--date", "2026-08-21")
        self.assertNotEqual(code, 0)
        self.assertIn(INBOX_HEADER, err)
        self.assertEqual(before, snapshot(root))

    def test_list_refuses_and_writes_nothing(self):
        root = self._root_with_legacy()
        before = snapshot(root)
        code, _, err = run(root, "list")
        self.assertNotEqual(code, 0)
        self.assertIn(INBOX_HEADER, err)
        self.assertEqual(before, snapshot(root))

    def test_handle_refuses_and_writes_nothing(self):
        root = self._root_with_legacy()
        before = snapshot(root)
        code, _, err = run(
            root, "handle", "--inbox", "2026-08-01-login", "--to", "done", "--note", "x"
        )
        self.assertNotEqual(code, 0)
        self.assertIn(INBOX_HEADER, err)
        self.assertEqual(before, snapshot(root))

    def test_legacy_markers_and_source_ids_survive_byte_identical(self):
        root = self._root_with_legacy()
        for args in (
            ("add", "--text", "another", "--date", "2026-08-21"),
            ("list",),
            ("handle", "--inbox", "SRC-0001", "--to", "dropped", "--note", "x"),
        ):
            run(root, *args)
        self.assertEqual(
            LEGACY_INBOX, (root / ".ai" / "INBOX.md").read_text(encoding="utf-8")
        )

if __name__ == "__main__":
    unittest.main()
