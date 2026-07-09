> ITER-0037 · MILE-0004 R2 · PRD 切分机制 · 收口即归档

本文件是**当前活跃迭代**的对象级变更流（ADD/EDIT/DELETE）。收口时归档至 `iterations/ITER-0037/CHANGELOG.md`。

## ADD

- `Coder/40_Context_Management/prd-split.md`（新建）：references-schema 契约的**产生动作层**（R2）。§1 定位（履行契约、契约 vs 动作分工 + 回指真源表）· §2 边界识别（按 PRD 自身语义/模块边界切、**绝不切碎一条完整规则**红线、宁粗不碎）· §3 slug 首切分配 + 写 `00_INDEX`/登记表（守 references-schema §3/§4）· §4 逐字保真（每片原文无损投影、守 §6 命门）· §5 小 PRD 单模块退化态（模块数=1 同一套模型、不退扁平）· §6 soft 对齐（提议→确认→落盘三拍 + 硬约束"未确认不得落盘"、同 [split]/[add-field] 信任模型）。只管首切。

## EDIT

- `Coder/00_System_Prompt/logic-protocol.md` §外部参考资料注入：类型表补一行"大/结构化 PRD → 走 `prd-split.md` 切成 `prd/` 知识文件夹态（提议→确认→落盘）"，判据回指 `references-schema §2`、不双写。
- `Coder/40_Context_Management/references-schema.md` §8：flip R2 前向指针（"把 PRD 切成 `prd/<slug>.md`" 由待落地 → **✅ 已由 `prd-split.md` 落地**）。
- `Coder/README.md`：目录结构树 `40_Context_Management` 下 `references-schema.md` 后补 `prd-split.md`；规则说明段补一条（产生动作层定位 + 只管首切 + 契约字段回指 references-schema）。

## DELETE

- 无
