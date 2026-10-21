# ITER-0125 · 升级器补上删除与移动

- 交付级别：迭代交付（小版本）
- 收口日期：2026-10-21
- 所属里程碑：MILE-0016（Butler 瘦身与重造）

## 本次交付目标

让升级器写得出删除，以及把仓根路径移进 `.ai/`。冲突时停下，失败能退回。本轮不写 v4.0.0 配方，不切版。

## 已完成内容

- `migration-schema.md` §4 补上 `[delete]` 和 `[move]`。`[split]` 整段保留。
- `upgrade.py` 认识这两类动作。路径不合法、正好点到 `.ai`、或点到受保护子目录时拒绝。重复执行按起始态处理。
- 目录删到一半或搬到一半失败时，临时项目回到动手前，退出码 5。
- 测试用临时目录，不改现有 `migrations/manifest.json`。`VERSION` 仍是 `3.6.0`。没有 `migrations/v4.0.0.md`。

## 关键变更 / 用户可感知变化

- 以后的迁移配方可以点名删掉一个文件或目录，也可以把仓根上的路径搬进 `.ai/`。
- 这次升级仍然不会动别人硬盘上的旧收件箱和 `origin/`。那要等 R15 的配方。
- `--split` 仍是 `apply` 的必填参数，取值仍是 `defer` 或 `now`。

## 高层影响范围

- 改动：`migration-schema.md` §4、`tools/butler-upgrade/upgrade.py`、`tools/butler-upgrade/README.md`、`scripts/test-butler-upgrade.py`、`.ai/debt.md`。
- 不算：不新建产品文件，不改 `migrations/manifest.json`，不写 `migrations/v4.0.0.md`，不改 `VERSION`，不在真实已部署项目上跑升级，不提交。

## 验证方式与结果摘要

7 条验收全部通过。升级器测试 31 passed。持续集成退出码 0，其中 pytest 211 passed。收口前完成裁决 `eligible`。独立复核未开。

审计退出码 0，0 条 DRIFT，2 条未发布。未发布是工作树有未提交改动，以及标签 `v3.6.0` 不在当前 HEAD。

## 已知剩余风险 / 延后事项

- 已部署项目里的旧收件箱和 `origin/` 要等 R15 的 `migrations/v4.0.0.md`。
- 源和目标路径重叠时会拒绝。这条写在代码和测试里，没有回写进已确认的方案正文。
- 幂等移动不比较目标现有内容。
- 测试跑在临时目录上，没有真实已部署项目的升级回归。
- 本轮不切版、不提交。

## 引用

- 四件套：`.ai/iterations/ITER-0125/CONCEPT.md`、`AC_LIST.md`、`TECH_PLAN.md`、`VERIFY_REPORT.md`
- 变更流：`.ai/iterations/ITER-0125/CHANGELOG.md`
- 证据：`.ai/iterations/ITER-0125/evidence/`（3 条记录）
