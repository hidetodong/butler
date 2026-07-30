# debt（已知长期欠债）

> 只放悬着没还的账。还掉的删除、不留历史（历史归 `ITERATIONS` / `deliveries`）。

- **butler 仓自身不 dogfood 运行自己的 hook**：live 机械门禁（含双 active 迭代拦截 `single_active_iteration`）在 butler 仓内不触发——规则仓非部署项目，不装自己的 PreToolUse hook。改由 pytest 验证 hook 逻辑 + prompt 级一致性自检兜底 butler 侧。MILE-0001 R2 已补执行门禁 hook + 自检探针；"butler 侧不 live 化"仍是**已知设计约束**，非待修 bug。
- **可执行升级器尚缺真实外部老项目 dogfood**：ITER-0059 已用 v1.1/v2.0/v2.14/v2.15 隔离 fixture 真跑 dry-run/apply/rerun、漂移与失败恢复，旧“只靠协议未执行”债已关闭；但尚未在一份用户真实老项目上完成受监督升级。首次外部使用仍应保留 backup/journal 并人工审阅 diff。
- **`verify-schema` 的「人测道小结」与五件套 manifest 不一致**：`verify-schema.md §2` 把它列为条件必填字段（存在 `human·待人` AC 时必填），但 `tools/artifact-pipeline/artifacts.v1.json` 的 `verify_report.sections` 不含该段——写进去会被 `contract.py check` 判 `drift`，不写又违反 schema。ITER-0097 因 AC4 改判自动道而绕开，未修；任何真有人测残余的迭代都会撞上，需独立迭代对齐两处真源（改 manifest 加段 或 改 schema 改用折进 Verification Results 的口径）。
- **危险模式与 Loop 的规则语义仍错误耦合**：用户已明确 `dangerous` 只替代人工把关，`/butler:loop` 必须保持独立显式升档；当前 `dangerous-engine.md` §4/§6/§8/§9 与 `logic-protocol.md` 仍写成危险模式自动复用 Loop。ITER-0096 运行时已按用户指令停止绑定，但规则真源尚未修，需独立迭代统一算法、入口和回归，防止后续会话再次误触发。
