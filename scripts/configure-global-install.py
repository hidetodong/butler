#!/usr/bin/env python3
"""Safely configure Butler's user-level Claude and shell integration."""
from __future__ import annotations

import argparse
import os
import re
import shlex
import stat
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

GLOBAL_MARKER = "<!-- butler-global-config -->"
EXPORT_RE = re.compile(r"^[ \t]*export[ \t]+BUTLER_PATH[ \t]*=", re.ASCII)


class ConfigError(ValueError):
    """Raised when user-owned state cannot be changed safely."""


@dataclass(frozen=True)
class FileWrite:
    path: Path
    content: str
    mode: int
    expected_content: str | None
    action: str


@dataclass(frozen=True)
class LinkWrite:
    path: Path
    target: Path
    expected_raw_target: str | None
    action: str


@dataclass(frozen=True)
class LinkRemoval:
    path: Path
    expected_raw_target: str
    action: str


@dataclass
class InstallPlan:
    file_writes: list[FileWrite] = field(default_factory=list)
    link_writes: list[LinkWrite] = field(default_factory=list)
    link_removals: list[LinkRemoval] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


def _lexists(path: Path) -> bool:
    return os.path.lexists(path)


def _normalized_link_target(link: Path) -> Path:
    raw = Path(os.readlink(link))
    target = raw if raw.is_absolute() else link.parent / raw
    return Path(os.path.abspath(os.path.normpath(target)))


def _butler_root_for_command_target(target: Path) -> Path | None:
    """Return a recognizable Butler root encoded by a command target path."""
    root: Path | None = None
    if (
        target.name == "butler"
        and target.parent.name == "commands"
        and target.parent.parent.name == ".claude"
    ):
        root = target.parent.parent.parent
    elif (
        target.name == "butler.md"
        and target.parent.name == "commands"
        and target.parent.parent.name == ".claude"
    ):
        root = target.parent.parent.parent
    elif (
        target.name == "butler-prd.md"
        and target.parent.name == "commands"
        and target.parent.parent.name == ".claude"
    ):
        root = target.parent.parent.parent
    elif (
        target.name == "prd.md"
        and target.parent.name == "butler"
        and target.parent.parent.name == "commands"
        and target.parent.parent.parent.name == ".claude"
    ):
        root = target.parent.parent.parent.parent
    if root is None:
        return None
    if (root / "Coder" / "README.md").is_file() and (root / "scripts" / "setup.sh").is_file():
        return root
    return None


def _read_regular_user_file(path: Path, label: str) -> tuple[str | None, int]:
    if not _lexists(path):
        return None, 0o644
    if path.is_symlink():
        raise ConfigError(
            f"{label} 是符号链接，无法在不改变链接语义的前提下原子替换：{path}。"
            "请先确认其真实目标并手动处理。"
        )
    if not path.is_file():
        raise ConfigError(f"{label} 不是普通文件：{path}。未做任何修改。")
    return path.read_bytes().decode("utf-8"), stat.S_IMODE(path.stat().st_mode)


def _append_block(existing: str, block: str) -> str:
    if not existing:
        return block
    if existing.endswith("\n\n"):
        separator = ""
    elif existing.endswith("\n"):
        separator = "\n"
    else:
        separator = "\n\n"
    return existing + separator + block


def merge_shell_rc(existing: str, butler_root: Path) -> str:
    lines = existing.splitlines(keepends=True)
    matches = [index for index, line in enumerate(lines) if EXPORT_RE.match(line.rstrip("\r\n"))]
    canonical = f"export BUTLER_PATH={shlex.quote(str(butler_root))}"
    if len(matches) > 1:
        line_numbers = ", ".join(str(index + 1) for index in matches)
        raise ConfigError(
            f"shell 配置中发现多条有效 BUTLER_PATH export（行 {line_numbers}）。"
            "请合并为一条后重试。"
        )
    if len(matches) == 1:
        index = matches[0]
        ending = "\r\n" if lines[index].endswith("\r\n") else ("\n" if lines[index].endswith("\n") else "")
        lines[index] = canonical + ending
        return "".join(lines)
    block = f"# Butler 规则仓库路径\n{canonical}\n"
    return _append_block(existing, block)


def render_global_block(butler_root: Path) -> str:
    return f"""{GLOBAL_MARKER}
## Butler 工程协作规则

本机 butler 规则仓库路径: {butler_root}

当用户给出工程开发任务时，从入口文件开始建立规则上下文：
1. 读取 {butler_root}/Coder/README.md（入口文件，包含目录结构与读取顺序）
2. 按其中定义的读取顺序依次读取规则文件
3. 若当前项目不存在 .ai/ 目录，视为新项目接入，按规则自然触发基地车部署

## 个人沟通风格（跟着 butler 仓走·每个会话常开）
下面这行把沟通风格正本 @import 进来，规定我该怎么跟你说话（语气/详略/说人话）。改说话风格改那个文件即可，它是唯一正本。
@{butler_root}/communication-style.md
{GLOBAL_MARKER}
"""


