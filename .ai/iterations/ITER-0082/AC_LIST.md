---
状态: ack-frozen
ACK 日期: 2026-07-22
---

> ⚠️ 危险模式：模型已过验收自审门并自主冻结（ITER-0082，2026-07-22）。

# Goal

- 让声明式 Workspace Scope 真正约束计划、真实改动和双宿主写入，并用完整版本链路证明 MILE-0009 达成。

# In Scope

- 自动发现/地图校验、共享与生成路径归属、TECH_PLAN 写计划、显式路径/Git diff 对账、PreToolUse 范围门禁。
- 多 PRD/跨包/legacy/事务/无损/双宿主 e2e；apps 原仓只读取证、临时副本 dogfood。

# Out of Scope

- 不写 apps 原仓；不自动扩张 PRD 范围或修改冻结 AC；不拦 shell；不切版/提交/推送。

# Acceptance Checklist

- [x] AC1：`discover` 从 npm `workspaces`（数组或 `packages` 对象）和 pnpm workspace 声明有限展开 manifest，输出稳定候选地图；忽略依赖目录，拒绝绝对/逃逸 pattern、symlink、重复身份、无名包和重叠工作区，全程零写。
- [x] AC2：`validate` 严格解析 `.ai/project/workspaces.md` 的 active/retired 地图及显式 Path Ownership；键、规范路径、manifest identity、kind/status、证据、共享/生成路径唯一归属不一致即 fail-closed。
- [x] AC3：需求范围从 AC 的集合钉版 `prd_refs` 解析 live 或该需求 archive；多需求显式权限冲突、未知/retired 键、模块范围扩张、legacy 无身份均拒绝，不从最新 live 偷换冻结版本。
- [x] AC4：TECH_PLAN 必须用机器可读 Workspace Write Plan 列出拟写 workspace 与路径；`check-plan` 证明计划路径归属唯一、落在该键内且权限为 primary/supporting，read-only/excluded/未声明或缺计划拒绝。
- [x] AC5：`check-diff` 对 Git tracked 变更、rename/delete 和可选 untracked 文件逐路径对账；共享/生成文件按显式 ownership 归属，目录移动/未知路径/越界均给稳定 JSON 与非零退出，不改工作树。
- [x] AC6：共享 PreToolUse `workspace_scope` rule 在存在 `prd_refs` 时复用同一 parser，逐 Edit/Write/MultiEdit/apply_patch target 拦越界；无 PRD 引用受控 N/A，坏范围 fail-closed，外部真实路径仍交宿主授权。
- [x] AC7：范围扩张必须先改 PRD Scope、退回 AC/Plan 重审；工具和 hook 只报告/拒绝，不自动修改 PRD、AC、TECH_PLAN、工作区地图或 origin，规则真源和双宿主薄适配一致。
- [x] AC8：隔离 e2e 覆盖 inbox 幂等/来源变化、两份独立 PRD 同名模块、不同版本钉版、update receipt、跨包范围、legacy migration/历史 resolver 与逐字 bytes 不变，完整链路可重复且失败可恢复。
- [x] AC9：真实 `WorkCode.nosync/apps` 原仓在 dogfood 前后整树状态不变；由真实 manifests 发现工作区，并在临时副本完成 legacy inspect/plan/apply/verify/rollback，核对 active/queued MILESTONE 与冻结/closed AC 引用报告，不静默规范化其非标准状态。
- [x] AC10：规则、Coder 入口、hook 部署/升级与 Codex wrapper、CLI README/tests/CI 全接线；完整 CI、diff check、Goal adjudicator、state audit 和 MILE-0009 路线/交付归档全部通过。

# Verification Method

- AC1–AC7：标准库 subprocess fixture + hook 单元/集成，用树 hash 证明零写与恢复，逐项断言 JSON、退出码和 denial。
- AC8：单一临时工程串联 R3–R8 驻留工具，核对内容 hash、receipt 与历史 resolver。
- AC9：只读采集 apps manifest/台账/PRD hash；复制必要项目事实到临时目录后执行迁移全回路，再复核原仓 Git/status/hash。
- AC10：规则结构 tests、Claude/Codex 真 wrapper、`bash scripts/verify-ci.sh`、evidence、Goal/state audit。

# External References

- N/A；本迭代没有外部权威 PRD。`WorkCode.nosync/apps` 是只读兼容样本，不注入 Butler 仓 references，也不作为需求真源。

# Open Questions / Risks

- shell 写入不经过当前 hook，因此交付口径必须明确：宿主 Edit/Write/apply_patch 前置拦截 + P5 Git diff 全量对账，两层共同覆盖，不能宣称单个 hook 全覆盖。
- apps 的 queued 里程碑是旧项目自定义状态；dogfood 只要求迁移/解析诚实报告与历史 bytes 不丢，不要求本迭代改写其项目治理状态。
- 当前工作树无干净 R8 前 Git 锚点；以窄文件面、专项树 hash、无破坏性命令和归档证据降低回退风险，并如实披露。
