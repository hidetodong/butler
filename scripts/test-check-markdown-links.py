#!/usr/bin/env python3
"""Fixture tests for the offline Markdown link checker."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("check-markdown-links.py")
SPEC = importlib.util.spec_from_file_location("check_markdown_links", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class MarkdownLinkTests(unittest.TestCase):
    def test_valid_files_fragments_and_ignored_content(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            guide = root / "docs" / "guide one.md"
            guide.parent.mkdir()
            guide.write_text(
                "# 中文 标题\n\n## Repeat\n\n## Repeat\n\n<a id=\"manual-anchor\"></a>\n",
                encoding="utf-8",
            )
            (root / "README.md").write_text(
                "# Home\n\n"
                "[guide](docs/guide%20one.md#中文-标题)\n"
                "[duplicate](docs/guide%20one.md#repeat-1)\n"
                "[manual](docs/guide%20one.md#manual-anchor)\n"
                "[directory](docs/)\n"
                "[same](#home)\n"
                "[external](https://example.com/missing)\n"
                "`[inline](missing.md)`\n"
                "```md\n[fenced](missing.md)\n```\n",
                encoding="utf-8",
            )
            problems, files, links = MODULE.check(root)
            self.assertEqual(problems, [])
            self.assertEqual(files, 2)
            self.assertEqual(links, 6)

    def test_bad_target_fragment_escape_and_absolute_are_reported(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "repo"
            root.mkdir()
            (root / "target.md").write_text("# Real heading\n", encoding="utf-8")
            (root / "README.md").write_text(
                "[missing](missing.md)\n"
                "[fragment](target.md#wrong)\n"
                "[escape](../outside.md)\n"
                "[absolute](/tmp/outside.md)\n",
                encoding="utf-8",
            )
            problems, _, _ = MODULE.check(root)
            rendered = "\n".join(problem.render() for problem in problems)
            self.assertIn("target does not exist", rendered)
            self.assertIn("heading fragment not found", rendered)
            self.assertIn("target escapes repository root", rendered)
            self.assertIn("absolute local path is not allowed", rendered)
            self.assertEqual([problem.line for problem in problems], [1, 2, 3, 4])

    def test_non_markdown_fragment_and_unknown_scheme_fail(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "asset.txt").write_text("data", encoding="utf-8")
            (root / "README.md").write_text(
                "[asset](asset.txt#section)\n[unknown](custom://value)\n",
                encoding="utf-8",
            )
            problems, _, _ = MODULE.check(root)
            reasons = [problem.reason for problem in problems]
            self.assertIn("fragment target is not a Markdown file", reasons)
            self.assertIn("unsupported link scheme: custom", reasons)


if __name__ == "__main__":
    unittest.main()
