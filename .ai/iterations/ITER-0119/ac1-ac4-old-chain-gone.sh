#!/usr/bin/env bash
# AC1/AC2/AC3/AC4 —— 旧链四类实体确实没了，且删除没有波及 hook 树。
set -euo pipefail
cd "$(dirname "$0")/../../.."

echo "== AC1 · 两份旧规则真源已删，Coder/README.md 已注销 =="
for f in Coder/40_Context_Management/inbox-schema.md Coder/40_Context_Management/inbox-workflow.md; do
  test ! -e "$f" && echo "  已删除: $f"
done
echo -n "  Coder/README.md 里 inbox-schema / inbox-workflow 命中数: "
grep -c -e "inbox-schema" -e "inbox-workflow" Coder/README.md || true

echo "== AC2 · tools/inbox/ 整目录已删，CI 里那行调用已摘 =="
test ! -e tools/inbox && echo "  已删除: tools/inbox/"
echo -n "  scripts/verify-ci.sh 里 inbox 命中数: "
grep -c "inbox" scripts/verify-ci.sh || true

echo "== AC3 · 合同测试已删，剩余用例只剩两个活接线，hook 树摘要未变 =="
test ! -e templates/hooks/tests/test_inbox_contract.py && echo "  已删除: test_inbox_contract.py"
grep -E "^def test_" templates/hooks/tests/test_inbox_workflow.py
python3 - <<'PY'
import hashlib, pathlib
root = pathlib.Path("templates/hooks")
skip_dirs = {"tests", "__pycache__", ".pytest_cache"}
non_deployed = {"conftest.py", "pytest.ini"}
files = {}
for p in sorted(root.rglob("*")):
    rel = p.relative_to(root)
    if not p.is_file() or p.is_symlink():
        continue
    if set(rel.parts) & skip_dirs or rel.suffix == ".pyc":
        continue
    if rel.as_posix() in non_deployed:
        continue
    files[rel] = p.read_bytes()
d = hashlib.sha256()
for rel, content in sorted(files.items(), key=lambda kv: kv[0].as_posix()):
    d.update(rel.as_posix().encode()); d.update(b"\0"); d.update(hashlib.sha256(content).digest())
print(f"  hook 树: {len(files)} 份文件, 摘要 = {d.hexdigest()}")
print("  开工前基线      = bd92a614f9582451ec3150d2c1113a2262bb874b97fd085adf6ad0ce7c91e56d")
assert d.hexdigest() == "bd92a614f9582451ec3150d2c1113a2262bb874b97fd085adf6ad0ce7c91e56d", "hook 树摘要变了"
print("  ✓ 逐字节相同")
PY

echo "-- AC3 补证：两个存活用例逐字节未动 --"
python3 - <<'PY2'
import hashlib, pathlib, difflib
# 把 P4 开工前的文件按「已知改了什么」原样重建，SHA 对上 pre-p4.baseline 就说明
# 这份文件在本轮只发生了两处改动：文档字符串重写 + 删掉那一个退役用例。
cur = pathlib.Path("templates/hooks/tests/test_inbox_workflow.py").read_text(encoding="utf-8")
old_doc = '''"""inbox 工作流的双宿主接线测试。

本文件里的用例分两半：
- `test_inbox_workflow_route_and_safety_contract` 描述的是旧规则文件 `inbox-workflow.md`
  本身的内容，随 MILE-0016 R8 与那份文件一起退役，本轮**原样不动**。
- 另外两个用例描述的是当前活着的接线（注册表条目、两份薄壳），R7 起改指
  `intake-schema.md` / `intake-workflow.md` / `tools/intake/`。
"""
'''
removed = '''def test_inbox_workflow_route_and_safety_contract() -> None:
    text = (ROOT / "Coder/40_Context_Management/inbox-workflow.md").read_text(encoding="utf-8")
    required = (
        "new-requirement", "existing-requirement-version", "supplemental-material",
        "fuzzy-idea", "milestone-direction", "record-only", "duplicate-candidate", "ambiguous",
        "awaiting-confirmation", "dangerous", ".ai/RUN_LOG.md", "processed_sha256",
        "活工作区保护", "一个冲突或失败项不能阻塞无依赖 sibling",
    )
    for token in required:
        assert token in text


'''
new_doc = cur[: cur.index('"""\n') + 4]
anchor = "def test_inbox_is_registered_for_both_hosts"
rebuilt = cur.replace(new_doc, old_doc, 1).replace(anchor, removed + anchor, 1)
sha = hashlib.sha256(rebuilt.encode("utf-8")).hexdigest()
baseline = "686251801c2cee840c777d9e5119f281a2c55a3aea53a6af52bd11b446ad37d6"
print(f"  重建 P4 前文件 SHA = {sha}")
print(f"  pre-p4.baseline    = {baseline}")
assert sha == baseline, "重建对不上基线，说明还有别的改动没交代"
before = rebuilt[rebuilt.index(anchor):]
after = cur[cur.index(anchor):]
assert before == after, "".join(difflib.unified_diff(before.splitlines(1), after.splitlines(1)))
print(f"  ✓ 两个存活用例逐字节相同（{hashlib.sha256(after.encode()).hexdigest()[:16]}）")
PY2

echo "== AC4 · e2e 摘掉头段后，余下四个工具的链条仍然跑通 =="
echo -n "  test_mile0009_e2e.py 里 INBOX / origin 命中数: "
grep -c -e "INBOX" -e "origin/" tools/mile0009-e2e/tests/test_mile0009_e2e.py || true
grep -c "prd_migrate\|prd_status\|prd_update\|workspace_scope\|MIGRATE\|STATUS\|UPDATE\|SCOPE" tools/mile0009-e2e/tests/test_mile0009_e2e.py
UV_NO_SYNC=1 uv run --locked --python 3.12.12 python -m unittest discover -s tools/mile0009-e2e/tests 2>&1 | tail -4
