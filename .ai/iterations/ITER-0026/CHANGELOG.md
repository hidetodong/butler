> R1 帮手名册骨架 + 复核三拆 + 通用规矩单源化 · closed · 2026-07-05

本文件是 ITER-0026 收口时归档的对象级变更流切片（ADD/EDIT/DELETE）。

## ADD
- `Coder/62_Extension_Agents/overview.md` — 新建帮手名册总述：帮手是什么 + 名册表（复核✅本轮立 / 更新说明🔜R4 / 查过时🔜R4）+ 通用规矩 G1–G4 唯一真源 + 触发式加载 + 生态校准（AGENTS.md 源 Sourcegraph Amp、Agent Skills 生态口径） → AC1 AC4
- `Coder/62_Extension_Agents/independent-review.md` — 新建复核帮手完整定义：中立定义表（角色 / 输入 spec-only / 输出 confirm·refute·无法验证 / 禁止 / 隔离 / 只读权限）+ 触发 / 断言核对 / 输出衔接 / 诚实兜底；共享审查流程回指 60 → AC2

## EDIT
- `Coder/60_Extension_CodeReview/review-engine.md §1–§7` — 复核三拆重写：身份回指 overview（G1）、独立复核定义迁出 independent-review 只留接口指针、§6 G2 诚实兜底回指总述 §3；保留 §1–§7 编号骨架不 renumber（防跨文件 §引用断裂） → AC3 AC8
- `Coder/65_Extension_Dangerous/dangerous-engine.md §7.3` — G2 引用从「review §6.4」改指 `62_Extension_Agents/overview.md §3 通用规矩 G2`，独立复核指针指 independent-review → AC4
- `Coder/20_Workflow_Lifecycle/verify-schema.md §4` — G2 引用从「review-engine §6.4」改指 `62_Extension_Agents/overview.md §3 通用规矩 G2` → AC4
- `Coder/00_System_Prompt/logic-protocol.md §90` — Review Mode 追加复核帮手完整定义指针（independent-review）+ 帮手通用规矩指针（overview §3 含独立性=上下文隔离） → AC4 AC5
- `Coder/README.md` — 目录树 + 目录说明 + 详细说明三处注册 `62_Extension_Agents/`（overview + independent-review，触发式加载、不进冷启动必读） → AC5

## DELETE
- 无
