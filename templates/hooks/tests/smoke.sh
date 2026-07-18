#!/usr/bin/env bash
# Tier 3 end-to-end smoke test for butler_gate.py.
# Not part of pytest — runs hook as a real subprocess with crafted stdin.
# Expected to be run manually after changing hook code.
set -euo pipefail

HOOKS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GATE="${HOOKS_DIR}/butler_gate.py"

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

echo "[smoke] tmp project: $TMP"

mkdir -p "$TMP/.ai"
cd "$TMP"

# --- Case 1: missing artifacts + gated path → expect exit 2 ---
echo "[smoke] case 1: gated path, no artifacts"
set +e
OUTPUT=$(echo '{"tool_name":"Edit","tool_input":{"file_path":"src/x.ts"},"cwd":"'"$TMP"'"}' \
  | python3 "$GATE" 2>&1)
RC=$?
set -e
if [[ $RC -ne 2 ]]; then
  echo "[smoke] FAIL: expected exit 2, got $RC"
  echo "$OUTPUT"
  exit 1
fi
if ! grep -q "phase_gate" <<<"$OUTPUT"; then
  echo "[smoke] FAIL: stderr did not mention phase_gate"
  echo "$OUTPUT"
  exit 1
fi
echo "[smoke] case 1 OK"

# --- Case 2: artifacts present + gated path → expect exit 0 ---
echo "[smoke] case 2: gated path, artifacts present"
printf "# CONCEPT\nstub\n" > .ai/CONCEPT.md
printf '%s\n' '---' '状态: ack-frozen' '---' '# AC_LIST' 'stub' > .ai/AC_LIST.md
printf '%s\n' '---' '方案状态: pass' '---' '# TECH_PLAN' 'stub' > .ai/TECH_PLAN.md
set +e
echo '{"tool_name":"Edit","tool_input":{"file_path":"src/x.ts"},"cwd":"'"$TMP"'"}' \
  | python3 "$GATE"
RC=$?
set -e
if [[ $RC -ne 0 ]]; then
  echo "[smoke] FAIL: expected exit 0, got $RC"
  exit 1
fi
echo "[smoke] case 2 OK"

# --- Case 3: bypass with reason → expect exit 0 + RUN_LOG entry ---
echo "[smoke] case 3: bypass with reason for protected path"
printf "hotfix reason\n" > .ai/bypass-reason.md
set +e
echo '{"tool_name":"Edit","tool_input":{"file_path":"99_Business_Extension/x.md"},"cwd":"'"$TMP"'"}' \
  | env BUTLER_BYPASS=1 python3 "$GATE"
RC=$?
set -e
if [[ $RC -ne 0 ]]; then
  echo "[smoke] FAIL: expected exit 0 under bypass, got $RC"
  exit 1
fi
if ! grep -q "protected_paths" .ai/RUN_LOG.md; then
  echo "[smoke] FAIL: RUN_LOG.md missing protected_paths entry"
  cat .ai/RUN_LOG.md
  exit 1
fi
echo "[smoke] case 3 OK"

echo "[smoke] ALL PASS"
