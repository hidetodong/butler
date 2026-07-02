# TECH_PLAN — ITER-0023

> ⚠️ 危险模式：本产物由模型自主 ACK（已过 §5.2 P3 设计自审门），未经用户确认（ITER-0023，2026-07-02）。

# Goal

造 MILE-0002 R3「交付自测」桥：Node 零依赖工具，manifest JSON → 渲染 GitHub 风格分步流程页 + 本地服务 + 开浏览器 → 四态 + 备注回传 → 写 `results.json` + 进程自退。定契约、真测（node + Playwright）、注册 `tools/`。

# Design Decisions

- **DD1 落点 `tools/delivery-selftest/`（AC9）**：新增顶层 `tools/`——butler 驻留可执行工具的家，区别于 `templates/`（拷给项目的模板）。桥不拷进目标项目，目标项目传 manifest 路径调用。
- **DD2 模块拆分（AC1/AC2）**：`render.js`（纯函数 `render(manifest)→HTML`，可单测、无 IO）+ `bridge.js`（CLI + HTTP 服务 + 开浏览器 + 写文件 + 自退）。渲染与 IO 解耦。
- **DD3 四态 ASCII 码 + 中文展示（AC3）**：机器码 `pass / fail / skip / defer`（利于 R4 稳健路由），页面展示中文「通过 / 未通过 / 跳过 / 延后处理」。`results.json` 存 ASCII state。
- **DD4 服务与自退（AC1/AC4）**：`http` 内建。路由 `GET /`（HTML）/ `GET /health`（就绪探针，供测试）/ `POST /submit`（收结果）。`/submit`：读 body → 校验 → 写 `results.json` → 响应 200 → 延迟 100ms `server.close(()=>process.exit(0))`（避免响应未刷完即退的竞态）。默认 `--port 0`（临时端口）、`--no-open`（测试用）、`--out`（覆写结果路径，默认 manifest 同目录 `results.json`）。
- **DD5 可测性（AC7/AC8）**：`bridge.js` 导出 `createBridge(manifest, {out, exitOnSubmit, onSubmitted})`——`exitOnSubmit:false` 供测试在进程内起服务、驱动、断言而不自杀进程；CLI `main()` 用 `exitOnSubmit:true`。`render.js` 纯函数直接单测。
- **DD6 安全渲染（AC1/AC2）**：客户端脚本用 DOM API + `textContent` 注入 item 文本（不用 innerHTML 拼用户串），避免注入；manifest 数据用 `JSON.stringify(...).replace(/</g,'\\u003c')` 安全内联进 `<script>`。
- **DD7 零依赖（AC6）**：仅 `require` 内建（`http`/`fs`/`path`/`child_process`/`url`）；无 `package.json` dependencies（如需 `package.json` 仅置 `type`/scripts、依赖为空）。
- **DD8 契约 + 路由语义（AC5）**：README 定 manifest / results 两 schema + 四态路由表（通过=收口 / 未通过=纠错 / 跳过=N/A / 延后=入账不阻塞）。桥本迭代只**产出** results 与自退；**消费**（路由 + 续跑）留 R4。

# Execution Steps

- [ ] T1（AC6/AC1/AC2）：`tools/delivery-selftest/render.js`——`render(manifest)`、`VERDICTS`、`escapeHtml`；GitHub 风格模板（保真样例结构）+ 客户端脚本（DOM/textContent 构建、四态、进度、POST /submit）。
- [ ] T2（AC1/AC3/AC4）：`tools/delivery-selftest/bridge.js`——`parseArgs` / `createBridge` / `openBrowser` / `summarize` / `main`；路由 GET·health·submit、写 results、自退。
- [ ] T3（AC5）：`tools/delivery-selftest/README.md`——用法 + manifest schema + results schema + 四态路由表 + 与 R4/R5 边界。
- [ ] T4（AC5）：`tools/delivery-selftest/example/manifest.json`——示例清单（3 项，覆盖典型人测类目）。
- [ ] T5（AC7）：`tools/delivery-selftest/test/bridge.test.js`——node 内建端到端：createBridge(exitOnSubmit:false) → GET 断言 → POST 断言 results.json/summary → 另 spawn 真进程测 exit 0；render 纯函数断言。
- [ ] T6（AC7）：实际运行 `node test/bridge.test.js`，全过（exit 0）。
- [ ] T7（AC8）：Playwright 起真浏览器打开桥页 → 点四态 + 填备注 + 提交 → 断言 done 面板 + results.json；截图留证（代理验证·弱档）。若环境不可用则如实标未执行、落 Remaining Risks。
- [ ] T8（AC9）：仓库根 `CLAUDE.md` 目录职责加 `tools/`；工具 README 已在 T3。
- [ ] T9：P5 §7.3 独立复核（fresh-context 子 agent，逐 AC）+ 原子收口五步（含 PROJECT 前滚 tools/ + 桥）。

# Impact / Boundary

- 新增：`tools/delivery-selftest/`（render.js / bridge.js / README.md / example/manifest.json / test/bridge.test.js，可选 package.json 零依赖）。
- 改（接线）：仓库根 `CLAUDE.md`、`.ai/PROJECT.md`（收口前滚）。
- 不碰：Coder 规则正文、hook、四件套 schema、桥下游接线（R4）、部署（R5）。
- 回滚：本轮 iteration-open 提交为锚点，P4 新增 tools/ 叠其上，`git reset` + 清未跟踪即回退。
