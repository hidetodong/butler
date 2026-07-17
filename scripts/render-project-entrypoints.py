#!/usr/bin/env python3
"""Render/update Butler CLAUDE.md and AGENTS.md as one protected operation."""
from __future__ import annotations

import argparse
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path

MANAGED_START = "<!-- butler-managed:start -->"
MANAGED_END = "<!-- butler-managed:end -->"
USER_START = "<!-- user-managed -->"
USER_END = "<!-- /user-managed -->"
PLACEHOLDERS = ("{{BUTLER_VERSION}}", "{{RULE_CARD_CONTENT}}", "{{BUTLER_PATH}}")


class RenderError(ValueError):
    pass


@dataclass(frozen=True)
class PlannedWrite:
    path: Path
    content: str


def rule_card_content(text: str) -> str:
    marker = "## 角色"
    pos = text.find(marker)
    if pos < 0:
        raise RenderError("templates/rule-card.md is missing the '## 角色' section")
    return text[pos:].strip()


def render_template(template: str, butler_root: Path, version: str, rule_card: str) -> str:
    rendered = template.replace("{{BUTLER_VERSION}}", version)
    rendered = rendered.replace("{{BUTLER_PATH}}", str(butler_root))
    rendered = rendered.replace("{{RULE_CARD_CONTENT}}", rule_card)
    leftovers = [value for value in PLACEHOLDERS if value in rendered]
    if leftovers:
        raise RenderError(f"unresolved placeholders: {', '.join(leftovers)}")
    _single_pair(rendered, USER_START, USER_END, "template user-managed")
    return rendered.strip() + "\n"


def _single_pair(text: str, start: str, end: str, label: str) -> tuple[int, int]:
    if text.count(start) != 1 or text.count(end) != 1:
        raise RenderError(f"{label} markers must appear exactly once")
    start_pos = text.index(start)
    end_pos = text.index(end)
    if end_pos <= start_pos:
        raise RenderError(f"{label} markers are out of order")
    return start_pos, end_pos


def _managed_block(rendered: str) -> str:
    return f"{MANAGED_START}\n{rendered.rstrip()}\n{MANAGED_END}"


def _inject_user_content(rendered: str, user_content: str) -> str:
    new_start, new_end = _single_pair(rendered, USER_START, USER_END, "template user-managed")
    new_inner_start = new_start + len(USER_START)
    return rendered[:new_inner_start] + user_content + rendered[new_end:]


def merge_existing(existing: str | None, rendered: str) -> str:
    """Append a first managed block or replace it while preserving its user region."""
    if existing is None or existing == "":
        return _managed_block(rendered) + "\n"

    start_count = existing.count(MANAGED_START)
    end_count = existing.count(MANAGED_END)
    if start_count == 0 and end_count == 0:
        user_start_count = existing.count(USER_START)
        user_end_count = existing.count(USER_END)
        if user_start_count == 1 and user_end_count == 1 and "规则源：butler v" in existing:
            old_user_start, old_user_end = _single_pair(
                existing, USER_START, USER_END, "legacy user-managed"
            )
            signature_pos = existing.index("规则源：butler v")
            legacy_start = existing.rfind("# 项目工程协作规则", 0, signature_pos)
            if legacy_start < 0:
                raise RenderError("legacy Butler entrypoint start cannot be identified safely")
            inner_start = old_user_start + len(USER_START)
            migrated = _inject_user_content(rendered, existing[inner_start:old_user_end])
            legacy_end = old_user_end + len(USER_END)
            prefix = existing[:legacy_start]
            suffix = existing[legacy_end:]
            return prefix + _managed_block(migrated) + suffix
        if user_start_count or user_end_count:
            raise RenderError("unmanaged file contains ambiguous user-managed markers")
        separator = "" if existing.endswith("\n\n") else ("\n" if existing.endswith("\n") else "\n\n")
        return existing + separator + _managed_block(rendered) + "\n"
    if start_count != 1 or end_count != 1:
        raise RenderError("managed markers must be absent or appear exactly once")

    managed_start, managed_end_pos = _single_pair(
        existing, MANAGED_START, MANAGED_END, "managed"
    )
    managed_end = managed_end_pos + len(MANAGED_END)
    old_block = existing[managed_start:managed_end]
    user_start, user_end = _single_pair(old_block, USER_START, USER_END, "user-managed")
    user_inner_start = user_start + len(USER_START)
    user_content = old_block[user_inner_start:user_end]

    rendered_with_user = _inject_user_content(rendered, user_content)
    return existing[:managed_start] + _managed_block(rendered_with_user) + existing[managed_end:]


def plan(target: Path, butler_root: Path) -> list[PlannedWrite]:
    if not target.exists():
        raise RenderError(f"target project root does not exist: {target}")
    if not target.is_dir():
        raise RenderError(f"target project root is not a directory: {target}")
    if not os.access(target, os.R_OK | os.W_OK | os.X_OK):
        raise RenderError(f"target project root is not readable/writable: {target}")
    version = (butler_root / "VERSION").read_text(encoding="utf-8").strip()
    rule_card = rule_card_content(
        (butler_root / "templates/rule-card.md").read_text(encoding="utf-8")
    )
    plans: list[PlannedWrite] = []
    for filename, template_name in (
        ("CLAUDE.md", "CLAUDE.md.template"),
        ("AGENTS.md", "AGENTS.md.template"),
    ):
        template = (butler_root / "templates" / template_name).read_text(encoding="utf-8")
        rendered = render_template(template, butler_root, version, rule_card)
        path = target / filename
        existing = path.read_text(encoding="utf-8") if path.exists() else None
        plans.append(PlannedWrite(path, merge_existing(existing, rendered)))
    return plans


def apply(plans: list[PlannedWrite]) -> None:
    """Stage every file first, then atomically replace each destination."""
    staged: list[tuple[Path, Path]] = []
    try:
        for item in plans:
            item.path.parent.mkdir(parents=True, exist_ok=True)
            fd, raw_temp = tempfile.mkstemp(prefix=f".{item.path.name}.", dir=item.path.parent)
            temp_path = Path(raw_temp)
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(item.content)
            mode = (item.path.stat().st_mode & 0o777) if item.path.exists() else 0o644
            os.chmod(temp_path, mode)
            staged.append((temp_path, item.path))
        for temp_path, destination in staged:
            os.replace(temp_path, destination)
    finally:
        for temp_path, _ in staged:
            temp_path.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, type=Path, help="Target project root")
    parser.add_argument(
        "--butler-root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Butler checkout root",
    )
    args = parser.parse_args()
    target = args.target.expanduser().resolve()
    butler_root = args.butler_root.expanduser().resolve()
    try:
        plans = plan(target, butler_root)
        apply(plans)
    except (OSError, RenderError) as error:
        print(f"render-project-entrypoints: {error}", file=os.sys.stderr)
        return 2
    print(f"Rendered CLAUDE.md and AGENTS.md in {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
