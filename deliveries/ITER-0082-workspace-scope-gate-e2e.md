# ITER-0082 · 工作区范围门禁与端到端验证

## 本次交付目标

让 PRD 声明的工作区范围真正约束技术方案、宿主写入和最终 Git 改动，并证明 MILE-0009 的整条需求治理链可以组合运行。

## 已完成内容

- 新增零依赖 workspace scope 共享内核和只读 CLI，覆盖 npm/pnpm/single-package 发现、地图/ownership、钉版范围、写计划、显式路径与 Git diff。
- PreToolUse 对 apply_patch、Edit、Write、MultiEdit 的每个目标复用同一判定；无 PRD 引用明确 N/A，legacy 无身份 fail-closed。
- 补齐 Path Ownership、Module Workspace Scope、Workspace Write Plan 与范围扩张的规则/部署/验证合同。
- 建立 MILE-0009 单工程 e2e 和真实 apps 只读 dogfood runner；迁移写入只发生在临时副本。

## 关键变更 / 用户可感知变化

- Workspace Scope 从“文档建议”升级为 `owner ∩ pinned scope ∩ write plan` 的机器门禁。
- shell 等绕过 PreToolUse 的写入由 P5 `check-diff` 兜底；rename/delete/untracked 都纳入检查。
- npm glob 可容纳普通非包目录，但 symlink、精确 workspace 缺 manifest、身份冲突或无匹配仍稳定拒绝。
- legacy 迁移兼容 `v28` 这类 doc revision，并能在产品版号同时出现时选择正确版本命名空间。

## 高层影响范围

- `templates/hooks/`、`plugins/butler/hooks/`
- `tools/workspace-scope/`、`tools/mile0009-e2e/`、`tools/prd-migrate/`
- Workspace/TECH_PLAN/VERIFY/部署 schema、Coder 入口与完整 CI

## 验证方式与结果摘要

- workspace 行为 10/10、hook/结构专项 13/13、MILE-0009 组合 e2e 通过。
- 真实 apps 发现 28 个 workspace；临时副本 migration plan/apply/verify/resolve/rollback 通过，原仓 Git status 与 PRD tree 双 hash 前后相同。
- 固定 Python 3.12.12 / uv 0.9.28 完整 CI 通过，hooks 195 项通过；Goal adjudicator 十项检查全绿。
- 证据索引：`.ai/iterations/ITER-0082/VERIFY_REPORT.md` 与 `.ai/iterations/ITER-0082/evidence/`。

## 已知剩余风险 / 延后事项

- PreToolUse 不覆盖 shell，交付流程必须保留 `check-diff`。
- Pi TypeScript 可选依赖在本机缺失，沿用既有 CI 警告降级；不是本迭代新增失败。
- 未执行 fresh-context 独立复核；已完成同上下文强审，最终 Must Fix 0、Should Fix 0。

## 引用

- `.ai/iterations/ITER-0082/`
- `.ai/iterations/ITER-0082/evidence/`
- `Coder/40_Context_Management/workspace-scope-schema.md`
- `tools/workspace-scope/`
- `tools/mile0009-e2e/`
