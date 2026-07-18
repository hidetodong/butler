> 分流: 完整 | 命中升级信号: 多文件改动、契约变更、跨模块影响、设计取舍 | 2026-07-18

# 一句话

- R5 用只读程序裁决“现在有没有资格收口”，任一方案、校准、AC、证据、审查或阻断事实不一致都拒绝。

# Goal

- 交付确定性 Goal completion adjudicator 和覆盖 R1 八类假完成的负向回归。

# Current Understanding

- 裁决器不替代真源，只组合读取；输出 eligible 只是允许执行收口仪式，complete 仍由 closed + 收口事实派生。
- Evidence Index 的路径在 active 阶段指向未来 archive，工具需从 hot record 验证并对账 AC 覆盖。
- review 与 blocker 需要 VERIFY 提供最小机读输入，不能从乐观散文猜。

# Constraints

- 默认只读、JSON 稳定输出；ineligible 为业务结论 exit 1，格式/环境错误 exit 2。
- 必须 fail-closed，未知/缺字段不得默认为绿。
- 不写台账、不自动 close、不信宿主 complete、不以 task done 为输入。
- R6 才做宿主接线与模板升级。

# Impact Scope

- 新增 `tools/goal-assurance/` CLI/测试，增强 VERIFY schema、Goal Contract/lifecycle/rule-card/README，接入固定 CI。

# Project Type / Active Profiles

- Python 标准库 CLI + Markdown 规则；危险模式 ON。

# Open Questions

- 无阻塞问题。
