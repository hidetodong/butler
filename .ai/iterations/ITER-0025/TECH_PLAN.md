# TECH_PLAN — ITER-0025

> P3 经**用户显式 ACK**（2026-07-02）。ACK 后用户开启 **/dangerous 危险模式**，P4→P5→收口由模型无人值守自治推进（§7.2 回滚锚点 + §7.3 P5 升格完整审查 + §7.1 审计披露）。R5 = MILE-0002 收尾：部署侧调用文档 + 人类侧使用说明 + 真样例 dogfood。

# Goal

- 支撑 AC1-AC9：给交付自测桥补"外面怎么用"——`mcv-deployment.md` 新增 butler 驻留工具调用节（AC1/AC2）、`HUMAN_GUIDE.md` 新增人测桥使用说明（AC3/AC4）、按外部调用形态真 dogfood 四态齐全回路（AC5/AC6）、样例固化为工具 fixture + README 指引（AC7）、注册确认（AC8）、收口前滚 + 里程碑收尾（AC9）。

# Files / Modules to Change

- `Coder/20_Workflow_Lifecycle/mcv-deployment.md` — 新增 §6「butler 驻留工具调用」（部署项目如何定位 + 调用桥），承接 §0 路径发现。
- `HUMAN_GUIDE.md` — §5 扩展模式区新增「人测回环（交付自测桥）」小节，人类用户视角。
- `tools/delivery-selftest/sample/manifest.sample.json` — 新增 dogfood 样例 fixture（四态齐全示例）。
- `tools/delivery-selftest/README.md` — 「用法」后补一句"外部项目调用样例"指引，指向 sample。
- `Coder/README.md` — 确认 mcv-deployment 描述仍准（§6 内嵌，无新文件依赖，按需微调描述）。
- `.ai/PROJECT.md` — 收口前滚（tools 条 + 现行约束反映"桥可用且调用方式已文档化"）。
- `.ai/MILESTONE.md` / `.ai/ITERATIONS.md` — 收口时台账翻转（原子仪式步③）。

# Interface / Contract

- **桥调用形态（对外契约，文档化不新造）**：`node $BUTLER/tools/delivery-selftest/bridge.js <manifest> [--out <results>] [--port N] [--no-open]`；输入/输出 JSON schema 与四态机器码以 `tools/delivery-selftest/README.md` 为真源，本迭代文档只引用。
- **路径解析**：复用 `mcv-deployment §0` 的 `$BUTLER` 发现结果（`$BUTLER_PATH` → 全局 CLAUDE.md → 询问），不另造。
- **落点约定**：目标项目 manifest/results 落本项目 `.ai/human-test/`（建议 gitignore），与四件套隔离——与 `human-test-bridge.md §3` 一致。

# State / Boundary

- 只加文档 + 样例 fixture + 一次 dogfood；**不改** `bridge.js`/`render.js` 代码、四态机器码、`human-test-bridge.md` SOP 语义、`dangerous-engine §7.4` 判据、四件套 schema、hook、P1-P5 状态机、根 CHANGELOG/VERSION。
- §7.4（无人异步入账 + 准入闸）R2 已交付——本迭代只**交叉引用**，不在 mcv-deployment/HUMAN_GUIDE 里重定义无人语义。
- dogfood 运行产物走临时路径（`/tmp` 或工作树临时目录），不入库；固化的 sample manifest 入库、results 不入库。

# Design Decisions

