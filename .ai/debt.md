# debt（已知长期欠债）

> 只放悬着没还的账。还掉的删除、不留历史（历史归 `ITERATIONS` / `deliveries`）。

- **butler 仓自身不 dogfood 运行自己的 hook**：live 机械门禁（含双 active 迭代拦截 `single_active_iteration`）在 butler 仓内不触发——规则仓非部署项目，不装自己的 PreToolUse hook。改由 pytest 验证 hook 逻辑 + prompt 级一致性自检兜底 butler 侧。MILE-0001 R2 已补执行门禁 hook + 自检探针；"butler 侧不 live 化"仍是**已知设计约束**，非待修 bug。
- **项目自有 hook 与 Butler 受管目录不能共存**：若项目把自有文件放进 `.claude/hooks/`，升级器会把它视为受管树漂移并拒绝覆盖；`claude-skills` 已证明守门行为正确，但尚无安全的共存或目录所有权合同。解决前不得用扩大白名单绕过。
- **`/butler:upgrade` 从未在真实已部署项目上跑过**：升级器（`tools/butler-upgrade/`）有 16 项历史 / 负向 / 事务专项进 CI，但全部跑在临时 fixture 上；真实老项目跨多个版本升级的端到端回归一次没做过。MILE-0016 R15 计划补这次回归。本条自 ITER-0112 从已删除的 `.ai/project/architecture.md` 成熟度段迁出。
