---
title: PRD 状态查询机制
audience: AI / 开发者
scope: 多 PRD 集合与 legacy 单 PRD 的确定性只读状态查询；按 prd_id 下钻、按 workspace_key 筛选、稳定 JSON、零写入与坏布局 fail-closed
---

# prd-status（PRD 状态查询机制）

`prd-status` 是日常只读入口，只回答“项目有哪些需求、某份需求当前是什么状态、哪些需求触及某个工作区”。它不执行首切、迁移或改版；事实只从 `references-schema.md` 与 `workspace-scope-schema.md` 定义的落盘结构读取。

## 1. 调用

```bash
python3 "$BUTLER_PATH/tools/prd-status/prd_status.py" status --project-root "$PROJECT_ROOT" [--prd-id YYYY-MM-DD-slug] [--workspace workspace_key]
```

- 无筛选：按 `prd_id` 排序列出项目级需求，并附各自当前详情。
- `--prd-id`：只返回该需求的版本、状态、模块和四类 Workspace Scope。
- `--workspace`：返回四类范围中包含该稳定 key 的需求，并标出命中的类别；可与 `--prd-id` 组合。
- stdout 为稳定 JSON；exit 0 表示成功且有结果，1 表示合法查询无匹配，2 表示输入或项目合同错误。

## 2. 发现与交叉核验

collection 模式只以项目级 `prd/00_INDEX.md` 的需求表发现身份，再逐行检查：

- `prd_id` 语法/日期合法、无重复，入口恰为 `<prd_id>/00_INDEX.md`；
- 目标目录真实存在且不是 symlink，目录名、单需求入口中的 ID 与项目行一致；
- 项目行当前版本/状态与单需求入口一致；
- 模块登记无重复，live 文件与 active 模块一一对应，同名 module slug 只在各自 `prd_id` 内比较；
- Workspace Scope 四类齐全、互斥；每个键必须在 `.ai/project/workspaces.md` 唯一登记且为 `active`，缺地图、重复键、retired/未知键均拒绝。

目录中出现未登记的日期化需求、索引登记缺目录、混合 legacy 根切片、symlink、坏日期、重复 ID/模块或字段漂移均 fail-closed。不得把“扫到一个像 PRD 的目录”静默升级为索引事实。

## 3. legacy 只读退化

legacy 单 PRD 根仍可列出当前版本和根级模块，返回 `layout: legacy`、`prd_id: null`、空 Workspace Scope，并明确 `migration_required: true`。它没有显式身份，因此：

- 不接受 `--prd-id` 假装下钻；
- `--workspace` 合法但无匹配，exit 1；
- 不创建 ID、索引、receipt 或范围；需要集合能力时走 R5 迁移指南。

collection 与 legacy 信号并存属于混合布局，exit 2。

## 4. 零写与输出边界

status 不创建缓存、lock、receipt、临时文件或缺失目录；成功、无匹配和错误三条路径都不得改变项目树。它不依赖对话中的最近一次 update。R7 更新回执落地后可作为附加只读字段接入，但不得取代 PRD 索引和模块事实。

JSON 顶层至少包含 `schema_version`、`layout`、`filters`、`requirements`；每份 collection 需求至少含 `prd_id`、`title`、`current_version`、`status`、`entry`、`workspace_scope`、`workspace_matches`、`modules` 与 `latest_update`。没有更新回执时后者为 `null`；有时只读投影最近 receipt 的版本、模块变化、三态影响与 dispositions，receipt 畸形即 fail-closed。数组按稳定键排序，未知字段不得凭模型补值。

## 5. 双宿主边界

`/butler:prd status` 与 `$butler-prd` status 都只负责解析参数、解析唯一 `PROJECT_ROOT`/`$BUTLER_PATH` 并调用上述工具；不得在宿主命令里重写解析算法。人类摘要可以从 JSON 转述，但 exit code、错误与 legacy 限制必须原样亮出。
