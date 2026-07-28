from __future__ import annotations

import json
import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[3]
TOOL = ROOT / "tools" / "project-config" / "config.py"
SCHEMA = ROOT / "tools" / "project-config" / "butler-config.schema.json"
DEPLOYMENT = ROOT / "Coder" / "20_Workflow_Lifecycle" / "mcv-deployment.md"
LOCAL_SCHEMA = ROOT / "Coder" / "20_Workflow_Lifecycle" / "local-constraints-schema.md"
RULE_CARD = ROOT / "templates" / "rule-card.md"
DEFAULT = {
    "schema_version": 1,
    "dangerous": False,
    "independent_review": False,
    "preference": True,
    "profiles": [],
}


def project(tmp_path: Path) -> Path:
    root = tmp_path / "project"
    (root / ".ai").mkdir(parents=True)
    return root


def legacy_text(*, dangerous: str = "off", profiles: str = "- 无，仅按通用 SOP") -> str:
    return (
        "# Project Type\n"
        "- CLI\n\n"
        "# Active Profiles\n"
        f"{profiles}\n\n"
        "# Local Constraints\n"
        "- keep this exact prose\n\n"
        "# Butler 功能开关\n"
        "# 项目级 butler 持久模式开关。\n"
        f"- dangerous: {dangerous}\n"
        "- independent_review: on\n"
        "- preference: off\n\n"
        "# Owner Notes\n"
        "owner bytes stay here\n"
    )


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(TOOL), *args],
        check=False,
        capture_output=True,
        text=True,
    )


def payload(result: subprocess.CompletedProcess[str]) -> dict:
    assert result.stderr == ""
    return json.loads(result.stdout)


def load_tool():
    spec = importlib.util.spec_from_file_location("butler_project_config", TOOL)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_schema_is_flat_strict_and_matches_defaults() -> None:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    assert schema["additionalProperties"] is False
    assert schema["required"] == list(DEFAULT)
    assert schema["properties"]["schema_version"] == {"const": 1}
    assert {
        key: value["default"]
        for key, value in schema["properties"].items()
        if "default" in value
    } == {key: value for key, value in DEFAULT.items() if key != "schema_version"}


def test_inspect_missing_returns_defaults_without_writing(tmp_path: Path) -> None:
    root = project(tmp_path)
    result = run("inspect", "--project-root", str(root))
    assert result.returncode == 0
    assert payload(result) == {
        "status": "ok",
        "source": "missing",
        "path": str(root / ".ai" / "butler.config.json"),
        "config": DEFAULT,
    }
    assert not (root / ".ai" / "butler.config.json").exists()


def test_missing_defaults_do_not_share_mutable_profile_state(tmp_path: Path) -> None:
    module = load_tool()
    root = project(tmp_path)
    first, _, _ = module.read(root)
    first["profiles"].append("mutated")
    second, _, _ = module.read(root)
    assert second == DEFAULT


def test_init_and_inspect_canonical_config(tmp_path: Path) -> None:
    root = project(tmp_path)
    created = run("init", "--project-root", str(root))
    assert created.returncode == 0
    assert payload(created)["source"] == "created"
    path = root / ".ai" / "butler.config.json"
    assert path.read_text(encoding="utf-8") == json.dumps(DEFAULT, indent=2) + "\n"

    inspected = run("inspect", "--project-root", str(root))
    assert inspected.returncode == 0
    assert payload(inspected)["source"] == "config"
    assert payload(inspected)["config"] == DEFAULT


def test_init_refuses_to_overwrite_existing_file(tmp_path: Path) -> None:
    root = project(tmp_path)
    path = root / ".ai" / "butler.config.json"
    path.write_text("{}\n", encoding="utf-8")
    result = run("init", "--project-root", str(root))
    assert result.returncode == 1
    assert payload(result)["code"] == "already_exists"
    assert path.read_text(encoding="utf-8") == "{}\n"


@pytest.mark.parametrize(
    "value,code",
    [
        ("{", "invalid_json"),
        (json.dumps({}), "missing_field"),
        (json.dumps({**DEFAULT, "schema_version": 2}), "unsupported_schema"),
        (json.dumps({**DEFAULT, "dangerous": "off"}), "invalid_type"),
        (json.dumps({**DEFAULT, "extra": True}), "unknown_field"),
        (json.dumps({**DEFAULT, "profiles": ["vue", "vue"]}), "duplicate_profile"),
        (json.dumps({**DEFAULT, "profiles": [""]}), "invalid_profile"),
    ],
)
def test_existing_invalid_config_fails_closed(
    tmp_path: Path, value: str, code: str
) -> None:
    root = project(tmp_path)
    path = root / ".ai" / "butler.config.json"
    path.write_text(value, encoding="utf-8")
    before = path.read_bytes()
    result = run("inspect", "--project-root", str(root))
    assert result.returncode == 2
    assert payload(result)["code"] == code
    assert path.read_bytes() == before


