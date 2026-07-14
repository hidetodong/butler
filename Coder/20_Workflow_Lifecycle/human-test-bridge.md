---
title: 人测桥等待-回收-续跑闭环协议
audience: AI / 开发者
scope: P5 人测道残余的回传闭环——何时起「交付自测」桥、如何后台起桥并阻塞等待、如何读回 results.json 并按四态路由续跑；无人值守场次的降级岔口。仅接线桥的下游消费，桥体契约见 tools/delivery-selftest/README.md
---

# 人测桥等待-回收-续跑闭环协议

## 1. 定位

R1 把验证分了自动道 / 人测道，R2 叠了置信档「可靠 / 弱 / 待人」，R3 造了 butler 驻留的**交付自测桥**（`tools/delivery-selftest/`：manifest JSON → 分步流程页 → 四态回传 → 进程自退）。但桥的**下游一直悬空**——butler 不知道何时该起桥、起完怎么等、结果回来怎么续跑。本协议补上这一环：把桥接进 P5，定义"**等待-回收-续跑**"闭环，让人测结论真正流回 butler、闭环真正合上。

本协议**只管桥的下游消费**（何时起、怎么等、怎么路由）；桥的输入 / 输出字段 schema 以 `tools/delivery-selftest/README.md` 为**契约真源**，本协议引用不重抄（单一来源纪律）。

## 2. 触发条件

同时满足才起桥：

- **P5 存在 `human·待人` 档残余 AC**：即经 R1 分道 + R2 代理验证后仍落人测道（连弱检查都造不出、只能人判定）的项（判据见 `30_Quality_Gate/testing-strategy.md §3 / §3.1`）。无此类残余 → 不起桥，P5 正常收口。
- **有人在场**：当前为有监督场次（人可交互勾选）。`/butler:dangerous` 无人值守场次桥会永久阻塞，**不起桥**，走 §5 降级。

## 3. 等待-回收-续跑闭环（五步）

有人场次、存在人测残余时，P5 按序执行：

1. **生成 manifest**：把 `human·待人` 残余 AC 整理成一份 manifest JSON（`id` 对齐 AC 号，`title` / `steps[]` / `expected` 按 `tools/delivery-selftest/README.md` 输入契约填），落 `.ai/human-test/manifest.json`（与四件套隔离，建议 gitignore）。
2. **后台起桥**：用 harness 后台能力（如 Claude Code 的 `run_in_background`）起 butler 驻留桥——`node <butler>/tools/delivery-selftest/bridge.js .ai/human-test/manifest.json --out .ai/human-test/results.json`，桥自动开浏览器弹分步流程页给人勾选（调用形态见 §6）。
3. **阻塞等待**：桥进程在人提交后写 `results.json`、响应、`process.exit(0)` 自退。butler **阻塞等待该后台进程退出**——进程退出即"人已提交"的信号，harness 后台任务完成即续跑，butler 无需轮询。
4. **读回结果**：桥退出后读 `.ai/human-test/results.json`，解析 `results[]`（每项 `id` / `state` / `note`）+ `summary`。
5. **四态路由回填**：按 §4 把每项 `state` 路由到下游动作，并回填 `VERIFY_REPORT.md`（人测道小结 + AC Status）。

若桥进程异常退出（非人提交导致，如崩溃 / 无 `results.json`）：视为回传失败，**不假绿**——按诚实停交还或重试起桥，绝不臆测人测结论（承 `30_Quality_Gate/correction-contract.md`）。

## 4. 四态路由

桥回传四态，各自映射一个下游动作。本表与 `tools/delivery-selftest/README.md`「四态 → 路由语义」表**逐条一致**（同机器码、同下游语义），此处补 SOP 侧落点：

| 状态 | 机器码 | 下游路由（SOP 侧动作） |
|---|---|---|
| 通过 | `pass` | 该 AC 人测通过 → 回填 `VERIFY_REPORT` 该 AC 满足、**计入收口** |
| 未通过 | `fail` | 进 `30_Quality_Gate/correction-contract.md` 纠错闭环（`note` 当线索）→ 该 AC **不得收口**，修到真过再回 P5 |
| 延后处理 | `defer` | 入欠债账（`VERIFY_REPORT` 的 `Remaining Risks` + `02_SESSION_HANDOFF.md`）→ **不阻塞收口**，标明待人清（"记账不阻塞"的人工版） |
| 跳过 | `skip` | 记 N/A（本次不测、非欠债）→ 回填 `VERIFY_REPORT` 标 N/A |

四态齐全 → 人无论选哪个，butler 都有确定动作、都能续跑，闭环成立。红线：`fail` 不得静默吞、`pass` 不得臆造（无 `results.json` 不算 `pass`）。

## 5. 无人场次降级（与 dangerous 的岔口）

桥是**有人场次**工具：它靠弹页面等人勾选，无人则永久阻塞。`/butler:dangerous` 无人值守下**不起桥**，人测残余改走 `65_Extension_Dangerous/dangerous-engine.md §7.4` 依赖感知准入闸：

- **叶子残余**（不卡下游）→ 异步入账、续跑。
- **卡下游残余** → 弱验证顶 / 砍隔离该分支 / 连弱验证都造不出则该活儿不具无人跑准入资格、写 handoff 留有人场次。
- **红线：绝不假绿**——`待人` 如实记 `VERIFY_REPORT`，不冒充已验。

一句话岔口：**有人 → 起桥走本协议四态路由；无人 → 不起桥走 dangerous §7.4 准入闸。** 两条路互斥、不重叠。

## 6. 调用形态（外部项目如何用）

桥是 butler 驻留工具，**不拷进目标项目**——目标项目的 butler（AI）在 P5 触发时：

- 把本项目的人测残余写成 manifest JSON（落本项目 `.ai/human-test/`）。
- **传 manifest 路径**调用 butler 仓的 `bridge.js`（`--out` 指向本项目 `.ai/human-test/results.json`），不在本项目存桥副本（避免漂移）。
- 后台起桥 + 阻塞等待 + 读回 + 四态路由，同 §3。

> 具体的 butler 仓路径解析（部署项目如何定位 butler 驻留工具）、`mcv-deployment` 部署登记、`HUMAN_GUIDE` 使用说明**留 R5**（部署 / 使用文档 + dogfood）。本协议只定"怎么接、怎么跑"的 SOP 语义，不做部署注册。

## 7. 与其他规则的关系

- **桥体契约真源**：`tools/delivery-selftest/README.md`（manifest / results schema + 四态机器码）——本协议引用不重抄。
- **人测道界定**：`30_Quality_Gate/testing-strategy.md §3 / §3.1`（哪些残余落人测道、先造弱检查）。
- **回填格式**：`20_Workflow_Lifecycle/verify-schema.md`（人测道小结 + `(human·待人)` 标记）。
- **纠错承接**：`30_Quality_Gate/correction-contract.md`（`fail` 进纠错闭环、禁伪造验证）。
- **无人降级**：`65_Extension_Dangerous/dangerous-engine.md §7.4 / §8`（无人不起桥、走准入闸；本协议与其双向一致）。
- **部署 / dogfood**：R5 承接（`mcv-deployment.md` / `HUMAN_GUIDE.md` / 真实样例跑通）。
