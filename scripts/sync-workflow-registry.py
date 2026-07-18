#!/usr/bin/env python3
"""Validate and synchronize Butler workflow metadata from one registry."""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

EXPECTED_IDS = {"prd", "review", "milestone", "upgrade", "ideation", "preference", "loop", "dangerous"}
HIGH_RISK = {"loop", "dangerous"}
TOP_KEYS = {"schema_version", "plugin", "workflows"}
PLUGIN_KEYS = {"name", "root", "manifest", "hooks", "personal_installer", "setup_entrypoint", "marketplace_mode", "team_distribution"}
WORKFLOW_KEYS = {"id", "rule_source", "risk", "allow_implicit_invocation", "semantic_triggers", "legacy_aliases", "claude", "codex"}
CLAUDE_KEYS = {"name", "path", "description", "default_prompt"}
CODEX_KEYS = {"name", "path", "description", "display_name", "short_description", "default_prompt"}
ALIAS_KEYS = {"name", "status"}
ALIAS_STATUSES = {"deprecated", "natural-language-compat", "harness-collision-do-not-generate", "deprecated-do-not-generate"}


class RegistryError(ValueError):
    pass


@dataclass(frozen=True)
class Projection:
    path: Path
    kind: str
    content: bytes | None = None
    target: str | None = None


def safe_path(root: Path, value: str) -> Path:
    path = Path(value)
    if path.is_absolute() or not path.parts or ".." in path.parts:
        raise RegistryError(f"unsafe repository-relative path: {value}")
    resolved = (root / path).resolve(strict=False)
    try:
        resolved.relative_to(root.resolve())
    except ValueError as error:
        raise RegistryError(f"path escapes repository root: {value}") from error
    return root / path


def read_registry(root: Path) -> dict[str, Any]:
    path = root / "workflows" / "registry.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise RegistryError(f"cannot read workflow registry: {error}") from error
    validate_registry(data, root)
    return data


