<!-- butler-artifact-template: 1.0.0 artifact=changelog -->
# ITER-0123 变更流

> usage 报告：90 天分档替代手工回忆 · closed · 2026-10-19

## ADD

- `tools/usage-report/` — 只读报告，按最后调用时间把入口分成 A/B/C/D，默认 90 天 → AC1 / AC2 / AC3 / AC4 / AC5 / AC8

## EDIT

- `tools/usage/usage.py` — 产品工具名单加入 `usage-report` → AC6
- `scripts/verify-ci.sh` — 接入 usage 与 usage-report 测试 → AC9
- `.ai/OVERVIEW.md` — 驻留工具清单纳入 usage-report → AC9
- `.ai/debt.md` — 给人读的工作流个数不再指望这份报告去改那三份散文

## DELETE

- `.ai/debt.md` 条目「运行时观测缺位」 → AC7
