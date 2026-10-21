<!-- butler-artifact-template: 1.0.0 artifact=tech_plan -->
# TECH_PLAN — ITER-0126

方案状态: pass
方案审查日期: 2026-10-21
方案审查方式: user-ack

## Design Decisions

- 本轮把 3.6.0 之后欠下的迁移写成 `migrations/v4.0.0.md`，并在临时项目上证明它跑得通。对应已冻结的 AC1 到 AC9。
- `VERSION` 保持 `3.6.0`。升级器只执行目标版本不高于 `VERSION` 的步骤，所以这条配方写进清单之后，对着本仓库做计划不会选中 `4.0.0/` 开头的动作。切版、发布说明、标签、提交和 MILE-0016 收口都不在本轮。
- 不新造动作类型。旧收件箱和仓根 `origin/` 的停，做在计划阶段的一道门里。`preference` 沿用已有的 `migrate_config`，只在目标是 4.0.0 的那一次写回里去掉。

### D1 · 清单和配方

在 `migrations/manifest.json` 末尾加一节：`source` 为 `3.6.0`，`target` 为 `4.0.0`，`recipe` 为 `v4.0.0.md`。动作编号都以 `4.0.0/` 开头，目标版本严格递增，配方文件和清单互相覆盖。`validate_manifest` 必须通过。

`migrations/v4.0.0.md` 按 `v3.6.0.md` 的写法说明影响、步骤、要人处理的部分，以及这次不做什么。已发布的历史配方一个字不改。`migration-schema.md` 里 `[split]` 整段原样留下，包含知识文件夹和退役说明。

这一节的动作，按这个顺序：

1. `4.0.0/01-global-install`，类型 `global_install`。域是机器。`apply` 只把它记成待外部确认，不调用 `scripts/setup.sh`，也不改本机插件。
2. `4.0.0/02-delete-project-dir`，删除 `.ai/project`。目录连同里面的文件一起删。已经不在则视为完成。
3. `4.0.0/03-delete-project-md`，删除 `.ai/PROJECT.md`。已经不在则视为完成。
4. `4.0.0/04-move-deliveries`，把仓根 `deliveries` 移到 `.ai/deliveries`。源在且目标不在才搬，字节不变，源消失。两边都在则整次计划停下，不覆盖。源已经不在且目标已经在，再次执行视为完成，不另造一份，也不比较目标里的字节。
5. `4.0.0/05-migrate-config`，类型 `migrate_config`。卸掉 `preference` 这一键，见 D4。
6. `4.0.0/06-regen-entrypoints`。
7. `4.0.0/07-sync-hooks`。
8. `4.0.0/08-restamp`。版本戳写成临时 butler 根里的 `4.0.0`。本仓库的 `VERSION` 文件不改成这个数。

删除和移动用 R14 已经落地的路径规则。正好点到 `.ai`、点到受保护子目录、符号链接、两边路径重叠，都拒绝。本轮不改那些规则。

### D2 · 旧收件箱和 origin 先停

门写在 `build_plan` 里，只有选中的队列包含目标 `4.0.0` 时才走。版本号还是 `3.6.0` 时队列里没有这一节，这道门不生效，已有的旧版本升级保持原样。

停下的判据：

- `.ai/INBOX.md` 是符号链接，或者仓根 `origin` 是符号链接：退出码 2，不跟随，零写入。
- `.ai/INBOX.md` 是普通文件，且正文里有 `butler-inbox:managed`：退出码 2，零写入。这个标记是旧格式的识别点。不靠表头用词，因为新旧表头有共用的字。
- 仓根 `origin` 作为真实文件或目录存在：退出码 2，零写入。不看里面有什么，避免把用户自己的文件删掉。

这三处任一命中，`.ai/project/`、`.ai/PROJECT.md`、`deliveries/` 也不动。没有「有冲突也继续删别的」这条路。

