#!/usr/bin/env python3
"""Read-only Butler iteration completion eligibility adjudicator."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

SCHEMA_VERSION = 1
AC_RE = re.compile(r"^- \[[ x]\] (AC[1-9][0-9]*)[：:]", re.MULTILINE)
PASSED_AC_RE = re.compile(r"^- \[x\] (AC[1-9][0-9]*) \(auto·", re.MULTILINE)
EVIDENCE_RE = re.compile(r"\.ai/iterations/(ITER-[0-9]{4,})/evidence/([a-z0-9][a-z0-9._-]*)/record\.json")
TDD_TOOL = Path(__file__).resolve().parents[1] / "verification-evidence" / "evidence.py"


class InputError(ValueError):
    pass


def read(root: Path, relative: str) -> str:
    path = root / relative
    try:
        return path.read_text(encoding="utf-8")
    except OSError as error:
        raise InputError(f"缺少或无法读取 {relative}: {error}") from error


def field(text: str, names: tuple[str, ...]) -> str | None:
    pattern = re.compile(rf"^\s*(?:-\s*)?(?:{'|'.join(map(re.escape, names))})\s*[:：]\s*(\S+)", re.I | re.M)
    match = pattern.search(text)
    return match.group(1).strip().lower() if match else None


def current_iteration(ledger: str) -> tuple[str, str | None]:
    match = re.search(r"^current:\s*(\S+)\s*$", ledger, re.MULTILINE)
    if not match or match.group(1) == "none":
        raise InputError("ITERATIONS.md 没有 current active iteration")
    iteration = match.group(1)
    for line in ledger.splitlines():
        if line.startswith(f"| {iteration} |"):
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            return iteration, cells[2] if len(cells) >= 3 else None
    raise InputError(f"current {iteration} 在台账中无对应行")


def calibration_blockers(text: str) -> list[str]:
    if "# Goal Calibration" not in text:
        return ["task-state 缺少 Goal Calibration 投影"]
    section = text.split("# Goal Calibration", 1)[1]
    blockers: list[str] = []
    for line in section.splitlines():
        if not line.startswith("| CAL-"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 6:
            blockers.append("校准投影行列数非法")
        elif cells[5].lower() in {"open", "blocked"}:
            blockers.append(f"{cells[0]}={cells[5].lower()}")
        elif cells[5].lower() != "resolved":
            blockers.append(f"{cells[0]} 状态未知")
    return blockers


def verify_evidence(root: Path, iteration: str, verify: str) -> tuple[bool, str, set[str]]:
    references = EVIDENCE_RE.findall(verify)
    wrong = {item_iteration for item_iteration, _ in references if item_iteration != iteration}
    ids = {evidence_id for item_iteration, evidence_id in references if item_iteration == iteration}
    evidence_root = root / ".ai" / "verification-evidence"
    actual = {path.name for path in evidence_root.iterdir() if path.is_dir()} if evidence_root.is_dir() else set()
    if wrong or not ids or actual != ids:
        return False, f"Evidence Index/set 不一致: ids={sorted(ids)} actual={sorted(actual)} wrong={sorted(wrong)}", set()
    covered: set[str] = set()
    for evidence_id in sorted(ids):
        directory = evidence_root / evidence_id
        try:
            record = json.loads((directory / "record.json").read_text(encoding="utf-8"))
            if record.get("schema_version") != 1 or record.get("evidence_id") != evidence_id:
                return False, f"{evidence_id} schema/id 非法", covered
            if record.get("iteration") != iteration:
                return False, f"{evidence_id} iteration 不一致", covered
            outcome = record.get("outcome")
            if outcome not in {"passed", "failed", "launch_error", "incomplete", "timeout"}:
                return False, f"{evidence_id} outcome 非法", covered
            for stream_name in ("stdout", "stderr"):
                stream = record[stream_name]
                data = (directory / stream["path"]).read_bytes()
                if stream.get("truncated") or len(data) != stream.get("captured_bytes"):
                    return False, f"{evidence_id}/{stream_name} 不完整", covered
                if hashlib.sha256(data).hexdigest() != stream.get("sha256"):
                    return False, f"{evidence_id}/{stream_name} hash 不符", covered
            if outcome == "passed":
                covered.update(record.get("ac_ids", []))
        except (OSError, KeyError, TypeError, json.JSONDecodeError) as error:
            return False, f"{evidence_id} record 非法: {error}", covered
    return True, f"records={sorted(ids)}; passing_coverage={sorted(covered)}", covered


def verify_tdd_pairs(root: Path, iteration: str) -> tuple[bool, str]:
    command = [
        sys.executable,
        str(TDD_TOOL),
        "check-tdd",
        "--project-root",
        str(root),
        "--iteration",
        iteration,
    ]
    try:
        result = subprocess.run(command, text=True, capture_output=True, check=False)
    except OSError as error:
        return False, f"TDD 配对检查无法启动: {error}"
    detail = "\n".join(part.strip() for part in (result.stdout, result.stderr) if part.strip())
    if result.returncode == 0:
        return True, detail or "TDD 配对检查通过"
    return False, detail or f"TDD 配对检查 exit={result.returncode}"


def evaluate(root: Path) -> dict[str, object]:
    ledger = read(root, ".ai/ITERATIONS.md")
    iteration, ledger_status = current_iteration(ledger)
    ac_text = read(root, ".ai/AC_LIST.md")
    plan_text = read(root, ".ai/TECH_PLAN.md")
    task_text = read(root, ".ai/task-state.md")
    verify_text = read(root, ".ai/VERIFY_REPORT.md")
    required_acs = set(AC_RE.findall(ac_text))
    passed_acs = set(PASSED_AC_RE.findall(verify_text))
    evidence_ok, evidence_detail, evidence_acs = verify_evidence(root, iteration, verify_text)
    tdd_ok, tdd_detail = verify_tdd_pairs(root, iteration)
    calibration = calibration_blockers(task_text)

    raw_checks = [
        ("ledger_active", ledger_status == "active", f"status={ledger_status}"),
        ("acceptance_frozen", field(ac_text, ("状态", "status")) == "ack-frozen", f"state={field(ac_text, ('状态', 'status'))}"),
        ("acceptance_defined", bool(required_acs), f"required={sorted(required_acs)}"),
        ("acceptance_passed", bool(required_acs) and required_acs <= passed_acs, f"passed={sorted(passed_acs)}"),
        ("plan_passed", field(plan_text, ("方案状态", "plan_status")) == "pass", f"state={field(plan_text, ('方案状态', 'plan_status'))}"),
        ("calibration_clear", not calibration, ", ".join(calibration) or "none"),
        ("review_passed", field(verify_text, ("Review Verdict",)) == "pass", f"verdict={field(verify_text, ('Review Verdict',))}"),
        ("completion_blockers_clear", field(verify_text, ("Completion Blockers",)) == "none", f"blockers={field(verify_text, ('Completion Blockers',))}"),
        ("evidence_valid", evidence_ok, evidence_detail),
        ("evidence_covers_ac", bool(required_acs) and required_acs <= evidence_acs, f"covered={sorted(evidence_acs)}"),
        ("tdd_pairs_valid", tdd_ok, tdd_detail),
    ]
    checks = [{"id": check_id, "passed": passed, "detail": detail} for check_id, passed, detail in raw_checks]
    reasons = [f"{item['id']}: {item['detail']}" for item in checks if not item["passed"]]
    return {
        "schema_version": SCHEMA_VERSION,
        "iteration": iteration,
        "verdict": "eligible" if not reasons else "ineligible",
        "reasons": reasons,
        "checks": checks,
        "meaning": "eligible permits the close ritual; complete still derives from closed and audited close facts",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    evaluate_parser = sub.add_parser("evaluate")
    evaluate_parser.add_argument("--project-root", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        root = args.project_root.expanduser().resolve()
        result = evaluate(root)
    except InputError as error:
        print(json.dumps({"schema_version": SCHEMA_VERSION, "error": str(error)}, ensure_ascii=False, sort_keys=True))
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["verdict"] == "eligible" else 1


if __name__ == "__main__":
    raise SystemExit(main())
