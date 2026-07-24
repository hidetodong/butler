---
状态: ack-frozen
ACK 日期: 2026-07-23
---
<!-- butler-artifact-template: 1.0.0 artifact=acceptance -->
# AC_LIST — ITER-0090

## Goal

- 用 `/butler:setup` / `$butler-setup` 完成 Butler 机器级安装，同时保持安装脚本单一真源和显式授权边界。

## In Scope

- setup 规则、双宿主入口、Codex skill 元数据、registry/软链/人读表、init 复用和测试。

## Out of Scope

- 不把安装逻辑复制进命令；不自动接受 Codex hook trust；不替代项目 init/upgrade。

## Acceptance Checklist

- [ ] AC1: registry 唯一登记 setup，并生成 `/butler:setup`、`$butler-setup`、agents metadata、仓库发现软链和人读表。
- [ ] AC2: 两宿主入口解析可信 `BUTLER_PATH`，先说明机器级影响并要求显式确认，再以 argv 方式调用 `scripts/setup.sh`。
- [ ] AC3: setup 成功时逐项报告 Claude/Codex/Pi 结果；失败时保留真实退出码和部分完成事实，不伪报成功、不自行绕过 hook trust。
- [ ] AC4: init 只复用 setup 命令/规则指针，不再复制机器级安装算法；init 项目部署语义保持不变。
- [ ] AC5: 首次安装的 bootstrap 边界写清：完全空白机器仍需从仓库执行脚本，已发现 Butler 的宿主可直接用命令。
- [ ] AC6: skill validator、registry 正负向、setup 隔离测试、Codex foundation、完整 CI、状态审计和 diff check 全部通过。

## Verification Method

- registry/skill 结构检查；临时 HOME + stub Codex/Pi 的 setup 脚本隔离测试；完整 CI 与状态审计。

## External References

- N/A

## Open Questions / Risks

- N/A
