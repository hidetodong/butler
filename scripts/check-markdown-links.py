#!/usr/bin/env python3
"""Offline checker for repository-local Markdown links and heading fragments."""

from __future__ import annotations

import argparse
import html
import re
import sys
import unicodedata
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urlsplit


EXCLUDED_PARTS = {".git", ".venv", ".uv-cache", "__pycache__", ".worktrees"}
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
ATX_HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$")
SETEXT_RE = re.compile(r"^\s{0,3}(=+|-+)\s*$")
HTML_ANCHOR_RE = re.compile(r"<(?:a\s+(?:[^>]*?\s)?(?:id|name)|[^>]+\sid)=[\"']([^\"']+)[\"']", re.I)
LINK_RE = re.compile(r"!?\[[^\]]*\]\((<[^>]+>|[^\s)]*(?:\([^)]*\)[^\s)]*)?)(?:\s+[\"'][^)]*[\"'])?\)")
INLINE_CODE_RE = re.compile(r"(`+)(.*?)\1")
MARKDOWN_LINK_TEXT_RE = re.compile(r"!?\[([^\]]*)\]\([^)]*\)")
HTML_TAG_RE = re.compile(r"<[^>]+>")
EXTERNAL_SCHEMES = {"http", "https", "mailto", "tel", "data", "ftp", "ssh", "git", "codex"}


@dataclass(frozen=True)
class Problem:
    file: str
    line: int
    target: str
    reason: str

    def render(self) -> str:
        return f"{self.file}:{self.line}: {self.target}: {self.reason}"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root (default: current directory)")
    return parser.parse_args(argv)


def markdown_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*.md"):
        relative = path.relative_to(root)
        if any(part in EXCLUDED_PARTS for part in relative.parts):
            continue
        if path.is_file():
            files.append(path)
    return sorted(files, key=lambda item: item.relative_to(root).as_posix())


def active_markdown_lines(path: Path) -> list[tuple[int, str]]:
    result: list[tuple[int, str]] = []
    fence: str | None = None
    text = path.read_text(encoding="utf-8")
    for number, line in enumerate(text.splitlines(), 1):
        match = FENCE_RE.match(line)
        if match:
            marker = match.group(1)
            if fence is None:
                fence = marker[0]
            elif marker[0] == fence:
                fence = None
            continue
        if fence is not None:
            continue
        without_code = INLINE_CODE_RE.sub("", line)
        result.append((number, without_code))
    return result


def github_slug(raw: str) -> str:
    value = MARKDOWN_LINK_TEXT_RE.sub(r"\1", raw)
    value = INLINE_CODE_RE.sub(lambda match: match.group(2), value)
    value = HTML_TAG_RE.sub("", value)
    value = html.unescape(value).strip().lower()
    value = "".join(
        character
        for character in value
        if character in {"-", "_", " "} or not unicodedata.category(character).startswith("P")
    )
    return re.sub(r"\s+", "-", value)


def anchors(path: Path) -> set[str]:
    result: set[str] = set()
    counts: defaultdict[str, int] = defaultdict(int)
    lines = active_markdown_lines(path)
    previous: tuple[int, str] | None = None
    for number, line in lines:
        for anchor in HTML_ANCHOR_RE.findall(line):
            result.add(unquote(anchor).lower())
        heading = ATX_HEADING_RE.match(line)
        raw_heading: str | None = heading.group(1) if heading else None
        if raw_heading is None and SETEXT_RE.match(line) and previous is not None:
            raw_heading = previous[1].strip()
        if raw_heading:
            base = github_slug(raw_heading)
            if base:
                occurrence = counts[base]
                result.add(base if occurrence == 0 else f"{base}-{occurrence}")
                counts[base] += 1
        previous = (number, line)
    return result


def extract_targets(path: Path) -> list[tuple[int, str]]:
    targets: list[tuple[int, str]] = []
    for number, line in active_markdown_lines(path):
        for match in LINK_RE.finditer(line):
            target = match.group(1)
            if target.startswith("<") and target.endswith(">"):
                target = target[1:-1]
            targets.append((number, html.unescape(target)))
    return targets


def is_external(target: str) -> bool:
    if target.startswith("//"):
        return True
    scheme = urlsplit(target).scheme.lower()
    return bool(scheme and scheme in EXTERNAL_SCHEMES)


def is_within(root: Path, target: Path) -> bool:
    try:
        target.relative_to(root)
    except ValueError:
        return False
    return True


def check(root: Path) -> tuple[list[Problem], int, int]:
    root = root.resolve()
    problems: list[Problem] = []
    files = markdown_files(root)
    link_count = 0
    anchor_cache: dict[Path, set[str]] = {}
    for source in files:
        relative_source = source.relative_to(root).as_posix()
        for line, raw_target in extract_targets(source):
            link_count += 1
            target = raw_target.strip()
            if not target or is_external(target):
                continue
            parsed = urlsplit(target)
            if parsed.scheme:
                problems.append(Problem(relative_source, line, target, f"unsupported link scheme: {parsed.scheme}"))
                continue
            path_text = unquote(parsed.path)
            fragment = unquote(parsed.fragment).lower()
            if path_text.startswith("/"):
                problems.append(Problem(relative_source, line, target, "absolute local path is not allowed"))
                continue
            destination = source if not path_text else source.parent / path_text
            resolved = destination.resolve()
            if not is_within(root, resolved):
                problems.append(Problem(relative_source, line, target, "target escapes repository root"))
                continue
            if not resolved.exists():
                problems.append(Problem(relative_source, line, target, "target does not exist"))
                continue
            if fragment:
                if not resolved.is_file() or resolved.suffix.lower() != ".md":
                    problems.append(Problem(relative_source, line, target, "fragment target is not a Markdown file"))
                    continue
                if resolved not in anchor_cache:
                    anchor_cache[resolved] = anchors(resolved)
                if fragment not in anchor_cache[resolved]:
                    problems.append(Problem(relative_source, line, target, f"heading fragment not found: #{fragment}"))
    problems.sort(key=lambda item: (item.file, item.line, item.target, item.reason))
    return problems, len(files), link_count


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    root = Path(args.root)
    if not root.is_dir():
        print(f"[FAIL] repository root is not a directory: {root}", file=sys.stderr)
        return 2
    try:
        problems, file_count, link_count = check(root)
    except (OSError, UnicodeError) as error:
        print(f"[FAIL] unable to scan Markdown: {error}", file=sys.stderr)
        return 2
    if problems:
        for problem in problems:
            print(problem.render())
        print(f"[FAIL] {len(problems)} broken local Markdown link(s)", file=sys.stderr)
        return 1
    print(f"[OK] Markdown links passed: files={file_count}, links={link_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
