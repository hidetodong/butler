# TECH_PLAN — ITER-0054

> ⚠️ 危险模式：本产物由模型自主 ACK（已过 dangerous-engine §5.2 自审门），未经用户确认（ITER-0054，2026-07-17）。

# Goal

用一个可测试的入口渲染器统一首次部署和升级，再让 setup 统一完成两宿主的机器级安装。

# Files / Modules

- `scripts/render-project-entrypoints.py` + tests/verify：双模板渲染、managed/user markers、原子写。
- `scripts/setup.sh`：Codex CLI 检测与 plugin installer 接线。
- `mcv-deployment.md` / `butler-upgrade.md` / `migration-schema.md`：双入口产生、升级 typed 标签和验证/回退。
- README/HUMAN/兼容说明、迁移/交付/台账/项目知识。

# Contract

- 外层 marker：`<!-- butler-managed:start -->` / `<!-- butler-managed:end -->`；每文件恰好 0 或 1 对，重复/残缺即拒绝。
- 0 对：目标不存在则创建 managed block；目标已有内容则保留原文并在末尾追加 block。
- 1 对：从旧 block 提取恰好一对 user-managed 内容，填入新模板后原位替换；block 外内容逐字保留。
- 两文件先完整规划并校验，再以同目录临时文件 + replace 写入；任何规划错误时两文件都不动。
- `setup.sh` 先导出本进程 `BUTLER_PATH`；有 `codex` 时调用 installer，无则明确跳过。hook trust 不自动绕过。

# Execution Steps

- [x] **T1** 实现渲染器与六类隔离测试 → AC2/3
- [x] **T2** setup 接 plugin installer，补有/无 Codex 隔离 HOME 回归 → AC1/6
- [x] **T3** 首次部署/升级/migration schema 接同一渲染契约 → AC4/5
- [x] **T4** 文档和最终兼容矩阵前滚 → AC7
- [x] **T5** 全套回归、P5 强审、ITER+MILE 原子收口与最终 MINOR 发布 → AC6/8

# Verification

- renderer unit/integration、isolated HOME setup ×2、无 codex 分支。
- R1/R2/R3 scripts、plugin validator、124 hook pytest、shell/Python syntax、diff check。
- 6 不变量 + 双层交付 + 版本/tag/真实 plugin installed/enabled。

# Risks

- 旧版无外层 marker 的 Butler 内容不会自动识别删除；选择保守追加，避免把用户内容误判为可覆盖。
- 双文件不能获得文件系统级跨文件事务；采用“先全校验、后逐文件原子 replace”，把可预见失败挡在写入前。
