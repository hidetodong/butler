---
title: 参考资料子系统格式契约
audience: AI / 开发者
scope: .ai/references/ 子系统的结构定义——扁平参考资料与 PRD 需求集合；项目级需求索引、日期化稳定 prd_id、单需求模块索引、无损切片、独立版本历史及 legacy 单 PRD 兼容边界
---

# references-schema（.ai/references/ 子系统格式契约）

本文件是 `.ai/references/` 的结构与身份契约。参考资料**怎么注入**由 `00_System_Prompt/logic-protocol.md` 负责；哪些 AC / 方案 / 验证结论引用了资料，由对应阶段 schema 负责。本文件只回答：资料落盘后长什么样、PRD 集合中的“这份需求是谁”如何保持稳定、该怎么读。

> MILE-0009 已把需求集合、多 PRD 钉版、legacy 显式迁移、首切/status、确定性改版与工作区范围门禁接成完整执行链；各动作仍只以本文件及其指向的专项 schema 为真源。

## 1. 定位

`.ai/references/` 是**外部资料的落盘区**：项目之外的东西，不管是用户丢进来的原件还是 AI 处理过的投影，都住这里，供后续阶段按指针引用。

它下面并存两类东西，**保真度和权威性都不同，靠目录分开**：

| 子区 | 存什么 | 谁写 | 权威性 |
|---|---|---|---|
| `raw/` | 用户自己的原始材料，自由格式、任意命名 | **只有用户**。AI 只读、不写不改不重命名不移动不归档不删除 | **非权威**。是输入，不是规格；用户随时可以清理 |
| 其余（扁平资料与 `prd/`） | AI 处理后的受控投影 | AI 派生并维护版本历史 | **权威**。P2 / P3 / P5 按指针引用对账 |

这条区分要记住：**「引用了 `.ai/references/` 里的东西」不等于「引用了权威投影」**。`raw/` 下面那份可能是用户三个月前随手扔进来、早就过时的草稿；它的价值是「这是人当初真正说的话」，不是「这是现在算数的规格」。凡是验收要对账的引用，指针必须落在 `raw/` 之外。

`raw/` 与 `references/` 的其余子目录一样按需产生，部署时不建。

## 2. 三类资料

- **用户原件**：`.ai/references/raw/`。用户自己投放的原始材料，自由格式、任意命名与数量。**不受本文件后续的任何约束**——不用 `prd_id`、不进版本历史、不被 `prd-split` 消费、不参与非回归门以外的任何机制。它唯一的规矩是那条只读纪律（见 §1 表与 §10）。
- **扁平资料**：`api-<name>.md`、`design-<name>.md`、`insight-<name>.md` 等小型或已消化资料。一个文件装下，不建 PRD 索引，不受本文件后续的 `prd_id` 约束。
- **PRD 需求集合**：`.ai/references/prd/`。项目内每份独立需求各占一个稳定目录；大 PRD 可切多个模块，小 PRD 也进入自己的需求目录，只是模块数为 1。

三类可以并存。原件是可选投放点，对话里直接粘贴同样合法；PRD 能力是可选加层：不用 PRD 的项目、直接对话的小任务和既有扁平资料流程继续合法。

## 3. 两层目录与索引

```txt
.ai/references/prd/
  00_INDEX.md                         # 项目级需求总索引：有哪些需求
  2026-07-22-user-login/              # prd_id：一份独立需求
    00_INDEX.md                       # 单需求索引：当前版本 + 有哪些模块
    login-flow.md                     # module_slug：逐字原文切片
    validation-copy.md
    .archive/
      v1.0/                           # 这份需求自己的旧版全量快照
        00_INDEX.md
        login-flow.md
        validation-copy.md
  2026-07-23-batch-import/            # 另一份需求，版本序列互不相干
    00_INDEX.md
    import-rules.md
    .archive/
      v2.1/
        00_INDEX.md
        import-rules.md
```

### 3.1 项目级 `prd/00_INDEX.md`

