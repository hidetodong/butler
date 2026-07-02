# CONCEPT — ITER-0025

> 分流: 完整 | 命中升级信号: 跨模块接线、涉及外部调用契约 | 2026-07-02 | MILE-0002 R5

## 一句话

给 MILE-0002 的人测桥补上"外面怎么用"这最后一块：部署项目的 AI 怎么定位并调用 butler 驻留桥、人怎么看懂弹出来的页面，再拿一个真样例把「manifest → 桥 → 四态 → 回填」端到端跑通一遍。前四个路线项把桥和 SOP 协议都造好了，但部署 / 使用文档是空的、也从没真跑过一遍，R5 收这个尾，收完 MILE-0002 全 closed。

## 背景与判断

- 里程碑归属：MILE-0002 收尾路线项 **R5**（扁平原子）。R1~R4 已收口：分道 / 置信 / 桥体 / 等待-回收-续跑 SOP 协议都齐了。
- **实测空缺**：grep 确认 `mcv-deployment.md` 与 `HUMAN_GUIDE.md` 对桥 / 驻留工具 / 人测**零引用**——部署项目的 AI 无从知道"butler 驻留工具怎么调、路径怎么解析"，人类用户也不知道那个弹出来的页面是什么、该怎么点。
- **scope 对账（防重复）**：R5 路线项原列"长程 / 无人的残余异步入账 + 准入闸落地"——该项**已由 R2 的 `dangerous-engine §7.4` 交付**（叶子残余异步入账 / 卡下游不硬闯 / 绝不假绿）。故 R5 对这条**只做交叉引用**（让部署 / 使用文档指向 §7.4 的无人岔口），**不重新实现**。
- 本迭代主体是文档接线（部署侧 + 人类侧）+ 一次真 dogfood；不动桥体代码、不动 SOP 语义。

## 目标（Goal）

- G1：**部署侧文档**——`mcv-deployment.md` 新增"butler 驻留工具调用"一节：驻留工具类别（不拷进目标项目、传参调用）+ 桥的具体调用形态（复用 §0 的 `$BUTLER` 路径发现 → `node $BUTLER/tools/delivery-selftest/bridge.js <manifest> --out ...`）+ manifest/results 落点（本项目 `.ai/human-test/`，建议 gitignore）+ 指向无人岔口 `§7.4`。
- G2：**人类侧文档**——`HUMAN_GUIDE.md` 新增人测桥使用说明：P5 出现机器测不了的残余时会弹一个浏览器分步流程页，你对每项点四态（通过 / 未通过 / 跳过 / 延后处理）+ 备注，提交即续跑；四态各自的下游含义一句话带过。
- G3：**真 dogfood**——拿一个贴近真实的样例 manifest，按部署项目的**外部调用形态**把回路跑通：manifest → 起桥（`--no-open` headless）→ 程序化提交四态 → 写 `results.json` → 读回演示四态路由，留跑通证据入 `VERIFY_REPORT`，证明"外部怎么用"文档写的路子真能走通。
- G4：**样例固化 + 注册**——dogfood 样例 manifest 固化为工具自带 fixture（可被 README / 使用文档直接引为示例）；新增节按需登记进 `Coder/README.md` 读序 / 描述；`tools/delivery-selftest/README.md` 补一句"外部项目调用样例"指引。
- G5：**收口前滚 + 里程碑收尾**——`.ai/PROJECT.md` 前滚（桥可用 + 调用方式已文档化）；R5 收口后 `.ai/MILESTONE.md` 三路线项全 closed，MILE-0002 方向达成、可聚合发布（发布节奏另议）。

## 约束（Constraints）

- **桥不拷进目标项目**（MILE-0002 硬约束）：文档必须写成"传 manifest 路径调用 butler 仓的 `bridge.js`"，不能写成"复制到项目里"；不引三方依赖。
- **路径解析复用现有机制**：桥调用直接引用 `mcv-deployment §0` 的 `$BUTLER` 发现结果，不另造一套发现逻辑。
- **单一来源纪律**：桥体输入 / 输出契约真源 = `tools/delivery-selftest/README.md`；SOP 下游语义真源 = `human-test-bridge.md`；无人岔口真源 = `dangerous-engine §7.4`。R5 文档只**引用**、不重抄字段 / 不重定义语义。
- **dogfood 环境限制**：本环境无法真人点浏览器，端到端以 headless（`--no-open` + 程序化提交四态）证明机械闭环；真人点选层 R3 已 Playwright 覆盖为弱档，R5 不重造。
- 文件名互引（不写脆弱行号，§引用仅用于跨文件指章节名）；符合本仓写作约定。
- 只做文档 + dogfood；**不改**桥体代码、SOP 语义、§7.4 判据、四件套 schema、hook、状态机、根 CHANGELOG / VERSION。

## 影响范围（Impact Scope）

- 改：`Coder/20_Workflow_Lifecycle/mcv-deployment.md`（新增驻留工具调用节）、`HUMAN_GUIDE.md`（新增人测桥使用说明）。
- 可能改：`Coder/README.md`（登记新节 / 描述）、`tools/delivery-selftest/README.md`（补外部调用样例指引）。
- 新增：dogfood 样例 manifest（工具自带 fixture）；端到端跑通证据入 `VERIFY_REPORT`。
- 里程碑：`.ai/MILESTONE.md` R5 绑号 + 收口后全 closed。
- **不影响**：桥体代码（`bridge.js` / `render.js` 逻辑不动）、`human-test-bridge.md` SOP 语义、`dangerous-engine §7.4`（只被引用）、四件套 schema、hook 体系、P1-P5 状态机、根 CHANGELOG / VERSION。

## 项目类型与 Profiles

- butler 规则仓（编辑规则本身）+ 一次 Node 驻留工具真 dogfood。
- 无 stack profile 强制启用；dogfood 触及 Node（零依赖，沿用 R3 自测口径）。验证遵循 R1 自动化优先——闭环用真跑证明（`auto·可靠`），不停在"文档写了就算"。

## 待澄清（Open Questions）

- Q1：dogfood 样例 manifest 放哪——`tools/delivery-selftest/sample/`（跟工具走、README 可直接引为示例）还是 `docs/`？倾向前者。（P3 定）
- Q2：`mcv-deployment` 驻留工具节，是否把 `tools/` 提升为通用"butler 驻留工具"类别（为将来其他驻留工具留位）还是只窄写 delivery-selftest 一个？倾向前者（一句话带类别 + 具体举 delivery-selftest）。（P3 定）
- Q3：R5 收口后是否立即聚合切版 MILE-0002（v1.7.0）？倾向收口后由用户拍板发布节奏（承 R4 收口口径：只提交、发布另议）。（P3 定）
