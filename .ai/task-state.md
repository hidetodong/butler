# Task State

> MILE-0003 · R1 / ITER-0026 · 阶段 P3（P2 自审门已过、AC 冻结；正写 TECH_PLAN）· ⚠️ 危险模式 ON（会话级）。

## 当前状态

- 里程碑：**MILE-0003** active；迭代：**ITER-0026** active（R1 帮手名册骨架 + 复核三拆 + 通用规矩单源化）。
- ⚠️ **危险模式 ON**（会话级，butler 仓无 local-constraints 落点）；北极星=ITER-0026 R1 单迭代，收口后交还；R2–R8 待指令。
- 阶段进度：P1 CONCEPT ✓（标准模式）→ **P2 AC_LIST ✓ 自审门过、ack-frozen（8 AC）** → P3 TECH_PLAN 进行中 → P4 → P5 强审 → 收口。
- 护栏：审计落 `.ai/RUN_LOG.md`（ITER-0026 段）；回滚锚点将于 P3 后 iteration-open commit 建立；P5 升格独立复核。

## 关键约束（防跑偏）

- 落点 `Coder/62_Extension_Agents/`，夹内零数字前缀；总述触发式加载、不进冷启动必读；名册表先列全三帮手（后两个标 R4）。
- 三拆带地址搬家（哪段搬哪、原地留指针）；G2 诚实兜底正文现只在 `review-engine §6.4`（dangerous §7.3 / verify-schema §4 是引用），上提总述后改这两处引用 + 全仓 grep 无漏网。
- 权限靠约定 + 如实说，本迭代不做工具层硬拦。
- 顺手改准两处事实错（AGENTS.md 起源 Sourcegraph Amp / Agent Skills 采用数加时间点）。

## 下一步入口

- 写 P3 `TECH_PLAN.md`（逐项映射 AC1–8 + Execution Steps）→ 过 §5.2 设计自审门 → 自主 ACK → commit iteration-open 回滚锚点（P1–P3 + 台账 + RUN_LOG）→ 进 P4。
