<!-- butler-artifact-template: 1.0.0 artifact=tech_plan -->
# TECH_PLAN — ITER-0102

方案状态: pass
方案审查日期: 2026-08-01
方案审查方式: user-ack

## Design Decisions

### Goal

- 用现有 Butler seam 落实 AC1–AC6：普通任务保留原快路径，Explore 只在用户主动表达探索意图或接受具体阻塞建议后进入；探索与交付通过显式 promotion 在 Iteration P1 交接。

### Files / Modules to Change

- `Coder/20_Workflow_Lifecycle/lifecycle.md` — **Standard lifecycle interface**；只定义普通任务中的 suggest-only 前置边界、零写等待与 promotion 后从 P1 开始，不承载探索算法。
- `Coder/50_Extension_Ideation/ideation-engine.md` — **Explore behavior module**；拥有激活、探索产物、Decision Map 真源期与显式 promotion 语义，删除自动写 `CONCEPT.md` / 直入 P2 的旧合同。
- `Coder/00_System_Prompt/workflow-router.md` — **Unified-entry routing interface**；区分用户主动探索表达与模型提出的未确认 suggest，继续只选已有 `ideation` workflow，不复制探索算法。
- `workflows/registry.json` — **Workflow metadata SSOT**；保留 13 个业务 workflow 与 `ideation` ID，更新 ideation 的宿主描述，明确显式入口和用户主动语义触发仍指向同一规则真源。
- `.claude/commands/butler/ideation.md`、`plugins/butler/skills/butler-ideation/SKILL.md` — **Host adapters**；只校准入口、项目根、P1 promotion 和非冻结产物说明，继续薄委托 `ideation-engine.md`。
- `docs/workflows.md`、`plugins/butler/skills/butler-ideation/agents/openai.yaml` 及 ideation 适配器 frontmatter — **Generated projections**；只由 `scripts/sync-workflow-registry.py --write` 从 registry 生成，不手工维护生成字段。
- `Coder/00_System_Prompt/logic-protocol.md`、`Coder/20_Workflow_Lifecycle/mcv-deployment.md`、`Coder/README.md` — **Human-facing supporting docs**；移除“显式命令才可启用”和“收敛后直接进 P2”等旧描述，统一为 opt-in Explore → 显式 promotion → P1。
- `scripts/test-workflow-registry.py` — **Contract test surface**；在现有 registry 测试中加入 Explore 边界断言，不新建一套测试工具或 workflow 状态机。

### Interface / Contract

- 输入分两类：用户主动说“脑暴 / 还没想清”等探索意图时，Router 可直接路由既有 `ideation`；普通任务处理中发现阻塞项时，只能输出包含具体阻塞理由的 Explore 建议并等待确认。
- suggest 输出合同至少包含：会改变目标、范围、AC、路线或高成本约束的具体阻塞项，以及“是否进入探索”的确认请求。输出建议本身不得创建持久化 Decision Map、Milestone、Iteration 或四件套。
- Explore 输出合同只保留已确认决定、开放问题和参考依据；它不是 `AC_LIST.md`，也不产生 P2 ACK。
- promotion 是唯一交付交接：用户明确选择推进后解析 `PROJECT_ROOT`，再按现有 lifecycle 开启 Iteration P1 并生成该迭代 `CONCEPT.md`。不得从 Explore 直接进入 P2。
- 真源优先级：探索中由 Decision Map 拥有决策状态；交付中由 Milestone 拥有版本路线、Iteration 四件套拥有当前交付；promotion 后 Decision Map 仅作理由、证据和历史参考。
- `/butler:ideation`、`$butler-ideation`、legacy `/ideation` 都是同一 `ideation` workflow 的 Adapter；不新增 `/explore`、`$butler-explore`、Explore workflow ID 或平行算法。

### State / Boundary

- `lifecycle.md` 与 `ideation-engine.md` 是本次行为合同的两个深模块：前者隐藏 Standard 模式的准入判断，后者隐藏探索过程；Router/registry/宿主入口只暴露小接口。
- 本迭代不定义 Decision Map 文件格式、DAG、Frontier、claim、helper 或 promotion 工具，不连接 Milestone/Iteration admission 机器状态。
- 本迭代不自动判断需求是否清晰、复杂或过大；只有已经可陈述的具体阻塞项才允许触发 suggest。
- 现有 P1→P5、P2/P3 ACK、单 active Iteration、Milestone 台账及 P4/P5 门禁不变。
- 删除测试：如果移除 Router 或任一宿主 Adapter，核心探索/交付合同仍完整存在于 lifecycle + ideation engine；因此不为 Explore 新建只转发调用的额外模块。

### Alternatives / Trade-offs

- 采用“现有 ideation workflow 深化 + Standard suggest seam”，而非新增 Explore workflow：复用现有两类宿主入口和 registry 投影，避免两个名字、两个触发表与两个算法发生漂移。
- 采用 suggest-only，而非模型自动分类后静默进入：牺牲一点自动化，换取零误创建状态和可审计的用户选择。
- 采用 promotion 回 P1，而非把脑暴 AC 直接送 P2：多一步结晶，但保持 `CONCEPT → AC_LIST → TECH_PLAN` 的冻结链和单一真源。

### Execution Steps

