---
title: PRD 首切机制
audience: AI / 开发者
scope: 把一份首次进入项目的独立权威 PRD，经身份四态判定、日期化 prd_id、模块边界与 Workspace Scope soft 对齐后，无损切入 references/prd/<prd_id>/；只管首切，不管已有需求改版
---

# prd-split（PRD 首切机制）

本文件是 PRD 需求集合的**首切动作层**。结构、身份与无损红线以 `references-schema.md` 为真源；工作区四类范围以 `workspace-scope-schema.md` 为真源。已有需求改版走 `prd-update.md`，只读查询走 `prd-status.md`。

## 1. 入口先判身份，零写盘

拿到 PRD 后，先按 `references-schema §5` 的证据顺序检查项目级索引、迁移/更新回执及稳定来源锚点，产出且只产出以下四态之一：

| 结果 | 本动作的处置 |
|---|---|
| `new-requirement` | 进入 §2–§6 的首切提案 |
| `new-version` | 保持唯一既有 `prd_id`，路由 `prd-update.md`；本动作零写 |
| `duplicate` | 不新建、不 bump，只向调用方返回既有 `prd_id` 与重复证据 |
| `ambiguous` | 列候选与冲突并停止，等待明确身份；本动作零写 |

不得先切模块再补身份，也不得用标题、文件名、相似关键词或“默认新建”越过此闸。项目仍是 legacy 单 PRD 时，先按 R5 迁移指南显式迁移，不得把第二份需求写进 legacy 根。

## 2. 日期化 `prd_id`

只有 `new-requirement` 可提议新身份。`prd_id` 必须是 `YYYY-MM-DD-<requirement-slug>`，并同时满足：

- 日期来自可审计的“此独立需求首次进入当前项目 Butler 体系”的证据；闪念口 `.ai/INBOX.md` 里去向指向本需求的那条闪念，它的「记于」日期优先；其次是用户明确给出的项目本地日期。
- 不得用当前日期、文件 mtime、PRD 发布日、改版日或模型推断替代。证据不足就停止并索要日期。
- slug 表达整份需求语义，不用 module slug、版本号、随机串或纯序号；语法、合法日期和同日冲突按 `references-schema §4` 校验。
- 项目级索引、目录与来源关系出现身份冲突时 fail-closed；登记后标题变化不改 ID。

## 3. 模块边界与无损切片

按 PRD 自身的章节、功能模块或修改项分组切，不自造业务边界。一个自然单元对应一个 `module_slug`；完整规则、校验、字段约束或精确文案不得拦腰拆散。拿不准时宁可切粗。

`<prd_id>/<module_slug>.md` 正文必须逐字搬运对应原文，不概括、不润色、不补写。`00_INDEX.md` 只是导航，可写摘要。小 PRD 不退回单文件态：仍创建自己的 `<prd_id>/`，只含一个模块。

## 4. 一次 soft 对齐

任何写盘前，一次性呈交并确认：

1. 身份判断及证据、拟用 `prd_id` 与首次进入日期依据；
2. 模块清单、每个 `module_slug`、原文边界及未切碎说明；
3. 需求级 `Workspace Scope` 四类集合；若模块需收窄，连同完整四类子集一起展示；
4. 项目级索引将新增的行、目标目录和初始版本。

Workspace key 必须来自 `.ai/project/workspaces.md` 的 active 行，四类互斥且模块只能收窄，细则不在此复述。标准模式等待用户确认；危险模式可按完整自审规则代 ACK，但仍不能自造日期证据或越过 ambiguous。

## 5. 确认后的落盘

预检全部通过后才落盘，写入面严格限定为：

```txt
.ai/references/prd/
  00_INDEX.md
  <prd_id>/
    00_INDEX.md
    <module_slug>.md
```

1. 在同父临时目录完整生成新的 `<prd_id>/`：单需求入口叙述、当前版本、来源指针、模块登记表、Workspace Scope 与逐字切片。
2. 对生成树复核 ID/版本、模块登记与文件一一对应、workspace 合同、原文 bytes/规范化文本无损。
3. 原子安装新的 `<prd_id>/`；目标已存在、是 symlink 或中途漂移则拒绝，不覆盖。
4. 最后以原子替换更新项目级 `prd/00_INDEX.md`，只新增该需求一行；保留其他 PRD 行和目录不动。若索引更新失败，移除本次尚未发布的目标目录并恢复原索引，不留下半登记需求。

项目级行字段和单需求索引字段只以 `references-schema §3` 为准。首切不创建 `.archive/` 快照；历史从第一次改版才开始冻结。

## 6. 里程碑并进与回执

由 milestone 的大 PRD 分类闸触发时，路线图与 §4 的首切提案合并呈交。新路线交叉指针写成：

```txt
→ prd: <prd_id>#<module_slug>
```

单需求入口只回指 owning milestone，不重复模块到路线的映射。非 milestone 首切省略该回指。本动作对用户原件只读，不改 `.ai/references/raw/` 里的任何文件。

## 7. 非回归与动作边界

- 不使用 PRD 的项目、扁平 `api-/design-/insight-` references 流程不变。
- 本动作不处理 update diff、先冻后更、认亲、影响面或 update receipt（R7）。
- 本动作不执行代码范围 hook 或 git diff 对账（R8）。
- 未确认/未自审通过、身份非 `new-requirement`、日期无证据、workspace map 异常或目标冲突时，必须零写盘。
