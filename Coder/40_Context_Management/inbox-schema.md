---
title: 需求收件箱数据契约
audience: AI / 开发者
scope: origin/、对话与外部文档进入需求收件箱时的稳定来源身份、SHA-256 双指纹、封闭处理状态、幂等/变化检测、多对多派生关系、隐私和 origin 零写入边界；只定数据形态，扫描分类路由行为由后续动作层负责
---

# inbox-schema（需求收件箱数据契约）

`.ai/INBOX.md` 是需求材料的**处理回执**：回答“看见了什么、处理到哪、派生去哪”。它不是原文仓库、PRD、任务台账或历史日志；完整内容仍由 `origin/`、对话或外部系统持有。

## 1. 输入来源与所有权

支持三类来源：

| kind | locator | 内容真源 |
|---|---|---|
| `origin-file` | 相对项目根的 `origin/<path>` | 用户管理的原始文件 |
| `conversation` | 宿主可回溯的会话 / turn 标识 | 用户对话原文 |
| `external-document` | 稳定 URL、文档 ID，能取得时附 revision | 外部文档系统 |

`origin/` 是可选输入通道，不是必经流程。AI 对其中内容**永远只读**：不得新增、改写、格式化、重命名、移动、归档或删除。扫描产生的 hash、状态和关系只写 `.ai/INBOX.md`；用户清理 `origin/` 不授权 AI 替他恢复或搬家。

## 2. `.ai/INBOX.md` 最小结构

文件含两张表，不复制整份原文。

两张表位于唯一 `<!-- butler-inbox:managed:start -->` / `<!-- butler-inbox:managed:end -->` 管理块内，由驻留 scanner 原子维护；块外是用户注释区，工具逐字保留。首次无 marker 时追加管理块；单边、逆序或重复 marker、表头漂移一律 fail-closed 且零写入。Markdown 是单一真源，不另建 JSON sidecar。

### 2.1 Sources

| 字段 | 含义 |
|---|---|
| `source_id` | `SRC-NNNN`，项目内单调递增、永不复用的来源身份 |
| `kind` | `origin-file` / `conversation` / `external-document` |
| `locator` | §1 定义的稳定定位；敏感 query/token 必须脱敏 |
| `source_revision` | 外部系统可变 revision / etag；文件和对话无则 `—`，不得拼进稳定 locator |
| `observed_sha256` | 本次观察内容的 `sha256:<64 lowercase hex>` |
| `processed_sha256` | 最近一次成功 routed/ignored 的内容指纹；从未完成则 `—` |
| `observed_at` | 最近观察时间，ISO 8601 带时区 |
| `status` | §4 封闭枚举 |
| `classification` | §5 分类枚举；未分析为 `—` |
| `proposed_route` | 待确认的动作指针；没有为 `—` |
| `actual_route` | 已完成的动作摘要；未完成为 `—` |
| `summary` | 一句脱敏摘要，只为识别，不代替原文 |
| `note` | 失败/忽略/冲突原因；无则 `—` |

### 2.2 Derivations

| 字段 | 含义 |
|---|---|
| `source_id` | 指向 Sources 中的稳定来源 |
| `artifact_kind` | `prd` / `milestone` / `milestone-backlog` / `ideation` / `reference` / `record-only` |
| `artifact_ref` | `prd_id`、`MILE-NNNN`、候办键或项目内相对路径 |
| `relation` | `created` / `updated` / `supports` / `duplicate-of` / `ignored-as` |
| `recorded_at` | 关系确认时间，ISO 8601 带时区 |

一份来源可有多行关系；一个 artifact 也可被多个 source_id 支撑。不得把多对多关系压成 Sources 的逗号列表。关系行只在实际动作成功后写入；提议阶段只写 `proposed_route`。

## 3. 稳定来源身份与指纹

### 3.1 `source_id` 不等于内容 hash

- 首次登记领取正式表最大号 +1 的 `SRC-NNNN`；四位只是最小显示宽度，超过 9999 正常增长。
- `source_id` 永不因内容、标题、文件名或外部 revision 变化而改变，也不回收。
- 同一 locator 的内容变化仍是同一来源；同一内容从不同 locator 进入仍是两个来源，最多标记重复候选。
- locator 的展示变化只有在能证明来源身份连续时才更新原行并记 note；无法证明时新建来源，不擅自认亲。

### 3.2 SHA-256 输入

