# TECH_PLAN — ITER-0059 · 可执行升级器

> ⚠️ 危险模式：本产物由模型自主 ACK（已过 `dangerous-engine.md §5.2` 自审门），未经用户逐项确认（ITER-0059，2026-07-18）。

## Goal

- 用结构化、可校验、无第三方运行时依赖的升级链兑现 AC1–AC9。
- 保留现有 renderer 和 MCV 项目根解析为底层真源，不复制入口渲染或项目根算法。
- 将项目内事务、人工决定和机器级外部动作拆成三个明确执行域。

## Files / Modules to Change

- **ADD `migrations/manifest.json`**：中心机器台账；登记 schema 版本、支持基线、每个发布区间和有限 action 列表。
- **ADD `tools/butler-upgrade/upgrade.py`**：标准库 CLI 与执行内核，提供 `inspect`、`plan`、`apply`、`global-install` 子命令和 JSON/human 输出。
- **ADD `tools/butler-upgrade/README.md`**：命令、状态码、运行区、恢复和动作域真源。
- **ADD `scripts/test-butler-upgrade.py`**：manifest 负向校验、历史 fixture、事务/锁/越界/故障注入 E2E。
- **EDIT `scripts/render-project-entrypoints.py`**：只补可复用的纯 plan/字节接口和自目标拒绝所需边界；现有 CLI 行为保持兼容。
- **EDIT `scripts/verify-dual-host.sh`**：把升级器专项纳入单一 CI/local 矩阵。
- **EDIT `Coder/20_Workflow_Lifecycle/butler-upgrade.md`、`migration-schema.md`、`mcv-deployment.md`**：切换到程序执行真源，保留人工决策语义和人读配方责任。
- **EDIT `.claude/commands/butler/upgrade.md`、`plugins/butler/skills/butler-upgrade/SKILL.md`**：两宿主薄壳只调用同一 CLI。
- **EDIT `README.md`、`HUMAN_GUIDE.md`、`docs/codex-compatibility.md`**：登记操作者用法和边界。
- **EDIT `migrations/v2.13.0.md`、`v2.14.0.md`、`v2.6.0.md`**：补齐人读 schema 章节/标准标签；只校正结构，不改变历史动作意图。

## Interface / Contract

### 1. 机器台账

`manifest.json` 顶层：

- `schema_version: 1`
- `baseline_version: "1.0.0"`
- `migrations: []`，按 target semver 严格升序。

每个 migration：`source`、`target`、`recipe`、`actions`。相邻记录必须 `previous.target == next.source`，recipe 必须存在且文件名等于 target。

每个 action：

- `id`：全台账唯一、稳定，格式 `<target>/<ordinal>-<slug>`。
- `type`：`regen_entrypoints | sync_hooks | rename | add_field | restamp | no_op | split | global_install`。
- `domain`：`project | decision | machine`，由 action schema 固定，不允许随记录伪装。
- 类型参数：rename 的 `from/to`、add_field 的 `path/section/key/value`；其余只接受白名单字段。

历史 `[regen-claude]`、`[global-install-rerun]` 只在 Markdown 兼容说明出现，manifest 统一归一为现代类型。

### 2. CLI

```text
python3 tools/butler-upgrade/upgrade.py inspect --project-root PATH [--json]
python3 tools/butler-upgrade/upgrade.py plan --project-root PATH [--split defer|now] [--json]
python3 tools/butler-upgrade/upgrade.py apply --project-root PATH --split defer|now [--json]
python3 tools/butler-upgrade/upgrade.py global-install --project-root PATH --confirm [--json]
```

- `inspect`/`plan` 永远零写入；未提供 split 决定时计划仍完整输出，但退出 `needs-decision`。
- `apply` 必须显式给 split 决定；`defer` 继续机械动作，`now` 在检测到真实单文件待拆时返回人工交接，不写项目。
- `global-install` 是独立命令，要求 `--confirm`，只运行 installer 并报告自身结果，不改变项目 journal 的 fully-complete 结论。
- 稳定退出码：0 success/already-current；2 invalid/conflict；3 needs-decision/manual；4 locked；5 apply-failed-restored；6 external-action-failed。
- JSON 固定包含 `status`、`project_root`、`from_version`、`to_version`、`actions`、`changes`、`conflicts`、`external_pending`、`run_id`（适用时）。

### 3. 计划与项目事务

- 项目根先 `resolve()`，拒绝等于/位于 Butler 根、非目录、不可写和软链越界。
- 从 CLAUDE.md/AGENTS.md 管理区读取唯一且一致版本戳；单入口旧项目允许从 CLAUDE 戳建立队列，renderer 在最终动作补 AGENTS。
- 收集 `from < target <= VERSION` 的记录，展开 actions；重复最终态写合并为一个目标文件 PlannedWrite，但每个 action ID 都在 journal 留状态。
- 全量 preflight 生成内存中的最终文件映射并检查所有冲突，成功前不创建运行目录或 lock。
- apply 使用目标 `.ai/butler-upgrade/runs/<run-id>/`：`journal.json`、`restore.json`、`backup/`。恢复 manifest 记录相对路径、存在性、mode、before/after SHA-256。
- lock 为 `.ai/butler-upgrade/apply.lock` 的排他创建；旧锁不自动删除，只报告 owner/run 信息。
- 备份和目标临时文件全部落同一文件系统；逐文件 `os.replace`。故障时按 restore manifest 逆序恢复，恢复成功才返回 5；恢复失败同时保留 journal 并报最高风险诊断。
- 不调用 git reset/checkout，不碰未登记文件；运行区自身不纳入恢复文件集合。

