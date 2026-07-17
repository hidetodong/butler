---
状态: ack-frozen
ACK 日期: 2026-07-17
ACK 方式: dangerous-self-review
---

> ⚠️ 危险模式：本产物由模型自主 ACK（已过 dangerous-engine §5.1 自审门），未经用户逐项确认（ITER-0053，2026-07-17）。

# Goal

交付 Codex `apply_patch` 的 Butler PreToolUse 门禁和 PostToolUse 提醒，同时共享既有规则算法并保持 Claude 非回归。

# In Scope

- `apply_patch` patch parser / Context adapter。
- gate/advisor dispatcher 多 target 支持。
- ledger rules 的 patch 增量适配。
- plugin 默认 hooks + wrapper、结构验证、单元/集成/真实 Codex E2E。
- R3 文档、归档与 v2.14.0 发布。

# Out of Scope

- 拦截 Codex 所有可能写路径或把 Butler hook 说成 sandbox。
- R4 setup、MCV、目标项目生成 `.codex`/双入口、既有部署升级全链。
- 改 P1–P5 或规则判定语义。
- 远端 push/merge、公共发布。

# Acceptance Checklist

- [x] **AC1（patch parser）**：解析 add/update/delete/move、多文件和多 hunk；路径越界/绝对路径走现有 OUT_OF_CWD；非空 apply_patch 无合法 target 时 gate fail-closed。
- [x] **AC2（多 target 门禁）**：gate 接受 `apply_patch`，对每个 target 顺序运行原 RULE_MODULES，任一 deny 即整体 deny；拒绝信息包含 canonical tool 与命中 target。
- [x] **AC3（ledger 语义）**：apply_patch 修改 `.ai/ITERATIONS.md` 时，非法状态与双 active 能被拒绝；同一 patch 先关旧 active 再开新 active 可放行。
- [x] **AC4（advisor）**：PostToolUse apply_patch 可逐 target 运行 advisory；写 MILESTONE 且无 PRD 时输出 Codex 支持的 additionalContext JSON，坏输入仍 fail-open。
- [x] **AC5（Claude 非回归）**：Edit/Write/MultiEdit 行为与输出不变，原 109 tests 全过；新增测试后全套通过。
- [x] **AC6（plugin hooks）**：`plugins/butler/hooks/hooks.json` 默认发现 Pre/Post，matcher 命中 apply_patch；wrapper 在 BUTLER_PATH 缺失时 gate fail-closed、advisor fail-open；manifest 不声明 validator 拒绝的 hooks 字段且仍通过 validator。
- [x] **AC7（真实 deny E2E）**：更新并重装 plugin 后，在无四件套的隔离 git 项目用真实 Codex apply_patch 写源码，PreToolUse 阻断且文件不存在。
- [x] **AC8（真实 allow/advisor E2E）**：有冻结四件套时真实 apply_patch 写源码可成功；写 MILESTONE 时 PostToolUse 提醒进入 Codex 上下文或事件输出。
- [x] **AC9（边界文档）**：README/HUMAN/兼容说明/Hook README 登记 R3 能力、trust 与不完整拦截边界，继续把部署接线标 R4。
- [x] **AC10（发布收口）**：P5 完整强审 0 Must Fix；归档、交付、知识前滚、v2.14.0 四方一致和 6 不变量通过。

# Verification Method

- AC1–4：pytest 单元 + dispatcher subprocess 集成（可靠）。
- AC5：全套 pytest、旧 payload 定向 diff/断言（可靠）。
- AC6：JSON/路径/权限/validator + wrapper 缺 env 测试（可靠）。
- AC7/8：`codex exec --dangerously-bypass-hook-trust` 隔离项目真实 tool call（可靠/事件文本弱档）。
- AC9/10：结构脚本、文档断言、发布与台账检查（可靠 + 人读）。

# Open Questions / Risks

- 无开放范围问题。若真实 Codex 选择 Bash 而非 apply_patch，E2E prompt 必须限定“一次 apply_patch 后停止”，不能把模型选路差异误判为 hook 失败。