- `origin-file`：对磁盘文件**原始字节**计算 SHA-256；不得用 mtime、大小、路径或换行转换后的文本冒充。
- `conversation`：取用户选定 turn 的 UTF-8 文本，只把 `CRLF` / `CR` 规范成 `LF`；不 trim、不 case-fold、不改 Unicode、不拼入模型回复。
- `external-document`：优先对 API 返回的确定性原始正文 bytes 计算；只能取得文本时，按 conversation 的最小换行规范化后编码 UTF-8。稳定文档 ID / URL 写 locator，可变 revision / etag 只写 `source_revision`，不代替内容 hash。
- 空内容也有合法 SHA-256，但动作层必须将其标为 failed 或等待确认，不能把空内容路由成需求。

保存 `observed_sha256` 与 `processed_sha256` 两个值：前者回答现在看见什么，后者回答上次成功处理的是什么。失败、仅分析或等待确认时不得推进 `processed_sha256`。

## 4. 封闭状态与转移

合法状态只有：

`unprocessed` / `analyzed` / `awaiting-confirmation` / `routed` / `ignored` / `source-changed` / `failed`

| 当前事实 | 合法状态 / 转移 |
|---|---|
| 首次登记 | `unprocessed` |
| 已产出分类与建议，尚无需/未进入确认 | `unprocessed → analyzed` |
| 路由或身份选择待确认 | `analyzed → awaiting-confirmation` |
| 实际动作成功且关系已写 | `analyzed|awaiting-confirmation → routed`，同时推进 processed hash |
| 明确决定无需推进并记录原因 | `analyzed|awaiting-confirmation → ignored`，同时推进 processed hash |
| 同 locator 的 observed 与 processed 不同 | `routed|ignored → source-changed`，processed 保留旧值 |
| 任一步失败 | 当前非终态 → `failed`；记录原因，processed 不推进 |
| 失败重试或 changed 重新分析 | `failed|source-changed → analyzed`，成功后再 routed/ignored |

`routed` 只表示登记内容对应的实际动作成功，不表示派生迭代或里程碑已完成。`ignored` 和 `failed` 绝不能伪装成 routed；`source-changed` 绝不能靠更新 observed hash 后静默恢复 routed。

## 5. 分类与路线字段

`classification` 封闭枚举：

- `new-requirement`
- `existing-requirement-version`
- `supplemental-material`
- `fuzzy-idea`
- `milestone-direction`
- `record-only`
- `duplicate-candidate`
- `ambiguous`

分类不是动作。`proposed_route` 可以指向 PRD 首切、PRD 更新、ideation、milestone 候办或仅记录；`actual_route` 和 Derivations 只在动作成功后回填。`ambiguous` / `duplicate-candidate` 必须等待确认或记录忽略原因，不能自动合并来源或覆盖 artifact。

## 6. 幂等与变化检测

扫描 / 更新动作必须守：

1. **同 locator + 同 observed hash**：更新 `observed_at` 和可用的 `source_revision` 即可，不新建 source、不重复路由、不重复关系行。
2. **同 locator + hash 变化**：保留 source_id，写新 observed hash；若已有 processed hash，置 `source-changed`，不覆盖旧 processed hash。
3. **不同 locator + 同 hash**：分别登记 source_id，标 `duplicate-candidate` 或关系 `duplicate-of` 候选；确认前绝不自动合并。
4. **同一关系重复回放**：`source_id + artifact_kind + artifact_ref + relation` 相同即幂等，不追加重复行。
5. **动作失败**：状态 `failed`，不得写成功关系、actual route 或推进 processed hash。

文件重命名若没有持久文件 ID，单靠新旧路径与相同 hash 只能提“可能同源”候选；不得自动把旧 locator 改成新 locator。

## 7. 隐私、体量与路径边界

- `.ai/INBOX.md` 不存完整原文、长摘录、认证信息、cookie、token、URL 敏感 query 或外部响应 headers。
- summary 只写识别所需一句话；精确规格应进入 PRD/reference 派生产物并由 Derivations 指针连接。
- locator 必须是项目内相对路径或经脱敏的外部标识；`origin-file` 解析后必须仍在唯一 PROJECT_ROOT 的 `origin/` 下，符号链接逃逸 fail-closed。
- 删除/不可达来源不删除 ledger 行；记录 note 并保持历史关系。INBOX 是回执，不能因源暂时消失就改写已经发生的派生事实。

## 8. 动作边界

- R3（本文件）只定数据合同。
- MILE-0009 R4 实现 `/butler:inbox` 扫描、分类、确认和路由，并用 fixture 证明 §4/§6。
- R5/R6 消费 source↔PRD/MILESTONE 指针；R7 的 PRD 更新 receipt 可回指 source_id，但不复制 INBOX 状态机。

在 R4 交付前，不得仅凭本文件宣称收件箱已经能自动扫描或路由。
