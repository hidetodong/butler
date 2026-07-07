# Verification Summary

> 监督态自驱（非 `/dangerous`）：本迭代由用户"继续吧"委托执行，P1–P3 自驱、AC ack-frozen；P5 起独立复核子 agent（fresh-context，验证者≠实现者）守质量。无 RUN_LOG 审计条（非无人值守）。

- ITER-0029（MILE-0003 R3）：把 R2 在 `project-digest-schema §6` 只**声明**的折叠维护模型**接线成活跃收口仪式**——①泛化收口步④为两态（`iteration-schema §5.5` + `milestone-schema §7.4`：项目已采用 `.ai/project/` 则按主题路由 delta **必做折叠** / 仍单文件 `.ai/PROJECT.md` 则**按需前滚**）；②`context-persistence §冷启动一致性自检` 加**第 6 条「知识文件夹漂移自检」**（条件不变量、单文件项目 N/A）；③全仓一致性自检计数 5→6 同步（`lifecycle` / `versioning-schema` / `iteration §5.5 步⑤`）；④顺修 R2 遗留漂移（`§5→§6` 引用 + context-persistence §7 契约描述 + 介绍段"强制化"表述）；⑤翻 `project-digest §6/§9` R3 指针（待→已接线）。
- 总体结论：**8/8 AC 通过**（AC6 复核初判 partial=介绍段矛盾残留，**已就地修**转 confirm），可收口。全 **auto·可靠**（规则文档：读正文确认 + `git`/`grep` 核守恒）。**核心对抗点（两态兼容）5 个改动点逐处显式保留单文件分支/N/A**，不砸 butler 自己或任何单文件项目的下一次收口。scope 守恒：改 6 规则文件，未越 R5（读序第一读仍 PROJECT.md）/R6（mcv+migrations 未碰）/R8（butler 自身仍单文件）、未 rename、未切版。

# AC Status

- [x] AC1（auto·可靠）✓ `iteration §5.5` 步④ 两分支齐：文件夹态"按主题路由折进对应 topic·**必做**·有 delta 即折·定向路由非重写·成本∝改动量"+ 单文件态"改长期事实才更新否则不动"；步内引用改指 `§6`
- [x] AC2（auto·可靠）✓ `milestone §7.4` 步④ 两态泛化 + 明写"里程碑级只保版本级全貌、各迭代已增量折叠不重折"；引用改指 `§6`
- [x] AC3（auto·可靠）✓ `context-persistence` 第 6 条追加于第 5 条后（不 renumber 前 5）+ 明标条件"采用 `.ai/project/` 适用、单文件 N/A"+ 可操作核法（近期 CHANGELOG delta 是否都折进对应 topic / 有无被取代结论残留，人工·prompt 级抽查非脚本）
- [x] AC4（auto·可靠）✓ `iteration §5.5 步⑤` / `lifecycle §收口 步⑤` / `versioning §切版自检` 三处 5→6 + 列举补第 6 项带条件；`grep "5 条不变量\|5 不变量" Coder/ templates/` exit=1（0 残留）；`preference §8 五条隔离` 无关未动
- [x] AC5（auto·可靠）✓ 5 个改动点逐处显式单文件分支/N/A（复核逐处核过）；模拟 butler 自身（无 `.ai/project/`）收口走单文件态按需前滚 + 第 6 条 N/A，不被要求折进空文件夹、不假红
- [x] AC6（auto·可靠）✓ `project-digest §6/§9` R3 指针待→已接线、指向真实落点（iteration §5.5 / 第 6 不变量，实存且一致）；**Should Fix 已修**：介绍段 L9 原把"强制化"仍称"后续路线项"（R2 遗留、漏扫）已改为"折叠已由 R3 接线 / 读序切换=R5"，全文无矛盾残留
- [x] AC7（auto·可靠）✓ 读序第一读仍 `.ai/PROJECT.md`（未切 00_INDEX＝未越 R5）；`git status` 无 mcv-deployment/migrations/VERSION（未越 R6）；`.ai/project/` 不存在＝butler 自身仍单文件结构（未越 R8）
- [x] AC8（auto·可靠）✓ 措辞必须/不得/应、跨目录带 `20_`/`40_` 前缀、增量不 renumber；`.ai/PROJECT.md` 三处前滚在收口步④落地（见下）；`git status` 改动集=6 规则文件 + `.ai/` 台账，无 rename、无计划外文件

