---
状态: ack-frozen
ACK 日期: 2026-07-02
ACK 方式: 危险模式 P2 自审门 self-ACK（非用户显式 ACK）
迭代: ITER-0023
里程碑: MILE-0002 R3
---

# AC_LIST — ITER-0023

> ⚠️ 危险模式：本 AC 清单未经用户显式 ACK，由 P2 自审门（对照 `acceptance-schema.md`）自主冻结；自审结论见 `RUN_LOG.md` ITER-0023 · P2-self-ack。
> 说明：本迭代是真代码，验证多为**真跑**（node 断言 / 子进程 / Playwright），故置信档不再全 `可靠`——AC8 为 `auto·弱`（浏览器代理验证），正好 dogfood R2 分级置信。

## 桥本体（G1）

- **AC1**：`bridge.js` 读 manifest JSON、在 `127.0.0.1` 起 HTTP 服务，`GET /` 返回 200 + 渲染 HTML；HTML 含 manifest 每个 item 的 id / 标题 / 每条分步步骤 / 预期结果。
  - 验证（auto·可靠）：起服务（`--no-open --port 0`）+ `http` 客户端 GET，断言状态码 200 且 body 含各 item 文本。
- **AC2**：渲染为 **GitHub 风格分步流程页**——含 sticky 进度条、分步流程卡（编号步骤）、四态按钮、备注框、提交栏（结构保真 `docs/research/MILE-0002-R2-manual-test-bridge-sample.html`）。
  - 验证（auto·可靠）：断言渲染 HTML 含 `statusbar` / `steps` / `verdicts` / `note` / `submitBtn` 等结构标记。

## 四态回传 + 自退（G2）

- **AC3**：每项四态 `pass / fail / skip / defer`（通过 / 未通过 / 跳过 / 延后处理）+ 备注；全判定后可提交，`POST /submit` 写 `results.json`，内容含 `results[]`（每项 id / state / note）+ `summary`（四态计数）。
  - 验证（auto·可靠）：POST 模拟四态 payload，断言 `results.json` 落盘且 results / summary 正确。
- **AC4**：提交后**进程自退**——写完 results、响应 200 后 `process.exit(0)`，服务关闭、端口释放。
  - 验证（auto·可靠）：`spawn` 子进程，POST 后断言子进程 exit code 0。

## 输入 / 输出契约（G3）

- **AC5**：契约成文——工具 `README.md` 定义 manifest 输入 schema（`title / project / iteration / items:[{id,title,steps[],expected}]`）+ results 输出 schema（`iteration / results:[{id,state,note}] / summary`）+ **四态→路由语义**（通过=计入收口 / 未通过=进纠错 / 跳过=N/A / 延后处理=入账不阻塞）。`example/manifest.json` 符合 schema 且能被桥成功渲染。
  - 验证（auto·可靠）：读 README 确认两 schema + 路由表；对 `example/manifest.json` 跑渲染无异常。

## 零依赖 + 自测（G4）

- **AC6**：**零三方依赖**——源码仅 `require` Node 内建（`http` / `fs` / `path` / `child_process` / `url` 等）；无第三方 import、无 `node_modules` 依赖。
  - 验证（auto·可靠）：grep 全部 `require(...)` 确认仅内建；无 `package.json` dependencies 或为空。
- **AC7**：**自测套件**——`test/bridge.test.js` 用 Node 内建跑端到端（起服务 → GET → POST → 断言 results.json → 断言自退），`node test/bridge.test.js` 退出码 0。
  - 验证（auto·可靠）：实际运行测试，断言 exit 0 + 打印全过。
- **AC8**：**浏览器交互实测（代理验证）**——真浏览器打开桥页、逐项点四态、填一条备注、点提交，页面出现"已提交"面板且 `results.json` 落盘。
  - 验证（auto·弱）：Playwright 驱动真浏览器交互 + 截图（代理验证，见 `testing-strategy §3.1`；置信弱于确定性断言、不冒充可靠）。

## 接线注册（G5）

- **AC9**：`tools/` 顶层目录注册进仓库根 `CLAUDE.md` 目录职责；工具自带 `README.md`；`.ai/PROJECT.md` 收口前滚（新增 tools/ 与桥工具入架构图 / 现行约束）。
  - 验证（auto·可靠）：读 `CLAUDE.md` / 工具 README / PROJECT 确认注册与前滚。

## In / Out Scope

- **In**：桥本体（服务 + 渲染 + 四态 + 自退）+ 输入 / 输出契约 + 零依赖 + 自测（node + Playwright）+ tools/ 注册。
- **Out**：**不接** P5 / correction-contract / 等待-回收-续跑（R4）；**不写**部署文档 / 真实 dogfood 跑通（R5）；不做多人 / 远程 / 持久看板；不改 Coder 规则正文 / 状态机 / 四件套脊柱 / hook。

## 风险

- R1：浏览器自动化环境（Playwright）不可用 → AC8 弱档验证降级：如实标注"未执行"落 Remaining Risks，不冒称已测（承 R2 红线）；AC1-AC7 可靠档不受影响仍覆盖核心。
- R2：`process.exit` 自退时机与响应刷新竞态 → 响应 end 后延迟再 exit，测试断言 exit code 兜底。
- R3：跨平台开浏览器（open / xdg-open / start）差异 → best-effort 且 `--no-open` 可关，不阻塞核心逻辑与测试。
