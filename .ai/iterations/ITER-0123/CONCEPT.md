<!-- butler-artifact-template: 1.0.0 artifact=concept -->
# CONCEPT — ITER-0123 · usage 报告：90 天分档替代手工回忆

> 分流: 完整 | 命中升级信号: 多文件改动、契约变更、跨模块影响、设计取舍 | 2026-09-14

## Current Understanding

- **R12 只出报告**。R11 已经把最后调用时间写在 `.ai/.usage.json`。本轮读这份文件和封闭名单，按 `--since` 窗口把每个入口打成 A/B/C/D。人看完自己决定砍不砍，工具不自动淘汰。
- **四档（只靠 last_used）**：A 窗口内用过；B 用过但早于窗口；C 名单里从未记下；D 文件里有、当前名单没有（退役残留）。没有次数数据，不按频次分档。
- **窗口**：`--since Nd`，N 是正整数天，默认 `90d`。不支持小时/周混写。
- **名单**：复用 `tools/usage` 的 `allowed_ids()`，不另造入口表。本轮新增 `tools/usage-report/`，要登记进产品工具名单并打点，否则 R11 的目录对账会红。
- **输出**：stdout 一份 JSON，含窗口、生成时间、四档数组。每条有 id、档、last_used（没有则 null）。缺文件或坏文件不崩溃：名单里的都算 C，D 为空。

## Scope

- 新建 `tools/usage-report/`：`report --project-root --since`，默认 90d。
- 把 `usage-report` 加进 `PRODUCT_TOOLS` 并在其 `main` 打点。
- 测试锁四档判定、默认窗口、坏文件/缺文件、非法 `--since`。
- CI 接入；OVERVIEW 随 tools/ 重算。
- `debt.md`「运行时观测缺位」在报告落地后删除；真实会话里有没有人看报告，不在本轮证明。

## Open Questions / Risks

- **~~--since 格式~~（已定）**：只接受 `Nd` 正整数天，默认 90。
- **风险 · 工作流从未被机械记下**：多数 workflow:* 会长期落在 C，这是 R11 的诚实缺口，报告要原样打出来，不把 C 解释成「没人用这个命令」。
- **风险 · 时钟**：分档用报告生成时的 UTC 墙钟，测试注入 `now`。