def exact_keys(value: Any, expected: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != expected:
        actual = set(value) if isinstance(value, dict) else set()
        raise RegistryError(f"{label} fields mismatch: {sorted(actual ^ expected)}")
    return value


def nonempty(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise RegistryError(f"{label} must be a non-empty string")
    return value


def validate_registry(data: Any, root: Path) -> None:
    exact_keys(data, TOP_KEYS, "registry")
    if data["schema_version"] != 1:
        raise RegistryError("schema_version must be 1")
    plugin = exact_keys(data["plugin"], PLUGIN_KEYS, "plugin")
    expected_plugin = {
        "name": "butler", "root": "plugins/butler",
        "manifest": "plugins/butler/.codex-plugin/plugin.json",
        "hooks": "plugins/butler/hooks/hooks.json",
        "personal_installer": "scripts/install-codex-plugin.sh",
        "setup_entrypoint": "scripts/setup.sh",
        "marketplace_mode": "personal", "team_distribution": "not-configured",
    }
    if plugin != expected_plugin:
        raise RegistryError("plugin/distribution declaration does not match Butler's supported boundary")
    for field in ("root", "manifest", "hooks", "personal_installer", "setup_entrypoint"):
        path = safe_path(root, plugin[field])
        if not path.exists():
            raise RegistryError(f"registered plugin path does not exist: {plugin[field]}")

    workflows = data["workflows"]
    if not isinstance(workflows, list) or len(workflows) != 8:
        raise RegistryError("registry must contain exactly 8 workflows")
    ids: set[str] = set()
    names: set[str] = set()
    aliases: set[str] = set()
    for index, workflow in enumerate(workflows):
        item = exact_keys(workflow, WORKFLOW_KEYS, f"workflow[{index}]")
        workflow_id = nonempty(item["id"], "workflow id")
        if not re.fullmatch(r"[a-z][a-z0-9-]*", workflow_id) or workflow_id in ids:
            raise RegistryError(f"invalid or duplicate workflow id: {workflow_id}")
        ids.add(workflow_id)
        rule = safe_path(root, nonempty(item["rule_source"], f"{workflow_id}.rule_source"))
        if not rule.is_file():
            raise RegistryError(f"rule source missing: {item['rule_source']}")
        risk = item["risk"]
        implicit = item["allow_implicit_invocation"]
        if risk not in {"normal", "high"} or not isinstance(implicit, bool):
            raise RegistryError(f"invalid risk/implicit policy for {workflow_id}")
        if workflow_id in HIGH_RISK:
            if risk != "high" or implicit:
                raise RegistryError(f"high-risk workflow must forbid implicit invocation: {workflow_id}")
        elif risk != "normal" or not implicit:
            raise RegistryError(f"normal workflow must explicitly allow implicit invocation: {workflow_id}")
        triggers = item["semantic_triggers"]
        if not isinstance(triggers, list) or not triggers or any(not isinstance(x, str) or not x for x in triggers):
            raise RegistryError(f"semantic_triggers must be non-empty strings: {workflow_id}")
        alias_items = item["legacy_aliases"]
        if not isinstance(alias_items, list) or not alias_items:
            raise RegistryError(f"legacy_aliases must be non-empty: {workflow_id}")
        for alias in alias_items:
            alias = exact_keys(alias, ALIAS_KEYS, f"{workflow_id}.alias")
            name = nonempty(alias["name"], f"{workflow_id}.alias.name")
            if name in aliases or alias["status"] not in ALIAS_STATUSES:
                raise RegistryError(f"duplicate alias or invalid status: {name}")
            aliases.add(name)
        claude = exact_keys(item["claude"], CLAUDE_KEYS, f"{workflow_id}.claude")
        codex = exact_keys(item["codex"], CODEX_KEYS, f"{workflow_id}.codex")
        if claude["name"] != f"/butler:{workflow_id}" or codex["name"] != f"$butler-{workflow_id}":
            raise RegistryError(f"canonical host name does not match workflow id: {workflow_id}")
        if claude["path"] != f".claude/commands/butler/{workflow_id}.md":
            raise RegistryError(f"Claude path does not match id: {workflow_id}")
        if codex["path"] != f"plugins/butler/skills/butler-{workflow_id}/SKILL.md":
            raise RegistryError(f"Codex path does not match id: {workflow_id}")
        for host, fields in (("claude", claude), ("codex", codex)):
            path = safe_path(root, fields["path"])
            if not path.is_file():
                raise RegistryError(f"{host} entry missing: {fields['path']}")
            for key, value in fields.items():
                if key != "path":
                    nonempty(value, f"{workflow_id}.{host}.{key}")
        if claude["name"] in names or codex["name"] in names:
            raise RegistryError(f"duplicate host name for {workflow_id}")
        names.update({claude["name"], codex["name"]})
    if ids != EXPECTED_IDS:
        raise RegistryError(f"workflow set mismatch: missing={sorted(EXPECTED_IDS-ids)}, extra={sorted(ids-EXPECTED_IDS)}")
    if "/loop" not in aliases:
        raise RegistryError("legacy /loop harness collision must stay registered")
    validate_repository_sets(data, root)
    validate_plugin_contract(data, root)
    validate_human_doc_routes(root)


def validate_repository_sets(data: dict[str, Any], root: Path) -> None:
    expected_commands = {item["claude"]["path"] for item in data["workflows"]}
    actual_commands = {path.relative_to(root).as_posix() for path in (root / ".claude/commands/butler").glob("*.md")}
    if actual_commands != expected_commands:
        raise RegistryError(f"Claude workflow set drift: missing={sorted(expected_commands-actual_commands)}, extra={sorted(actual_commands-expected_commands)}")
    expected_skills = {item["codex"]["path"] for item in data["workflows"]}
    actual_skills = {path.relative_to(root).as_posix() for path in (root / "plugins/butler/skills").glob("*/SKILL.md")}
    if actual_skills != expected_skills:
        raise RegistryError(f"Codex workflow set drift: missing={sorted(expected_skills-actual_skills)}, extra={sorted(actual_skills-expected_skills)}")
    expected_links = {item["codex"]["name"].removeprefix("$") for item in data["workflows"]}
    skills_dir = root / ".agents/skills"
    actual_links = {path.name for path in skills_dir.iterdir() if path.name.startswith("butler-")}
    if actual_links != expected_links:
        raise RegistryError(f"Codex discovery set drift: missing={sorted(expected_links-actual_links)}, extra={sorted(actual_links-expected_links)}")
    forbidden_alias_entities = [root / ".claude/commands/loop.md", root / ".claude/commands/dangerous.md"]
    if any(path.exists() for path in forbidden_alias_entities):
        raise RegistryError("high-risk legacy aliases must not be generated as command files")


def validate_plugin_contract(data: dict[str, Any], root: Path) -> None:
    plugin = data["plugin"]
    try:
        manifest = json.loads((root / plugin["manifest"]).read_text(encoding="utf-8"))
        hooks = json.loads((root / plugin["hooks"]).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise RegistryError(f"plugin contract JSON is invalid: {error}") from error
    if manifest.get("name") != plugin["name"] or manifest.get("skills") != "./skills/":
        raise RegistryError("plugin manifest name/skills path drift")
    if "hooks" in manifest:
        raise RegistryError("unsupported hooks field must not be added to plugin.json")
    events = hooks.get("hooks") if isinstance(hooks, dict) else None
    expected = {"PreToolUse": "butler-gate.sh", "PostToolUse": "butler-advisor.sh"}
    if not isinstance(events, dict) or set(events) != set(expected):
        raise RegistryError("plugin hook events must be exactly PreToolUse/PostToolUse")
    for event, wrapper in expected.items():
        entries = events[event]
        if not isinstance(entries, list) or len(entries) != 1 or entries[0].get("matcher") != "apply_patch|Edit|Write":
            raise RegistryError(f"plugin hook matcher drift: {event}")
        commands = entries[0].get("hooks")
        expected_command = {"type": "command", "command": f'"$PLUGIN_ROOT/hooks/{wrapper}"'}
        if not isinstance(commands, list) or commands != [expected_command]:
            raise RegistryError(f"plugin hook command drift: {event}")
        wrapper_path = root / plugin["root"] / "hooks" / wrapper
        if not wrapper_path.is_file() or not os.access(wrapper_path, os.X_OK):
            raise RegistryError(f"plugin hook wrapper missing or not executable: {wrapper_path.relative_to(root)}")
    setup = (root / plugin["setup_entrypoint"]).read_text(encoding="utf-8")
    installer = (root / plugin["personal_installer"]).read_text(encoding="utf-8")
    if "install-codex-plugin.sh" not in setup:
        raise RegistryError("setup no longer routes the Codex installer")
    for token in ("update_plugin_cachebuster.py", "codex plugin add", "marketplace.json"):
        if token not in installer:
            raise RegistryError(f"personal installer contract missing: {token}")


def validate_human_doc_routes(root: Path) -> None:
    required = {
        "README.md": "docs/workflows.md",
        "HUMAN_GUIDE.md": "docs/workflows.md",
        "Coder/README.md": "docs/workflows.md",
        "docs/codex-compatibility.md": "workflows.md",
    }
    for relative, token in required.items():
        path = root / relative
        try:
            content = path.read_text(encoding="utf-8")
        except OSError as error:
            raise RegistryError(f"human workflow guide missing: {relative}") from error
        if token not in content:
            raise RegistryError(f"human workflow guide must route to generated registry table: {relative}")


def rewrite_frontmatter(path: Path, updates: dict[str, str]) -> bytes:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        raise RegistryError(f"frontmatter start missing: {path}")
    end = next((i for i, line in enumerate(lines[1:], 1) if line.strip() == "---"), None)
    if end is None:
        raise RegistryError(f"frontmatter end missing: {path}")
    for key, value in updates.items():
        indexes = [i for i in range(1, end) if re.match(rf"^{re.escape(key)}\s*:", lines[i])]
        if len(indexes) != 1:
            raise RegistryError(f"frontmatter field {key} must appear once: {path}")
        if "\n" in value or "\r" in value:
            raise RegistryError(f"multiline frontmatter value is not supported: {path}:{key}")
        lines[indexes[0]] = f"{key}: {value}\n"
    return "".join(lines).encode("utf-8")


def quote_yaml(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def openai_yaml(item: dict[str, Any]) -> bytes:
    codex = item["codex"]
    value = (
        "interface:\n"
        f"  display_name: {quote_yaml(codex['display_name'])}\n"
        f"  short_description: {quote_yaml(codex['short_description'])}\n"
        f"  default_prompt: {quote_yaml(codex['default_prompt'])}\n"
        "policy:\n"
        f"  allow_implicit_invocation: {'true' if item['allow_implicit_invocation'] else 'false'}\n"
    )
    return value.encode("utf-8")


def docs_table(data: dict[str, Any]) -> bytes:
    rows = []
    for item in data["workflows"]:
        aliases = "<br>".join(f"`{a['name']}` ({a['status']})" for a in item["legacy_aliases"])
        triggers = "、".join(f"`{value}`" for value in item["semantic_triggers"])
        policy = "允许" if item["allow_implicit_invocation"] else "禁止（必须显式）"
        rows.append(
            f"| {item['id']} | `{item['claude']['name']}` | `{item['codex']['name']}` | {item['risk']} | {policy} | {triggers} | {aliases} | `{item['rule_source']}` |"
        )
    text = f"""# Butler 双宿主工作流注册表

> 本页由 `workflows/registry.json` 通过 `scripts/sync-workflow-registry.py --write` 生成，请勿手改。机器 registry 是元数据真源；本页是唯一八项人读能力表。

| ID | Claude Code | Codex | 风险 | 隐式调用 | 语义触发 | 旧名 / 兼容 | 规则真源 |
|---|---|---|---|---|---|---|---|
{chr(10).join(rows)}

## 安全与兼容

- `loop` / `dangerous` 是 high risk，Codex `allow_implicit_invocation=false`；只能由用户显式点名 Butler 模式。旧 `/loop` 与 Claude harness 自带循环撞名，绝不生成旧实体命令。
- 其余六项显式 `allow_implicit_invocation=true`，仍须按各自 SKILL description 的语义边界触发。
- legacy alias 是识别/弃用元数据，不代表仓库重新创建同名入口。

## 发现与分发状态

| 层 | 当前状态 | 真源 / 边界 |
|---|---|---|
| Claude 全局命令 | available via setup symlink | `.claude/commands/butler/` → `scripts/setup.sh` |
| Codex repo discovery | available | `.agents/skills/` 的 8 个相对软链，实体在 `plugins/butler/skills/` |
| Codex personal plugin | available via explicit installer | `scripts/install-codex-plugin.sh` + personal marketplace；安装副本单独 cachebuster |
| Plugin hooks | declared via standard auto-discovery | `plugins/butler/hooks/hooks.json`；不向 `plugin.json` 塞不受支持字段 |
| Team/public distribution | **not configured** | 没有团队 marketplace / 公共发布；个人已安装不等于团队可用 |
"""
    return text.encode("utf-8")


def build_projections(data: dict[str, Any], root: Path) -> list[Projection]:
    projections: list[Projection] = []
    for item in data["workflows"]:
        claude = root / item["claude"]["path"]
        skill = root / item["codex"]["path"]
        projections.append(Projection(claude, "file", rewrite_frontmatter(claude, {"description": item["claude"]["description"]})))
        projections.append(Projection(skill, "file", rewrite_frontmatter(skill, {"name": item["codex"]["name"].removeprefix("$"), "description": item["codex"]["description"]})))
        projections.append(Projection(skill.parent / "agents/openai.yaml", "file", openai_yaml(item)))
        link = root / ".agents/skills" / item["codex"]["name"].removeprefix("$")
        target = f"../../plugins/butler/skills/{item['codex']['name'].removeprefix('$')}"
        projections.append(Projection(link, "symlink", target=target))
    projections.append(Projection(root / "docs/workflows.md", "file", docs_table(data)))
    return sorted(projections, key=lambda item: item.path.as_posix())


def projection_drift(projection: Projection) -> str | None:
    path = projection.path
    if projection.kind == "symlink":
        if not path.is_symlink():
            return "missing or not a symlink"
        actual = os.readlink(path)
        return None if actual == projection.target else f"symlink target {actual!r} != {projection.target!r}"
    if path.is_symlink() or not path.is_file():
        return "missing or not a regular file"
    return None if path.read_bytes() == projection.content else "content drift"


def atomic_write(path: Path, content: bytes, mode: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, raw = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temp = Path(raw)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(content)
        os.chmod(temp, mode)
        os.replace(temp, path)
    finally:
        temp.unlink(missing_ok=True)


def apply_projections(projections: list[Projection]) -> None:
    snapshots: list[tuple[Projection, str, bytes | None, int | None]] = []
    for item in projections:
        if item.path.is_symlink():
            snapshots.append((item, "symlink", os.readlink(item.path).encode(), None))
        elif item.path.exists():
            snapshots.append((item, "file", item.path.read_bytes(), item.path.stat().st_mode & 0o777))
        else:
            snapshots.append((item, "missing", None, None))
    applied: list[tuple[Projection, str, bytes | None, int | None]] = []
    try:
        for item, old_kind, old_data, old_mode in snapshots:
            if projection_drift(item) is None:
                continue
            item.path.parent.mkdir(parents=True, exist_ok=True)
            if item.kind == "file":
                mode = old_mode if old_kind == "file" and old_mode is not None else 0o644
                atomic_write(item.path, item.content or b"", mode)
            else:
                temp = item.path.parent / f".{item.path.name}.{os.getpid()}.tmp"
                temp.unlink(missing_ok=True)
                os.symlink(item.target or "", temp)
                os.replace(temp, item.path)
            applied.append((item, old_kind, old_data, old_mode))
    except Exception:
        for item, old_kind, old_data, old_mode in reversed(applied):
            item.path.unlink(missing_ok=True)
            if old_kind == "file":
                atomic_write(item.path, old_data or b"", old_mode or 0o644)
            elif old_kind == "symlink":
                os.symlink((old_data or b"").decode(), item.path)
        raise


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--check", action="store_true")
    action.add_argument("--write", action="store_true")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args(argv)
    root = args.root.expanduser().resolve()
    try:
        data = read_registry(root)
        projections = build_projections(data, root)
        drift = [(item, projection_drift(item)) for item in projections]
        drift = [(item, reason) for item, reason in drift if reason]
        if args.check:
            if drift:
                for item, reason in drift:
                    print(f"[DRIFT] {item.path.relative_to(root)}: {reason}", file=sys.stderr)
                return 1
            print(f"[OK] workflow registry projections: workflows=8 projections={len(projections)}")
            return 0
        apply_projections(projections)
        remaining = [(item, projection_drift(item)) for item in projections if projection_drift(item)]
        if remaining:
            raise RegistryError("write completed with projection drift")
        print(f"[OK] synchronized workflow registry: workflows=8 projections={len(projections)} changed={len(drift)}")
        return 0
    except (OSError, RegistryError) as error:
        print(f"workflow-registry: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
