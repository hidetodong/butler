# VERIFY_REPORT — ITER-0052

> 2026-07-17 · 危险模式 P5 完整强审 · 结论：AC1–AC10 通过，0 Must Fix。

## 验收结果

| AC | 结果 | 证据 |
|---|---|---|
| AC1 | ✅ 可靠 | 官方 `plugin-creator` 脚手架生成；`validate_plugin.py` 在 PyYAML 隔离环境通过。manifest 为 Butler 2.13.0，只声明 `skills`，无 TODO/hooks/MCP/apps。 |
| AC2 | ✅ 可靠 | 8 个 skill 恰好齐全；8 次 `quick_validate.py` 全部 `Skill is valid!`。 |
| AC3 | ✅ 可靠 + 人读 | 每份 SKILL.md 仅 5 步左右，统一定位 `BUTLER_PATH` 并回指 `Coder/`；定向审查未发现 P1–P5、PRD、复核或危险算法复制。 |
| AC4 | ✅ 可靠 | 6 个低风险 skill 保持默认隐式资格；loop/dangerous 的 `agents/openai.yaml` 均为 `allow_implicit_invocation: false`，结构脚本机械断言。 |
| AC5 | ✅ 可靠 | `.agents/skills/` 恰有 8 个相对软链，逐个解析到 `plugins/butler/skills/`，无第二份实体 SKILL.md。 |
| AC6 | ✅ 可靠 | 隔离 HOME 连跑安装两次成功，marketplace 只有一个 Butler 条目、cachebuster 单 suffix、两次均 installed/enabled；真实 HOME 安装成功。安装器增加版本精确后置断言，防 CLI 假成功。 |
| AC7 | ✅ 普通入口可靠；高风险入口弱 | `/tmp` 新 `codex exec` 自动从 plugin cache 加载 `$butler-review` 并读对真源；`$butler-dangerous` 因禁隐式未出现在非交互 catalog，但定向定位已安装 skill 后准确回报两真源和禁隐式策略。交互 UI 的 mention 注入待人补测，不放宽风险门。 |
| AC8 | ✅ 可靠 | Claude 定向 diff 为空；`uv run --with pytest pytest templates/hooks/tests -q` 为 109 passed。 |
| AC9 | ✅ 可靠 + 人读 | README、Coder README、HUMAN_GUIDE、兼容说明均登记 `plugins/butler/`，继续明确 hooks=R3、部署=R4。 |
| AC10 | ✅ 可靠 | 完整多维强审 0 Must Fix；归档、交付、v2.13.0 四方一致与 6 不变量在发布后复核。 |

## 自动验证

- `bash scripts/verify-codex-foundation.sh` → PASS。
- `bash scripts/verify-codex-workflows.sh`（仓根与 `/tmp`）→ PASS，8 skills。
- 官方 plugin validator + 8 个 skill validators → 全过。
- 隔离 HOME 安装器 ×2 + `codex plugin list --json` → 同名条目唯一、两版 cache 均正确刷新、最终 installed/enabled。
- 真实个人安装 → `butler@personal` installed/enabled。
- `bash -n`、`git diff --check` → PASS。
- Claude hook tests → 109 passed。

## 完整审查

- 逻辑健壮性：安装器对源/目标同路径、根目录、缺 helper、CLI 假成功均有阻断；更新使用官方 cachebuster/helper/CLI。
- 可读性：8 skills focused、命名统一，详细算法留在真源。
- 性能：安装只复制小型 Markdown plugin；validator 开销可接受。
- 安全：高风险 skill 禁隐式；安装仅接管个人 marketplace 的 Butler 条目和 `~/plugins/butler`，不改其他 plugin 条目。
- 独立复核：未执行。当前团队策略不允许未经明确委派启动子 agent；本报告是主代理完整强审，不冒称独立。

## Remaining Risks

- **Should Fix / 待人**：Codex 非交互 `exec` 对 `allow_implicit_invocation:false` skill 的纯文本 `$mention` 没像普通 skill 一样直接注入 catalog；交互式 `/skills` 或桌面 app mention 需用户后续补测。安全上宁可保持显式门，不为测试便利放宽。
- plugin 依赖 `BUTLER_PATH`；全新 Codex-only 机器的统一环境安装归 R4，当前安装器适用于已配置 Butler 路径的维护者环境。
