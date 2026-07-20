---
方案状态: pass
方案审查日期: 2026-07-20
方案审查方式: self
---

# Goal
薄壳路由器命令，委托 mcv-deployment.md 执行。

# Files
| 文件 | 操作 |
|---|---|
| .claude/commands/butler/init.md | 新增 |
| plugins/butler/skills/butler-init/ | 新增 |
| .agents/skills/butler-init | 新增软链 |
| workflows/registry.json | 修改 |
| scripts/sync-workflow-registry.py | 修改 |
| docs/workflows.md | 修改 |

# Design Decisions
- 命令薄壳路由器，委托 mcv-deployment.md
- legacy_aliases 允许空列表
- normal risk, allow_implicit_invocation=true
