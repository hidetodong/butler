---
方案状态: pass
方案审查日期: 2026-07-21
方案审查方式: self
---

# Goal
仓库卫生清理：清除过期 worktree 残留、堆积的本地/远程分支、空壳目录，让仓库回到干净状态。

# In Scope
- 删除 `.claude/worktrees/iter-0045/`（4.2 MB 过期并行工作副本）
- 清理已合并的本地分支（worktree-agent-* + 已合并 feat/fix/style/docs）
- 清理已合并的远程分支
- 评估 Learner/ 和 Composer/ 去留（当前各只有 README，6 月至今无实质内容）

# Out of Scope
- 不改规则文件内容
- 不改 CI / hook / 部署逻辑
- 不动 ITERATIONS.md 历史行