- **DD1 mcv-deployment 新增 §6 而非塞进 §5 Hook（AC1）**：驻留工具调用与 hook 注入是两件事（hook 拷进目标项目、驻留工具反之不拷）。独立成 §6「butler 驻留工具调用」更清晰，且为将来其他驻留工具留位。
- **DD2 `tools/` 抽象为通用"butler 驻留工具"类别（Q2 定：采纳）**：§6 开头一句话定义类别（存 butler 仓、不拷进目标项目、目标项目传参调用、与 hook 副本相反），再具体举 delivery-selftest 桥的调用形态。轻量抽象，不过度工程。
- **DD3 单一来源纪律（AC2）**：§6 不重抄 manifest/results 字段与四态码，只引用 `tools/delivery-selftest/README.md`（契约）+ `human-test-bridge.md`（下游语义）+ `dangerous-engine §7.4`（无人岔口）。三处文件名互引。
- **DD4 HUMAN_GUIDE 落 §5 扩展区（AC3/AC4）**：人测桥是 P5 收口时按需触发的能力，与扩展模式（review/dangerous 等可选能力）同类，放 §5 末尾新小节；不动 §2 核心工作流表、不移既有节。措辞用"你会看到一个浏览器页面…点四态…提交后 AI 继续"，人类视角、非指令腔。
- **DD5 样例 fixture 落 `tools/delivery-selftest/sample/`（Q1 定：采纳）**：跟工具走，README 与使用文档可直接引为示例，dogfood 与"使用样例"复用同一份。fixture 覆盖四态齐全（4 项，各一态）以同时满足 AC6。
- **DD6 dogfood = 外部调用形态的机械闭环（AC5/AC6）**：模拟部署项目调用——起 `bridge.js sample/manifest.sample.json --no-open --port 0 --out <tmp>/results.json`（`run_in_background`）→ 解析监听端口 → 程序化 POST `/submit` 四态 payload → 断言桥 exit 0 自退 → 读 results.json 断言 summary 四态各≥1 → 按路由表打印 pass/fail/defer/skip 分派。真人点选层 R3 Playwright 已弱档覆盖，不重造；差异记 Remaining Risks。
- **DD7 Coder/README 按需微调（AC8）**：mcv-deployment 已注册，本迭代只在其内部加 §6，不新增文件、不改读序 → 确认描述仍准即可，若 README 有"驻留工具"可提及处顺手补一句，避免隐式依赖。
- **DD8 发布节奏延后（Q3 定）**：R5 收口只做原子仪式 + 提交，**不聚合切版**；MILE-0002 三路线项全 closed 后由用户拍板 v1.7.0 发布节奏（承 R4 口径）。

# Execution Steps

- [ ] T1（AC5/AC6/AC7）：写 `tools/delivery-selftest/sample/manifest.sample.json`（四态齐全 4 项，贴近真实 P5 残余）→ 先落样例，dogfood 与文档共用。
- [ ] T2（AC5/AC6）：真 dogfood——`run_in_background` 起 `bridge.js sample --no-open --port 0 --out /tmp/...results.json` → 程序化 POST 四态 → 断言 exit 0 + results summary 四态各≥1 + 路由分派一致；证据留待回填 VERIFY。
- [ ] T3（AC1/AC2）：`mcv-deployment.md` 新增 §6「butler 驻留工具调用」（类别定义 + 桥调用形态 + `.ai/human-test/` 落点 + 引用三处真源 + 无人岔口指 §7.4）。
- [ ] T4（AC3/AC4）：`HUMAN_GUIDE.md` §5 新增「人测回环（交付自测桥）」小节（何时弹页面 / 点四态+备注 / 提交即续跑 / 四态含义），位置自洽不移既有节。
- [ ] T5（AC7）：`tools/delivery-selftest/README.md` 补"外部项目调用样例"指引指向 sample。
- [ ] T6（AC8）：读 `Coder/README.md` 确认 mcv-deployment 描述仍准、无遗漏依赖（按需补"驻留工具"一句）。
- [ ] T7（AC9）：原子收口五步——归档四件套+changelog切片 / 交付 md+html / 台账翻转+收编 01_CHANGELOG / PROJECT 前滚 / 收口自检 5 不变量；MILESTONE R5→closed + 范围演进。

# Verification Plan

- AC1/AC2：读 mcv-deployment §6 确认三点齐全、不拷副本口径、引用真源无重抄、含无人岔口。
- AC3/AC4：读 HUMAN_GUIDE 新小节确认覆盖四要点、人类视角、既有节未移位。
- AC5/AC6：实跑 dogfood，断言退出码 0、results.json 四态齐全可解析、路由分派与协议表一致；证据（命令 + 输出摘要）入 VERIFY_REPORT。
- AC7：确认 sample manifest 存在、为合法 manifest（dogfood 已解析过）、README 有指引。
- AC8：读 Coder/README 确认描述准确。
- AC9：读 PROJECT/MILESTONE 确认前滚 + 路线项状态；收口自检 5 不变量全绿。

# Risks / Open Questions

- R1（环境）：本环境无真人浏览器点选 → dogfood 以 headless 程序化提交证机械闭环；真人层 R3 Playwright 弱档覆盖。差异记 VERIFY Remaining Risks。
- R2（一致性）：§6 路径发现须引用 §0 不分叉——T3 强制引用兜底。
- R3（措辞）：HUMAN_GUIDE 易滑成指令腔 → T4 显式人类视角复核。
- 回滚锚点：本轮 iteration-open（已落台账/四件套 draft）为基线；P4 文档+dogfood 叠其上，`git reset` + 清未跟踪即回退。标准模式无危险模式回滚锚点提交要求。
