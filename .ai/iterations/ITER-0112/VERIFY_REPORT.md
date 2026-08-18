<!-- butler-artifact-template: 1.0.0 artifact=verify_report -->
# VERIFY_REPORT — ITER-0112

## Verification Summary

- 10/10 AC 达成：7 条 `auto·可靠`（AC1、AC3–AC8），3 条 `auto·弱`（AC2、AC9、AC10）。9 条 evidence record，8 条 `passed`、1 条 `failed` 保留为诊断。完整 `scripts/verify-ci.sh` 退出码 0。
- 本轮删掉的是「靠 delta 折叠维护、需要回头重评旧内容」的那部分：`.ai/project/` 下 5 份文件、折叠结构契约 `project-digest-schema.md`、两个折叠 / 漂移帮手，以及两处收口仪式对折叠的强制。留下的 `invariants.md`（纯追加）与 `frontier.md`（整体覆写）一字未删。
- 删 `capabilities.md` 前 22 个小节逐条核过，不是整文件一删了事。核查结论是 22 节全部可弃、真源在别处；唯一无真源的一条欠债已迁进 `.ai/debt.md`。
- 执行中撞到一次 AC 自相矛盾（AC1 要求 `invariants.md` 一字不动 vs AC6 要求活文件无断指针），按 `iteration-schema.md §5.3` 走了 amend + 重新 ACK，没有绕过。
- 有两个东西 P1 阶段没看出来、执行时才发现，都已按发现原样处理并登记：`.ai/project/workspaces.md` 是 workspace-scope 的活契约（由 PreToolUse hook 消费），跟知识文件夹机制无关，不在删除面内；`[split]` 标签不能删，历史配方 v1.6.0–v2.2.0 引用它、配方清单有一致性校验。

## AC Status

- [x] AC1 (auto·可靠): `.ai/project/` 下只剩 `invariants.md` 与 `frontier.md`；`frontier.md` 未被本迭代触碰；`invariants.md` 只改了三行（冷启动读序第一读、一致性自检条数、全貌产物形态），`*为什么*` 理由从 39 条增到 42 条、一条未少；`.ai/debt.md` 存在，正文与迁移前一致，只多了迁出的那一条（`ac1-files`）。
- [x] AC2 (auto·弱): 22 个小节的核查结论逐条写进 `.ai/01_CHANGELOG.md` 的 DELETE 段，机器复核了小节计数为 22、迁出条目确实落在 `.ai/debt.md`、被指为真源的 11 个文件全部存在（`ac2-ac9-ac10-proxy`）。人读部分见下「Verification Results」的抽查记录。标 `弱` 而非 `可靠`——机器查得出真源文件在不在，查不出里面写的是不是真比被删的那份更准。
- [x] AC3 (auto·可靠): `Coder/62_Extension_Agents/` 只剩 `overview.md` / `independent-review.md` / `decision-work.md` 三份；`overview.md` 与 `Coder/README.md` 检索 `knowledge-fold` / `drift-check` 零命中（`ac3-roster`）。
- [x] AC4 (auto·可靠): 两处收口仪式检索 `折叠` / `knowledge-fold` / `project-digest` 零命中；迭代收口改为「前三步必做、第四步自检」，里程碑收口改为「三步必做」，步骤编号连贯（`ac4-rituals`）。
- [x] AC5 (auto·可靠): `project-digest-schema.md` 已删且 `Coder/README.md` 检索 `project-digest` 零命中；`context-persistence.md §6` 漂移自检不变量已删，余下 5 条编号连续（`ac5-schema-gone`）。
- [x] AC6 (auto·可靠): 按归档白名单过滤后，`project-digest|knowledge-fold|drift-check|fold-state` 在活跃文件中零命中（`AC6-CLEAN`）；剩余 12 处 `.ai/project` 路径字样逐条核对去向，2 处指 `invariants.md`（真实存在）、9 处指部署项目侧的 `workspaces.md`、1 处是升级器测试的夹具路径（`ac6-scan`）。
- [x] AC7 (auto·可靠): `bash scripts/verify-ci.sh` 退出码 0，无跳过、无单点豁免（`ac7-verify-ci`）。
- [x] AC8 (auto·可靠): `scripts/audit-project-state.py` 802 项 OK，非 OK 行只剩 `release.worktree` 与 `release.tag` 两项发布态提示（`ac8-audit-final`，按 `iteration-schema.md §5.5 步④` 对 Butler 仓用 `--allow-unreleased` 并保留亮牌）；输出中不再有任何 fold receipt 或知识文件夹校验行。
- [x] AC9 (auto·弱): `.ai/MILESTONE.md §5.4` 末条为「R1 收口 · 交接登记」，三处逐项写明现状与归属；机器复核了三项都在、R14 / R15 都点了名，并反查三处现状与登记描述一致（`ac2-ac9-ac10-proxy`）。标 `弱`——机器查得出登记写没写，查不出归属分得对不对。
- [x] AC10 (auto·弱): 交付总结「已知剩余风险 / 延后事项」第一、二条分别记录两项信息损失，并写明确定性数据要等 R11（`ac2-ac9-ac10-proxy`）。标 `弱`——机器查得出段落在不在，判不了描述是否诚实，这一条终究靠自觉。

