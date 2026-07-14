# Task State

> **活跃里程碑 MILE-0005**（butler 命令命名空间系统）· **活跃迭代 ITER-0047**（R1 命名空间地基 + `/butler-prd` 迁移）· 阶段 **P1 已出 `CONCEPT.md`，下一步 P2 写 `AC_LIST.md` 呈交 ACK 冻结**。分支 `feat/mile-0005-butler-command-namespace`（从 v2.6.1 = d0ae8ec）。

## MILE-0005 里程碑（active）

把 butler 散在规则正文里的「散文触发词」（`/milestone`、`/review`、`/loop` 等只是文档暗号、没有真实命令文件）收敛成一整套 `/butler:xxx` 命名空间下的真实 slash command——补全菜单可见、全局任意项目可用、`butler:` 前缀隔离撞名。路线图 4 迭代：**R1** 地基（ITER-0047，进行中）→ **R2** 批量补 milestone/upgrade/ideation → **R3** preference（子命令最多）→ **R4** loop/dangerous（加风险闸）。产物真源 `.ai/MILESTONE.md`。

## ITER-0047（active·R1 地基）

- **范围**：① 建 `.claude/commands/butler/` 命名空间子目录；② `/butler-prd`→`/butler:prd` 破坏性迁移（移文件 + 清旧全局软链 + 更新活规则/文档引用 + `[rename]` 迁移配方）；③ 改 `setup.sh` 软链逻辑（逐个软链 `*.md` → 软链整个 `butler/` 目录，一条目录软链托管全套）；④ 落 `/butler:review`（纯薄壳、验证范式可复制）。
- **已查证地基**：子目录＝命名空间、`butler/prd.md`→`/butler:prd`、user 级全局同理、frontmatter 照常、command `.md` 软链已实跑验证（维持 commands 路线、不迁 skills）。
- **P1 已完成**：`CONCEPT.md` 已写（含 3 个 Open Questions：切版号 bump / `/butler:review` 参数面 / 正文引用更新边界，均待 P2 定）。

## 下一步入口

- **P2 写 `AC_LIST.md`** → 呈交用户 **ACK 冻结**（`状态: ack-frozen`）才进 P3/P4。这是本迭代第一个硬门。
- 冷启动读序（butler 文件夹态）：`.ai/project/00_INDEX.md` → `.ai/MILESTONES.md` / `.ai/ITERATIONS.md` → 本文件 → `.ai/MILESTONE.md`（里程碑范围）/ `.ai/CONCEPT.md`（迭代 P1）→ 代码。
