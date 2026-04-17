# Session Handoff

## 任务断点

butler 规则仓当前状态：**v0.2.0 Harness 升级 Phase 1 完成**（merge commit `170f974`，tag `v0.2.0-phase1-hook-gate`）。

在 `v0.1.1-upgrade-protocol`（基地车生命周期三阶段齐备）之后，启动 **Butler Harness 升级 8-phase roadmap**，把工程 SOP 从 prompt-only 升级为 prompt + hook 双层执行。本轮完成 Phase 1 —— Claude Code PreToolUse hook 机制化拦截。

**Roadmap 进度**：

| Phase | 子系统 | 状态 |
|---|---|---|
| 1 | Hook-based 硬门控 | ✅ 本轮完成 |
| 2 | 工具亲和力矩阵 | ⏸ 排队中（依赖 Phase 1 hook 机制） |
| 3 | 按阶段裁剪 context 加载 | ⏸ |
| 4 | 失败模式目录 & 升级到人 | ⏸ |
| 5 | SESSION_HANDOFF 结构化 | ⏸ |
| 6 | 沙盒 & 可逆性默认 | ⏸ |
| 7 | 遥测 RUN_LOG | ⏸（RUN_LOG 种子已在 Phase 1 落地） |
| 8 | 规则自测 fixture | ⏸ |

Phase 1 产物：`templates/hooks/`（Python 模块化 dispatcher + 3 rules + 2 lib helpers + 63 pytest 测试 + smoke.sh），`templates/settings.hooks-snippet.json`，`mcv-deployment.md §5`。

## 关键决策摘要

### Phase 1 Harness 机制层

- **生效范围**：只在 `/mcv-deploy` 部署后的目标项目生效（α 方案）；butler 仓自身 dogfood 后置。
- **拦截范围（本轮）**：`Edit` / `Write` / `MultiEdit` 三件工具；Bash 写入边缘场景延后到 Phase 6/H。
- **三类违规**：
  - (a) 跳过 P1/P2：源码路径写需 `.ai/CONCEPT.md` + `AC_LIST.md` + `TECH_PLAN.md` 三者齐全且非空
  - (c) 业务扩展：`99_Business_Extension/` 直接拦（不碰 `.ai/` schema 保护——留到 Phase 4+ 与 mcv-update 联动）
  - (e) 产物链断裂：本轮仅 **存在性降级**；内容级 AC-ID linkage 作为独立后置 sub-project
- **Bypass 契约**：`BUTLER_BYPASS=1` + `.ai/bypass-reason.md`（strip 后非空）→ allow + 追加 `.ai/RUN_LOG.md`；reason 不自动清理（低摩擦优先）。
- **Fail-closed**：dispatcher 顶层 `try/except` → `exit 2`；bypass 通道兜底逃生。
- **黑名单路径**：`.ai/` / `deliveries/` / `.claude/` / `.git/` / `node_modules/` / `.vscode/` / `.idea/` 免检（硬编码在 `lib/io.GATED_BLACKLIST`，待 Phase 3 配置化）。
- **RUN_LOG 行格式**：`<ISO-UTC> | <rule_id> | <tool_name> | <relative_target> | <sanitized_reason_first_line>`（pipe 被转义为 `/`，控制字符去除，200 字符截断加 `…`）。
- **SSOT 策略**：`templates/hooks/` 是真源，mcv-deployment §5.1 整体拷贝（不软链）；`settings.hooks-snippet.json` 按 `matcher` 字面幂等合并。

### 产物组织约定（本轮新增）

- Harness 升级的 spec/plan 统一落到 `docs/superpowers/{specs,plans}/`，日期前缀命名（`YYYY-MM-DD-<topic>-design.md` / `-<topic>.md`）。
- brainstorming → writing-plans → subagent-driven-development skill 链条适配本仓库：spec 审完 user gate，plan 自审再 user gate，实施用 fresh subagent per task + two-stage review。

### 沿袭自前代的决策（未变）

