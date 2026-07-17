# Codex 兼容地基：Butler 开始原生认识第二个宿主

> ITER-0051 · MILE-0006 R1 · 收口 2026-07-17 · v2.12.0

## 本次交付目标

让 Codex 不靠用户级兜底配置，就能在 Butler 仓根识别规则、恢复 `.ai/` 状态并找到完整 `Coder/` 真源；同时把后续 skills/plugin、hooks、部署升级所需的双宿主边界先钉牢。

## 已完成内容

- 新增仓根 `AGENTS.md`，声明这是规则仓而非业务项目，固定地图→台账→断点→四件套→规则真源的冷启动顺序。
- 新增 `templates/AGENTS.md.template`。它与 Claude 模板共享版本、规则卡、仓路径占位契约和 user-managed 保护区，不复制第二份规则卡。
- 新增 `docs/codex-compatibility.md`，区分共同内核、Claude 适配层、Codex 适配层，并公开 R1–R4 支持矩阵。
- 新增 `scripts/verify-codex-foundation.sh`，从任意目录运行都能检查入口、读序、模板契约、单一真源和文档注册。
- README、Coder 入口和 HUMAN_GUIDE 已短注册当前能力；Claude Code 现有入口、命令、hooks、setup 和算法均未改。

## 验证结果

- AC1–AC9 全过。
- 真实 `codex exec` 只读新会话准确复述仓库定位、第一冷启动文件和验证命令，证明 `AGENTS.md` 自动发现生效。
- 结构脚本在仓根与 `/tmp` 调用都通过；`bash -n`、`git diff --check` 通过。
- 既有 Claude hook 测试 109 passed；Claude 入口、命令、hook、setup 定向 diff 为空。

## 用户可感知变化

从 v2.12.0 起，在 Butler 仓库里启动 Codex，它会原生读到仓库规则入口。这个版本没有自动改任何已部署目标项目，也没有提供 Codex skills 或机械门禁。

## 剩余路线

- R2：8 个工作流 skills + plugin。
- R3：Codex hooks + `apply_patch` 适配。
- R4：首次部署、升级双入口和 Claude/Codex 双端回归。

## 引用

- 架构与状态：`docs/codex-compatibility.md`
- 仓库入口：`AGENTS.md`
- 目标模板：`templates/AGENTS.md.template`
- 验证：`.ai/iterations/ITER-0051/VERIFY_REPORT.md`
- 迁移：`migrations/v2.12.0.md`
