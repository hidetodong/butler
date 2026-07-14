# 01_CHANGELOG

> **ITER-0047 已收口**（MILE-0005 R1·命名空间地基 + `/butler-prd` 迁移）。对象级变更流（ADD/EDIT/DELETE），绑 AC、文件+章节级粒度。变更流已归档 `iterations/ITER-0047/CHANGELOG.md`；开新迭代时本文件整体覆写。
>
> 上一迭代 ITER-0046 变更流见 `iterations/ITER-0046/CHANGELOG.md`。

## ADD

- `.claude/commands/butler/`（新建命名空间子目录，Claude Code 里子目录＝冒号前缀，`butler/<name>.md`→`/butler:<name>`）→ AC1
- `.claude/commands/butler/review.md`（新命令 `/butler:review` 纯薄壳路由器：默认当前上下文自检 → `review-engine §5` / `independent` → `independent-review`+`overview §3` fresh 子 agent 独立复核；第 0 步优雅降级、委托真源不复述算法、frontmatter 两行说人话）→ AC5
- `migrations/v2.7.0.md`（迁移配方：个人命令层 `[rename]` + 部署面 `[no-op]`+`[restamp]` + `[global-install]` 机器动作）→ AC6

## EDIT

- `scripts/setup.sh` §3（软链逻辑：逐文件 `for src in .../*.md` → `ln -sfn` 软链整个 `butler/` 命名空间目录到 `~/.claude/commands/butler`；新增旧扁平软链 `butler-prd.md` 的 `-L` 迁移清理段 + `-n` 防 `butler/butler` 套娃 + 计数 echo；收尾提示 `/butler-prd`→`/butler:prd`）→ AC4
- `README.md`（§目录结构树 `.claude/commands/` 重构出 `butler/` 子树含 `prd.md`+`review.md`）→ AC2
- `HUMAN_GUIDE.md` §3（slash 命令软链描述 `.claude/commands/*.md`→`butler/` 命名空间目录、`/butler-prd`→`/butler:prd`）→ AC2
- `.ai/project/capabilities.md`（命令表 `/butler-prd`→`/butler:prd` + 路径 `butler/prd.md` + §35 setup.sh 机制句改命名空间目录软链）→ AC2 + 收口折叠
- `.ai/project/frontier.md`（版本史/战线/下一步 3 处 `/butler-prd`→`/butler:prd`）→ AC2 + 收口折叠
- `VERSION`（2.6.1 → 2.7.0）→ AC7
- `CHANGELOG.md`（顶条新增 `## [2.7.0]` MINOR）→ AC7

## DELETE

- `.claude/commands/butler-prd.md`（**破坏性改名迁移**：`git mv` → `.claude/commands/butler/prd.md`，正文 byte-identical 零改；旧全局软链 `~/.claude/commands/butler-prd.md` 由 setup.sh 迁移清理段兜底删除）→ AC1/AC3
