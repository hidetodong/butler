# Task State

> **无活跃迭代 / 无活跃里程碑**（`ITERATIONS.current: none`、`MILESTONES.current: none`）。**v2.2.0 已切版（本地 tag，未推送）**——聚合 ITER-0042（PRD 先行触发加固）。等下一个方向。

## 当前状态

- 无进行中工作。ITER-0042 独立迭代（MILE-0004 已收）修掉了 v2.1.0 PRD 子系统的实战缺陷——Confluence 地址经 MCP 直读当 `/milestone` brief 时漏切 `references/prd/`。三层已补（注入表内容路由 + `milestone §6.4` 分类闸前移 + 新增 PostToolUse advisory hook `butler_advisor.py`）。交付 `deliveries/ITER-0042-prd-trigger-hardening.md`+`.html`，归档 `.ai/iterations/ITER-0042/`。
- **v2.2.0 已切版（本地）**：`VERSION`=`2.2.0`、`CHANGELOG.md` 顶条 `## [2.2.0]`、tag `v2.2.0` 打在发布提交上、`migrations/v2.2.0.md` 已写（**本仓首个含 `[sync-hooks]`** 的配方——既有部署需拷 `butler_advisor.py`/`prd_split_reminder.py`/更新 `lib/io.py` + settings 合并补 PostToolUse 键 + `[restamp]`）。发布是独立 `chore(release)` 提交，与 ITER-0042 迭代提交（`0930bc8`）分开。
- 全貌产物（`frontier.md` / `architecture.md`）已折叠 ITER-0042 delta；`frontier.md` 已前滚至 v2.2.0 已切版态。

## 下一步入口

- **推送**（待放行）：v2.2.0 发布提交 + tag、ITER-0042 迭代提交 + 历史 v2.1.0 发布与 ITER-0035~0041 提交**均在本地 main、未推送**。推送待用户说"推送"（一推会把整批本地历史 + `v2.2.0` tag 一起推上去）。
- **待用户给方向**：新里程碑 / 独立迭代由用户发起。候选——PRD 全链真实 dogfood（拿一份真 PRD 走导入→改版全程），可一并还上"从未真跑"的欠账。
- 冷启动读序（butler 文件夹态）：`.ai/project/00_INDEX.md` → `.ai/MILESTONES.md` / `.ai/ITERATIONS.md` → 本文件 → 代码。