新格式闪念口仍是 `.ai/INBOX.md`，标题是 `## 闪念`。文件里没有那个旧标记时，不因为它停下，也不改它的字节。两个条件都不存在时，升级继续。

不新增动作类型。现有前置条件必须和动作表逐字匹配，没有「在则冲突」这种类型可以挂。

### D3 · --split 不再必填，形状检查去掉

`apply` 的 `--split` 改为可带可不带。取值仍只有 `defer` 和 `now`。不带时不再因为缺参数被拒绝。

删掉 `build_plan` 里形状检查那一整段。现在它做两件事：项目只有 `.ai/project/`、没有 `00_INDEX.md` 时直接报错；`.ai/PROJECT.md` 还在、索引不在时返回 `needs-decision` 或 `manual-split`。两段都去掉，不留半段。

由此接受的结果：从还含历史 `[split]` 的老版本升上来，并且 `.ai/PROJECT.md` 还在时，不再停下来问拆不拆。历史 split 仍按版本排在 v4 删除前面，但这个动作本身不写文件。队列一旦包含 4.0.0，后面的删除会删掉这个单文件。本轮不把这道停加回去。

对着本仓库做计划时版本号仍是 `3.6.0`，4.0.0 的删除不会入队。所以一个停在 1.7.0、带着 `.ai/PROJECT.md` 的临时项目，在本仓库上计划时文件还在，只是不再被旧检查拦住。要看到删除，得用版本写成 `4.0.0` 的临时 butler 根。

人读入口改成和这个行为一致：`tools/butler-upgrade/README.md`、`plugins/butler/skills/butler-upgrade/SKILL.md`、`Coder/20_Workflow_Lifecycle/butler-upgrade.md`。这三处现在写着 apply 必须带 `--split`，形状不对就停。改它们是让说明跟上已冻结的行为，不加新行为。`migration-schema.md` 的 `[split]` 定义不动。

### D4 · preference 从契约里卸掉

活字段只留 `schema_version`、`dangerous`、`independent_review`、`profiles`。默认值里不再有 `preference`。`tools/project-config/butler-config.schema.json` 的必填列表和属性一起拿掉这一键。

读的时候：文件里如果还有这一键，并且值是布尔，从返回值里丢掉，不报未知字段，也不改文件。值不是布尔则拒绝。别的未知字段仍然拒绝。这样版本号还是 `3.6.0` 时，已在当前版本的项目不会因为文件里留着旧键就被判成配置漂移。`plan_migration` 对已经存在的合法配置仍不主动重写。

写回只发生在目标为 `4.0.0` 的 `migrate_config` 上。那一次读原始 JSON，去掉 `preference`，其余三个字段的值保持原样，再按现有编码写回。文件里本来没有这一键，就不为它多写一次。没有配置文件时，沿用现在的 `plan_migration`：要创建才写成不含这一键的默认配置。

旧 Markdown 里的 `preference: on|off` 视为退役行：跳过，不抄进 JSON，也不把整份旧文件判成无法读取。别的无法识别的开关仍然拒绝。机器段的整段删除保持现在的做法。

`set` 如果重写这份 JSON，编码结果里也不会再有这一键。验收锁的是升级那一次。本轮不做「重写时故意把退役键留在磁盘上」。

人读文档不再写这个布尔还在。改这几处现在仍这么写的正文：`templates/rule-card.md`、`HUMAN_GUIDE.md`、`Coder/00_System_Prompt/logic-protocol.md`、`Coder/20_Workflow_Lifecycle/local-constraints-schema.md`、`Coder/20_Workflow_Lifecycle/mcv-deployment.md`、`tools/project-config/README.md`。`tools/project-config/tests/` 里把这一键当成活字段的断言跟着改。

不删 `tools/preference-experiment/`，不删 `templates/preference/`，不碰仓库外的偏好数据。全仓不得出现 `reorder_options` 或 `reorder_by_profile`。历史 `CHANGELOG.md` 和已发布配方里的旧句子不动。

### D5 · 临时回归怎么搭

