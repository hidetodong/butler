# Workspace Scope Tool

标准库只读工具，把项目工作区地图、AC 钉版的 PRD 范围、TECH_PLAN 写计划和真实路径放到同一套规则中对账。

```bash
python3 tools/workspace-scope/workspace_scope.py discover --project-root "$PROJECT_ROOT"
python3 tools/workspace-scope/workspace_scope.py validate --project-root "$PROJECT_ROOT"
python3 tools/workspace-scope/workspace_scope.py check-plan --project-root "$PROJECT_ROOT"
python3 tools/workspace-scope/workspace_scope.py check-paths --project-root "$PROJECT_ROOT" --path apps/web/src/main.ts
python3 tools/workspace-scope/workspace_scope.py check-diff --project-root "$PROJECT_ROOT" --base HEAD --include-untracked
```

- 全部动作只读，stdout 是 schema v1 稳定 JSON。
- exit 0 表示通过；exit 2 表示输入、布局、范围或 Git 检查失败。
- 没有 `prd_refs` 的普通迭代返回 `applicable:false`，不伪造需求范围。
- 有 `prd_refs` 时，地图、钉版版本、模块范围、Write Plan 或路径归属任一不完整都会 fail-closed。
- `check-diff` 是 shell 等不经过 PreToolUse hook 的 P5 兜底；它不替代宿主物理权限。
