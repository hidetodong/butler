# ITER-0120 · 根布局整理：backlog 与 deliveries 迁入 .ai

- 交付级别：迭代交付（小版本）
- 收口日期：2026-09-14
- 所属里程碑：MILE-0016（Butler 瘦身与重造）

## 本次交付目标

把两件还露在「项目根 / 带里程碑专名」里的东西收进 `.ai/`：候办草稿目录从 `.ai/milestone-backlog/` 改成 `.ai/backlog/`，仓根 `deliveries/` 整树搬进 `.ai/deliveries/`。活着的规则、工具、测试、台账都指新路径；冻结快照不改写。不留兼容软链。Butler 仓自己一次搬干净，已部署项目的搬家只登记给后续升级器补动作和配方。

## 已完成内容

- **候办目录改名**：`.ai/milestone-backlog/` → `.ai/backlog/`，10 份草稿文件名不变。闪念口去向、待办区草稿列、`tools/intake/` 常量和测试夹具一起改。
- **交付树搬家**：仓根 `deliveries/` → `.ai/deliveries/`，272 个文件，迭代交付仍平铺、里程碑交付仍在 `milestones/` 子目录。用 `git mv` 保血缘，不建仓根软链。
- **活指针改、历史记述不改**：规则、工具、测试、台账交付列（热表 + 两片冷分片）、CHANGELOG 里「去哪找文件」的链接、冷启动读序投影改到新路径。收口快照、已发布配方、交付正文内部的「当时写到 deliveries/」不改。
- **部署只建 `.ai/`**：init / 部署协议 / 规则卡不再在仓根建 `deliveries/`。`.ai/backlog/` 与 `.ai/deliveries/` 按需产生。
- **hook 黑名单故意不动**：进摘要的 hook 文件零字节改动，给还没升级的项目留着仓根 `deliveries/` 豁免。
- **范围演进登记**：v4.0.0 必须含入口重生成；不需要 hook 同步；候办改名可走现有改名动作；仓根交付搬家等升级器补「移动」动作。

## 关键变更 / 用户可感知变化

- **以后找交付总结，去 `.ai/deliveries/`**，不再去项目根。
- **以后找候办草稿，去 `.ai/backlog/`**。这个目录已经不只装里程碑那一档，名字不再带 milestone。
- **新部署的项目根更干净**：只建 `.ai/`，不再多一个仓根 `deliveries/`。
- **老项目这轮不会被自动搬走**。别人硬盘上仓根的 `deliveries/` 和旧候办目录还在，等升级器能表达「移动」之后再写配方。

## 高层影响范围

- 搬家：候办草稿 10 份、交付文件 272 个。
- 改动：录入工具与测试、状态审计、冷启动读序真源和四处投影、部署与收口规则、台账热表与冷分片、CHANGELOG 找文件的链接。
- 新增：本轮路径扫描 `.ai/iterations/ITER-0120/ac-sweep.py`。
- **完全没碰的**：hook 源文件 19 份、历史快照目录、已发布迁移配方、`docs/research/`、`docs/superpowers/`。
- 目标项目侧：改了规则卡和两份入口模板，下次切版的迁移配方必须含入口重生成。

## 验证方式与结果摘要

12 条验收全部通过。9 份自动道证据全绿，其中一份是收口前简评复跑。CI 退出码 0，状态审计 0 漂移、2 条未发布标记（本轮不切版，预期内）。路径扫描 A 组 0 命中、B 组全在场。

收口前完成裁决 `eligible`。P5 简评复跑了 intake 测试、审计测试、路径扫描、冷启动读序投影、领域合同，没有 Must Fix。独立复核未跑。

`git log --follow` 在未提交前追不到新路径，这是 git 的正常行为；index 里 ITER-0119 那份交付是 `R100`，提交之后 follow 才能跨过这次改名。

## 已知剩余风险 / 延后事项

- **`git log --follow` 要等这次改名进提交之后才能跨路径追历史。**
- **已部署项目仓根的 `deliveries/` 和旧候办目录本轮没搬**，等 R14 补移动动作、R15 写进 v4.0.0 配方。
- **hook 黑名单里的 `deliveries/` 豁免故意留着**，给还没升级的项目用。
- 本轮不切版、不打 tag、不提交。

## 引用

- 四件套：`.ai/iterations/ITER-0120/CONCEPT.md`、`AC_LIST.md`、`TECH_PLAN.md`、`VERIFY_REPORT.md`
- 变更流：`.ai/iterations/ITER-0120/CHANGELOG.md`
- 证据：`.ai/iterations/ITER-0120/evidence/`（9 条记录）
- 可重跑验收扫描：`.ai/iterations/ITER-0120/ac-sweep.py`
- 开工前基线：`.ai/iterations/ITER-0120/pre-p4.baseline.json`
