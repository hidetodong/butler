# VERIFY_REPORT — ITER-0054

> 2026-07-17 · 危险模式 P5 完整强审 · 结论：AC1–AC8 通过，0 Must Fix。

## 验收结果

| AC | 结果 | 证据 |
|---|---|---|
| AC1 | ✅ 可靠 | 隔离 HOME 覆盖无 Codex 跳过、假 Codex 调 installer、Claude 全局 marker/软链/rc 幂等；两分支 exit 0。 |
| AC2 | ✅ 可靠 | renderer 首次生成两入口，版本/路径/规则卡占位符全部替换；重跑 byte-idempotent，默认权限 0644。 |
| AC3 | ✅ 可靠 | 7 个 unittest 覆盖非 Butler 前缀保真、两份 user 区逐字保留、legacy 前后缀迁移、重复 marker 双文件不写、缺模板不写。 |
| AC4 | ✅ 可靠 + 人读 | MCV §3 调统一 renderer 同时生成两入口，§2/4/5 原结构与 Claude hook 部署未删；明确 plugin 不复制进项目。 |
| AC5 | ✅ 可靠 + 人读 | upgrade 的侦察/首次/常规/验证/回退全部覆盖双入口；migration schema 新增 regen-entrypoints/global-install，历史 regen-claude 兼容。 |
| AC6 | ✅ 可靠 | `verify-dual-host.sh` 汇总隔离 setup/renderer、R1–R3 scripts、124 hook tests、官方 plugin validator、compile；全绿。 |
| AC7 | ✅ 可靠 + 人读 | README/HUMAN/兼容说明/Coder README 已登记统一 setup、双入口与 trust/非 sandbox 边界，无 R4 计划中残留。 |
| AC8 | ✅ 可靠 | 主代理完整强审修正 legacy 外部用户内容保真与文件 mode 两项 Must Fix 后 0 Must Fix；双层收口/发布后终检。 |

## 自动验证

- `bash scripts/verify-dual-host.sh` → PASS（含 renderer 7 tests、R1/R2/R3、124 pytest、plugin validator）。
- `bash -n`、Python compile、`git diff --check` → PASS。
- 协议结构断言：MCV renderer、upgrade AGENTS、migration 两 typed 标签 → PASS。

## 完整审查

- 正确性：两入口先全部 plan/validate，再各自原子 replace；marker 冲突 fail-closed；版本/路径/规则卡单源。
- 内容安全：普通用户文件 byte-prefix 保留；legacy Butler 区识别边界明确，区外前后缀与 user 区保留；临时文件继承原权限或 0644。
- 非回归：setup 原 Claude 三项和风格原文未删；MCV `.ai`/local constraints/Claude hooks 未改判定；124 hook tests 全绿。
- 边界：setup 不自动 trust；Codex 缺失时不影响 Claude；PreToolUse 未扩称 sandbox。
- 独立复核：未执行。团队策略不允许未经明确委派启动子 agent；本报告为主代理完整强审，不冒称独立。

## Remaining Risks

- 两文件是“各文件原子”，不是文件系统级跨文件事务；可预见错误已在写前全校验，极端磁盘/权限故障仍可能只替换第一份。
- Codex hook 首次信任必须由用户在实际产品中完成；自动化不能代替该动作。
