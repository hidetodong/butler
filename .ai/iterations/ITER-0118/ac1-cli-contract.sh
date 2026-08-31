#!/usr/bin/env bash
# AC1：工具存在、自带测试、三个子命令都收 --project-root 且输出 JSON、校验不过整次不落盘
set -uo pipefail
cd "$(dirname "$0")/../../.." || exit 1
fail=0
ok(){ echo "[OK] $1"; }; bad(){ echo "[FAIL] $1"; fail=1; }

[ -f tools/intake/intake.py ] && ok "工具入口存在" || bad "工具入口存在"
[ -d tools/intake/tests ] && ok "自带测试目录" || bad "自带测试目录"

TMP=$(mktemp -d); mkdir -p "$TMP/.ai/milestone-backlog"
for c in add list handle; do
  python3 tools/intake/intake.py "$c" --help 2>&1 | grep -q -- "--project-root" \
    && ok "$c 收 --project-root" || bad "$c 收 --project-root"
done

out=$(python3 tools/intake/intake.py add --project-root "$TMP" --text "json probe" --date 2026-08-20)
echo "$out" | python3 -c "import json,sys; d=json.load(sys.stdin); assert d['key']=='2026-08-20-json-probe'" \
  && ok "add 输出可解析 JSON" || bad "add 输出可解析 JSON"
python3 tools/intake/intake.py list --project-root "$TMP" --layer inbox | python3 -c "import json,sys; json.load(sys.stdin)" \
  && ok "list 输出可解析 JSON" || bad "list 输出可解析 JSON"

before=$(shasum -a 256 "$TMP/.ai/INBOX.md" | awk '{print $1}')
python3 tools/intake/intake.py handle --project-root "$TMP" --inbox 2026-08-20-nope --to done --note x >/dev/null 2>&1
rc=$?
after=$(shasum -a 256 "$TMP/.ai/INBOX.md" | awk '{print $1}')
[ "$rc" -ne 0 ] && ok "校验不过时退出码非零（${rc}）" || bad "校验不过时退出码非零"
[ "$before" = "$after" ] && ok "校验不过时整次不落盘" || bad "校验不过时整次不落盘"
rm -rf "$TMP"

python3 -m unittest tools.intake.tests.test_intake.TestCli -v 2>&1 | tail -3
python3 -m unittest tools.intake.tests.test_intake.TestCli >/dev/null 2>&1 \
  && ok "端到端 CLI 用例通过" || bad "端到端 CLI 用例通过"
exit $fail
