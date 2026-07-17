# Goal

按已冻结的 AC1–AC9 交付 ITER-0051：增加 Codex 原生规则发现、目标项目入口模板和双宿主架构契约，同时用自动检查守住 `.ai/` 冷启动读序、`rule-card.md` 单一真源和 Claude Code 非回归；skills/plugin、Codex hooks、完整部署升级接线不提前进入本迭代。

# Files / Modules to Change

## 新增

- `AGENTS.md`（AC1/AC2）——Butler 规则仓的 Codex 原生入口。只放仓库定位、编辑硬约束、`.ai/` 冷启动读序和 `Coder/README.md` 深读指针，不复制完整规则算法。
- `templates/AGENTS.md.template`（AC3）——未来目标项目的 Codex 入口模板。与 `CLAUDE.md.template` 共用 `{{BUTLER_VERSION}}`、`{{RULE_CARD_CONTENT}}`、`{{BUTLER_PATH}}` 和 user-managed 保护区契约。
- `docs/codex-compatibility.md`（AC4/AC5）——双宿主兼容架构单一说明：共同内核、两端适配层、R1–R4 支持矩阵、hook 当前诚实边界和维护红线。
- `scripts/verify-codex-foundation.sh`（AC3/AC8）——零依赖结构检查，验证入口、读序、模板占位符、保护区、共同深读指针、规则卡未复制和文档注册。
- `migrations/v2.12.0.md`（AC9）——R1 发布配方；对既有部署项目明确 `[no-op]` + `[restamp]`，不假装已自动生成 `AGENTS.md`。

## 更新

- `README.md`（AC6）——在核心能力/快速上手/目录树中短注册 Codex R1 支持和兼容说明链接，不改 Claude 安装步骤。
- `Coder/README.md`（AC6）——在入口文档和支撑目录中登记 `AGENTS.md`、目标模板及兼容架构真源。
- `HUMAN_GUIDE.md`（AC5/AC6）——增加短小的“Codex 支持状态”说明：R1 能做什么、暂时不能做什么、完整兼容路线指向哪里。
- `VERSION`、`CHANGELOG.md`（AC9）——发布 v2.12.0。
- `.ai/**`、`deliveries/**`、`.ai/project/**`（P5 收口）——按既有原子收口仪式归档、交付和前滚长期知识，不属于产品接口。

## 明确不改

- `CLAUDE.md`、`.claude/commands/butler/*.md`。
- `templates/hooks/**`、`templates/settings.hooks-snippet.json`。
- `scripts/setup.sh`、`Coder/20_Workflow_Lifecycle/mcv-deployment.md`、`butler-upgrade.md`。
- P1–P5、四件套、PRD、危险模式、偏好探针等算法真源。

# Interface / Contract

## 仓根 `AGENTS.md`

- Codex 自动发现的仓库级指令文件；作用域覆盖整个 Butler 仓。
- 必须包含以下最小契约：
  - 规则仓定位与“编辑规则，不是用规则开发业务软件”的边界。
  - 根 `CLAUDE.md` 已有的 5 条编辑约束，不扩写为第二份规则体系。
  - `.ai/` 冷启动顺序：地图 → 两台账 → task-state/handoff → 当前四件套 → 规则真源。
  - `Coder/README.md` 为完整规则入口；按需读，不全量吞历史归档。
- 不依赖用户 `project_doc_fallback_filenames`，不使用 Claude 的 `@import` 语法。

## `templates/AGENTS.md.template`

- 生成输入与 Claude 模板一致：
  - `{{BUTLER_VERSION}}`：Butler 版本。
  - `{{RULE_CARD_CONTENT}}`：从 `templates/rule-card.md` 的 `## 角色` 起注入。
  - `{{BUTLER_PATH}}`：完整规则仓路径。
- user-managed 区必须由 `<!-- user-managed -->` / `<!-- /user-managed -->` 包围，未来升级必须逐字保留。
- 模板正文可以解释 Codex 的 `.ai/` 冷启动顺序，但不得内联第二份 `rule-card` 正文。
- 本迭代只提供模板契约；R4 才把模板接进首次部署和升级执行链。

## 兼容架构说明

- 共同内核：`Coder/`、`.ai/`、`templates/rule-card.md`、hook 的规则判断模块。
- Claude Code 适配层：`CLAUDE.md`、`.claude/commands/`、`.claude/hooks/`、Claude settings。
- Codex 适配层：`AGENTS.md`、skills/plugin、`.codex/hooks.json` 或 plugin hooks、Codex config/trust。
- 状态标记必须区分：R1 已完成；R2/R3/R4 计划中。不得用“全面兼容”描述 v2.12.0。

## 自检脚本

- POSIX/Bash、零第三方依赖，从仓根或任意 cwd 调用都先解析自身仓根。
- 失败返回非零并指出具体缺项；成功输出简短汇总。
- 不改文件、不调用网络、不启动模型，适合作为快速结构回归。

# State / Boundary

