---
状态: ack-frozen
ACK 日期: 2026-06-30
---

> ITER-0019（MILE-0001 R2）。P2 经用户显式 ACK 冻结（2026-06-30），并授权 `/dangerous` 危险模式自治执行至收口；验收范围锁定，进入 P3。背景见 CONCEPT，不重述。

# Goal

- 给收口加门槛：hook 机械拦截"未收口先开新迭代"+ 冷启动一致性自检探针（butler 自身可跑）+ 原子收口仪式清单。MILE-0001 收尾路线项。

# In Scope

- 新增 hook 规则（单 active 迭代不变量）+ pytest + 派发器注册。
- 冷启动一致性自检不变量清单 + 落进读序。
- §5.5 收口原子清单 + 末尾自检步。
- hook/规则接线 + dogfood 自检。

# Out of Scope

- 不改 phase_gate / ledger_status 既有判据。
- 不改四件套字段结构、AC 脊柱、P1-P5 状态机、版本机制、根 CHANGELOG。
- `/close` 命令实现（如 P3 判定做则纳入，否则延后）。

# Acceptance Checklist

- [ ] AC1: 新增 hook 规则，对 `.ai/ITERATIONS.md` 写入做机械门禁——写入后 active 迭代行 > 1 即 `deny`（语义=未收口/废弃旧迭代就开新）；deny 文案含命中行号与 remediation（先按 §5.4/§5.6 收口或废弃）。
- [ ] AC2: 规则正确处理 Write / Edit / MultiEdit——用 effective-text（Write 取 content；Edit/MultiEdit 读现文件套用替换后）还原写入后全表再计数，避免 Edit 片段只见新行漏看旧 active；非 ITERATIONS 路径与半写/空表不误杀。
- [ ] AC3: 规则注册进 `butler_gate.py` 的 `RULE_MODULES`（合理顺序）；保持 first-deny-wins / fail-closed / bypass 契约不变。
- [ ] AC4: 新增 `templates/hooks/tests/test_<规则>.py`，覆盖：单 active 放行 / 双 active 拒绝 / 全 closed 放行 / 收口同写（旧 closed+新 active）放行 / Edit 新增 active 触发 / 非台账路径放行 / 空表放行；`cd templates/hooks && python3 -m pytest tests/` 全绿。
- [ ] AC5: 定义冷启动一致性自检不变量清单：① current↔状态（current=ITER-N 则该行 active；current=none 则无 active）② 至多一个 active ③ closed 行须有收口日期+交付链接，且 `deliveries/<链接>` 存在 ④ closed 行须有 `iterations/ITER-N/` 归档 ⑤ 里程碑路线项状态与迭代实际状态对账。
- [ ] AC6: 一致性自检落进 `context-persistence.md` 冷启动读序——冷启动读完台账后跑自检，发现漂移先暴露、不静默继续。
- [ ] AC7: `iteration-schema.md §5.5` 收口强化为原子有序清单（含 R1 前滚 PROJECT + R3 必产 changelog），末尾加"收口自检"步（跑 AC5 探针）；`lifecycle.md §165` 同步。
- [ ] AC8: `iteration-schema.md §5.1` 交叉引用新 hook 门禁（如 ledger_status 的交叉引用写法）；hook `README.md` + `mcv-deployment.md §5` + `Coder/README.md` 注册/描述新规则。
- [ ] AC9: dogfood——对 butler 自身 `.ai/` 跑一遍 AC5 一致性自检并记录结果（现状预期全绿）；rule-card 裁决（门禁不进强制产物集，记理由）。
- [ ] AC10: 不破坏不变量——四件套字段 schema / phase_gate / ledger_status 判据 / P1-P5 状态机 / 根 CHANGELOG / VERSION 未动；本仓五约束自检；hook 零三方依赖、fail-closed 保持。

# Verification Method

- AC1/AC2/AC3: 读新规则 + butler_gate diff，核对判据 / effective-text / 注册 / 契约。
- AC4: 实跑 `python3 -m pytest tests/`，贴通过数。
- AC5/AC6: 读 context-persistence 冷启动段，核对不变量清单 + 触发点。
- AC7: 读 iteration-schema §5.5 + lifecycle §165，核对原子清单 + 自检步。
- AC8: grep 新规则名在 hook README / mcv-deployment / Coder README / iteration-schema 的注册与交叉引用。
- AC9: 跑自检记录 + grep rule-card。
- AC10: git diff 确认未碰不变量文件；pytest 全绿即 fail-closed/零依赖未破。

# Open Questions / Risks

- 见 CONCEPT Open Questions（规则命名 / effective-text 口径 / 自检落点 / 是否做 /close），P3 定。
- 风险：butler 自身不跑 hook → 门禁无法在 butler 内 live 验证，靠 pytest 充当验证（与现有规则同策略）。
- 风险：effective-text 读现文件失败（IO 异常）→ 按 fail-closed 与现有规则一致处理，不放过也不误杀（P3 定边界）。
