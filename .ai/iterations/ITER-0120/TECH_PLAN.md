<!-- butler-artifact-template: 1.0.0 artifact=tech_plan -->
# TECH_PLAN — ITER-0120

方案状态: pass
方案审查日期: 2026-09-11
方案审查方式: user-ack

## Design Decisions

### D1 · 先 `git mv`，同一工作树里立刻改完活指针

两棵目录都用 `git mv` 保血缘，内部形状不动：`.ai/milestone-backlog/` → `.ai/backlog/`（10 份草稿文件名不变）；仓根 `deliveries/` → `.ai/deliveries/`（迭代交付平铺，`milestones/` 子目录保留）。不建仓根软链。

顺序不能反，也不能在中间跑 CI：先搬文件，活指针会暂时指向不存在的旧路径；先改指针，文件还在旧位置，测试会按新路径找不到。正确做法是同一个工作树里连续做完「搬家 + 改完所有活指针」，再跑测试。中途中断用 `git checkout` 退回。

### D2 · 活指针改、历史记述不改；`deliveries/` 按「找文件 / 当时做过什么」拆

`.ai/milestone-backlog` 这个字符串在活面上就是路径，活跃文件里整词替换成 `.ai/backlog` 即可。

`deliveries/` 不行。同一串字有两种身份：

| 身份 | 改不改 | 例子 |
|---|---|---|
| 找文件的活指针 | 改成 `.ai/deliveries/` | 台账「交付」列、`delivery-summary.md` 落点、CHANGELOG 里「详见 `deliveries/ITER-…`」、冷启动读序第 5 步 |
| 当时做过什么的叙述 | 不改 | 收口快照、已发布配方、交付正文内部、CHANGELOG 里「本轮写到 deliveries/」这种句子 |

排除面写死在扫描脚本里，不允许执行时临时加名单。交付正文里的 `../ITER-….md` 相对链接整树平移后仍有效，不改。

台账冷分片是**活索引**，不是收口快照：审计会把热表和 `.ai/history/iterations/` 两片拼起来，按「交付」列当相对项目根的路径去 `test -f`。只改热表会一次红一百来条。改完热表和两片冷分片后跑 `python3 tools/state-ledger/state_ledger.py migrate --project-root .`——它会按改过的行重画分片并刷新哈希回执。`migrate` 自己不改交付路径，所以路径必须先写进 markdown。

闪念口去向和待办区草稿列也是活指针。`intake.py` 没有「只改路径、不转移状态」的动作，本轮作为数据迁移一次性改写这两处，不走 `handle`。这不是日常手改闪念口。

### D3 · 部署只建 `.ai/`；hook 黑名单故意不动

init / `mcv-deployment.md` / rule-card 现在写的是建 `.ai/` 和仓根 `deliveries/` 两个目录。搬家后仓根不再有交付目录：部署只建 `.ai/`，`.ai/backlog/` 与 `.ai/deliveries/` 都按需产生（第一次孵化、第一次收口）。

`templates/hooks/lib/io.py` 的 `GATED_BLACKLIST` 仍保留 `deliveries/`。已部署项目在 R15 之前仓根还有这个目录，删掉豁免会让他们写交付被 phase_gate 误拦。新路径 `.ai/deliveries/` 已经被 `.ai/` 前缀覆盖。进摘要的 hook 文件本轮零字节改动，避开「hook 树摘要必须等于当前 VERSION 对应 tag」那条 CI。

### D4 · 冷启动读序只改真源，四处投影抄同一段

第 5 步「不全量读取 … 或 `deliveries/` 历史归档」改成 `.ai/deliveries/`。第 3 条自检从写死 `deliveries/<链接>` 改成「按台账交付列相对项目根解析」。真源只在 `context-persistence.md §6`。改完把标记块原样抄到 `Coder/README.md`、仓根 `AGENTS.md`、两份入口模板，再跑 `python3 tools/context-budget/context_budget.py check`。`check` 只核对、不代写。仓根本体 `CLAUDE.md` 没有这段投影，它那处 `deliveries/` 是 CHANGELOG 职责说明，按活指针改。

### D5 · 已部署项目本轮只登记，不写配方、不跑升级器

按 `migration-schema.md §5` 写进 `.ai/MILESTONE.md` 范围演进记录：

- 改了 `templates/rule-card.md` 和两份入口模板 → v4.0.0 必须含 `[regen-entrypoints]`
- 未改 hook 树 → 不需要 `[sync-hooks]`
- 候办改名在 `.ai/` 内部 → 现有 `[rename]` 能表达
- 仓根 `deliveries/` 搬进 `.ai/` → `[rename]` 要求源路径第一段是 `.ai/`，表达不了，等 R14 补移动动作，配方正文归 R15

本轮不写 `migrations/v4.0.0.md`，不抬 VERSION。

### D6 · 不声明 TDD；扫描脚本模式串拼接，避免自命中

本轮没有新行为可先红后绿：搬家之后测试按旧路径红、改夹具后绿，那是迁移不是 TDD。扫描脚本放 `.ai/iterations/ITER-0120/ac-sweep.py`（P4 提前建这个目录只为放脚本和基线，不是收口归档）。模式串用变量拼接，排除面写死。

### 执行顺序

