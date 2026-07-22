---
方案状态: pass
方案审查日期: 2026-07-22
方案审查方式: dangerous-self-review
---

# Goal

- 以规则真源 + 标准库只读 CLI + registry 投影完成 AC1–AC9。

# Files / Modules to Change

- `prd-split.md`、新 `prd-status.md`、`milestone-schema.md`、Coder README：动作与指针合同。
- `tools/prd-status/`：只读 scanner/status CLI 与 tests。
- `.claude/commands/butler/prd.md`、`plugins/butler/skills/butler-prd/SKILL.md`、`workflows/registry.json` 及生成投影。
- 结构 tests、`scripts/verify-ci.sh`。

# Interface / Contract

- CLI：`python3 tools/prd-status/prd_status.py status --project-root ROOT [--prd-id ID] [--workspace KEY]`。
- JSON stdout；0 成功、1 查询无匹配、2 合同/输入错误；只读命令前后不得产生或修改文件。
- collection 结果以 `prd_id` 排序；详情含 version、status、modules、workspace_scope；workspace filter 匹配四类稳定 key。
- milestone 新指针：`→ prd: <prd_id>#<module_slug>, ...`。

# State / Boundary

- status 只读 `.ai/references/prd/`、需求索引与 `.ai/project/workspaces.md`，不读取或改写对话状态。
- split 写入仅限新的目标需求目录和项目索引；身份闸/soft 对齐未通过时零写。
- R7 update 仍只做命令路由声明，不在本工具实现任何写动作。

# Design Decisions

- 使用独立 status 工具而非扩大 migration CLI：查询是日常稳定接口，迁移只是 legacy 一次性动作。
- 解析合同约束下的 Markdown；不引入通用 Markdown/YAML 引擎，遇未知形态拒绝并给出修复方向。
- project index 是需求发现真源，目录用于交叉核对；不会把“扫到某目录”静默当成已登记需求。

# Plan Admission

- AC Coverage：split AC1–4，status AC5–6，指针/host AC7–8，验证 AC9。
- Assumptions：R1/R2 的 index 与 workspace schema 已成立；legacy 只允许单需求只读回退。
- Alternatives / Trade-offs：散文 status 不可重复验证；复用 migration 工具会耦合一次性事务；通用 parser 依赖过重。选择窄合同 CLI。
- Failure Modes：日期猜测、重复 ID、目录/索引漂移、symlink 逃逸、同名 slug 串线、status 意外写盘、host 投影漂移，均有负向 fixture。
- Impact / Scope Challenge：不实现 update transaction 或 write gate，避免越过 R6。
- Verification Blind Spots：真实 apps dogfood 和实际改动范围对账留 R8。
- Verdict：pass；AC 可验证、边界完整，无已知 Must Fix。

# Execution Steps

- [x] T1 改造 split/指针合同并新增 status 规则 → AC1–AC4, AC7
- [x] T2 实现只读 status CLI 与 fixture → AC5, AC6, AC9
- [x] T3 同步双宿主/registry 投影 → AC8
- [x] T4 完整验证、强审、Goal 与状态收口 → AC1–AC9

# Verification Plan

- `python3 -m unittest discover -s tools/prd-status/tests`
- `python3 -m pytest templates/hooks/tests/test_prd_split_status_contract.py -q`
- `python3 scripts/sync-workflow-registry.py --check`
- `bash scripts/verify-ci.sh`、`git diff --check`、Goal/state audit。

# Risks / Open Questions

- status parser 必须与 references/workspace 两份 schema 的可复制模板严格对齐，测试需覆盖空白与表格列顺序。
