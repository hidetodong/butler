<!-- butler-artifact-template: 1.0.0 artifact=verify_report -->
# VERIFY_REPORT — ITER-0125

## Verification Summary

7 条验收都有通过证据。升级器能删除点名的文件或目录，也能把仓根路径移进 `.ai/`。冲突时停下，失败能退回。历史 `[split]` 和 `--split` 保持原样。仓库里没有 `migrations/v4.0.0.md`，`VERSION` 仍是 `3.6.0`。升级器测试 31 项通过。整仓持续集成退出码 0。收口前审计退出码 0，没有 DRIFT。

## AC Status

- [x] AC1 (auto·可靠): `migration-schema.md` §4 在 `[rename]` 后写了 `[delete]` 和 `[move]`。两段都写明起始态、重复执行的结果，以及冲突时停下、不覆盖。同节仍保留 `[split]` 的定义。
- [x] AC2 (auto·可靠): `upgrade.py` 认识 `delete` 和 `move`。现有 `migrations/manifest.json` 仍能通过校验。`apply` 不带 `--split` 时仍拒绝执行。未知动作类型仍被拒绝。
- [x] AC3 (auto·可靠): 删除能去掉动作点名的文件或目录，目录连同里面的文件一起去掉。目标已经不存在时再跑，退出码 0。`..`、绝对路径，以及 `.ai/` 下的 `iterations`、`milestones`、`references`、`verification-evidence`、`butler-upgrade` 被拒绝，动手前的文件还在。路径正好是 `.ai` 时也拒绝。
- [x] AC4 (auto·可靠): 移动能把仓根上的文件或目录搬到 `.ai/` 下的非保护路径，内容保持不变，源路径消失。源和目标都已存在时退出码非 0，两边都不变。源和目标都不存在时退出码非 0。源已经不在、目标已经在时再跑，退出码 0，不另造一份，也不比较目标现有字节。
- [x] AC5 (auto·可靠): 删除或移动一个含文件的目录时，用 `BUTLER_UPGRADE_FAIL_AFTER` 注入写到一半失败。失败退出码是 5。临时项目里的目录和文件回到动手前。摘要忽略 `.ai/butler-upgrade`。
- [x] AC6 (auto·可靠): 仓库里没有 `migrations/v4.0.0.md`。`VERSION` 仍是 `3.6.0`。
- [x] AC7 (auto·可靠): `python3 scripts/test-butler-upgrade.py` 退出码 0。`bash scripts/verify-ci.sh` 退出码 0。`python3 scripts/audit-project-state.py --project-root . --allow-unreleased` 退出码 0，输出里没有 `[DRIFT]`。

## 人测道小结

- N/A（本轮无 human·待人 档 AC，人测道不适用）。

## Evidence Index

| Evidence ID | AC | 强度 | Outcome | Record |
|---|---|---|---|---|
| ac-upgrade | AC1, AC2, AC3, AC4, AC5, AC6, AC7 | captured | passed | .ai/iterations/ITER-0125/evidence/ac-upgrade/record.json |
| ac-ci | AC7 | captured | passed | .ai/iterations/ITER-0125/evidence/ac-ci/record.json |
| ac-audit | AC7 | captured | passed | .ai/iterations/ITER-0125/evidence/ac-audit/record.json |

强度写 captured：这些命令是实现者这次录下来的，没有另请复核者重跑。

## Verification Results

- `ac-upgrade`：`python3 scripts/test-butler-upgrade.py` 退出码 0，31 项通过，耗时约 1.2 秒。标准错误里的拒绝行是测试故意点到非法路径和冲突起始态，用例本身通过。
- `ac-ci`：`bash scripts/verify-ci.sh` 退出码 0，耗时约 33 秒。其中 pytest 211 passed，升级器测试再次 31 passed。stderr 里三条 CRLF 提示是既有登录流程 PRD 备份。Pi 扩展的 tsc 缺类型提示也是既有的，脚本按既有口径跳过，不是本轮改动。
- `ac-audit`：`python3 scripts/audit-project-state.py --project-root . --allow-unreleased` 退出码 0，输出里没有 `[DRIFT]`。两条未发布是工作树有未提交改动，以及标签 `v3.6.0` 不在当前 HEAD。本轮不提交、不切版，这两条是预期。
- 源路径和目标路径互相包含时，实现也会拒绝，退出码 2，一个字节都不写。已确认的方案正文没写这条。补上是因为把目录搬进自己里面，会删掉刚写好的那份。测试 `test_manifest_accepts_delete_and_move_and_rejects_illegal_paths` 锁着 `.ai/box` 到 `.ai/box/nested`。
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
- Tech Plan Alignment：D1 补上 `[delete]` 和 `[move]`，`[split]` 整段保留。D2 路径允许仓根来源，拒绝 `.ai` 本身和五个受保护子目录。D3 按起始态执行，幂等移动不比较目标字节。D4 目录失败能退回，退出码 5。未声明 TDD。不写 v4 配方，不改 `VERSION`，不改 `--split`。

## References Compliance

- N/A

## Remaining Risks

- 动作写得出来了，已部署项目不会因此被清理。没有 `migrations/v4.0.0.md`。别人硬盘上的旧收件箱和 `origin/` 要等 R15。
- 源和目标路径重叠时的拒绝，写在代码和测试里，没有回写进已确认的方案正文。回写会把方案裁决打回草稿，本轮不回写。
- 幂等移动只看「源已经不在、目标已经在」，不核对目标内容是不是当初搬过去的那一份。
- 测试跑在临时目录上，没有在真实已部署项目上执行升级。
- 本轮不切版、不提交。工作区是脏的，发布标签 `v3.6.0` 不在当前 HEAD。审计会亮这两条未发布，这是预期。

## Handoff / Next Step

- 证据归档并收口 ITER-0125。
- MILE-0016 下一段是 R15，还没开工。
