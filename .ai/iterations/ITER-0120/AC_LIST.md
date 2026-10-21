---
状态: ack-frozen
ACK 日期: 2026-09-11
---
<!-- butler-artifact-template: 1.0.0 artifact=acceptance -->
# AC_LIST — ITER-0120

## Goal

- 候办草稿和交付总结都住进 `.ai/`：候办目录改名 `.ai/backlog/`，仓根 `deliveries/` 搬到 `.ai/deliveries/`。活着的规则、工具、测试、台账都指新路径；冻结快照不改写。Butler 仓自己一次搬干净，已部署项目的搬家只登记给 R14 / R15。

## In Scope

- `git mv` `.ai/milestone-backlog/` → `.ai/backlog/`，10 份草稿文件名不变；同步闪念口去向、待办区索引、`tools/intake/`、审计与相关测试。
- `git mv` 仓根 `deliveries/` → `.ai/deliveries/`，保留 `milestones/` 子目录；同步规则、脚本、工具、测试、台账交付列（热表 + 冷分片）、CHANGELOG 里找文件的链接、冷启动读序投影。
- 部署协议与 init 改为只建 `.ai/`；`.ai/backlog/` 与 `.ai/deliveries/` 按需产生。
- 冷启动一致性自检第 3 条改为按台账交付列相对项目根解析。
- 按 `migration-schema.md §5` 把已部署项目影响写进 `.ai/MILESTONE.md` 范围演进记录。
- 可重跑扫描 + `.ai/OVERVIEW.md` 重算 + CI / 审计全绿。

## Out of Scope

- 不留仓根 `deliveries` 兼容软链，不把 `milestones/` 子目录拍平，不新分迭代子目录。
- 不改写 `.ai/iterations/`、`.ai/milestones/` 收口快照，不改已发布 `migrations/`，不改 `docs/research/` 与 `docs/superpowers/`，不改交付正文内部的历史叙述。
- 不改 `templates/hooks/` 下任何进摘要的文件（含 `GATED_BLACKLIST` 里的 `deliveries/` 豁免）。
- 不给升级器新增删除 / 移动动作（归 R14）；不写 `migrations/v4.0.0.md`、不在真实已部署项目上跑升级（归 R15）。
- 不迁 `.ai/project/workspaces.md`，不切版、不发布、不提交。

## Acceptance Checklist

- [ ] AC1: `.ai/milestone-backlog/` 不存在；`.ai/backlog/` 存在，且其中 `.md` 文件名集合等于开工前那 10 个候办键。`.ai/INBOX.md` 已孵化那一行的去向、`.ai/MILESTONES.md` 待办区「草稿」列，全部是 `.ai/backlog/<候办键>.md`。
- [ ] AC2: `tools/intake/intake.py` 的孵化区相对路径是 `.ai/backlog`；`tools/intake/tests/` 与 `tools/explore-dogfood/` 夹具不再出现 `milestone-backlog`。`python -m unittest discover -s tools/intake/tests -t .` 退出码 0。
- [ ] AC3: `scripts/audit-project-state.py` 校验候办草稿时读 `.ai/backlog/`；`scripts/test-audit-project-state.py` 的夹具与期望路径同步。该测试文件单独跑退出码 0。
- [ ] AC4: 仓根 `deliveries/` 不存在（不是软链、不是空目录）；`.ai/deliveries/` 存在，含 `milestones/` 子目录，文件数 272。搬运用 `git mv`，`git log --follow -- .ai/deliveries/ITER-0119-retire-old-inbox-chain.md` 能追到搬家前的提交。
- [ ] AC5: `.ai/ITERATIONS.md` 热表、`.ai/MILESTONES.md` 正式表、`.ai/history/iterations/` 两片冷分片里，所有 `closed` 行的「交付」列都以 `.ai/deliveries/` 开头，且该文件在磁盘上存在。改完冷分片后 `python3 tools/state-ledger/state_ledger.py check --project-root .` 退出码 0。
- [ ] AC6: 部署与收口真源改写完整且互不矛盾——`mcv-deployment.md`、`delivery-summary.md`、`iteration-schema.md`、`milestone-schema.md`、`lifecycle.md`、`.claude/commands/butler/init.md`、`plugins/butler/skills/butler-init/SKILL.md`、`templates/rule-card.md` 都不再把仓根 `deliveries/` 写成现行落点；部署只建 `.ai/`，并写明 `.ai/backlog/` 与 `.ai/deliveries/` 按需产生。
- [ ] AC7: 冷启动读序真源 `context-persistence.md §6` 第 5 步把「历史归档」写成 `.ai/deliveries/`；第 3 条自检改成按台账交付列相对项目根解析，不再写死 `deliveries/<链接>`。`Coder/README.md`、`AGENTS.md`、`CLAUDE.md`、两份入口模板里的读序投影与真源一致。
- [ ] AC8: `templates/hooks/` 下进摘要的文件集与开工前逐字节相同（用升级器现有的 `hook_source_files` + `tree_digest` 口径）。`GATED_BLACKLIST` 仍含 `deliveries/`。
- [ ] AC9: 历史快照与已发布配方未被改写——`.ai/iterations/`、`.ai/milestones/`、`migrations/`、`docs/research/`、`docs/superpowers/` 相对开工前 `git diff` 为空。
- [ ] AC10: `.ai/MILESTONE.md` 范围演进记录追加本轮判定：①活指针改、冻结快照不改；②hook 黑名单故意不动及理由；③按 `migration-schema.md §5`——改了 rule-card 与两份入口模板，v4.0.0 必须含 `[regen-entrypoints]`；未改 hook 树，不需要 `[sync-hooks]`；候办改名可走现有 `[rename]`，仓根交付搬家等 R14 的移动动作，配方正文归 R15。
- [ ] AC11: `.ai/OVERVIEW.md` 由 `--write` 重算且 `--check` 退出码 0。`bash scripts/verify-ci.sh` 退出码 0；`python3 scripts/audit-project-state.py --project-root . --allow-unreleased` 退出码 0，`[DRIFT]` 为 0。
- [ ] AC12: 可重跑扫描两组均成立——A 组活跃面零命中 `milestone-backlog` 与仓根路径字样 `deliveries/`（排除面必须在验证报告里逐份列明，且只允许是冻结快照、已发布配方、交付正文内部叙述、CHANGELOG 里「当时做了什么」的句子、hook 黑名单旧豁免、本迭代四件套）；B 组在场断言：`.ai/backlog/` 10 份草稿、intake 常量、审计读新目录、台账交付列前缀、`delivery-summary.md` 新落点、部署只建 `.ai/`、读序投影含 `.ai/deliveries/`。

