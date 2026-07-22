---
方案状态: pass
方案审查日期: 2026-07-22
方案审查方式: dangerous-self-review
---

# Goal

- 以最小变更把 AC1–AC7 落到既有 references 契约真源，并用结构测试防止后续动作层重新漂回单 PRD 模型。

# Files / Modules to Change

- `Coder/40_Context_Management/references-schema.md`：重写 PRD 结构、两层索引、身份与独立版本契约；保留扁平 references 与无损红线。
- `Coder/README.md`：更新 references 子系统的目录摘要和职责说明。
- `templates/hooks/tests/test_prd_collection_contract.py`：新增纯标准库结构合同测试。
- `.ai/*`：本迭代状态、证据、归档和交付。

# Interface / Contract

- 项目级入口：`.ai/references/prd/00_INDEX.md`。
- 单需求入口：`.ai/references/prd/<prd_id>/00_INDEX.md`。
- `prd_id`：`YYYY-MM-DD-<requirement-slug>`，日期为首次进入当前项目 Butler 体系的本地日期；分配后不可因改版、改标题或源地址变化而改变。
- 模块身份仍为单需求内的 `module_slug`；完整逻辑锚点由 `prd_id + prd_version + module_slug` 构成，但本轮不修改消费者字段。
- 每个 `<prd_id>` 目录独立维护 live 模块与 `.archive/vN/`。

# State / Boundary

- R1 只定义结果形态和身份判定，不实现产生/更新动作。
- legacy 根结构继续可读且不自动搬迁；R5/R8 承接兼容迁移和验证。
- 非 PRD 扁平 references 语义保持不变。

# Design Decisions

- 原位升级 `references-schema.md`，不新增 `prd-collection-schema.md`，避免两份结构真源。
- 采用日期 + 语义 slug 的人读稳定身份；拒绝内容 hash 作为主身份，因为改版会改变 hash，也无法让人从路径理解需求。
- 项目级索引只登记需求，不复制模块表；模块表只存在各需求目录，避免两层重复信息漂移。
- 判定先查显式 `prd_id` / 已登记来源关系，再看同一需求证据；信号冲突或无法唯一命中就停，不自动新建或合并。
- 本轮新增结构测试而非实现解析器：R1 是 Markdown 契约，最小足够的机械保护是检查关键不变量存在；行为 fixture 留给动作实现迭代。

# Plan Admission

- AC Coverage：AC1–AC6 由 references 契约章节直接覆盖，AC7 由 README + unittest + 完整 CI 覆盖。
- Assumptions：仓库现有 PRD 能力仍是单需求模型；已由当前 schema/split/update 三份真源核实。日期按项目本地日期记录，跨时区输入的首次落盘动作需在 R6 明确，但不影响身份格式。
- Alternatives / Trade-offs：新增平行 schema 能少改旧文，但会制造两个真源；内容 hash 稳定去重但不稳定代表持续改版的需求。选择原位升级 + 人读 `prd_id`，代价是后续动作层和迁移必须逐步适配。
- Failure Modes：同一需求被重复建目录、不同需求被错误合并、日期被版本发布日期替代、模块 slug 被当成 prd_id、两份 PRD 共用 `.archive/vN/`。契约逐项禁止，歧义 fail-closed。
- Impact / Scope Challenge：不提前修改 split/update/AC/hook；这些变化虽最终必需，但越过 R1 会让契约和动作同时变化、无法独立审计。
- Verification Blind Spots：结构测试只能证明契约文本存在，不能证明迁移和命令行为；这部分必须在 R5–R8 用 fixture 与真实项目验证，R1 不宣称覆盖。
- Verdict：pass。边界单一、AC 全覆盖、无已知 Must Fix，可以进入 P4。

# Execution Steps

- [x] T1 盘点现行单 PRD schema、split、update 和消费者边界 → AC1–AC6
- [x] T2 设计两层索引、稳定身份和新需求/新版判定 → AC1–AC6
- [x] T3 完成危险模式 P2/P3 自审并冻结 → AC1–AC7
- [ ] T4 原位升级 references 契约和 README 导航 → AC1–AC6
- [ ] T5 新增结构合同测试并运行专项/完整验证 → AC7
- [ ] T6 执行 P5 强审、Goal 裁决、归档与交付 → AC1–AC7

# Verification Plan

- 运行 `python3 -m unittest templates.hooks.tests.test_prd_collection_contract -v`。
- 运行 `bash scripts/verify-ci.sh`、`git diff --check`、`python3 scripts/audit-project-state.py --project-root <root> --allow-unreleased`。
- 对照 AC1–AC7 做同上下文完整强审，保留失败证据，不把未执行的 R5–R8 行为写成已验证。

# Risks / Open Questions

- 现有非回归门把 `acceptance-schema` 等列为不得触碰；本轮遵守，后续 R5 若明确修改引用契约，必须在其 AC 中说明为何属于有意范围变化。
- `prd_id` slug 的具体字符校验和冲突后缀策略在动作层实现前仍只是契约；R6 必须补可执行验证。