def test_set_updates_supported_fields_deterministically(tmp_path: Path) -> None:
    root = project(tmp_path)
    assert run("init", "--project-root", str(root)).returncode == 0

    changed = run("set", "dangerous", "true", "--project-root", str(root))
    assert changed.returncode == 0
    assert payload(changed)["config"]["dangerous"] is True

    profiles = run(
        "set",
        "profiles",
        '["typescript-rules", "build-tooling"]',
        "--project-root",
        str(root),
    )
    assert profiles.returncode == 0
    assert payload(profiles)["config"]["profiles"] == [
        "typescript-rules",
        "build-tooling",
    ]
    stored = json.loads((root / ".ai" / "butler.config.json").read_text())
    assert stored == payload(profiles)["config"]


def test_set_rejects_bad_value_without_modifying_file(tmp_path: Path) -> None:
    root = project(tmp_path)
    assert run("init", "--project-root", str(root)).returncode == 0
    path = root / ".ai" / "butler.config.json"
    before = path.read_bytes()
    result = run("set", "preference", "yes", "--project-root", str(root))
    assert result.returncode == 2
    assert payload(result)["code"] == "invalid_value"
    assert path.read_bytes() == before


def test_set_rejects_missing_config_and_unknown_field(tmp_path: Path) -> None:
    root = project(tmp_path)
    missing = run("set", "dangerous", "true", "--project-root", str(root))
    assert missing.returncode == 2
    assert payload(missing)["code"] == "missing_config"

    assert run("init", "--project-root", str(root)).returncode == 0
    path = root / ".ai" / "butler.config.json"
    before = path.read_bytes()
    unknown = run("set", "schema_version", "1", "--project-root", str(root))
    assert unknown.returncode == 2
    assert payload(unknown)["code"] == "invalid_field"
    assert path.read_bytes() == before


