# 冷启动读序切换 + digest-and-point 读纪律（两态第一读）

> 分流：完整迭代（P1–P5）· ITER-0031 · MILE-0003 R5 · 监督态自驱（用户"继续吧"委托，非 /dangerous）

## 一句话

把冷启动"第一读"从写死的 `.ai/PROJECT.md` 泛化成**两态**：采用 `.ai/project/` 知识文件夹的项目先读 `00_INDEX.md` 拿地图、再按需钻主题（digest-and-point 读纪律）；仍单文件的项目照旧读 `.ai/PROJECT.md`——把 R2 定的文件夹读法接成活跃读序，且**不砸**任何还没迁移的项目。

## 为什么现在做

- R2 立了 `.ai/project/` 知识文件夹契约、R3 把折叠维护 + 漂移自检接成活跃仪式、R4 补齐了执行帮手；但**冷启动到底先读哪个文件**至今还写死在 `context-persistence §冷启动读序` 指 `.ai/PROJECT.md`（R2/R3/R4 都明确留给 R5、没碰）。知识文件夹再全，AI 冷启动不去读 `00_INDEX` 就白搭。
- R5 就补这一环：读序第一读切成两态。**这是"知识地图真被用起来"的最后一段接线**——R6（部署种子/迁移）、R8（butler 自身迁移 + 切版）仍留后续。

## make-or-break：第一读切换必须两态（不是可选优化）

- 冷启动读序是**活规则**：每个部署项目、乃至 butler 仓自己下一次冷启动，都按它建立上下文（butler 读这些规则来接手自己）。
- 而 R6 部署种子 / R8 butler 迁移都没落地——**此刻含 butler 在内的绝大多数项目仍是单文件 `.ai/PROJECT.md`**。
- 若把第一读**无条件**改成 `.ai/project/00_INDEX.md`，单文件项目冷启动会被指去读一个**不存在的文件**、当场踩空。
- 故必须两态：**采用 `.ai/project/` → 第一读 `00_INDEX.md` + 按需主题；仍单文件 → 第一读 `.ai/PROJECT.md`**。这与 R3 收口步④、第 6 不变量用的是同一套两态纪律（`iteration-schema §5.5` / `context-persistence 第 6 不变量`），保持一致。

## digest-and-point 读纪律（读侧对齐写侧）

- 写侧 digest-and-point 密度（消化过的真内容 + 指针、已有真源不复制）R2 已落 `project-digest-schema §5`；R5 补**读侧对齐**：冷启动读 `00_INDEX` 拿全貌与地图 → **按当前任务需要钻相关主题文件（不必一次性读全部主题）** → 再按指针钻代码。
- 这样即使知识文件夹随项目越长越全，冷启动预算仍**有界**（读地图 + 定向钻取，不 slurp 整个文件夹）。

## 做什么（G1–G4）

- **G1 两态化第一读**（主）：`context-persistence §冷启动读序` 第 1 项从写死 `.ai/PROJECT.md` 改为两态分支（文件夹态 `00_INDEX` + 按需主题 / 单文件态 `.ai/PROJECT.md`）；收尾"互补"句同步两态措辞。加读侧 digest-and-point 纪律一句。
- **G2 翻 R5 指针**：`project-digest-schema` 介绍段 line 9 + §9 R5 路线项 + §9 header，从"待实现/后续路线项 R5"翻成"✅ 已接线（两态）"（同 R3 翻 §6/§9 的做法）。
- **G3 同步 README 读序**：`Coder/README.md §读取顺序` 冷启动读序描述改两态。
- **G4 顺修 handoff-spec 单文件中心措辞**：`handoff-spec §1` "状态全貌由 `.ai/PROJECT.md` 承载"改为两态产物（单文件 `.ai/PROJECT.md` 或 `.ai/project/` 文件夹），仍指 context-persistence §6 为读序真源、不重写读序。

## 不做（边界）

- 不碰 R6：`mcv-deployment`（部署仍种单文件、老项目迁移配方）、`migrations/`。
- 不碰 R8：butler 自身 `.ai/PROJECT.md → .ai/project/` 实体迁移、切版 `VERSION`/v2.0.0。
- 不碰 R7 说人话（`presentation-protocol` / `artifact-style`）。
- 不改 R3 强制语义（折叠必做 / 第 6 不变量）、不改 `.ai/project/` 结构契约（R2 已定）、不改 `logic-protocol §1.1`（那是 SOP 规则加载序、与 `.ai/` 产物冷启动序无关）。
- 不动 P1–P5 状态机 / 四件套字段 / hook / 迭代里程碑双层。

## 收口前滚（本迭代自身，butler 单文件态按需）

- `.ai/PROJECT.md`：「冷启动读序固定」条改两态措辞（规则已两态、butler 自身单文件走 PROJECT.md 分支）+ 知识文件夹条 R5 指针翻已接线。

## 明确不影响

- R3 折叠必做 / 第 6 不变量强制语义、`.ai/project/` 结构、P1–P5 状态机、四件套字段、hook、迭代/里程碑双层、部署种子迁移（R6）、butler 实体迁移（R8）、`VERSION`、`logic-protocol §1.1` 规则加载序。
