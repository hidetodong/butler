# Verification Summary

- 给收口加门槛（MILE-0001 收尾 R2）：新增 hook 规则 `single_active_iteration`（写 ITERATIONS 后 active 行 >1 即 deny，effective-text 还原 Write/Edit/MultiEdit 后全表）+ 15 条 pytest；定义并接线冷启动一致性自检 5 不变量（对 butler 自身也生效）；把收口强化为原子仪式（§5.5 五步，末步自检）。改动集中在 hook 子树 + 20/40 层文档接线，未碰 phase_gate/ledger_status 判据、四件套字段 schema、状态机、根 CHANGELOG、VERSION。
- 危险模式 §7.3：P5 升格完整审查（非简评），逐维审新 Python 规则；用户显式 ACK + 授权自治，回滚锚点 = commit `1b3eca2`。

# AC Status

- [x] AC1 ✓ `rules/single_active_iteration.py`：对 `.ai/ITERATIONS.md` 写入统计写入后 active 行，>1 即 deny，reason 含命中迭代号、remediation 指向 §5.5/§5.6。
- [x] AC2 ✓ effective-text 还原：Write 取 content；Edit 读现文件替换 old→new 首次；MultiEdit 按序套用；读失败/未命中退化为片段计数（allow-on-uncertainty，不误杀）；非台账路径/空表放行。测试覆盖以上全部分支。
- [x] AC3 ✓ 注册进 `butler_gate.py` RULE_MODULES（ledger_status 之后、artifact_chain 之前）；first-deny-wins/fail-closed/bypass 契约未改（integration 测试全绿）。
- [x] AC4 ✓ 新增 `tests/test_single_active_iteration.py`（15 例）；`python3 -m pytest tests/` = **97 passed**（原套件无回归）。
- [x] AC5 ✓ 一致性自检 5 不变量定义于 `context-persistence.md` §冷启动一致性自检：current↔状态 / 至多一个 active / closed 有交付且文件存在 / closed 有归档 / 里程碑路线项对账。
- [x] AC6 ✓ 自检落进冷启动读序段（§6 之后），明文"发现漂移先暴露、不静默继续"。
- [x] AC7 ✓ `iteration-schema §5.5` 收口强化为原子仪式五步（前三必做+第四按需+第五自检）；`lifecycle §165` 同步（收口原子仪式、⑤ 自检）。
- [x] AC8 ✓ `iteration-schema §5.1` 交叉引用 hook 门禁；`templates/hooks/README.md`（规则清单+运行机制）、`mcv-deployment §5`、`Coder/README.md` 均注册/描述新规则。
- [x] AC9 ✓ dogfood：对 butler 自身 `.ai/` 跑 5 不变量 = **全绿**（current=ITER-0019 唯一 active；18 closed 全有归档 + 交付文件全存在；R1/R3 closed、R2 active 对账一致）；rule-card 裁决不进强制产物集（grep 0 门禁命中，文件未改）。
- [x] AC10 ✓ git diff 确认 concept/acceptance/tech-plan/verify schema、根 CHANGELOG、VERSION、rule-card、phase_gate、ledger_status 均未改；P1-P5 状态机未动；hook 零三方依赖、fail-closed 保持（pytest 全绿佐证）。

# Verification Results

- AC1/2/3：读规则 + butler_gate diff（+17 行仅注册），核对判据/effective-text/契约。
- AC4：实跑 `rtk proxy python3 -m pytest tests/` → 97 passed；单跑新文件 15 passed。
- AC5/6/7/8：逐文件读改动段核对；grep `single_active` 命中 hook README / mcv-deployment / Coder README / iteration-schema。
- AC9：bash 实跑 5 不变量对 butler `.ai/`，逐 closed 行校验交付文件 `test -f` 全存在。
- AC10：`git diff --quiet HEAD -- <不变量文件>` 逐个确认未改。

# Gate Coverage

- 通用质量门禁：新 Python 规则含 docstring + 类型注解（`from __future__ import annotations`，Py3.9 兼容）；镜像 ledger_status 结构；无三方依赖。
- Active Profiles：Python（hook 子树）——pytest 97 passed、零依赖、fail-closed 未破。
- Tech Plan Alignment：T1–T11 全兑现；Design Decisions Q1（独立规则命名）/Q2（effective-text+allow-on-uncertainty）/Q3（自检内联 context-persistence）/Q4（不做 /close，延后）均按方案落地。
- References Compliance：N/A（无 `.ai/references/`）。

# Independent Review

- 复核方式：同上下文完整多维审查（危险模式 §7.3 要求升格完整审查；环境未起 fresh-context 子 agent，按 review-engine §6.4 如实标注"未独立"）。
- 逐维结论：逻辑（effective-text 三分支 + 计数正确，close/正常开新不误触发）、健壮性（空/读失败/未命中均有兜底）、安全（仅读 cwd 内台账、无 eval/注入）、一致性（镜像 ledger_status）——**无 Must Fix**。

# Remaining Risks

- **Should Fix（不阻断，按 ITER-0018 口径记此）**：Edit/MultiEdit 在 `old_string` 未命中现文件时退化为片段计数，可能漏判"隐蔽的双 active"——有意的 allow-on-uncertainty 取舍（避免误杀），残留由 Write 全覆写路径 + 冷启动一致性自检兜底。正常"先收口再开新"流程不受影响。
- butler 仓自身不跑 hook → 门禁无法在 butler 内 live 触发，靠 pytest 验证 + prompt 级自检覆盖 butler 侧（已知设计约束）。
- `/close` 原子收口命令未做（Q4 延后）——收口仪式已清单化 + 自检，命令化留作后续 polish。
- 无遗留 Must Fix。

# Handoff / Next Step

- ITER-0019 验证闭环，可收口（归档 + changelog 切片 + 交付 md/html + 台账 closed + PROJECT 前滚 + 收口自检）。
- 收口后 MILE-0001 三路线项（R1/R2/R3）全 closed，可聚合发布（切版 + 根 CHANGELOG + migrations）——本次按用户指令只提交推送、不切版，里程碑聚合发布留作后续。
