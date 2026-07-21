---
方案状态: pass
方案审查日期: 2026-07-21
方案审查方式: self
---

# Goal
仓库卫生清理——纯 git/file 操作，不改规则内容。

# Files
| 文件/目录 | 操作 |
|---|---|
| .claude/worktrees/ | 删除整个目录 |
| 本地已合并分支 | git branch -d |
| 远程已合并分支 | git push origin --delete |
| Learner/ | 评估后删除或保留 |
| Composer/ | 评估后删除或保留 |
| .ai/project/architecture.md | 若删除 Learner/Composer 则移除引用 |

# Design Decisions
- 纯清理操作，不涉及规则算法变更
- 分支清理前先确认 main 是最新的
- Learner/Composer 若 README 描述的功能仍有意向则保留并标注，否则删除
