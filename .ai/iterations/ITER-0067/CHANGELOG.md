> 项目外写入授权边界 · closed · 2026-07-18

## ADD

- `templates/hooks/tests/test_external_write_policy.py` — 锁定危险模式授权上限和宿主权限分工的文档合同 → AC6, AC7

## EDIT

- `templates/hooks/lib/io.py` — 拆开未知目标与项目外目标，统一按真实项目根归属并支持多项目 patch → AC1, AC2, AC3, AC4
- `templates/hooks/rules/phase_gate.py` — 坏输入继续拒绝，真实项目外目标退出 Butler 流程判定 → AC1, AC2, AC5
- `templates/hooks/tests/test_io.py`、`test_phase_gate.py`、`test_codex_patch.py`、`test_integration.py` — 覆盖外部放行、坏输入拒绝、子目录、兄弟项目和多根正反路径 → AC1, AC2, AC3, AC4, AC5
- `scripts/verify-codex-hooks.sh` — 把聚合目录外部写入 E2E 从 Butler 拒绝改为宿主权限接管 → AC1, AC7
- `Coder/65_Extension_Dangerous/dangerous-engine.md` — 新增启动冻结授权上限、范围内动态施工和范围外依赖路由 → AC6
- `Coder/20_Workflow_Lifecycle/mcv-deployment.md`、`Coder/README.md`、`templates/hooks/README.md`、`templates/rule-card.md` — 统一项目流程门禁与宿主文件权限的职责边界 → AC6, AC7

## DELETE

- 无
