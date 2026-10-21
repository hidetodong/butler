<!-- butler-artifact-template: 1.0.0 artifact=changelog -->
# ITER-0121 变更流

> hook 拦截日志与仓根 meta 逃生舱 · closed · 2026-09-14

## ADD

- `templates/hooks/lib/block_log.py` — 最终 deny 追加 `.ai/.hook-blocks.log`，256KB 上限 → AC1 / AC3
- `templates/hooks/lib/iteration_state.py` — 有无 active 迭代、仓根五份 meta 判断 → AC4 / AC5 / AC6
- `.ai/.hook-blocks.log` gitignore 条目 → AC2

## EDIT

- `templates/hooks/butler_gate.py` — 最终 deny 写拦截日志 → AC1
- `templates/hooks/rules/phase_gate.py` / `workspace_scope.py` — 无迭代时放行五份仓根 meta → AC4 / AC5 / AC6
- `scripts/test-butler-upgrade.py` — 摘要可等于当前 tag 或已登记白名单 → AC7
- `migrations/manifest.json` — 登记本轮 hook 树摘要 → AC8
- `templates/hooks/README.md` — 拦截日志与逃生舱说明 → AC2
- `.ai/MILESTONE.md` §5.4 — v4.0.0 必须 `[sync-hooks]` → AC9
- `.ai/debt.md` — 删掉已解开的 hook 摘要欠账 → AC9

## DELETE

- `.ai/debt.md` 条目「hook 树一改就必须跟切版绑在一起」 → AC9
