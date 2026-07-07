# Task State

> 无活跃迭代 · MILE-0003 active（R1/ITER-0026 + R2/ITER-0028 + R3/ITER-0029 已收口）· ITER-0029 收口 2026-07-07。

## 当前状态

- 无活跃迭代（`ITERATIONS.current: none`）。
- **ITER-0029（MILE-0003 R3）已收口 2026-07-07**：把 R2 声明的知识文件夹折叠模型接线成活跃收口仪式——泛化收口步④为两态（文件夹态按主题必做折叠 / 单文件暂态按需前滚，`iteration-schema §5.5` + `milestone-schema §7.4`）+ `context-persistence §冷启动一致性自检` 加第 6 条「知识文件夹漂移自检」（条件不变量、单文件 N/A）+ 全仓 5→6 计数同步（lifecycle / versioning / iteration §5.5 步⑤）+ 顺修 R2 遗留 §5→§6 及介绍段漂移 + 翻 `project-digest §6/§9` R3 指针（待→已）。交付 `deliveries/ITER-0029-maintenance-loop-wiring.md`。8/8 AC、P5 独立复核 APPROVE-WITH-NITS（0 Must Fix，两态兼容 5 处逐处 confirm，Should Fix 已修）。
- **两态兼容硬约束**：R6 部署种子 / R8 butler 自身迁移未落地，含 butler 自己在内多数项目仍单文件 `.ai/PROJECT.md`；折叠强制 + 第 6 不变量只对已采用 `.ai/project/` 的项目生效，单文件项目走旧按需前滚、第 6 条 N/A。
- 里程碑 **MILE-0003** 仍 active、R1+R2+R3 已收口（含迭代 ITER-0026, ITER-0028, ITER-0029）；本轮收口已提交（见下），未推送、未切版。

## 下一步入口

- 等用户指令：开 MILE-0003 剩余路线项（R4 更新说明+查过时帮手 / R5 冷启动读序切换 / R6 部署种子+迁移 / R7 说人话 / R8 butler 自身 dogfood）；或开新独立迭代。
- MILE-0003 收口（R8）时切 **v2.0.0**（MAJOR）+ 迁移配方 + tag。
- 若要把 ITER-0029 推送到远端，需用户明示（`git push github main`）。
