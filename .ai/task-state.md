# Task State

> **ITER-0039 P2 · 等待 ACK**（`ITERATIONS.current: ITER-0039`）。里程碑 **MILE-0004** active，R1–R3 已收口，本轮做 R4（AC 钉版 + P2/P3/P5 接线）。

## 当前状态

- `ITERATIONS.current: ITER-0039`（MILE-0004 R4 · AC 钉版 + P2/P3/P5 接线）。已开迭代、写完 P1 CONCEPT + P2 AC_LIST（`状态: draft`），**待用户 ACK 冻结后进 P3/P4**。
- `MILESTONES.current: MILE-0004`（路线图 R1–R6 见 `.ai/MILESTONE.md §5.3`）。已落：R1 契约（`references-schema`）+ R2 切分（`prd-split`）+ R3 `/milestone` 并进入口 + 两海拔交叉指针。"一份输入喂两个海拔"闭环成型、但指针指 live 最新、**未版本化**——R4 补钉版。
- 全貌产物（`frontier.md` / `capabilities.md`）保持 R3 收口态，待 R4 收口再前滚。

## 下一步入口

- **等待 ACK**：用户确认 AC_LIST 后，把 `状态` 改 `ack-frozen`、填 `ACK 日期`，写 P3 TECH_PLAN，进 P4 执行（扩展 acceptance/tech-plan/verify 三 schema + flip references-schema §7/§8）。**未 ACK 不得写 P4 源改动。**
- R4 改动集（4 文件、全接线/翻牌、无新文件）：`acceptance-schema`（加 `prd_version` 字段 + 绑定语义 + 编写规则）/ `tech-plan-schema`（External References 继承钉住版）/ `verify-schema`（References Compliance 对钉住版核）/ `references-schema`（§7/§8 flip R4 指针）。
- 冷启动读序（butler 文件夹态）：`.ai/project/00_INDEX.md` → `.ai/MILESTONES.md` / `.ai/MILESTONE.md` / `.ai/ITERATIONS.md` → 本文件 → 代码。
