# delivery-selftest — 交付自测桥

butler 驻留的**人测回传桥**：外部项目把"机器测不了、需人判定的残余项"整理成一份 manifest JSON 传给本工具，工具渲染一张 GitHub 风格的**分步流程页**、本地起服务并开浏览器；人对每项选**四态**（通过 / 未通过 / 跳过 / 延后处理）+ 备注，提交后结果写回 `results.json`、**进程自退**。

- **零三方依赖**：只用 Node 内建（`http` / `fs` / `path` / `child_process`）。
- **butler 驻留**：本工具存 butler 仓，**不拷进目标项目**；目标项目通过传 manifest 路径调用。
- **单机单次握手**：不做多人 / 远程 / 持久看板。

> 归属 MILE-0002 R3。本工具只负责"渲染 + 回传 + 自退"；把它接进 P5 / 纠错闭环、后台等待续跑的 SOP 协议已由 **R4** 补全——何时起桥 / 后台等待 / 四态路由见 `Coder/20_Workflow_Lifecycle/human-test-bridge.md`；部署 / 使用文档 / dogfood 是 **R5**。

## 用法

```bash
node bridge.js <manifest.json> [--out results.json] [--port N] [--no-open]
```

- `<manifest.json>`：人测清单（schema 见下）。
- `--out`：结果写出路径，默认 = manifest 同目录 `results.json`。
- `--port`：监听端口，默认 `0`（系统分配空闲端口）。
- `--no-open`：不自动开浏览器（无头 / 测试用）。

提交后工具向 `--out` 写结果、响应浏览器、然后 `process.exit(0)`。调用方（R4）用后台方式起桥并阻塞等待，**进程退出即续跑**。

**外部项目调用样例**：目标项目不拷本工具、按路径调 butler 仓这一份——

```bash
node $BUTLER/tools/delivery-selftest/bridge.js \
  <你的项目>/.ai/human-test/manifest.json \
  --out <你的项目>/.ai/human-test/results.json
```

`example/manifest.json` 是一份可直接跑的四态齐全样例清单（4 项人测残余）；部署 / 使用说明与路径解析见 `Coder/20_Workflow_Lifecycle/mcv-deployment.md §6`，何时起桥 / 怎么等 / 四态怎么续跑见 `Coder/20_Workflow_Lifecycle/human-test-bridge.md`。

## 输入契约（manifest JSON）

```jsonc
{
  "project": "acme-web",        // 可选，展示用
  "iteration": "ITER-0042",     // 可选，展示 + 回填 results
  "phase": "P5 验证 · 人测道残余", // 可选，展示用
  "items": [                     // 必填，非空数组
    {
      "id": "AC3",              // 必填，回传结果的锚点（建议对齐 AC 号）
      "title": "登录页深色模式观感", // 必填，一句话说清测什么
      "steps": ["切深色模式", "刷新首页", "看品牌色对比度"], // 步骤数组，渲染为分步流程
      "expected": "品牌色不刺眼、对比度舒适"  // 预期结果（也接受 expect）
    }
  ]
}
```

## 输出契约（results JSON）

```jsonc
{
  "project": "acme-web",
  "iteration": "ITER-0042",
  "phase": "P5",
  "submittedAt": "2026-07-02T08:00:00.000Z",
  "results": [
    { "id": "AC3", "state": "pass", "note": null }
  ],
  "summary": { "pass": 1, "fail": 0, "defer": 0, "skip": 0 }
}
```

- `state` 机器码（ASCII）：`pass` / `fail` / `skip` / `defer`；页面展示对应中文「通过 / 未通过 / 跳过 / 延后处理」。
- 非法 / 缺失 state 归 `null`（视为未判定，正常流程中提交按钮要求全判定后才可点）。

## 四态 → 路由语义（R4 `human-test-bridge.md` 消费）

| 状态 | 机器码 | 下游路由 |
|---|---|---|
| 通过 | `pass` | 计入收口（该 AC 人测通过） |
| 未通过 | `fail` | 进纠错闭环（`correction-contract`），备注当线索 |
| 延后处理 | `defer` | 入欠债账、**不阻塞收口**（"记账不阻塞"的人工版，对应 dangerous §7.4 无人版） |
| 跳过 | `skip` | 记 N/A（本次不测，非欠债） |

四态齐全 → 人无论选哪个，butler 都能续跑，闭环成立。

## 自测

```bash
node test/bridge.test.js       # node 内建端到端 + render 单测（零依赖）
```

浏览器交互层（真实点选四态 + 提交）由 Playwright 覆盖，属"代理验证·弱档"（见 `Coder/30_Quality_Gate/testing-strategy.md §3.1`）。
