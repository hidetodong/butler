<!-- butler-artifact-template: 1.0.0 artifact=verify_report -->
# VERIFY_REPORT — ITER-0126

## Verification Summary

9 条验收都有通过证据。`migrations/v4.0.0.md` 和清单里 3.6.0 到 4.0.0 那一节已经写上。临时项目上，这条配方能删掉 `.ai/project/` 和 `.ai/PROJECT.md`，并把仓根 `deliveries/` 挪到 `.ai/deliveries/`。旧收件箱和仓根 `origin/` 会在写文件前停下。`VERSION` 仍是 `3.6.0`。升级器测试 36 项通过。整仓持续集成退出码 0。收口前审计退出码 0，没有 DRIFT。

## AC Status

- [x] AC1 (auto·可靠): 清单有 source 3.6.0、target 4.0.0、recipe v4.0.0.md，配方文件在。清单能通过校验。`VERSION` 仍是 `3.6.0`。用本仓库做计划时，没有 `4.0.0/` 开头的动作。
- [x] AC2 (auto·可靠): 这一节含 global_install、两次删除、一次移动、migrate_config、regen_entrypoints、sync_hooks、restamp。`[split]` 定义还在，仍写着知识文件夹和退役说明。
- [x] AC3 (auto·可靠): 临时项目经过版本写成 4.0.0 的临时 butler 根之后，`.ai/project/` 和 `.ai/PROJECT.md` 消失，`deliveries/` 的字节出现在 `.ai/deliveries/`，源路径消失。入口用户区原文还在，版本戳是 4.0.0，hook 与配方来源一致。再跑一次退出码 0，不另造一份。这次没有调用 `scripts/setup.sh`。
- [x] AC4 (auto·可靠): 旧收件箱（正文有 `butler-inbox:managed`）或仓根 `origin/` 让升级退出码非 0，这两处和 `.ai/project/`、`.ai/PROJECT.md`、`deliveries/` 都不变。标题是 `## 闪念` 且没有旧标记的收件箱不会让升级停下，字节保持原样。
- [x] AC5 (auto·可靠): 仓根 `deliveries/` 和 `.ai/deliveries/` 都在时退出码非 0，两边字节都不变。
- [x] AC6 (auto·可靠): `apply` 不带 `--split` 不再因缺参数被拒绝。`--split defer` 和 `--split now` 仍被接受。只有半成形的 `.ai/project/` 时，不再因形状检查停下。
- [x] AC7 (auto·可靠): 字段表、默认值和规则卡不再把 preference 当活字段。旧配置经过这条升级后只少这一键，另外三个字段保持原值。没有这一键的配置仍能读。实验工具还在。没有名为 `reorder_options` 或 `reorder_by_profile` 的函数。
- [x] AC8 (auto·可靠): `.ai/debt.md` 不再写还没有 `migrations/v4.0.0.md`，也不再写升级不会碰旧收件箱和 `origin/`。人还得自己处理的句子留着。「从未在真实已部署项目上跑过」留着。
- [x] AC9 (auto·可靠): `python3 scripts/test-butler-upgrade.py` 退出码 0。`bash scripts/verify-ci.sh` 退出码 0。`python3 scripts/audit-project-state.py --project-root . --allow-unreleased` 退出码 0，输出里没有 `[DRIFT]`。

## 人测道小结

- N/A（本轮无 human·待人 档 AC，人测道不适用）。

## Evidence Index

| Evidence ID | AC | 强度 | Outcome | Record |
|---|---|---|---|---|
| ac-upgrade | AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9 | captured | passed | .ai/iterations/ITER-0126/evidence/ac-upgrade/record.json |
| ac-ci | AC9 | captured | passed | .ai/iterations/ITER-0126/evidence/ac-ci/record.json |
| ac-audit | AC9 | captured | passed | .ai/iterations/ITER-0126/evidence/ac-audit/record.json |

强度写 captured：这些命令是实现者这次录下来的，没有另请复核者重跑。

## Verification Results