行为测试仍用临时目录。证明 v4 配方时，临时 butler 根从本仓库拷出升级器真正会读的部分：`migrations/`、`templates/`、`scripts/render-project-entrypoints.py`、`tools/project-config/config.py`，再把这个根里的 `VERSION` 写成 `4.0.0`。动作使用这份拷贝里的真实清单，不另手写一套替代动作。执行的是本仓库的 `upgrade.py`，`--butler-root` 指向拷贝。

临时项目和这个根并排放，不能放进根里面，否则会触发「拒绝升级 butler 自己」。项目戳在 `3.6.0`，入口带用户区原文。有带文件的 `.ai/project/`、有 `.ai/PROJECT.md`、仓根有 `deliveries/`。快乐路径没有旧收件箱，也没有 `origin/`。

跑完之后：那两个路径消失，`deliveries/` 的内容在 `.ai/deliveries/` 且字节不变，源路径消失，用户区原文还在，版本戳是 `4.0.0`，hook 与这份临时根的配方来源一致。再跑一次，退出码 0，不另造一份。断言没有调用 `scripts/setup.sh`。本机插件目录不作为写入目标；需要家目录时用临时家目录。

`scripts/test-butler-upgrade.py` 里这两条改写，不删掉测试文件：`test_release_has_no_v4_recipe` 改成锁住配方内容和「对本仓库做计划时没有 `4.0.0/` 动作」。`test_apply_without_split_is_still_refused` 改成缺参数不再被拒绝，`defer` 和 `now` 仍被接受。形状检查的旧断言改成不再因为部分成形的 `.ai/project/` 停下。历史 split 加 `.ai/PROJECT.md` 的那条，改成锁住 D3 里接受的结果，不把旧的 `needs-decision` 加回去。

### D6 · debt.md 只改被还清的句子

`.ai/debt.md` 里旧收件箱和 `origin/` 那一条：删掉「还没有 `migrations/v4.0.0.md`」，也删掉「升级不会碰这两处」。留下人还得自己处理它们，因为配方是停下，不是删掉。

「从未在真实已部署项目上跑过」留下。这一条里「R15 计划补这次回归」改成仍欠着，本轮只在临时项目上证明配方。不把这条账删掉。其余长期约束不动。不处理收件箱里那两条旧缺陷。

### 执行顺序

- [ ] T1 写入 `migrations/v4.0.0.md` 和清单里 3.6.0 到 4.0.0 那一节，动作顺序按 D1。不改 `VERSION`，不改已发布配方，不动 `[split]` 定义 → AC1 AC2
- [ ] T2 在 `build_plan` 加上 D2 的门，并删掉形状检查整段。`--split` 改为可带可不带。三处人读入口改成和这个行为一致 → AC4 AC5 AC6
- [ ] T3 从字段表、默认值、schema、规则卡和 D4 点名的人读文档卸掉 `preference`。`migrate_config` 只在目标 4.0.0 时写回去掉这一键。旧 Markdown 的退役行跳过 → AC7
- [ ] T4 按 D6 改 `.ai/debt.md` → AC8
- [ ] T5 在 `scripts/test-butler-upgrade.py` 和 `tools/project-config/tests/` 补上临时回归，并改写会挡住新行为的旧断言 → AC1 AC3 AC4 AC5 AC6 AC7
- [ ] T6 跑 `python3 scripts/test-butler-upgrade.py`。完整的持续集成和审计留到验收阶段核对 AC9 → AC9

### Plan Admission

