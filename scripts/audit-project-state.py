#!/usr/bin/env python3
"""Read-only Butler project state and verification evidence auditor."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ITERATION_RE = re.compile(r"^ITER-[0-9]{4,}$", re.ASCII)
MILESTONE_RE = re.compile(r"^MILE-[0-9]{4,}$", re.ASCII)
MILESTONE_BACKLOG_SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$", re.ASCII)
EVIDENCE_PATH_RE = re.compile(
    r"\.ai/iterations/(ITER-[0-9]{4,})/evidence/([a-z0-9][a-z0-9._-]{0,63})/record\.json"
)
VERSION_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$", re.ASCII)
SHARD_RE = re.compile(r"^(ITER|MILE)-([0-9]{6,})-([0-9]{6,})\.md$", re.ASCII)


class AuditError(ValueError):
    """Raised when the audit cannot start safely."""


@dataclass
class Finding:
    ok: bool
    name: str
    detail: str
    level: str = "OK"


class Audit:
    def __init__(self, root: Path, allow_unreleased: bool) -> None:
        self.root = root
        self.allow_unreleased = allow_unreleased
        self.findings: list[Finding] = []

    def add(self, ok: bool, name: str, detail: str) -> None:
        self.findings.append(Finding(ok, name, detail, "OK" if ok else "DRIFT"))

    def note(self, name: str, detail: str, level: str = "INFO") -> None:
        self.findings.append(Finding(True, name, detail, level))

    def read(self, relative: str) -> str:
        return (self.root / relative).read_text(encoding="utf-8")

    def ledger_text(self, hot_relative: str, cold_relative: str) -> str:
        hot = self.read(hot_relative)
        index_path = self.root / ".ai" / "state-index.json"
        if index_path.is_file():
            try:
                index = json.loads(index_path.read_text(encoding="utf-8"))
                if index.get("schema_version") == 2:
                    kind = "iterations" if hot_relative.endswith("ITERATIONS.md") else "milestones"
                    prefix = "ITER" if kind == "iterations" else "MILE"
                    relative_dir = f".ai/history/{kind}"
                    expected_routing = {
                        "scheme": "fixed-range-v1",
                        "directory": relative_dir,
                        "prefix": prefix,
                        "minimum_width": 6,
                        "receipt_suffix": ".json",
                    }
                    ledger = index["ledgers"][kind]
                    if ledger["routing"] != expected_routing:
                        raise AuditError(f"{kind} routing 元数据非法")
                    shard_size = int(index["shard_size"])
                    if shard_size < 1:
                        raise AuditError("shard_size 必须为正数")
                    expected_dir = self.root / relative_dir
                    if expected_dir.is_symlink() or (expected_dir.exists() and not expected_dir.is_dir()):
                        raise AuditError(f"{kind} shard 目录非法")
                    chunks = [hot]
                    if not expected_dir.exists():
                        return hot
                    for path in sorted(expected_dir.glob("*.md")):
                        match = SHARD_RE.fullmatch(path.name)
                        if path.is_symlink() or not path.is_file() or match is None or match.group(1) != prefix:
                            raise AuditError(f"{kind} shard 非法：{path.name}")
                        start, end = int(match.group(2)), int(match.group(3))
                        width = max(6, len(str(end)))
                        canonical = f"{prefix}-{start:0{width}d}-{end:0{width}d}.md"
                        if path.name != canonical or (start - 1) % shard_size or end != start + shard_size - 1:
                            raise AuditError(f"{kind} shard 范围非法：{path.name}")
                        chunks.append(path.read_text(encoding="utf-8"))
                    return "\n".join(chunks)
            except (KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
                raise AuditError(f"state index v2 无法导航 {hot_relative}：{error}") from error
        cold = self.root / cold_relative
        return hot + ("\n" + cold.read_text(encoding="utf-8") if cold.is_file() else "")

    @staticmethod
    def canonical_identity(value: str, prefix: str) -> bool:
        pattern = ITERATION_RE if prefix == "ITER" else MILESTONE_RE
        if pattern.fullmatch(value) is None:
            return False
        numeric = int(value.partition("-")[2])
        return numeric >= 1 and value == f"{prefix}-{numeric:04d}"

    @staticmethod
    def current_pointer(text: str, label: str) -> str:
        for line in text.splitlines():
            if line.startswith("current:"):
                return line.partition(":")[2].strip()
        raise AuditError(f"{label} 缺少 current 指针")

    @staticmethod
    def table_rows(text: str, prefix: str, columns: int) -> dict[str, list[str]]:
        rows: dict[str, list[str]] = {}
        for line in text.splitlines():
            if not line.startswith(f"| {prefix}"):
                continue
            values = [value.strip() for value in line.strip().strip("|").split("|")]
            if len(values) > columns:
                tail_count = columns - 2
                values = [values[0], "|".join(values[1:-tail_count]).strip(), *values[-tail_count:]]
            if len(values) != columns:
                raise AuditError(f"{values[0] if values else prefix} 台账列数应为 {columns}")
            if values[0] in rows:
                raise AuditError(f"台账存在重复 ID：{values[0]}")
            rows[values[0]] = values
        return rows

    @staticmethod
    def milestone_backlog_rows(text: str) -> dict[str, list[str]]:
        rows: dict[str, list[str]] = {}
        in_backlog = False
        for line in text.splitlines():
            if line == "## 待办区（未编号）":
                in_backlog = True
                continue
            if in_backlog and line.startswith("## "):
                break
            if not in_backlog or not line.startswith("| ") or line.startswith("|---") or line.startswith("| 候办键 "):
                continue
            values = [value.strip() for value in line.strip().strip("|").split("|")]
            if len(values) > 5:
                values = [values[0], "|".join(values[1:-3]).strip(), *values[-3:]]
            if len(values) != 5:
                raise AuditError(f"候办项 {values[0] if values else '?'} 列数应为 5")
            if values[0] in rows:
                raise AuditError(f"待办区存在重复候办键：{values[0]}")
            rows[values[0]] = values
        return rows

    def audit_iterations(self) -> tuple[str, dict[str, list[str]]]:
        hot_text = self.read(".ai/ITERATIONS.md")
        text = self.ledger_text(".ai/ITERATIONS.md", ".ai/history/ITERATIONS.cold.md")
        current = self.current_pointer(hot_text, "ITERATIONS.md")
        rows = self.table_rows(text, "ITER-", 7)
        invalid_ids = sorted(iteration for iteration in rows if not self.canonical_identity(iteration, "ITER"))
        self.add(not invalid_ids, "iterations.ids", f"invalid={invalid_ids}" if invalid_ids else "格式均合法")
        active = [iteration for iteration, row in rows.items() if row[2] == "active"]
        valid_status = all(row[2] in {"active", "closed", "abandoned"} for row in rows.values())
        self.add(valid_status, "iterations.status", "状态均合法" if valid_status else "存在非法状态")
        self.add(len(active) <= 1, "iterations.single_active", f"active={active}")
        expected = active[0] if active else "none"
        self.add(current == expected, "iterations.current", f"current={current}, expected={expected}")

        for iteration, row in rows.items():
            if row[2] != "closed":
                continue
            closed_date, delivery = row[4], row[6]
            archive = self.root / ".ai" / "iterations" / iteration
            delivery_path = self.root / delivery
            self.add(closed_date != "—", f"{iteration}.closed_date", closed_date)
            self.add(delivery != "—" and delivery_path.is_file(), f"{iteration}.delivery", delivery)
            iteration_number = int(iteration.partition("-")[2])
            if delivery_path.suffix == ".md" and iteration_number >= 10:
                self.add(delivery_path.with_suffix(".html").is_file(), f"{iteration}.delivery_html", str(delivery_path.with_suffix(".html").relative_to(self.root)))
            required = ("CONCEPT.md", "AC_LIST.md", "TECH_PLAN.md", "VERIFY_REPORT.md")
            missing = [name for name in required if not (archive / name).is_file()]
            self.add(not missing, f"{iteration}.archive", "complete" if not missing else f"missing={missing}")
            verify_path = archive / "VERIFY_REPORT.md"
            if verify_path.is_file() and "# Evidence Index" in verify_path.read_text(encoding="utf-8"):
                self.audit_evidence(iteration, verify_path)
                self.audit_fold_receipt(iteration, archive)
        return current, rows

    def audit_evidence(self, iteration: str, verify_path: Path) -> None:
        text = verify_path.read_text(encoding="utf-8")
        section_match = re.search(
            r"^# Evidence Index\s*$\n(?P<body>.*?)(?=^# (?!Evidence Index\s*$)|\Z)",
            text,
            re.MULTILINE | re.DOTALL,
        )
        evidence_section = section_match.group("body") if section_match else ""
        references = EVIDENCE_PATH_RE.findall(evidence_section)
        ids = sorted({evidence_id for evidence_iteration, evidence_id in references if evidence_iteration == iteration})
        auto_acs = set(re.findall(r"^- \[x\] (AC[1-9][0-9]*) \(auto·", text, re.MULTILINE))
        wrong_iterations = sorted({value for value, _ in references if value != iteration})
        self.add(bool(ids), f"{iteration}.evidence_index", f"ids={ids}" if ids else "Evidence Index 无 record 指针")
        self.add(not wrong_iterations, f"{iteration}.evidence_iteration", f"wrong={wrong_iterations}" if wrong_iterations else "引用迭代一致")
        evidence_root = self.root / ".ai" / "iterations" / iteration / "evidence"
        actual = sorted(path.name for path in evidence_root.iterdir() if path.is_dir()) if evidence_root.is_dir() else []
        self.add(actual == ids, f"{iteration}.evidence_set", f"index={ids}, actual={actual}")
        passed_acs: set[str] = set()
        nonpassing: list[str] = []
        for evidence_id in ids:
            try:
                record = json.loads((evidence_root / evidence_id / "record.json").read_text(encoding="utf-8"))
                if record.get("outcome") == "passed":
                    passed_acs.update(record.get("ac_ids", []))
                else:
                    nonpassing.append(evidence_id)
            except (OSError, json.JSONDecodeError, TypeError):
                nonpassing.append(evidence_id)
        self.add(auto_acs <= passed_acs, f"{iteration}.evidence_ac_coverage", f"auto={sorted(auto_acs)}, passed={sorted(passed_acs)}")
        if nonpassing:
            self.note(f"{iteration}.evidence_diagnostics", f"保留非通过记录={nonpassing}", "INFO")
        tool = Path(__file__).resolve().parent.parent / "tools" / "verification-evidence" / "evidence.py"
        if tool.is_file() and evidence_root.is_dir():
            result = subprocess.run(
                [
                    sys.executable,
                    str(tool),
                    "verify",
                    "--project-root",
                    str(self.root),
                    "--iteration",
                    iteration,
                    "--source",
                    "archive",
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            detail = (result.stdout + result.stderr).strip().replace("\n", "; ")
            self.add(result.returncode == 0, f"{iteration}.evidence_hashes", detail or f"exit={result.returncode}")
        else:
            self.add(False, f"{iteration}.evidence_hashes", "证据工具或归档目录不存在")

    def audit_fold_receipt(self, iteration: str, archive: Path) -> None:
        state_path = self.root / ".ai" / "project" / "fold-state.json"
        try:
            state = json.loads(state_path.read_text(encoding="utf-8"))
            if state.get("schema_version") != 1:
                raise AuditError("fold-state schema_version 必须为 1")
            receipts = state["receipts"]
            if not isinstance(receipts, dict) or not receipts:
                raise AuditError("fold-state receipts 为空")
            receipt = receipts[iteration]
            latest_iteration = max(receipts)
            changelog = receipt["changelog"]
            changelog_path = self.root / changelog["path"]
            expected_path = archive / "CHANGELOG.md"
            if changelog_path.resolve() != expected_path.resolve():
                raise AuditError("receipt changelog 路径不是本迭代归档")
            if hashlib.sha256(changelog_path.read_bytes()).hexdigest() != changelog["sha256"]:
                raise AuditError("receipt changelog SHA-256 不符")
            topics = receipt["topics"]
            if not isinstance(topics, list) or not topics:
                raise AuditError("receipt topics 为空")
            for topic in topics:
                path = self.root / topic["path"]
                if path.resolve().parent != (self.root / ".ai" / "project").resolve():
                    raise AuditError(f"topic 路径越界：{topic['path']}")
                if not isinstance(topic.get("sha256"), str) or SHA256_RE.fullmatch(topic["sha256"]) is None:
                    raise AuditError(f"topic SHA-256 格式非法：{topic['path']}")
                if iteration == latest_iteration and hashlib.sha256(path.read_bytes()).hexdigest() != topic["sha256"]:
                    raise AuditError(f"topic SHA-256 不符：{topic['path']}")
            mode = "current" if iteration == latest_iteration else "historical-snapshot"
            self.add(True, f"{iteration}.fold_receipt", f"topics={len(topics)}, mode={mode}")
        except (OSError, KeyError, TypeError, json.JSONDecodeError, AuditError) as error:
            self.add(False, f"{iteration}.fold_receipt", str(error))

    def audit_milestones(self, iteration_rows: dict[str, list[str]]) -> None:
        path = self.root / ".ai" / "MILESTONES.md"
        if not path.is_file():
            self.note("milestones", "项目未采用里程碑台账", "N/A")
            return
        hot_text = path.read_text(encoding="utf-8")
        text = self.ledger_text(".ai/MILESTONES.md", ".ai/history/MILESTONES.cold.md")
        current = self.current_pointer(hot_text, "MILESTONES.md")
        rows = self.table_rows(text, "MILE-", 7)
        invalid_ids = sorted(milestone for milestone in rows if not self.canonical_identity(milestone, "MILE"))
        self.add(not invalid_ids, "milestones.ids", f"invalid={invalid_ids}" if invalid_ids else "格式均合法")
        numbers = sorted(int(milestone.partition("-")[2]) for milestone in rows if MILESTONE_RE.fullmatch(milestone))
        expected_numbers = list(range(1, numbers[-1] + 1)) if numbers else []
        self.add(numbers == expected_numbers, "milestones.sequence", f"actual={numbers}, expected={expected_numbers}")
        active = [milestone for milestone, row in rows.items() if row[2] == "active"]
        valid_status = all(row[2] in {"active", "closed", "abandoned"} for row in rows.values())
        self.add(valid_status, "milestones.status", "状态均合法" if valid_status else "存在非法状态")
        self.add(len(active) <= 1, "milestones.single_active", f"active={active}")
        expected = active[0] if active else "none"
        self.add(current == expected, "milestones.current", f"current={current}, expected={expected}")
        for milestone, row in rows.items():
            listed = [value.strip() for value in row[5].split(",") if value.strip() and value.strip() != "—"]
            unknown = [iteration for iteration in listed if iteration not in iteration_rows]
            wrong_owner = [iteration for iteration in listed if iteration in iteration_rows and iteration_rows[iteration][5] != milestone]
            self.add(not unknown and not wrong_owner, f"{milestone}.iterations", f"unknown={unknown}, wrong_owner={wrong_owner}")
            if row[2] == "closed":
                delivery = self.root / row[6]
                archive = self.root / ".ai" / "milestones" / milestone / "MILESTONE.md"
                self.add(row[4] != "—" and delivery.is_file(), f"{milestone}.delivery", row[6])
                self.add(archive.is_file(), f"{milestone}.archive", str(archive.relative_to(self.root)))

        workspace = self.root / ".ai" / "MILESTONE.md"
        if current != "none":
            self.add(workspace.is_file(), "milestones.workspace", str(workspace.relative_to(self.root)))
        if current != "none" and workspace.is_file():
            for line in workspace.read_text(encoding="utf-8").splitlines():
                if not line.startswith("| R"):
                    continue
                values = [value.strip() for value in line.strip().strip("|").split("|")]
                if len(values) > 4:
                    values = [values[0], "|".join(values[1:-2]).strip(), *values[-2:]]
                if len(values) != 4 or values[2] == "—":
                    continue
                iteration, route_status = values[2], values[3]
                actual = iteration_rows.get(iteration, ["", "", "missing"])[2]
                self.add(route_status == actual, f"route.{values[0]}", f"{iteration}: route={route_status}, ledger={actual}")

        backlog_rows = self.milestone_backlog_rows(hot_text)
        backlog_root = self.root / ".ai" / "milestone-backlog"
        indexed_paths: set[str] = set()
        for slug, row in backlog_rows.items():
            valid_slug = MILESTONE_BACKLOG_SLUG_RE.fullmatch(slug) is not None and not slug.startswith("mile-")
            self.add(valid_slug, f"backlog.{slug}.slug", "kebab-case" if valid_slug else "候办键非法或伪装成正式里程碑号")
            expected_path = f".ai/milestone-backlog/{slug}.md"
            valid_path = row[3] == expected_path
            self.add(valid_path, f"backlog.{slug}.path", f"actual={row[3]}, expected={expected_path}")
            if not valid_path:
                continue
            indexed_paths.add(row[3])
            draft = self.root / row[3]
            valid_draft = draft.is_file() and not draft.is_symlink()
            self.add(valid_draft, f"backlog.{slug}.draft", row[3])
            if valid_draft:
                draft_text = draft.read_text(encoding="utf-8")
                key_markers = [value.strip() for value in re.findall(r"(?m)^候办键:\s*([^\r\n]+?)\s*$", draft_text)]
                state_markers = [value.strip() for value in re.findall(r"(?m)^候办状态:\s*([^\r\n]+?)\s*$", draft_text)]
                markers_ok = key_markers == [slug] and state_markers == ["deferred"]
                detail = "unique identity" if markers_ok else f"keys={key_markers}, states={state_markers}"
                self.add(markers_ok, f"backlog.{slug}.markers", detail)

        actual_drafts = {
            str(path.relative_to(self.root))
            for path in backlog_root.rglob("*.md")
        } if backlog_root.is_dir() else set()
        self.add(actual_drafts == indexed_paths, "milestones.backlog_set", f"index={sorted(indexed_paths)}, actual={sorted(actual_drafts)}")

    def audit_runtime_pointers(self, current: str) -> None:
        for relative in (".ai/task-state.md", ".ai/02_SESSION_HANDOFF.md"):
            path = self.root / relative
            if not path.is_file():
                self.add(False, relative, "文件不存在")
                continue
            text = path.read_text(encoding="utf-8")
            expected = current if current != "none" else "无 active"
            self.add(expected in text, relative, f"应包含当前状态指针：{expected}")

    def audit_handoff_freshness(self) -> None:
        receipt = self.root / ".ai" / "handoff-state.json"
        if not receipt.exists():
            self.note("handoff.freshness", "legacy：尚无 handoff receipt", "N/A")
            return
        tool = Path(__file__).resolve().parent.parent / "tools" / "handoff" / "handoff.py"
        result = subprocess.run(
            [sys.executable, str(tool), "check", "--project-root", str(self.root)],
            text=True,
            capture_output=True,
            check=False,
        )
        detail = (result.stdout + result.stderr).strip().replace("\n", "; ")
        self.add(result.returncode == 0, "handoff.freshness", detail or f"exit={result.returncode}")

    def audit_state_index(self) -> None:
        index = self.root / ".ai" / "state-index.json"
        if not index.exists():
            self.note("state_index", "legacy：尚未迁移双台账热冷分层", "N/A")
            return
        tool = self.root / "tools" / "state-ledger" / "state_ledger.py"
        result = subprocess.run(
            [sys.executable, str(tool), "check", "--project-root", str(self.root)],
            text=True, capture_output=True, check=False,
        )
        detail = (result.stdout + result.stderr).strip().replace("\n", "; ")
        self.add(result.returncode == 0, "state_index", detail or f"exit={result.returncode}")

    def audit_release_metadata(self) -> None:
        version_path = self.root / "VERSION"
        plugin_path = self.root / "plugins" / "butler" / ".codex-plugin" / "plugin.json"
        if not version_path.is_file() or not plugin_path.is_file():
            self.note("release", "非 Butler 规则仓，跳过发布元数据", "N/A")
            return
        version = version_path.read_text(encoding="utf-8").strip()
        self.add(bool(VERSION_RE.fullmatch(version)), "release.version", version)
        try:
            plugin_version = json.loads(plugin_path.read_text(encoding="utf-8"))["version"]
        except (OSError, KeyError, json.JSONDecodeError) as error:
            self.add(False, "release.plugin", str(error))
            return
        self.add(plugin_version == version, "release.plugin", f"VERSION={version}, plugin={plugin_version}")
        changelog = self.root / "CHANGELOG.md"
        migration = self.root / "migrations" / f"v{version}.md"
        self.add(changelog.is_file() and f"## [{version}]" in changelog.read_text(encoding="utf-8"), "release.changelog", version)
        self.add(migration.is_file(), "release.migration", str(migration.relative_to(self.root)))

        git = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=self.root,
            text=True,
            capture_output=True,
            check=False,
        )
        if git.returncode != 0:
            self.add(False, "release.git", git.stderr.strip() or "git status 失败")
            return
        dirty = bool(git.stdout.strip())
        if dirty:
            if self.allow_unreleased:
                self.note("release.worktree", "UNRELEASED：工作树有未发布改动", "UNRELEASED")
            else:
                self.add(False, "release.worktree", "工作树有未发布改动；需要 --allow-unreleased 亮牌")
        tag = subprocess.run(
            ["git", "tag", "--points-at", "HEAD"],
            cwd=self.root,
            text=True,
            capture_output=True,
            check=False,
        )
        current_tag = f"v{version}"
        points_at_head = tag.returncode == 0 and current_tag in tag.stdout.splitlines()
        if points_at_head:
            self.add(True, "release.tag", f"{current_tag} points at HEAD")
        elif self.allow_unreleased:
            self.note("release.tag", f"UNRELEASED：{current_tag} 不指向 HEAD", "UNRELEASED")
        else:
            self.add(False, "release.tag", f"{current_tag} 不指向 HEAD；需要 --allow-unreleased 亮牌")

    def run(self) -> int:
        current, iteration_rows = self.audit_iterations()
        self.audit_milestones(iteration_rows)
        self.audit_runtime_pointers(current)
        self.audit_handoff_freshness()
        self.audit_state_index()
        self.audit_release_metadata()
        for finding in self.findings:
            print(f"[{finding.level}] {finding.name}: {finding.detail}")
        return 1 if any(not finding.ok for finding in self.findings) else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", required=True, type=Path)
    parser.add_argument("--allow-unreleased", action="store_true")
    args = parser.parse_args()
    root = args.project_root.expanduser().resolve()
    if not root.is_dir() or not (root / ".ai" / "ITERATIONS.md").is_file():
        print(f"audit-project-state: 不是已部署 Butler 的项目根：{root}", file=sys.stderr)
        return 2
    try:
        return Audit(root, args.allow_unreleased).run()
    except (AuditError, OSError, UnicodeError, json.JSONDecodeError) as error:
        print(f"audit-project-state: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
