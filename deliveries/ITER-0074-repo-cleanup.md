# ITER-0074 仓库卫生清理

## 一句话
清理过期 worktree 残留、堆积分支和空壳目录，让仓库回到干净状态。

## 做了什么

| 清理项 | 操作 | 释放 |
|---|---|---|
| `.claude/worktrees/iter-0045/` | `git worktree remove --force` | 4.2 MB |
| 16 个已合并本地分支 | `git branch -d/-D`（含 3 个 worktree-agent-*） | — |
| 10 个已合并 github 远程分支 | `git push github :xxx` | — |
| 1 个已合并 origin 远程分支 | 连接不可达，本地 tracking ref 已清 | — |
| `Learner/` + `Composer/` | `rm -rf`（6 月至今只有 WIP README） | ~1 KB |
| README.md / architecture.md / CLAUDE.md | 移除 Learner/Composer 引用 | — |

## 附带修复（P0，审计发现）

- `test-workflow-registry.py` case=10：`[-1]` 索引改为按 `id=="dangerous"` 查找（新增 init/progress 后最后一个 workflow 不再是高风险）
- `verify-codex-workflows.sh` / `test_vendored_validators.py` / `test-goal-host-wiring.py`：skill/workflow 计数 8→10
- `.ai/task-state.md`：补 `# Goal Calibration` 空投影段
- `.ai/project/frontier.md`：版本 v2.17.0→v2.18.0 + 活跃战线更新
- `.ai/project/architecture.md` / `invariants.md` / `AGENTS.md` / `Coder/README.md`：8→10 文档同步

## 结果
- `verify-ci.sh` 全绿
- `git branch` 只剩 `* main`
- `git branch -r` 只剩 `github/main` + `origin/main`
