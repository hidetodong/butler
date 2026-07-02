---
状态: ack-frozen
ACK 日期: 2026-07-02
迭代: ITER-0025
里程碑: MILE-0002 R5
---

# AC_LIST — ITER-0025

> 标准模式：本清单经用户显式 ACK 冻结（2026-07-02），验收范围锁定，进 P3。
> R5 主体是文档接线（部署侧 + 人类侧）+ 一次真 dogfood；文档类 AC 验证=读文件确认写到位（`auto·可靠`），dogfood AC 验证=真跑外部调用回路（`auto·可靠`）。

## 部署侧文档（G1）

- **AC1**：`Coder/20_Workflow_Lifecycle/mcv-deployment.md` 新增"butler 驻留工具调用"一节，含：① 驻留工具类别定义（存 butler 仓、**不拷进目标项目**、目标项目传参调用）② 桥的具体调用形态（复用本文件 §0 的 `$BUTLER` 路径发现 → `node $BUTLER/tools/delivery-selftest/bridge.js <manifest> --out <本项目 results>`）③ manifest / results 落点（本项目 `.ai/human-test/`，建议 gitignore）。
  - 验证（auto·可靠）：读该节确认三点齐全、明写"不拷副本、传路径调用"、路径解析引用 §0 不另造。
- **AC2**：该节**不重抄** manifest / results 字段与四态机器码——以 `tools/delivery-selftest/README.md`（契约）+ `human-test-bridge.md`（下游语义）为真源，仅引用；无人场次以文件名指向 `dangerous-engine.md §7.4`（不起桥走准入闸）。
  - 验证（auto·可靠）：读该节确认引用三处真源、无字段级重抄、含无人岔口指引。

## 人类侧文档（G2）

- **AC3**：`HUMAN_GUIDE.md` 新增人测桥使用说明（一小节）：说清 P5 出现机器测不了的残余时会**弹一个浏览器分步流程页**，用户对每项点**四态（通过 / 未通过 / 跳过 / 延后处理）+ 备注**，提交即续跑；四态各自下游含义一句话带过（通过=计入 / 未通过=返修 / 延后=记账不挡 / 跳过=不测）。
  - 验证（auto·可靠）：读该小节确认覆盖"何时弹、点什么、四态含义、提交即续跑"，措辞面向人类用户（非 AI 指令腔）。
- **AC4**：该说明与 `扩展模式` / `核心工作流` 现有结构自洽衔接（放在 P5 / 扩展相关处），不移动 / 破坏既有小节，不与已有版本 / 里程碑段冲突。
  - 验证（auto·可靠）：读 HUMAN_GUIDE 确认新小节位置合理、既有小节未移位。

## 真 dogfood（G3）

- **AC5**：按部署项目的**外部调用形态**真跑一遍闭环——用样例 manifest → 起 `bridge.js`（`--no-open --port <p> --out <results>`，模拟 `$BUTLER/tools/...` 被外部调用）→ 程序化提交四态 payload → 桥进程 **exit 0** 自退 → 读 `results.json` 解析四态 → 按四态路由表演示 `pass/fail/defer/skip` 分派。
  - 验证（auto·可靠）：实际执行，断言退出码 0、`results.json` 落盘且四态齐全可解析、路由分派与协议表一致；证据入 `VERIFY_REPORT`。
- **AC6**：dogfood 覆盖**四态齐全**的样例（至少各一项 pass/fail/defer/skip），证明"人无论选哪个 butler 都能续跑"在真跑中成立（非仅规则正文断言）。
  - 验证（auto·可靠）：results.json 的 `summary` 四态计数均 ≥1、每项 state 合法。

## 样例固化 + 注册（G4）

- **AC7**：dogfood 样例 manifest 固化为工具自带 fixture（落 `tools/delivery-selftest/sample/`，Q1 待定则以 P3 结论为准），可被使用文档 / README 直接引为示例；`tools/delivery-selftest/README.md` 补一句"外部项目调用样例"指引指向它。
  - 验证（auto·可靠）：确认 fixture 存在且为合法 manifest（能被 bridge 解析，AC5 已跑过）、README 有指引。
- **AC8**：新增 / 改动的文档若影响 `Coder/README.md` 的读序或文件说明，按"无隐式依赖"约束登记（mcv-deployment 已注册，本迭代若只在其内部加节则确认无需新登记，并说明）。
  - 验证（auto·可靠）：读 Coder/README 确认 mcv-deployment 描述仍准确、无遗漏新依赖。

## 前滚 + 里程碑收尾（G5）

- **AC9**：`.ai/PROJECT.md` 收口前滚——反映"交付自测桥已可用且外部调用方式已文档化"（现行约束 / 架构图 tools 条按需微调）；`.ai/MILESTONE.md` R5 绑 ITER-0025、收口置 closed + 范围演进记录追加，收口后三路线项全 closed。
  - 验证（auto·可靠）：读 PROJECT / MILESTONE 确认前滚与路线项状态到位；收口自检 5 不变量全绿。

## In / Out Scope

- **In**：部署侧调用文档（mcv-deployment 新节）+ 人类侧使用说明（HUMAN_GUIDE）+ 真 dogfood（外部调用形态跑通四态齐全样例）+ 样例固化 + 前滚 + 里程碑收尾。
- **Out**：**不重新实现**无人异步入账 / 准入闸（已由 R2 `§7.4` 交付，R5 只交叉引用）；不改桥体代码 / 四态机器码 / `human-test-bridge.md` SOP 语义 / hook / 状态机 / 四件套脊柱；不做多人 / 远程 / 持久看板；不聚合切版（发布节奏 Q3 另议）。

## 风险

- R1：本环境无法真人点浏览器 → dogfood 以 headless 程序化提交证明**机械闭环**（AC5/AC6），真人点选层 R3 已 Playwright 弱档覆盖；文档描述真人操作、dogfood 证机制，二者不冲突，差异如实记 Remaining Risks。
- R2：部署侧文档若把路径发现另写一套会与 §0 分叉 → AC1 强制引用 §0 兜底。
- R3：使用文档面向人写、易滑成 AC 指令腔 → AC3 显式要求人类用户视角措辞。

## Open Questions（P3 定）

- Q1：样例 manifest 落 `tools/delivery-selftest/sample/`（倾向）还是 `docs/`。
- Q2：mcv-deployment 是否把 `tools/` 抽象为通用"butler 驻留工具"类别（倾向，一句话带过 + 举 delivery-selftest）。
- Q3：R5 收口后是否立即聚合切版 v1.7.0（倾向收口后用户拍板）。
