#!/usr/bin/env bash
set -euo pipefail
export LC_ALL=C
export LANG=C

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
EXPECTED_UV="0.9.28"
EXPECTED_PYTHON="3.12.12"

command -v uv >/dev/null 2>&1 || {
  echo "[FAIL] uv $EXPECTED_UV is required" >&2
  exit 2
}
actual_uv="$(uv --version | awk '{print $2}')"
[[ "$actual_uv" == "$EXPECTED_UV" ]] || {
  echo "[FAIL] expected uv $EXPECTED_UV, got $actual_uv" >&2
  exit 2
}

cd "$ROOT"
uv sync --locked --python "$EXPECTED_PYTHON"
actual_python="$(UV_NO_SYNC=1 uv run --locked --python "$EXPECTED_PYTHON" python -c 'import platform; print(platform.python_version())')"
[[ "$actual_python" == "$EXPECTED_PYTHON" ]] || {
  echo "[FAIL] expected Python $EXPECTED_PYTHON, got $actual_python" >&2
  exit 2
}
echo "[INFO] pinned toolchain: platform=$(uname -s)/$(uname -m) python=$actual_python uv=$actual_uv"
UV_NO_SYNC=1 uv run --locked --python "$EXPECTED_PYTHON" bash "$ROOT/scripts/verify-dual-host.sh"
bash "$ROOT/scripts/verify-pi-extension.sh"
UV_NO_SYNC=1 uv run --locked --python "$EXPECTED_PYTHON" python "$ROOT/scripts/test-goal-contract.py"
UV_NO_SYNC=1 uv run --locked --python "$EXPECTED_PYTHON" python "$ROOT/scripts/test-plan-admission.py"
UV_NO_SYNC=1 uv run --locked --python "$EXPECTED_PYTHON" python "$ROOT/scripts/test-goal-calibration.py"
UV_NO_SYNC=1 uv run --locked --python "$EXPECTED_PYTHON" python "$ROOT/tools/goal-assurance/test_goal.py"
UV_NO_SYNC=1 uv run --locked --python "$EXPECTED_PYTHON" python -m unittest tools.handoff.tests.test_handoff
UV_NO_SYNC=1 uv run --locked --python "$EXPECTED_PYTHON" python -m unittest discover -s tools/state-ledger/tests
UV_NO_SYNC=1 uv run --locked --python "$EXPECTED_PYTHON" python -m unittest discover -s tools/artifact-pipeline/tests
UV_NO_SYNC=1 uv run --locked --python "$EXPECTED_PYTHON" python tools/artifact-pipeline/contract.py check project --project-root .
UV_NO_SYNC=1 uv run --locked --python "$EXPECTED_PYTHON" python -m pytest tools/project-config/tests -q
UV_NO_SYNC=1 uv run --locked --python "$EXPECTED_PYTHON" python "$ROOT/scripts/test-butler-upgrade.py"
UV_NO_SYNC=1 uv run --locked --python "$EXPECTED_PYTHON" python "$ROOT/scripts/test-goal-host-wiring.py"
UV_NO_SYNC=1 uv run --locked --python "$EXPECTED_PYTHON" python -m unittest tools.inbox.tests.test_inbox
UV_NO_SYNC=1 uv run --locked --python "$EXPECTED_PYTHON" python -m unittest discover -s tools/prd-migrate/tests
UV_NO_SYNC=1 uv run --locked --python "$EXPECTED_PYTHON" python -m unittest discover -s tools/prd-status/tests
UV_NO_SYNC=1 uv run --locked --python "$EXPECTED_PYTHON" python -m unittest discover -s tools/prd-update/tests
UV_NO_SYNC=1 uv run --locked --python "$EXPECTED_PYTHON" python -m unittest discover -s tools/workspace-scope/tests
UV_NO_SYNC=1 uv run --locked --python "$EXPECTED_PYTHON" python -m unittest discover -s tools/mile0009-e2e/tests
