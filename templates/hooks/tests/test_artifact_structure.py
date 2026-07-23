from pathlib import Path, PurePosixPath
from lib.io import Context
from rules import artifact_structure


def test_unrelated_path_is_silent():
    result = artifact_structure.evaluate(Context("/tmp", "Write", PurePosixPath("src/x.py"), {}))
    assert result.message == ""


def test_legacy_artifact_is_silent(tmp_path, monkeypatch):
    (tmp_path / ".ai").mkdir()
    (tmp_path / ".ai/CONCEPT.md").write_text("# legacy\n")
    monkeypatch.setenv("BUTLER_PATH", str(Path(__file__).parents[3]))
    result = artifact_structure.evaluate(Context(str(tmp_path), "Write", PurePosixPath(".ai/CONCEPT.md"), {}))
    assert result.message == ""


def test_strict_drift_emits_advisory(tmp_path, monkeypatch):
    (tmp_path / ".ai").mkdir()
    (tmp_path / ".ai/CONCEPT.md").write_text("<!-- butler-artifact-template: 1.0.0 artifact=concept -->\n# x\n## Wrong\n- x\n")
    monkeypatch.setenv("BUTLER_PATH", str(Path(__file__).parents[3]))
    result = artifact_structure.evaluate(Context(str(tmp_path), "Write", PurePosixPath(".ai/CONCEPT.md"), {}))
    assert "结构漂移" in result.message
