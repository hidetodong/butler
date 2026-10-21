<!-- butler-artifact-template: 1.0.0 artifact=tech_plan -->
# TECH_PLAN — ITER-0125

方案状态: pass
方案审查日期: 2026-10-21
方案审查方式: user-ack

## Design Decisions

- 本轮要让升级器写得出两类动作：删掉点名的文件或目录，以及把仓根上的路径搬进 `.ai/`。对应已冻结的 AC1 到 AC7。
- 改这四处：`Coder/20_Workflow_Lifecycle/migration-schema.md` 第 4 节、`tools/butler-upgrade/upgrade.py`、`tools/butler-upgrade/README.md` 里项目域那一行、`scripts/test-butler-upgrade.py`。
- 不改 `migrations/manifest.json`，不新建 `migrations/v4.0.0.md`，不改 `VERSION`。`--split` 的参数定义保持 `apply` 必填、取值只有 `defer` 和 `now`。preference、loop、evidence 都不碰。
- 已有动作的行为保持原样。`rename`、hook 同步里现有的文件级删除还走原来的 `unlink`。目录的创建和删除是这次新增的操作，不把旧动作改成另一套写法。

### D1 · 标签和程序类型

在 `[rename]` 后面加上 `[delete]` 和 `[move]`。`[split]` 整段原样留下，包含它自 v4.0.0 起不再产生新实例的那句退役说明。

程序类型用 `delete` 和 `move`，域都是 `project`。字段：删除只有 `path`，移动只有 `from` 和 `to`。公共字段仍是 `id`、`type`、`domain`、`preconditions`。前置条件用新名字，删除是 `delete-path-allowed`，移动是 `move-path-allowed`，两项都是恰好这一条，不复用 `rename` 的前置条件。

校验器在认动作时就检查路径。现有清单里没有这两类，所以现有 `migrations/manifest.json` 仍能通过。未知类型（现有测试把类型改成 `shell`）仍拒绝。

### D2 · 路径允许什么

路径先过现有的相对路径检查：拒绝绝对路径、`..` 和单独一个 `.`。

删除允许仓根上的相对路径，例如 `origin`。也允许 `.ai/` 下不受保护的路径。路径正好是 `.ai` 时拒绝，因为删掉它会毁掉项目状态。第一段是 `.ai`、第二段是 `iterations`、`milestones`、`references`、`verification-evidence`、`butler-upgrade` 时拒绝。不额外禁止别的仓根名字，因为以后要删的 `origin/` 就在仓根。

移动的源用和删除同一套允许范围。目标必须在 `.ai/` 下面，不能正好是 `.ai`，也不能落进上面那五个保护目录。源在 `.ai/` 外、目标也在 `.ai/` 外，拒绝。`from` 和 `to` 相同，拒绝。

### D3 · 起始态

两类都先看起始态，不满足就不动。

删除：目标在，就删。文件只删该文件。目录连同里面的文件一起删，空目录也算一次真正的变更。目标已经不在，再跑视为完成，计划里没有变更，执行变成已经是当前版本，退出码 0。

移动：源在、目标不在，才搬。搬完内容字节不变，源消失。源和目标都在，退出码 2，两边都不改，不覆盖。源和目标都不在，退出码 2，不当成已经搬完。源已经不在、目标已经在，视为完成，退出码 0，不再造第二份。这一条不比较目标现有字节和上一次搬过去的内容是否相同。

顶层路径或任一子项是符号链接时，整次动作拒绝，退出码 2，不跟随链接，项目内容不变。路径分量上的符号链接，现有的边界检查已经会拒绝。

计划阶段就拒绝的情况，在写入前退出，不建本次备份。

### D4 · 目录怎样进现有事务

现有执行队列按路径排序，然后按 `unlink` 删文件。目录不能靠这个顺序，因为先删父目录会让后面的文件找不到，失败后也恢复不回来。

排序之后把队列重排成四段，同一段内部仍按路径排序：先 `ensure-dir`（补目标目录），再 `write`（写文件），再 `delete`（删文件），最后 `remove-dir`（删目录，深的在前）。`BUTLER_UPGRADE_FAIL_AFTER` 仍按这个重排后的队列计数，数到就抛出错误并恢复。

恢复按队列反序。被删的源目录先重建，再把文件从本次备份写回去。本次新建的目标目录，在里面的文件撤掉之后删掉。文件的备份和写回保持现在的做法。`restore.json` 每条记下操作种类，这样恢复知道该建目录还是写文件。

失败退出码仍是 5。比对项目是否回到动手前时，忽略 `.ai/butler-upgrade` 这棵运行时目录，沿用测试里已有的 `ignore_runtime`。

### D5 · 测试不走真实版本链

不改仓库里的 `migrations/manifest.json`，也不复制整个仓库当升级源。每个行为测试自建一个临时的 butler 根：`VERSION` 写 `0.0.1`，清单基线 `0.0.0`，只有一条迁到 `0.0.1` 的迁移，旁边放一个空的 `migrations/v0.0.1.md`，动作里只有正在测的 `delete` 或 `move`。

