# TECH_PLAN — ITER-0024

> ⚠️ 危险模式：本产物由模型自主 ACK（已过 §5.2 P3 设计自审门），未经用户确认（ITER-0024，2026-07-02）。

# Goal

把 R3 交付自测桥接进 butler SOP：新增等待-回收-续跑闭环协议 `human-test-bridge.md`，定四态路由，接线 P5 / 纠错 / 无人降级，注册前滚，并机械跑通一遍证明协议可执行。

# Design Decisions

- **DD1 新协议落 `20_Workflow_Lifecycle/human-test-bridge.md`（AC1）**：它是 P5 的生命周期子流程（等待-回收-续跑），非质量门禁判据，故归 20_ 而非 30_。文件名与工具"交付自测桥"呼应。结构：§1 定位 / §2 触发条件 / §3 等待-回收-续跑闭环（五步）/ §4 四态路由 / §5 无人场次降级 / §6 调用形态 / §7 与其他规则关系。
- **DD2 契约单一来源（AC2）**：manifest / results 字段 schema 只在 `tools/delivery-selftest/README.md`，协议引用不重抄；协议管"何时起、怎么等、怎么路由"，工具 README 管"传什么、回什么"。
- **DD3 四态路由表 = 工具 README 镜像（AC3/AC4）**：协议 §4 路由表与工具 README 同机器码同动作（pass=收口 / fail=纠错 / defer=入账不阻塞 / skip=N/A），并补 SOP 侧动作（回填 VERIFY_REPORT / 进 correction-contract / 记 Remaining Risks+handoff）。两表并置比对确保不分叉。
- **DD4 接线用文件名互引、增量追加（AC5/AC6/AC7）**：
  - `verify-schema.md`：§4 编写规则加一条 bullet——人测道残余的回传闭环见 `human-test-bridge.md`（有人场次经桥四态回填；无人走 dangerous §7.4）。§4 不移位（护 changelog-schema 引用）。
  - `testing-strategy.md §3`：人测道判定纪律末尾加一句——落人测道的残余，其回传闭环走 `human-test-bridge.md`。
  - `correction-contract.md §3`：加一条关系 bullet——人测 `fail`（经桥回传）进本契约纠错闭环、备注当线索。
  - `dangerous-engine.md §7.4`：加一句——交付自测桥属有人场次工具，无人值守下不起桥（否则永久阻塞），无人残余按本节准入闸处置；§8 注已有"待人不构成停止条件"，补指有人分支走 `human-test-bridge.md`。
  - 均为增量，不 renumber、不移动既有小节。
- **DD5 无人岔口双向锁死（AC7）**：桥协议 §5 明写"无人场次不起桥 → 走 dangerous §7.4"；dangerous §7.4 明写"桥属有人场次 → 无人不起桥"。两处互指，语义一致（有人=弹页面等人；无人=异步入账/准入闸）。
- **DD6 调用形态只定协议、不做部署登记（AC1/Out）**：协议 §6 描述外部项目调用形态（butler 传 manifest 路径调 butler 驻留 `bridge.js`、不拷副本、`--out` 收 results），并标注"具体路径解析 / 部署注册 / HUMAN_GUIDE 登记留 R5"。避免与 R5 抢范围。
- **DD7 落点隔离（AC9/风险 R3）**：约定运行期 manifest/results 落 `.ai/human-test/`（与四件套隔离、建议 gitignore）；机械验证用临时目录（`/tmp` 或工作树临时路径），产物不入库。
- **DD8 机械验证复用桥、不新增工具代码（AC9/Constraints）**：写一次性样例 manifest，`run_in_background` 起 `bridge.js --no-open`，node/`curl` 程序化 POST 四态，断言 exit 0 + results.json 四态 + 路由分派。桥体代码不动；若暴露缺陷另记欠债。

# Execution Steps

- [x] T1（AC1/AC2/AC3/AC4）：新增 `Coder/20_Workflow_Lifecycle/human-test-bridge.md`（§1-§7，含四态路由表镜像工具 README、引用契约真源）。
- [x] T2（AC5）：接线 `verify-schema.md` §4 + `testing-strategy.md §3`（增量追加、文件名互引、§4 不移位）。
- [x] T3（AC6）：接线 `correction-contract.md §3`（人测 fail 进纠错闭环）。
- [x] T4（AC7）：接线 `dangerous-engine.md §7.4/§8`（有人起桥 / 无人走准入闸，与桥协议双向一致）。
- [x] T5（AC8）：注册 `Coder/README.md`（目录 + 文件说明）；改工具 `README.md`（R4 已完成 + 指向协议）；收录 `rule-card.md` 一句。
- [x] T6（AC9）：机械跑通闭环——样例 manifest → 起桥（&/run_in_background）→ POST 四态 → 断言 exit 0（自退）+ results.json summary{pass:1,fail:1,defer:1,skip:1} + 路由分派 ASSERT PASS。
- [x] T7：一致性对账——7 处新引用可解析、四态两表逐条一致、verify §4 未移位（changelog-schema §4 引用不破）、dangerous §7.4↔协议 §5 双向指向。
- [ ] T8：P5 §7.3 独立复核（fresh-context 子 agent，逐 AC + 一致性 + dogfood 可读性）+ 原子收口五步（含 PROJECT 前滚）。

# Impact / Boundary

- 新增：`Coder/20_Workflow_Lifecycle/human-test-bridge.md`。
- 改（接线）：`verify-schema.md` / `testing-strategy.md` / `correction-contract.md` / `dangerous-engine.md` / `Coder/README.md` / `templates/rule-card.md` / `tools/delivery-selftest/README.md` / `.ai/PROJECT.md`。
- 不碰：桥工具代码、hook、四件套 schema、状态机、四态机器码、R5 部署 / dogfood。
- 回滚：本轮 iteration-open 提交为锚点，P4 接线叠其上，`git reset` + 清未跟踪即回退。
