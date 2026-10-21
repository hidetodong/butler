# ITER-0112 · 退役项目知识文件夹与折叠机制（MILE-0016 R1）

- 交付级别：迭代交付（小版本）
- 收口日期：2026-08-18
- 所属里程碑：MILE-0016（Butler 瘦身与重造）

## 本次交付目标

`.ai/project/` 这个「项目知识文件夹」当初是想给新会话一份项目全貌，靠每次迭代收口时把变更「折」进去来维护。半年下来，里面有的文件一直准，有的已经烂到不能读。这一轮先把烂掉的那部分连同折叠机制一起拆掉，把因此断掉的指针全部改到自洽，并且当场登记清楚哪些活儿留给了后面的路线项。

## 已完成内容

- 删掉六份文件与两个帮手：`.ai/project/` 下的 `00_INDEX.md` / `identity.md` / `constraints.md` / `architecture.md` / `fold-state.json` 五份，加上定义折叠结构的 `Coder/40_Context_Management/project-digest-schema.md`；帮手侧删掉 `knowledge-fold.md`（把迭代变更折进知识文件夹）与 `drift-check.md`（查知识文件夹有没有过时），帮手名册从四个减到两个。
- 删 `capabilities.md`（27KB、22 个小节）前逐节核过一遍，不是整文件一删了事：22 节全部在仓里别处能找到更准的原文，核查结论逐条写进了本迭代的变更流。唯一一条别处没有的判断——「升级器从没在真实已部署项目上跑过」——已迁进 `.ai/debt.md`，没有随文件一起消失。
- 保留 `invariants.md` 与 `frontier.md` 原位不动，只把其中三条因本轮删除而变成假话的不变量改对。这两份一直准，留给 MILE-0016 R3 的替代品设计接手。
- `debt.md` 从 `.ai/project/` 迁到 `.ai/debt.md`，内容原样。
- 解除两处收口仪式对折叠的强制：迭代收口从四步必做变成「前三步必做、第四步自检」，里程碑收口从四步减到三步；冷启动一致性自检从 6 条不变量减到 5 条。
- 拆掉机器侧的知识文件夹校验与夹具：状态审计脚本里的折叠回执检查、上下文预算的重复真源候选表、Codex 基线脚本的冷启动读序断言，以及相关单元测试。
- 34 处活引用改到自洽，包括仓根 `AGENTS.md`、部署入口模板、`/butler:init` 命令与 skill、`Coder/README.md` 的目录结构与读取顺序。

## 关键变更 / 用户可感知变化

- **冷启动第一读换了目标**：以前是 `.ai/project/00_INDEX.md`，现在是 `.ai/debt.md`（长期欠债与硬约束）。这是过渡措辞，新读序的正面定义归 R2。
- **部署新项目不再自动建 `.ai/project/` 空目录**。老项目磁盘上已经建出来的空目录本轮不清理，归 R15 的迁移配方交代。
- **收口时少一步**：不用再折叠知识文件夹，也不用再跑漂移检查。
- **`.ai/project/` 目前只剩两个文件**（`invariants.md`、`frontier.md`），处在半拆状态，等 R3 给它们定新落点。

## 高层影响范围

- 删除文件 9 个：`.ai/project/` 下 5 个、`Coder/62_Extension_Agents/` 下 2 个、`Coder/40_Context_Management/` 下 1 个、`.ai/project/debt.md` 迁位 1 个。
- 修改规则文件 16 份，其中 `iteration-schema.md` 与 `milestone-schema.md` 动了收口仪式步骤编号、`context-persistence.md` 动了冷启动读序与不变量清单。
- 修改机器侧 6 处：`scripts/audit-project-state.py` 及其测试、`tools/context-budget/` 及其测试、`scripts/verify-codex-foundation.sh`、`Coder/domain-glossary.md`（术语从 20 条减到 19 条，机器校验的精确条数同步改）。
- 修改入口 4 份：`AGENTS.md`、`templates/AGENTS.md.template`、`.claude/commands/butler/init.md`、`plugins/butler/skills/butler-init/SKILL.md`。
- `migration-schema.md` 的 `[split]` 标签**没有删**，只加了退役标注——历史迁移配方 v1.6.0 到 v2.2.0 引用了它，配方清单有一致性校验，删了会红。
- 未触碰升级器 `upgrade.py` 的动作类型表与 CLI 参数，未改双台账结构，未切版发布。

## 验证方式与结果摘要

- 10 条验收标准全部达成：7 条有机器证据（`ac1-files` / `ac3-roster` / `ac4-rituals` / `ac5-schema-gone` / `ac6-scan` / `ac7-verify-ci` / `ac8-audit-final`，全部 passed），3 条为人读核对（迁出核查留痕、交接登记、本节两项信息损失）。
- 完整 `scripts/verify-ci.sh` 退出码 0；状态审计退出码 0，除「工作树有未发布改动」「tag 不指向 HEAD」这两条发布态亮牌外无漂移。
- 全仓检索 `project-digest` / `knowledge-fold` / `drift-check` / `fold-state` 在活跃文件中零命中，历史归档按纪律保留不追改。剩余的 `.ai/project` 路径字样逐条人读过，都指向 `invariants.md`、`frontier.md`，或部署项目侧的 `workspaces.md`（butler 是单包仓，本仓没有这个文件，属正常）。
- 执行中撞到一次验收标准自相矛盾并按规则 amend：原 AC1 要求 `invariants.md` 一字不动，但里面有三条不变量在删除后变成假话，留着正违背本里程碑要消灭的「陈旧的完整」。AC1 收窄为只允许改这三条，产物退回 draft 重新 ACK 后继续。

## 已知剩余风险 / 延后事项

- **折叠回执的历史不可再机器验证**。`fold-state.json` 记录了哪些迭代参与过折叠、每次折叠的内容 hash，删掉之后这段历史只剩 git 记录，没有工具能再校验它。判断是这段历史本身没有消费者——它唯一的读者就是已经一起删掉的漂移检查。
- **本轮论证的是「没有证据表明它被读过」，不是「已证明它从未被读过」**。半年里没有任何一次决策能追溯到读知识文件夹，也没有任何工具记录过对它的读取——但没有读取记录不等于没有读取。真正的确定性数据要等 R11 的使用监视器上线，那之前这个判断建立在缺席证据上，请当作有一定不确定性的结论看。
- **半拆状态不能拖太久**。冷启动第一读现在处在「不再指知识文件夹、新读序还没正式定义」的过渡措辞上，`.ai/project/` 也只剩两个孤立文件。R2 定读序、R3 定全貌产物落点；这两项若迟迟不开，这个中间态会变成事实上的常态，比拆干净或者不拆都糟。
- **`[split]` 标签与 `--split` 参数仍在**，指向的机制已经退役。标签扩展归 R14，v4.0.0 迁移配方归 R15，两处都已在里程碑演进记录里登记现状与归属。

## 引用

- `.ai/iterations/ITER-0112/CONCEPT.md`
- `.ai/iterations/ITER-0112/AC_LIST.md`
- `.ai/iterations/ITER-0112/TECH_PLAN.md`
- `.ai/iterations/ITER-0112/VERIFY_REPORT.md`
- `.ai/iterations/ITER-0112/CHANGELOG.md`
- `.ai/iterations/ITER-0112/evidence/`
