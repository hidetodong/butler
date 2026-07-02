# CONCEPT — ITER-0023

> 分流：完整路径 | 命中升级信号：新增可执行工具（真代码）、跨模块契约（输入 / 输出 JSON）、多文件、关键路径（R4/R5 依赖其契约） | 2026-07-02 | MILE-0002 R3 | ⚠️ 危险模式（P4 起自治；P2/P3 自审门自 ACK）

## 一句话

R1/R2 把"人测残余"结构化并定了置信档，但残余的**回传通道**仍缺——人测完，结论断在人这侧、butler 收不回。R3 造「交付自测」桥：一个**只驻留 butler 仓**的 Node 零依赖工具，外部项目**传一份 JSON 清单** → 桥渲染 GitHub 风格分步流程页、本地起服务、开浏览器 → 人对每项选**四态**（通过 / 未通过 / 跳过 / 延后处理）+ 备注 → 提交后写 `results.json`、**进程自退** → 为 R4 的"等待-回收-续跑"接线铺好契约与产物。

## 背景与判断

- 里程碑归属：MILE-0002 路线项 **R3**。承 R1（分道）R2（置信）——它们定"哪些要人测、多大把握"，R3 造"人测完怎么把结论传回"的物理通道。
- 关键设计（用户已定，见 `MILESTONE.md` 关键设计 + 样例 `docs/research/MILE-0002-R2-manual-test-bridge-sample.html`）：butler 驻留（不拷进目标项目，外部传 JSON 调用）、Node 零三方依赖、GitHub 风格、分步流程页、每项四态 + 备注、提交自退。
- 本迭代**只造桥 + 定契约**；把桥接进 P5 / correction-contract / 外部调用方式 = R4；部署文档 + dogfood = R5。
- 与 R2 无人残余处置互补：R2 是 `/dangerous` **无人**场景（异步入账）；R3 是**有人**场景（弹页面回传）。四态里「延后处理」正是"记账不阻塞"的人工版。

## 目标（Goal）

- G1：**桥本体**——Node 零依赖工具，读 manifest JSON → 起本地 HTTP 服务 → 渲染分步流程页（GitHub 风格，保真样例）→ 开浏览器。
- G2：**四态回传 + 自退**——每项四态（pass / fail / skip / defer）+ 备注；提交 POST → 写 `results.json`（含 summary）→ 响应后 `process.exit(0)`（后台进程退出即触发 R4 续跑）。
- G3：**输入 / 输出契约**——manifest 输入 schema（`{title, project, iteration, items:[{id,title,steps[],expected}]}`）与 results 输出 schema（`{iteration, results:[{id,state,note}], summary}`）成文，四态→路由语义（通过=收口 / 未通过=纠错 / 跳过=N/A / 延后=入账不阻塞）写清。
- G4：**真测**——node 内建断言测服务与契约（可靠档）+ Playwright 浏览器交互测真 UI（代理验证·弱档），dogfood R2 分级置信。
- G5：**接线注册**——新增 `tools/` 顶层目录，注册进仓库 `CLAUDE.md` 目录职责 + 工具自带 README；PROJECT 收口前滚。

## 约束（Constraints）

- **零三方依赖**：只用 Node 内建（`http` / `fs` / `path` / `child_process`）；不引 express / 测试框架。
- **butler 驻留**：工具存 butler 仓、不拷进目标项目；目标项目通过传 manifest JSON 路径调用。
- **单机单次握手**：不做多人 / 远程 / 持久看板。
- 只造桥、定契约、自测；**不接** P5 / correction-contract / 续跑（R4）、**不写**部署文档 / dogfood（R5）。
- 不改 P1-P5 状态机、四件套脊柱、hook。

## 影响范围（Impact Scope）

- 新增：`tools/delivery-selftest/`（`bridge.js` 服务 + 自退、`render.js` 渲染、`README.md` 契约、`example/manifest.json`、`test/bridge.test.js`）。
- 改（接线）：仓库根 `CLAUDE.md`（目录职责加 `tools/`）、`.ai/PROJECT.md`（前滚）。
- 不影响：Coder 规则正文（R3 是工具不是规则）、hook、四件套 schema、桥的下游接线（R4）。

## 项目类型与 Profiles

butler 仓内首次引入**可执行 Node 工具**（非规则正文）。无既有 JS profile 落盘，按通用 SOP + Node 零依赖约束推进；测试遵循 R1 自动化优先（能自动必自动，UI 用浏览器自动化）。

## 待澄清（Open Questions）

- Q1：工具落点 `tools/delivery-selftest/` vs `templates/`？倾向 `tools/`——它是 butler 驻留可执行工具、非部署模板（`templates/` 是拷给项目的）。（P3 定）
- Q2：四态机器码用 ASCII（pass/fail/skip/defer）还是中文（样例里的中文）？倾向 ASCII 码 + 中文展示——利于 R4 机器路由稳健。（P3 定）
- Q3：渲染单文件内联 vs 拆 render.js？倾向拆 `render.js`（纯函数、可单测），`bridge.js` 管服务 / IO。（P3 定）
- Q4：results.json 落点默认 = manifest 同目录 `results.json`，可 `--out` 覆写。（P3 定）
