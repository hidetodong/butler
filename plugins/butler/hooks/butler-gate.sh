#!/bin/sh
set -eu

if [ -z "${BUTLER_PATH:-}" ] || [ ! -f "$BUTLER_PATH/templates/hooks/butler_gate.py" ]; then
  cat >/dev/null
  echo "❌ butler-gate unavailable: set BUTLER_PATH to a Butler checkout" >&2
  exit 2
fi

exec python3 "$BUTLER_PATH/templates/hooks/butler_gate.py"