def merge_global_claude(existing: str, butler_root: Path) -> str:
    lines = existing.splitlines(keepends=True)
    marker_lines: list[tuple[int, int]] = []
    offset = 0
    for line in lines:
        body = line.rstrip("\r\n")
        if body == GLOBAL_MARKER:
            marker_lines.append((offset, offset + len(line)))
        offset += len(line)
    if existing.count(GLOBAL_MARKER) != len(marker_lines):
        raise ConfigError(
            f"Claude 全局配置中的 Butler marker 必须独占一行：{GLOBAL_MARKER}。未做任何修改。"
        )
    if not marker_lines:
        return _append_block(existing, render_global_block(butler_root))
    if len(marker_lines) != 2:
        raise ConfigError(
            f"Claude 全局配置应有 0 个或 2 个 Butler marker，实际为 {len(marker_lines)} 个："
            f"{GLOBAL_MARKER}。请修复边界后重试。"
        )
    start = marker_lines[0][0]
    end = marker_lines[1][1]
    return existing[:start] + render_global_block(butler_root) + existing[end:]


def _plan_file(
    plan: InstallPlan,
    path: Path,
    existing: str | None,
    content: str,
    mode: int,
    label: str,
) -> None:
    if existing == content:
        plan.notes.append(f"[保持] {label} 已是最新：{path}")
        return
    action = "写入" if existing is None else "更新"
    plan.file_writes.append(
        FileWrite(path, content, mode, existing, f"[{action}] {label}：{path}")
    )


def _plan_shell(plan: InstallPlan, home: Path, butler_root: Path) -> None:
    candidates = (home / ".zshrc", home / ".bashrc")
    selected: Path | None = None
    for candidate in candidates:
        if _lexists(candidate):
            selected = candidate
            break
    if selected is None:
        plan.notes.append(
            f"[跳过] 未找到 .zshrc 或 .bashrc；请手动添加："
            f"export BUTLER_PATH={shlex.quote(str(butler_root))}"
        )
        return
    existing, mode = _read_regular_user_file(selected, "shell 配置")
    assert existing is not None
    merged = merge_shell_rc(existing, butler_root)
    _plan_file(plan, selected, existing, merged, mode, "BUTLER_PATH")


def _plan_claude(plan: InstallPlan, home: Path, butler_root: Path) -> None:
    path = home / ".claude" / "CLAUDE.md"
    existing, mode = _read_regular_user_file(path, "Claude 全局配置")
    merged = merge_global_claude(existing or "", butler_root)
    _plan_file(plan, path, existing, merged, mode, "Claude 全局配置")


def _plan_legacy_flat_link(plan: InstallPlan, home: Path) -> None:
    path = home / ".claude" / "commands" / "butler-prd.md"
    if not _lexists(path):
        return
    if not path.is_symlink():
        plan.notes.append(f"[保留] 旧命令同名目标不是 Butler 软链，未接管：{path}")
        return
    raw = os.readlink(path)
    target = _normalized_link_target(path)
    if _butler_root_for_command_target(target) is None:
        plan.notes.append(f"[保留] 无法证明旧命令软链属于 Butler，未删除：{path} -> {raw}")
        return
    plan.link_removals.append(LinkRemoval(path, raw, f"[清理] 已认领的旧命令软链：{path}"))


def _plan_command_link(plan: InstallPlan, home: Path, butler_root: Path) -> None:
    source = butler_root / ".claude" / "commands" / "butler"
    if not source.is_dir():
        raise ConfigError(f"Butler 命令源不存在：{source}")
    destination = home / ".claude" / "commands" / "butler"
    if not _lexists(destination):
        plan.link_writes.append(
            LinkWrite(destination, source, None, f"[软链] Butler 命令命名空间：{destination}")
        )
        return
    if not destination.is_symlink():
        raise ConfigError(
            f"Claude 命令目标已存在且不是软链：{destination}。"
            "Butler 不会删除或写入该目标；请改名或手动确认后重试。"
        )
    target = _normalized_link_target(destination)
    if target == source:
        plan.notes.append(f"[保持] Butler 命令软链已是最新：{destination}")
        return
    if _butler_root_for_command_target(target) is None:
        raise ConfigError(
            f"Claude 命令软链不属于可识别的 Butler checkout：{destination} -> {os.readlink(destination)}。"
            "未覆盖该软链；请人工确认所有权。"
        )
    plan.link_writes.append(
        LinkWrite(
            destination,
            source,
            os.readlink(destination),
            f"[更新] Butler 命令软链迁移到当前仓库：{destination}",
        )
    )


def _plan_router_link(plan: InstallPlan, home: Path, butler_root: Path) -> None:
    source = butler_root / ".claude" / "commands" / "butler.md"
    if not source.is_file():
        raise ConfigError(f"Butler Router 命令源不存在：{source}")
    destination = home / ".claude" / "commands" / "butler.md"
    if not _lexists(destination):
        plan.link_writes.append(LinkWrite(destination, source, None, f"[软链] Butler Router 根命令：{destination}"))
        return
    if not destination.is_symlink():
        raise ConfigError(f"Claude Router 命令目标已存在且不是软链：{destination}。Butler 不会覆盖用户文件。")
    target = _normalized_link_target(destination)
    if target == source:
        plan.notes.append(f"[保持] Butler Router 命令软链已是最新：{destination}")
        return
    if _butler_root_for_command_target(target) is None:
        raise ConfigError(f"Claude Router 命令软链不属于可识别的 Butler checkout：{destination} -> {os.readlink(destination)}。")
    plan.link_writes.append(LinkWrite(destination, source, os.readlink(destination), f"[更新] Butler Router 命令软链迁移到当前仓库：{destination}"))