项目级索引只回答“项目里有哪些需求、从哪里进入单需求地图”，不得复制各需求的模块登记表。每份需求一行，最小字段如下：

| 字段 | 含义 |
|---|---|
| `prd_id` | 日期化稳定身份，同时是相对目录名，规则见 §4 |
| 标题 | 当前人类可读标题；可改，不参与稳定寻址 |
| 当前版本 | 该需求自己的 live 版本，如 `v1.2` |
| 状态 | `active` / `superseded` / `retired`；不回收 `prd_id` |
| 来源线索 | 可用于认回同一需求的稳定源标识或回执指针；不得复制整份原文 |
| 入口 | 固定指向 `<prd_id>/00_INDEX.md` |

未来的收件箱状态等能力可以增加列或指针，但不得把模块表搬到项目级索引，也不得改变 `prd_id` 的身份语义。代码工作区范围不放项目级 PRD 总索引，统一在单需求入口声明。

### 3.2 单需求 `<prd_id>/00_INDEX.md`

单需求索引只回答“这份需求当前是哪一版、有哪些模块”。它包含：

1. 入口叙述：需求标题、`prd_id`、当前版本、来源指针与模块地图；允许摘要，因为它只负责导航。
2. 模块登记表：每个模块一行，字段为 `module_slug`、标题 / 章节、首见版本、当前版本、状态 `active|removed`。
3. `Workspace Scope`：用稳定 `workspace_key` 声明整份需求的主要实现、配套可写、只读与排除范围；字段和扩张纪律只以 `workspace-scope-schema.md` 为真源，本文件不复制。

为让 status 不靠自然语言猜字段，入口必须包含以下机器可读身份块；值与项目级索引同一行严格一致：

```md
## Requirement Identity

- prd_id: 2026-07-22-user-login
- current_version: v1.0
- status: active
```

字段名固定，值不加解释性尾注。标题与来源仍由入口叙述和项目级索引承载；身份块不复制模块表。

`module_slug` 只在所属 `prd_id` 内唯一。完整模块锚点由 `prd_id + prd_version + module_slug` 唯一表达；项目级需求身份与单需求内模块身份是两层概念，不得把其中一个当另一个使用。

## 4. 两层稳定身份：`prd_id` 与 `module_slug`

### 4.1 语法

`prd_id` 严格采用：

```txt
YYYY-MM-DD-<requirement-slug>
```

- `YYYY-MM-DD` 必须是合法日期，取**该独立需求首次进入当前项目 Butler 体系的项目本地日期**。
- 日期不是源文件创建日、产品版本发布日期、最近改版日或当前处理日的任意替代；已经登记后不得重算。
- `<requirement-slug>` 使用小写 ASCII 字母、数字和单个短横线分词，需表达需求语义；不得用模块 slug、版本号、随机串或纯序号冒充。
- 同日语义重名必须在首次分配前加有意义的区分词。身份一旦写入项目级索引，不得通过改目录名“修漂亮”；需要纠错时走后续迁移协议并保留旧引用兼容。

### 4.2 稳定性

`prd_id` 一次分配、终身不变。以下变化都**不得**产生新 `prd_id`：

- PRD 从 v1.0 升到 v1.1；
- 标题、章节号、源文件名或外部 URL 的展示文本变化；
- 模块新增、删除、合并、拆分或改名；
- 实现代码所在目录移动。

一份新需求必须领取新的 `prd_id`；两个独立需求不得因为属于同一产品、里程碑或代码包而共用身份。已 retired 的 `prd_id` 不回收、不复用。

### 4.3 `module_slug`：单需求内的模块身份

- 模块首次切片时领取 `module_slug`；它只在所属 `prd_id` 内唯一，一次分配、只增不改、不回收。
- 模块改名保留原 slug；新增发新 slug；删除置 `removed`。合并 / 拆分的认亲动作仍由 `prd-update.md` 承担。
- `prd_id` 定位哪份独立需求，`module_slug` 定位该需求里的哪个规格模块；两层都稳定，但作用域不同。

