<!-- butler-artifact-template: 1.0.0 artifact=tech_plan -->
# TECH_PLAN — ITER-0122

方案状态: pass
方案审查日期: 2026-09-14
方案审查方式: user-ack

## Design Decisions

### D1 · 一个库、一份本地文件、fail-open

`tools/usage/usage.py` 是唯一写盘者。落点 `$PROJECT_ROOT/.ai/.usage.json`。没有 `.ai/` 目录就跳过，不在仓根造文件。写盘用临时文件再 `os.replace`。任何 IO/解析错误吞掉。`record` CLI 对写失败退出码 0；对未知 id 退出码 1 且零写入。

### D2 · 入口身份封闭，从 registry + 工具目录派生

允许的 id：`workflow:router`、`workflow:<registry id>`、`tool:<产品目录名>`。产品目录名单与「明确跳过」名单写死在 usage.py，测试断言 `tools/` 子目录恰好等于两名单之并。漏加新产品工具会红。

### D3 · CLI 在 `main` 里 stamp，用 argv 里的 `--project-root`

测试经常直接调 `main([...])`，不能读 `sys.argv`。`stamp_tool(__file__, argv)` 从 argv 抽 `--project-root`，没有则看 cwd 是否有 `.ai/`。

### D4 · 工作流只加薄壳一句，不假装有进程钩

Claude 命令和 Codex skill 在解析出 PROJECT_ROOT 之后调用 `usage.py record --id workflow:<id>`。AC7 扫字面。

### D5 · 不声明 TDD

新库用正向测试锁行为。现有工具测试应继续绿。

### 执行顺序

- [ ] T1 usage 库 + 测试 + gitignore → AC1–AC4 / AC6
- [ ] T2 产品 CLI `main` 打点 → AC5 / AC9
- [ ] T3 工作流薄壳 → AC7
- [ ] T4 debt.md → AC8
- [ ] T5 CI 接入 usage 测试，跑 verify-ci 与审计 → AC10

### Plan Admission

- **AC Coverage**：AC1–AC4/AC6→T1；AC5/AC9→T2；AC7→T3；AC8→T4；AC10→T5。
- **Assumptions**：产品工具都有可识别的 `main`；`--project-root` 是通用旗标。
- **Alternatives / Trade-offs**：否掉家目录全局账（里程碑写明 gitignore）。否掉宿主 UserPromptSubmit 钩（Codex 走不通）。否掉打点次数。
- **Verdict**：pass。用户 ACK 验收范围并授权开写。

## Failure Paths

- 解析不到项目根却在 cwd 乱写：没有 `.ai/` 就跳过。
- 未知 id 被 stamp_tool 用目录名造出来：目录不在产品名单则 stamp_tool 直接返回。
- 采集异常改变退出码：stamp 全吞；record CLI 只对未知 id 非零。
- 新产品工具没登记：AC4 目录集合对账。

## Test Strategy

本轮**不声明 TDD cycle**。`tools/usage/tests` 覆盖 schema、覆盖更新、未知 id、目录对账、写失败 fail-open、三个真实 CLI 抽样。既有工具测试回归。

## References Compliance

- N/A
