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
EVIDENCE_PATH_RE = re.compile(
    r"\.ai/iterations/(ITER-[0-9]{4,})/evidence/([a-z0-9][a-z0-9._-]{0,63})/record\.json"
)
VERSION_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$", re.ASCII)


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

    def audit_iterations(self) -> tuple[str, dict[str, list[str]]]:
        text = self.read(".ai/ITERATIONS.md")
        current = self.current_pointer(text, "ITERATIONS.md")
        rows = self.table_rows(text, "ITER-", 7)
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
        text = path.read_text(encoding="utf-8")
        current = self.current_pointer(text, "MILESTONES.md")
        rows = self.table_rows(text, "MILE-", 7)
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

    def audit_runtime_pointers(self, current: str) -> None:
        for relative in (".ai/task-state.md", ".ai/02_SESSION_HANDOFF.md"):
            path = self.root / relative
            if not path.is_file():
                self.add(False, relative, "文件不存在")
                continue
            text = path.read_text(encoding="utf-8")
            expected = current if current != "none" else "无 active"
            self.add(expected in text, relative, f"应包含当前状态指针：{expected}")

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
            ["git", "tag", "--list", f"v{version}"],
            cwd=self.root,
            text=True,
            capture_output=True,
            check=False,
        )
        self.add(tag.returncode == 0 and tag.stdout.strip() == f"v{version}", "release.tag", f"v{version}")

    def run(self) -> int:
        current, iteration_rows = self.audit_iterations()
        self.audit_milestones(iteration_rows)
        self.audit_runtime_pointers(current)
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
