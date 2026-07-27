> 分流: 完整 | 命中升级信号: 多文件改动、契约变更、跨模块影响、设计取舍 | 2026-07-25
> ⚠️ 危险模式：本产物由模型自主确认问题理解，未经用户逐项确认（ITER-0091，2026-07-25）
<!-- butler-artifact-template: 1.0.0 artifact=concept -->
# CONCEPT — ITER-0091 · 轻量 TDD 配对合同与检查器

## Current Understanding

- Butler 已能保存真实测试命令的失败和通过 record，但不会判断两条 record 是否构成同一 TDD cycle 的 Red→Green 配对。
- R1 只建立最小机器合同：任务在 TECH_PLAN 明确声明 cycle 后，检查器验证同一 argv/cwd 先失败、后通过。
- 这份证据只证明 Butler 亲自记录到配对事实，不声称证明生产代码一定在 Red 后才修改，也不判断失败原因是否有效。

## Scope

- 在 `TECH_PLAN.md` 的 `Test Strategy` 段声明稳定 cycle 名、对应 AC、测试 argv JSON 与项目相对 cwd。
- 复用 verification evidence v1 record；以 `tdd-<cycle>-red` / `tdd-<cycle>-green` 约定配对，不增加 sidecar 或第二日志格式。
- 在 evidence 工具中增加只读检查命令和正负向测试；生命周期、Goal 完成门和真实 dogfood 留给 R2。

## Open Questions / Risks

- Markdown 表格只承担声明，不复制 record 事实；解析必须 fail-closed，避免模糊命令文本被错误配对。
- baseline、文件哈希、测试弱化检测、有效 Red 分类、adapter 和最终 diff 对账均明确不属于 R1。