## 人测道小结

- N/A（本轮无 `human·待人` 档 AC——AC2 / AC9 / AC10 原定人读，按 `testing-strategy.md §3`「能造出弱检查的项就不算人测残余」造了代理验证，归自动道弱档，不起交付自测桥）。

## Evidence Index

| Evidence ID | AC | 强度 | Outcome | Record |
|---|---|---|---|---|
| ac1-files | AC1 | captured | passed | `.ai/iterations/ITER-0112/evidence/ac1-files/record.json` |
| ac2-ac9-ac10-proxy | AC2,AC9,AC10 | captured | passed | `.ai/iterations/ITER-0112/evidence/ac2-ac9-ac10-proxy/record.json` |
| ac3-roster | AC3 | captured | passed | `.ai/iterations/ITER-0112/evidence/ac3-roster/record.json` |
| ac4-rituals | AC4 | captured | passed | `.ai/iterations/ITER-0112/evidence/ac4-rituals/record.json` |
| ac5-schema-gone | AC5 | captured | passed | `.ai/iterations/ITER-0112/evidence/ac5-schema-gone/record.json` |
| ac6-scan | AC6 | captured | passed | `.ai/iterations/ITER-0112/evidence/ac6-scan/record.json` |
| ac7-verify-ci | AC7 | captured | passed | `.ai/iterations/ITER-0112/evidence/ac7-verify-ci/record.json` |
| ac8-audit | AC8 | captured | failed | `.ai/iterations/ITER-0112/evidence/ac8-audit/record.json` |
| ac8-audit-final | AC8 | captured | passed | `.ai/iterations/ITER-0112/evidence/ac8-audit-final/record.json` |

## Verification Results

- **保留的那条 failed record 是什么**：`ac8-audit` 是不带 `--allow-unreleased` 的首跑，退出码 1。除两项发布态 DRIFT 外，它还报了第三项 `handoff.freshness: stale`——迭代改了一堆源文件、handoff 回执还停在旧 hash。跑 `tools/handoff/handoff.py sync` 同步后复跑即净，`ac8-audit-final` 是同步后的记录。首跑不删，留作「审计确实抓到了漂移」的痕迹。
- **AC2 的人读抽查**：从 22 节里抽了 5 条反查真源，全部命中——「远端 required check 未启用」这条诚实声明在 `HUMAN_GUIDE.md`（3 处）/ `docs/codex-compatibility.md` / `README.md` 都在；驻留工具描述在 `Coder/README.md` 第 172–217 行比被删那份更详（每个工具都写了职责边界与「不做什么」）；工作流注册的两个真源 `workflows/registry.json` 与 `docs/workflows.md` 都在；semver 与提交规约在 `versioning-schema.md §5`；迁出的那条欠债在 `.ai/debt.md` 里。
- **AC1 的三行修订具体改了什么**：一是冷启动读序的第一读，从「知识文件夹两态」改成 `.ai/debt.md`；二是一致性自检的条数，6 条改 5 条；三是新增一条「全貌产物不靠 delta 折叠维护（ITER-0112 起）」，把本轮的诊断结论固定下来——整体覆写和纯追加活得下来、需要回头重评旧内容的必烂。理由层没动，`*为什么*` 反而多了 3 条（新写的那条自带理由）。
- **AC6 白名单的边界**：扫描排除 `.git/`、`.ai/iterations/`、`.ai/milestones/`、`.ai/history/`、`deliveries/`、`docs/research/`、`migrations/v1.` 与 `v2.`、`CHANGELOG.md`、工作区四件套自身与 `.ai/verification-evidence/`，另外单独放行 `migration-schema.md`（`[split]` 退役标注）与 `overview.md`（帮手退役说明）——这两处是有意留的退役标注，不是漏改。排除项都是历史归档或本轮有意保留的说明，不是为了让扫描变绿而设的豁免。
- **两处 P1 没看出来的东西**：
  - `.ai/project/workspaces.md` 不属于知识文件夹机制。它是 workspace-scope 的项目工作区地图，由 `templates/hooks/` 的 PreToolUse hook 实际读取来拦越界写入，有 4 份规则 + 4 份测试在消费。butler 是单包仓、本仓没有这个文件，所以扫描时它表现为「悬空指针」，其实是部署项目侧的正常路径。已在变更流里标为「保留（不属本机制）」。
  - `[split]` 标签删不掉。`migrations/v1.6.0` 到 `v2.2.0` 五份历史配方引用了它，`migrations/manifest.json` 有标签定义与配方引用的一致性校验，删定义就红。改为在原处加退役标注（自 v4.0.0 起不再产生新实例），动作类型的正式改造交给 R14。
