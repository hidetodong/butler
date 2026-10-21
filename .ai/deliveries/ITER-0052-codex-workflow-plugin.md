# Codex 八工作流 plugin：Butler 从“能读规则”走到“能调用工作流”

> ITER-0052 · MILE-0006 R2 · 危险模式自主 ACK + P5 完整强审 · 2026-07-17 · v2.13.0

## 交付结果

- `plugins/butler/` 成为可安装 Codex plugin，包含 `$butler-prd`、`$butler-review`、`$butler-milestone`、`$butler-upgrade`、`$butler-ideation`、`$butler-preference`、`$butler-loop`、`$butler-dangerous`。
- `.agents/skills/` 只放 8 个相对软链，repo discovery 与 plugin 共用实体真源。
- 每个 skill 都是薄适配：定位 `BUTLER_PATH`、读取对应 `Coder/` 真源、分派和优雅降级，不复制算法。
- loop/dangerous 禁隐式触发；安装器经个人 marketplace、cachebuster、validator 与 CLI 安装，并精确核对最终版本。

## 验证

- 官方 plugin validator 与 8 个 skill validator 全过。
- 结构脚本在仓根和 `/tmp` 均通过。
- 隔离 HOME 安装两次与真实 HOME 安装通过；`butler@personal` installed/enabled。
- 新 `codex exec` 普通 review skill 自动从 plugin cache 加载并读对真源；危险 skill 状态路径返回正确双真源和禁隐式策略。
- Claude 109 个 hook tests 通过，Claude 入口/commands/hooks/setup 定向 diff 为空。

## 危险模式披露

本迭代 P2/P3 未经用户逐项确认，由模型通过强制自审门后自主 ACK；决策与修正逐条记录于 `.ai/RUN_LOG.md`。P5 为主代理完整多维强审，0 Must Fix；受团队策略限制未启动子 agent，因此不宣称独立复核。

## 剩余风险

- 非交互 `codex exec` 对禁隐式 skill 的纯文本 `$mention` 与交互 UI mention 不完全同构；交互式选择待人补测，安全策略保持不放宽。
- R3 才提供 Codex hooks；R4 才提供统一 setup、目标项目双入口与升级回归。

## 引用

- plugin：`plugins/butler/`
- 验证：`.ai/iterations/ITER-0052/VERIFY_REPORT.md`
- 兼容状态：`docs/codex-compatibility.md`
- 迁移：`migrations/v2.13.0.md`
