#!/usr/bin/env python3
"""Mechanical contract tests for Butler's required GitHub Actions workflow."""

from __future__ import annotations

import copy
import os
import re
import shutil
import subprocess
import tempfile
import tomllib
import unittest
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "ci.yml"
CHECKOUT = "actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd"
SETUP_UV = "astral-sh/setup-uv@08807647e7069bb48b6ef5acd8ec9567f424441b"
SHA_ACTION_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+@[0-9a-f]{40}$")


def load_workflow(path: Path = WORKFLOW) -> dict[str, Any]:
    payload = yaml.load(path.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
    if not isinstance(payload, dict):
        raise AssertionError("workflow root must be a mapping")
    return payload


def walk(value: Any):
    yield value
    if isinstance(value, dict):
        for item in value.values():
            yield from walk(item)
    elif isinstance(value, list):
        for item in value:
            yield from walk(item)


def validate_contract(workflow: dict[str, Any]) -> None:
    if workflow.get("name") != "Butler CI":
        raise AssertionError("workflow name must remain `Butler CI`")
    triggers = workflow.get("on")
    if not isinstance(triggers, dict) or set(triggers) != {"pull_request", "push"}:
        raise AssertionError("workflow must trigger only on pull_request and push")
    push = triggers.get("push")
    if not isinstance(push, dict) or push.get("branches") != ["main"] or push.get("tags") != ["v*"]:
        raise AssertionError("push must cover main and v* release tags")
    if workflow.get("permissions") != {"contents": "read"}:
        raise AssertionError("workflow permissions must be contents: read only")
    concurrency = workflow.get("concurrency")
    if not isinstance(concurrency, dict) or concurrency.get("cancel-in-progress") != "true":
        raise AssertionError("concurrency cancellation must be enabled")

    for node in walk(workflow):
        if isinstance(node, dict) and "continue-on-error" in node:
            raise AssertionError("continue-on-error is forbidden")
        if isinstance(node, dict) and "uses" in node:
            action = node["uses"]
            if not isinstance(action, str) or SHA_ACTION_RE.fullmatch(action) is None:
                raise AssertionError(f"action is not pinned to a full SHA: {action}")

    jobs = workflow.get("jobs")
    if not isinstance(jobs, dict) or set(jobs) != {"verify", "required"}:
        raise AssertionError("workflow must contain verify and required jobs")
    verify = jobs["verify"]
    matrix = verify.get("strategy", {}).get("matrix", {}).get("os")
    if matrix != ["ubuntu-24.04", "macos-14"]:
        raise AssertionError("verify matrix must require ubuntu-24.04 and macos-14")
    if verify.get("runs-on") != "${{ matrix.os }}" or verify.get("timeout-minutes") != "30":
        raise AssertionError("verify runner/timeout contract drifted")
    if verify.get("strategy", {}).get("fail-fast") != "false":
        raise AssertionError("matrix must retain both platform results")
    steps = verify.get("steps")
    if not isinstance(steps, list):
        raise AssertionError("verify steps missing")
    actions = [step.get("uses") for step in steps if isinstance(step, dict) and "uses" in step]
    if actions != [CHECKOUT, SETUP_UV]:
        raise AssertionError("verify actions or order drifted")
    run_steps = [step.get("run") for step in steps if isinstance(step, dict) and "run" in step]
    if run_steps != ["bash scripts/verify-ci.sh"]:
        raise AssertionError("workflow must call only the repository verification entrypoint")
    setup = steps[1].get("with", {})
    if setup.get("version") != "0.9.28" or setup.get("python-version") != "3.12.12":
        raise AssertionError("uv/Python versions must remain exact")
    checkout = steps[0].get("with", {})
    if checkout.get("persist-credentials") != "false":
        raise AssertionError("checkout credentials must not persist")

    required = jobs["required"]
    if required.get("name") != "Butler required checks":
        raise AssertionError("stable required check name drifted")
    if required.get("needs") != "verify" or required.get("if") != "always()":
        raise AssertionError("required job must always aggregate verify")
    required_steps = required.get("steps")
    if not isinstance(required_steps, list) or len(required_steps) != 1:
        raise AssertionError("required job must have one aggregation step")
    aggregate = required_steps[0]
    if aggregate.get("env", {}).get("VERIFY_RESULT") != "${{ needs.verify.result }}":
        raise AssertionError("required job must consume the verify result")
    if aggregate.get("run") != 'test "$VERIFY_RESULT" = "success"':
        raise AssertionError("required job must fail unless every matrix leg succeeds")


def validate_toolchain() -> None:
    python_version = (ROOT / ".python-version").read_text(encoding="utf-8").strip()
    if python_version != "3.12.12":
        raise AssertionError(".python-version must remain exact")
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    metadata = project.get("project", {})
    if metadata.get("requires-python") != "==3.12.12":
        raise AssertionError("pyproject Python requirement drifted")
    if metadata.get("dependencies") != ["pytest==8.4.2", "pyyaml==6.0.3"]:
        raise AssertionError("direct verification dependencies drifted")
    lock = tomllib.loads((ROOT / "uv.lock").read_text(encoding="utf-8"))
    if lock.get("requires-python") != "==3.12.12":
        raise AssertionError("uv.lock Python requirement drifted")
    versions = {
        package.get("name"): package.get("version")
        for package in lock.get("package", [])
        if isinstance(package, dict)
    }
    if versions.get("pytest") != "8.4.2" or versions.get("pyyaml") != "6.0.3":
        raise AssertionError("uv.lock direct dependency versions drifted")
    entrypoint = (ROOT / "scripts" / "verify-ci.sh").read_text(encoding="utf-8")
    for required in ('EXPECTED_UV="0.9.28"', 'EXPECTED_PYTHON="3.12.12"', "uv sync --locked", "uv run --locked"):
        if required not in entrypoint:
            raise AssertionError(f"verification entrypoint missing: {required}")
    matrix = (ROOT / "scripts" / "verify-dual-host.sh").read_text(encoding="utf-8")
    if "uv run --with" in matrix:
        raise AssertionError("verification matrix must not resolve transient dependencies")


class CIContractTests(unittest.TestCase):
    def test_repository_workflow(self) -> None:
        validate_contract(load_workflow())
        validate_toolchain()

    def test_floating_action_is_rejected(self) -> None:
        workflow = load_workflow()
        workflow["jobs"]["verify"]["steps"][0]["uses"] = "actions/checkout@v6"
        with self.assertRaisesRegex(AssertionError, "full SHA"):
            validate_contract(workflow)

    def test_single_os_or_continue_on_error_is_rejected(self) -> None:
        workflow = load_workflow()
        workflow["jobs"]["verify"]["strategy"]["matrix"]["os"] = ["ubuntu-24.04"]
        with self.assertRaisesRegex(AssertionError, "matrix"):
            validate_contract(workflow)
        workflow = load_workflow()
        workflow["jobs"]["verify"]["continue-on-error"] = "true"
        with self.assertRaisesRegex(AssertionError, "forbidden"):
            validate_contract(workflow)

    def test_wrong_uv_version_fails_before_sync(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            fake = Path(temp) / "uv"
            fake.write_text("#!/bin/sh\necho 'uv 9.9.9'\n", encoding="utf-8")
            fake.chmod(0o755)
            env = os.environ.copy()
            env["PATH"] = f"{temp}:/usr/bin:/bin"
            result = subprocess.run(
                ["/bin/bash", str(ROOT / "scripts" / "verify-ci.sh")],
                cwd=ROOT,
                env=env,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("expected uv 0.9.28, got 9.9.9", result.stderr)

    def test_stale_lock_is_rejected(self) -> None:
        uv = shutil.which("uv")
        self.assertIsNotNone(uv, "pinned uv must be on PATH")
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            shutil.copy2(ROOT / "pyproject.toml", project / "pyproject.toml")
            shutil.copy2(ROOT / "uv.lock", project / "uv.lock")
            pyproject = project / "pyproject.toml"
            pyproject.write_text(
                pyproject.read_text(encoding="utf-8").replace("pytest==8.4.2", "pytest==8.4.1"),
                encoding="utf-8",
            )
            result = subprocess.run(
                [uv, "lock", "--check", "--offline", "--project", str(project)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
