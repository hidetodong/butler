# Task State

> **无活跃迭代 / 无活跃里程碑**（`ITERATIONS.current: none`、`MILESTONES.current: none`）。**ITER-0042（PRD 先行触发加固）已收口、待切 v2.2.0**（MINOR）。等下一个方向。

## 当前状态

- 无进行中工作。ITER-0042 独立迭代（MILE-0004 已收）修掉了 v2.1.0 PRD 子系统的实战缺陷——Confluence 地址经 MCP 直读当 `/milestone` brief 时漏切 `references/prd/`。三层已补（注入表内容路由 + `milestone §6.4` 分类闸前移 + 新增 PostToolUse advisory hook `butler_advisor.py`）。交付 `deliveries/ITER-0042-prd-trigger-hardening.md`+`.html`，归档 `.ai/iterations/ITER-0042/`。
- **未切版**：`VERSION` 仍 `2.1.0`。ITER-0042 判 **MINOR（v2.2.0）**——加 PostToolUse hook 属能力新增，切版需 `migrations/v2.2.0.md`（`[sync-hooks]` 拷 `butler_advisor.py`/`prd_split_reminder.py` + settings 合并补 PostToolUse 键 + `[restamp]`）。切版是独立 `chore(release)` 发布动作、待用户放行。
- 全貌产物（`frontier.md` / `architecture.md`）已折叠 ITER-0042 delta。

## 下一步入口

- **切 v2.2.0**（待放行）：聚合 ITER-0042，写 `migrations/v2.2.0.md`（首个含 `[sync-hooks]` 的迁移配方——既有部署需补 PostToolUse hook）。
- **待用户给方向**：新里程碑 / 独立迭代由用户发起。候选——PRD 全链真实 dogfood（拿一份真 PRD 走导入→改版全程），可一并还上"从未真跑"的欠账。
- **推送**：ITER-0042 迭代提交 + 历史 v2.1.0 发布与 ITER-0035~0041 提交**均在本地 main、未推送**。推送待用户说"推送"。
- 冷启动读序（butler 文件夹态）：`.ai/project/00_INDEX.md` → `.ai/MILESTONES.md` / `.ai/ITERATIONS.md` → 本文件 → 代码。
