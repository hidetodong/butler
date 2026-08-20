#!/usr/bin/env python3
"""`scripts/sync-project-overview.py` 的负例为主测试套。

夹具是合成的最小仓（不拷真实 `Coder/` 与 `tools/`）：这里要证的是生成器的行为——
缺源头是否拒绝出页、漂移诊断是否指名到节、上限与棘轮是否真的拦得住。真实内容与
机器源头是否对得上，由 CI 里那行 `--check` 在真仓上守。
"""
from __future__ import annotations

import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODULE_PATH = ROOT / "scripts/sync-project-overview.py"
SPEC = importlib.util.spec_from_file_location("sync_project_overview", MODULE_PATH)
assert SPEC and SPEC.loader
overview = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = overview
SPEC.loader.exec_module(overview)

DIRECTORIES = ("00_System_Prompt", "20_Workflow_Lifecycle", "40_Context_Management")


def readme_text(directories=DIRECTORIES) -> str:
    lines = ["# Coder", "", "## 目录结构", "", "规则目录说明：", ""]
    for name in directories:
        lines.append(f"- `{name}/`：夹具用的职责说明 {name}。")
    lines += ["", "## 读取顺序", "", "略。"]
    return "\n".join(lines) + "\n"


def ledger(kind: str, current: str, rows: list[tuple[str, ...]]) -> str:
    head = ["# 台账", "", f"current: {current}", "",
            "| 号 | 标题 | 状态 | 开启 | 收口 | 含迭代 | 交付 |", "|---|---|---|---|---|---|---|"]
    for row in rows:
        head.append("| " + " | ".join(row) + " |")
    return "\n".join(head) + "\n"


def invariants_text(no_pointer: int) -> str:
    lines = ["# invariants", "", "> 夹具。", ""]
    for index in range(no_pointer):
        lines.append(f"- **无指针条目 {index}**：这条没有任何反引号真源指针。*为什么*：夹具需要。")
    lines.append("- **有指针条目**：见 `Coder/README.md`。*为什么*：夹具需要。")
    return "\n".join(lines) + "\n"


class SyncProjectOverviewTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.write("VERSION", "9.9.9\n")
        self.write(".ai/ITERATIONS.md", ledger("iter", "ITER-0002", [
            ("ITER-0002", "夹具迭代二", "active", "2026-01-02", "—", "MILE-0001", "—"),
            ("ITER-0001", "夹具迭代一", "closed", "2026-01-01", "2026-01-01", "MILE-0001", "d.md"),
        ]))
        self.write(".ai/MILESTONES.md", ledger("mile", "MILE-0001", [
            ("MILE-0001", "夹具里程碑", "active", "2026-01-01", "—", "ITER-0001, ITER-0002", "—"),
        ]))
        self.write(".ai/state-index.json", json.dumps(
            {"ledgers": {"iterations": {"row_count": 2}, "milestones": {"row_count": 1}}}))
        self.write(".ai/invariants.md", invariants_text(overview.INVARIANT_POINTER_EXEMPT))
        self.write("Coder/README.md", readme_text())
        for name in DIRECTORIES:
            self.write(f"Coder/{name}/rule.md", "# rule\n")
        self.write("workflows/registry.json", json.dumps({
            "router": {"claude": {"name": "/butler"}, "codex": {"name": "$butler-router"}},
            "workflows": [
                {"id": "inbox", "risk": "normal", "rule_source": "Coder/x.md",
                 "claude": {"name": "/butler:inbox"}, "codex": {"name": "$butler-inbox"}},
            ],
        }))
        for name in ("alpha", "beta"):
            self.write(f"tools/{name}/README.md", f"# {name} tool\n")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write(self, relative: str, text: str) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def run_cli(self, *args: str) -> int:
        # 生成器成功时会往 stdout 打一行 JSON；测试里吞掉，免得淹没 CI 输出。
        from io import StringIO
        original, sys.stdout = sys.stdout, StringIO()
        try:
            return overview.main([*args, "--project-root", str(self.root)])
        finally:
            sys.stdout = original

    def stderr_of(self, *args: str) -> tuple[int, str]:
        from io import StringIO
        buffer = StringIO()
        original, sys.stderr = sys.stderr, buffer
        try:
            code = self.run_cli(*args)
        finally:
            sys.stderr = original
        return code, buffer.getvalue()

    # —— 正例 ——

    def test_write_then_check_is_clean(self) -> None:
        self.assertEqual(0, self.run_cli("--write"))
        self.assertEqual(0, self.run_cli("--check"))

    def test_write_is_idempotent(self) -> None:
        self.run_cli("--write")
        first = (self.root / overview.OVERVIEW_RELATIVE).read_bytes()
        self.run_cli("--write")
        self.assertEqual(first, (self.root / overview.OVERVIEW_RELATIVE).read_bytes())

    def test_check_and_write_are_mutually_exclusive(self) -> None:
        with self.assertRaises(SystemExit):
            self.run_cli("--check", "--write")

    # —— 负例：源头缺失一律拒绝出页 ——

    def test_missing_sources_are_named(self) -> None:
        cases = [
            ("VERSION", "VERSION"),
            (".ai/ITERATIONS.md", ".ai/ITERATIONS.md"),
            (".ai/MILESTONES.md", ".ai/MILESTONES.md"),
            ("Coder/README.md", "Coder/README.md"),
            ("workflows/registry.json", "workflows/registry.json"),
        ]
        for relative, needle in cases:
            with self.subTest(source=relative):
                self.tearDown()   # 每个子例换一份干净夹具，旧临时目录先收干净
                self.setUp()
                (self.root / relative).unlink()
                code, err = self.stderr_of("--write")
                self.assertEqual(1, code)
                self.assertIn(f"missing source: {needle}", err)
                self.assertFalse((self.root / overview.OVERVIEW_RELATIVE).exists(),
                                 "缺源头时不得产出残缺页")

    def test_missing_tools_directory_is_named(self) -> None:
        shutil.rmtree(self.root / "tools")
        code, err = self.stderr_of("--write")
        self.assertEqual(1, code)
        self.assertIn("missing source: tools/", err)

    # —— 负例：漂移诊断必须指名到节 ——

    def test_check_names_the_drifting_section(self) -> None:
        self.run_cli("--write")
        path = self.root / overview.OVERVIEW_RELATIVE
        text = path.read_text(encoding="utf-8")
        path.write_text(text.replace("| `tools/alpha/` |", "| `tools/被改过/` |", 1), encoding="utf-8")
        code, err = self.stderr_of("--check")
        self.assertEqual(1, code)
        self.assertIn(f"overview section drift: {overview.SECTION_TOOLS}", err)
        self.assertNotIn(f"overview section drift: {overview.SECTION_VERSION}", err)

    def test_check_reports_section_set_mismatch(self) -> None:
        self.run_cli("--write")
        path = self.root / overview.OVERVIEW_RELATIVE
        path.write_text(path.read_text(encoding="utf-8").replace(
            f"## {overview.SECTION_TOOLS}", "## 被改名的节", 1), encoding="utf-8")
        code, err = self.stderr_of("--check")
        self.assertEqual(1, code)
        self.assertIn("overview section set mismatch", err)

    # —— 负例：上限与棘轮 ——

    def test_size_ceiling_is_enforced(self) -> None:
        for index in range(400):
            self.write(f"tools/bulk{index:03d}/README.md", f"# 体量夹具工具 {index:03d}\n")
        code, err = self.stderr_of("--write")
        self.assertEqual(1, code)
        self.assertIn("overview too large:", err)
        self.assertIn(str(overview.OVERVIEW_MAX_BYTES), err)

    def test_invariant_pointer_ratchet_blocks_new_entries(self) -> None:
        self.run_cli("--write")
        self.assertEqual(0, self.run_cli("--check"))
        self.write(".ai/invariants.md",
                   invariants_text(overview.INVARIANT_POINTER_EXEMPT) +
                   "- **新加的无指针条目**：这条也没给真源。*为什么*：夹具需要。\n")
        code, err = self.stderr_of("--check")
        self.assertEqual(1, code)
        self.assertIn(
            f"invariants without source pointer: {overview.INVARIANT_POINTER_EXEMPT + 1}"
            f" > {overview.INVARIANT_POINTER_EXEMPT}", err)
        self.assertIn("新加的无指针条目", err)

    # —— 负例：README 漏登记目录 ——

    def test_directory_without_description_is_rejected(self) -> None:
        self.write("Coder/77_Extension_Unlisted/rule.md", "# rule\n")
        code, err = self.stderr_of("--write")
        self.assertEqual(1, code)
        self.assertIn("directory has no description in Coder/README.md: 77_Extension_Unlisted", err)


if __name__ == "__main__":
    unittest.main()
