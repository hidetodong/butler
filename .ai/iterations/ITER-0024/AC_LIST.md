---
状态: ack-frozen
ACK 日期: 2026-07-02
ACK 方式: 危险模式 P2 自审门 self-ACK（非用户显式 ACK）
迭代: ITER-0024
里程碑: MILE-0002 R4
---

# AC_LIST — ITER-0024

> ⚠️ 危险模式：本 AC 清单未经用户显式 ACK，由 P2 自审门（对照 `acceptance-schema.md`）自主冻结；自审结论见 `RUN_LOG.md` ITER-0024 · P2-self-ack。
> 说明：R4 主体是规则协议接线（`auto·可靠`=读规则确认存在且自洽），另叠一条 `auto·可靠` 机械验证（真跑桥回路证明协议可执行）。

## 闭环协议成文（G1）

- **AC1**：新增 `Coder/20_Workflow_Lifecycle/human-test-bridge.md`，frontmatter 含 audience + scope；正文定义 ①触发条件（P5 存在 `human·待人` 残余 **且** 有人在场）②等待-回收-续跑闭环步骤（生成 manifest → `run_in_background` 起桥 → 阻塞等桥进程退出 → 读 `results.json` → 四态路由回填 `VERIFY_REPORT`）③调用形态（butler 传 manifest 路径调用 butler 驻留工具、不拷副本）。
  - 验证（auto·可靠）：读该文件确认三部分齐全、frontmatter 合规。
- **AC2**：协议**不复述**工具 schema——manifest / results 字段以 `tools/delivery-selftest/README.md` 为契约真源，桥协议只引用不重抄（单一来源纪律）。
  - 验证（auto·可靠）：读协议确认引用工具 README 为契约真源、无字段级重抄。

## 四态路由口径（G2）

- **AC3**：四态路由语义成文：`pass`=计入收口 / `fail`=进 `correction-contract` 纠错（备注当线索）/ `defer`=入欠债账（Remaining Risks + handoff）不阻塞收口 / `skip`=记 N/A（非欠债）；四态结论回填 `VERIFY_REPORT.md`。
  - 验证（auto·可靠）：读协议路由表确认四态齐全、动作明确、含回填要求。
- **AC4**：路由表与工具 `README.md`「四态 → 路由语义」表**逐条一致**（同机器码、同下游动作），不出现口径分叉。
  - 验证（auto·可靠）：并置两表逐行比对一致。

## P5 / 纠错 / 无人 接线（G3/G4/G5）

- **AC5**：`verify-schema.md`（人测道回填处）与 `testing-strategy.md §3`（人测道界定处）均以文件名指向 `human-test-bridge.md` 作为人测残余的回传通道；接线为**增量追加**、不移动既有小节、不破坏 `changelog-schema` 对 verify-schema §4 的引用。
  - 验证（auto·可靠）：grep 两文件含 `human-test-bridge` 引用；确认 verify-schema §4 未移位。
- **AC6**：`correction-contract.md` 明确"人测 `fail`（经桥回传）进本契约纠错闭环、备注当线索"，且落在既有章节的增量追加、不破坏其常驻底线定位。
  - 验证（auto·可靠）：读 correction-contract 确认新增该口径。
- **AC7**：`dangerous-engine.md §7.4/§8` 与 `human-test-bridge.md` **双向一致**厘清岔口——桥属**有人场次**工具；`/dangerous` 无人场次**不起桥**（否则永久阻塞），走 §7.4 依赖感知准入闸；桥协议反向指向 §7.4 为无人分支。
  - 验证（auto·可靠）：读两文件确认双向指向且语义不矛盾（有人起桥 / 无人走准入闸）。

## 注册 + 前滚（G6）

- **AC8**：`Coder/README.md` 目录结构 + 读序/文件说明注册 `human-test-bridge.md`；工具 `README.md` 把"接进 P5 / 纠错闭环、后台等待续跑是 R4"改为**已完成**并指向协议；`templates/rule-card.md` 收录一句人测回传闭环口径；`.ai/PROJECT.md` 收口前滚（现行约束 + 架构图按需）。
  - 验证（auto·可靠）：读四处确认注册 / 改写 / 收录 / 前滚到位。

## 机械跑通闭环（G7）

- **AC9**：真跑一遍 butler 侧回路证明协议可执行——写样例 manifest → 用 `run_in_background` 起 `bridge.js`（`--no-open --port <p> --out <results>`）→ 程序化 POST `/submit` 四态 payload → 后台桥进程 **exit 0** 自退 → 读 `results.json` 解析出四态 → 按路由表演示 `pass/fail/defer/skip` 各自分派动作。
  - 验证（auto·可靠）：实际执行上述回路，断言进程退出码 0、`results.json` 落盘且四态可解析、路由分派与协议表一致。

## In / Out Scope

- **In**：闭环协议成文（触发 + 五步 + 调用形态）+ 四态路由口径 + P5/纠错/无人三处接线 + 注册前滚 + 机械跑通验证。
- **Out**：**不写**部署注册文档（mcv-deployment / HUMAN_GUIDE 调用方式登记）、**不做**真实项目端到端 dogfood（R5）；不改桥工具代码 / 四态机器码 / hook / 状态机 / 四件套脊柱；不做多人 / 远程 / 持久看板。

## 风险

- R1：run_in_background 的"进程退出即续跑"依赖 harness 后台能力，不同 harness 行为可能差异 → 协议描述机制与依赖，机械验证在本 harness 证明可行；跨 harness 差异记 Remaining Risks。
- R2：有人 / 无人岔口写不清会与 dangerous §7.4 冲突（无人下误起桥→永久阻塞）→ AC7 强制双向一致对账兜底。
- R3：manifest / results 落点若与四件套混放会污染工作区 → 约定落 `.ai/human-test/`、隔离，机械验证用临时路径不入库。
