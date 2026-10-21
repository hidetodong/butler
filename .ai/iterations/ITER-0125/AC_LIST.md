---
状态: ack-frozen
ACK 日期: 2026-10-20
---
<!-- butler-artifact-template: 1.0.0 artifact=acceptance -->
# AC_LIST — ITER-0125

## Goal

- 升级器能表达删除，以及把仓根路径移进 `.ai/`。
- 两类动作都能重复跑、冲突时停下、失败能退回。
- 历史 `[split]` 和 `--split` 保持原样。本轮不写 v4.0.0 配方，不切版。

## In Scope

- `Coder/20_Workflow_Lifecycle/migration-schema.md` §4 的 `[delete]` 与 `[move]`。
- `tools/butler-upgrade/upgrade.py` 的动作表、路径校验，以及这两类动作的执行。
- `scripts/test-butler-upgrade.py` 里用临时目录覆盖的行为。

## Out of Scope

- 不写 `migrations/v4.0.0.md`，不改 `VERSION`。
- 不在真实已部署项目上跑升级，不删除别人盘上的 `origin/` 或旧收件箱，不搬 `deliveries/`。
- 不改 `--split` 必填，不删历史 `[split]` 定义，不改其他已有动作的行为。
- 不改 preference、loop 和 evidence。

## Acceptance Checklist

- [ ] AC1: `migration-schema.md` §4 有 `[delete]` 和 `[move]`。两段都写明起始态、重复执行的结果，以及冲突时停下、不覆盖。同节仍保留 `[split]` 的定义。
- [ ] AC2: `upgrade.py` 认识 `delete` 和 `move`。现有 `migrations/manifest.json` 仍能通过校验。`apply` 不带 `--split` 时仍拒绝执行。未知动作类型仍被拒绝。
- [ ] AC3: 删除能去掉动作点名的文件或目录；目录连同里面的文件一起去掉。目标已经不存在时再跑，退出码 0，不报错。`..`、绝对路径，以及 `.ai/` 下的 `iterations`、`milestones`、`references`、`verification-evidence`、`butler-upgrade` 被拒绝，动手前的文件还在。
- [ ] AC4: 移动能把仓根上的文件或目录搬到 `.ai/` 下的非保护路径，内容保持不变，源路径消失。源和目标都已存在时退出码非 0，两边都不变。源和目标都不存在时退出码非 0。源已经不在、目标已经在时再跑，退出码 0，不另造一份。
- [ ] AC5: 删除或移动一个含文件的目录时，用现有的失败注入让它写到一半失败。失败后这个临时项目里的目录和文件回到动手前。
- [ ] AC6: 仓库里没有 `migrations/v4.0.0.md`。`VERSION` 仍是 `3.6.0`。
- [ ] AC7: `python3 scripts/test-butler-upgrade.py` 退出码 0。`bash scripts/verify-ci.sh` 退出码 0。`python3 scripts/audit-project-state.py --project-root . --allow-unreleased` 退出码 0，输出里没有 `[DRIFT]`。

## Verification Method

- AC1: 读 `migration-schema.md` §4。
- AC2–AC5: 在 `scripts/test-butler-upgrade.py` 里用临时目录跑 `upgrade.py`，不碰本仓库自己的 `.ai/`。
- AC6: 看 `migrations/v4.0.0.md` 不存在，并读 `VERSION`。
- AC7: 跑升级器测试、持续集成和审计，审计输出里检索 `[DRIFT]`。

## External References

- N/A

## Open Questions / Risks

- 本轮只让动作写得出来。已部署项目要等 R15 的配方才会真的删除或移动。
