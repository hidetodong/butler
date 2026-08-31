#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/../../.."
echo "== 旧 inbox 全链逐份哈希比对 =="
n=0
while read -r d p; do
  case "$d" in \#*) continue;; esac
  [ -z "${p:-}" ] && continue
  a=$(shasum -a 256 "$p" | awk '{print $1}')
  if [ "$a" = "$d" ]; then echo "unchanged  $p"; else echo "DRIFT      $p"; exit 1; fi
  n=$((n+1))
done < .ai/iterations/ITER-0117/legacy-inbox.baseline
echo "checked=$n"
echo "== registry 的 inbox 条目仍在 =="
python3 -c "
import json;d=json.load(open('workflows/registry.json'))
w=[x for x in d['workflows'] if x['id']=='inbox']
print('inbox entry:', w[0]['id'], w[0]['claude'], '| rule_source:', w[0]['rule_source'], '| workflows total:', len(d['workflows']))
assert len(w)==1 and len(d['workflows'])==12"
echo "AC10 PASS"
