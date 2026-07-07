# 知识文件夹维护回路接线（折叠模型 → 强制收口仪式）

> ITER-0029 · 迭代交付（小版本）· 收口 2026-07-07 · MILE-0003 R3 · 监督态自驱（用户"继续吧"委托，非 /dangerous；P5 起独立复核守质量）

## 本次交付目标

- R2 把冷启动"整体"产物的格式契约改成了 `.ai/project/` 知识文件夹，但只在 `project-digest-schema §6` **声明**了折叠维护模型，把"强制化 + 漂移自检"留给了 R3。若一直只声明不强制，知识文件夹就会精确地退化成 R2 点名的最大风险——"陈旧的完整比诚实的薄更毒"（AI 信滞后内容做错判）。
- R3 把这套模型**接线成活跃收口仪式**：收口时必折叠、冷启动自检漂移。**边界**：只接线维护回路，冷启动读序切换（R5）/ 部署种子迁移（R6）/ butler 自身迁移（R8）仍留后续。

## 已完成内容

- **泛化收口步④为两态**（`iteration-schema §5.5` + `milestone-schema §7.4`）：
  - 项目**已采用 `.ai/project/` 知识文件夹** → 把本迭代 `01_CHANGELOG.md` 的 delta **按主题路由折进对应 topic 文件、必做**（有对象级 delta 即折，不再"按需"）；定向路由非重写全份，成本∝改动量。
  - 项目**仍单文件 `.ai/PROJECT.md`**（未迁移暂态）→ 保留旧"按需前滚长期事实字段"。
- **新增冷启动一致性自检第 6 条「知识文件夹漂移自检」**（`context-persistence §冷启动一致性自检`）：采用 `.ai/project/` 的项目核对"近期 CHANGELOG delta 是否都已折进对应 topic、有无被取代结论残留"，脱节先暴露；**条件不变量**——单文件项目 N/A。复用 MILE-0001 的 5 不变量 + 原子收口先例。
- **全仓一致性自检计数 5→6 同步**：`lifecycle §收口`、`versioning-schema §切版自检`、`iteration §5.5 步⑤` 三处（第 6 条均带条件标注）。
- **顺修 R2 遗留漂移**：`iteration §5.5` / `milestone §7.4` 里"见 project-digest-schema §5"改指 §6（R2 renumber 后 §6 才是折叠模型）；`context-persistence §7` schema 契约描述改成两态准确；`project-digest §6/§9` R3 指针从"待接线"翻成"已接线"、介绍段"强制化"表述同步。

## 关键变更 / 用户可感知变化

- 采用知识文件夹的项目，从此**每次收口必把改动折进知识地图 + 冷启动自检它是否陈旧**——R2 声明的"越补越全、强制可验证折叠"从纸面变成活跃执行纪律。
- **两态兼容是核心设计约束**（不是可选优化）：R6 部署种子 / R8 butler 迁移都还没落地，此刻含 butler 仓自己在内的绝大多数项目仍是单文件 `.ai/PROJECT.md`。R3 改的是**活跃收口路径**、会立刻管每个项目乃至 butler 自己的下一次收口——所以"必做折叠 / 第 6 不变量"一律**只在项目已采用 `.ai/project/` 时生效**，单文件项目继续走旧按需前滚、第 6 条 N/A，不会被要求"折进一个不存在的文件夹"、也不会在自检时假红。
- 向后兼容：未改冷启动第一读目标（仍 PROJECT.md，切 00_INDEX 是 R5）、未加部署种子（R6）、未迁移 butler 自身实体（R8）、未切版；未动状态机 / 四件套 / hook / 迭代里程碑双层。

## 高层影响范围

- 改（章节级，6 规则文件）：`iteration-schema §5.5`、`milestone-schema §7.4`、`context-persistence §冷启动一致性自检 + §7`、`lifecycle §收口`、`versioning-schema §切版自检`、`project-digest-schema §6/§9 + 介绍段`。
- 收口前滚（本迭代自身）：`.ai/PROJECT.md` 三处——收口仪式步④两态 / 一致性自检 5→6 / 知识文件夹 R3 已接线。
- 没碰（R3 边界）：`context-persistence §冷启动读序`第一读（R5）、`mcv-deployment` / `migrations/`（R6）、butler 自身 `.ai/PROJECT.md → .ai/project/` 实体迁移（R8）、`VERSION`、P1–P5 状态机 / 四件套字段 / hook / 迭代里程碑双层。

## 验证方式与结果摘要

- **8/8 AC 通过**，全 **auto·可靠**（读正文确认 + `git`/`grep` 核守恒，确定性可复现）；无人测道残余。
- P5 **独立复核**（fresh-context 子 agent，验证者≠实现者）：**两态兼容 5 个改动点逐处 confirm 单文件分支/N/A 显式、无一处无条件必做**；计数守恒 grep 0 残留；scope 不越 R5/R6/R8；预研 §5前提2/§6 保真——**APPROVE-WITH-NITS，0 Must Fix**。
- Should Fix **已就地修**：`project-digest §介绍段` 遗留把"强制化"仍称"后续路线项"（R2 写的、漏扫）已改为"折叠已由 R3 接线 / 读序切换=R5"，全文无矛盾残留。
- 守恒核对：`grep "5 条不变量\|5 不变量" Coder/` exit=1（0 残留）；`grep "project-digest-schema §5" Coder/` exit=1；`git status` 改动集=6 规则文件 + `.ai/` 台账 + PROJECT.md 前滚，无 rename、无越界。

## 已知剩余风险 / 延后事项

- **两态兼容依赖措辞纪律**：暂态靠"文件夹态必做 / 单文件态按需 + 第 6 条 N/A"的显式分支兜住；R6/R8 落地后单文件分支才退场。此前任何改动误把某分支写成无条件即会砸单文件项目收口——已由本轮显式分支 + 一致性自检兜底。
- **最大风险对 butler 自身要到 R8 才闭合**：折叠强制只对已采用 `.ai/project/` 的项目生效，butler 自己在 R8 迁移前仍单文件、第 6 条 N/A。
- 本轮按惯例收口即提交，**未推送、未切版**；MILE-0003 仍 active，剩 R4/R5/R6/R7/R8（v2.0.0 切版在 R8），待用户指令。

## 引用（只引用路径，不嵌全文）

- 归档四件套 + 切片：`.ai/iterations/ITER-0029/CONCEPT.md` / `AC_LIST.md` / `TECH_PLAN.md` / `VERIFY_REPORT.md` / `CHANGELOG.md`
- 改动：`Coder/20_Workflow_Lifecycle/iteration-schema.md`、`milestone-schema.md`、`lifecycle.md`、`versioning-schema.md`、`Coder/40_Context_Management/context-persistence.md`、`project-digest-schema.md`
- 设计基准（预研，未追踪）：`docs/research/MILE-0003-project-knowledge-folder.html`（§5 前提2 / §6 维护回路）
