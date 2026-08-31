#!/usr/bin/env bash
# AC6 / AC7：活接线改指新契约、旧链逐字节未动、测试只改活接线那两个用例
set -uo pipefail
cd "$(dirname "$0")/../../.." || exit 1
fail=0
ok(){ echo "[OK] $1"; }; bad(){ echo "[FAIL] $1"; fail=1; }

python3 scripts/sync-workflow-registry.py --check && ok "注册表投影 --check 退出码 0" || bad "注册表投影 --check 退出码 0"

python3 - <<'PY'
import json, sys
d = json.load(open("workflows/registry.json", encoding="utf-8"))
e = [w for w in d["workflows"] if w["id"] == "inbox"][0]
assert e["rule_source"] == "Coder/40_Context_Management/intake-workflow.md", e["rule_source"]
assert len(d["workflows"]) == 12, len(d["workflows"])
print("[OK] rule_source 指向新动作层，业务工作流仍 12 个")
PY
[ $? -eq 0 ] || fail=1

OLDDIR="ori""gin/"
OLDRULE="inbox""-workflow.md"
for f in .claude/commands/butler/inbox.md plugins/butler/skills/butler-inbox/SKILL.md; do
  n=$(grep -cF "$OLDDIR" "$f" || true); [ "$n" = "0" ] && ok "$f 无旧来源目录字样" || bad "$f 无旧来源目录字样（$n）"
  n=$(grep -cF "$OLDRULE" "$f" || true); [ "$n" = "0" ] && ok "$f 无旧动作层字样" || bad "$f 无旧动作层字样（$n）"
  grep -qF "tools/intake/" "$f" && ok "$f 调新工具" || bad "$f 调新工具"
  grep -qF "intake-schema.md" "$f" && ok "$f 读新契约" || bad "$f 读新契约"
done

# 旧链逐字节未动
while read -r digest path; do
  case "$path" in
    Coder/40_Context_Management/inbox-schema.md|Coder/40_Context_Management/inbox-workflow.md|templates/hooks/tests/test_inbox_contract.py|tools/inbox/*) ;;
    *) continue ;;
  esac
  now=$(shasum -a 256 "$path" | awk '{print $1}')
  [ "$now" = "$digest" ] && ok "旧链未动：$path" || bad "旧链被改：$path"
done < <(grep -v '^#' .ai/iterations/ITER-0118/pre-p4.baseline | grep -v '^$')

# 测试只改活接线那两个用例
changed=$(git diff -U0 -- templates/hooks/tests/test_inbox_workflow.py | grep -c '^[+-][^+-]' || true)
grep -qF 'intake-workflow.md' templates/hooks/tests/test_inbox_workflow.py && ok "注册断言改指新动作层" || bad "注册断言改指新动作层"
grep -qF 'tools/intake/' templates/hooks/tests/test_inbox_workflow.py && ok "薄壳断言改指新工具" || bad "薄壳断言改指新工具"
grep -qF 'inbox-workflow.md' templates/hooks/tests/test_inbox_workflow.py && ok "旧规则用例原样保留（仍断言旧文件）" || bad "旧规则用例原样保留"
echo "  该测试文件对 HEAD 的净改动行数：$changed"
exit $fail
