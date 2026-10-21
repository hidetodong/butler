#!/usr/bin/env python3
from pathlib import Path
root = Path(".").resolve()
errors=[]
def need(path, token, msg):
    text = (root/path).read_text(encoding="utf-8")
    if token not in text:
        errors.append(msg + ": missing " + token[:60])
need("Coder/20_Workflow_Lifecycle/mcv-deployment.md", "强制创建 `.ai/` 这一个基础目录", "deploy")
need("Coder/20_Workflow_Lifecycle/delivery-summary.md", "`.ai/deliveries/`", "delivery-summary")
need("templates/rule-card.md", "只在该项目根创建 `.ai/` 与双宿主入口", "rule-card")
need(".claude/commands/butler/init.md", "只创建 `.ai/` 目录", "init")
need("plugins/butler/skills/butler-init/SKILL.md", "create `.ai/` only", "init skill")
need(".ai/MILESTONE.md", "2026-09-11（R9 · 按 `migration-schema.md §5` 的迁移判定）", "milestone log")
need(".ai/MILESTONE.md", "必须含 `[regen-entrypoints]`", "regen-entrypoints")
need(".ai/MILESTONE.md", "不需要 `[sync-hooks]`", "no sync-hooks")
if errors:
    print("FAIL")
    for e in errors: print(e)
    raise SystemExit(1)
print("OK docs AC6 AC10")
