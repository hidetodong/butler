# CONCEPT — ITER-0059 · 可执行升级器

> 分流: 完整 | 命中升级信号: 新增迁移执行器、历史兼容、事务写入 | 2026-07-18

## 一句话

把 Butler 升级从“模型读 Markdown 后临场照做”改成仓库程序按结构化动作先规划、再安全执行。升级结果要能复跑、能停在冲突前、失败能恢复，并且每个结论都有机器证据。

## Goal

- G1：建立机器可读迁移台账，明确版本区间、动作参数、前置条件和执行域，不再解析迁移散文决定写什么。
- G2：提供默认零写入的 inspect/dry-run，以及显式 apply；计划与执行日志可审计且结果确定。
- G3：项目内变更先全量预检、再原子落地；冲突在写入前停机，意外失败恢复到执行前字节状态。
- G4：把可机械执行、需人工决定和机器级外部动作分开，绝不以“已升级”掩盖 `[split]`、首次无戳项目或全局安装的未决状态。
- G5：用历史项目 fixture 跑通跨版本、幂等、漂移、用户区保护与故障注入，并通过现有证据链记录验证事实。

## Current Understanding

- `butler-upgrade.md` 当前让模型扫描版本戳、收集 `migrations/v*.md`、解释 typed 标签并手工执行；仓库没有可调用的升级程序、结构化 plan、运行 journal 或自动恢复。
- Markdown 配方不能安全充当程序输入：`v2.13.0`、`v2.14.0` 缺 `## 迁移步骤`，`v2.6.0` 使用非 schema 标签 `[global-install-rerun]`，而标签还会在说明段落中出现。
- 现有 renderer 已能同时维护 CLAUDE.md/AGENTS.md、保护各自 user-managed 内容并拒绝异常 marker；它适合作为入口重生成动作的底层能力，但当前 CLI 直接写入且未暴露 dry-run/事务接口。
- hook 同步与 settings 合并已有文字契约，尚无共享的确定性实现；全局安装会修改用户 HOME，不能与目标项目事务伪装成同一回滚单元。
- `[split]` 是内容语义重组且按既有规则必须 opt-in；程序可以记录“现在迁/暂缓”的决定并在未决时停机，但不能假装已理解并安全拆分任意用户知识。
- 无版本戳的首次升级缺少确定的迁移链起点，应进入明确的 manual-bootstrap 状态，不应默认覆盖。

## Constraints

- 所有目标路径先经唯一 `PROJECT_ROOT` 解析；不得把启动 cwd 当施工根，不得对 Butler 规则仓自身运行目标项目升级。
- `origin/`、`deliveries/`、迭代历史和用户管理区不属于升级器自由改写范围；入口保护区必须逐字保留。
- dry-run 对目标项目与用户 HOME 都零写入；apply 必须显式触发，不能因“检测到可升级”自动修改。
- 项目内动作、人工决策、机器级外部动作必须在 plan/journal 中分域；默认 apply 不修改 HOME。
- 未知 action、清单缺口、版本前向、marker 漂移、路径逃逸、软链越界和部分成形目标均 fail-closed，不静默跳过。
- 复用 Python 3.12/uv 锁定验证环境和 ITER-0057 evidence runner；不得新增浮动依赖。
- 本轮不发布、不提交、不推送，也不推进 R5。

## Impact Scope

- 新增：机器迁移台账、升级 CLI、事务/备份/journal 模块、历史 fixture 与专项测试。
- 修改：入口 renderer 暴露可复用 plan 能力；hook/settings 同步形成可测试实现；升级命令/skill、升级协议、迁移 schema 和人读迁移配方接到程序真源。
- 验证：把升级器专项并入 `verify-ci.sh` 的现有完整矩阵，并用 evidence records 覆盖成功与失败路径。
- 不影响：P1–P5 核心语义、业务工作流、历史 deliveries/origin 内容、GitHub 远端配置和 R5 注册表。

## Project Type / Active Profiles

- 项目类型：Markdown 规则仓 + Python/Bash 工具 + Claude/Codex 双宿主适配。
- Active Profiles：无；遵循通用路径安全、事务写入、兼容性和证据化验证纪律。

## Open Questions

- P3 决定机器台账采用单一 manifest 还是分版本 sidecar；选择标准是 schema 可验证、diff 易审查、历史版本覆盖完整。
- P3 决定执行 journal/backup 的具体位置和清理策略；必须位于目标项目 `.ai/` 下的受控运行区，不能污染 Butler 仓或历史迭代归档。
- `[split]` 的“现在迁”仍需模型/用户参与内容路由；本轮程序边界是阻塞并产出可恢复的决策上下文，还是提供独立受控 resume 步骤，需在不承诺错误自动语义拆分的前提下设计。
