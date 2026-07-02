# TECH_PLAN — ITER-0022

> ⚠️ 危险模式：本产物由模型自主 ACK（已过 §5.2 P3 设计自审门），未经用户确认（ITER-0022，2026-07-02）。

# Goal

落地 MILE-0002 R2：在 R1 分道二分之上叠**分级置信**（可靠 / 弱 / 待人），补**代理验证**把弱可测项拉回自动道，补**无人残余处置 + 依赖感知准入**让 `/dangerous` 长程自治遇人测残余不僵死、不假绿。全部为规则正文增量，不动状态机 / 字段脊柱 / hook。

# Design Decisions

- **DD1 置信档记法（AC1/AC2）**：置信档**合并进 R1 的 lane 标记**，不另立字段——`(auto·可靠)` / `(auto·弱)` / `(human·待人)`。三档判据写入 `verify-schema.md §4`（承既有「分道回填」bullet 追加「分级置信」bullet）；`§3` 模板 AC Status 示例与「人测道小结」块更新为带档形式。理由：承 R1 行内式最省、可读；`待人` 天然等价于 human 道残余，不产生新概念。
- **DD2 代理验证落点（AC3/AC4）**：`testing-strategy.md §3`（分道口径）下新增 **§3.1「代理验证」**——手段清单（截图对基线 diff / VLM 判读截图 / 启发式断言）+ earned `弱` 档 + 诚实边界（不冒充可靠绿）+ 置信三档统一口径；`§3` 判定纪律补一句"归人测道前先问能否造弱检查，能造=自动道弱档、不算残余"。新增子节不改 §3 编号，§4/§5 对 §3 的引用不受影响。
- **DD3 无人残余处置落点（AC5/AC6/AC7）**：`dangerous-engine.md §7`（安全护栏）下新增 **§7.4「无人残余处置与依赖感知准入」**——① 不阻塞、异步入账 ② 先尽量弱验证顶 ③ 依赖感知准入闸（叶子残余续跑 / 卡下游三处置：弱验证顶·砍分支·不具准入资格交还）④ 红线绝不假绿。additive，不 renumber。
- **DD4 与 §8 熔断的语义边界（风险 R2）**：§7.4 引语明确两条不同路径——**熔断**=能力 / 安全触顶、写 RCA 交还（既有 §8）；**残余入账**=不阻塞、续跑（新 §7.4）；仅当残余**卡死下游关键路径且连弱验证都造不出**时，才走准入闸交还。§8 补一句"待人残余异步入账、不阻塞自治继续"与 §7.4 呼应闭环。
- **DD5 接线（AC8）**：`rule-card.md` 自动化优先行补半句（能造弱检查就造 / 标弱不假绿）；`README.md` §99 group desc + §132 dangerous desc + §134 verify desc 补置信档 / 无人残余处置；`HUMAN_GUIDE.md` 275 / 286 注释补置信档 / 代理验证；`PROJECT.md` 现行约束前滚（收口步，属收口债）。
- **DD6 边界守恒**：不改 P1-P5 状态机、四件套脊柱、AC 验收脊柱、hook、correction-contract；不重构 R1 分道二分字段；不 renumber 既有 §（testing-strategy 新增 §3.1 子节、dangerous 新增 §7.4，均为末位追加）。`changelog-schema §4` 依赖的 verify-schema §4 只**追加 bullet**、不移动。

# Execution Steps

- [ ] T1（AC1/AC2）：`verify-schema.md` §4 加「分级置信」bullet（三档判据 + 记法）；§2 条件字段说明 + §3 模板 AC Status 示例 + 人测道小结块更新为带置信档形式。
- [ ] T2（AC3/AC4）：`testing-strategy.md` §3 新增 §3.1「代理验证」（手段清单 + earned 弱 + 诚实边界 + 三档口径）；§3 判定纪律补"先问能否造弱检查"一句。
- [ ] T3（AC5/AC6/AC7）：`dangerous-engine.md` §7 新增 §7.4「无人残余处置与依赖感知准入」（四要点 + 叶子/卡下游区分 + 红线 + 与 §8 边界引语）。
- [ ] T4（AC7）：`dangerous-engine.md` §8 补"待人残余异步入账、不阻塞自治继续"呼应句。
- [ ] T5（AC8）：`rule-card.md` 执行纪律「自动化优先」行补半句。
- [ ] T6（AC8）：`Coder/README.md` §99 group desc + §132 dangerous desc + §134 verify desc 更新。
- [ ] T7（AC8）：`HUMAN_GUIDE.md` 275 / 286 注释更新。
- [ ] T8（AC8）：全仓 §号 + 引用对账（testing §3 引用仍有效、verify §4 未移位、新 §号无悬挂）。
- [ ] T9：P5 §7.3 独立复核（fresh-context 子 agent，逐 AC）+ 原子收口五步（含 PROJECT 前滚）。

# Impact / Boundary

- 改（核心 3）：`verify-schema.md`、`testing-strategy.md`、`dangerous-engine.md`。
- 改（接线 4）：`rule-card.md`、`Coder/README.md`、`HUMAN_GUIDE.md`、`.ai/PROJECT.md`（收口前滚）。
- 不碰：状态机 / 四件套脊柱 / AC 脊柱 / hook / correction-contract / 桥（R3）/ 续跑（R4）。
- 回滚：本轮 iteration-open 提交为锚点，P4 改动叠其上，`git reset` 到锚点即回退全部自治改动、保留已自审 ACK 的计划。
