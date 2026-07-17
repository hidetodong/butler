#!/bin/sh

# Advisory is deliberately fail-open: a missing/invalid Butler checkout must
# never turn a PostToolUse reminder into a write failure.
if [ -z "${BUTLER_PATH:-}" ] || [ ! -f "$BUTLER_PATH/templates/hooks/butler_advisor.py" ]; then
  cat >/dev/null
  exit 0
fi

python3 "$BUTLER_PATH/templates/hooks/butler_advisor.py" || exit 0
