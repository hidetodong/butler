#!/usr/bin/env bash
# AC2 / AC3 / AC4：add 的键与追加、list 的只读与筛选、handle 只认穷举的四条转移
set -uo pipefail
cd "$(dirname "$0")/../../.." || exit 1
fail=0
ok(){ echo "[OK] $1"; }; bad(){ echo "[FAIL] $1"; fail=1; }

for cls in TestAdd TestList TestTransitions; do
  python3 -m unittest "tools.intake.tests.test_intake.$cls" >/dev/null 2>&1 \
    && ok "$cls 全通过" || bad "$cls 全通过"
done

# AC3 的只读性另外用真实哈希再证一遍
TMP=$(mktemp -d); mkdir -p "$TMP/.ai/milestone-backlog"
printf '# 里程碑台账\n\ncurrent: none\n\n| 里程碑号 | 标题 | 状态 | 开启 | 收口 | 含迭代 | 交付 |\n|---|---|---|---|---|---|---|\n\n## 待办区（未编号）\n\n| 候办键 | 标题 | 暂缓日期 | 草稿 | 暂缓原因 |\n|---|---|---|---|---|\n' > "$TMP/.ai/MILESTONES.md"
python3 tools/intake/intake.py add --project-root "$TMP" --text "readonly probe" --date 2026-08-20 >/dev/null
b=$(shasum -a 256 "$TMP/.ai/INBOX.md" | awk '{print $1}')
bd=$(find "$TMP/.ai/milestone-backlog" -type f | wc -l | tr -d ' ')
python3 tools/intake/intake.py list --project-root "$TMP" >/dev/null
python3 tools/intake/intake.py list --project-root "$TMP" --layer inbox --state new >/dev/null
a=$(shasum -a 256 "$TMP/.ai/INBOX.md" | awk '{print $1}')
ad=$(find "$TMP/.ai/milestone-backlog" -type f | wc -l | tr -d ' ')
[ "$b" = "$a" ] && ok "list 跑完 INBOX.md 哈希不变" || bad "list 跑完 INBOX.md 哈希不变"
[ "$bd" = "$ad" ] && ok "list 跑完孵化区文件数不变" || bad "list 跑完孵化区文件数不变"
rm -rf "$TMP"

# AC4 的穷举来源：合法转移必须恰是契约里那四条
python3 - <<'PY'
import re, sys, pathlib
sys.path.insert(0, ".")
from tools.intake import intake
text = pathlib.Path("Coder/40_Context_Management/intake-schema.md").read_text(encoding="utf-8")
declared = set(re.findall(r"^\| `(\w+) → (\w+)` \|", text, re.M))
if declared != intake.TRANSITIONS:
    print(f"[FAIL] 工具的合法转移集合与契约不一致：契约={declared} 工具={intake.TRANSITIONS}")
    sys.exit(1)
print(f"[OK] 工具的合法转移集合恰是契约穷举的 {len(declared)} 条")
PY
[ $? -eq 0 ] || fail=1
exit $fail
