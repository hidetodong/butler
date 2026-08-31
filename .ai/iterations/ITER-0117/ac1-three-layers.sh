#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/../../.."
F=Coder/40_Context_Management/intake-schema.md
echo "== 三层骨架 =="
grep -n '^## 1\. 第一层\|^## 2\. 第二层\|^## 3\. 第三层' "$F"
echo "== 第一层：字段清单 / 稳定键形态 =="
grep -n '闪念键 | 记于 | 一句话 | 状态 | 去向' "$F"
grep -n 'YYYY-MM-DD-<kebab 短句>' "$F"
echo "== 第一层：状态封闭四态 + 转移四条 =="
python3 - <<'PY'
import re, pathlib
t = pathlib.Path('Coder/40_Context_Management/intake-schema.md').read_text(encoding='utf-8')
s = re.findall(r'^\| `([a-z]+)` \|', t.split('### 1.4')[1].split('### 1.5')[0], re.M)
m = re.findall(r'^\| `(\w+) → (\w+)` \|', t.split('### 1.5')[1].split('### 1.6')[0], re.M)
assert s == ['new','incubated','done','dropped'], s
assert m == [('new','incubated'),('new','done'),('new','dropped'),('incubated','dropped')], m
print('states =', s)
print('transitions =', m)
PY
echo "== 第二层：规模三档 + 按档结构 =="
python3 - <<'PY'
import re, pathlib
t = pathlib.Path('Coder/40_Context_Management/intake-schema.md').read_text(encoding='utf-8')
g = re.findall(r'^\| `([a-z]+)` \|', t.split('### 2.2')[1].split('### 2.3')[0], re.M)
assert g == ['milestone','iteration','undecided'], g
seg = t.split('### 2.3')[1].split('### 2.4')[0]
for want in ['范围评估 / 理解阐释 / 拆分路线图 / 范围演进记录', '要解决什么 / 暂缓原因', '想做什么 / 卡在哪']:
    assert want in seg, want
print('tiers =', g, '| 三档段落集齐备')
PY
echo "== 第三层：三条出口 + 前置条件 =="
python3 - <<'PY'
import re, pathlib
t = pathlib.Path('Coder/40_Context_Management/intake-schema.md').read_text(encoding='utf-8')
seg = t.split('### 3.1')[1].split('### 3.2')[0]
exits = re.findall(r'^\| (提升为里程碑|开为迭代|撤回) \|', seg, re.M)
assert exits == ['提升为里程碑','开为迭代','撤回'], exits
assert '当前没有 active 里程碑' in seg and '当前没有 active 迭代' in seg
print('exits =', exits, '| 前置条件在场')
PY
echo "== 无开口措辞 =="
if grep -nE '等等|视情况而定' "$F"; then echo "FAIL: 枚举有开口"; exit 1; fi
echo "AC1 PASS"
