# Verification Summary
- 覆盖范围：为 butler 规则仓库引入硬版本概念并切基线 v1.0.0——版本载体（VERSION/CHANGELOG/tag）、版本治理规则（versioning-schema）、部署版本戳（`{{BUTLER_VERSION}}`）、升级版本感知（butler-upgrade 读戳/报 gap/重戳、反转 §8），及 README/HUMAN_GUIDE/根 CLAUDE.md 注册。
- 总体结论：AC1–AC18 全部满足；逐 AC grep 落点通过，AC16 零改动经 `git status` 确认护栏文件未入改动名单，旧"butler 不引入版本戳"句已消失。ITER-0007 闭合，git tag `v1.0.0` 在收口提交后打。

# AC Status
- [x] AC1: 根 `VERSION` = 单行 `1.0.0`（`wc -l`=1）
- [x] AC2: 根 `CHANGELOG.md` 含 `## [1.0.0] - 2026-06-19`，聚合 ITER-0001~0007、引用 ITERATIONS.md/deliveries、不复述
- [x] AC3: 收口提交后打 `git tag v1.0.0`（P5 收口环节执行）
- [x] AC4: 新增 `versioning-schema.md`（frontmatter 合规）+ MAJOR/MINOR/PATCH 规则仓口径定义
- [x] AC5: CHANGELOG↔ITER 台账分工（聚合/只引用不复述）+ CHANGELOG 格式/位置 + git tag `vX.Y.Z` 约定
- [x] AC6: 切版流程 + 部署戳口径 + 升级 gap 口径（版本号为辅、内容差异为主）+ 戳语义=规则源版本
- [x] AC7: `CLAUDE.md.template` 新增 `{{BUTLER_VERSION}}`（行 15，落 `<!-- user-managed -->`(行 37) 之前）+ 顶部注释补说明
- [x] AC8: `mcv-deployment §3` 新增步 4 读 VERSION + 替换 `{{BUTLER_VERSION}}`，步骤连续重编号（5/6 顺延）
- [x] AC9: `butler-upgrade §3` 新增动作 4 计算/汇报版本 gap，目标无戳→§4 路径
- [x] AC10: §4 步2 首次戳入、§5 步2 重戳 + 步4 清单含版本 gap、§7 验证项"版本戳已更新"
- [x] AC11: §8 旧"不引入版本戳"反转为"版本号为辅、内容差异为主"；butler 自身升级指向 versioning-schema 切版流程
- [x] AC12: `Coder/README.md` 目录结构（行 52）+ 规则说明（行 129）双处注册 versioning-schema
- [x] AC13: `HUMAN_GUIDE.md` 新增「Butler 版本」小节（行 126）+ §8 速查树补 versioning-schema（行 272）
- [x] AC14: 根 `CLAUDE.md` 目录结构补 `VERSION`/`CHANGELOG.md`（行 14-15）
- [x] AC15: `{{BUTLER_VERSION}}` 三文件一致；当前版本数字唯一真源在 `VERSION`（butler-upgrade 内 `v1.0.0→v1.2.0` 为示例非真源）
- [x] AC16: 零改动护栏——rule-card / templates/hooks / 70_Extension_Preference / concept·acceptance·tech-plan·verify-schema / iteration·milestone schema 均不在改动名单
- [x] AC17: 未破坏 CLAUDE.md 五约束（分层未混、产物链未动、新 schema 已注册、模板 SSOT 未手写重复、frontmatter 合规）
- [x] AC18: ITER-0007 归档 + delivery + 台账 closed（P5 收口环节执行）

# Verification Results
- AC1：`cat VERSION`=`1.0.0`，`wc -l`=1（单行无多余空行）。
- AC2/AC5：`grep` CHANGELOG 命中 `## [1.0.0] - 2026-06-19`、`聚合 ITER-0001 ~ ITER-0007`、`.ai/ITERATIONS.md`/`deliveries/` 引用；目视确认条目为能力基线要点而非逐迭代复述。
- AC4/AC6：`grep` versioning-schema 命中 MAJOR/MINOR/PATCH 三级定义、`## 5. 切版流程`、`## 6. 部署版本戳`、`## 7. 升级版本 gap`、`版本号为辅、内容差异为主`、SSOT `VERSION` 表述。
- AC7：`grep` template 行 15 `{{BUTLER_VERSION}}` 在 `<!-- user-managed -->`（行 37）之前；顶部注释含版本占位符替换说明。
- AC8：`grep` mcv-deployment 行 86 步 4 读 `$BUTLER/VERSION` + 替换 `{{BUTLER_VERSION}}`；后续步骤 5/6 顺延。
- AC9/10/11：`grep` butler-upgrade 命中 §3 动作 4 版本 gap、§4/§5 戳/重戳、§5 清单版本 gap 项、§7 版本戳验证项、§8 versioning-schema 指向 + 内容差异为主；旧"不引入版本戳"句 `grep` 无命中（已删除）。
- AC12/13/14：`grep` README / HUMAN_GUIDE / 根 CLAUDE.md 命中各落点。
- AC15：`grep -rln BUTLER_VERSION` 命中 template / mcv-deployment / butler-upgrade 三文件；`grep -rn 1\.0\.0` 在规则/模板/文档树中仅命中 butler-upgrade 的两处示例（`v1.0.0 → v1.2.0`），无第二处当前版本硬编码真源。
- AC16：`git status --short` 改动名单 = `.ai/` 四件套+台账、CLAUDE.md、butler-upgrade、mcv-deployment、README、HUMAN_GUIDE、template（改）+ VERSION、CHANGELOG.md、versioning-schema.md（新增）；护栏文件均不在内。

# Gate Coverage
- 通用质量门禁：遵守 CLAUDE.md 五约束——分层未混（改动落 20_ + 根载体 + 文档/模板）、产物链未动、新增 versioning-schema 已在 README 目录结构+说明双处注册、模板 SSOT 未手写重复（rule-card 未改，版本戳是部署替换值与 `{{BUTLER_PATH}}` 同类）、versioning-schema frontmatter 含 audience/scope。
- Active Profiles：未命中（Markdown 规则仓库），N/A。
- Tech Plan Alignment：TECH_PLAN 九文件改动与六项 Design Decisions 全兑现——VERSION 单一真源、版本戳落 butler 管理区、版本为辅内容为主、CHANGELOG 只引用不复述、不改 rule-card、tag 收口后打。
- References Compliance：本轮无 `.ai/references/`，N/A。

# Remaining Risks
- 切版与版本戳维护靠规则纪律（无 hook 强制），与现有"会话起始必读"同源同险——versioning-schema §8 如实标注。
- 反转 butler-upgrade §8 削弱"纯内容差异"的旧简洁性，以"版本号为辅、内容差异为主"措辞兜底，不引入"凭版本号跳过升级"危险捷径。
- 存量旧项目无版本戳：butler-upgrade §3/§4 已定义"无戳=前版本化、首次升级路径首戳"，本轮不批量回填。

# Handoff / Next Step
- 任务闭合。收口动作：归档四件套→`.ai/iterations/ITER-0007/`、写 `deliveries/ITER-0007-<slug>.md`、台账置 closed + `current: none`、提交后 `git tag v1.0.0`。