- [ ] T1 在 lifecycle 与 ideation engine 固定 suggest、零写、Explore 产物、真源优先级和 P1 promotion 合同 → AC1、AC2、AC4、AC5
- [ ] T2 校准 Router 与 registry 的统一入口及 ideation 元数据，保持 workflow 集合与兼容入口不变 → AC1、AC3
- [ ] T3 运行 registry 写投影，再校准 Claude/Codex 薄适配器正文 → AC3、AC4、AC6
- [ ] T4 同步 logic protocol、MCV 部署说明和 Coder README 的人读语义 → AC1、AC4、AC6
- [ ] T5 扩展现有 workflow-registry 回归测试，覆盖 suggest 边界、P1 promotion、真源优先级和禁止新增 Explore workflow → AC2、AC3、AC4、AC5、AC6
- [ ] T6 执行专项、投影、链接、diff 与完整 CI 验证，并按 AC 回填证据 → AC1–AC6

### Plan Admission

- **AC Coverage**：AC1 由 lifecycle + Router + 人读文档覆盖；AC2 由 lifecycle suggest 合同覆盖；AC3 由 registry + 两宿主 Adapter 覆盖；AC4 由 ideation engine + Adapter promotion 覆盖；AC5 由 ideation engine 的真源优先级覆盖；AC6 由 registry 投影、现有测试面和完整 CI 覆盖。六项均有设计与验证映射。
- **Assumptions**：registry 的语义触发只解释用户原始请求，不能把模型内部判断伪装成用户 opt-in；通过 Router 文本和专项测试固定。`sync-workflow-registry.py --write` 只改投影字段并保留 Adapter 正文；已有幂等/正文保留测试验证。
- **Impact / Scope Challenge**：最小可行改动是修正 4 个现有接口及 3 处旧说明，不建立 Decision Map 实体。后续 R2–R5 可在该合同下独立实现存储、并行探索与交接工具。
- **Verification Blind Spots**：静态测试无法判断自由文本中的阻塞理由是否“足够具体”，也不能证明模型永不误判；本迭代只证明权威规则、入口元数据和适配器没有赋予静默进入或写状态的权限。
- **Verdict**：`pass` — 设计覆盖全部冻结 AC，无已知 Must Fix；用户已完成 P3 ACK，可进入 P4。

## Failure Paths

- **双真源**：新建 Explore workflow/命令或在 Adapter 重写算法会产生漂移；通过 workflow 集合精确断言、规则源路径断言和人工 diff 拒绝。
- **静默写状态**：把“建议”描述成路由结果或自动创建 `.ai/00_IDEATION.md` / Decision Map；通过 lifecycle/engine 合同断言“等待确认、建议零写”，并检查相反表述。
- **错误交接**：残留“收敛后写 CONCEPT 并进入 P2”会绕过 P1/P2 冻结链；专项测试拒绝该旧合同，要求 promotion、项目根解析和 P1 同时出现。
- **快路径回归**：把 Explore 变成所有需求的前置阶段；测试要求普通明确需求继续走极小/简化/完整既有分流，并人工核对 lifecycle diff。
- **投影漂移**：手改生成字段会被同步器覆盖；先改 registry，再运行 `--write`，最后以 `--check` 验证零漂移。
- **文档残留**：README、logic protocol 或 MCV 部署说明仍宣称 explicit-only / 自动 P2；使用定向 `rg` 与 Markdown 链接检查清除矛盾描述。
- **范围膨胀**：实现 Decision Map 存储或分类器会越过 R1；执行 diff 若出现新 workflow、状态文件 schema 或 admission 工具即退回 P3。

### Risks / Open Questions

- 已知风险只有自由文本 blocker 的质量无法被静态测试完全裁决；它已明确保留为人工场景验证，不构成扩大 R1 的理由。
- 当前无待用户选择的设计分叉；P3 ACK 只决定是否按上述边界进入实现。

## Test Strategy

- `python3 scripts/test-workflow-registry.py`：验证 `ideation` ID 和业务 workflow 集合不变、三类入口/规则真源一致、suggest 零写、promotion 进 P1、禁止自动 P2及真源优先级（AC1–AC6）。
- `python3 scripts/sync-workflow-registry.py --check`：验证 registry 生成投影与 Claude/Codex metadata、`docs/workflows.md` 一致（AC3、AC6）。
- `bash scripts/verify-codex-workflows.sh`：验证 Router + 13 workflow skills、薄适配入口与 implicit policy 未回归（AC1、AC3、AC6）。
- `python3 scripts/check-markdown-links.py`（若仓库实际入口不同则使用现有等价命令）：验证本次规则文档链接可解析（AC6）。
- `git diff --check` 与定向 `rg`：拒绝旧的自动 `CONCEPT → P2`、新 Explore ID/入口、模板残留和格式错误（AC2–AC6）。
- `bash scripts/verify-ci.sh`：执行仓库完整回归；专项 workflow 测试若当前未接入该脚本，则本迭代把它接入后再跑（AC6）。
- 人工场景推演：①明确小需求保持快路径；②普通任务发现具体 blocker 只建议且零写；③用户主动说“先脑暴”直达 ideation；④探索多轮后不 promotion 不开迭代；⑤显式 promotion 后从 P1 开始并正确归属 active Milestone（AC1、AC2、AC4、AC5）。

## References Compliance

- N/A：本 AC 无 `prd_refs`，`.ai/references/` 也无本迭代必须继承的外部资料；无需 `Workspace Write Plan`。