def plan_global_install(home: Path, butler_root: Path) -> InstallPlan:
    home = home.expanduser().resolve()
    butler_root = butler_root.expanduser().resolve()
    if not home.is_dir():
        raise ConfigError(f"HOME 不是可用目录：{home}")
    if not (butler_root / "Coder" / "README.md").is_file():
        raise ConfigError(f"不是可识别的 Butler 仓库：{butler_root}")
    if "\n" in str(butler_root) or "\r" in str(butler_root):
        raise ConfigError("Butler 仓库路径含换行，无法安全写入 shell/Markdown 配置。")
    plan = InstallPlan()
    _plan_shell(plan, home, butler_root)
    _plan_claude(plan, home, butler_root)
    _plan_legacy_flat_link(plan, home)
    _plan_command_link(plan, home, butler_root)
    _plan_router_link(plan, home, butler_root)
    return plan


def _stage_file(item: FileWrite) -> Path:
    item.path.parent.mkdir(parents=True, exist_ok=True)
    fd, raw_temp = tempfile.mkstemp(prefix=f".{item.path.name}.", dir=item.path.parent)
    temp_path = Path(raw_temp)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(item.content.encode("utf-8"))
        os.chmod(temp_path, item.mode)
    except BaseException:
        temp_path.unlink(missing_ok=True)
        raise
    return temp_path


def _stage_link(item: LinkWrite) -> Path:
    item.path.parent.mkdir(parents=True, exist_ok=True)
    fd, raw_temp = tempfile.mkstemp(prefix=f".{item.path.name}.", dir=item.path.parent)
    os.close(fd)
    temp_path = Path(raw_temp)
    temp_path.unlink()
    try:
        temp_path.symlink_to(item.target)
    except BaseException:
        temp_path.unlink(missing_ok=True)
        raise
    return temp_path


def _validate_plan_unchanged(plan: InstallPlan) -> None:
    """Fail before the first commit if user state changed after planning."""
    for item in plan.file_writes:
        if item.expected_content is None:
            if _lexists(item.path):
                raise ConfigError(f"规划后目标文件被创建，停止覆盖：{item.path}")
            continue
        current, _ = _read_regular_user_file(item.path, "待更新用户配置")
        if current != item.expected_content:
            raise ConfigError(f"规划后用户配置发生变化，停止覆盖：{item.path}")
    for item in plan.link_removals:
        if not item.path.is_symlink() or os.readlink(item.path) != item.expected_raw_target:
            raise ConfigError(f"规划后旧命令软链发生变化，停止清理：{item.path}")
    for item in plan.link_writes:
        if item.expected_raw_target is None:
            if _lexists(item.path):
                raise ConfigError(f"规划后命令目标被创建，停止覆盖：{item.path}")
            continue
        if not item.path.is_symlink() or os.readlink(item.path) != item.expected_raw_target:
            raise ConfigError(f"规划后命令软链发生变化，停止覆盖：{item.path}")


def apply_global_install(plan: InstallPlan) -> None:
    staged_files: list[tuple[Path, FileWrite]] = []
    staged_links: list[tuple[Path, LinkWrite]] = []
    try:
        # Do not create even staging directories when the plan is already stale.
        _validate_plan_unchanged(plan)
        for item in plan.file_writes:
            staged_files.append((_stage_file(item), item))
        for item in plan.link_writes:
            staged_links.append((_stage_link(item), item))

        # Close the race window introduced by staging work before the first commit.
        _validate_plan_unchanged(plan)
        for note in plan.notes:
            print(note)
        for temp_path, item in staged_files:
            os.replace(temp_path, item.path)
            print(item.action)
        for item in plan.link_removals:
            item.path.unlink()
            print(item.action)
        for temp_path, item in staged_links:
            os.replace(temp_path, item.path)
            print(item.action)
    finally:
        for temp_path, _ in staged_files + staged_links:
            temp_path.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--butler-root", required=True, type=Path)
    parser.add_argument("--home", type=Path, default=None, help="Override HOME for isolated testing")
    args = parser.parse_args()
    raw_home = args.home or (Path(os.environ["HOME"]) if os.environ.get("HOME") else None)
    if raw_home is None:
        print("configure-global-install: HOME is not set", file=sys.stderr)
        return 2
    try:
        plan = plan_global_install(raw_home, args.butler_root)
        apply_global_install(plan)
    except (ConfigError, OSError, UnicodeError) as error:
        print(f"configure-global-install: {error}", file=sys.stderr)
        print("如上方已经出现成功步骤，它们不会被伪称为已回滚；请按错误对象检查。", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
