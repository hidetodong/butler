# Verification Summary
- 覆盖范围：D1（ACK/冻结状态外化）+ D4（入口分流三档化、分流记录、升级转换）的规则层与 hook 层改动，及 butler 自身 ITER-0004 收口 dogfood
- 总体结论：AC1–AC11 全部满足；hook 三态实测符合设计，69 项测试全绿无回归；迭代闭合

# AC Status
- [x] AC1: acceptance-schema 加 `状态`/`ACK 日期` 字段与语义（§2/§3/§4）
- [x] AC2: lifecycle P2 写明 draft→ack-frozen 状态机、dangerous 自审门置位、amend 退回 draft
- [x] AC3: iteration-schema §5.2 冻结物化、§5.3 amend 退回 draft
- [x] AC4: phase_gate.py draft→deny、ack-frozen/无字段→allow（实测通过）
- [x] AC5: hook 测试覆盖 draft/frozen/legacy/未知值/英文 key，69 passed 无回归
- [x] AC6: rule-card ACK 文案改为"置 ack-frozen 即冻结"
- [x] AC7: lifecycle §2.2 三档边界（极小/简化/完整）已定义
- [x] AC8: lifecycle §2.3 分流记录 + concept-schema/acceptance-schema 落点登记
- [x] AC9: lifecycle §2.4 低档→高档升级转换已定义
- [x] AC10: logic-protocol §5 对齐极小边界并引用 §2；rule-card 同步三档与升级
- [x] AC11: 本迭代 CONCEPT 带分流记录、AC_LIST 经 draft→ack-frozen；ITER-0004 三步收口

# Verification Results
- AC1: `acceptance-schema.md` §2 必填字段加冻结 frontmatter；§3 模板顶部加 `状态`/`ACK 日期`；新增 §4 冻结状态字段定义 draft/ack-frozen 语义、hook 联动、amend 退回、简化路径可选。
- AC2: `lifecycle.md` P2 强制规则首条改写为"ACK 物化为 `状态` 字段、draft 被 hook 拦、`/dangerous` 自审门自置、amend 退回 draft"。
- AC3: `iteration-schema.md` §5.2 新增"物化标志：冻结 = `状态: ack-frozen`"；§5.3 动作加"把 `状态` 退回 `draft` 重新 ACK"。
- AC4: 仿 `mcv-deployment §5.3` 真实子进程实测——draft→exit 2 + `phase_gate` + 明确 reason；ack-frozen→exit 0；legacy 无字段→exit 0。三态均符合设计。
- AC5: `uv run --with pytest pytest` → 69 passed；新增 `TestAcFreezeGate`（draft/frozen/legacy/未知值/英文 key 五例）+ 整合测试 draft→exit 2；既有 `full-artifacts`/`with-bypass-reason` legacy 用例不回归。
- AC6/AC10: `rule-card.md` 强制工作流段重写为三档 + 分流记录 + 升级转换；ACK 行与迭代化需求段同步 ack-frozen 口径。`logic-protocol.md §5` 改为三档分流并引用 `lifecycle.md §2`。
- AC7/AC8/AC9: `lifecycle.md §2` 重构为 §2.1 升级信号 / §2.2 三档边界 / §2.3 分流记录 / §2.4 升级转换；`concept-schema.md`（完整路径落点）与 `acceptance-schema.md`（简化路径落点）各自登记分流记录位。
- AC11: 工作区四件套已整体覆写为 ITER-0004；`.ai/CONCEPT.md` 顶部含分流记录行、`.ai/AC_LIST.md` 顶部 `状态: ack-frozen` + `ACK 日期: 2026-06-15`；归档与台账见收口步骤。

# Gate Coverage
- 通用质量门禁：`uv run pytest`（69 passed）+ 真实 `butler_gate.py` 子进程三态实测 + grep 交叉核对章节号与跨文件引用一致。
- Active Profiles：未命中，N/A。
- Tech Plan Alignment：Design Decisions 全部兑现——扫描 `状态` 行不引 YAML 依赖、无字段 legacy 放行、未知值保守 deny、三档保留、升级转换补产物不推翻、已知局限如实标注。
- References Compliance：本轮无外部参考资料，N/A。

# Remaining Risks
- 已知局限（如实标注、本轮不解决）：hook 只能校验"字段写了 frozen"，不能校验"人是否真的 ACK"；`/dangerous` 模式由模型自置 ack-frozen，属自校验。
- `_STATUS_RE` 用 `re.IGNORECASE` 匹配 `状态`/`status` 取首个匹配；理论上正文若在 frontmatter 之前出现 `状态:` 行会误命中，但实际 AC_LIST 字段恒在顶部 frontmatter，风险极低。
- 简化路径 AC_LIST `状态` 字段可选（省略即 legacy 放行）；这是有意取舍，避免轻量任务被 hook 拖累，但也意味着简化路径的冻结不强制可见。
- D2 / D3 / D5 / D6 四条 review 缺陷未动，留作后续迭代候选（D3 的 AC-ID linkage 仍可落在占位的 `artifact_chain.py`）。

# Handoff / Next Step
- 本迭代已闭合，无跨会话接力需求。下一步若继续，可挑 D2（P1→P2 确认门）或 D5（迭代台账一致性 linter）开新迭代。
