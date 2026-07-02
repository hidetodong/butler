# 「交付自测」桥工具：Node 零依赖人测回传桥（JSON → 分步流程页 → 四态回传 → 自退）

> ITER-0023 · 迭代交付（小版本）· 收口 2026-07-02 · MILE-0002 R3 · ⚠️ 危险模式（P2/P3 自审门 self-ACK，P4 自治 + P5 独立复核）

## 本次交付目标

- MILE-0002 第三个路线项 R3（扁平原子）。承 R1（分道）R2（置信）——它们定"哪些要人测、多大把握"，R3 造"人测完怎么把结论传回"的物理通道。
- 缺口：R1/R2 把人测残余结构化了，但**结论断在人这侧、butler 收不回**。
- 目标：造只驻留 butler 仓的 Node 零依赖桥——外部项目传 manifest JSON → 渲染 GitHub 风格分步流程页 + 起本地服务 + 开浏览器 → 人对每项四态（通过/未通过/跳过/延后处理）+ 备注 → 提交写 `results.json` + 进程自退；定输入/输出契约。

## 已完成内容

- 新增 `tools/`（butler 驻留可执行工具的家，非规则、非部署模板）+ `tools/delivery-selftest/`：
  - `render.js`：`render(manifest)→HTML` 纯函数（GitHub 风格：sticky 进度条 / 编号分步卡 / 四态按钮 / 备注框 / 提交栏），客户端用 DOM + `textContent` 构建（防注入）、`safeJson` 内联数据（转义 `<`、U+2028/2029）。
  - `bridge.js`：CLI + `http` 服务（`GET /`·`/health`·`/favicon.ico`·`POST /submit`）+ 开浏览器（best-effort 跨平台）+ 写 `results.json` + `process.exit(0)` 自退；导出 `createBridge`（`exitOnSubmit` 可关，供测试进程内驱动）。
  - `README.md`：manifest / results 两 schema + 四态→路由语义表 + R4/R5 边界；`example/manifest.json` 示例；`test/bridge.test.js` node 内建端到端。
  - `package.json`：零依赖标识（dependencies 空）。
- 四态机器码 ASCII（pass/fail/skip/defer）+ 中文展示，利于 R4 稳健路由。
- 接线：仓库根 `CLAUDE.md` 目录职责注册 `tools/`。

## 关键变更 / 用户可感知变化

- 人测有了**回传通道**：AI 把人测残余写成 manifest JSON → 桥弹 GitHub 风格页让人勾四态 → 结论落 `results.json`、进程自退（后台进程退出即触发 R4 续跑）。
- 四态齐全（通过/未通过/跳过/延后处理），人无论选哪个 butler 都能续跑；「延后处理」= "记账不阻塞"的人工版（对应 R2 dangerous §7.4 的无人版）。
- **零三方依赖**：只用 Node 内建，双击即用、无需 `npm install`；butler 驻留、不拷进目标项目（外部传 JSON 路径调用）。
- 本工具是真代码，验证真跑：node 自测 8/8 + Playwright 真浏览器端到端 + 进程 exit 0——比规则正文验证更硬。

## 高层影响范围

- 新增：`tools/delivery-selftest/`（render.js / bridge.js / README.md / package.json / example/manifest.json / test/bridge.test.js）。
- 改（接线）：仓库根 `CLAUDE.md`（目录职责）、`.ai/PROJECT.md`（收口前滚）。
- 没碰：Coder 规则正文、hook、四件套 schema、桥的下游接线（R4）、部署 / dogfood（R5）。

## 验证方式与结果摘要

- 9 条 AC 全部满足（逐项见 VERIFY_REPORT）。置信分布 **8 `auto·可靠` + 1 `auto·弱`**（AC8 浏览器代理验证）——首次出现真 `弱` 档，dogfood R2 分级置信。
- `node test/bridge.test.js`：**8 checks ALL PASS、exit 0**（render 单测 / GET / health / 404 / POST 写 results / summary / 非法 state→null / 真进程自退 / example 渲染）。
- **Playwright 真浏览器端到端**：打开桥页 → 点四态（通过/延后/跳过）→ 提交 → done 面板 + `results.json` 落盘（state + summary 正确）+ 后台服务进程 **exit 0** 自退（回环打通）。
- **危险模式 P5 §7.3 独立复核**：fresh-context 子 agent 实读代码 + 实跑测试 + 对抗探测（XSS / 畸形 payload / 超大 body / 写失败 / 自退竞态）。结论：**9/9 confirm、0 Must Fix、0 Should Fix、3 Nit**（缺 id 脏结果 + README 四态顺序已就地修，便民端点保留）。

## 已知剩余风险 / 延后事项

- AC8 弱档：浏览器代理验证强于静态断言、弱于确定性单测；已如实标弱、不冒充可靠。截图会话内、未入库（Playwright 产物不提交）。
- 跨平台开浏览器 best-effort，仅 macOS 实测；失败不影响服务与 `--no-open` 路径。
- 下游消费（四态路由 + 后台等待续跑）留 R4；部署 / 真实 dogfood 留 R5。本迭代只到"能起、能测、能回传、能自退"。

## 引用

- 归档四件套 + 切片：`.ai/iterations/ITER-0023/CONCEPT.md` / `AC_LIST.md` / `TECH_PLAN.md` / `VERIFY_REPORT.md` / `CHANGELOG.md`
- 工具：`tools/delivery-selftest/`（`bridge.js` / `render.js` / `README.md` 契约 / `example/manifest.json` / `test/bridge.test.js`）
- 渲染保真参照：`docs/research/MILE-0002-R2-manual-test-bridge-sample.html`（预研样例）
- 接线：仓库根 `CLAUDE.md`；前滚：`.ai/PROJECT.md`
- 危险模式审计：`.ai/RUN_LOG.md`（ITER-0023 段）
