# TECH_PLAN — ITER-0053

> ⚠️ 危险模式：本产物由模型自主 ACK（已过 dangerous-engine §5.2 自审门），未经用户确认（ITER-0053，2026-07-17）。

# Goal

以宿主输入适配层把 Codex apply_patch 转成既有 Context，不改规则判定层。

# Files / Modules to Change

- `templates/hooks/lib/codex_patch.py`：patch section/hunk 增量 parser。
- `templates/hooks/lib/io.py`：payload → 一个或多个 Context 的宿主适配接口。
- `templates/hooks/butler_gate.py` / `butler_advisor.py`：多 Context dispatch。
- `templates/hooks/rules/{ledger_status,single_active_iteration}.py`：读取 adapter 提供的 added/removed 增量。
- `templates/hooks/tests/**`：parser、gate、advisor、ledger Codex cases。
- `plugins/butler/hooks/`：默认 hooks.json + gate/advisor wrappers。
- `scripts/verify-codex-hooks.sh`、文档、发布/交付/台账。

# Interface / Contract

- `parse_patch(command) -> list[PatchChange]`；每个 change 含 path、operation、added_lines、removed_lines。move 同时产生 source delete 与 destination add/update target，确保两端都受 protected/phase 检查。
- `contexts_from_payload(payload) -> list[Context]`：Claude 返回单 Context；apply_patch 返回每 target 一个 Context，synthetic tool_input 保留原 command 并加 `butler_patch_*` 内部字段。
- apply_patch command 非空但 parser 无 target：抛异常；gate 捕获后 exit 2，advisor 捕获后 exit 0。
- dispatcher 对 contexts 外层循环、rules 内层循环；先出现的 deny 立即结束。
- plugin `hooks/hooks.json` 使用 `Edit|Write` matcher；command 调 wrapper，wrapper 再从 `BUTLER_PATH` exec Python 真源。

# State / Boundary

- rules 的 verdict 与优先级不变；Codex adapter 只提供等价输入。
- PostToolUse 只提醒，绝不撤销或阻断已执行 patch。
- trust bypass 只用于 E2E 命令，不写入产品配置。
- R4 前不把 hooks 复制进目标项目 `.codex/`。

# Design Decisions

1. **parse once, evaluate many。** 多文件 patch 不能只取第一个路径；每 target 独立 Context 最直接复用现有规则。
2. **增量而非完整 patch 应用器。** ledger 不需要重放所有文本位置，只需用 removed/added 行更新 active 集合与扫描新增状态；比实现完整 patch engine 更小、更稳。
3. **默认 plugin hook discovery。** 放 `hooks/hooks.json`，不写 manifest hooks 字段，兼容当前 validator 与最新运行时。
4. **wrapper 明确风险方向。** gate 缺 BUTLER_PATH 退出 2，advisor 缺路径退出 0，与现有 fail-closed/fail-open 对称。
5. **v2.14.0 MINOR。** 新增 Codex 机械门禁能力，但明确不是完整 enforcement boundary。

# Execution Steps

- [x] **T1** 实现 patch parser 与 Context adapter，先写覆盖 grammar 的测试 → AC1
- [x] **T2** 改 gate/advisor 多 target dispatch 并补 subprocess tests → AC2/4/5
- [x] **T3** 适配 ledger_status/single_active_iteration patch 增量 → AC3/5
- [x] **T4** 增 plugin default hooks/wrappers 与结构验证 → AC6
- [x] **T5** 更新 plugin 版本、真实重装并跑 deny/allow/advisor E2E → AC7/8
- [x] **T6** 更新边界文档，跑完整回归与 P5 强审 → AC5/9/10
- [x] **T7** 归档交付、发布 v2.14.0 并自动进入 R4 → AC10

# Verification Plan

- pytest 覆盖 parser 6 类、dispatcher 多文件、ledger 三路径、advisor fail-open。
- 原 109 tests + 新 tests 全过。
- plugin validator、R1/R2/R3 三个 verify scripts。
- 三个真实 Codex fixture：deny、allow、advisor。
- `git diff --check`、版本/tag/台账/知识 6 不变量。

# Risks / Open Questions

- 独立复核受团队策略限制不启动子 agent；主代理执行完整强审并披露。
- E2E hook trust 使用官方测试开关，不能证明用户已在交互 UI 审阅信任；文档需保留人工 trust 步骤。
