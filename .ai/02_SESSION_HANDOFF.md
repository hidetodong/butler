# Session Handoff

## 任务断点

butler 规则仓当前状态：**v0.1.1 基地车生命周期三阶段齐备**（commit `205ca09 feat(0.1.1)`）。

在 `v0.1.0-first-stable`（audit 全周期闭环）之后新增 `/butler-upgrade` feature —— 已部署项目可通过一条命令主动同步到最新版 butler。

延后项：**Bucket H (N-6)** — `10_Domain_Stack_Profiles/` 目录分层，策略性延后，等 profile 数量到 5-6 个再做。

## 关键决策摘要

- **基地车三阶段**：`mcv-deployment.md`（部署）/ `butler-upgrade.md`（跨版本升级）/ `mcv-update.md`（`.ai/` 内部维护）并列；角色边界清晰，不混用。
- **保护区契约**：`<!-- user-managed -->` / `<!-- /user-managed -->` 包裹 CLAUDE.md 的"项目特定约束"章节 —— 用户内容放保护区内永不被覆盖。
- **升级触发**：`/butler-upgrade` + 语义词（"升级 butler" / "同步到新版" / "同步 butler 规则"）；非持久 Mode，执行一次后返回 Standard。
- **老项目（无保护区）首次升级**：备份 + 交互 ACK（方案 b）—— 不自动猜测、不静默覆盖。
- **`.ai/` 升级粒度**：命名 + schema 必填补齐（方案 ii），不动 CHANGELOG / BUG_LOG / 任务产物。
- **不引入版本戳（β 决策）**：靠差异检测，不靠版本号比较。
- **术语契约**：Mode = 运行时能力（与 /xxx 命令绑定）；Role = 职责切换（与 P1-P5 阶段映射）。
- **命名契约**：`.ai/` 根下热数据带数字前缀（`00_` / `01_` / `02_` / `03_`）；archive/ 不强求前缀。
- **模板 SSOT**：`rule-card.md` 是浓缩规则真源；`CLAUDE.md.template` 通过 `{{RULE_CARD_CONTENT}}` 占位符引用。

## 环境脏点

- 本地有 2 个 milestone tag：`v0.0.8`、`v0.1.0-first-stable`，均未 push 到 remote。
- `.claude/settings.local.json` 未 gitignore（Claude Code 本地权限，按惯例不提交）。
- `v0.1.1` 新 milestone tag 待打（本轮之后）。

## 已知风险

- `/butler-upgrade` 协议**首次实跑待 dogfooding** —— 尚无实际老项目走过完整升级流程。协议按最高清晰度文档化，但首次执行可能暴露边界情况。
- butler 仓自身的 `CLAUDE.md`（仓根）**未加保护区标记**，按 `butler-upgrade.md § 8` 显式不做（butler 自身演进走 audit 流程，不走 upgrade 协议）。
- `scripts/setup.sh` Linux 分支未真机验证（代码评审通过）。

## 唤醒指令

新会话从项目 `CLAUDE.md` + `Coder/README.md § 读取顺序` 建立上下文。

若要实跑 `/butler-upgrade`：先找一个老项目，让 AI 读 `butler-upgrade.md`，按 § 3 侦察 → § 4 或 § 5 执行。

若要推进 Bucket H：先 `ls Coder/10_Domain_Stack_Profiles/` 评估 profile 数量是否到临界点。

## 状态指针

- 最新产物链：`.ai/{CONCEPT, AC_LIST, TECH_PLAN, VERIFY_REPORT}.md`（对应 `/butler-upgrade` feature 轮次）
- 历史决策链：`git log --oneline v0.0.2..HEAD`（9 轮提交 + 2 个 milestone tag）
- 人类可读归档：`deliveries/` 下 9 份 Delivery Summary（8 审计修复 + 1 feature）
