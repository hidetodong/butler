---
状态: ack-frozen
ACK 日期: 2026-07-29
---
<!-- butler-artifact-template: 1.0.0 artifact=acceptance -->
# AC_LIST — ITER-0099

身份迁移: 2026-08-01 从冲突编号 ITER-0096 迁移；原冻结范围未改变，用户已明确同意按 ITER-0099 继续验证、收口与提交。

分流: 完整（P1 见 .ai/CONCEPT.md）| 2026-07-29

## Goal

让已按 Butler 部署过的项目能正常通过 `sync_hooks` 守门：把树摘要的统计口径修正到「实际会铺到项目的文件集」，并让白名单如实覆盖各历史版本，同时保住守门器原本要防的事——真被改过的 hook 树仍须拒绝覆盖。

## In Scope

- `tools/butler-upgrade/upgrade.py` 中 `hook_source_files()` 与 `target_hook_files()` 的文件过滤口径，收敛为单一定义并排除 pytest 脚手架。
- `migrations/manifest.json` 的 `known_hook_tree_digests`：按新口径全部重算，补齐 v2.18.0 / v3.0.0 / v3.1.0，并对来源不明项作出显式决定。
- 新增机械测试：锁定「部署铺设文件集 == 摘要参与文件集」不变量，以及被改动过的 hook 树仍被拒绝。

## Out of Scope

- hook 规则自身的判定逻辑与告警文案。
- Active Profiles 段的解析宽容化（独立需求，另立迭代）。
- `[split]`、`migrate_config`、`global_install` 的既有语义。
- 任何被观测项目的文件改动；butler-radar 的实际升级执行。
- `artifacts.v1.json` 与 `concept-schema.md` 的段落定义错位（只记录）。

## Acceptance Checklist

- [ ] AC1: `hook_source_files()` 与 `target_hook_files()` 的排除规则来自同一个定义，源码中不存在第二份重复的过滤条件。
- [ ] AC2: 新口径下 `templates/hooks` 的摘要文件集不含 `conftest.py` 与 `pytest.ini`，且与部署实际铺设的文件集完全一致。
- [ ] AC3: `known_hook_tree_digests` 按新口径重算后，覆盖 v0.2.0 起每个曾改动 `templates/hooks` 的历史版本，含此前缺失的 v2.18.0 / v3.0.0 / v3.1.0。
- [ ] AC4: 本机 6 个已部署项目中，butler-radar、butler-sticker、m5-sticks3-lab、ultra-learning、utopia 五个的 hook 树摘要命中白名单；`claude-skills` 的处置有明确结论。
- [ ] AC5: 对 butler-radar 跑 `plan` 不再返回 hook 树相关 `conflict`（其余状态与冲突另行判断，不要求本 AC 覆盖）。
- [ ] AC6: 负向保障——一棵被真实改动过内容的 hook 树（任意文件内容被修改，或含项目独有文件）仍被拒绝覆盖，守门器的原有防护未被削弱。
- [ ] AC7: 新增测试可独立运行并覆盖 AC2 与 AC6；`scripts/test-butler-upgrade.py` 既有用例全绿。
- [ ] AC8: butler 仓 CI 契约检查（`scripts/verify-ci.sh` 涉及本次改动的部分）通过，无新增失败。

## Verification Method

- AC1 / AC2：读源码确认单一定义；运行新增测试比对两个函数的文件集。
- AC3 / AC4：以复算脚本遍历全部 tag 与改动过 `templates/hooks` 的 commit，生成摘要表，逐项与 manifest 对账；同一脚本扫描本机各项目 hook 树并输出命中矩阵。
- AC5：在 butler-radar 上运行 `upgrade.py plan --json`，确认错误信息不再是 hook 树失配。
- AC6：构造改动过的 hook 树 fixture，断言 `UpgradeError` 仍被抛出。
- AC7 / AC8：运行 `python3 scripts/test-butler-upgrade.py` 与新增测试，以及 CI 契约脚本；证据按 verification-evidence 记录，不以口头结论替代。

## External References

- `Coder/20_Workflow_Lifecycle/butler-upgrade.md`：升级协议与 conflict 停机口径。
- `tools/butler-upgrade/README.md`：退出码与运行区契约。
- `Coder/20_Workflow_Lifecycle/mcv-deployment.md`：部署侧 hook 注入范围，是「实际会铺哪些文件」的依据。

## Open Questions / Risks

- 来源不明的白名单项 `4ff6400939b6cabf…`：保留（加注来源待考）还是移除，需在 P3 定夺，AC3 的「覆盖」口径随该决定收敛。
- 新代码与新白名单必须同一次提交落地，中间态会维持现有的全项目失配，因此不接受分两次发布。
- `claude-skills` 只有 1 个 hook 文件，可能压根不是 Butler 部署项目；AC4 只要求结论明确，不预设它必须命中。
