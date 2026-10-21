---
状态: ack-frozen
ACK 日期: 2026-09-14
---
<!-- butler-artifact-template: 1.0.0 artifact=acceptance -->
# AC_LIST — ITER-0122

## Goal

- 产品驻留 CLI 被调用后，项目本地能读到该入口的最后调用时间。这份数据不进 git。采集失败不能把原命令弄挂。90 天报告不做。

## In Scope

- `tools/usage/` 读写 `.ai/.usage.json`（record + 只读查询）。
- gitignore。
- 产品驻留 Python CLI 的 `main` 打点。
- 工作流薄壳的 record 调用说明 + `usage.py record workflow:<id>`。
- 入口身份封闭名单与 fail-open。
- 更新 `debt.md` 观测缺位那条。

## Out of Scope

- `tools/usage-report/`、`usage report --since 90d`、A/B/C/D 分档。
- 自动淘汰、preference、evidence 降维。
- 切版、v4.0.0 配方。
- 宿主级自动拦截 slash 命令。
- 采集次数/参数/路径；采集 hook 放行。
- vendored validators、dogfood 脚本、delivery-selftest。

## Acceptance Checklist

- [ ] AC1: `.ai/.usage.json` schema 为 `schema_version: 1` 加 `entries` 对象；每条只有 `last_used`（UTC `YYYY-MM-DDTHH:MM:SSZ`）。本仓 `.gitignore` 含 `.ai/.usage.json`。
- [ ] AC2: `python3 tools/usage/usage.py record --project-root <root> --id tool:intake` 在该根写入/覆盖 `tool:intake` 的 `last_used`；同 id 第二次调用时间戳更新；只读查询能读出。
- [ ] AC3: 未知 id（不在封闭名单）record 退出码非 0、零字节写入。名单含 `workflow:router`、registry 里全部 12 个工作流 id，以及 Scope 列出的产品驻留工具。
- [ ] AC4: 名单派生可重跑：漏掉一个产品工具目录或 registry 工作流，检查会失败。
- [ ] AC5: 产品驻留工具至少抽 3 个真实 CLI（`intake`、`handoff`、`goal-assurance`）跑一遍无害子命令后，对应 `tool:<名>` 出现在 `.ai/.usage.json`。
- [ ] AC6: record 在目录不可写时退出码 0（CLI record 自己）或被包装的工具仍返回原退出码；不新建半截文件。没有 `.ai/` 且解析不到项目根时静默跳过、不在仓根造文件。
- [ ] AC7: 12 个工作流薄壳 + router（Claude 命令与 Codex skill）正文都出现 `usage.py record` 与对应 `workflow:<id>`。
- [ ] AC8: `debt.md` 不再把「每个入口记录最后调用时间戳」写成未做；报告/分档仍指向 R12。
- [ ] AC9: `python3 -m pytest tools/usage/tests -q` 退出码 0；被打点工具的既有测试不因打点变红。
- [ ] AC10: `bash scripts/verify-ci.sh` 退出码 0；`python3 scripts/audit-project-state.py --project-root . --allow-unreleased` 退出码 0，`[DRIFT]` 为 0。

## Verification Method

- AC1 / AC2 / AC3 / AC6: `tools/usage/tests` 用临时项目根。
- AC4: 同一测试读 registry 与 tools 目录集合。
- AC5: 测试里 subprocess 调三个 CLI。
- AC7: 扫 `.claude/commands/butler/` 与 `plugins/butler/skills/`。
- AC8: grep `debt.md`。
- AC9 / AC10: pytest、verify-ci、审计取退出码。

## External References

- N/A

## Open Questions / Risks

- 工作流薄壳的打点没有进程级机械保证，AC7 只能证明「写了这一步」。
- 抽 3 个 CLI 不能证明每一个 main 都接上了；AC4 锁名单，AC5 锁接线样本。漏接的工具会在 AC4 红，除非有人把目录从名单里拿掉。
