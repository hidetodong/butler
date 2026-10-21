<!-- butler-artifact-template: 1.0.0 artifact=concept -->
# CONCEPT — ITER-0122 · usage 采集：CLI 入口记下最后调用时间

> 分流: 完整 | 命中升级信号: 多文件改动、契约变更、跨模块影响、设计取舍 | 2026-09-14

## Current Understanding

- **R11 只做采集**。每个 CLI 入口把「最后一次被调用的时间」写到项目本地。90 天报告和 A/B/C/D 分档是 R12，本轮不做。没有这份时间戳，后面的淘汰判断还是靠回忆。
- **落点**：项目根 `.ai/.usage.json`。跟拦截日志同类：本机数据、进 gitignore、不进共享仓。不写家目录，不写 butler 仓一份全局账。
- **记什么**：只要 ISO-UTC 时间戳。不记次数、参数、路径、用户。同一入口再次调用就覆盖 `last_used`。
- **谁算入口**：封闭名单。`workflow:<id>` 来自 `workflows/registry.json` 的 12 个工作流加 `router`；`tool:<目录名>` 来自产品驻留工具（见 Scope）。调用方不能随口造 id，未知 id 拒绝写入。
- **怎么打点**：Python CLI 的 `main` 开头机械调用，测试能证明跑过命令就有时间戳。工作流是 markdown 薄壳，没有进程钩——薄壳加一条调用 `tools/usage/usage.py record`，不能宣称 slash 命令会自动记到。
- **失败策略**：采集失败 fail-open。打点出错不得改变原命令退出码，也不能挡住正经工作。
- **不算本轮 CLI**：vendored 的 `tools/codex-validators/`、一次性 dogfood（`explore-dogfood` / `mile0009-e2e`）、Node 的 `delivery-selftest`。hook 放行/拦截不走这份文件（R10 已经有拦截日志）。

## Scope

- 新建 `tools/usage/`：`record` / 只读查询、schema、测试。
- `.gitignore` 加 `.ai/.usage.json`。
- 产品驻留工具 CLI 在 `main` 打点：artifact-pipeline、butler-upgrade、context-budget、decision-map、decision-promotion、decision-work、domain-contract、goal-assurance、handoff、intake、iteration-intake、prd-migrate、prd-status、prd-update、project-config、state-ledger、verification-evidence、workspace-scope，以及 usage 自己。
- 工作流薄壳（Claude 命令 / Codex skill）写明调用 `usage.py record workflow:<id>`；router 用 `workflow:router`。
- 入口名单可从 registry + 上述工具目录派生，有测试锁住集合，避免漏接新工具却没人知道。
- `debt.md`「运行时观测缺位」改成采集已落地、报告仍归 R12。

## Open Questions / Risks

- **~~vendored / dogfood / Node 打不打点~~（已定）**：不算。只打产品驻留 Python CLI + 工作流 record 入口。
- **风险 · 工作流打点靠薄壳自觉**：没有宿主钩。本轮机械保证只覆盖 Python CLI；工作流是「薄壳有这一步 + CLI 能记」，不声称每次 `/butler:inbox` 都已经记到。
- **风险 · 采集写盘失败**：必须 fail-open，测试要注入写失败并断言原命令仍按原退出码返回。
- **风险 · 项目根解析失败**：没有 `.ai/` 的目录不该硬建 usage 文件；解析不到项目根就静默跳过。
