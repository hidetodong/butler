---
状态: ack-frozen
ACK 日期: 2026-07-29
---
<!-- butler-artifact-template: 1.0.0 artifact=acceptance -->
# AC_LIST — ITER-0096

> ⚠️ 危险模式：本验收清单由模型完成反证、自洽性与可验证性审查后自主 ACK，未经用户逐项确认（ITER-0096，2026-07-29）

修订记录: 2026-07-29 · P5 安全审查明确回执不是写入授权或 Butler 绕过，并把并发同名写入收紧为 create-only 后重选短序号；不改变协议级 MVP 范围。

## Goal

- 建立一套轻量、可复用的旁路工作回执协议，让用户主动发起、脱离主上下文完成的代码与调研成果能由用户用一个文件路径稳定钩回主 Agent。

## In Scope

- 回执规则真源、canonical 模板、首次落盘与命名规则、生产/消费流程、代码与调研混装、共享工作区可信度披露、入口文档和机械结构验证。

## Out of Scope

- 不新增接受/拒绝或未读/已读状态，不设索引和自动扫描，不自动合并代码，不自动改写主线产物，不新增命令、skill、Agent 调度器或跨项目汇总。

## Acceptance Checklist

- [ ] AC1: `Coder/40_Context_Management/sidework-receipt.md` 成为单一规则真源，明确旁路工作由用户主动发起、回执用于发现/理解/续接而非模型审批，并与 session handoff、references、task-state 和交付总结划清职责。
- [ ] AC2: canonical 模板能在同一回执中表达代码、调研、方案、实验和验证成果；固定包含用户目标、成果结论、成果与改动位置、验证事实、主线影响和续接入口，正文只写结论与稳定指针，不复制长报告、代码或日志。
- [ ] AC3: 生产/消费流程明确要求旁路执行者新建一份回执、返回路径且不修改主线四件套、task-state、台账或 session handoff；主 Agent 仅在用户给出路径后定向读取、对账和亮出冲突，方向取舍仍交给用户。
- [ ] AC4: `.ai/sidework/<YYYY-MM-DD>-<slug>.md` 按需创建、一个任务一文件；同名时用 create-only 追加递增短序号且绝不覆盖，路径必须留在项目根内。回执不是写入授权或流程绕过；代码成果记录基线和实际改动，共享工作区必须披露低归属强度，不能冒称独立提交。
- [ ] AC5: `Coder/README.md` 注册新规则文件、触发式读取语义和职责说明；`HUMAN_GUIDE.md` 给出用户可直接照做的发起与回钩示例，并在部署目录说明 `.ai/sidework/` 为按需目录。
- [ ] AC6: 专项结构检查能发现模板章节/表头漂移、规则入口缺失和危险反模式，纳入 `scripts/verify-ci.sh`；专项、Markdown 链接、完整 CI、状态审计与 `git diff --check` 通过，危险模式完整审查无 Must Fix。

## Verification Method

- AC1: 静态读取规则真源并断言定位、边界与禁止审批语义；核对与既有 handoff/references 指针不冲突。
- AC2: 专项脚本验证模板 H1/H2 顺序、成果表表头、必填占位和“指针不复制”约束。
- AC3: 专项脚本断言生产者禁止写入清单、显式路径消费和用户决策边界均存在。
- AC4: 专项脚本断言目录、命名、并发同名不覆盖、项目根边界、回执非授权、基线与共享工作区披露规则。
- AC5: 专项脚本核对 `Coder/README.md` 文件登记与说明、`HUMAN_GUIDE.md` 目录/示例接线；运行 Markdown links。
- AC6: 用 verification evidence runner 捕获专项、完整 CI、状态审计和 diff check；P5 按完整审查门复核实际 diff。

## External References

- N/A

## Open Questions / Risks

- 第一版依赖用户把回执路径显式交给主 Agent；这是已经确认的控制边界，不把“可能忘记回钩”提前升级成自动扫描功能。
- 规则与模板能提高交接质量，但不能从共享脏工作区事后恢复可靠作者归属；该限制必须在回执中如实暴露。