这小节也保留 MILE-0004 动作层对 `references-schema §4` 的既有回指语义：旧文中的“slug 身份”现在明确指 `module_slug`，不等于日期化 `prd_id`。

## 5. 全新需求、已有需求新版与重复输入

身份判断先认“是不是同一份需求”，再谈版本；不得用标题相似或文件名相同直接覆盖旧目录。按以下证据顺序判断：

1. **显式身份**：输入或既有回执明确给出已登记 `prd_id`，且来源关系不冲突 → 认作该需求。
2. **持久来源关系**：项目级索引或更新回执已把稳定外部文档 ID / 来源锚点绑定到唯一 `prd_id` → 认作该需求。
3. **内容与业务边界对账**：没有显式绑定时，比较需求目标、产品边界、稳定外部 ID 与历史内容；只有全部证据能唯一命中同一候选时，才可提议认作已有需求新版。
4. **弱信号不得单独定案**：标题、文件名、上传人、目录位置、相似关键词或同属一个 milestone 都只能辅助，不能独自决定身份。

判断结果是四态：

| 结果 | 条件 | 处置边界 |
|---|---|---|
| `new-requirement` | 没有既有候选且证据不冲突 | 提议新的日期化 `prd_id`，经动作层审查后登记 |
| `new-version` | 唯一命中既有 `prd_id`，内容相对当前版有变化 | 保持 `prd_id`，进入该需求自己的改版流程 |
| `duplicate` | 唯一命中且内容与已处理版本相同 | 不新建目录、不 bump 版本，记录重复来源即可 |
| `ambiguous` | 多候选、证据冲突或无法确定是新需求还是新版 | fail-closed：停止身份写入，列出候选与冲突，等待确认 |

任何动作层都不得用“默认新建”绕过 `ambiguous`，也不得用“看起来像”把不同需求静默合并。误新建会制造重复真源，误合并会污染历史；两者都比明确停机更坏。

## 6. 无损硬区分与读纪律

- 两层 `00_INDEX.md` 都是地图，可以摘要。
- `<prd_id>/<module_slug>.md` 必须是对应模块的逐字原文、无损投影；不得套用 `.ai/OVERVIEW.md` 那种概括、蒸馏或当前真相覆写的语义。
- 精确文案、字段约束和完整规则不得删改或拆成失去语义的半条。切片只能在目标需求改版时由新版对应原文整片替换。
- 读取顺序是：先读项目级 `prd/00_INDEX.md` 找 `prd_id` → 读 `<prd_id>/00_INDEX.md` 找 `module_slug` → 只读任务需要的模块切片。
- 正常执行读该需求的 live；钉版复现才读 `<prd_id>/.archive/vN/`。不得跨需求从另一个目录借同名模块补全当前规格。

这节保留既有动作层对 `references-schema §6` 的无损红线回指；目录从 legacy 根切片升级为 `<prd_id>` 内切片，不改变“模块原文必须逐字”的底线。

## 7. 独立版本历史

- 每个 `<prd_id>` 独立维护版本序列和 `.archive/vN/`。两个需求都可以各自存在 `v1.0`，它们互不比较、互不覆盖。
- 改版时只把目标 `<prd_id>` 的当前 `00_INDEX.md` 与全部 live 模块冻入该目录的 `.archive/v<旧版>/`，再更新该需求的 live。不得把项目级 `prd/00_INDEX.md` 或其他需求一起塞进单需求快照。
- 一个归档版本必须自包含，能还原该需求当时的模块地图和全部切片。

## 8. legacy 单 PRD 结构

以下旧形态是 MILE-0004 交付的 **legacy 单 PRD 结构**：

```txt
.ai/references/prd/
  00_INDEX.md
  <module_slug>.md
  .archive/vN/
```

迁移前它仍可读，代表“这个项目只有一份尚未领取 `prd_id` 的 PRD”。任何消费者都不得静默创建日期、猜 slug、移动文件或改历史 AC，也不得假装它已经是新集合结构。

