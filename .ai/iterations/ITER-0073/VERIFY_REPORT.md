# Verify Report

## 自动道

- [x] **AC1（命令文件成立）**(auto·可靠)：`.claude/commands/butler/progress.md` 存在，frontmatter 含 description + argument-hint，正文含第 0 步降级、brief/完整两分支路由、§1–§9 固定段落定义
- [x] **AC2（Codex skill 成立）**(auto·可靠)：`plugins/butler/skills/butler-progress/SKILL.md` 存在且含 name + description frontmatter；`.agents/skills/butler-progress` 软链 → `../../plugins/butler/skills/butler-progress` 正确
- [x] **AC3（registry 注册）**(auto·可靠)：`workflows/registry.json` 含 `progress` 工作流（10 个总计）；`scripts/sync-workflow-registry.py --check` exit 0
- [x] **AC4（投影同步）**(auto·可靠)：`docs/workflows.md` 含 progress 行；`sync-workflow-registry.py --check` 报 10 workflows / 41 projections 无报错
- [x] **AC5（文档计数一致）**(auto·可靠)：capabilities.md(2处) / HUMAN_GUIDE.md(3处) / README.md(1处) / codex-compatibility.md(1处) 均已更新为 10
- [x] **AC6（全局可达）**(auto·可靠)：命令文件在 `.claude/commands/butler/` 命名空间目录下，经 setup.sh 目录软链机制自动全局可用

## 人测道

无（纯文件结构变更，无需人测）

## 置信档

全部 6 条 AC 由机器命令验证通过，置信档：**可靠**。

## Independent Review

未执行（独立迭代，改动面为新增文件 + 计数更新，无算法变更）
