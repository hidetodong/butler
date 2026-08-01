#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source_plugin="$repo_root/plugins/butler"
personal_root="$HOME/.agents/plugins"
marketplace="$personal_root/marketplace.json"
target_parent="$HOME/plugins"
creator_root="${BUTLER_PLUGIN_CREATOR_DIR:-${CODEX_HOME:-$HOME/.codex}/skills/.system/plugin-creator}"
validator_python="${BUTLER_PLUGIN_VALIDATOR_PYTHON:-$repo_root/.venv/bin/python}"
skip_add=false

if [[ "${1:-}" == "--no-add" ]]; then
  skip_add=true
elif [[ $# -gt 0 ]]; then
  echo "usage: $0 [--no-add]" >&2
  exit 2
fi

for required in \
  "$source_plugin/.codex-plugin/plugin.json" \
  "$creator_root/scripts/create_basic_plugin.py" \
  "$creator_root/scripts/update_plugin_cachebuster.py" \
  "$creator_root/scripts/read_marketplace_name.py"; do
  [[ -f "$required" ]] || { echo "missing required file: $required" >&2; exit 1; }
done

mkdir -p "$target_parent"
target_parent="$(cd "$target_parent" && pwd -P)"
source_plugin="$(cd "$source_plugin" && pwd -P)"
target_plugin="$target_parent/butler"
[[ "$target_parent" != "/" ]] || { echo "refusing unsafe plugin parent: $target_parent" >&2; exit 1; }
[[ "$source_plugin" != "$target_plugin" ]] || {
  echo "refusing to overwrite the source checkout at $source_plugin; keep the Butler checkout outside ~/plugins/butler" >&2
  exit 1
}

# Use the official creator to seed/update only Butler's marketplace entry while
# preserving other entries and top-level marketplace metadata.
python3 "$creator_root/scripts/create_basic_plugin.py" butler \
  --path "$target_parent" \
  --with-skills \
  --with-marketplace \
  --marketplace-path "$marketplace" \
  --force >/dev/null

[[ "$target_plugin" == "$target_parent/butler" ]] || {
  echo "refusing unsafe target path: $target_plugin" >&2
  exit 1
}
rm -rf "$target_plugin"
cp -R "$source_plugin" "$target_plugin"

python3 "$creator_root/scripts/update_plugin_cachebuster.py" "$target_plugin"

if [[ -f "$creator_root/scripts/validate_plugin.py" ]]; then
  if command -v uv >/dev/null 2>&1; then
    uv run --with pyyaml python "$creator_root/scripts/validate_plugin.py" "$target_plugin"
  elif [[ -x "$validator_python" ]] && "$validator_python" -c 'import yaml' >/dev/null 2>&1; then
    "$validator_python" "$creator_root/scripts/validate_plugin.py" "$target_plugin"
  elif python3 -c 'import yaml' >/dev/null 2>&1; then
    python3 "$creator_root/scripts/validate_plugin.py" "$target_plugin"
  else
    echo "plugin validation requires uv or a Python runtime with PyYAML; checked: $validator_python and python3" >&2
    exit 2
  fi
fi

marketplace_name="$(python3 "$creator_root/scripts/read_marketplace_name.py" --marketplace-path "$marketplace")"
if [[ "$skip_add" == true ]]; then
  echo "Butler plugin staged at $target_plugin (marketplace: $marketplace_name; install skipped)"
else
  codex plugin add "butler@$marketplace_name"
  expected_version="$(python3 -c 'import json, sys; print(json.load(open(sys.argv[1]))["version"])' "$target_plugin/.codex-plugin/plugin.json")"
  codex plugin list --json | \
    BUTLER_EXPECTED_MARKETPLACE="$marketplace_name" BUTLER_EXPECTED_VERSION="$expected_version" python3 -c '
import json, os, sys
payload = json.load(sys.stdin)
marketplace = os.environ["BUTLER_EXPECTED_MARKETPLACE"]
version = os.environ["BUTLER_EXPECTED_VERSION"]
matches = [item for item in payload.get("installed", []) if item.get("name") == "butler" and item.get("marketplaceName") == marketplace and item.get("version") == version]
if not matches or not matches[0].get("installed") or not matches[0].get("enabled"):
    raise SystemExit(f"Butler plugin {version} was not installed and enabled from {marketplace}")
'
  echo "Butler plugin installed from marketplace '$marketplace_name'. Start a new Codex thread to load it."
fi