### 8.1 显式迁移

迁移由 `$BUTLER_PATH/tools/prd-migrate/prd_migrate.py` 执行，必须先 `inspect/plan`，再由显式 `prd_id` 与标题驱动 `apply`。工具不得从文件 mtime、当前日期、PRD 版本或标题自动回填“首次进入本项目”的日期；证据不足就停。

apply 将 legacy 根完整搬入 `<prd_id>/`，生成项目级 `00_INDEX.md`，并在 `.ai/references/prd/.butler-migration.json` 写 receipt。切换必须使用同父目录 staging/backup/rename；成功后 backup 留在 `.ai/references/.prd-migration-backups/`，直到 verify 通过且用户按指南决定清理。混合布局、symlink、未知结构或 identity 冲突 fail-closed。

receipt 最小字段：`schema_version`、`migration_id`、`prd_id`、`title`、`migrated_at`、`backup`、`legacy_tree_sha256`、`collection_tree_sha256`、逐文件 `legacy_path → collection_path + sha256`、引用影响面。它是兼容解析数据，不是 PRD 内容真源。

### 8.2 历史引用兼容

- 新集合 AC 用 `acceptance-schema.md` 的 `prd_refs`，正文路径必须带 `prd_id`。
- legacy AC 的 `prd_version + references/prd/<module_slug>.md` 不回写；resolver 从 migration receipt 取得隐式 `prd_id`，live 版本吻合时指向 `<prd_id>/<module_slug>.md`，否则指向 `<prd_id>/.archive/<prd_version>/<module_slug>.md`。
- `prd/00_INDEX.md` 在迁移后变成项目级索引；旧 legacy index 的逐字副本保存在 `<prd_id>/00_INDEX.md`，resolver 对历史 legacy index 引用也必须转到单需求入口。
- 缺 receipt、多 receipt 候选、版本目录不存在、模块未登记或文件 hash 漂移都不得猜；返回失败并亮出缺口。

迁移只改 PRD 结构与兼容 receipt，不改 `.ai/MILESTONE.md`、active/future AC 或 `.ai/iterations/` 的历史快照。影响面必须分组报告，让后续工作选择是否改用新路径；closed/frozen 继续靠 resolver 回溯。

## 9. 动作边界与路线

本文件是声明式契约，不含执行逻辑：

| 动作 | 当前归属 |
|---|---|
| 单 PRD 首切与模块边界 | ✅ `prd-split.md`：身份四态、日期证据、`<prd_id>/` 首切与 workspace soft 对齐 |
| 单 PRD 改版、先冻后更、模块认亲 | ✅ `prd-update.md` + `tools/prd-update/`：已确认 spec、事务 apply、持久 receipt、verify/rollback |
| 多 PRD 版本引用与 legacy 迁移 | ✅ MILE-0009 R5：三阶段 schema + `tools/prd-migrate/` + migration guide |
| 项目级 status、双宿主命令适配 | ✅ `prd-status.md` + `tools/prd-status/` + 双宿主薄入口 |
| 工作区范围与实际改动门禁 | ✅ `workspace-scope-schema.md` + `tools/workspace-scope/` + PreToolUse 共享解析内核 |

目标结构已经写进本文件，不等于未交付动作已经适配。动作层在各自迭代交付前必须继续把未实现能力标为 planned。

## 10. 非回归门

PRD 需求集合是可选加层。任何相关迭代都必须明确自己的改动范围，并守住：

- 不用 PRD 的对话驱动 P1–P5 流不变。
- `api-` / `design-` / `insight-` 等扁平资料流不变。
- `.ai/references/raw/` 用户原稿不因 PRD 集合而被改写、移动或删除。
- 已冻结与已收口产物不被静默回写。
- 若某后续路线必须有意修改既有 PRD 消费者，AC 与 TECH_PLAN 必须明确列出原因、兼容策略和负向回归，不能拿“非回归”口号掩盖真实迁移面。
