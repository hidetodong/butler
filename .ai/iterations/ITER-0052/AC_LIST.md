---
状态: ack-frozen
ACK 日期: 2026-07-17
ACK 方式: dangerous-self-review
---

> ⚠️ 危险模式：本产物由模型自主 ACK（已过 dangerous-engine §5.1 自审门），未经用户逐项确认（ITER-0052，2026-07-17）。

# Goal

交付 MILE-0006 R2：8 个 Codex skills、可验证的 Butler plugin、repo fallback 与个人安装/刷新路径，同时保持共同真源和 R3/R4 边界。

# In Scope

- `plugins/butler/` plugin 包与 8 skills。
- `.agents/skills/` repo discovery 软链。
- 安装/更新与结构验证脚本。
- 当前支持状态的最小文档注册、v2.13.0 发布与迭代收口。

# Out of Scope

- Codex hooks / `apply_patch` 适配（R3）。
- `setup.sh`、MCV、目标项目双入口部署/升级（R4）。
- Claude commands 或 `Coder/` 算法改写。
- 公共 marketplace、远端 push/merge。

# Acceptance Checklist

- [x] **AC1（plugin 骨架）**：`plugins/butler/.codex-plugin/plugin.json` 由官方脚手架产生并通过官方 validator；name/version/interface/skills 路径有效，无 TODO、hooks、MCP、apps 假声明。
- [x] **AC2（8 skills 齐全）**：plugin 内恰有 prd/review/milestone/upgrade/ideation/preference/loop/dangerous 八个 skill；每个含合法 `SKILL.md` 与 `agents/openai.yaml`，通过 `quick_validate.py`。
- [x] **AC3（薄适配单一真源）**：8 skills 只负责触发、定位 `BUTLER_PATH`、读取对应 `Coder/` 真源、按需分派与优雅降级；不复制 P1–P5、风险护栏或工作流算法。
- [x] **AC4（触发安全）**：6 个低风险 skill 允许隐式触发；`butler-loop`、`butler-dangerous` 明确禁隐式调用，只能显式 `$skill`，且保留风险回声与引擎闸。
- [x] **AC5（repo fallback）**：`.agents/skills/` 恰有 8 个相对软链，全部解析到 plugin 的同名 skill；仓内启动 Codex 可发现，无第二份实体 SKILL.md。
- [x] **AC6（安装/更新路径）**：提供幂等脚本，把当前 plugin 同步到个人 marketplace 约定位置、通过官方 helper 更新 cachebuster、用 `codex plugin add` 安装；不得手改既有 marketplace 更新流。
- [x] **AC7（真实 Codex 验证）**：安装后 `codex plugin list` 能看到 Butler；新 `codex exec` 显式调用至少覆盖一个普通 skill 和一个高风险 skill 的只读/status 路径，并准确回指真源。
- [x] **AC8（Claude 非回归）**：`CLAUDE.md`、`.claude/**`、`templates/hooks/**`、`scripts/setup.sh` 与 Python gate 行为不变；109 个既有 hook 测试通过。
- [x] **AC9（文档与边界）**：兼容说明、README、Coder README、HUMAN_GUIDE 登记 R2 已完成和安装入口，同时继续明确 hooks=R3、部署升级=R4。
- [x] **AC10（发布收口）**：P5 强制完整审查无 Must Fix；归档/交付/台账/知识前滚完成，VERSION/CHANGELOG/migration/tag 对齐 v2.13.0，工作树干净。

# Verification Method

- AC1/2/5/6：官方 validator、skill quick validator、symlink/readlink 和幂等脚本测试（auto·可靠）。
- AC3/4：结构脚本 + 定向人读，搜索禁止复制的算法段和 invocation policy（auto + 人读）。
- AC7：真实 CLI 安装、`codex plugin list`、全新 `codex exec` 探测（auto·可靠；语义触发只作补充）。
- AC8：定向 git diff + `uv run --with pytest pytest templates/hooks/tests -q`（auto·可靠）。
- AC9/10：路径/文案断言、发布四方一致与 6 不变量检查（auto·可靠）。

# Open Questions / Risks

- 官方 manual 与本机 plugin validator 对 manifest `hooks` 字段存在版本差异；R2 完全不声明 hooks，R3 再按当时 CLI/validator 实测决定接线形式。
- 本机个人 marketplace 若已有同名 Butler 条目，安装脚本必须显式覆盖自己的条目而不改其他条目顺序或 metadata。
