# Task State

> ITER-0025（MILE-0002 R5）· 阶段 P3（TECH_PLAN 待用户 ACK）。任务清单镜像自 TECH_PLAN Execution Steps。

## 当前状态

- ITER-0025，P2 已 ACK 冻结（2026-07-02），P3 TECH_PLAN 完成、待用户 ACK 进 P4。
- 主题：MILE-0002 收尾 R5——部署侧调用文档 + 人类侧使用说明 + 真样例 dogfood。
- Q1/Q2/Q3 已在 P3 落定：样例落 `tools/delivery-selftest/sample/`；`tools/` 抽象为通用驻留工具类别；收口不切版、发布节奏用户拍板。

## 任务清单（镜像 TECH_PLAN，P4 执行时更新活进度）

- [ ] T1（AC5/6/7）：写 sample manifest（四态齐全 fixture）
- [ ] T2（AC5/6）：真 dogfood 跑通外部调用回路 + 留证据
- [ ] T3（AC1/2）：mcv-deployment 新增 §6 驻留工具调用节
- [ ] T4（AC3/4）：HUMAN_GUIDE §5 新增人测桥使用说明
- [ ] T5（AC7）：README 补外部调用样例指引
- [ ] T6（AC8）：Coder/README 描述确认
- [ ] T7（AC9）：原子收口五步 + MILESTONE 收尾

## 下一步入口

- 等用户 ACK P3 → 进 P4 按 T1→T7 执行（dogfood 先行，文档随后）。