### 4. 动作实现

- `regen_entrypoints/restamp`：复用 renderer 的 `plan()`，一次生成当前 VERSION 的双入口最终态；保护管理区外和各自 user-managed 内容。
- `sync_hooks`：以当前 `templates/hooks/`（除 tests/cache）为真源，目标存在时只接受 manifest 登记的历史受管 tree digest 或当前 digest；额外/漂移受管文件冲突。settings 用纯函数按 matcher+入口名幂等合并，只追加 Butler 自己的两条，不改其他条目。
- `rename`：只允许 project-relative、白名单前缀路径；旧存在且新不存在才计划 rename，二者都不存在视已完成，二者同时存在冲突。
- `add_field`：只对 manifest 指定 Markdown 段落/key/default 做窄编辑；已有同 key 同值跳过，异值视用户选择并保留，不覆盖。
- `split`：decision 域；无 PROJECT.md 或已有完整 project/00_INDEX 视已决定/已迁；部分成形冲突；真实待拆按 defer/now 路由。
- `global_install`：machine 域，仅登记 pending；项目 apply 永不执行。

## State / Boundary

- manifest 是执行数据真源；Markdown migration 是人读发布说明，CI 只校验一一覆盖和结构，不从正文派生 action。
- journal 是单次执行事实，不是版本台账；历史 run 不自动删除，用户可审计后自行清理。
- 项目事务只承诺 manifest 登记路径；HOME/global install、语义 split 和用户仓库 git 状态不在原子边界。
- 无戳项目返回 manual-bootstrap；本轮不自动猜旧内容归属。
- 当前工作树含 R1–R3 未提交改动；进入 P4 前建隔离分支 checkpoint，R4 修改继续在同分支追加，不改写历史 commit。
- Active Profiles：无；`.ai/local-constraints.md` 只启用 dangerous，自审/审计/强审和 checkpoint 护栏必须完整执行。

## Design Decisions

- **中心 JSON 而非逐 Markdown 解析或 YAML**：标准库可严格读写，单文件能机械检查全链连续性和唯一 ID；代价是发布时需同时维护人读 recipe，CI 覆盖检查负责防漏。
- **有限 action 联合而非通用脚本语言**：每类动作有确定 schema、路径和冲突语义，未来新增类型必须改代码与测试；牺牲任意性换审计性。
- **最终态合并写，不逐版本落中间态**：历史队列仍逐 action 记录，但入口/hook 只写当前仓最终态，避免 renderer 使用当前 VERSION 却伪造中间版本；最终结果与连续逐版的幂等语义等价。
- **preflight 在运行区创建前完成**：满足冲突零写入；只有真正 apply 才生成 lock/backup/journal。
- **global install 独立子命令**：HOME 无法与目标项目原子回滚，强行合并会产生虚假事务承诺。
- **split 的 now 诚实交接**：任意知识文本无法可靠机械路由；程序负责阻塞、记录、续跑边界，不用粗暴按标题切分冒充语义迁移。

## Execution Steps

- [ ] **T1** 写 manifest schema/覆盖负向测试与历史动作清单，再落 `migrations/manifest.json` → AC1
- [ ] **T2** 实现 inspect/plan、版本/marker/root/symlink 检查和稳定 JSON/exit contract → AC2、AC3
- [ ] **T3** 实现纯动作计划器、renderer 复用、hook/settings/rename/add-field/split/global 域 → AC5、AC6
- [ ] **T4** 实现 lock、backup/journal、原子 apply、故障注入恢复和 rerun → AC4、AC5
- [ ] **T5** 建 v1.x/v2.0/v2.14/v2.15/current fixture 与冲突/并发/恢复 E2E → AC2–AC7
- [ ] **T6** 修正历史 recipe 结构，接线 Claude/Codex 薄壳、规则与人类文档 → AC1、AC8
- [ ] **T7** 接入完整 CI，捕获 evidence、执行危险模式全维审查并修到 0 Must Fix → AC9

## Verification Plan

- manifest：正常全链；删除/重复/断链/坏 domain/未知字段/未知 action/缺 recipe 均失败。
- plan：每个历史基线输出黄金 JSON 关键字段；前后递归摘要相同；无戳/前向/双戳不一/marker 异常诊断稳定。
- security：self-target、path traversal、绝对路径、外指 symlink、extra hook、部分 split、目标冲突全部首写前拒绝。
- transaction：逐写点故障注入，文件集合/bytes/mode 恢复；双进程锁仅一方成功；旧锁不偷删。
- idempotence：fixture 首次 apply 后第二次零内容 diff；入口区外和 user-managed 逐字节一致。
- host/docs：官方 Codex validator、Claude/Codex workflow checks、Markdown link checker、完整 `verify-ci.sh`。
- evidence：专项、负向风险复现、完整矩阵、diff-check、state audit 全由 evidence runner 捕获，VERIFY 逐 AC 引用。

## Risks / Open Questions

- 历史 hook 的合法旧 digest 需要从已发布 tag 机械提取并固化到 manifest 或测试数据；若某 tag 不含完整 hook 树，计划器应按版本明确“无已知受管副本”，不能宽放任意内容。
- settings.json 是用户共享配置；只允许纯函数追加缺失 Butler 条目，JSON 非对象/字段类型异常必须冲突，格式变化要保持最小。
- apply 进程被 `SIGKILL` 无法在当下自动恢复；下次 inspect 必须识别 incomplete journal 并阻止新 apply，给出显式恢复指引。本轮若实现自动 resume/restore 会扩大接口，优先保证检测与 fail-closed。
- 当前无设计阻塞；影响面均在 AC 已冻结范围内。
