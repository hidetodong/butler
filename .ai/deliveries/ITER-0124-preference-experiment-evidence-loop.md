# ITER-0124 · preference 实验、evidence 降维与 loop 处置

- 交付级别：迭代交付（小版本）
- 收口日期：2026-10-20
- 所属里程碑：MILE-0016（Butler 瘦身与重造）

## 本次交付目标

用一条可重跑的实验判定 preference 反哺会不会改变提案排序，并按结果处置。evidence 不新增人读出口。loop 保持冻结。

## 已完成内容

- 新建 `tools/preference-experiment/`。仓库内夹具上连续两次 stdout 相同，`ranking_changed` 为 false。
- preference 的机器入口已退役：registry 条目、规则、命令、skill 和软链都删了。实验工具留下。项目配置里的布尔还在，不再启动采集。
- 三份人读文档里的业务工作流个数改成 11，和 registry 一致。
- loop 的最终处置写成保持冻结。欠债里等 R13 的那句删了。命令和引擎正文没改。
- 证据工具的子命令和读者用测试锁住。上一轮归档仍能校验。

## 关键变更 / 用户可感知变化

- `python3 tools/preference-experiment/experiment.py --project-root .` 打出排序没有变化。
- `/butler:preference` 不再提供。`/butler:loop` 仍可用，只是不再演进。
- 证据记录仍给完成裁决和收口审计用，没有新增人读摘要或看板。

## 高层影响范围

- 新增：`tools/preference-experiment/`。
- 删除：preference 的规则真源、Claude 命令、Codex skill 和软链。
- 改动：registry、三份人读文档的个数、loop 冻结段、`debt.md`、证据测试。
- 不算：不新写排序器，不改 `goal.py` 和证据记录格式，不扩展升级器，不写 `migrations/v4.0.0.md`，不切版。

## 验证方式与结果摘要

9 条验收全部通过。实验测试 7 passed，目标与证据测试 44 passed，registry 校验为 11 条业务工作流。ITER-0123 归档校验退出码 0。持续集成退出码 0。收口前完成裁决 `eligible`。独立复核未开。

审计退出码 0，0 条 DRIFT，2 条未发布。本机系统 Python 没有 pytest，目标与证据测试用的是持续集成同一套锁定解释器。

## 已知剩余风险 / 延后事项

- 仓库外已经采集的偏好数据没有迁移。已部署项目里的旧命令要等 R15。
- preference 布尔还在，但不启动采集。`templates/preference/` 骨架还在，已标明退役。
- loop 的冻结没有机器门禁。没有最后调用时间不能当成已经证实没人用。
- 给人读的文档里，工作流个数仍然没有永久扫描器。
- 实验没有用一场真实模型对话证明排序变过。`ranking_changed` 是 false。
- 本轮不切版、不提交。

## 引用

- 四件套：`.ai/iterations/ITER-0124/CONCEPT.md`、`AC_LIST.md`、`TECH_PLAN.md`、`VERIFY_REPORT.md`
- 变更流：`.ai/iterations/ITER-0124/CHANGELOG.md`
- 证据：`.ai/iterations/ITER-0124/evidence/`（6 条记录）
