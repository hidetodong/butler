---
方案状态: pass
方案审查日期: 2026-07-22
方案审查方式: dangerous-self-review
---

# Goal

- 以已确认 JSON spec + 整个 PRD root 事务交换完成 AC1–AC9。

# Files / Modules to Change

- `tools/prd-update/`：plan/apply/verify/rollback、receipt、lock、fault injection 与 tests。
- `prd-update.md`、`prd-status.md`/status CLI：执行合同与最近 receipt 只读视图。
- Claude/Codex PRD 入口、结构 tests、`scripts/verify-ci.sh`、Coder README。

# Interface / Contract

- CLI：`prd_update.py plan|apply --project-root ROOT --spec SPEC`；`verify|rollback --project-root ROOT --prd-id ID [--update-id ID]`。
- plan/verify 零写；JSON stdout；0 成功，1=plan 未 ready/无更新，2=输入/事务错误。
- spec 只接受 schema v1 精确字段；active module source 为真实 UTF-8 普通文件，source bytes hash 进入 plan/receipt。
- receipt 位于 `<prd_id>/.butler-updates/<update_id>.json`；backup 位于 `.ai/references/.prd-update-backups/<update_id>`。

# State / Boundary

- 唯一写面是 `.ai/references/prd/` 整体交换、同父 backup 和短命 lock/stage；origin 与工作产物只读扫描。
- apply 前锁内重算全部 hash；stage 验证通过才 rename，live 验证失败立即恢复 backup。
- rollback 要求当前 collection 等于 receipt post hash且 backup 等于 pre hash；否则拒绝。

# Design Decisions

- 复用 `tools/prd-status/prd_status.py` 的索引/范围解析，避免 update 另造 collection 语义。
- 整 root 交换比逐文件替换多占临时空间，但能把总索引、target archive/live 和 receipt 放在同一个原子切换边界。
- receipt 文件排除自身后计算 post hash，避免循环；receipt schema 与路径逐字段校验。
- 每个 impact path 都需合法 disposition，future 也显式记录，避免对话默认值丢失。

# Plan Admission

- AC Coverage：spec/plan AC1–2，transaction/receipt AC3–5，idempotence/verify/rollback/fault AC6–8，wiring/CI AC9。
- Assumptions：R6 collection/status 合同成立；语义层能在 apply 前产出已确认最终模块原文。
- Alternatives / Trade-offs：逐文件 journal 更省空间但切换窗口复杂；把模型启发式塞 CLI 不确定；Git commit 依赖外部状态。选择标准库整树事务。
- Failure Modes：source/现场 TOCTOU、同版本、archive 已存在、lock 冲突、stage 中断、两次 rename 任一点失败、receipt 路径篡改、后续更新后误 rollback，全部有负向 fixture。
- Impact / Scope Challenge：只记录处置，不碰 active/closed 文件；不提前做 R8。
- Verification Blind Spots：超大 PRD 的磁盘开销与真实 apps 文件形态留 R8 dogfood。
- Verdict：pass；事务边界、恢复条件和语义/机械分工完整，无已知 Must Fix。

# Execution Steps

- [x] T1 完整改版规则与 spec/receipt 合同 → AC1, AC2, AC4, AC5
- [x] T2 实现 plan/apply/verify/rollback 与 status receipt 视图 → AC2–AC7
- [x] T3 建多 PRD/影响/幂等/故障/篡改 fixture → AC1–AC8
- [x] T4 同步双宿主/README/CI，完整强审与收口 → AC9

# Verification Plan

- `python3 -m unittest discover -s tools/prd-update/tests`
- `python3 -m pytest templates/hooks/tests/test_prd_update_transaction_contract.py -q`
- `bash scripts/verify-ci.sh`、`git diff --check`、Goal/state audit。

# Risks / Open Questions

- R6 status 的严格 parser 是共享依赖；更新工具必须把 staged index 再喂回它验证，不能只相信自己写出的 Markdown。
