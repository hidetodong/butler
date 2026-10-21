# Pinned Codex validators

This directory contains byte-for-byte snapshots of the official OpenAI Codex plugin validator, skill validator, and the three plugin-creator scripts Butler's installer runs: `create_basic_plugin.py`, `update_plugin_cachebuster.py`, and `read_marketplace_name.py`. `PROVENANCE.json` fixes the upstream repository, commit, source paths, and SHA-256 digests. `LICENSE` is the upstream Apache-2.0 license.

Butler uses these snapshots in local verification and CI so validation and the dual-host installer check never depend on whichever system skills happen to exist under a user's home directory. Missing or modified snapshots fail closed. A machine that already has Codex's plugin-creator skill still uses that live skill for a real plugin install.

To update them, fetch both files from the exact new `openai/codex` commit, review the upstream diff, replace the snapshots, update every digest and provenance field, and run:

```bash
python3 tools/codex-validators/test_vendored_validators.py
```

Do not update from a floating `main` URL during verification.
