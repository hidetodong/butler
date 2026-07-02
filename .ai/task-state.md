# Task State

> 活跃迭代 ITER-0024（MILE-0002 R4，等待-回收-续跑接线）· 危险模式自治 · P1-P3 自审门已过、待 P4 执行。

## 当前状态

- 活跃迭代 **ITER-0024**（current=ITER-0024，2026-07-02），归属 **MILE-0002 R4**。
- 危险模式：本会话自治（承 ITER-0021/0022/0023 precedent）；P2/P3 已过自审门 self-ACK；回滚锚点=本轮 iteration-open 提交。butler 仓无 `.ai/local-constraints.md` 落点，本次自治收口后交还即回标准模式。
- P1-P3 四件套已 overwrite 覆写为 ITER-0024；AC_LIST 9 条 AC 已 ack-frozen（自审门）；TECH_PLAN 8 DD / 8 步已自审 ACK。

## 下一步入口

- P4 执行 T1-T7：新增 `human-test-bridge.md` 闭环协议 + 接线 verify-schema/testing-strategy/correction-contract/dangerous-engine + 注册 Coder/README + 改工具 README + 收录 rule-card + 机械跑通桥回路 + 一致性对账。
- P5：独立复核（fresh-context 子 agent，逐 AC）+ 原子收口五步（归档 + 交付 md/html + 翻台账 R4 closed + PROJECT 前滚 + 收口自检 5 不变量）。
- MILE-0002 R4 收口后剩 **R5**（部署 / 使用文档注册 + 真实 dogfood + 长程无人准入闸落地），待用户指令。
