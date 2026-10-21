<!-- butler-artifact-template: 1.0.0 artifact=tech_plan -->
# TECH_PLAN — ITER-0123

方案状态: pass
方案审查日期: 2026-09-29
方案审查方式: user-ack

## Design Decisions

- 新建只读工具 `tools/usage-report/`，按最后调用时间把入口分成 A/B/C/D，默认 90 天。
- 缺文件或坏文件仍退出码 0，名单全在 C；坏文件不打点、不改字节。
- 报告不把 C 写成「没人用」，也不自动淘汰。

### D1 · 单独一个只读报告工具

新建 `tools/usage-report/usage_report.py`。子命令 `report --project-root --since`。`--since` 只接受正整数加 `d`，默认 `90d`。stdout 一份 JSON，含 `since_days`、`generated_at`、`buckets` 下的 A/B/C/D。每条有 `id`、`bucket`、`last_used`。

### D2 · 先读后打点，坏文件一字不改

分档读的是这次调用之前的 `.ai/.usage.json`。缺文件，或采集器认不出这份文件，退出码 0，名单全在 C，D 为空。文件能读时，报告打出之后再给自己记一笔 `tool:usage-report`。文件认不出时不打点，避免采集器把坏文件整份换掉。

### D3 · 分档只比最后调用时间

窗口起点是生成时刻往前 `since_days` 天，格式与采集时间戳相同，字符串可以直接比。等于起点算 A，更早算 B。名单里没有合法时间戳算 C，`last_used` 为 null。文件里多出来的 id 算 D。

### D4 · 名单复用，不另造表

覆盖范围就是 `allowed_ids()`。`usage-report` 加进产品工具名单，目录对账才绿。测试注入 `now`。命令行不提供改时钟的参数。

### D5 · 不声明 TDD

行为用正向测试锁住。本轮没有先红后绿的配对。

### 执行顺序

- [ ] T1 报告库与测试 → AC1–AC5 / AC8
- [ ] T2 登记产品工具并打点 → AC6
- [ ] T3 删掉 debt 里缺报告那条 → AC7
- [ ] T4 CI 接入，重算全貌，跑验证与审计 → AC9

### Plan Admission

- **AC Coverage**：AC1–AC5 与 AC8 由 T1 覆盖；AC6 由 T2；AC7 由 T3；AC9 由 T4。
- **Assumptions**：采集文件仍是第 1 版，时间戳仍是 UTC 的 `YYYY-MM-DDTHH:MM:SSZ`。窗口按整天计算。
- **Alternatives / Trade-offs**：否掉在 `usage.py` 里加子命令，避免采集和报告缠在一起。否掉命令行改时钟。否掉从坏文件里掏 D，认不出的文件不能当证据。否掉自动淘汰。
- **Failure Modes**：非法 `--since` 非零退出，且 stdout 不是成功报告。时间戳残缺时，名单内进 C，名单外进 D 且 `last_used` 为 null。坏文件不打点。
- **Impact / Scope Challenge**：不改采集格式，不补次数，不切版，不改工作流薄壳。
- **Verification Blind Spots**：真实会话里有没有人看这份报告，本轮不证明。工作流多数会落在 C，因为它们没有进程钩，这不是使用量为零的证据。
- **Verdict**：pass。用户说「继续开发」，验收范围按已起草的清单冻结，并授权按该清单开写。没有必须先改的设计缺陷。

## Failure Paths

- 非法窗口写到 stderr，stdout 为空，退出码 1。
- 缺文件或坏文件退出码 0，全员 C，D 为空。坏文件保持原字节。
- 合法文件里的坏时间戳不抬高档位。名单内进 C，名单外进 D。
- 打点失败时报告已经打出，采集错误不改变退出码。

## Test Strategy

本轮不声明 TDD cycle。`tools/usage-report/tests` 锁四档、默认 90 天、7 天边界、非法 since、缺文件、坏文件、全名单覆盖和打点顺序。`tools/usage/tests` 的目录对账继续绿。

## References Compliance

- N/A
