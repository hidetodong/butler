# CONCEPT — ITER-0052 · Codex 工作流入口

> ⚠️ 危险模式：本迭代由模型自治推进；P2/P3 将在强制自审门通过后自主 ACK，未经用户逐项确认。

## 一句话目标

把 Butler 的 8 个 Claude 薄壳命令变成 Codex 可发现、可安装、仍回指共同规则真源的 8 个 skills，并用 plugin 作为最终分发包。

## 问题

- R1 只让 Codex 认识 Butler 仓库，还没有可显式或语义触发的 Butler 工作流入口。
- 直接复制 Claude command 正文会形成第二套算法；skills 必须只做定位、读真源、分派和优雅降级。
- repo skills 适合开发发现，plugin 适合全局安装；两份实体内容会漂移，需要单一物理真源。

## 已确认决策

1. `plugins/butler/skills/` 是 8 skills 的发布真源；`.agents/skills/` 只放指向它们的相对软链，既满足 repo discovery，也不双写。
2. plugin 名为 `butler`，由官方 `plugin-creator` 脚手架建立，manifest 不夹带 R3 hooks、MCP 或 apps。
3. 8 个 skill 对应 `prd`、`review`、`milestone`、`upgrade`、`ideation`、`preference`、`loop`、`dangerous`；每个都从 `BUTLER_PATH` 定位 `Coder/` 真源。
4. 高风险的 `loop` 与 `dangerous` 禁止隐式触发；其 `agents/openai.yaml` 设 `allow_implicit_invocation: false`。其余 6 个允许语义触发。
5. R2 按 MINOR 发布 v2.13.0；R3 hooks、R4 目标项目双入口部署不提前进入。

## 范围

- 建 plugin manifest、8 skills、UI metadata、repo fallback 软链。
- 增加安装/刷新脚本与结构验证，真实安装到本机个人 marketplace 后用新 Codex 会话验证发现和触发。
- 更新兼容说明、README/HUMAN_GUIDE/Coder 注册与项目知识。

## 不做

- 不增加 `.codex/hooks.json`，不改 Python gate，不宣称 `apply_patch` 已受门禁。
- 不修改 `scripts/setup.sh`、目标项目首次部署或升级生成双入口的执行链。
- 不改 Claude commands 和工作流算法。
- 不发布公共 marketplace，不 push、不合并。

## 风险

- plugin 安装会写用户级 `~/.agents/plugins/` 与 Codex 插件缓存；这是用户要求的全局兼容目标内动作，必须通过官方脚本和 CLI，且保留可移除路径。
- 本地 plugin 缓存不会自动跟随仓库更新；更新脚本必须处理同步、cachebuster 与重装。
- skill 的隐式触发存在模型判断不确定性；以显式 `$skill` 为可靠验收，低风险 skills 再做语义触发代理验证。
