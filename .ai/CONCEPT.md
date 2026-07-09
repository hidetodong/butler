# MILE-0004 R1 · references 索引化基座

> ITER-0036 · 里程碑 MILE-0004 首块 · 监督态自驱（承 grilling 十节点决议）· 不切版（纯规则新增）

## 一句话

`references/` 子系统当年没被 MILE-0003 的知识文件夹待遇覆盖到——**无 schema、无索引、无读纪律**。R1 新建 `references-schema.md`，给它补上"索引 + 渐进读"的**契约层**：定义 `references/prd/` 知识文件夹形态（`00_INDEX` 入口 + 模块登记表）、digest-and-point 读纪律、"索引可摘要 / 切片必原文"硬区分、live + `.archive` 落盘契约。**只定契约**，切分动作 / 入口 / 钉版 / 同步留 R2–R5。

## 背景（这块地基为什么先做）

- references/ 现状：`logic-protocol` 定注入、`mcv-deployment` 定目录、`acceptance/tech-plan/verify` 定 `External References` 字段——但**没有一份 schema** 说 references/ 内部怎么组织、怎么读。
- MILE-0004 要 PRD 先行 + 版本化改版同步，全都得踩在"references 有索引、有稳定模块身份、有版本落盘"的地基上。R1 就是这块地基（契约）：R2 切、R3 接入口、R4 钉版、R5 同步全依赖它。地基先浇，动作后砌。

## 做什么（DD）

- **DD1 · 新建 `Coder/40_Context_Management/references-schema.md`**：references/ 子系统首份契约。两部分——通用（references/ 是什么；既有扁平单文件 `api-`/`design-`/`insight-` 归入"扁平态"）+ prd/ 知识文件夹态（下列 DD2–DD5）。
- **DD2 · `references/prd/00_INDEX` 契约**：入口（这份 PRD 是什么 + 模块地图）+ **模块登记表**——每模块一行：`slug`（终身身份）↔ 当前标题/章节（会变的门牌）↔ 首见版本 ↔ 当前版本 ↔ 状态（active / removed）。slug 一次分配、跨改版不变（Q7）。
- **DD3 · digest-and-point 读纪律**：读 references/prd 先读 `00_INDEX` 地图 → 按需钻用到的那片 `prd/<slug>.md` → 指针钻源。执行默认读 live 最新（Q2）。借 `.ai/project` 的读法用在参考资料上。
- **DD4 · "索引可摘要 / 切片必原文"硬区分**：`00_INDEX`（含登记表）**可以是摘要 / 路由**；`prd/<slug>.md` 切片**必须逐字原文、无损**（少一字验收就错）。这是 references 相对 `.ai/project` 的命门差异——project 全是有损摘要，references 的切片是无损真源。
- **DD5 · 落盘契约**：live 目录 `references/prd/<slug>.md` = 最新版、无版本前缀、执行直读（Q10）；`.archive/vN/` = 改版时冻的旧版**全量快照**、自包含（Q2/Q10）。`prd_version` 只在回溯（钉版迭代 / 闭档审计）时去 `.archive` 找。
- **DD6 · README 注册**：新 schema 登进 `Coder/README.md` 目录结构 + 读取顺序（守"新规则文件必须注册"）。

## 边界（不做）

- 不做**切分动作**（怎么把一份 PRD 切成 slug 切片、边界算法、soft 对齐拆法）——R2。
- 不动 `/milestone` 入口、不做首切触发、不做路线图 ↔ 模块交叉指针——R3。
- 不碰 AC frontmatter `prd_version` 钉版、不改 acceptance/tech-plan/verify 接线——R4。
- 不做 `/prd update` 同步、变更检测、影响面、`.archive` 快照的**产生动作**（R1 只定 `.archive` 的**契约/形态**，不写"何时怎么冻"）——R5。
- 不改 references/ 既有扁平用法（`api-`/`design-`/`insight-` 注入照旧）、不动非 PRD 流、不切版。

## 关键设计约束

- **契约层与动作层分离**：R1 只定"references/prd 长什么样、怎么读、怎么落盘"，一切**产生 / 变更动作**归 R2–R5。R1 是纯声明式契约、可被后续迭代当地基引用，不含执行逻辑。
- **无损 vs 有损的红线（DD4）**：整个 MILE-0004 的命门——一旦有人拿 `project-digest` 的有损 overwrite 语义套到 prd 切片上，PRD 精确文案就废了。schema 里把这条写成硬约束、显式对比 `.ai/project`。
- **slug 终身身份**：DD2 的 slug 不随章节重编号变（Q7），是 R5 改版认亲的锚点。R1 定死"slug 一次分配、只增不改（除非模块真 removed）"。
