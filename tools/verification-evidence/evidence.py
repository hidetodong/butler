#!/usr/bin/env python3
"""Capture, verify, archive, and reopen Butler verification evidence."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import BinaryIO

SCHEMA_VERSION = 1
ID_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{0,63}$", re.ASCII)
ITERATION_RE = re.compile(r"^ITER-[0-9]{4,}$", re.ASCII)
AC_RE = re.compile(r"^AC[1-9][0-9]*$", re.ASCII)
DEFAULT_TIMEOUT = 900.0
DEFAULT_MAX_OUTPUT_BYTES = 1_048_576


class EvidenceError(ValueError):
    """Raised when an evidence operation cannot be performed safely."""


@dataclass
class StreamCapture:
    path: Path
    limit: int
    total_bytes: int = 0
    captured_bytes: int = 0
    sha256: str = ""
    truncated: bool = False
    error: BaseException | None = None

    def drain(self, pipe: BinaryIO) -> None:
        digest = hashlib.sha256()
        try:
            with self.path.open("wb") as output:
                while True:
                    chunk = pipe.read(65_536)
                    if not chunk:
                        break
                    self.total_bytes += len(chunk)
                    remaining = max(0, self.limit - self.captured_bytes)
                    kept = chunk[:remaining]
                    if kept:
                        output.write(kept)
                        digest.update(kept)
                        self.captured_bytes += len(kept)
                    if len(kept) != len(chunk):
                        self.truncated = True
        except BaseException as error:  # surfaced after both pipes are drained
            self.error = error
        finally:
            pipe.close()
            self.sha256 = digest.hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def resolve_project_root(raw: Path) -> Path:
    root = raw.expanduser().resolve()
    if not root.is_dir() or not (root / ".ai" / "ITERATIONS.md").is_file():
        raise EvidenceError(f"不是已部署 Butler 的项目根：{root}")
    if (root / ".ai").is_symlink():
        raise EvidenceError(f".ai 不得是符号链接：{root / '.ai'}")
    return root


def require_iteration(value: str) -> str:
    if not ITERATION_RE.fullmatch(value):
        raise EvidenceError(f"非法迭代号：{value}")
    return value


def current_iteration(root: Path) -> str:
    for line in (root / ".ai" / "ITERATIONS.md").read_text(encoding="utf-8").splitlines():
        if line.startswith("current:"):
            value = line.partition(":")[2].strip()
            if value == "none" or ITERATION_RE.fullmatch(value):
                return value
            break
    raise EvidenceError("ITERATIONS.md 缺少合法 current 指针")


def iteration_is_closed(root: Path, iteration: str) -> bool:
    for line in (root / ".ai" / "ITERATIONS.md").read_text(encoding="utf-8").splitlines():
        if not line.startswith(f"| {iteration} |"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        return len(cells) >= 3 and cells[2] == "closed"
    return False


def require_current(root: Path, iteration: str, allow_closed: bool = False) -> None:
    current = current_iteration(root)
    if allow_closed and current == "none" and iteration_is_closed(root, iteration):
        return
    if current != iteration:
        raise EvidenceError(f"证据迭代 {iteration} 与 current {current} 不一致")


def parse_ac_ids(raw: str) -> list[str]:
    values = [value.strip() for value in raw.split(",") if value.strip()]
    if not values or any(not AC_RE.fullmatch(value) for value in values):
        raise EvidenceError(f"AC 列表非法：{raw}")
    return list(dict.fromkeys(values))


def resolve_cwd(root: Path, raw: str) -> tuple[Path, str]:
    relative = Path(raw)
    if relative.is_absolute():
        raise EvidenceError("--cwd 必须是项目根内相对路径")
    resolved = (root / relative).resolve()
    try:
        normalized = resolved.relative_to(root)
    except ValueError as error:
        raise EvidenceError(f"--cwd 越出项目根：{raw}") from error
    if not resolved.is_dir():
        raise EvidenceError(f"--cwd 不是目录：{raw}")
    return resolved, normalized.as_posix() if normalized.parts else "."


def record_stream(capture: StreamCapture, name: str) -> dict[str, object]:
    return {
        "path": f"{name}.log",
        "bytes": capture.total_bytes,
        "captured_bytes": capture.captured_bytes,
        "sha256": capture.sha256,
        "truncated": capture.truncated,
    }


def terminate_process_group(process: subprocess.Popen[bytes]) -> None:
    if os.name == "posix":
        try:
            os.killpg(process.pid, signal.SIGKILL)
            return
        except ProcessLookupError:
            return
        except OSError:
            pass
    process.kill()


def write_record(path: Path, record: dict[str, object]) -> None:
    path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def capture_run(args: argparse.Namespace) -> int:
    root = resolve_project_root(args.project_root)
    iteration = require_iteration(args.iteration)
    require_current(root, iteration, args.allow_closed)
    if not ID_RE.fullmatch(args.evidence_id):
        raise EvidenceError(f"非法 evidence ID：{args.evidence_id}")
    ac_ids = parse_ac_ids(args.ac)
    if args.timeout <= 0 or args.max_output_bytes <= 0:
        raise EvidenceError("timeout 和 max-output-bytes 必须为正数")
    cwd, relative_cwd = resolve_cwd(root, args.cwd)
    command = list(args.command)
    if command and command[0] == "--":
        command.pop(0)
    if not command:
        raise EvidenceError("缺少 -- 后的验证命令 argv")

    hot_root = root / ".ai" / "verification-evidence"
    if os.path.lexists(hot_root) and hot_root.is_symlink():
        raise EvidenceError(f"证据热区不得是符号链接：{hot_root}")
    hot_root.mkdir(parents=True, exist_ok=True)
    destination = hot_root / args.evidence_id
    claim = hot_root / f".claim-{args.evidence_id}"
    if os.path.lexists(destination):
        raise EvidenceError(f"evidence ID 已存在，禁止覆盖：{args.evidence_id}")
    try:
        claim.mkdir()
    except FileExistsError as error:
        raise EvidenceError(f"evidence ID 正在使用或残留 claim：{args.evidence_id}") from error

    temp_dir = Path(tempfile.mkdtemp(prefix=f".tmp-{args.evidence_id}-", dir=hot_root))
    stdout_capture = StreamCapture(temp_dir / "stdout.log", args.max_output_bytes)
    stderr_capture = StreamCapture(temp_dir / "stderr.log", args.max_output_bytes)
    started_at = utc_now()
    started_clock = time.monotonic()
    process_exit_code: int | None = None
    outcome = "launch_error"
    launch_error: str | None = None
    runner_exit = 2
    process: subprocess.Popen[bytes] | None = None
    threads: list[threading.Thread] = []
    try:
        try:
            process = subprocess.Popen(
                command,
                cwd=cwd,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=False,
                start_new_session=(os.name == "posix"),
            )
            assert process.stdout is not None and process.stderr is not None
            threads = [
                threading.Thread(target=stdout_capture.drain, args=(process.stdout,), daemon=True),
                threading.Thread(target=stderr_capture.drain, args=(process.stderr,), daemon=True),
            ]
            for thread in threads:
                thread.start()
            try:
                process_exit_code = process.wait(timeout=args.timeout)
            except subprocess.TimeoutExpired:
                terminate_process_group(process)
                process_exit_code = process.wait()
                outcome = "timeout"
                runner_exit = 124
            for thread in threads:
                thread.join()
            stream_errors = [capture.error for capture in (stdout_capture, stderr_capture) if capture.error]
            if stream_errors:
                raise OSError(f"读取子进程输出失败：{stream_errors[0]}")
            if outcome != "timeout":
                if stdout_capture.truncated or stderr_capture.truncated:
                    outcome = "incomplete"
                    runner_exit = 3
                elif process_exit_code == 0:
                    outcome = "passed"
                    runner_exit = 0
                else:
                    outcome = "failed"
                    runner_exit = 1
        except OSError as error:
            launch_error = str(error)
            stderr_capture.path.write_bytes((launch_error + "\n").encode("utf-8"))
            stderr_capture.total_bytes = stderr_capture.path.stat().st_size
            stderr_capture.captured_bytes = stderr_capture.total_bytes
            stderr_capture.sha256 = hashlib.sha256(stderr_capture.path.read_bytes()).hexdigest()
            if not stdout_capture.path.exists():
                stdout_capture.path.write_bytes(b"")
                stdout_capture.sha256 = hashlib.sha256(b"").hexdigest()

        finished_at = utc_now()
        record: dict[str, object] = {
            "schema_version": SCHEMA_VERSION,
            "evidence_id": args.evidence_id,
            "iteration": iteration,
            "ac_ids": ac_ids,
            "command": {"argv": command, "cwd": relative_cwd},
            "started_at": started_at,
            "finished_at": finished_at,
            "duration_ms": round((time.monotonic() - started_clock) * 1000),
            "process_exit_code": process_exit_code,
            "outcome": outcome,
            "stdout": record_stream(stdout_capture, "stdout"),
            "stderr": record_stream(stderr_capture, "stderr"),
        }
        if launch_error is not None:
            record["launch_error"] = launch_error
        write_record(temp_dir / "record.json", record)
        if os.path.lexists(destination):
            raise EvidenceError(f"运行期间 evidence ID 被占用：{args.evidence_id}")
        os.rename(temp_dir, destination)
        print(f"[{outcome}] {args.evidence_id} -> {destination / 'record.json'}")
        return runner_exit
    finally:
        if process is not None and process.poll() is None:
            terminate_process_group(process)
            process.wait()
        for thread in threads:
            thread.join(timeout=1)
        shutil.rmtree(temp_dir, ignore_errors=True)
        claim.rmdir()


def safe_log_path(item_root: Path, raw: object, expected: str) -> Path:
    if raw != expected:
        raise EvidenceError(f"日志路径必须为 {expected}，实际为 {raw!r}")
    path = (item_root / expected).resolve()
    if (item_root / expected).is_symlink():
        raise EvidenceError(f"日志不得是符号链接：{raw}")
    try:
        path.relative_to(item_root.resolve())
    except ValueError as error:
        raise EvidenceError(f"日志路径越界：{raw}") from error
    return path


def validate_record(item_root: Path, expected_iteration: str | None = None) -> list[str]:
    errors: list[str] = []
    record_path = item_root / "record.json"
    try:
        if item_root.is_symlink() or record_path.is_symlink():
            raise EvidenceError("证据目录和 record.json 不得是符号链接")
        expected_names = {"record.json", "stdout.log", "stderr.log"}
        actual_names = {path.name for path in item_root.iterdir()}
        if actual_names != expected_names:
            raise EvidenceError(f"证据目录文件集不符：{sorted(actual_names)}")
        record = json.loads(record_path.read_text(encoding="utf-8"))
        if not isinstance(record, dict):
            raise EvidenceError("record 根必须是对象")
        evidence_id = record.get("evidence_id")
        if evidence_id != item_root.name or not isinstance(evidence_id, str) or not ID_RE.fullmatch(evidence_id):
            raise EvidenceError("evidence_id 与目录名不一致或非法")
        if record.get("schema_version") != SCHEMA_VERSION:
            raise EvidenceError("schema_version 不受支持")
        iteration = record.get("iteration")
        if not isinstance(iteration, str) or not ITERATION_RE.fullmatch(iteration):
            raise EvidenceError("iteration 非法")
        if expected_iteration is not None and iteration != expected_iteration:
            raise EvidenceError(f"iteration 应为 {expected_iteration}，实际为 {iteration}")
        ac_ids = record.get("ac_ids")
        if not isinstance(ac_ids, list) or not ac_ids or any(
            not isinstance(value, str) or not AC_RE.fullmatch(value) for value in ac_ids
        ):
            raise EvidenceError("ac_ids 非法")
        command = record.get("command")
        if not isinstance(command, dict) or not isinstance(command.get("argv"), list) or not command["argv"]:
            raise EvidenceError("command.argv 非法")
        if any(not isinstance(value, str) for value in command["argv"]):
            raise EvidenceError("command.argv 只能包含字符串")
        cwd = command.get("cwd")
        if not isinstance(cwd, str) or Path(cwd).is_absolute() or ".." in Path(cwd).parts:
            raise EvidenceError("command.cwd 非法或越界")
        timestamps: list[datetime] = []
        for timestamp_name in ("started_at", "finished_at"):
            timestamp = record.get(timestamp_name)
            if not isinstance(timestamp, str) or not timestamp.endswith("Z"):
                raise EvidenceError(f"{timestamp_name} 非法")
            timestamps.append(datetime.fromisoformat(timestamp.removesuffix("Z") + "+00:00"))
        if timestamps[1] < timestamps[0]:
            raise EvidenceError("finished_at 早于 started_at")
        duration = record.get("duration_ms")
        if type(duration) is not int or duration < 0:
            raise EvidenceError("duration_ms 非法")

        streams: dict[str, dict[str, object]] = {}
        for name in ("stdout", "stderr"):
            stream = record.get(name)
            if not isinstance(stream, dict):
                raise EvidenceError(f"{name} 元数据缺失")
            log_path = safe_log_path(item_root, stream.get("path"), f"{name}.log")
            data = log_path.read_bytes()
            if stream.get("captured_bytes") != len(data):
                raise EvidenceError(f"{name} captured_bytes 不符")
            if stream.get("sha256") != hashlib.sha256(data).hexdigest():
                raise EvidenceError(f"{name} SHA-256 不符")
            total = stream.get("bytes")
            captured = stream.get("captured_bytes")
            truncated = stream.get("truncated")
            if type(total) is not int or type(captured) is not int or not isinstance(truncated, bool):
                raise EvidenceError(f"{name} 字节/截断字段非法")
            if total < captured or truncated != (total > captured):
                raise EvidenceError(f"{name} 截断状态与字节数不一致")
            streams[name] = stream

        outcome = record.get("outcome")
        process_exit = record.get("process_exit_code")
        truncated = bool(streams["stdout"]["truncated"] or streams["stderr"]["truncated"])
        valid = (
            (outcome == "passed" and process_exit == 0 and not truncated)
            or (outcome == "failed" and type(process_exit) is int and process_exit != 0 and not truncated)
            or (outcome == "timeout" and type(process_exit) is int and process_exit != 0)
            or (outcome == "incomplete" and truncated)
            or (outcome == "launch_error" and process_exit is None and isinstance(record.get("launch_error"), str))
        )
        if not valid:
            raise EvidenceError("outcome、exit code 与截断状态不一致")
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        errors.append(str(error))
    return errors


def evidence_root(root: Path, iteration: str, source: str) -> Path:
    if source == "hot":
        return root / ".ai" / "verification-evidence"
    return root / ".ai" / "iterations" / iteration / "evidence"


def verify_tree(root: Path, iteration: str, source: str, quiet: bool = False) -> bool:
    target = evidence_root(root, iteration, source)
    if target.is_symlink() or not target.is_dir():
        if not quiet:
            print(f"[DRIFT] 证据目录不存在：{target}")
        return False
    unexpected = [path for path in target.iterdir() if path.name.startswith(".")]
    items = sorted(path for path in target.iterdir() if not path.name.startswith("."))
    ok = bool(items) and not unexpected
    if unexpected and not quiet:
        for path in unexpected:
            print(f"[DRIFT] 残留临时/claim：{path}")
    if not items and not quiet:
        print(f"[DRIFT] 证据目录为空：{target}")
    for item in items:
        errors = validate_record(item, iteration) if item.is_dir() and not item.is_symlink() else ["证据项不是普通目录"]
        if errors:
            ok = False
            if not quiet:
                for error in errors:
                    print(f"[DRIFT] {item.name}: {error}")
        elif not quiet:
            print(f"[OK] {item.name}")
    return ok


def verify_command(args: argparse.Namespace) -> int:
    root = resolve_project_root(args.project_root)
    iteration = require_iteration(args.iteration)
    return 0 if verify_tree(root, iteration, args.source) else 1


def archive_command(args: argparse.Namespace, reopen: bool = False) -> int:
    root = resolve_project_root(args.project_root)
    iteration = require_iteration(args.iteration)
    require_current(root, iteration, args.allow_closed)
    hot = evidence_root(root, iteration, "hot")
    archived = evidence_root(root, iteration, "archive")
    if (root / ".ai" / "iterations").is_symlink():
        raise EvidenceError(".ai/iterations 不得是符号链接")
    if archived.parent.is_symlink():
        raise EvidenceError(f"迭代归档目录不得是符号链接：{archived.parent}")
    source, destination = (archived, hot) if reopen else (hot, archived)
    source_name = "archive" if reopen else "hot"
    if not verify_tree(root, iteration, source_name):
        raise EvidenceError(f"{source_name} 证据校验失败，拒绝移动")
    if os.path.lexists(destination):
        raise EvidenceError(f"证据目标已存在，拒绝双真源：{destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    os.replace(source, destination)
    action = "reopened" if reopen else "archived"
    print(f"[{action}] {source} -> {destination}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    run = subparsers.add_parser("run", help="Run a command and capture evidence")
    run.add_argument("--project-root", required=True, type=Path)
    run.add_argument("--iteration", required=True)
    run.add_argument("--id", dest="evidence_id", required=True)
    run.add_argument("--ac", required=True)
    run.add_argument("--cwd", default=".")
    run.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT)
    run.add_argument("--max-output-bytes", type=int, default=DEFAULT_MAX_OUTPUT_BYTES)
    run.add_argument("--allow-closed", action="store_true", help="Allow a closed iteration when current is none")
    run.add_argument("command", nargs=argparse.REMAINDER)

    verify = subparsers.add_parser("verify", help="Verify captured evidence without writing")
    verify.add_argument("--project-root", required=True, type=Path)
    verify.add_argument("--iteration", required=True)
    verify.add_argument("--source", choices=("hot", "archive"), default="hot")

    for name in ("archive", "reopen"):
        move = subparsers.add_parser(name, help=f"{name.title()} the evidence tree")
        move.add_argument("--project-root", required=True, type=Path)
        move.add_argument("--iteration", required=True)
        move.add_argument("--allow-closed", action="store_true", help="Allow a closed iteration when current is none")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.subcommand == "run":
            return capture_run(args)
        if args.subcommand == "verify":
            return verify_command(args)
        return archive_command(args, reopen=args.subcommand == "reopen")
    except (EvidenceError, OSError, UnicodeError, json.JSONDecodeError) as error:
        print(f"verification-evidence: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