- **AC Coverage**：AC1 由 T1 和 T5 覆盖。AC2 由 T1 覆盖。AC3、AC4、AC5、AC6 由 T2 和 T5 覆盖。AC7 由 T3 和 T5 覆盖。AC8 由 T4 覆盖。AC9 由 T6 和验收阶段的三条命令覆盖。
- **Assumptions**：临时拷贝足以让渲染器、hook 来源和配置工具从 `--butler-root` 读到真实文件。`apply` 不会调用 `global_install`，所以不跑 `scripts/setup.sh` 就能满足 AC3 的机器侧观察。现有删除和移动的起始态足以表达 deliveries 两边都在时停下。
- **Alternatives / Trade-offs**：放弃新造「在则冲突」动作类型，因为前置条件必须和动作表逐字匹配，而这道门是整次计划停、不是一条文件变更。放弃在 `plan_migration` 里无条件重写旧键，因为版本号还是 `3.6.0` 时，那会把已在当前版本的项目判成配置漂移。放弃保留形状检查的一半，因为用户冻结时没有要求留下「有待拆单文件就停」。
- **Failure Modes**：旧收件箱或 `origin/` 命中时退出码 2，零写入。deliveries 两边都在时退出码 2，两边都不改。符号链接不跟随。`preference` 的值不是布尔时拒绝，不写出半份配置。
- **Impact / Scope Challenge**：不改 `VERSION`，不写发布说明，不打标签，不提交，不收口里程碑。不在未点名的真实项目上执行升级，也不升级 butler 仓自己。不改 loop，不加排序器，不删仓库外偏好数据和 `templates/preference/` 骨架。不重开 ITER-0123、ITER-0124、ITER-0125。
- **Verification Blind Spots**：幂等的移动不核对目标里的字节是否等于当初搬过去的内容。临时回归还清不了「从未在真实已部署项目上跑过」。历史 split 排在删除前面且不再拦截，是这次接受的结果，不是另一套拆分行为。
- **Verdict**：pass。用户在 2026-10-21 说「开始把」。没有必须先改的设计缺陷。

## Failure Paths

- 清单链断、配方文件缺失、动作编号或前置条件不对：校验失败，不执行。
- 用本仓库当 butler 根、项目戳在 `3.6.0`：计划里没有 `4.0.0/` 动作。这条配方不跑。
- 旧收件箱带 `butler-inbox:managed`，或仓根 `origin/` 存在，或这两处是符号链接：退出码 2，相关路径和另外三处都不改。
- 新格式闪念口没有旧标记：升级不停，该文件字节不变。
- 仓根 `deliveries/` 和 `.ai/deliveries/` 都在：退出码 2，两边都不改，不覆盖。整次计划在写入前停下。
- `.ai/project/` 或 `.ai/PROJECT.md` 已经不在：删除视为完成。源已经不在且 `.ai/deliveries/` 已经在：移动视为完成，不另造一份。
- `preference` 不是布尔，或配置里有别的未知字段：拒绝，不写回。没有这一键的配置仍能读。
- `apply` 不带 `--split`：不因为缺参数被拒绝。带 `defer` 或 `now`：参数仍被接受。只有半成形的 `.ai/project/` 时，不因为形状检查停下。

## Test Strategy

本轮不声明 TDD cycle。没有先失败再通过的配对。

`scripts/test-butler-upgrade.py` 用临时目录覆盖 AC1、AC3、AC4、AC5、AC6。临时 butler 根的版本写成 `4.0.0`，动作用清单里那一节真实动作。项目与这个根并排。断言用户区原文、搬家后的字节、第二次退出码 0，以及没有调用 `scripts/setup.sh`。对本仓库的计划断言没有 `4.0.0/` 动作，`VERSION` 仍是 `3.6.0`。

AC7 同时覆盖配置测试和这条临时升级：升级后 JSON 只少 `preference`，另外三个字段值不变；没有这一键的配置仍能读；实验工具目录还在；全仓检索不到 `reorder_options` 和 `reorder_by_profile`。

AC8 读 `.ai/debt.md`，确认那两句假话不在，人还得处理旧收件箱和 `origin/` 的句子还在，真实项目那条账还在。

验收阶段另跑 `bash scripts/verify-ci.sh` 和 `python3 scripts/audit-project-state.py --project-root . --allow-unreleased`，后者输出里不得有 `[DRIFT]`。

## References Compliance

- N/A
