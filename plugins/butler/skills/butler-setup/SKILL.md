---
name: butler-setup
description: Install or refresh Butler machine-wide across Claude Code, Codex, and Pi by delegating to the repository setup entrypoint. Use when the user invokes $butler-setup, asks to run Butler setup/global installation, refresh host commands or plugins, or install Butler's machine-level integrations.
---

# Butler Setup

1. Resolve a unique `BUTLER_PATH`; require `VERSION`, `Coder/README.md`, `Coder/20_Workflow_Lifecycle/butler-setup.md`, and `scripts/setup.sh`.
2. Read `Coder/20_Workflow_Lifecycle/butler-setup.md` in full. Do not copy or simulate setup steps from the skill.
3. Echo the resolved root and disclose the machine-level user-directory changes before execution.
4. Treat an explicit `$butler-setup` invocation or direct request to install/refresh Butler now as confirmation. For informational or ambiguous setup questions, wait for explicit confirmation.
5. After confirmation, run only `bash "$BUTLER_PATH/scripts/setup.sh"` as an argv-style command. Never set `BUTLER_BYPASS`, accept hook trust, initialize a project, or invent recovery writes.
6. Preserve stdout, stderr, and the real exit code. Report Claude, Codex, and Pi results separately, including skipped or partially completed components.
7. State the bootstrap boundary: a machine with no Butler discovery surface must first clone the repository and run `bash scripts/setup.sh` once.
