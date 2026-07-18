---
迭代: ITER-0067
方案状态: pass
准入方式: dangerous-ack
---

# Plan Summary

把“坏输入”和“项目外目标”拆成两个显式标记：坏输入继续 fail-closed，项目外目标让所有 Butler 项目规则退出判定；能解析出兄弟项目根的 patch 则切换到该根逐目标执行现有规则。

# Design Decisions

- 在 `lib/io.py` 增加独立的未知目标标记，不复用项目外标记。
- `is_gated` 对未知目标保持保守门禁，对项目外目标返回不适用。
- Codex patch 的绝对、相对目标统一尝试从真实目标位置解析项目根；没有项目根时标为项目外。
- 删除“多项目根直接报错”，保留 dispatcher 的逐 target、first-deny-wins 语义。
- 不新增 Butler 授权文件。宿主权限是机械授权真源；危险模式文档只定义预授权上限、冻结与阻塞路由。

# Alternatives and Trade-offs

- 让 AI 写 `.ai/write-scope`：可机械比较路径，但 AI 能给自己改授权，不能作为可信权限真源，否决。
- 保留 `BUTLER_BYPASS`：实现最省，但把正常跨目录写入伪装成违规，交互重且会污染审计，否决。
- 所有项目外路径直接 allow：会连缺失路径等坏输入一起放掉；本方案用双标记避免该漏洞。

# Failure Paths

- 目标路径缺失、补丁无文件段、项目根解析内部异常：hook fail-closed。
- 外部路径未获宿主权限：由宿主拒绝或请求授权，Butler 不伪造成功。
- 危险模式遇到授权上限外依赖：继续不依赖它的工作；关键链路受阻则记 Goal calibration 并诚实停。
- 多项目 patch 任一根的规则拒绝：整个工具调用拒绝。

# Impact Surface

- `templates/hooks/lib/io.py`
- `templates/hooks/rules/phase_gate.py`
- `templates/hooks/tests/test_io.py`
- `templates/hooks/tests/test_codex_patch.py`
- `templates/hooks/tests/test_phase_gate.py`
- `templates/hooks/tests/test_integration.py`
- `Coder/65_Extension_Dangerous/dangerous-engine.md`
- `Coder/20_Workflow_Lifecycle/mcv-deployment.md`
- `templates/hooks/README.md`
- `templates/rule-card.md`
- `Coder/README.md`

# Verification Plan

- 专项 pytest：路径解析、phase gate、Codex patch、dispatcher integration。
- 结构检查：危险模式和三处对外说明包含授权上限、宿主权限与范围外路由。
- 完整验证：`bash scripts/verify-ci.sh`、`bash scripts/verify-codex-foundation.sh`、`git diff --check`。
- 完整路径证据由 verification evidence runner 生成，最终交给 Goal adjudicator 裁决。

# Execution Steps

- [ ] T1：先补失败测试，覆盖外部 allow、坏输入 deny、相对兄弟项目和多根 patch → AC1–AC5
- [ ] T2：最小修改路径分类与 patch 锚定逻辑 → AC1–AC5
- [ ] T3：更新危险模式与双宿主说明 → AC6–AC7
- [ ] T4：运行专项和完整验证，强审后修复问题并收口 → AC1–AC7

# Plan Admission

- AC 覆盖：7/7。
- 假设：宿主权限系统负责真实文件系统授权；Butler 只做项目流程门禁。
- 反证：未发现必须由 Butler 再维护第二套权限真源的证据。
- Must Fix：0。
- Verdict：pass。
