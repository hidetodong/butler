# Verification Summary

> 监督态自驱（非 `/dangerous`）：本迭代由用户"继续吧"委托执行，P1–P3 自驱、AC ack-frozen；P5 起独立复核子 agent（fresh-context，验证者≠实现者）守质量。无 RUN_LOG 审计条（非无人值守）。

- ITER-0031（MILE-0003 R5）：把冷启动"第一读"从写死 `.ai/PROJECT.md` 泛化成**两态**——①`context-persistence §冷启动读序` 第 1 项拆两分支（采用 `.ai/project/` 的项目先读 `00_INDEX` + 按需主题 / 仍单文件 `.ai/PROJECT.md` 的项目读 `.ai/PROJECT.md`）+ 加读侧 digest-and-point 纪律（读地图 → 按需钻主题 → 指针钻代码、不 slurp、预算有界）+ 收尾互补句两态；②翻 `project-digest-schema` R5 指针三处（介绍段 line 9 + §9 header + §9 R5 路线项，待→已接线，指真实落点）；③`README §读取顺序` 两态措辞同步；④`handoff-spec §1` 状态全貌承载产物措辞两态。
- 总体结论：**8/8 AC 通过**，可收口。全 **auto·可靠**（规则文档：读正文确认 + `git`/`grep` 核守恒，确定性可复现），无人测道残余。**核心对抗点（两态兼容）四处逐处过关**：context-persistence / project-digest §9 / README / handoff 第一读均两态、单文件分支显式（前两处显式含 butler 自身）、全仓无一处无条件 `00_INDEX`——不砸含 butler 在内的单文件项目冷启动。scope 守恒：改 4 规则文件，未越 R6（mcv/migrations）/R7（说人话）/R8（butler 实体迁移+切版）、未 rename、无新增规则文件、未切版。

# AC Status

- [x] AC1（auto·可靠）✓ `context-persistence §冷启动读序` 第 1 项拆两分支：文件夹态"第一读 `00_INDEX` + 按需主题"/ 单文件态"读 `.ai/PROJECT.md`（未迁移暂态，含 butler 仓自身）"，两分支均标"冷启动第一读"、格式指 `project-digest-schema.md`
- [x] AC2（auto·可靠）✓ 文件夹态第一读写明读侧纪律"读 `00_INDEX` 拿地图 → 只钻相关主题（**不必一次性读全部**）→ 指针钻代码"，点明"预算…仍**有界**（读地图 + 定向钻取，不 slurp）"；写侧密度回指 `project-digest-schema §5`（未重抄）
- [x] AC3（auto·可靠）✓ 收尾互补句改两态："项目全貌产物与 handoff 互补…（`.ai/project/` 知识文件夹或单文件 `.ai/PROJECT.md`）"，无残留单文件中心表述
- [x] AC4（auto·可靠）✓ R5 指针三处齐翻：介绍段 line 9"已由 R5 接线为两态"、§9 header line 147"R3 / R5 已接线；R6 / R8 待实现"、§9 R5 路线项 line 149"✅ 已接线"+ 指向真实落点（`context-persistence §冷启动读序` 两态第 1 项）；无残留"后续路线项 R5 / 切换前仍按现读序"旧话（grep 复查：line 147 命中系正则贪婪匹配同行"R6/R8 待实现"、非旧指针残留）
- [x] AC5（auto·可靠）✓ `README §读取顺序` line 131 冷启动读序描述两态（文件夹态 `00_INDEX` + 按需主题 / 单文件态 `.ai/PROJECT.md`），仍指 `context-persistence.md §6`（含两态第一读与读纪律），未复写整套读序
- [x] AC6（auto·可靠）✓ `handoff-spec §1` line 15"状态全貌由项目全貌产物承载（两态：`.ai/project/` 文件夹或单文件 `.ai/PROJECT.md`）"，仍指 `context-persistence.md §6` 为读序真源、不在此重写读序
- [x] AC7（auto·可靠）✓ R3 折叠必做（`iteration §5.5` "必做"计数=2 未减）/ 第 6 不变量均未在 diff（一字未动）；`.ai/project/` 结构契约（R2）未改；`git status` 无 `mcv-deployment`/`migrations/`/`VERSION`/`logic-protocol`（未越 R6/R8）；butler 自身 `.ai/project/` 不存在＝仍单文件
- [x] AC8（auto·可靠）✓ 措辞必须/不得/应、跨目录带 `40_` 前缀、增量不 renumber；两态第一读单文件分支显式（模拟 butler 自身冷启动仍走 `.ai/PROJECT.md`、不被指向不存在的 `00_INDEX`）；`git status` 改动集=4 改规则文件 + `.ai/` 台账，无新增规则文件、无 rename。**收口前滚 `.ai/PROJECT.md` 两处（读序两态 + R5 指针）在收口步④落地**（见 Independent Review Nit·下方收口执行）

