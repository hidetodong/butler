# debt（已知长期欠债）

> 只放悬着没还的账。还掉的删除、不留历史（历史归 `ITERATIONS` / `deliveries`）。

- **butler 仓自身不 dogfood 运行自己的 hook**：live 机械门禁（含双 active 迭代拦截 `single_active_iteration`）在 butler 仓内不触发——规则仓非部署项目，不装自己的 PreToolUse hook。改由 pytest 验证 hook 逻辑 + prompt 级一致性自检兜底 butler 侧。MILE-0001 R2 已补执行门禁 hook + 自检探针；"butler 侧不 live 化"仍是**已知设计约束**，非待修 bug。
- **项目自有 hook 与 Butler 受管目录不能共存**：若项目把自有文件放进 `.claude/hooks/`，升级器会把它视为受管树漂移并拒绝覆盖；`claude-skills` 已证明守门行为正确，但尚无安全的共存或目录所有权合同。解决前不得用扩大白名单绕过。
- **`verify-schema` 的「人测道小结」与五件套 manifest 不一致**：`verify-schema.md §2` 把它列为条件必填字段（存在 `human·待人` AC 时必填），但 `tools/artifact-pipeline/artifacts.v1.json` 的 `verify_report.sections` 不含该段——写进去会被 `contract.py check` 判 `drift`，不写又违反 schema。ITER-0097 因 AC4 改判自动道而绕开，未修；任何真有人测残余的迭代都会撞上，需独立迭代对齐两处真源（改 manifest 加段 或 改 schema 改用折进 Verification Results 的口径）。
- **危险模式与 Loop 的规则语义仍错误耦合**：用户已明确 `dangerous` 只替代人工把关，`/butler:loop` 必须保持独立显式升档；当前 `dangerous-engine.md` §4/§6/§8/§9 与 `logic-protocol.md` 仍写成危险模式自动复用 Loop。ITER-0096 运行时已按用户指令停止绑定，但规则真源尚未修，需独立迭代统一算法、入口和回归，防止后续会话再次误触发。
