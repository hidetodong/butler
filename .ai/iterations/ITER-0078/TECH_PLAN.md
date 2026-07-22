---
方案状态: pass
方案审查日期: 2026-07-22
方案审查方式: dangerous-self-review
---

# Goal

- 用确定性 CLI 管事实、薄工作流管语义路由，完成 AC1–AC9。

# Files / Modules to Change

- `tools/inbox/inbox.py` + `tools/inbox/README.md` + tests：扫描与 canonical ledger。
- `inbox-schema.md` / 新 `inbox-workflow.md`：管理块和动作真源。
- `.claude/commands/butler/inbox.md`、`plugins/butler/skills/butler-inbox/SKILL.md`。
- `workflows/registry.json`、同步器/测试、plugin/docs 生成投影。
- HUMAN_GUIDE/README/capabilities 计数与入口。

# Interface / Contract

- CLI：`status|scan`；scan 默认 plan，`--apply` 原子写；`--project-root` 必填。
- JSON：schema_version/action/changed/counts/sources/rejected。
- INBOX managed markers 包住两张 canonical 表；外部内容逐字保留。
- 工作流：scan → analyze → confirm/self-review → delegate route → update receipt。

# State / Boundary

- scanner 不分类、不写 actual route/derivation 成功事实。
- workflow 调现有规则，不复制算法。
- 活工作区冲突按项等待，不阻塞安全的 sibling 项。

# Design Decisions

- Markdown 管理块 + 原子替换：兼顾人读 SSOT 与确定性写入，不引入 JSON 第二真源。
- plan 默认、apply 显式，避免扫描即写；workflow 可在呈交前 apply 机械事实，但不能提前路由。
- 不跟随 symlink，最小化 origin 信任边界。
- registry 仍是入口元数据 SSOT，更新 EXPECTED_IDS/数量合同，不手工维护软链。

# Plan Admission

- AC Coverage：CLI AC1–4/9，workflow AC5–7，registry AC8，完整矩阵 AC9。
- Assumptions：Markdown 管理块由工具独占；首次文件无 marker 时只在用户内容后追加，残缺/重复 marker fail-closed。
- Alternatives / Trade-offs：纯模型写 ledger 简单但不可重复；JSON sidecar好解析但制造第二真源。选择 Markdown managed block，代价是需严格 parser。
- Failure Modes：部分写、marker 冲突、hash 错字节、symlink 逃逸、route 前确认缺失、批量覆盖活工作区、registry 计数漂移。均有断言/流程门。
- Impact / Scope Challenge：不实现语义分类器；模型判断才是合适层，CLI 只做可证明事实。
- Verification Blind Spots：真实宿主菜单发现靠结构/registry；R8 再做最终端到端。
- Verdict：pass，无已知 Must Fix。

# Execution Steps

- [x] T1 盘点 registry/入口/工具模式 → AC8
- [x] T2 设计 CLI、managed block 与路由协议 → AC1–AC7
- [x] T3 危险模式 P2/P3 自审 → AC1–AC9
- [ ] T4 实现 CLI 与 fixture → AC1–AC4, AC9
- [ ] T5 实现 workflow/registry/投影 → AC5–AC9
- [ ] T6 完整验证、强审、Goal 裁决与收口 → AC1–AC9

# Verification Plan

- `python3 -m unittest tools.inbox.tests.test_inbox -v`
- `python3 scripts/test-workflow-registry.py`、`python3 scripts/sync-workflow-registry.py --check`
- `bash scripts/verify-ci.sh`、diff/Goal/state audit。

# Risks / Open Questions

- R4 会扩大 workflow 集合合同；所有硬编码 10 的人读/测试投影必须一起收敛，不能只改 registry。
