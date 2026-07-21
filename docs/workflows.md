# Butler 双宿主工作流注册表

> 本页由 `workflows/registry.json` 通过 `scripts/sync-workflow-registry.py --write` 生成，请勿手改。机器 registry 是元数据真源；本页是唯一八项人读能力表。

| ID | Claude Code | Codex | 风险 | 隐式调用 | 语义触发 | 旧名 / 兼容 | 规则真源 |
|---|---|---|---|---|---|---|---|
| prd | `/butler:prd` | `$butler-prd` | normal | 允许 | `PRD`、`产品需求文档`、`split PRD`、`update PRD`、`PRD status` | `/butler-prd` (deprecated)<br>`/prd` (natural-language-compat) | `Coder/40_Context_Management/references-schema.md` |
| review | `/butler:review` | `$butler-review` | normal | 允许 | `review`、`代码复核`、`产物复核`、`independent review` | `/review` (natural-language-compat) | `Coder/60_Extension_CodeReview/review-engine.md` |
| milestone | `/butler:milestone` | `$butler-milestone` | normal | 允许 | `milestone`、`里程碑`、`roadmap`、`multi-iteration`、`milestone backlog`、`里程碑候办`、`多方向候办`、`one direction per draft` | `/milestone` (natural-language-compat) | `Coder/20_Workflow_Lifecycle/milestone-schema.md` |
| upgrade | `/butler:upgrade` | `$butler-upgrade` | normal | 允许 | `upgrade Butler`、`升级 Butler`、`同步 Butler`、`version gap` | `/butler-upgrade` (deprecated) | `Coder/20_Workflow_Lifecycle/butler-upgrade.md` |
| init | `/butler:init` | `$butler-init` | normal | 允许 | `init`、`initialize`、`初始化`、`部署基地车`、`deploy Butler`、`setup Butler`、`bootstrap` |  | `Coder/20_Workflow_Lifecycle/mcv-deployment.md` |
| ideation | `/butler:ideation` | `$butler-ideation` | normal | 允许 | `brainstorm`、`脑暴`、`需求还没想清`、`refine idea` | `/ideation` (natural-language-compat) | `Coder/50_Extension_Ideation/ideation-engine.md` |
| preference | `/butler:preference` | `$butler-preference` | normal | 允许 | `preference`、`偏好探针`、`reback`、`distill preference` | `/preference` (natural-language-compat) | `Coder/70_Extension_Preference/preference-probe-engine.md` |
| loop | `/butler:loop` | `$butler-loop` | high | 禁止（必须显式） | `$butler-loop`、`/butler:loop`、`死磕`、`explicit convergence loop` | `/loop` (harness-collision-do-not-generate) | `Coder/55_Extension_ConvergenceLoop/convergence-loop-engine.md` |
| dangerous | `/butler:dangerous` | `$butler-dangerous` | high | 禁止（必须显式） | `$butler-dangerous`、`/butler:dangerous`、`危险模式`、`explicit unattended autonomy` | `/dangerous` (deprecated-do-not-generate) | `Coder/65_Extension_Dangerous/dangerous-engine.md` |
| progress | `/butler:progress` | `$butler-progress` | normal | 允许 | `progress`、`进度`、`项目进度`、`current status`、`当前状态`、`how is it going` |  | `.claude/commands/butler/progress.md` |

## 安全与兼容

- `loop` / `dangerous` 是 high risk，Codex `allow_implicit_invocation=false`；只能由用户显式点名 Butler 模式。旧 `/loop` 与 Claude harness 自带循环撞名，绝不生成旧实体命令。
- 其余六项显式 `allow_implicit_invocation=true`，仍须按各自 SKILL description 的语义边界触发。
- legacy alias 是识别/弃用元数据，不代表仓库重新创建同名入口。

## 发现与分发状态

| 层 | 当前状态 | 真源 / 边界 |
|---|---|---|
| Claude 全局命令 | available via setup symlink | `.claude/commands/butler/` → `scripts/setup.sh` |
| Codex repo discovery | available | `.agents/skills/` 的 10 个相对软链，实体在 `plugins/butler/skills/` |
| Codex personal plugin | available via explicit installer | `scripts/install-codex-plugin.sh` + personal marketplace；安装副本单独 cachebuster |
| Plugin hooks | declared via standard auto-discovery | `plugins/butler/hooks/hooks.json`；不向 `plugin.json` 塞不受支持字段 |
| Team/public distribution | **not configured** | 没有团队 marketplace / 公共发布；个人已安装不等于团队可用 |
