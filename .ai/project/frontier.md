# frontier（当前形态 / 活跃战线 / 下一个瓶颈）

> 变得最快的一层。战线收了就覆盖删除，不叠历史。

## 当前形态

- **版本**：v2.13.0。MILE-0006 R1/R2 已完成：Codex 能从 `AGENTS.md` 发现规则，并通过 `plugins/butler/` 安装 8 个 Butler workflow skills；`.agents/skills/` 是同一实体源的仓库软链发现面。
- **里程碑**：MILE-0006 active；R1/R2 closed，R3/R4 planned；R2 收口后危险模式将自动开启 R3。
- **分发**：`scripts/install-codex-plugin.sh` 使用个人 marketplace、官方 cachebuster/validator 和 `codex plugin add`；当前本机 `butler@personal` 已安装。
- **边界**：Claude 能力未变。Codex hooks 尚未适配 `apply_patch`；目标项目双入口和统一 setup/upgrade 尚未接线。

## 活跃战线

- 下一项 R3：Codex PreToolUse/PostToolUse hooks、`apply_patch` patch 解析、共享规则判断复用和拒绝/提醒端到端验证。

## 下一个瓶颈

- 现有 `butler_gate.py` / `butler_advisor.py` dispatcher 只识别 Claude 工具名和 `tool_input.file_path`；需要在不改规则算法的前提下增加 Codex 协议适配。
- 本机 plugin validator 与最新 manual 对 manifest `hooks` 字段支持存在差异。R3 必须以当前 CLI 实装路径和验证结果为准，不能只写一个 validator 不接受的字段。
