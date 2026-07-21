---
状态: ack-frozen
ACK 日期: 2026-07-21
---

# Goal
仓库卫生清理。

# Acceptance Checklist
- [x] AC1：`.claude/worktrees/` 目录不存在或为空
- [x] AC2：本地分支只剩 main（无 worktree-agent-*、无已合并 feat/fix/style/docs）
- [x] AC3：远程只保留 main + 仍有用的活跃分支（无已合并的残留）
- [x] AC4：Learner/ 和 Composer/ 删除并在 architecture.md/README.md/CLAUDE.md 移除引用
- [x] AC5：`verify-ci.sh` 全绿，`git status` 干净
