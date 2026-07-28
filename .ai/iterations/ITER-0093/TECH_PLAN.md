<!-- butler-artifact-template: 1.0.0 artifact=tech_plan -->
# TECH_PLAN — ITER-0093

方案状态: pass
方案审查日期: 2026-07-28
方案审查方式: dangerous-self-review

> ⚠️ 危险模式：本方案由模型完成 Plan Admission 后自主 ACK，未经用户确认（ITER-0093，2026-07-28）

## Design Decisions

- 在 `tools/project-config/` 建立单一配置内核：`config.py` 同时提供可导入函数与薄 CLI，`butler-config.schema.json` 是公开数据合同，测试直接对账两者。
- 配置路径恒为显式项目根下 `.ai/butler.config.json`。读取时解析项目根、拒绝 symlink 和非普通文件；写入用同目录临时文件、`fsync`、`os.replace`，不跨文件系统。
- 缺失配置由 `inspect` 返回规范默认值但不落盘；已存在配置必须完整满足 schema，任何错误均 fail-closed。这样兼顾新项目探测与损坏配置安全。
- CLI 使用 `inspect`、`init`、`set` 三个动作；stdout 始终是单 JSON，诊断也以 JSON 返回，方便后续规则、命令和迁移器复用。
- R1 不实现 legacy Markdown 解析，避免把迁移策略和基础 JSON 合同绑死；R2 在该内核之上增加兼容层。

## Failure Paths

- 项目根不存在、不是目录或 `.ai` 不可达：退出 2，零写。
- 配置是 symlink、目录、坏 UTF-8/JSON、字段不全或类型不符：退出 2，零写且不套默认值。
- `init` 遇已有配置：退出 1，拒绝覆盖；`set` 遇缺失或非法配置：退出 2，不创建半成品。
- 原子写中途失败：清理临时文件，原配置字节保持不变。

## Test Strategy

- 先写 schema/CLI 合同测试，确认工具缺失时失败；再实现最小标准库内核并逐项跑绿。
- 用 subprocess 验证退出码、stdout 单 JSON和零写，用模块级测试验证 schema 与运行时校验一致。
- 完成后运行项目配置专项、五件套合同、状态/交接检查和完整 CI。

## References Compliance

- `.ai/local-constraints.md` 当前约束只限制施工根；新工具所有测试写入临时目录，实际源码只落本仓授权范围。