- `ac-upgrade`：`python3 scripts/test-butler-upgrade.py` 退出码 0，36 项通过。标准错误里的拒绝行是测试故意点到非法路径和冲突起始态，用例本身通过。
- `ac-ci`：`bash scripts/verify-ci.sh` 退出码 0，耗时约 37 秒。其中 pytest 211 passed，升级器测试再次 36 passed，项目配置测试 32 passed。stderr 里三条 CRLF 提示是既有登录流程 PRD 备份。Pi 扩展的 tsc 缺类型提示也是既有的，脚本按既有口径跳过。
- `ac-audit`：`python3 scripts/audit-project-state.py --project-root . --allow-unreleased` 退出码 0，输出里没有 `[DRIFT]`。两条未发布是工作树有未提交改动，以及标签 `v3.6.0` 不在当前 HEAD。本轮不提交、不切版，这两条是预期。
- 仓根 `deliveries/` 和 `.ai/deliveries/` 都不存在时，整次 v4 计划会停。这是上一轮搬移动作的既有规则：两边都没有就算冲突。本轮按已确认方案沿用，没有改成「都没有也算成功」。
- 从还含历史 `[split]` 的老版本升上来，并且 `.ai/PROJECT.md` 还在时，不再停下来问拆不拆。队列含 4.0.0 时，后面的删除会删掉这个文件。这是冻结验收时接受的结果。
- P5 简评没有 Must Fix。独立复核未开（项目配置 `independent_review` 为 false）。

## TDD Pair Status

- N/A（TECH_PLAN 未声明 TDD cycle）。

## Goal Calibration

- 当前无未闭合运行时信号（N/A）。

## Completion Inputs

- Review Verdict: pass
- Completion Blockers: none

## Gate Coverage

- 通用质量门禁：`bash scripts/verify-ci.sh` 退出码 0。`python3 scripts/audit-project-state.py --project-root . --allow-unreleased` 退出码 0，没有 `[DRIFT]`。
- Workspace Scope：N/A（本轮 AC 没有 `prd_refs`）。
- Tech Plan Alignment：D1 写了配方和清单节，八个动作顺序与方案一致，不新造动作类型。D2 的门只在队列含 4.0.0 时生效，旧标记和仓根 origin 在写入前停下。D3 去掉形状检查整段，`--split` 可省略，历史 `[split]` 定义保留。D4 卸掉 preference，读时容忍布尔旧键且不改文件，只在 4.0.0 的迁移写回时从磁盘去掉。D5 的临时 butler 根使用清单里的真实动作。D6 只改 debt.md 里已经不真的句子。未声明 TDD。不改 `VERSION`，不收口里程碑。
- References Compliance：N/A

## References Compliance

- N/A

## Remaining Risks

- 这条配方还没有在真实已部署项目上跑过。`.ai/debt.md` 里这句话留着。别人硬盘上的旧收件箱和 `origin/` 遇到就停，仍要人自己处理。
- 仓根 `deliveries/` 和 `.ai/deliveries/` 都不存在时，整次升级会停。已经只有 `.ai/deliveries/` 的项目可以过。从没建过这两个目录的项目，这条配方会整单停下。要放行得改方案。
- 幂等移动只看「源已经不在、目标已经在」，不核对目标内容是不是当初搬过去的那一份。
- 本仓库自己的 `.ai/butler.config.json` 里 `preference` 还在。当前版本读的时候丢掉这一键，不改文件。要等版本切到 4.0.0 之后的升级，才会从磁盘去掉。本轮不升级这个仓库。
- 源和目标路径重叠时的拒绝，仍只写在代码和测试里，没有回写进上一轮已确认的方案正文。本轮不回写。
- 本轮不切版、不提交。工作区是脏的，发布标签 `v3.6.0` 不在当前 HEAD。审计会亮这两条未发布，这是预期。

## Handoff / Next Step

- 证据归档并收口 ITER-0126。
- MILE-0016 仍开着。切版留在里程碑收口。
