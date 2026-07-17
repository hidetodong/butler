"""Codex apply_patch parser and context fan-out tests."""
from __future__ import annotations

from pathlib import PurePosixPath

import pytest

from lib.codex_patch import parse_apply_patch
from lib.io import OUT_OF_CWD, contexts_from_payload


def test_multi_file_multi_hunk_is_aggregated_in_order():
    command = """*** Begin Patch
*** Update File: src/a.py
@@
-old
+new
@@
+tail
*** Add File: src/b.py
+hello
*** Delete File: src/c.py
-gone
*** End Patch"""
    changes = parse_apply_patch(command)
    assert [(c.path, c.operation) for c in changes] == [
        ("src/a.py", "update"),
        ("src/b.py", "add"),
        ("src/c.py", "delete"),
    ]
    assert changes[0].added_lines == ("new", "tail")
    assert changes[0].removed_lines == ("old",)


def test_move_exposes_source_and_destination_targets():
    changes = parse_apply_patch("""*** Begin Patch
*** Update File: src/old.py
*** Move to: protected/new.py
@@
-old
+new
*** End Patch""")
    assert [(c.path, c.operation) for c in changes] == [
        ("src/old.py", "delete"),
        ("protected/new.py", "add"),
    ]


@pytest.mark.parametrize("command", ["", "nonsense", "*** Begin Patch\n*** End Patch"])
def test_empty_or_sectionless_patch_raises(command):
    with pytest.raises(ValueError):
        parse_apply_patch(command)


def test_contexts_fan_out_and_preserve_patch_metadata(tmp_path):
    payload = {
        "tool_name": "apply_patch",
        "cwd": str(tmp_path),
        "tool_input": {
            "command": "*** Begin Patch\n*** Update File: a.py\n-old\n+new\n*** Add File: b.py\n+x\n*** End Patch"
        },
    }
    contexts = contexts_from_payload(payload)
    assert [c.target_path for c in contexts] == [PurePosixPath("a.py"), PurePosixPath("b.py")]
    assert contexts[0].tool_input["butler_patch_removed"] == ["old"]
    assert contexts[1].tool_input["butler_patch_added"] == ["x"]


@pytest.mark.parametrize("path", ["../escape.py", "/outside/absolute.py"])
def test_patch_target_outside_cwd_uses_sentinel(tmp_path, path):
    payload = {
        "tool_name": "apply_patch",
        "cwd": str(tmp_path),
        "tool_input": {
            "command": f"*** Begin Patch\n*** Add File: {path}\n+x\n*** End Patch"
        },
    }
    assert contexts_from_payload(payload)[0].target_path == OUT_OF_CWD
