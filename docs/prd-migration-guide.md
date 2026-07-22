# 旧单 PRD 迁移到需求集合

这份指南给维护项目的人使用：把旧的 `.ai/references/prd/<module>.md` 搬进一个明确的日期化需求目录，同时保证冻结/已收口工作仍能按原版本回溯。迁移工具不会替你猜需求身份，也不会改历史 AC。

> 当前能力边界：本指南与迁移器只处理既有 legacy PRD 的结构和引用兼容。新 PRD 首切/status 的完整适配在 MILE-0009 R6，确定性 update 在 R7；未交付前不要把迁移成功等同于整条多 PRD 自动链路已经完成。

## 1. 迁移前盘点

先确认项目根和 Butler 仓：

```bash
export PROJECT_ROOT=/absolute/path/to/project
export BUTLER_PATH=/absolute/path/to/butler
python3 "$BUTLER_PATH/tools/prd-migrate/prd_migrate.py" inspect --project-root "$PROJECT_ROOT"
```

只有输出 `state=legacy` 才进入下一步。以下情况先停：

- `absent/empty`：没有可迁移的 legacy PRD；
- `collection`：已经是需求集合，不要重复迁移；
- `mixed/unknown`：根模块、日期化目录或未知文件混装，需要人工厘清；
- symlink / 非普通文件：工具会拒绝，先确认真实所有权和路径。

盘点并保留这些证据：旧 `prd/00_INDEX.md` 的当前版本、模块清单、`.archive/vN/`、原始来源/收件箱回执、首次进入本项目的日期证据，以及所有引用旧路径的 MILESTONE/AC/TECH_PLAN/VERIFY。

## 2. 确定日期化 `prd_id`

格式是 `YYYY-MM-DD-<requirement-slug>`。日期取这份独立需求**首次进入当前项目 Butler 体系**的项目本地日期，不是本次迁移日、文件 mtime、最近改版日或产品发布日期。

证据优先级建议：首次 PRD 切片提交/迭代记录 → `.ai/INBOX.md`/来源回执 → 可审计会话或文档接入记录。证据冲突就停下来确认；工具要求显式 `--prd-id`，不会猜。

slug 用小写 ASCII、数字和单短横线表达整份需求，例如 `2026-07-22-user-login`。不要塞版本号、模块名、随机串或纯序号。标题可以以后改，`prd_id` 一旦登记不再“修漂亮”。

## 3. 先看零写迁移计划

```bash
python3 "$BUTLER_PATH/tools/prd-migrate/prd_migrate.py" plan \
  --project-root "$PROJECT_ROOT" \
  --prd-id 2026-07-22-user-login \
  --title "用户登录"
```

plan 不写文件。逐项核对：

- `current_version` 是否等于旧索引；
- `legacy_tree_sha256` 和每个 mapping 是否覆盖 00_INDEX、全部 live 模块与所有 archive 文件；
- `impact` 是否列出使用 `references/prd/<slug>.md` 的 MILESTONE、当前/未来工作与 closed history；
- 一个 legacy 根是否确实只代表这一份需求。若实际混了多份需求，不能用一次迁移硬并，先人工拆清身份。

## 4. 处理 MILESTONE 与 AC 引用

迁移器只报告、不回写这些文件：

- **MILESTONE / 未开工**：迁移后新写法改为 `references/prd/<prd_id>/<module_slug>.md`；路线项仍由 MILESTONE 保存映射。
- **active / frozen**：不要直接改。确需切新路径或改变钉版时，按 amend 把 AC 退回 draft、重冻，再写 `prd_refs`。
- **closed**：永远不回写归档。旧 `prd_version + prd/<slug>.md` 由 migration receipt 和 resolver 解析到新目录的 live 或 archive。

新集合 AC 的 frontmatter 示例：

```yaml
prd_refs:
  - prd_id: 2026-07-22-user-login
    prd_version: v1.1
    module_slugs: [login-flow, validation-copy]
  - prd_id: 2026-07-23-batch-import
    prd_version: v2.0
    module_slugs: [import-rules]
```

`prd_refs` 与旧单值 `prd_version` 不得并存。P3/P5 继承这张表，不另写版本。

## 5. 执行事务迁移

确认 plan 后执行：

```bash
python3 "$BUTLER_PATH/tools/prd-migrate/prd_migrate.py" apply \
  --project-root "$PROJECT_ROOT" \
  --prd-id 2026-07-22-user-login \
  --title "用户登录"
```

工具先在 `.ai/references/` 同父目录建立 staging，复制原始 bytes 并计算 hash；预检完成后才把旧 `prd` 原子换到 `.prd-migration-backups/<migration_id>`，再把 staging 换成新 `prd`。第二步或迁移后自检失败会恢复旧根，不留下半套集合。

成功后会出现：

```text
.ai/references/prd/00_INDEX.md
.ai/references/prd/<prd_id>/00_INDEX.md
.ai/references/prd/<prd_id>/<module>.md
.ai/references/prd/<prd_id>/.archive/vN/...
.ai/references/prd/.butler-migration.json
.ai/references/.prd-migration-backups/<migration_id>/...
```

`origin/`、MILESTONE、当前四件套和 `.ai/iterations/` 不在写集。

## 6. 迁移后验证

```bash
python3 "$BUTLER_PATH/tools/prd-migrate/prd_migrate.py" verify --project-root "$PROJECT_ROOT"
python3 "$BUTLER_PATH/tools/prd-migrate/prd_migrate.py" resolve \
  --project-root "$PROJECT_ROOT" \
  --ac-file .ai/iterations/ITER-0001/AC_LIST.md \
  --ref prd/login-flow.md
```

verify 对账 collection tree、逐文件 mapping 和 backup hash。resolve 应把旧 closed AC 的隐式 PRD 身份补成新 `prd_id`；若旧 AC 钉的是历史版本，结果必须落 `<prd_id>/.archive/<prd_version>/<module>.md`，不能误读 live 最新。

再执行项目自己的完整验证和 `git diff --check`，人工检查：项目级索引只有需求列表；单需求索引/模块 bytes 未变；MILESTONE 与 active/future 引用已按决定处理；closed 归档 hash 未变。

backup 不自动删除。至少等 verify、项目 CI、提交审查和一次历史 resolver 抽查都通过后再决定清理；需要保守恢复窗口时可以长期保留。清理是单独的用户资产决定，不要让 AI 在迁移成功后顺手删除。

## 7. 失败恢复

apply 自己报错且输出未显示成功时，先重新 `inspect`，不要手工拼目录：

- `legacy`：事务已自动恢复，可修正输入后重跑 plan；
- `collection`：运行 verify；只有 verify 绿才算成功；
- `mixed/unknown`：停止写入，保留现场与 backup，请按 receipt/migration_id 人工审计。

若迁移成功后决定撤回：

```bash
python3 "$BUTLER_PATH/tools/prd-migrate/prd_migrate.py" rollback --project-root "$PROJECT_ROOT"
```

rollback 先重新验证当前 collection 和 backup hash；任何迁移后漂移都会拒绝，避免把新改动覆盖掉。要保留迁移后的新工作时，不要强行 rollback：先备份现场并人工决定如何合并。

## 8. 常见禁区

- 用“今天”代替首次进入日期；
- 因标题相似把两份需求并成一个 `prd_id`；
- 为迁移方便回写 frozen/closed AC；
- 手工移动 live 后才补 archive/receipt；
- verify 未过就删除 backup；
- 在 R6/R7 未交付前宣称 split/status/update 已全部支持多 PRD。
