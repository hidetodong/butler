#!/usr/bin/env bash
# ITER-0115 · AC6/AC7：三处机器断言改齐并跑绿；plugin 清单去 progress 且官方 validator 通过。
set -uo pipefail
cd "$(dirname "$0")/../../.."
fail=0
ok()  { echo "[OK]   $*"; }
bad() { echo "[FAIL] $*"; fail=1; }

echo "=== AC6 · verify-codex-workflows.sh ==="
if UV_NO_SYNC=1 uv run --locked --python 3.12.12 bash scripts/verify-codex-workflows.sh > /tmp/iter0115-codex.log 2>&1; then
  ok "退出码 0"
  tail -1 /tmp/iter0115-codex.log | sed 's/^/       /'
else
  bad "未通过："; tail -20 /tmp/iter0115-codex.log | sed 's/^/       /'
fi
if grep -qF 'Router + 12 workflow skills' /tmp/iter0115-codex.log; then ok "结尾文案报 12 个 workflow skills"; else bad "结尾文案没跟上"; fi
if grep -q 'progress' scripts/verify-codex-workflows.sh; then bad "脚本里仍有 progress"; else ok "两处 names 名单已去 progress"; fi

echo "=== AC6 · test-workflow-registry.py ==="
if grep -qF 'self.assertEqual(12, len(data["workflows"]))' scripts/test-workflow-registry.py; then
  ok "数量断言已是 12"
else
  bad "数量断言没改到 12"
fi
if UV_NO_SYNC=1 uv run --locked --python 3.12.12 python scripts/test-workflow-registry.py > /tmp/iter0115-reg.log 2>&1; then
  ok "全部用例通过"
  grep -E '^Ran |^OK' /tmp/iter0115-reg.log | sed 's/^/       /'
else
  bad "用例未全过："; tail -20 /tmp/iter0115-reg.log | sed 's/^/       /'
fi

echo "=== AC6 · project-config 消费者契约 ==="
if UV_NO_SYNC=1 uv run --locked --python 3.12.12 python -m pytest tools/project-config/tests -q > /tmp/iter0115-pc.log 2>&1; then
  ok "pytest 全绿"
  tail -1 /tmp/iter0115-pc.log | sed 's/^/       /'
else
  bad "pytest 未通过："; tail -20 /tmp/iter0115-pc.log | sed 's/^/       /'
fi
n=$(grep -c 'progress' tools/project-config/tests/test_consumers.py | tr -d ' ')
if [ "$n" = 0 ]; then ok "test_consumers.py 零 progress 路径"; else bad "仍有 ${n} 处 progress"; fi
if grep -q 'test_progress_version_does_not_come_from_project_config' tools/project-config/tests/test_consumers.py; then
  bad "progress 专属测试方法还在"
else
  ok "progress 专属测试方法已删除"
fi
for keep in dangerous preference review; do
  if grep -q "butler-${keep}" tools/project-config/tests/test_consumers.py; then
    ok "仍覆盖 ${keep} 消费者（没有误删同元组的邻居）"
  else
    bad "${keep} 消费者被误删"
  fi
done

echo "=== AC7 · plugin 清单 ==="
python3 - <<'PY'
import json, sys
data = json.load(open("plugins/butler/.codex-plugin/plugin.json", encoding="utf-8"))
desc = data["interface"]["longDescription"]
bad = 0
if "progress" in desc:
    print("[FAIL] longDescription 仍含 progress"); bad = 1
else:
    print("[OK]   longDescription 已去 progress")
for field, expected in (("name", "butler"), ("skills", "./skills/")):
    if data.get(field) != expected:
        print(f"[FAIL] {field} 被误改为 {data.get(field)}"); bad = 1
    else:
        print(f"[OK]   {field} 未动（{expected}）")
sys.exit(bad)
PY
[ $? = 0 ] || fail=1
if UV_NO_SYNC=1 uv run --locked --python 3.12.12 python tools/codex-validators/test_vendored_validators.py > /tmp/iter0115-val.log 2>&1; then
  ok "固定版 plugin/skill validator 全部通过（含实体数量断言 13）"
else
  bad "validator 未通过："; tail -20 /tmp/iter0115-val.log | sed 's/^/       /'
fi

echo
[ "$fail" = 0 ] && echo "ASSERTIONS-CLEAN" || echo "ASSERTIONS-DIRTY"
exit "$fail"
