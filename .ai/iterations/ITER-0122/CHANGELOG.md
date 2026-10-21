<!-- butler-artifact-template: 1.0.0 artifact=changelog -->
# ITER-0122 变更流

> usage 采集：CLI 入口记下最后调用时间 · closed · 2026-09-14

## ADD

- `tools/usage/` — record / show / catalog，落点 `.ai/.usage.json` → AC1 / AC2 / AC3
- `.gitignore` 条目 `.ai/.usage.json` → AC1

## EDIT

- 产品驻留工具 `main` 打点 → AC5
- 工作流薄壳（Claude 命令与 Codex skill）加上 `usage.py record workflow:<id>` → AC7
- `scripts/verify-ci.sh` 接入 usage 测试 → AC9 / AC10
- `.ai/debt.md` 运行时观测缺位改为采集已落地、报告归 R12 → AC8
- `.ai/OVERVIEW.md` 驻留工具清单纳入 usage → AC10
- 若干工具测试的树哈希忽略 `.usage.json`；workspace-scope check-diff 忽略该文件 → AC9

## DELETE

- 无