- **`domain-model.md` 的断指针**：AC6 扫描抓到全仓唯一一处真断链——第 53 行「当前已知语义债务：`.ai/project/debt.md`」，`debt.md` 已迁位。已改为 `.ai/debt.md`。

## TDD Pair Status

- N/A（TECH_PLAN 未声明 TDD cycle；本轮是删除与去指针，机器侧改动是拆掉夹具而非新增行为）。

## Goal Calibration

- 当前无未闭合运行时信号（N/A）。

## Completion Inputs

- Review Verdict: pass
- Completion Blockers: none

## Gate Coverage

- 自动道：10/10 AC 由 evidence record 支撑，7 条可靠档、3 条弱档，无 `reported` 档口头结论。
- 机器门禁：完整 `verify-ci.sh`（含 artifact contract、domain contract、context budget、markdown 链接、双宿主与 Pi 扩展验证、全量单测）退出码 0；状态审计在 AC8 记录时点 802 项 OK，收口自检复跑 811 项 OK、退出码 0，非 OK 行只剩两条 `UNRELEASED` 亮牌。
- 拆门禁的诚实交代：本轮**减少**了机器检查——删掉了 fold receipt 审计、`test-audit-project-state.py` 的 3 项折叠测试，`context_budget.py` 的重复真源候选表少了一项。这是机制退役的必然结果，不是放宽判定；被删的检查所守护的对象已不存在。删除过程中误删过一条与折叠无关的正面测试（`test_valid_evidence_index_and_fold_receipt_pass`），已重建为 `test_valid_evidence_index_passes`，审计测试套 22 项通过。
- 人测道：不适用。

## References Compliance

- N/A（本迭代不消费 `.ai/references/` 下的 PRD 或外部规格）。

## Remaining Risks

- **半拆状态不能拖太久**。冷启动第一读现在是过渡措辞（不再指知识文件夹、新读序还没正式定义），`.ai/project/` 只剩两个孤立文件。R2 定读序、R3 定全貌产物落点；两项若迟迟不开，这个中间态会变成事实上的常态，比拆干净或不拆都糟。这一条在 AC_LIST 的 Open Questions 里就写着，收口时仍然成立。
- **「无证据被消费」不等于「从未被消费」**。删除决策建立在缺席证据上：半年里没有任何一次决策能追溯到读知识文件夹，也没有任何工具记录过对它的读取。但没有读取记录不等于没有读取。真正的确定性数据要等 R11 的使用监视器。
- **折叠回执历史不可再机器验证**。`fold-state.json` 删掉后，哪些迭代参与过折叠、每次折叠的内容 hash 只剩 git 记录，没有工具能再校验。判断是这段历史唯一的读者就是已经一起删掉的漂移检查。
- **`invariants.md` 与 `frontier.md` 现在没有维护机制**。它们过去靠折叠仪式被顺带更新，仪式没了，在 R3 定出新落点之前，这两份处在「准确但无人负责刷新」的状态。`frontier.md` 覆盖到 MILE-0015，MILE-0016 的进展不会自动进去。
- **老项目磁盘上的空 `.ai/project/` 目录没人清**。部署侧不再生成，但存量不会自动消失，归 R15。

## Handoff / Next Step

- MILE-0016 R1 完成，可开 R2（冷启动读序改造）——R1 留下的过渡措辞就在 `context-persistence.md §6`，是 R2 的直接输入。
- R3（项目全貌产物重建）要接手 `.ai/project/` 剩下的两份文件，落点由替代品设计决定。
- 本轮改了 `templates/AGENTS.md.template`（部署入口模板），下个发布版切版时必须含 `[regen-entrypoints]`，不得记 `[no-op]`。
