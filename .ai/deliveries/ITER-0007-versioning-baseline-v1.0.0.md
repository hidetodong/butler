# ITER-0007 引入硬版本概念 + 切基线 v1.0.0（基线 + 接入部署/升级）

## 本次交付目标
butler 规则仓库此前**没有硬版本概念**——"当前规则源是哪一版"只活在 git 历史里，部署到目标项目的产物也无从得知自己基于哪一版生成，升级只能纯靠内容比对。本轮把版本变成机器可读、人类可读、可比较的事实，并按用户拍板的范围（**基线 + 接入部署/升级**）把版本接入部署产物与升级协议，切出首个正式基线 **v1.0.0**。

## 已完成内容
- **版本载体三件**：仓库根 `VERSION`（机器 SSOT，单行 `1.0.0`）+ 根 `CHANGELOG.md`（人读发布史，v1.0.0 基线条目聚合 ITER-0001~0007、只引用台账/deliveries 不复述）+ git tag `v1.0.0`（收口提交锚点）。
- **版本治理规则**：新增 `Coder/20_Workflow_Lifecycle/versioning-schema.md`——定义 VERSION 的 SSOT 地位与格式、规则仓口径 semver 语义（MAJOR 破坏性 / MINOR 兼容新增 / PATCH 澄清修订）、CHANGELOG 与 ITER 台账分工、切版流程、部署戳与升级 gap 口径、版本戳语义边界。
- **部署接入版本戳**：`templates/CLAUDE.md.template` 新增 `{{BUTLER_VERSION}}` 占位符（落 butler 管理区、保护区之外，供升级原地重戳）；`mcv-deployment.md §3` 增"读 `$BUTLER/VERSION` → 替换 `{{BUTLER_VERSION}}`"注入步（步骤顺延重编号）。
- **升级版本感知**：`butler-upgrade.md` §3 侦察增"读目标戳 vs 仓库 VERSION → 报版本 gap"、§4/§5 升级时戳/重戳、§5 清单含版本 gap 项、§7 验证增版本戳项；**§8 反转**原"butler 不引入版本戳"为"版本号为辅、内容差异为主"，并把 butler 自身升级治理指向 versioning-schema 切版流程。
- **注册与人类文档**：`Coder/README.md` 双处注册 versioning-schema；`HUMAN_GUIDE.md` 新增「Butler 版本」小节 + §8 速查树补登；butler 自身 `CLAUDE.md` 目录结构补 `VERSION`/`CHANGELOG.md`。

## 关键变更 / 使用者可感知变化
- butler 现在**有版本号了**：`VERSION` 看机器真源、`CHANGELOG.md` 看发布史、`git tag` 看每版确切提交。
- 以后部署进项目的 `CLAUDE.md` 顶部会标注"规则源：butler vX.Y.Z"——一眼知道这个项目基于哪一版规则。
- `/butler-upgrade` 升级为**版本感知**：会告诉你项目落后几个版本、升级后把版本戳更新到最新——但**判断要不要升级仍以内容差异为准**，版本号只是辅助路标（项目文件可能已手工漂移）。

## 高层影响范围
- 新增：`VERSION`、`CHANGELOG.md`、`Coder/20_Workflow_Lifecycle/versioning-schema.md`。
- 改：`templates/CLAUDE.md.template`、`Coder/20_Workflow_Lifecycle/{mcv-deployment,butler-upgrade}.md`、`Coder/README.md`、`HUMAN_GUIDE.md`、根 `CLAUDE.md`。
- 收口动作：`git tag v1.0.0`。
- 不涉及（零改动护栏）：`templates/rule-card.md`、`templates/hooks/`、`70_Extension_Preference/`、产物链四 schema（concept/acceptance/tech-plan/verify）、迭代/里程碑台账字段。

## 验证方式与结果摘要
- 逐 AC（AC1–AC18）grep 落点命中各目标文件，全部通过。
- AC15 单一真源：`{{BUTLER_VERSION}}` 三文件一致；规则/模板/文档树中无第二处当前版本硬编码（butler-upgrade 内 `v1.0.0→v1.2.0` 为示例）。
- AC16 零改动：`git status` 确认护栏文件（rule-card / hooks / preference / 四 schema / 台账字段）未入改动名单。
- 旧"butler 不引入版本戳"句已删除（§8 反转生效）。
- 详见 `.ai/iterations/ITER-0007/VERIFY_REPORT.md`。

## 已知剩余风险 / 延后事项
- 切版与版本戳维护靠规则纪律（无 hook 强制），与现有读取顺序同源同险。
- 反转 §8 削弱"纯内容差异"旧简洁性，以"版本号为辅、内容差异为主"兜底，不引入凭版本号跳过升级的捷径。
- 存量旧项目无版本戳：butler-upgrade 已定义"无戳=前版本化、首次升级首戳"，本轮不批量回填；自动化 bump/CI 校验亦属后续候选。

## 引用
- `.ai/iterations/ITER-0007/CONCEPT.md`
- `.ai/iterations/ITER-0007/AC_LIST.md`
- `.ai/iterations/ITER-0007/TECH_PLAN.md`
- `.ai/iterations/ITER-0007/VERIFY_REPORT.md`
