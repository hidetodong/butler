# AC List

状态: ack-frozen

- [ ] **AC1（命令文件成立）**：`.claude/commands/butler/progress.md` 存在且 frontmatter 含 description + argument-hint；正文含第 0 步降级、brief/完整两分支路由、§1–§9 固定段落定义
- [ ] **AC2（Codex skill 成立）**：`plugins/butler/skills/butler-progress/SKILL.md` 存在且含 name + description frontmatter；`.agents/skills/butler-progress` 软链指向正确
- [ ] **AC3（registry 注册）**：`workflows/registry.json` 含 `progress` 工作流；`scripts/sync-workflow-registry.py --check` 报 10 workflows 且 exit 0
- [ ] **AC4（投影同步）**：`docs/workflows.md` 含 progress 行；`scripts/sync-workflow-registry.py --write` 生成 41 个投影无报错
- [ ] **AC5（文档计数一致）**：capabilities.md / HUMAN_GUIDE.md / README.md / codex-compatibility.md 中的工作流/skill 计数从 8 更新到 10
- [ ] **AC6（全局可达）**：`.claude/commands/butler/progress.md` 在命名空间目录下，经 setup.sh 目录软链机制自动全局可用
