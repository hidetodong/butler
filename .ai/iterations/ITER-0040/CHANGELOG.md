# 01_CHANGELOG — ITER-0040（MILE-0004 R5 · 改版同步 `/prd update`）

> 本文件是**当前活跃迭代 ITER-0040** 的对象级变更流（ADD/EDIT/DELETE）。收口时切片归档至 `iterations/ITER-0040/CHANGELOG.md`。

## ADD · `Coder/40_Context_Management/prd-update.md`（新建改版同步动作层）

- ADD §1 定位：契约 vs 动作 + 回指表 + `prd-split` 管首切 / `prd-update` 管改版分工 + "改版走本机制非重新注入"。
- ADD §2 变更检测：清单优先 → diff 兜底 → 对账（分歧必亮、不静默采信任一方），产出受影响模块清单。
- ADD §3 重新派生 + 落盘：按 prd-split 重新派生受影响模块 + **硬顺序"先冻旧版 `.archive/v<旧版>/` 全量快照，再更 live"** + bump 全局版本，落盘回指 references-schema §7。
- ADD §4 登记表认亲基础态：新增发新 slug/首见版本=新版/active，消失置 removed、slug 不回收；合并/拆分/改名显式留 R6。
- ADD §5 三态影响面报告：没开工/进行中/已收口分类表 + **硬约束"亮牌不自动默认"**（只报告、绝不静默改已冻结/已收口工作）。
- ADD §6 受影响工作路由：进行中→amend 重冻（回指 `iteration-schema §5.3`+`acceptance-schema §4`）/ 已收口→开新迭代承接（回指 `iteration-schema §5.4`）/ 没开工→无动作；只回指不改仪式。
- ADD §7 `/prd status` 只读看板（当前版本 + 登记表 + 最近改版三态影响面，只读非改版入口）。
- ADD §8 soft 对齐硬约束：改版同 split 提议→确认→落盘，未经确认不得覆盖 live/冻快照/重冻 AC。

## EDIT · 接线

- EDIT `Coder/00_System_Prompt/logic-protocol.md` 注入表：大 PRD 行首切句尾补"已切进来的 PRD 出新版走 `prd-update.md` 改版同步、非重新注入"。
- EDIT `Coder/20_Workflow_Lifecycle/acceptance-schema.md §4`：`prd_version` bullet 的"属 `/prd update`"补指针 `（见 prd-update.md）`。
- EDIT `Coder/40_Context_Management/references-schema.md §7`：快照产生动作 bullet flip 为**已由 `prd-update.md §3` 落地**。
- EDIT `Coder/40_Context_Management/references-schema.md §8`：R5 行 flip 为 **✅ 已由 `prd-update.md` 落地**。
- EDIT `Coder/README.md`：结构树 `40_Context_Management` 注册 `prd-update.md`；说明段加 prd-update 描述行 + 顺修 prd-split 行尾"钉版/改版同步属 R4–R5"过时指针为"R4/R5 已落地"。
