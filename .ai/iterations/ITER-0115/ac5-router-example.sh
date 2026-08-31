#!/usr/bin/env bash
# ITER-0115 · AC5：路由样例改写为 not-butler，样例集仍覆盖全部 12 个工作流。
set -uo pipefail
cd "$(dirname "$0")/../../.."
fail=0
python3 - <<'PY'
import json, sys
bad = 0
def ok(m): print(f"[OK]   {m}")
def no(m):
    global bad
    print(f"[FAIL] {m}"); bad = 1

fixture = json.load(open("workflows/router-examples.json", encoding="utf-8"))
examples = fixture["examples"]
hits = [e for e in examples if e["request"] == "现在项目进度怎么样"]
if len(hits) != 1:
    no(f"那条请求出现 {len(hits)} 次，期望 1 次")
else:
    e = hits[0]
    ok(f"请求文字保留：{e['request']}")
    ok("expected_status = not-butler") if e["expected_status"] == "not-butler" else no(f"expected_status = {e['expected_status']}")
    ok("expected_primary = null") if e["expected_primary"] is None else no(f"expected_primary = {e['expected_primary']}")
    ok("expected_state_writes = false") if e["expected_state_writes"] is False else no("expected_state_writes 非 false")

raw = open("workflows/router-examples.json", encoding="utf-8").read()
ok("样例文件全文零 progress 字样") if "progress" not in raw else no("样例文件仍含 progress")

registry = json.load(open("workflows/registry.json", encoding="utf-8"))
ids = {w["id"] for w in registry["workflows"]}
covered = {e["expected_primary"] for e in examples if e["expected_primary"]}
if ids == covered:
    ok(f"样例集覆盖全部 {len(ids)} 个工作流 ID，无缺无余")
else:
    no(f"覆盖对不上：缺={sorted(ids-covered)} 余={sorted(covered-ids)}")
sys.exit(bad)
PY
[ $? = 0 ] || fail=1
echo
[ "$fail" = 0 ] && echo "ROUTER-EXAMPLE-CLEAN" || echo "ROUTER-EXAMPLE-DIRTY"
exit "$fail"
