# MILE-0016 · Butler 瘦身与重造：砍 fold 与死码、重造 inbox、装监视器

- 交付级别：里程碑交付（大版本）
- 收口日期：2026-10-21
- 含迭代：ITER-0112 至 ITER-0126
- 版本：4.0.0（MAJOR）

## 本次交付目标

Butler 到 v3.6.0 时，规则、工具和命令只加不减。知识文件夹靠折叠自转，项目全貌会悄悄过期，闪念没有一个三秒能记下来的入口，也没有使用记录能说明哪条命令真的被用过。

这一版做三件事：先拆掉已经证明维护不住的机构，再补上闪念口、拦截日志和仓根文件逃生舱，最后装上本地使用记录，让以后的淘汰有数可查。收口时把版本切到 4.0.0。这是破坏性版本：已部署项目要走 `migrations/v4.0.0.md`，没有兼容期软链。

## 已完成内容

- **止血**（R1–R5）：删掉 `.ai/project/` 里靠折叠维护的产物、`fold-state.json`、knowledge-fold 与 drift-check；冷启动改读欠债、交接和双台账；项目全貌改为可重算的 `.ai/OVERVIEW.md`，不变量和欠债分开存放；`/butler:progress` 整条链删除；`/butler:loop` 保留可用，但停止演进。
- **重造**（R6–R10）：闪念口、孵化区和执行分流定成新契约；`/butler:inbox` 能记下一条闪念并孵化；旧 inbox 扫描链和 `origin/` 的工具支持退役；候办目录改名为 `.ai/backlog/`，交付从仓库根挪进 `.ai/deliveries/`；hook 拦截写入 `.ai/.hook-blocks.log`，仓库根的说明文件在没有进行中的迭代时也可以直接改。
- **治根**（R11–R15）：命令行入口记下最后调用时间；90 天报告按调用时间分档，不自动淘汰；偏好反哺实验判定排序没有变化，机器入口退役，本机偏好目录和模板骨架保留；升级器新增删除和移动；`migrations/v4.0.0.md` 写好，并在临时项目上跑通。
- **切版**：`VERSION`、更新日志、README 版本徽章和 Codex 插件版本对齐到 4.0.0。没有推送。

## 关键变更 / 用户可感知变化

- 冷启动不再读项目知识文件夹。人要看的全貌在 `.ai/OVERVIEW.md`，欠着的账在 `.ai/debt.md`。
- `/butler:progress` 没有了。`/butler:preference` 的机器入口没有了。`/butler:loop` 还在，但是冻结的，没有最后调用时间，不能当成已经证实没人用。
- 记一句话走 `/butler:inbox`。旧格式收件箱和仓库根的 `origin/` 不会被升级器删掉；升到 4.0.0 时遇到它们会在写入前停下。
- 给人看的交付总结改在 `.ai/deliveries/`。仓库根不再放 `deliveries/`。
- 一个 3.6.0 的项目拿本仓库做升级计划时，会选中 4.0.0 的删除、搬家、配置、入口、hook 和版本戳。本仓库自己没有对自己执行这次升级。

## 高层影响范围

- 冷启动读序、迭代与里程碑收口仪式、命令注册表、hook、`.ai/` 布局、升级器动作和 v4.0.0 配方。
- 没动的：P1 到 P5 的阶段顺序，MILE-0014 的决策地图，MILE-0015 的领域合同工具。
- 仓库里的 `.ai/butler.config.json` 仍保留 `preference: true`。读取时会丢掉这一键，写回要等一次真正的 4.0.0 升级。这次收口没有改那个文件。

## 拆分路线图回填

