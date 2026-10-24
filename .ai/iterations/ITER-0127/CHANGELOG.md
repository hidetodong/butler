<!-- butler-artifact-template: 1.0.0 artifact=changelog -->
# ITER-0127 变更流

> 把 Grok CLI 做成正式宿主 · closed · 2026-10-24

## ADD

- `templates/hooks/tests/test_grok_tool_names.py` — 比对 Grok 的两个写文件工具名和现有名字的退出码、规则号，并确认终端命令仍放行 → AC2

## EDIT

- `scripts/setup.sh` — 发现 Grok 时把技能目录软链到 `~/.grok/skills/`；找不到就跳过，不创建该目录；同名真实文件或目录则停下，不删除 → AC1
- `scripts/verify-dual-host.sh` — 用临时家目录锁住装上、重跑、跳过、改错链和真实目录冲突，并断言三份文档里的那句话和两份入口 → AC1 / AC3 / AC5
- `templates/hooks/butler_gate.py` — 入口处把 `write` 译成 `Write`、把 `search_replace` 译成 `Edit`，并接受驼峰字段名；终端命令不翻译 → AC2
- `README.md`、`HUMAN_GUIDE.md`、`docs/codex-compatibility.md` — 写明 Grok 是宿主，技能用软链安装，找不到就跳过，两份入口都会被读到 → AC3
- `migrations/manifest.json` — 钩子树白名单追加当前工作区摘要，保留 `v4.0.0` 那条，不因此切版 → AC5

## DELETE

- 无
