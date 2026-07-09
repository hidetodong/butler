# 01_CHANGELOG — ITER-0041（MILE-0004 R6 · 认亲边缘 + 非回归门 + 收尾）

> 本文件是**当前活跃迭代 ITER-0041** 的对象级变更流（ADD/EDIT/DELETE）。P4 执行时回填；收口时切片归档至 `iterations/ITER-0041/CHANGELOG.md`。

## EDIT · `Coder/40_Context_Management/prd-update.md`（认亲对账松边 → AC1/AC2）

- §4 标题从"登记表认亲基础态（只做新增/消失）"改为"登记表认亲：基础态（新增/消失）+ 松边（改名/合并/拆分）"；引言改为分两层（先基础态、套不上再松边）。
- 拆出 **§4.1 基础态**（新增/消失，原两条 bullet 保留 + 补"纯增/纯消到此为止不必往下猜"）。
- 新增 **§4.2 松边**：仅当"slug 消失 + slug 新增"同次出现才可能是改名/合并/拆分；启发式提候选（一对一近似→改名、一对多→拆分、多对一→合并）**只提不改**；认亲落法守 slug 终身（改名保留旧 slug 只换标题/章节、合并拆分按用户确认发新 slug + 旧置 removed）；**松边红线·宁可不认也不误并**（拿不准退回 §4.1 基础态）。
- frontmatter scope：认亲基础态 → "认亲（基础态 + 松边）"，删去句尾"模块合并/拆分/改名认亲见 MILE-0004 R6"。

## EDIT · `Coder/40_Context_Management/references-schema.md`（非回归门 + flip → AC3/AC5）

- 新增 **§9 非回归门**：显式列出 PRD 子系统作为 opt-in 加层**不得触碰**的五条非 PRD 流（对话驱动录入 / `origin/` brief / 扁平态 references 注入 / 核心 P1–P5 状态机 / 里程碑非 PRD 合成）+ 各自真源；**验证判据成文 = 这些文件/路径 `git diff` 为空**。
- flip §4 认亲边缘句：`属 MILE-0004 R6` → **已由 `prd-update.md §4.2`（松边）落地**。
- flip §8 前向指针表 R6 行：`R6` → **R6 ✅ 已由 `prd-update.md §4.2` 落地**（至此 §8 表 R1–R6 全绿）。
- frontmatter scope：补"非回归门"、动作范围 R2–R5 → R2–R6（+认亲）。

## EDIT · `HUMAN_GUIDE.md`（PRD 先行用法节 → AC4）

- §5 扩展模式在"里程碑"与"`/review`"之间插入 **PRD 先行（大规格版本化）** 节：人话讲清定位（有损路线图扛不住组件细节、切片逐字兜底、opt-in）、首切随 `/milestone` 触发、`/prd update`（改版同步：清单优先+diff 防漏、先冻旧版再更、三态影响面、每步确认）、`/prd status`（只读看板）、绝不静默动已冻结/已收口工作；机制真源回指 `prd-update.md`。

## EDIT · `Coder/README.md`（收尾·flip 过时指针 → AC7 收尾/独立复核 Should Fix）

- 目录说明 prd-update 行的"合并/拆分/改名留 R6"过时指针 flip 为"松边：启发式提候选→确认、拿不准退回基础态、见 §4.2，R6 落地"。

## 自检 · 说人话（AC6）

- `references-schema` / `prd-split` / `prd-update` 三份过说人话三条：松边 / 非回归门 / opt-in 加层 / 启发式 均首现带解释，slug/soft 对齐/认亲已在既有正文解释，无裸英文变量。零星修正：无（新增内容自带解释、旧文本合规）。