临时项目和这个夹具根并排放，不能放进夹具里面，否则会触发「拒绝升级 butler 自己」。项目里有 `.ai/`，两份入口文件带合法标记，版本戳是 `规则源：butler v0.0.0`。

用仓库里的 `upgrade.py`，`--butler-root` 指向夹具，`--project-root` 指向临时项目，`apply` 带 `--split defer`。这条动作不重戳版本，所以第二次执行仍会选中同一条动作。幂等靠动作自己的起始态，不靠版本戳往前走。

另外复制一份内存里的真实清单，把其中一条动作改成合法的 `delete` 或 `move`，校验器应接受。改成非法路径应拒绝。`apply` 不带 `--split` 仍由参数解析拒绝，这条用子进程断言，参数定义不改。

### 执行顺序

- [ ] T1 在 `migration-schema.md` 第 4 节的 `[rename]` 后写上 `[delete]` 与 `[move]`，写明起始态、重复执行的结果、冲突即停且不覆盖 → AC1
- [ ] T2 在 `upgrade.py` 接上动作表、路径校验、规划、重排后的执行和恢复，并在 README 的项目域那一行写上 delete/move → AC2 AC3 AC4 AC5
- [ ] T3 在 `scripts/test-butler-upgrade.py` 用临时夹具补测试 → AC2 AC3 AC4 AC5 AC6
- [ ] T4 跑 `python3 scripts/test-butler-upgrade.py`。完整的持续集成和审计留到验收阶段核对 AC7 → AC7

### Plan Admission

- **AC Coverage**：AC1 由 T1 覆盖。AC2、AC3、AC4、AC5 由 T2 和 T3 覆盖。AC6 由 T3 覆盖。AC7 由 T4 和验收阶段的三条命令覆盖。
- **Assumptions**：临时夹具清单足以走真正的 `build_plan` 和 `apply_plan`。本轮不需要一份 v4.0.0 配方才能证明动作可用。
- **Alternatives / Trade-offs**：放弃只对文件调用 `unlink`，因为删掉的目录树恢复不回来。放弃让建目录和删文件混在同一条路径排序里。放弃改真实清单或复制整个仓库当夹具。放弃改 `--split`，那会把已退役的知识文件夹和 v4 配方拉进本轮。
- **Failure Modes**：源和目标冲突，或两边都不存在，退出码 2，项目摘要不变。遇到符号链接，同样拒绝且不写入。注入失败后退出码 5，忽略运行时目录后项目摘要回到动手前。
- **Impact / Scope Challenge**：不写 v4.0.0 配方，不切版，不在真实已部署项目上跑，不改 preference、loop、evidence。持续集成脚本已经会跑升级器测试，本轮不改那条调用。
- **Verification Blind Spots**：幂等的移动不核对目标里的字节是否等于当初搬过去的内容。已部署项目里的 `origin/`、旧收件箱和仓根 `deliveries/` 要等 R15 的配方才会真的被删或被搬。本轮不证明一个真实项目的升级。
- **Verdict**：pass。用户在 2026-10-21 说「方案可以」。没有必须先改的设计缺陷。

## Failure Paths

- 路径不合法、点到 `.ai` 本身或五个保护目录、移动目标不在 `.ai/` 下、`from` 与 `to` 相同：退出码 2，零写入。
- 移动时两边都在，或两边都不在：退出码 2，零写入，不覆盖。
- 顶层或子项是符号链接：退出码 2，不跟随，零写入。
- 删除的目标已经不在，或移动已经完成（源不在、目标在）：退出码 0，不另造一份。
- 目录写到一半失败：退出码 5，临时项目的目录和文件回到动手前。锁在收尾时释放，本次备份留在 `.ai/butler-upgrade/runs/`。

## Test Strategy

本轮不声明 TDD cycle。没有先失败再通过的配对。

`scripts/test-butler-upgrade.py` 用临时目录覆盖：删除文件、删除含文件的目录、删除空目录、目标已不在时再跑退出码 0、非法路径和保护目录拒绝且原文件还在。移动仓根文件和目录进 `.ai/` 后字节不变且源消失。两边都在、两边都不在时退出码非 0。源已不在且目标已在时退出码 0。符号链接拒绝。删除和移动含文件目录时注入中途失败，摘要回到动手前。真实清单仍通过校验，合法的新动作形状被接受，`shell` 仍被拒绝，`apply` 缺 `--split` 仍非 0。断言仓库没有 `migrations/v4.0.0.md`，`VERSION` 仍是 `3.6.0`。

验收阶段另跑 `bash scripts/verify-ci.sh` 和 `python3 scripts/audit-project-state.py --project-root . --allow-unreleased`，后者输出里不得有 `[DRIFT]`。

## References Compliance

- N/A
