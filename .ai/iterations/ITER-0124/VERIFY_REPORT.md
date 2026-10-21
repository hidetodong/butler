<!-- butler-artifact-template: 1.0.0 artifact=verify_report -->
# VERIFY_REPORT — ITER-0124

## Verification Summary

9 条验收都有通过证据。实验在仓库内夹具上打出排序没有变化，preference 的机器入口已退役，loop 保持冻结。证据工具的命令和读者没有改行为。整仓持续集成退出码 0。收口前审计退出码 0，没有 DRIFT。

## AC Status

- [x] AC1 (auto·可靠): 实验测试连续跑同一夹具，stdout JSON 稳定，含 `ranking_changed`、`order_off`、`order_on`，不写项目外的偏好目录。
- [x] AC2 (auto·可靠): 没有重排函数时 `ranking_changed` 为 false，两份顺序都等于夹具原顺序。测试发现名为 `reorder_options` 或 `reorder_by_profile` 的函数就退出码 2。
- [x] AC3 (auto·可靠): registry 不再有 `"id": "preference"`，原先指向的规则、命令、skill 和软链已删除，registry 校验仍通过，实验工具留下。true 只在测试里喂假 JSON，不恢复已删文件。
- [x] AC4 (auto·可靠): 三份人读文档里的业务工作流个数是 11，和 registry 条数一致。
- [x] AC5 (auto·可靠): 冻结段写明最终处置是保持冻结。理由是没有最后调用时间，不能当成已经证实没人用。`"id": "loop"` 和规则文件仍在。
- [x] AC6 (auto·可靠): `debt.md` 不再含「随 MILE-0016 R13 对 loop 做最终处置」。
- [x] AC7 (auto·可靠): 子命令仍是 `run`、`verify`、`check-tdd`、`archive`、`reopen`。读 `record.json` 的产品代码只留证据工具、`goal.py` 和审计。README 没有人读摘要或看板。
- [x] AC8 (auto·可靠): ITER-0123 归档校验退出码 0。`goal.py` 仍只读热区。目标与证据测试 44 passed。本机系统 `python3` 没有 pytest，所以这条测试用的是持续集成同一套锁定解释器。
- [x] AC9 (auto·可靠): `bash scripts/verify-ci.sh` 退出码 0。审计 `--allow-unreleased` 退出码 0，输出里没有 `[DRIFT]`。

## 人测道小结

- N/A（本轮无 human·待人 档 AC，人测道不适用）。

## Evidence Index

| Evidence ID | AC | 强度 | Outcome | Record |
|---|---|---|---|---|
| ac-experiment | AC1, AC2, AC3, AC4, AC5, AC6 | captured | passed | .ai/iterations/ITER-0124/evidence/ac-experiment/record.json |
| ac-registry | AC3 | captured | passed | .ai/iterations/ITER-0124/evidence/ac-registry/record.json |
| ac-archive | AC8 | captured | passed | .ai/iterations/ITER-0124/evidence/ac-archive/record.json |
| ac-pytest | AC7, AC8 | captured | passed | .ai/iterations/ITER-0124/evidence/ac-pytest/record.json |
| ac-ci | AC9 | captured | passed | .ai/iterations/ITER-0124/evidence/ac-ci/record.json |
| ac-audit | AC9 | captured | passed | .ai/iterations/ITER-0124/evidence/ac-audit/record.json |

强度写 captured：这些命令是实现者这次录下来的，没有另请复核者重跑。

## Verification Results

- `ac-experiment`：7 passed。`ac-registry`：`workflows=11 projections=49`。`ac-archive`：ITER-0123 的 7 条归档记录校验通过，含先前失败的诊断记录。`ac-pytest`：44 passed。
- `ac-ci`：`bash scripts/verify-ci.sh` 退出码 0，耗时约 199 秒。stderr 里三条 CRLF 提示是既有登录流程 PRD 备份，不是本轮改动。
- AC8 冻结文本写的是 `python3 -m pytest`。本机这条命令起不来，因为系统 Python 没有 pytest。录下的命令是 `uv run --locked --python 3.12.12 python -m pytest tools/goal-assurance/test_goal.py tools/verification-evidence/test_evidence.py -q`，和持续集成用的是同一套锁定解释器。ITER-0123 的归档校验命令与验收文本一致。
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
- Tech Plan Alignment：D1 实验不调用排序器，没有就打出排序没变。D2 按 false 退役机器入口，布尔保留，true 只留在测试。D3 三份人读文档改成 11，不新做永久扫描器。D4 证据工具和 `goal.py` 行为不改，只加锁。D5 loop 保持冻结，引擎正文不改。D6 实验工具进产品名单、持续集成和全貌。未声明 TDD。

## References Compliance

- N/A

## Remaining Risks

- 仓库外已经采集的偏好数据没有迁移。已部署项目里的旧命令要等 R15 的升级配方才清得掉。
- `project-config` 的 preference 布尔还在，但它不再启动采集。`templates/preference/` 骨架还在，开头已标明退役。
- loop 的冻结靠声明和评审自觉，没有机器检查会拦住违反它的改动。
- 给人读的文档里，工作流个数仍然没有永久扫描器。实验测试只锁住这三处现数。
- 实验只检查有没有重排函数。没有一场真实模型对话证明排序变过。`ranking_changed` 是 false。
- 本轮不切版、不提交。工作区是脏的，发布标签 `v3.6.0` 不在当前 HEAD。审计会亮这两条未发布，这是预期。

## Handoff / Next Step

- 证据归档并收口 ITER-0124。
- MILE-0016 下一段是 R14，还没开工。
