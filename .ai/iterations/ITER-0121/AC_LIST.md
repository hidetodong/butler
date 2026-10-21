---
状态: ack-frozen
ACK 日期: 2026-09-14
---
<!-- butler-artifact-template: 1.0.0 artifact=acceptance -->
# AC_LIST — ITER-0121

## Goal

- 拦下来的 hook 能在 `.ai/.hook-blocks.log` 里翻到；没有进行中的迭代时，五份仓根说明书能直接改。改 hook 源文件不会因为「摘要必须等于当前 tag」让 CI 红。

## In Scope

- 最终 deny 追加 `.ai/.hook-blocks.log`（gitignore、256KB 上限、写失败仍 deny）。
- 无 active 迭代时，`README.md` / `CHANGELOG.md` / `.gitignore` / `VERSION` / `LICENSE` 不被 `phase_gate` 和 `workspace_scope` 拦。
- hook 树摘要 CI 允许登记未发布摘要，本轮新摘要进白名单。
- 测试、hook README、里程碑范围演进记录（v4.0.0 必须 `[sync-hooks]`）。

## Out of Scope

- 不切 VERSION、不写 `migrations/v4.0.0.md`、不跑真实升级器。
- 不加 usage instrumentation，不加 `references/raw/` 只读门禁。
- 不改 bypass / `RUN_LOG.md` 语义，不把 allow 记进拦截日志。
- 不把 `CLAUDE.md` / `AGENTS.md` 放进逃生舱。

## Acceptance Checklist

- [ ] AC1: 最终 deny（bypass 未生效）会往项目根 `.ai/.hook-blocks.log` 追加恰好一行，含 UTC 时间、rule_id、tool_name、相对路径、reason 首行。allow 不建、不写这份文件。bypass 成功只写 `RUN_LOG.md`，不写 `.hook-blocks.log`。
- [ ] AC2: 本仓 `.gitignore` 含 `.ai/.hook-blocks.log`。hook README 写明目标项目也应忽略该文件。
- [ ] AC3: 追加后若文件超过 256KB，丢掉最旧的完整行直到能放下新行；新行仍在。日志目录不可写时 dispatcher 仍 exit 2，不放行。
- [ ] AC4: `current: none` 或没有 `.ai/ITERATIONS.md` 时，五份仓根 meta 对 `phase_gate` 为 allow，即使没有 CONCEPT / AC_LIST / TECH_PLAN。
- [ ] AC5: 同上条件下，对已启用 workspace scope 的项目写这五份文件，`workspace_scope` 为 allow（对照：写 `packages/api/...` 仍 deny）。
- [ ] AC6: 台账 `current` 指向一个 active 迭代、且缺少四件套时，写 `README.md` 仍被 `phase_gate` deny。逃生舱不是永久白名单。
- [ ] AC7: `scripts/test-butler-upgrade.py` 不再要求工作区 hook 摘要等于当前 VERSION 对应 tag；工作区摘要在 `known_hook_tree_digests` 里即可。历史 tag `v1.0.0` / `v2.18.0` / `v3.1.0` 的摘要仍必须在白名单里。
- [ ] AC8: 本轮 hook 源文件改完后，当前树摘要已写入 `known_hook_tree_digests`。`python3 -m pytest templates/hooks/tests -q` 退出码 0；`python3 scripts/test-butler-upgrade.py` 退出码 0。
- [ ] AC9: `.ai/MILESTONE.md` 范围演进记录写明本轮改了 hook 树，v4.0.0 必须含 `[sync-hooks]`。`.ai/debt.md` 里「hook 树一改就必须跟切版绑在一起」若已解开则删除，否则如实保留。
- [ ] AC10: `bash scripts/verify-ci.sh` 退出码 0；`python3 scripts/audit-project-state.py --project-root . --allow-unreleased` 退出码 0，`[DRIFT]` 为 0。

## Verification Method

- AC1 / AC3: hook pytest 用临时项目根喂 deny / allow / bypass，断言文件内容和退出码。
- AC2: 读本仓 `.gitignore` 与 `templates/hooks/README.md`。
- AC4 / AC6: `test_phase_gate.py` 夹具分别构造 `current: none` 与 active 台账。
- AC5: 复用 `test_workspace_scope_gate.py` 的 scoped 项目，台账置 `current: none`。
- AC7 / AC8: 升级器测试 + 本轮摘要登记 + pytest。
- AC9: grep 范围演进记录与 `debt.md`。
- AC10: 两条命令取退出码。

## External References

- N/A

## Open Questions / Risks

- 日志写失败路径依赖夹具把目录打成只读，在部分系统上可能不好造；造不出就改用注入写失败，不假装测过。
- butler 仓不跑 live hook，AC1–AC6 只在 pytest 里为真。
