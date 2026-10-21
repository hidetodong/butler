<!-- butler-artifact-template: 1.0.0 artifact=tech_plan -->
# TECH_PLAN — ITER-0121

方案状态: pass
方案审查日期: 2026-09-14
方案审查方式: user-ack

## Design Decisions

### D1 · 最终 deny 才写拦截日志，写失败不能放行

dispatcher 在 bypass 判定之后、exit 2 之前追加 `.ai/.hook-blocks.log`。allow 不碰这份文件。bypass 成功仍只写 `RUN_LOG.md`。

行格式跟 RUN_LOG 同一套五列：`UTC | rule_id | tool_name | 相对路径 | reason 首行`。reason 同样去掉控制字符、把 `|` 换成 `/`、截到 200 字。不改 `bypass.py` 的对外行为。

写日志失败继续 deny：函数本身不吞异常，dispatcher 顶层 catch 本来就会 exit 2。测试用注入写失败，不依赖 chmod。

上限 256KB（`256 * 1024` 字节）。超了丢掉最旧的完整行，再追加新行。

### D2 · 逃生舱看台账 `current`，只放行仓根那五份文件

`current: none` 或没有 `.ai/ITERATIONS.md` → 没有 active 迭代。台账读失败或 `current` 缺失 → 当有迭代处理（逃生舱不开）。

五份文件必须是项目根那一层：`README.md` / `CHANGELOG.md` / `.gitignore` / `VERSION` / `LICENSE`。`docs/README.md` 不算。

`phase_gate` 和 `workspace_scope` 各自在自己的 `evaluate` 开头认这个条件，认到就 allow。有 active 迭代时两道门原样跑。

共享判断放 `lib/iteration_state.py`，两道规则引用，避免各写一份。

### D3 · 摘要 CI 改成「当前 tag 或已登记」

`test_whitelist_holds_only_recomputable_history_digests` 里那条「工作区摘要必须等于 `v{VERSION}`」改成：工作区摘要等于当前 tag，**或**已在 `known_hook_tree_digests` 里。历史 tag `v1.0.0` / `v2.18.0` / `v3.1.0` 仍必须在白名单。白名单不得重复。

hook 源文件改完后，把新树摘要追加进 `migrations/manifest.json`。升级器 `sync_hooks` 本来就把源侧当前摘要并进 known 集合，已部署项目认得出新树。

不切 VERSION。本轮改了 hook 树，v4.0.0 必须含 `[sync-hooks]`。

### D4 · 不声明 TDD

没有可先红后绿的新行为契约值得配对。日志、逃生舱、摘要口径都是新允许路径，用正向回归锁。

### 执行顺序

- [ ] T1 改摘要对账测试，让未发布登记合法 → AC7
- [ ] T2 `lib/iteration_state.py` + `lib/block_log.py` → AC1 / AC3 / AC4
- [ ] T3 dispatcher 最终 deny 写日志；phase_gate / workspace_scope 接逃生舱 → AC1 / AC4 / AC5 / AC6
- [ ] T4 pytest：日志、bypass 不写、上限、注入写失败、逃生舱正反例 → AC1 / AC3 / AC4 / AC5 / AC6
- [ ] T5 `.gitignore`、hook README、范围演进、删掉已还的 hook 摘要欠账 → AC2 / AC9
- [ ] T6 登记新树摘要；跑 hook pytest、升级器测试、CI、审计 → AC8 / AC10

### Plan Admission

- **AC Coverage**：AC1/AC3→D1+T2–T4；AC2/AC9→T5；AC4–AC6→D2+T3–T4；AC7–AC8→D3+T1+T6；AC10→T6。
- **Assumptions**：pytest 能在临时项目根驱动 dispatcher；注入写失败能代替只读目录。
- **Alternatives / Trade-offs**：否掉抬 VERSION（R8 探针证明会多红）。否掉把日志写进 RUN_LOG（那份是 bypass 审计，git 可见；拦截日志要进 gitignore）。否掉 GATED_BLACKLIST 加五份文件名（那会在有迭代时也放行，AC6 禁止）。
- **Failure Modes**：见下一节。
- **Impact / Scope Challenge**：不扩到 CLAUDE.md / AGENTS.md，不加 raw 只读门禁。
- **Verification Blind Spots**：butler 仓不跑 live hook。摘要白名单多一个未发布值，不证明升级器在真实老项目上能 sync。
- **Verdict**：pass。用户 ACK 验收范围并授权开写。

## Failure Paths

- **日志写失败被吞掉**：不在 append 里 catch。
- **逃生舱把子路径 README 也放了**：只认单段路径。
- **台账读失败却放行**：当有迭代处理。
- **白名单加了随机哈希**：新摘要必须等于当前工作区 `tree_digest`；T6 用同一口径算完再写进 manifest。
- **改完 hook 忘了登记摘要**：AC8 跑升级器测试会红。

## Test Strategy

本轮**不声明 TDD cycle**。

- 日志：dispatcher 集成测试 deny / allow / bypass；unit 测上限与注入写失败。
- 逃生舱：phase_gate unit + workspace_scope 集成（scoped 项目 `current: none` vs active）。
- 摘要：改过的升级器测试 + 当前摘要在白名单。
- 收口门：`verify-ci.sh`、审计 `--allow-unreleased`。

## References Compliance

- N/A