- [ ] T1 记下开工前基线：hook 树摘要、候办文件名集合、交付文件数 272、冷分片交付列样本 → AC8 / AC1 / AC4
- [ ] T2 `git mv` 两棵目录 → AC1 / AC4
- [ ] T3 改 `tools/intake/` 常量、测试夹具、闪念口去向、待办区草稿列 → AC1 / AC2
- [ ] T4 改 `scripts/audit-project-state.py` 与 `scripts/test-audit-project-state.py` → AC3 / AC5
- [ ] T5 改活规则与入口：schema、部署、init、rule-card、README、HUMAN_GUIDE、delivery-summary、lifecycle、milestone / iteration schema → AC6
- [ ] T6 改 `context-persistence.md §6`，四处投影抄同一段，跑 context-budget `check` → AC7
- [ ] T7 改热表 + 两片冷分片的交付列，跑 state-ledger `migrate` 再 `check` → AC5
- [ ] T8 改 CHANGELOG 里找文件的链接；`.ai/invariants.md` 与决策地图里仍指向旧候办路径的活指针 → AC12
- [ ] T9 写 `.ai/MILESTONE.md` 范围演进记录 → AC10
- [ ] T10 写扫描脚本、`--write` OVERVIEW、跑 CI 与审计 → AC11 / AC12

T3–T8 在 T2 之后同一工作树连续做，不穿插 CI。T10 最后做。

### Plan Admission

- **AC Coverage**：AC1–AC4 由 T2–T4 覆盖；AC5 由 T7；AC6–AC7 由 T5–T6；AC8 由 D3 的「零改动」加 T1 基线比对；AC9 由 `git diff` 对排除目录；AC10 由 T9；AC11–AC12 由 T10。12 条都有设计落点和验证动作。
- **Assumptions**：`git mv` 能保住 `ITER-0119` 那份交付的 follow 历史；`state-ledger migrate` 重画分片时只刷新哈希、不把交付列改回旧值；四处读序投影仍按字节相等校验，改一步多四个字符仍低于 1400 字节上限。
- **Alternatives / Trade-offs**：否掉兼容软链（里程碑已定破坏性搬家）。否掉先改指针再搬家（中间态测试全红且更难回滚）。否掉本轮改 hook 黑名单（R8 已证明会让 CI 红，且已部署项目还需要旧豁免）。否掉把 `.ai/project/workspaces.md` 捎上（不是本路线项）。
- **Failure Modes**：见下一节。
- **Impact / Scope Challenge**：最小方案就是两次 `git mv` 加活指针改写，没有更小还能过审计的做法。不把工作区地图改名、不拍平 `milestones/`、不写升级配方。
- **Verification Blind Spots**：扫描按字面匹配，改成同义换说法会漏网，CHANGELOG 人读句只能抽查。`git log --follow` 对一次 rename 通常有效，但不保证所有交付文件的血缘展示都好看。静态扫描证不了「下次收口真的写到新路径」——那要等 ITER-0120 自己收口，本轮只保证规则和工具已经指向新路径。
- **Verdict**：pass。没有已知 Must Fix；等用户 ACK 后把顶部 `方案状态` 置 `pass` 再进 P4。

## Failure Paths

- **冷分片漏改或漏跑 migrate**：审计按拼起来的台账找文件，漏一片就红一片。T7 把改列和 `migrate`/`check` 绑在一起，`check` 不绿不准进 T10。
- **CHANGELOG 误伤历史叙述**：整文件替换 `deliveries/` 会把「当时写到 deliveries/」改成假话。T8 只改「详见 `deliveries/…`」这种链接形态，扫描排除叙述句。
- **搬家和改指针之间跑了测试**：中间态必红。T2 之后到 T8 结束前不跑 CI。
- **误改冻结快照**：对 `.ai/iterations/`、`.ai/milestones/`、`migrations/`、`docs/research/`、`docs/superpowers/` 做路径替换。T10 的 AC9 用 `git diff` 对这些目录必须为空来拦。
- **误改 hook 源文件**：T1 记下摘要，T10 用同一口径复算，对不上就停。
- **读序投影漏抄一处**：`context_budget.py check` 会指名哪份和真源不一致。T6 以它的退出码为准，不靠人眼。
- **intake 测试夹具漏改**：常量改了、测试还 mkdir `milestone-backlog`，单跑 intake 测试就会红。T3 把常量和测试放在同一批。

## Test Strategy

本轮**不声明 TDD cycle**。没有新行为可先红后绿。

- **搬家血缘**：`git log --follow -- .ai/deliveries/ITER-0119-retire-old-inbox-chain.md` 能追到搬家前提交。
- **工具回归**：`python -m unittest discover -s tools/intake/tests -t .`；`python3 scripts/test-audit-project-state.py`；explore-dogfood 相关测试随 CI。
- **台账**：`python3 tools/state-ledger/state_ledger.py check --project-root .`；审计对每个 closed 行的交付文件 `test -f`。
- **读序**：`python3 tools/context-budget/context_budget.py check`。
- **hook 未动**：升级器 `hook_source_files` + `tree_digest` 与 T1 基线比对。
- **扫描**：`.ai/iterations/ITER-0120/ac-sweep.py` A/B 两组；排除面写进 VERIFY_REPORT。
- **收口门**：`python3 scripts/sync-project-overview.py --write` 再 `--check`；`python3 scripts/audit-project-state.py --project-root . --allow-unreleased`；`bash scripts/verify-ci.sh`。

## References Compliance

- 本迭代无 `.ai/references/` 外部参考资料，不涉及 PRD 切片。
- 按 `migration-schema.md §5` 判定见 D5，结论落 `.ai/MILESTONE.md` 范围演进记录，不在本轮写配方。
- 按 `references-schema.md` 非回归门：不改 PRD 消费者，不碰 `.ai/references/raw/`。
- 按 `intake-schema.md`：日常闪念口仍只由 `intake.py` 写；本轮路径改写是一次性数据迁移，在方案里单列，不设成新入口。
