# TECH_PLAN — ITER-0052

> ⚠️ 危险模式：本产物由模型自主 ACK（已过 dangerous-engine §5.2 自审门），未经用户确认（ITER-0052，2026-07-17）。

# Goal

以单一实体 skill 源交付可安装的 Butler plugin 和仓库 fallback，覆盖 AC1–AC10。

# Files / Modules to Change

- `plugins/butler/.codex-plugin/plugin.json`：plugin manifest。
- `plugins/butler/skills/butler-*/`：8 个 skill 及 `agents/openai.yaml`。
- `.agents/skills/butler-*`：指回 plugin skills 的相对软链。
- `scripts/install-codex-plugin.sh`、`scripts/verify-codex-workflows.sh`：个人安装/刷新与结构验证。
- `docs/codex-compatibility.md`、README/Coder/HUMAN_GUIDE：R2 状态与入口注册。
- 发布、交付、`.ai/**`：v2.13.0 收口。

# Interface / Contract

- skill 名统一为 `butler-<command>`，避免与通用 skill 撞名；描述前置触发语义。
- skill 从环境变量 `BUTLER_PATH` 定位规则仓；缺失或路径无效时停止 Butler 专用流程，给出 `scripts/setup.sh` / 仓路径设置提示，不臆造规则。
- `agents/openai.yaml` 只含 interface 与 invocation policy；默认 prompt 必须显式包含 `$butler-<command>`。
- plugin manifest 的 `skills` 为 `./skills/`；不声明 R2 未提供的组件。
- 安装脚本默认把 repo plugin 同步到 `~/plugins/butler`（个人 marketplace 的 `./plugins/butler` 由 CLI 相对 HOME 解析），用官方 scaffold/helper 管 marketplace/cachebuster，再调用 `codex plugin add butler@<marketplace-name>`；隔离测试通过临时 HOME 完成，避免污染真实配置。

# State / Boundary

- plugin skill 是物理真源，repo skill 是软链；不得出现第二套 SKILL.md。
- plugin 安装缓存是派生物，不纳入 Git；仓库源与个人 marketplace 副本可由脚本重复同步。
- R2 不修改 hook、setup、MCV 或 Claude command。

# Design Decisions

1. **plugin 内 canonical、repo 外层软链。** plugin 可独立打包，Codex 又能在仓内直接发现；代价是 Git/平台需支持 symlink，验证脚本机械兜底。
2. **8 个独立 focused skills。** 对应用户已有心智模型和命令边界，避免一个巨型 skill 在隐式触发时加载无关内容。
3. **高风险 skill 禁隐式。** loop/dangerous 的“郑重显式触发”不能因迁到 Codex 降门槛；其余工作流保持自然语言发现能力。
4. **安装脚本走官方 helper/CLI。** 初建 marketplace 使用 `plugin-creator`，更新使用 cachebuster helper，不手改 config；脚本只编排可重复步骤。
5. **R2 v2.13.0 MINOR。** 新增可安装工作流入口，不破坏 Claude 与部署项目契约。

# Execution Steps

- [x] **T1** 用官方 plugin scaffold 在 `plugins/` 创建 Butler + skills 骨架 → AC1
- [x] **T2** 用 `init_skill.py` 初始化并实现 8 个薄 skills/metadata → AC2/3/4
- [x] **T3** 建 `.agents/skills` 8 个相对软链并验证唯一实体源 → AC5
- [x] **T4** 实现个人安装/刷新脚本与结构验证脚本 → AC6
- [x] **T5** 更新四份支持文档并守住 R3/R4 边界 → AC9
- [x] **T6** 隔离安装测试、真实个人安装与新 Codex 触发验证 → AC1–7
- [x] **T7** 跑 Claude 非回归、P5 强审并修复 Must Fix → AC8/10
- [x] **T8** 归档交付、切 v2.13.0、提交/tag 与 6 不变量检查 → AC10

# Verification Plan

- 官方 plugin validator + 8 次 quick validator。
- `scripts/verify-codex-workflows.sh` 从仓根和 `/tmp` 各跑一次。
- 隔离 HOME/BUTLER_CODEX_HOME 连跑安装脚本两次，核幂等、marketplace 保留与缓存版本。
- 真实 `codex plugin list` 和两个 `codex exec` 探测。
- Claude 定向 diff、109 hook tests、`git diff --check`。

# Risks / Open Questions

- 无开放设计问题。若 CLI 的个人 marketplace 实际解析与脚手架契约冲突，以本机官方 helper/CLI 实测为准，并把差异记入 VERIFY_REPORT，不绕过 validator。
- 危险模式 P5 按规则应建议 fresh-context 独立复核；当前团队策略不允许无明确委派的子 agent，因此执行主代理完整多维强审并如实披露，绝不冒称独立。