# Verification Results

- AC1–AC3：逐条读改后 `context-persistence §冷启动读序` 正文，确认第 1 项两分支齐、读侧 digest-and-point 纪律在、互补句两态。
- AC4：`/usr/bin/grep -n 'R5' project-digest-schema.md` 三处指针均翻已接线、指真实落点；残留扫描 count=1 经复查系正则贪婪匹配同行"R6/R8 待实现"（假阳性），无真残留。
- AC5/AC6：读 `README §读取顺序` / `handoff-spec §1`，两态措辞 + 指向 context-persistence §6 真源、不重写读序。
- AC7/AC8：`git status --short` 证明未触 `mcv-deployment`/`migrations/`/`VERSION`/`logic-protocol`、无新增规则文件；`ls .ai/project/` 不存在＝butler 仍单文件；grep R3"必做"=2、第 6 不变量在且未在 diff。

# Gate Coverage

- 通用质量门禁：规则文档（非可执行代码），验证=读正文确认 + git/grep 核守恒（`auto·可靠`）；无 UI / 交互残余、无人测道残余（8 条全 `auto·可靠`）。
- Active Profiles：无（Markdown 规则仓，未命中 `10_Domain_Stack_Profiles/`），N/A。
- Tech Plan Alignment：DD1–DD6 全兑现——两态显式分支不隐去单文件（DD1）、读侧纪律只在读序真源写一次 + 写侧回指 §5（DD2）、R5 指针三处齐翻不删声明（DD3）、README/handoff 只同步措辞不重写读序（DD4）、R5 边界硬钉未越 R6/R8/R7（DD5）、PROJECT 前滚在收口步④落（DD6）。无偏离。
- References Compliance：本轮无 `.ai/references/` 产出，N/A。

# Independent Review

- 复核方式：fresh-context general-purpose 子 agent（agentId ae1a0bc8531723aac，验证者≠实现者），逐 AC + 两态兼容四处逐处核 + digest-and-point 读纪律 + R5 指针三处齐翻 + 不改 R3 语义 + scope 边界 + DRY 不重写读序对抗探测。
- 逐 AC 裁决：**confirm 8/8**；两态四处逐处 confirm 第一读两态、单文件分支显式（context-persistence 与 project-digest §9 显式含 butler 自身）、全仓无一处无条件 `00_INDEX`。
- 结论：**APPROVE，0 Must Fix**。1 Should Fix（收口守门项）：`.ai/PROJECT.md` line 25 读序固定条 + line 29 R5 指针须在收口步④前滚，否则收口后 line 29 残留"R5 待接线"、line 25 与新两态规则自相矛盾——已在下方收口执行落地。1 Nit（不阻断）：handoff/README 单文件分支未点名 butler（语义完整、不踩空，不改）。

# Remaining Risks

- **两态兼容依赖措辞纪律**（承 R3）：暂态靠"文件夹态第一读 `00_INDEX` / 单文件态第一读 `.ai/PROJECT.md`"显式分支兜住；R6 部署种子 / R8 butler 迁移落地后单文件分支才逐步退场。此前任何改动误把第一读写成无条件 `00_INDEX` 即会砸单文件项目冷启动——已由本轮四处显式分支 + P5 对抗核过兜底，属受控。
- **收口前滚是自相矛盾防线**：`.ai/PROJECT.md`（butler 自身全貌产物）line 25/29 若不随本轮前滚，butler 自己的 digest 会与刚改的两态规则打架——已在收口步④落地（下方）。
- 收口非 hook 门禁，butler 仓不 live 跑自己的 hook（既有设计约束）；本迭代不新增 hook 需求。

# Handoff / Next Step

- 本迭代闭合，进原子收口五步（归档四件套+切片 / 交付 md+html / 翻台账 current=none + ITER-0031 行 closed + MILESTONE R5 行 closed + 范围演进 R5 收口 / `.ai/PROJECT.md` 前滚[读序两态 + R5 指针已接线] / 收口自检 6 不变量）。北极星=ITER-0031（MILE-0003 R5·冷启动读序切换）达成。
- 归属 MILE-0003 R5；收口后 MILE-0003 仍 active，剩 R6（部署迁移）/R7（说人话）/R8（butler 自身 dogfood + 切 v2.0.0），待用户指令。本轮按惯例收口即提交（不推送、不切版）。