- 基地车三阶段：`mcv-deployment.md`（部署）/ `butler-upgrade.md`（跨版本升级）/ `mcv-update.md`（`.ai/` 内部维护）。
- 保护区契约：`<!-- user-managed -->` / `<!-- /user-managed -->` 包裹 CLAUDE.md 的"项目特定约束"章节。
- 模板 SSOT：`rule-card.md` 是浓缩规则真源；`CLAUDE.md.template` 通过 `{{RULE_CARD_CONTENT}}` 占位符引用。
- 术语契约：Mode = 运行时能力（与 /xxx 命令绑定）；Role = 职责切换（与 P1-P5 阶段映射）。

## 环境脏点

- **所有 milestone tag 此前均未 push 到 remote**（`v0.0.8`、`v0.1.0-first-stable`、`v0.1.1-upgrade-protocol`、`v0.2.0-phase1-hook-gate`）；本轮一起推。
- **本地 main 超前 origin/main 17 commits**（含本轮 Phase 1 merge + 前代 v0.1.1 相关提交）；本轮一起推。
- `.claude/settings.local.json` 未 gitignore（Claude Code 本地权限，按惯例不提交）。
- `templates/hooks/README.md` 中 "已测试的 Claude Code 版本" 字段仍是 `待补`，等首次真实 `/mcv-deploy` dogfood 后填入确认过的 Claude Code 版本号。
- `templates/hooks/conftest.py` 是空文件（顶层占位，final code review 判定无害保留）。

## 已知风险

- **Phase 1 hook 未在真实 Claude Code PreToolUse 场景下跑过**：subprocess 集成测试 + 端到端 smoke 都是手工 stdin 喂 JSON 模拟；真实 Claude Code 可能有 payload 字段命名 / 路径怪事 / env 继承差异。**首次 `/mcv-deploy` dogfood 是关键下一步**。
- **`protected_paths.PROTECTED_PREFIXES`** 当前硬编码仅 `99_Business_Extension/`。Phase 2+ 增加保护前缀时，要考虑是否中心化到 `lib/io.py`。
- **Phase 1 未做 butler-upgrade 的 hooks 版本同步**：hook 副本与 SSOT 漂移时无检测。跟踪为 follow-up，待 Phase 1 dogfood 稳定后处理。
- `/butler-upgrade` 协议**至今仍未在老项目上实跑**，v0.1.1 的遗留 dogfood 债；Phase 1 上线后，这一风险同时存在。
- `scripts/setup.sh` Linux 分支仍未真机验证（v0.1.1 遗留）。

## 唤醒指令

新会话从项目 `CLAUDE.md` + `Coder/README.md § 读取顺序` 建立上下文。

**若要推进 Phase 2（工具亲和力矩阵）**：
- 从 `docs/superpowers/specs/2026-04-17-butler-hook-gate-design.md §8.3` 读取扩展点
- 走 brainstorming → spec → plan → impl 同一链条
- Phase 2 设计时注意：`rules/` 新增 rule module 即可，dispatcher 的 `RULE_MODULES` 自动分发；不需要动 bypass / io 基础设施

**若要先 dogfood Phase 1**：
- 选一个真实老项目或 throw-away 项目
- 先执行 `/mcv-deploy`（或手工按 `mcv-deployment.md §5.1-5.2` 拷文件 + 合并 settings.json）
- 在其中跑一轮完整 P1-P5 任务，观察 hook 行为
- 发现 bug → bugfix commit 到 main；把真实版本号填入 `templates/hooks/README.md`

**若要实跑 `/butler-upgrade`**（v0.1.1 遗留）：先找老项目，让 AI 按 `butler-upgrade.md §3` 侦察 → §4 或 §5 执行。

## 状态指针

- 最新产物链：`.ai/{CONCEPT, AC_LIST, TECH_PLAN, VERIFY_REPORT}.md`（对应 `/butler-upgrade` feature 轮次，**未 checkpoint 本轮 Phase 1**——本轮走 spec/plan 而非产物链四件套）
- 本轮 spec：`docs/superpowers/specs/2026-04-17-butler-hook-gate-design.md`
- 本轮 plan：`docs/superpowers/plans/2026-04-17-butler-hook-gate.md`
- 历史决策链：`git log --oneline v0.0.2..HEAD`（10+ 轮提交 + 4 个 milestone tag）
- 人类可读归档：`deliveries/` 下 9 份 Delivery Summary（8 审计修复 + 1 v0.1.1 feature；**Phase 1 尚未补 delivery summary**，可作 follow-up）