- `.ai/` 的结构和状态枚举完全不变；本轮只把既有恢复纪律暴露给 Codex。
- `AGENTS.md` 与 `CLAUDE.md` 是两个宿主入口，不互相 import；它们共同回指 `Coder/`，目标模板共同从 `rule-card.md` 注入强制规则。
- R1 不让目标项目自动获得 `AGENTS.md`：模板先落，执行接线归 R4。发布和 HUMAN_GUIDE 必须明确这一点。
- R1 不触碰 Codex hook：现有 Python gate 对 `apply_patch` 的输入不兼容，继续作为已知未完成项留给 R3。
- R1 不使用 plugin-creator；plugin 的目录、manifest、skills 和安装缓存流程只在 R2 开始时按对应 skill 执行。

# Design Decisions

1. **新增原生 `AGENTS.md`，不依赖 fallback。** fallback 需要每台机器改 Codex 配置，不能成为仓库共享契约；原生文件能随仓版本化。代价是多一个入口文件，靠“短入口 + 共同真源 + 自动检查”控制漂移。
2. **目标模板单独存在，但不复制规则卡。** `AGENTS.md.template` 与 `CLAUDE.md.template` 的宿主说明不同，强行合成一个模板会充满条件分支；两个薄模板更清楚。强制规则仍只从 `rule-card.md` 注入，自动检查共同占位和深读指针。
3. **兼容真源放 `docs/codex-compatibility.md`。** 它是跨 Coder/模板/安装层的宿主架构，不塞进 SOP Core；README/HUMAN_GUIDE/Coder 入口只登记和回指，避免三处重复。
4. **新增长期自检脚本。** 仅靠人读无法稳定守住两个模板的占位符和指针一致性；脚本以文本契约做确定性断言。代价是新增少量维护面，但比手工回归更低。
5. **R1 发布为真实但有限的 MINOR。** 仓库本身从 v2.12.0 起可被 Codex 原生发现，属于新增能力；目标项目自动部署、工作流和 hooks 尚未完成，发布文案必须限定范围。

# Execution Steps

- [x] **T1** 新增仓根 `AGENTS.md`，写入仓库边界、编辑约束和 `.ai/` 冷启动读序 → AC1/AC2
- [x] **T2** 新增 `templates/AGENTS.md.template`，复用版本/规则卡/路径占位符与保护区契约 → AC3
- [x] **T3** 新增 `docs/codex-compatibility.md`，落共同内核、双适配层、R1–R4 状态和 hook 诚实边界 → AC4/AC5
- [x] **T4** 新增 `scripts/verify-codex-foundation.sh`，覆盖入口、读序、模板、SSOT 和文档回指断言 → AC3/AC8
- [x] **T5** 更新 README、Coder 入口与 HUMAN_GUIDE，只做短注册并统一回指兼容真源 → AC5/AC6
- [x] **T6** 运行结构脚本、Markdown/路径检查、Claude 非回归 diff 和 Codex 新会话发现探测；发现问题只在冻结范围内修正 → AC1–AC8
- [x] **T7** 更新 VERSION/CHANGELOG/migration，发布 v2.12.0，并完成 P5 四件套、交付、台账、知识前滚和一致性自检 → AC9

# Verification Plan

- **AC1（auto·可靠）**：`test -f AGENTS.md`；结构脚本断言规则仓定位和编辑约束；从仓根启动新的 `codex exec`，让其列出发现的项目指令来源或复述仓库边界。
- **AC2（auto·可靠）**：结构脚本按顺序匹配 `.ai/project/00_INDEX.md`、两台账、task-state/handoff、四件套、`Coder/README.md`；检查未要求全量读取 `.ai/iterations/`。
- **AC3（auto·可靠）**：断言模板三个占位符、两个保护区标记和完整规则指针；比较两模板中的 `{{BUTLER_PATH}}/Coder/` 指针集合一致。
- **AC4/AC5（auto + 人读）**：检查架构文档包含共同内核/Claude/Codex/R1–R4/support status；人工核对没有复制规则算法，明确 `apply_patch` 未兼容。
- **AC6（auto·可靠）**：三份入口文档都链接 `docs/codex-compatibility.md`；全文搜索确保详细支持矩阵只在真源出现一次。
- **AC7（auto·可靠）**：`git diff --exit-code -- CLAUDE.md .claude templates/hooks templates/settings.hooks-snippet.json scripts/setup.sh`；运行 `python3 -m pytest templates/hooks/tests -q` 作为既有 hook 回归。
- **AC8（auto·可靠）**：`bash scripts/verify-codex-foundation.sh`、`git diff --check`、所有新增相对路径存在性检查。
- **AC9（auto·可靠）**：VERSION/CHANGELOG/migration/tag 四方一致；收口 6 不变量检查通过。

# Risks / Open Questions

- **无开放设计问题**：文件落点、R1 边界和版本策略已明确，待用户 P3 ACK。
- `codex exec` 探测依赖本机 Codex 登录和可用模型；若外部服务不可用，结构检查仍可给确定性证据，但 VERIFY_REPORT 必须把真实 Codex 启动探测标为未执行/受阻，不能假绿。
- 两模板的注释可能天然不同；自检只比较占位符和深读路径契约，不做整文件逐字相等，避免把宿主差异误判为漂移。
- v2.12.0 创建本地 tag 属发布动作；不会自动 push tag、合并分支或发布 marketplace，外部状态变化仍需用户另行授权。
