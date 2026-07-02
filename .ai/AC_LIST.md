---
状态: ack-frozen
ACK 日期: 2026-07-02
---

> ITER-0021（MILE-0002 R1）。分流与背景见 CONCEPT，不重述。验收范围已 ACK 冻结，进 P3。

# Goal

- 把测试纪律升级为**自动化优先**（竭尽自动化，含浏览器自动化覆盖 UI / 交互）+ 在 VERIFY_REPORT 引入**自动道 / 人测道**双道回填；人测道界定为机器不可测残余。

# In Scope

- `testing-strategy.md`：分层建议 → 自动化优先硬纪律 + 分道口径。
- `verify-schema.md`：VERIFY_REPORT 增分道回填字段。
- README / rule-card / PROJECT.md 接线与裁决。

# Out of Scope

- 分级置信（可靠 / 弱 / 待人）、代理验证（截图 diff / VLM 判图）、依赖感知准入 —— R2。
- 「交付自测」桥实现 —— R3。
- 不改 P1-P5 状态机、四件套字段脊柱、AC 验收脊柱、hook 代码。

# Acceptance Checklist

- [ ] AC1：`testing-strategy.md` §2 从"分层**建议**"改为"**自动化优先**"硬纪律——明确"凡机器能测的必须自动化"，并显式把 UI / 交互纳入自动道（浏览器自动化 / headless / 可编程视觉断言）；§3"关键路径**手动**验证完成"改为"关键路径**默认自动**验证，人测是例外残余"。
- [ ] AC2：`testing-strategy.md` 新增「分道口径」节——定义自动道（butler 可执行）/ 人测道（机器不可测残余）的判定标准；给出允许落人测道的**类目锚点清单**（主观审美 / 物理设备 / 真人感知 / 外部人工闸）；写明**默认归自动道**——拿不准时先尝试自动化，仅确证机器不可测才落人测道。
- [ ] AC3：`verify-schema.md` VERIFY_REPORT 模板 `AC Status` 每条 AC 增 **lane 标记**（`(auto)` / `(human)`），并新增「人测道小结」字段——列人测道各项及其待测 / 结论。
- [ ] AC4：`verify-schema.md` 编写规则补**分道回填要求**——自动道 AC 必须给可复现的自动验证证据；人测道 AC 必须说明为何机器不可测（对应 AC2 类目）。
- [ ] AC5：`verify-schema.md` **只加**分道字段——既有必填字段（Verification Summary / AC Status / Verification Results / Gate Coverage / Remaining Risks / Handoff）结构与语义不变，不破坏四件套脊柱。
- [ ] AC6：指针同步——`Coder/README.md` 中 `testing-strategy` / `verify-schema` 的一句话描述更新，反映自动化优先 + 分道；守"无隐式依赖"。
- [ ] AC7：`templates/rule-card.md` 裁决——"能自动必自动"是否入强制卡并记理由（倾向记一句强纪律）；`.ai/PROJECT.md` 现行纪律段按需前滚补"自动化优先测试纪律"一句（收口时）。
- [ ] AC8：不破坏不变量——P1-P5 状态机 / 四件套字段脊柱 / AC 验收脊柱 / hook 代码 / correction-contract 等未改；R2 / R3 内容（分级置信 / 代理验证 / 准入 / 桥）未被提前塞入；本仓五约束自检。

# Verification Method

- AC1/AC2：读改后 `testing-strategy.md`，核对纪律措辞（建议→必须）、UI 归自动道、§3 改写、分道口径节 + 类目清单 + 默认归自动道齐备。
- AC3/AC4/AC5：读改后 `verify-schema.md` 模板与编写规则，核对 lane 标记 + 人测道小结 + 分道回填要求；比对既有必填字段未增删改。
- AC6：grep `testing-strategy` / `verify-schema` 在 `README` 的描述，确认同步。
- AC7：看 rule-card 裁决记录 + PROJECT.md diff。
- AC8：`git diff --stat` 确认状态机 / 四件套 schema / hook / correction-contract 未动；通读确认无 R2/R3 内容混入。

# Open Questions / Risks

- 见 CONCEPT Open Questions（分道成节位置 / 回填形态 / rule-card 裁决 / 人测道类目清单），P3 定。
- 风险：R1 与 R2 边界——"浏览器自动化覆盖 UI"（R1，确定性断言）与"代理验证 / 弱视觉判断"（R2，分级置信）易混；本迭代只写"能确定性自动化的必自动"，把弱信号 / 置信分级显式留给 R2。
