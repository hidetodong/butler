---
状态: ack-frozen
ACK 日期: 2026-10-19
---
<!-- butler-artifact-template: 1.0.0 artifact=acceptance -->
# AC_LIST — ITER-0124

## Goal

- 用一条可重跑的实验判定 preference 反哺会不会改变提案排序，并按结果处置。
- evidence 不新增人读出口；归档搬家和现有读者保持可用。
- loop 保持冻结。理由写进规则，等 R13 的那条欠债删掉。不删除这条命令。

## In Scope

- 仓库内夹具上的 preference 对照实验，以及和结果一致的处置。
- 锁住 `tools/verification-evidence/` 的子命令和读者；ITER-0123 的归档仍能校验。
- 更新 loop 冻结段，并删除 `debt.md` 里等 R13 处置的那句。
- 退役分支上，三份人读文档里的工作流个数改到和 registry 一致。

## Out of Scope

- 不先改 preference 的采集和蒸馏存储，也不为了做出「有影响」去新写排序器。
- 不把 C 档写成已经证实没人用，不删除 `/butler:loop`。
- 不改 `goal.py` 的完成判定，不让它改去读归档目录。
- 不给人读 evidence 摘要或看板，不改旧 record 的字段。
- 不扩展升级器的删除和移动，不写 `migrations/v4.0.0.md`，不切版。
- 不动 Decision Map 和领域合同。

## Acceptance Checklist

- [ ] AC1: 实验对同一份仓库内夹具连续跑两次，两次 stdout JSON 相同。JSON 含 `ranking_changed`（布尔）、`order_off`、`order_on`。实验不写项目外的偏好目录。
- [ ] AC2: 夹具里的通识偏好和初始选项顺序相反。仓库里没有「读画像后重排选项」的函数时，`ranking_changed` 必须是 false。测试要能拦住「先新增排序器再让结果变成 true」。
- [ ] AC3: 处置和 AC2 的结果一致。false：`workflows/registry.json` 不再有 `"id": "preference"`，这条原来指向的规则、命令、skill 文件删除，registry 校验仍通过；实验命令和夹具留下。true：这些文件都还在，规则写明触发条件是「反哺开、有监督、只参考通识层、排序变化」，同一夹具重跑仍是 true。
- [ ] AC4: 结果是 false 时，`HUMAN_GUIDE.md`、`Coder/README.md`、`docs/codex-compatibility.md` 三处工作流个数和 registry 的工作流条数一致。结果是 true 时，这三处个数保持原样。
- [ ] AC5: `Coder/55_Extension_ConvergenceLoop/convergence-loop-engine.md` 顶部写明最终处置是保持冻结，理由是 `workflow:loop` 没有最后调用时间，不能当成已经证实没人用，所以不删除。文中不再把解冻条件写成等 R13。registry 里 `"id": "loop"` 仍在，规则文件仍在。
- [ ] AC6: `.ai/debt.md` 不再含「随 MILE-0016 R13 对 loop 做最终处置」。
- [ ] AC7: `evidence.py` 的子命令仍是且仅是 `run`、`verify`、`check-tdd`、`archive`、`reopen`。除这个工具自身、`goal.py`、`scripts/audit-project-state.py` 和测试以外，没有 Python 去读证据 `record.json`。README 不新增人读摘要或看板。
- [ ] AC8: `python3 tools/verification-evidence/evidence.py verify --project-root . --iteration ITER-0123 --source archive` 退出码 0。`goal.py` 仍只从 `.ai/verification-evidence/` 读热区。`python3 -m pytest tools/goal-assurance/test_goal.py tools/verification-evidence/test_evidence.py -q` 退出码 0。
- [ ] AC9: `bash scripts/verify-ci.sh` 退出码 0。`python3 scripts/audit-project-state.py --project-root . --allow-unreleased` 退出码 0，输出里没有 `[DRIFT]`。

## Verification Method

- AC1–AC3: 实验测试用仓库内夹具重跑，并检查 preference 入口是留下还是删掉。
- AC4: 数 registry 工作流条数，再对三份人读文档。
- AC5–AC6: 读冻结段、registry 和 `debt.md`。
- AC7: 枚举子命令，并扫描 Python 里谁读 `record.json`。
- AC8: 对 ITER-0123 归档跑 verify；goal 与 evidence 的既有测试。
- AC9: 取持续集成和审计的退出码，并检索 `[DRIFT]`。

## External References

- N/A

## Open Questions / Risks

- 反哺目前只写在规则里。按 AC2，实验会得到排序没变，preference 的机器入口会被退役。这是这条验收的结果，不是另开一轮再判。
- 归档搬家被收口仪式和审计使用，本轮不删。旧 record 字段也不改，避免已收口迭代的校验变红。
- C 档不是没人用，所以 loop 保持冻结。本轮不切版。
