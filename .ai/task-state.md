# Task State

> **ITER-0040 P2 · 等待 ACK**（`ITERATIONS.current: ITER-0040`）。里程碑 **MILE-0004** active，R1–R4 已收口，本轮做 R5（改版同步 `/prd update`）——MILE-0004 收官核心。

## 当前状态

- `ITERATIONS.current: ITER-0040`（MILE-0004 R5 · 改版同步 `/prd update`）。已开迭代、写完 P1 CONCEPT + P2 AC_LIST（`状态: draft`，10 条 AC），**待用户 ACK 冻结后进 P3/P4**。
- `MILESTONES.current: MILE-0004`（路线图 R1–R6 见 `.ai/MILESTONE.md §5.3`）。已落：R1 契约 + R2 切分 + R3 /milestone 入口 + R4 钉版。R5 补动态那一半（PRD 改版怎么办），是"改版有确定性协议兜底"的收官核心；R6 认亲边缘 + 非回归 + 收尾待。
- 全貌产物（`frontier.md` / `architecture.md`）保持 R4 收口态，待 R5 收口再前滚。

## 下一步入口

- **等待 ACK**：用户确认 AC_LIST 后，把 `状态` 改 `ack-frozen`、填 `ACK 日期`，写 P3 TECH_PLAN，进 P4 执行。**未 ACK 不得写 P4 源改动。**
- R5 改动集（新增 1 + 接线 4 + flip）：新建 `Coder/40_Context_Management/prd-update.md`（动作层：变更检测清单优先+diff兜底 / 重新派生+冻旧版快照 / 登记表认亲基础态 / 三态影响面亮牌不自动 / 受影响路由回指 amend·扩张 / `/prd status`）+ 接线 `logic-protocol` 注入表 / `acceptance-schema §4` / `README` + flip `references-schema §7·§8` R5 指针。
- 设计已由 2026-07-08 grilling 十节点决议钉死（检测 c / 三态 a / live+快照 a / 全局版本 b），R5 是决议物化。
- 冷启动读序（butler 文件夹态）：`.ai/project/00_INDEX.md` → `.ai/MILESTONES.md` / `.ai/MILESTONE.md` / `.ai/ITERATIONS.md` → 本文件 → 代码。
