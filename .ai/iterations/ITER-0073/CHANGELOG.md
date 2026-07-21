# CHANGELOG — ITER-0073

## ADD
- .claude/commands/butler/progress.md
- plugins/butler/skills/butler-progress/SKILL.md
- plugins/butler/skills/butler-progress/agents/openai.yaml
- .agents/skills/butler-progress（软链）
- deliveries/ITER-0073-butler-progress-command.md
- deliveries/ITER-0073-butler-progress-command.html

## EDIT
- workflows/registry.json（新增 progress 工作流，第 10 个）
- scripts/sync-workflow-registry.py（EXPECTED_IDS 加 progress）
- docs/workflows.md（新增 progress 行）
- .ai/project/capabilities.md（工作流计数 8→10）
- HUMAN_GUIDE.md（工作流计数 8→10）
- README.md（工作流计数 8→10）
- docs/codex-compatibility.md（工作流计数 8→10）
- scripts/test-workflow-registry.py（高风险 workflow 按 id 查找替代 [-1] 索引）
- scripts/verify-codex-workflows.sh（skill 计数 8→10 + names 数组补 init/progress）
- tools/codex-validators/test_vendored_validators.py（skill 计数 8→10）
- scripts/test-goal-host-wiring.py（workflow 计数 8→10）
- .ai/task-state.md（Goal Calibration 空投影段补齐）
- .ai/project/frontier.md（版本 v2.17.0→v2.18.0 + 活跃战线更新）
- .ai/project/architecture.md（8→10 文档同步）
- .ai/project/invariants.md（8→10 文档同步）
- AGENTS.md（8 skills→10 skills）
- Coder/README.md（8 个工作流→10 个工作流）

## DELETE
（无）
