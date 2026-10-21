---
状态: ack-frozen
ACK 日期: 2026-09-29
---
<!-- butler-artifact-template: 1.0.0 artifact=acceptance -->
# AC_LIST — ITER-0123

## Goal

- 一条命令能按时间窗口把全部入口分成 A/B/C/D 打出来，让淘汰判断第一次有数据可依。不自动砍。

## In Scope

- `tools/usage-report/` 只读报告。
- `--since Nd`，默认 90d。
- 复用 usage 封闭名单；usage-report 自己进产品工具名单。
- 缺/坏 `.usage.json` 仍能出完整名单报告。
- CI、OVERVIEW、debt 观测缺位条目。

## Out of Scope

- 自动淘汰、preference、evidence 降维。
- 改采集 schema、补次数、补 slash 进程钩。
- 切版。

## Acceptance Checklist

- [ ] AC1: `python3 tools/usage-report/usage_report.py report --project-root <root>` 默认窗口 90 天；stdout 是 JSON，含 `since_days`、`generated_at`、`buckets`（A/B/C/D 四个键）。
- [ ] AC2: 夹具里一条 last_used 在窗口内 → A；一条更早 → B；名单里没有记录 → C；文件里多一个已不在名单的 id → D。每条含 `id`、`bucket`、`last_used`（C 为 null）。
- [ ] AC3: `--since 7d` 改变分档边界；非法值（缺 d、0d、小时）退出码非 0，stdout 不是成功报告。
- [ ] AC4: 没有 `.usage.json` 或文件损坏时退出码 0，名单条目全在 C，D 为空。
- [ ] AC5: 报告覆盖 `allowed_ids()` 的每一个 id，不丢、不加名单外的活入口（D 除外）。
- [ ] AC6: `tools/usage/usage.py` 的 `PRODUCT_TOOLS` 含 `usage-report`；`tool_dirs` 对账仍绿。
- [ ] AC7: `debt.md` 不再有「还没有 90 天报告和 A/B/C/D 分档」这句。
- [ ] AC8: `python3 -m pytest tools/usage-report/tests -q` 退出码 0；`python3 -m pytest tools/usage/tests -q` 仍绿。
- [ ] AC9: `bash scripts/verify-ci.sh` 退出码 0；审计 `--allow-unreleased` 退出码 0，`[DRIFT]` 为 0。

## Verification Method

- AC1–AC5 / AC8: usage-report 测试用临时项目根和注入 `now`。
- AC6: usage 既有目录对账测试。
- AC7: grep debt.md。
- AC9: CI 与审计取退出码。

## External References

- N/A

## Open Questions / Risks

- C 档会偏多，因为工作流大多没有机械打点。报告不得把 C 写成「已证实无人使用」。