# Verification Results

- AC1–AC3/AC6：逐条读改后 `iteration §5.5` / `milestone §7.4` / `context-persistence 第 6 条` / `project-digest §6/§9` 正文确认要素齐、两分支/条件/落点到位、与预研 §5前提2/§6 保真。
- AC4：`/usr/bin/grep -rn "5 条不变量\|5 不变量" Coder/ templates/` exit=1；`grep "6 条不变量\|第 6 条\|知识文件夹漂移" Coder/` 命中 5 文件（真源 + 4 引用点）。
- AC5：读 5 处两态分支 + 第 6 条 N/A 标注，模拟单文件项目走位无假红、无悬空。
- AC7：`git status --short` + 读 `context-persistence §冷启动读序`(第一读未变) + `ls .ai/project/`(不存在)，证明 R5/R6/R8 未越界。
- AC8：`grep "project-digest-schema.md §5" Coder/` exit=1（§5 误引已清）；改动集守恒、无 rename。

# Gate Coverage

- 通用质量门禁：规则文档（非可执行代码），验证=读正文确认 + git/grep 核守恒（`auto·可靠`）；无 UI / 交互残余、无人测道残余（8 条全 `auto·可靠`）。
- Active Profiles：无（Markdown 规则仓，未命中 `10_Domain_Stack_Profiles/`），N/A。
- Tech Plan Alignment：DD1–DD6 全兑现——两态用显式分支（DD1）、第 6 条定为条件不变量（DD2）、定义只在 context-persistence 真源其余处引用计数（DD3）、§5→§6 顺修不扩范围（DD4）、R3 指针翻面不删声明（DD5）、读序第一读不碰（DD6）。无偏离。
- References Compliance：本轮无 `.ai/references/`，N/A。

# Independent Review

- 复核方式：fresh-context general-purpose 子 agent（agentId aafa3e68239fba763，验证者≠实现者），逐 AC + 两态兼容逐处核 + 计数守恒 + scope 边界 + 预研保真 + 折叠非伪接线对抗探测。
- 逐 AC 裁决：**confirm 7 + AC6 partial（矛盾残留）**；对抗核心（两态兼容 5 处）**逐处 confirm 单文件分支显式、无一处无条件必做**。
- 结论：**APPROVE-WITH-NITS，0 Must Fix**。1 Should Fix（介绍段 L9"强制化"仍称后续路线项、触 AC6）**已就地修** → AC6 转 confirm、**8/8**。1 Nit=`.ai/PROJECT.md` 三处前滚待收口步④落地（复核提醒务必真写，否则 butler 自身全貌产物与新规则自我打脸）——已在下方收口执行。

# Remaining Risks

- **两态兼容依赖措辞纪律**：R3 靠"文件夹态必做 / 单文件态按需 + 第 6 条 N/A"的显式分支兜住暂态；R6 部署种子 / R8 butler 迁移落地后，单文件分支才逐步退场。在此之前，任何后续改动误把某分支写成无条件即会砸单文件项目收口——已由本轮显式分支 + 一致性自检兜底，属受控。
- **陈旧的完整比诚实的薄更毒**（承 R2 最大风险）：R3 已把折叠 + 漂移自检从"声明"变"强制/可验证"，对冲了该风险；但强制仅对**已采用 `.ai/project/` 的项目**生效，butler 自身在 R8 迁移前仍是单文件、第 6 条 N/A，该风险对 butler 自身要到 R8 才真正闭合。
- 收口非 hook 门禁，butler 仓不 live 跑自己的 hook（既有设计约束），两态收口步 + 第 6 不变量靠纪律 + 收口自检兜底。

# Handoff / Next Step

- 本迭代闭合，进原子收口五步（归档 / 交付 md+html / 翻台账 current=none + ITER-0029 行 closed / **PROJECT 前滚三处**[收口仪式步④两态 / 一致性自检 5→6 / 知识文件夹 R3 已接线] / 收口自检 6 不变量）。北极星=ITER-0029（MILE-0003 R3·维护回路接线）达成。
- 归属 MILE-0003 R3；收口后 MILE-0003 仍 active，剩 R4（更新说明+查过时帮手）/R5（读序切换）/R6（部署迁移）/R7（说人话）/R8（butler 自身 dogfood + 切 v2.0.0），待用户指令。本轮按惯例收口即提交（不推送、不切版）。
