# TECH_PLAN — ITER-0086

方案状态: pass
方案审查: dangerous-self-review

# Design Decisions

- `tools/artifact-pipeline/artifacts.v1.json` 为结构 SSOT，templates 仅承载可填槽文本。
- manifest 明确 artifact、phase、path、template、required_sections、frontmatter、fixed_tables 与 conditional_sections。
- 合同库只读解析 Markdown，先服务测试，R2 再复用为 CLI 生成/检查内核。
- legacy archive 不纳入 strict 检查；严格性由 live 工作区的模板版本标记启用。

# Failure Paths

- manifest/模板不一致、重复 H1、章节换序或表头漂移：fail-closed。
- 未知模板版本：拒绝，不猜兼容结构。

# Test Strategy

- 正向五模板全量通过；逐类 mutation 负向失败；完整 CI 回归。

# References Compliance

- N/A
