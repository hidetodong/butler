# ITER-0083 · handoff 确定性可信闭环

## 本次交付目标

把经常漏写、内容可能陈旧的会话交接改成由权威状态确定性生成、可机械验鲜、失效可重建的派生视图。

## 已完成内容

- 新增标准库实现的 handoff 工具，提供 inspect、sync、check 三个命令。
- 用来源哈希、状态快照与成品哈希组成 receipt，检测来源变化、状态漂移和成品篡改。
- 接入 PostToolUse 提醒、冷启动协议、状态审计和完整 CI；写入采用成对事务并在失败时回滚。
- 固定 H1 与六个 H2，限制输入源和提取长度，不再依赖模型自由发挥交接结构。

## 关键变更 / 用户可感知变化

- `.ai/02_SESSION_HANDOFF.md` 现在只由工具生成，陈旧时明确拒绝，不再被当成独立真源。
- 权威状态变化后可用 `sync` 幂等重建；未变化重复生成得到相同内容。
- 当前迭代/里程碑指针会校验前缀、最少四位与 active 状态，错误状态 fail-closed。
- 纯聊天中从未落盘的决定仍无法恢复，重要决定必须先进入权威状态文件。

## 高层影响范围

- `tools/handoff/`
- `templates/hooks/`、`scripts/audit-project-state.py`、`scripts/verify-ci.sh`
- handoff、context persistence、maintenance boundary 与冷启动入口文档

## 验证方式与结果摘要

- handoff 工具最终 6 项测试通过，覆盖幂等、陈旧/篡改、错误指针和事务回滚。
- hook 与状态审计专项通过，完整 hooks 197 项通过。
- 完整 CI 复核通过，Goal adjudicator 十项检查全绿并判定 eligible。
- 证据索引：`.ai/iterations/ITER-0083/VERIFY_REPORT.md` 与 `.ai/iterations/ITER-0083/evidence/`。

## 已知剩余风险 / 延后事项

- 工具不能恢复从未写入任何权威状态文件的纯聊天决定；这是明确边界，不是假装可恢复。
- 当前环境按约束未启动 fresh-context 独立复核；已执行危险模式完整自审并修复两项 Must Fix。
- 本迭代由模型自主 ACK，并附 P5 完整审查结论；用户已授权本次受控 bypass，但本迭代未实际使用 bypass。

## 引用

- `.ai/iterations/ITER-0083/`
- `.ai/iterations/ITER-0083/evidence/`
- `Coder/40_Context_Management/handoff-spec.md`
- `tools/handoff/`

