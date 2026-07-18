"""Codex apply_patch parser and context fan-out tests."""
from __future__ import annotations

from pathlib import PurePosixPath
import subprocess

import pytest

from lib.codex_patch import parse_apply_patch
from lib.io import OUTSIDE_PROJECT, contexts_from_payload


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
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
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


def test_absolute_target_outside_session_cwd_uses_actual_git_root(tmp_path):
    session = tmp_path / "aggregate"
    project = tmp_path / "actual"
    session.mkdir()
    project.mkdir()
    subprocess.run(["git", "init", "-q", str(project)], check=True)
    target = project / ".ai" / "ITERATIONS.md"
    payload = {
        "tool_name": "apply_patch",
        "cwd": str(session),
        "tool_input": {
            "command": f"*** Begin Patch\n*** Add File: {target}\n+x\n*** End Patch"
        },
    }
    context = contexts_from_payload(payload)[0]
    assert context.cwd == str(project.resolve())
    assert context.target_path == PurePosixPath(".ai/ITERATIONS.md")


def test_patch_spanning_two_project_roots_returns_one_context_per_root(tmp_path):
    session = tmp_path / "aggregate"
    one = tmp_path / "one"
    two = tmp_path / "two"
    session.mkdir()
    for project in (one, two):
        project.mkdir()
        subprocess.run(["git", "init", "-q", str(project)], check=True)
    command = (
        "*** Begin Patch\n"
        f"*** Add File: {one / 'a.py'}\n+a\n"
        f"*** Add File: {two / 'b.py'}\n+b\n"
        "*** End Patch"
    )
    contexts = contexts_from_payload(
        {"tool_name": "apply_patch", "cwd": str(session), "tool_input": {"command": command}}
    )
    assert [context.cwd for context in contexts] == [str(one.resolve()), str(two.resolve())]
    assert [context.target_path for context in contexts] == [
        PurePosixPath("a.py"),
        PurePosixPath("b.py"),
    ]


def test_relative_path_from_aggregate_selects_actual_child_repo(tmp_path):
    aggregate = tmp_path / "aggregate"
    project = aggregate / "child"
    aggregate.mkdir()
    project.mkdir()
    subprocess.run(["git", "init", "-q", str(project)], check=True)
    payload = {
        "tool_name": "apply_patch",
        "cwd": str(aggregate),
        "tool_input": {
            "command": "*** Begin Patch\n*** Add File: child/src/x.py\n+x\n*** End Patch"
        },
    }
    context = contexts_from_payload(payload)[0]
    assert context.cwd == str(project.resolve())
    assert context.target_path == PurePosixPath("src/x.py")


@pytest.mark.parametrize("path", ["../escape.py", "/outside/absolute.py"])
def test_patch_target_without_a_project_uses_outside_sentinel(tmp_path, path):
    payload = {
        "tool_name": "apply_patch",
        "cwd": str(tmp_path),
        "tool_input": {
            "command": f"*** Begin Patch\n*** Add File: {path}\n+x\n*** End Patch"
        },
    }
    assert contexts_from_payload(payload)[0].target_path == OUTSIDE_PROJECT
