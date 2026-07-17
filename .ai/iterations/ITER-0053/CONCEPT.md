# CONCEPT — ITER-0053 · Codex hooks

> ⚠️ 危险模式：本迭代由模型自治推进；P2/P3 经强制自审门后自主 ACK。

## 一句话目标

让 Butler 的同一套 gate/advisor 真正识别 Codex `apply_patch`，并通过已安装 plugin 的生命周期 hooks 在写入前阻断、写入后提醒。

## 已确认事实

- Codex `PreToolUse` / `PostToolUse` 对文件编辑报告 `tool_name: apply_patch`，patch 文本在 `tool_input.command`。
- matcher 可写 `Edit|Write` 命中 `apply_patch`；PreToolUse 可用 exit 2 + stderr 拒绝，PostToolUse 可输出 `hookSpecificOutput.additionalContext`。
- plugin 默认发现 `hooks/hooks.json`，无需 manifest `hooks` 字段；这绕开当前本机 validator 拒绝该字段而最新 manual 又支持它的版本差异。
- plugin hooks 必须经 trust；自动 E2E 可用官方 `--dangerously-bypass-hook-trust` 只在测试命令中绕过交互审阅。

## 设计方向

1. 新增 Codex patch parser，把一个多文件 patch 拆成多个 target Context；dispatcher 逐 target 复用现有规则，第一条 deny 胜出。
2. parser 为每个 target 提供 added/removed 行和 operation；ledger rules 用这些增量还原/检查状态，不复制规则算法。
3. Claude `Edit/Write/MultiEdit` 路径保持原样，旧 109 测试必须全过。
4. plugin 只加默认 hooks 配置与薄 shell wrapper，Python 真源仍在 `BUTLER_PATH/templates/hooks/`。
5. R3 发布 v2.14.0；R4 才做 setup/MCV/目标项目部署升级和整体双端矩阵。

## 风险

- `apply_patch` grammar 包含 add/update/delete/move 与多 hunks；漏解析 target 会让 gate 静默放行，parser 遇到非空但无合法 target 必须让 gate fail-closed。
- PreToolUse 不是完整安全边界，官方说明 unified exec/等价工具仍可能绕过；文档必须叫“支持的 apply_patch 路径机械门禁”，不能写成不可绕过安全沙箱。
- plugin hook trust 由 Codex 管理，安装不能替用户静默信任。
