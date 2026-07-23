# TECH_PLAN — ITER-0087

方案状态: pass

# Design Decisions
- 扩展 contract.py 为 CLI；render 永远零写，init 缺失才写，reset 要 force。
- phase 顺序 P1/P2/P3/P5/close；调用方传 current phase，禁止生成更后阶段。

# Failure Paths
- 目标存在、越阶段、模板坏、原子替换失败均拒绝。

# Test Strategy
- temp project 覆盖 render/init/idempotence/dry-run/reset/phase/rollback。

# References Compliance
- N/A