## Verification Method

- AC1: `test ! -e .ai/milestone-backlog`；`ls .ai/backlog/*.md` 文件名集合与开工前清单比对；`grep` 断言 INBOX 去向与待办区草稿列。
- AC2 / AC3: `grep` 断言常量与夹具；unittest 取退出码。
- AC4: `test ! -e deliveries` 且 `test ! -L deliveries`；`find .ai/deliveries -type f | wc -l` 为 272；`git log --follow` 至少跨过搬家提交。
- AC5: 解析热表 + 两片冷分片的交付列，逐条 `test -f`；state-ledger `check` 取退出码。
- AC6 / AC7: `grep -qF` 断言新措辞在场、旧落点在这些活文件中消失；读序投影用现有同步检查（与 R2/R3 同一口径）取退出码。
- AC8: 升级器 `hook_source_files` + `tree_digest` 与开工前比对。
- AC9: `git diff -- .ai/iterations .ai/milestones migrations docs/research docs/superpowers` 为空。
- AC10: `grep -qF` 断言范围演进记录里五条判定都在。
- AC11: 三条命令各取退出码并留完整输出。
- AC12: 本轮新增扫描脚本，模式串用变量拼接避免自命中；排除面写进验证报告。

## External References

- 本迭代无 `.ai/references/` 外部参考资料。
- 内部依赖：`Coder/20_Workflow_Lifecycle/migration-schema.md §4 / §5`（typed 标签与领域变更判定）、`Coder/20_Workflow_Lifecycle/mcv-deployment.md §2`（部署建哪些目录）、`Coder/20_Workflow_Lifecycle/delivery-summary.md`（交付落点）、`Coder/40_Context_Management/intake-schema.md`（孵化区路径）、`Coder/40_Context_Management/context-persistence.md §6`（冷启动读序与自检）、`tools/butler-upgrade/upgrade.py`（hook 树摘要口径）。

## Open Questions / Risks

- **风险 · 冷分片漏改会让审计一次红一百来条。** AC5 把热表和两片冷分片绑在一起验收，改完必须重算 state-ledger 回执。
- **风险 · CHANGELOG 里「叙述」和「找文件」混在同一段。** 扫 `deliveries/` 时不能把「当时写了 deliveries/」的历史句子当成漏改；验证报告必须能指出排除的是哪一类。
- **风险 · 已部署项目在 R15 之前仓根仍有 `deliveries/`。** 本轮不动 hook 黑名单，避免把别人还在用的豁免提前删掉。
- **风险 · 搬家文件多，回滚靠 git。** 全部改动停在工作树、本轮不提交；最坏情况可整体退回，但台账和冷分片是本轮新写的，退回会丢掉 ITER-0120 记录。
