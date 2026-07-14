# 01_CHANGELOG

> **ITER-0047 开放中**（MILE-0005 R1·命名空间地基 + `/butler-prd` 迁移）。对象级变更流（ADD/EDIT/DELETE），绑 AC、文件+章节级粒度，仅承载**当前开放迭代**的热数据。开新迭代时整体覆写；收口时归档至 `iterations/ITER-0047/CHANGELOG.md`。
>
> 上一迭代 ITER-0046 已收口，变更流见 `iterations/ITER-0046/CHANGELOG.md`。
>
> 本迭代改动在 P4 执行阶段产生（AC_LIST ack-frozen 前不写码），届时按 ADD/EDIT/DELETE 逐条回填。

## ADD

- 待 P4（预计：`.claude/commands/butler/review.md` 新命令 + `migrations/vX.Y.Z.md` 迁移配方）。

## EDIT

- 待 P4（预计：`scripts/setup.sh` 软链逻辑改造 + 活规则/文档对 `/butler-prd` 的引用更新）。

## DELETE

- 待 P4（预计：`.claude/commands/butler-prd.md` 迁移移除，内容转入 `butler/prd.md`）。