| 路线 | 交付切片 | 承接迭代 | 结果 |
|---|---|---|---|
| R1 | 退役折叠机制和靠它维护的知识文件夹产物 | [ITER-0112](../ITER-0112-retire-project-knowledge-folder.md) | closed |
| R2 | 冷启动改读欠债、交接和双台账 | [ITER-0113](../ITER-0113-cold-start-read-order.md) | closed |
| R3 | 项目全貌改为生成加手写理由，不再靠折叠重评 | [ITER-0114](../ITER-0114-project-overview-rebuild.md) | closed |
| R4 | 删除 `/butler:progress` 整条链 | [ITER-0115](../ITER-0115-retire-butler-progress.md) | closed |
| R5 | `/butler:loop` 冻结，并撤掉升级器重写候办 | [ITER-0116](../ITER-0116-loop-freeze-backlog-withdrawal.md) | closed |
| R6 | 闪念、孵化、执行三层契约 | [ITER-0117](../ITER-0117-intake-three-layer-contract.md) | closed |
| R7 | `/butler:inbox` 命令和工具，并跑通记一条闪念 | [ITER-0118](../ITER-0118-inbox-command-and-tool.md) | closed |
| R8 | 退役旧 inbox 扫描链 | [ITER-0119](../ITER-0119-retire-old-inbox-chain.md) | closed |
| R9 | 候办改名，交付挪进 `.ai/deliveries/` | [ITER-0120](../ITER-0120-layout-backlog-deliveries.md) | closed |
| R10 | hook 拦截日志和仓根文件逃生舱 | [ITER-0121](../ITER-0121-hook-block-log-meta-escape.md) | closed |
| R11 | 命令行入口记录最后调用时间 | [ITER-0122](../ITER-0122-usage-cli-last-used.md) | closed |
| R12 | 90 天使用报告，只分档，不自动淘汰 | [ITER-0123](../ITER-0123-usage-report-90d.md) | closed |
| R13 | 偏好反哺实验：排序没变，机器入口退役，loop 继续冻结 | [ITER-0124](../ITER-0124-preference-experiment-evidence-loop.md) | closed |
| R14 | 升级器新增删除和移动 | [ITER-0125](../ITER-0125-upgrade-delete-move.md) | closed |
| R15 | 写出 v4.0.0 配方，并在临时项目上跑通 | [ITER-0126](../ITER-0126-v4-upgrade-recipe.md) | closed |

## 验证方式与结果摘要

- 十五条路线全部 closed。各迭代的归档、交付和证据留在 `.ai/iterations/ITER-NNNN/` 与 `.ai/deliveries/`，这里不嵌原文。ITER-0126 的证据在 `.ai/iterations/ITER-0126/evidence/`。
- 切版提交前，`python3 scripts/test-butler-upgrade.py` 36 项通过；`bash scripts/verify-ci.sh` 退出码 0，其中 pytest 211 项通过。Pi 扩展的类型声明警告是原有的，这轮 CI 仍以退出码 0 结束。
- 没有做换上下文的独立复核。

## 已知剩余风险 / 延后事项

- **真实已部署项目的升级一次都没跑过。** v4.0.0 配方只在临时项目上证明过。已部署项目磁盘上的旧收件箱、仓库根 `origin/`、空知识目录，都还在原地。这次收口没有把它们清掉。
- **旧收件箱和仓库根 `origin/` 会让整次升级在写入前停下。** 配方不删这两处，要人自己处理。
- **仓库根 `deliveries/` 和 `.ai/deliveries/` 都不存在时，整次 4.0.0 升级会停下，包括前面的删除。** 只有 `.ai/deliveries/` 时，搬家这一步视为已经完成。两边都在则停下，不覆盖。
- **本仓库的配置文件仍写着 `preference: true`。** 不在这次收口里改写。`templates/preference/` 和本机 `~/.butler/preferences/` 也保留。
- **`/butler:inbox` 的提升和开迭代两条出口，在本仓库当时有进行中的里程碑，只在临时项目上跑过。** 真实使用还没发生。
- **使用报告只按最后调用时间分档。** 没有调用记录不等于已经证实没人用，所以 loop 不删。
- 收件箱里 2026-10-10 的两条缺陷没有在这次收口里处理：没有里程碑行时领不了第一个迭代；证据工具多次传入验收编号时只保留最后一个。

## 引用（只链接，不嵌入）

- `.ai/milestones/MILE-0016/MILESTONE.md`
- `.ai/deliveries/ITER-0112-retire-project-knowledge-folder.md`
- `.ai/deliveries/ITER-0113-cold-start-read-order.md`
- `.ai/deliveries/ITER-0114-project-overview-rebuild.md`
- `.ai/deliveries/ITER-0115-retire-butler-progress.md`
- `.ai/deliveries/ITER-0116-loop-freeze-backlog-withdrawal.md`
- `.ai/deliveries/ITER-0117-intake-three-layer-contract.md`
- `.ai/deliveries/ITER-0118-inbox-command-and-tool.md`
- `.ai/deliveries/ITER-0119-retire-old-inbox-chain.md`
- `.ai/deliveries/ITER-0120-layout-backlog-deliveries.md`
- `.ai/deliveries/ITER-0121-hook-block-log-meta-escape.md`
- `.ai/deliveries/ITER-0122-usage-cli-last-used.md`
- `.ai/deliveries/ITER-0123-usage-report-90d.md`
- `.ai/deliveries/ITER-0124-preference-experiment-evidence-loop.md`
- `.ai/deliveries/ITER-0125-upgrade-delete-move.md`
- `.ai/deliveries/ITER-0126-v4-upgrade-recipe.md`
- `migrations/v4.0.0.md`
