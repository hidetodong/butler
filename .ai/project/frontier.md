# frontier（当前形态 / 活跃战线 / 下一个瓶颈）

> 变得最快的一层。战线收了就覆盖删除，不叠历史。

## 当前形态

- **版本**：**v2.0.0 已发布**（MILE-0003 收尾切版，MAJOR——冷启动核心产物契约破坏性重构）。上一版 v1.7.0。本版之后的迭代均未再切版。
- **活跃里程碑 MILE-0004**（"PRD 先行 + references 版本化改版同步"，2026-07-08 开启）：给 `.ai/references/` 补上当年只给了 `.ai/project/` 的"索引 + 渐进读"待遇，并新增 PRD 先行入口与改版同步协议。路线图 R1–R6 见 `.ai/MILESTONE.md §5.3`。
- **R1（ITER-0036）已收口**：新建 `Coder/40_Context_Management/references-schema.md`——references 子系统首份结构契约（`prd/00_INDEX` + 模块登记表 slug 身份 + digest-and-point 读纪律 + "索引可摘要/切片必逐字原文"硬区分 + live/`.archive` 落盘）。**只定契约地基、不做产生动作**。

## 活跃战线

- **MILE-0004 契约地基已浇（R1），下一步砌动作层**：R1 把 references/prd 的结构、身份、读法、落盘一次定死；R2–R5 才是真正把 PRD 切成片、从 `/milestone` 触发首切、给 AC 钉版、`/prd update` 改版同步的**产生动作**。
- **贯穿整个里程碑的命门红线已立**：PRD 切片必须逐字原文、无损，绝不能拿 `.ai/project/` 的有损 overwrite 概括去套（`references-schema §6` 硬约束）——这条要在 R2 真切分时靠执行遵从守住。

## 下一个瓶颈

- **紧接 R2 · PRD 切分机制**：按语义/模块边界切 `prd/<slug>.md`（逐字保真）+ 写登记表 + 小 PRD 单模块退化态 + soft 对齐拆法（提议→确认、绝不切碎一条规则）。这是把 R1 契约"真踩上去"的第一步，也是最先能证伪契约设计的地方。
- **两笔历史欠债仍悬着**（见 `debt.md`）：hook 在 butler 侧不 live、`/butler-upgrade` 从未真跑——后者带 `[split]` 迁移的升级执行器接线已于 ITER-0035 补齐（`butler-upgrade §6.5` opt-in 选择闸就位），就差真实老项目端到端跑一遍。
