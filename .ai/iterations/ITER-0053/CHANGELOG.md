# 01_CHANGELOG

> ITER-0053 · MILE-0006 R3 · Codex apply_patch hooks。

## ADD

- `templates/hooks/lib/codex_patch.py` 与测试：解析 Codex patch 并逐 target 提供增删行（AC1）。
- `plugins/butler/hooks/`：默认 Pre/Post 配置和风险对称 wrappers（AC6）。
- `scripts/verify-codex-hooks.sh`、`migrations/v2.14.0.md`、ITER-0053 归档与交付（AC6/AC10）。

## EDIT

- `templates/hooks/{butler_gate,butler_advisor,lib/io}.py`：接入 apply_patch 多 target dispatch（AC2/AC4/AC5）。
- `templates/hooks/rules/{ledger_status,single_active_iteration}.py`：读取 patch 增量（AC3/AC5）。
- README、HUMAN_GUIDE、兼容说明、hook README：登记能力、trust 和不完整安全边界（AC9）。
- `.ai/project/*` 与台账：前滚 R3 现状及 R4 战线（AC10）。

## DELETE

- 无。
