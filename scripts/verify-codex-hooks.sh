#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
HOOKS_JSON="$ROOT/plugins/butler/hooks/hooks.json"
MANIFEST="$ROOT/plugins/butler/.codex-plugin/plugin.json"
GATE="$ROOT/plugins/butler/hooks/butler-gate.sh"
ADVISOR="$ROOT/plugins/butler/hooks/butler-advisor.sh"
WORK=$(mktemp -d "${TMPDIR:-/tmp}/butler-codex-hooks.XXXXXX")
trap 'rm -rf "$WORK"' EXIT HUP INT TERM

python3 -m json.tool "$HOOKS_JSON" >/dev/null
python3 - "$HOOKS_JSON" "$MANIFEST" <<'PY'
import json
import sys

hooks = json.load(open(sys.argv[1], encoding="utf-8"))["hooks"]
assert hooks["PreToolUse"][0]["matcher"] == "apply_patch|Edit|Write|MultiEdit"
assert hooks["PostToolUse"][0]["matcher"] == "apply_patch|Edit|Write|MultiEdit"
manifest = json.load(open(sys.argv[2], encoding="utf-8"))
assert "hooks" not in manifest
PY
[ -x "$GATE" ]
[ -x "$ADVISOR" ]

mkdir -p "$WORK/.ai" "$WORK/src"
git init -q "$WORK"
printf '%s\n' concept > "$WORK/.ai/CONCEPT.md"
printf '%s\n' '---' '方案状态: draft' '---' '# Plan Admission' '- Verdict: revise' > "$WORK/.ai/TECH_PLAN.md"
printf '%s\n' '---' '状态: ack-frozen' '---' > "$WORK/.ai/AC_LIST.md"

payload() {
  python3 -c 'import json,sys; print(json.dumps({"tool_name":"apply_patch","cwd":sys.argv[1],"tool_input":{"command":sys.argv[2]}}))' "$WORK" "$1"
}

ALLOW='*** Begin Patch
*** Add File: src/allowed.py
+allowed = True
*** End Patch'
DENY='*** Begin Patch
*** Add File: 99_Business_Extension/blocked.md
+blocked
*** End Patch'
MILESTONE='*** Begin Patch
*** Update File: .ai/MILESTONE.md
+brief
*** End Patch'

# Codex apply_patch 真链路必须拒绝未通过方案；重审置 pass 后才放行。
set +e
PLAN_ERR=$(payload "$ALLOW" | BUTLER_PATH="$ROOT" "$GATE" 2>&1)
PLAN_RC=$?
set -e
[ "$PLAN_RC" -eq 2 ]
printf '%s' "$PLAN_ERR" | grep -q 'P3 方案未通过'
printf '%s\n' '---' '方案状态: pass' '---' '# Plan Admission' '- Verdict: pass' > "$WORK/.ai/TECH_PLAN.md"
payload "$ALLOW" | BUTLER_PATH="$ROOT" "$GATE"

# 会话从多仓父目录启动时，绝对 target 按实际 Git 项目根校验；
# 父目录自身无法证明是项目根时 Butler 退出判定，由宿主权限接管。
SESSION_ROOT=$(dirname "$WORK")
ABSOLUTE_ALLOW="*** Begin Patch
*** Add File: $WORK/src/absolute-allowed.py
+allowed = True
*** End Patch"
python3 -c 'import json,sys; print(json.dumps({"tool_name":"apply_patch","cwd":sys.argv[1],"tool_input":{"command":sys.argv[2]}}))' \
  "$SESSION_ROOT" "$ABSOLUTE_ALLOW" | BUTLER_PATH="$ROOT" "$GATE"

RELATIVE_PARENT='*** Begin Patch
*** Add File: .ai/ITERATIONS.md
+wrong root
*** End Patch'
python3 -c 'import json,sys; print(json.dumps({"tool_name":"apply_patch","cwd":sys.argv[1],"tool_input":{"command":sys.argv[2]}}))' \
  "$SESSION_ROOT" "$RELATIVE_PARENT" | BUTLER_PATH="$ROOT" "$GATE"
[ ! -e "$SESSION_ROOT/.ai/ITERATIONS.md" ]

set +e
DENY_ERR=$(payload "$DENY" | BUTLER_PATH="$ROOT" "$GATE" 2>&1)
DENY_RC=$?
set -e
[ "$DENY_RC" -eq 2 ]
printf '%s' "$DENY_ERR" | grep -q 'protected_paths'
[ ! -e "$WORK/99_Business_Extension/blocked.md" ]

ADVISORY=$(payload "$MILESTONE" | BUTLER_PATH="$ROOT" "$ADVISOR")
printf '%s' "$ADVISORY" | python3 -c 'import json,sys; value=json.load(sys.stdin); assert "references/prd" in value["hookSpecificOutput"]["additionalContext"]'

set +e
payload "$ALLOW" | env -u BUTLER_PATH "$GATE" >/dev/null 2>&1
MISSING_GATE_RC=$?
set -e
[ "$MISSING_GATE_RC" -eq 2 ]
MISSING_ADVISOR=$(payload "$MILESTONE" | env -u BUTLER_PATH "$ADVISOR")
[ -z "$MISSING_ADVISOR" ]

echo "Codex hook wrapper verification passed"
