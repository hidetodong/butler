<!-- butler-artifact-template: 1.0.0 artifact=verify_report -->
# VERIFY_REPORT — ITER-0120

## Verification Summary

12 条 AC 全绿。8 份自动道 evidence 全部 `passed`。`verify-ci.sh` 退出码 0；状态审计 0 DRIFT、恰 2 条 UNRELEASED（未切版，预期内）。

候办目录现在是 `.ai/backlog/`（10 份草稿），交付树在 `.ai/deliveries/`（272 个文件，`milestones/` 子目录还在）。仓根没有 `deliveries/`，也没有软链。hook 树摘要仍是开工前的 `bd92a614f9582451ec3150d2c1113a2262bb874b97fd085adf6ad0ce7c91e56d`。

`git log --follow` 在未提交前追不到新路径，这是 git 的正常行为。index 里 ITER-0119 那份交付是 `R100`，旧路径历史还在。提交之后 follow 才能跨过这次改名。

## AC Status

- [x] AC1 (auto·可靠): `.ai/milestone-backlog/` 不存在；`.ai/backlog/` 10 份草稿文件名与基线一致；闪念口去向与待办区草稿列都是 `.ai/backlog/<候办键>.md`。
- [x] AC2 (auto·可靠): `BACKLOG_REL = ".ai/backlog"`；intake 测试 32 passed。
- [x] AC3 (auto·可靠): 审计读 `.ai/backlog/`；`test-audit-project-state.py` 22 passed。
- [x] AC4 (auto·可靠): 仓根 `deliveries/` 不存在且不是软链；`.ai/deliveries/` 272 个文件且含 `milestones/`；ITER-0119 交付在 index 里是 `R100`。
- [x] AC5 (auto·可靠): 热表与两片冷分片的 closed 交付列都以 `.ai/deliveries/` 开头，含 ITER-0001 那份日期命名文件；state-ledger `check` 退出码 0。
- [x] AC6 (auto·可靠): 部署协议、init、rule-card 改为只建 `.ai/`；`delivery-summary.md` 落点是 `.ai/deliveries/`。
- [x] AC7 (auto·可靠): 冷启动读序第 5 步写 `.ai/deliveries/`；四处投影字节一致；`context_budget.py check` 退出码 0。
- [x] AC8 (auto·可靠): hook 源文件 19 份，摘要与开工前逐字相同。
- [x] AC9 (auto·可靠): `.ai/milestones/`、`migrations/`、`docs/research/`、`docs/superpowers/` 相对 HEAD 无改动；`.ai/iterations/` 只新增本轮 `ITER-0120/` 工作文件。
- [x] AC10 (auto·可靠): `.ai/MILESTONE.md` 追加三条 2026-09-11 登记，含 `[regen-entrypoints]` / 不需要 `[sync-hooks]` / 候办可 `[rename]`、交付搬家等 R14。
- [x] AC11 (auto·可靠): `bash scripts/verify-ci.sh` 退出码 0；审计 0 DRIFT、2 UNRELEASED。
- [x] AC12 (auto·可靠): `ac-sweep.py` A 组 0 命中、B 组全在场，退出码 0。

## 人测道小结

- N/A（本轮无 human·待人 档 AC）。

## Evidence Index

| Evidence ID | AC | 强度 | Outcome | Record |
|---|---|---|---|---|
| ac-layout | AC1, AC4, AC5, AC8, AC9 | 可靠 | passed | .ai/iterations/ITER-0120/evidence/ac-layout/record.json |
| ac-intake | AC2 | 可靠 | passed | .ai/iterations/ITER-0120/evidence/ac-intake/record.json |
| ac-audit-tests | AC3 | 可靠 | passed | .ai/iterations/ITER-0120/evidence/ac-audit-tests/record.json |
| ac-docs | AC6, AC10 | 可靠 | passed | .ai/iterations/ITER-0120/evidence/ac-docs/record.json |
| ac-context-order | AC7 | 可靠 | passed | .ai/iterations/ITER-0120/evidence/ac-context-order/record.json |
| ac-sweep | AC12 | 可靠 | passed | .ai/iterations/ITER-0120/evidence/ac-sweep/record.json |
| ac-gates | AC11 | 可靠 | passed | .ai/iterations/ITER-0120/evidence/ac-gates/record.json |
| ac-ci | AC11 | 可靠 | passed | .ai/iterations/ITER-0120/evidence/ac-ci/record.json |
| review-p5-sample | AC1, AC2, AC3, AC7, AC12 | 可靠 | passed | .ai/iterations/ITER-0120/evidence/review-p5-sample/record.json |

## Verification Results

- 搬家用 `git mv`，index 里是 `R100`。未提交时 `git log --follow` 新路径无输出，旧路径仍能追到 `659b3e9`。
- ITER-0001 的交付是日期命名 `2026-04-20-chat-recap-style.md`，第一次改列漏了它，审计红了这一条后补上并重跑 `state-ledger migrate`。
- 冷启动读序多了 4 个字节（`deliveries/` → `.ai/deliveries/`），`context-budget` 测试里写死的 `order_bytes` 从 1284 改成 1288。
- 扫描把 `.ai/` 树里的子目录名 `deliveries/`（HUMAN_GUIDE / README 目录图、`mcv-deployment.md` 的 `.ai/` 子目录清单）和 hook 黑名单旧豁免、本轮四件套、冻结快照排除在外。历史迭代文件名 `ITER-0068-milestone-backlog-numbering.md` 是当时的 slug，不改。
- P5 简评复跑了 intake 测试、审计测试、路径扫描、冷启动读序投影、领域合同；全部退出码 0。没有 Must Fix。领域面只改了活指针（`domain-model.md` 一份交付路径、`README.md` / `AGENTS.md` / `rule-card.md` 的读序投影），所有者、兼容影响和迁移路径写在 TECH_PLAN D2/D4/D5，负向样例是 AC12 扫描。独立复核未跑。

## TDD Pair Status

- N/A（TECH_PLAN 未声明 TDD cycle）。

## Goal Calibration

- 当前无未闭合运行时信号（N/A）。

## Completion Inputs

- Review Verdict: pass
- Completion Blockers: none

## Gate Coverage

- `bash scripts/verify-ci.sh` 退出码 0。
- `python3 scripts/audit-project-state.py --project-root . --allow-unreleased` 退出码 0，`[DRIFT]` 0，`[UNRELEASED]` 2。
- `python3 tools/verification-evidence/evidence.py verify --source hot` 9/9 OK。
- `git diff --check` 无输出。

## References Compliance

- N/A

## Remaining Risks

- `git log --follow` 要等这次改名进提交之后才能跨路径追历史。
- 已部署项目仓根的 `deliveries/` 和 `.ai/milestone-backlog/` 本轮没搬，登记在里程碑范围演进记录里，等 R14 / R15。
- hook 黑名单里的 `deliveries/` 豁免故意留着，给还没升级的项目用。

## Handoff / Next Step

- 完成裁决通过后进入收口仪式。
