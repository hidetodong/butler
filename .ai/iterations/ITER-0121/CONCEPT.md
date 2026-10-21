<!-- butler-artifact-template: 1.0.0 artifact=concept -->
# CONCEPT — ITER-0121 · hook 拦截日志与仓根 meta 逃生舱

> 分流: 完整 | 命中升级信号: 多文件改动、契约变更、跨模块影响、设计取舍 | 2026-09-14

## Current Understanding

- **R10 要做的两件事**：拦下来的 hook 事后能翻到原因；没有 active 迭代时，几份仓根说明书也能改，不用先开一轮迭代、凑齐四件套。
- **拦截日志**：最终 deny（真拦住、exit 2）往 `.ai/.hook-blocks.log` 追加一行。bypass 成功仍只写现有 `.ai/RUN_LOG.md`，两份不混。写日志失败不能改成放行，还是否认。文件进 gitignore，体积上限 256KB，超了丢掉最旧的完整行再追加。
- **逃生舱**：没有 active 迭代时，`README.md` / `CHANGELOG.md` / `.gitignore` / `VERSION` / `LICENSE` 这五份不被 `phase_gate` 和 `workspace_scope` 拦。有 active 迭代时它们仍走原门禁，不是永久白名单。不扩到 `CLAUDE.md` / `AGENTS.md`。
- **改 hook 的前提**：当前 CI 要求工作区 hook 树摘要等于 `VERSION` 对应 tag。tag 已经打过 `v3.6.0`，任何非测试 hook 改动都会红，抬版本号绕不开。本轮把判据改成「等于当前 tag，或已登记进 `known_hook_tree_digests`」，再把本轮新摘要登记进去。不切版。历史 tag 的摘要仍必须在白名单里，已部署项目才能升级。
- **明确不做**：不写 v4.0.0 配方、不加 usage 采集、不加 `references/raw/` 只读门禁（欠账写明等切版之后）、不改 bypass / RUN_LOG 语义、不做拦截看板。

## Scope

- dispatcher 在最终 deny 时追加 `.ai/.hook-blocks.log`；allow 和 bypass 成功不写这份文件。
- 日志进 gitignore（本仓必加；部署说明写清目标项目也该忽略）。
- 体积上限 256KB，超限丢掉最旧完整行。
- `ITERATIONS.md` 的 `current` 为 `none`（或没有这份台账）时，五份仓根 meta 对 `phase_gate` 和 `workspace_scope` 放行。
- 有 active 迭代时，五份文件仍受原门禁。
- 改 `scripts/test-butler-upgrade.py` 的摘要对账：允许已登记的未发布摘要；本轮改完的 hook 树摘要登记进 `known_hook_tree_digests`。
- pytest hook 测试覆盖日志、逃生舱、有迭代时仍拦截；升级器测试覆盖新摘要口径。
- hook README 写清日志和逃生舱；`.ai/MILESTONE.md` 登记 v4.0.0 必须含 `[sync-hooks]`。
- 本轮改了 hook 源文件，欠账里「hook 树一改就必须跟切版绑在一起」若被本轮解开就删掉，没解开就如实留着。

## Open Questions / Risks

- **~~日志上限~~（已定）**：256KB，超了丢最旧行。
- **~~逃生舱扩不扩~~（已定）**：不扩，就里程碑点名的五份。
- **风险 · 日志写失败**：必须继续 deny。测试要覆盖「目录不可写时仍 exit 2」。
- **风险 · 摘要白名单被理解成任意放行**：历史 tag 复算对账仍在；只多允许「当前工作区这份未发布摘要」这一条登记。
- **风险 · butler 仓自己不跑 live hook**：行为靠 pytest 锁，本仓改 README 不会真触发门禁。
