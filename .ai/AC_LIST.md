---
状态: ack-frozen
ACK 日期: 2026-07-17
ACK 方式: dangerous-self-review
---

> ⚠️ 危险模式：本产物由模型自主 ACK（已过 dangerous-engine §5.1 自审门），未经用户逐项确认（ITER-0054，2026-07-17）。

# Goal

交付 Claude/Codex 统一安装、双入口首次部署与升级链，并完成 MILE-0006 回归收官。

# Acceptance Checklist

- [x] **AC1（统一 setup）**：`setup.sh` 保持既有 Claude 全局配置/命令/风格行为，并在 Codex CLI 可用时调用 plugin 安装；不可用时明确跳过且退出 0；隔离 HOME 重跑幂等。
- [x] **AC2（双入口渲染器）**：标准库工具从两模板+单一 rule-card 渲染 CLAUDE.md/AGENTS.md，替换全部占位符、写同版号/路径；首次运行生成，重复运行无 diff。
- [x] **AC3（内容保护）**：已有非 Butler 文件不被覆盖而追加 managed block；更新 managed block 时两个入口各自 user-managed 内容逐字保留；异常/重复 marker fail-closed、不写半成品。
- [x] **AC4（首次部署接线）**：mcv-deployment 明确同时生成两入口并调用渲染器；`.ai/`/local constraints/Claude hooks 原流程不退化，Codex plugin 保持机器级、不复制到项目。
- [x] **AC5（既有升级接线）**：butler-upgrade 侦察、首次升级、常规队列、验证/回退覆盖 AGENTS.md；migration schema 新增双入口 typed 标签并规定幂等/漂移即停。
- [x] **AC6（回归矩阵）**：新增脚本在隔离 HOME/目标项目验证 setup 有/无 Codex 分支、渲染六场景、Claude hook tests、R1–R3 scripts、plugin validator；全绿。
- [x] **AC7（使用说明）**：README/HUMAN_GUIDE/兼容说明不再标 R4 计划中，说明一次 setup、双入口、hook trust 和未覆盖边界。
- [x] **AC8（发布收官）**：P5 完整强审 0 Must Fix；ITER-0054 与 MILE-0006 原子收口，归档/双层交付/知识前滚、最终版本四方一致、本地 tag 与 6 不变量通过。

# Verification Method

- AC1–3/6：隔离目录可执行断言（可靠）。
- AC4/5/7：结构 grep + 协议人读对账（可靠 + 人读）。
- AC8：完整测试、台账/归档/交付/版本/tag 机械检查（可靠）。

# Risks

- setup 调 plugin 安装涉及真实用户目录；回归用隔离 HOME，最终真实刷新只接管既有 `butler@personal`。
- managed markers 是新契约；无 marker 的旧文件只追加，不猜测删除旧内容，避免误伤，升级报告需提示人工清理重复旧 Butler 段。