def test_failed_precommit_sync_preserves_original_and_cleans_temp(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    module = load_tool()
    root = project(tmp_path)
    module.initialize(root)
    path = root / ".ai" / "butler.config.json"
    before = path.read_bytes()

    def fail_sync(_directory: Path) -> None:
        raise OSError("injected directory sync failure")

    monkeypatch.setattr(module, "_fsync_directory", fail_sync)
    with pytest.raises(OSError, match="injected directory sync failure"):
        module.update(root, "dangerous", "true")

    assert path.read_bytes() == before
    assert list(path.parent.glob(".butler.config.*.tmp")) == []


def test_rejects_invalid_root_ai_directory_and_config_path(tmp_path: Path) -> None:
    missing = run("inspect", "--project-root", str(tmp_path / "missing"))
    assert missing.returncode == 2
    assert payload(missing)["code"] == "invalid_project_root"

    root_file = tmp_path / "project-file"
    root_file.write_text("not a directory", encoding="utf-8")
    not_directory = run("inspect", "--project-root", str(root_file))
    assert not_directory.returncode == 2
    assert payload(not_directory)["code"] == "invalid_project_root"

    outside_ai = tmp_path / "outside-ai"
    outside_ai.mkdir()
    linked_ai_root = tmp_path / "linked-ai-project"
    linked_ai_root.mkdir()
    (linked_ai_root / ".ai").symlink_to(outside_ai, target_is_directory=True)
    linked_ai = run("inspect", "--project-root", str(linked_ai_root))
    assert linked_ai.returncode == 2
    assert payload(linked_ai)["code"] == "invalid_ai_directory"

    root = project(tmp_path)
    target = tmp_path / "outside.json"
    target.write_text(json.dumps(DEFAULT), encoding="utf-8")
    (root / ".ai" / "butler.config.json").symlink_to(target)
    linked = run("inspect", "--project-root", str(root))
    assert linked.returncode == 2
    assert payload(linked)["code"] == "unsafe_config_path"

    linked_path = root / ".ai" / "butler.config.json"
    linked_path.unlink()
    linked_path.mkdir()
    directory = run("inspect", "--project-root", str(root))
    assert directory.returncode == 2
    assert payload(directory)["code"] == "unsafe_config_path"


def test_cli_usage_errors_preserve_single_json_stdout_contract() -> None:
    result = run("set", "dangerous", "true")
    assert result.returncode == 2
    assert payload(result)["code"] == "invalid_arguments"


def test_legacy_resolve_and_migration_plan_preserve_human_sections(tmp_path: Path) -> None:
    module = load_tool()
    root = project(tmp_path)
    legacy = legacy_text(
        dangerous="on", profiles="- `typescript-rules`\n- build-tooling"
    )
    local = root / ".ai" / "local-constraints.md"
    local.write_text(legacy, encoding="utf-8")

    resolved = run("resolve", "--project-root", str(root))
    assert resolved.returncode == 0
    assert payload(resolved)["source"] == "legacy"
    assert payload(resolved)["config"] == {
        **DEFAULT,
        "dangerous": True,
        "independent_review": True,
        "preference": False,
        "profiles": ["typescript-rules", "build-tooling"],
    }
    assert not (root / ".ai" / "butler.config.json").exists()

    changes = module.plan_migration(root)
    assert set(changes) == {
        Path(".ai/butler.config.json"),
        Path(".ai/local-constraints.md"),
    }
    narrowed = changes[Path(".ai/local-constraints.md")].decode("utf-8")
    assert "# Active Profiles" not in narrowed
    assert "# Butler 功能开关" not in narrowed
    assert "# Local Constraints\n- keep this exact prose" in narrowed
    assert "# Owner Notes\nowner bytes stay here" in narrowed
    assert local.read_text(encoding="utf-8") == legacy


def test_json_is_authoritative_and_reports_legacy_conflicts(tmp_path: Path) -> None:
    root = project(tmp_path)
    assert run("init", "--project-root", str(root)).returncode == 0
    (root / ".ai" / "local-constraints.md").write_text(
        legacy_text(dangerous="on"), encoding="utf-8"
    )
    resolved = run("resolve", "--project-root", str(root))
    assert resolved.returncode == 0
    assert payload(resolved)["source"] == "config"
    assert payload(resolved)["config"] == DEFAULT
    assert payload(resolved)["legacy_conflicts"] == [
        "dangerous",
        "independent_review",
        "preference",
    ]


@pytest.mark.parametrize(
    "body",
    [
        "# Active Profiles\n- TypeScript rules for this project\n",
        "# Active Profiles\n- vue\n- vue\n",
        "# Butler 功能开关\n- dangerous: maybe\n",
        "# Butler 功能开关\n- unknown: on\n",
    ],
)
def test_ambiguous_legacy_configuration_fails_closed(
    tmp_path: Path, body: str
) -> None:
    root = project(tmp_path)
    local = root / ".ai" / "local-constraints.md"
    local.write_text(body, encoding="utf-8")
    before = local.read_bytes()
    result = run("resolve", "--project-root", str(root))
    assert result.returncode == 2
    assert payload(result)["code"] in {"ambiguous_legacy", "duplicate_profile"}
    assert local.read_bytes() == before
    assert not (root / ".ai" / "butler.config.json").exists()


def test_migration_rejects_conflict_and_accepts_matching_json(tmp_path: Path) -> None:
    module = load_tool()
    root = project(tmp_path)
    local = root / ".ai" / "local-constraints.md"
    local.write_text(legacy_text(dangerous="on"), encoding="utf-8")
    module.initialize(root)
    with pytest.raises(module.ConfigError) as raised:
        module.plan_migration(root)
    assert raised.value.code == "legacy_conflict"

    config = {
        **DEFAULT,
        "dangerous": True,
        "independent_review": True,
        "preference": False,
    }
    (root / ".ai" / "butler.config.json").write_text(
        json.dumps(config, indent=2) + "\n", encoding="utf-8"
    )
    changes = module.plan_migration(root)
    assert set(changes) == {Path(".ai/local-constraints.md")}


def test_conflicting_legacy_review_policy_is_rejected(tmp_path: Path) -> None:
    root = project(tmp_path)
    (root / ".ai" / "local-constraints.md").write_text(
        "# Butler 功能开关\n"
        "- independent_review: off\n\n"
        "# Review Policy\n"
        "- independent_review: on\n",
        encoding="utf-8",
    )
    result = run("resolve", "--project-root", str(root))
    assert result.returncode == 2
    assert payload(result)["code"] == "ambiguous_legacy"


def test_new_deployment_contract_uses_json_without_markdown_double_write() -> None:
    deployment = DEPLOYMENT.read_text(encoding="utf-8")
    local_schema = LOCAL_SCHEMA.read_text(encoding="utf-8")
    rule_card = RULE_CARD.read_text(encoding="utf-8")
    assert "config.py\" init --project-root" in deployment
    assert "新部署不得继续生成 legacy 机器段" in deployment
    assert "机器配置不双写" in local_schema
    assert ".ai/butler.config.json" in rule_card
    assert "JSON 存在即为唯一真源" in rule_card
