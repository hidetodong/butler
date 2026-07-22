# ITER-0080 · 首切、状态与命令适配

## Problem

- `prd-split` 仍把模块直接写到 `references/prd/` 根，第二份需求会与第一份需求混合。
- 首切未先执行新需求/新版/重复/歧义四态身份判断，可能为同一需求另造日期目录或猜首次进入日期。
- `/butler:prd status` 仍是单 PRD 散文看板，无法稳定列出多份需求，也不能按 `prd_id` 或 workspace 下钻。
- milestone 路线指针只写 module slug；不同需求使用同名 slug 时无法唯一定位。

## Goal

- 让新需求按日期化 `prd_id` 安全首切，并提供确定性、零写入、可筛选的多 PRD 状态查询及双宿主入口。

## In Scope

- 首切身份四态、显式日期证据、模块方案与 Workspace Scope 一次 soft 对齐。
- 项目级索引和 `<prd_id>/00_INDEX.md`/模块切片的职责与写入顺序。
- 标准库 status CLI：全项目列表、`prd_id` 下钻、workspace 筛选和 legacy 只读兼容。
- milestone 指针升级为 `prd_id#module_slug`；Claude command、Codex skill、registry 投影同步。
- 临时项目 fixture 验证多需求、同名模块、筛选、零写与坏输入拒绝。

## Out of Scope

- 不实现 R7 的 update diff、归档事务、影响面处置和更新 receipt。
- 不实现 R8 的实际代码改动范围门禁，不写外部 apps 项目。
- 不自动猜首次进入日期，不在 duplicate/ambiguous/new-version 状态创建新目录。
- 不回写历史 closed milestone 或 iteration 指针。

## Key Decisions

- 身份判断先于切片设计和任何写盘；只有 `new-requirement` 可进入首切。
- 首切确认把 `prd_id`、模块 slug/边界、需求级 Workspace Scope 合并为一次提案，减少半确认状态。
- status 使用独立标准库只读 CLI，输出稳定 JSON；不复用会改变状态的 migration/update 路径。
- 新 milestone 指针采用 `<prd_id>#<module_slug>`，既紧凑又能唯一定位；旧 slug-only 仅历史兼容读取。

## Risks

- Markdown 索引存在格式变体；status 仅接受合同形态并对混合/重复/不完整数据 fail-closed。
- workspace path 会变化，因此筛选按稳定 workspace key，不把物理路径当需求身份。
