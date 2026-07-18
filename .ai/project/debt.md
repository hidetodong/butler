# debt（已知长期欠债）

> 只放悬着没还的账。还掉的删除、不留历史（历史归 `ITERATIONS` / `deliveries`）。

- **butler 仓自身不 dogfood 运行自己的 hook**：live 机械门禁（含双 active 迭代拦截 `single_active_iteration`）在 butler 仓内不触发——规则仓非部署项目，不装自己的 PreToolUse hook。改由 pytest 验证 hook 逻辑 + prompt 级一致性自检兜底 butler 侧。MILE-0001 R2 已补执行门禁 hook + 自检探针；"butler 侧不 live 化"仍是**已知设计约束**，非待修 bug。
- **可执行升级器尚缺真实外部老项目 dogfood**：ITER-0059 已用 v1.1/v2.0/v2.14/v2.15 隔离 fixture 真跑 dry-run/apply/rerun、漂移与失败恢复，旧“只靠协议未执行”债已关闭；但尚未在一份用户真实老项目上完成受监督升级。首次外部使用仍应保留 backup/journal 并人工审阅 diff。
