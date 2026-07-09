---
状态: ack-frozen
ACK 日期: 2026-07-09
迭代: ITER-0041
里程碑: MILE-0004（R6·收官）
---

# AC_LIST — ITER-0041（MILE-0004 R6 · 认亲边缘 + 非回归门 + 收尾）

> 监督态自驱。全为规则文档接线（扩 `prd-update §4` + `references-schema` 加非回归节/flip §4·§8 + HUMAN_GUIDE 用法节 + 说人话自检），验证 = 读改后正文核契约 + `git grep`/`git diff` 核守恒 + 非回归核对，确定性可复现（auto·可靠）。**待 ACK 冻结后方可进 P4。**

## 块1 · 认亲对账松边

- **AC1（认亲对账扩 `prd-update §4`·松边·不改改版主流程）**：`prd-update.md §4` 从"只做新增/消失"扩为含**改名 / 合并 / 拆分**跨版本认亲对账——检测到"slug 消失 + slug 新增"时**启发式提候选**（标题/内容相近→改名；一消失对多新增→拆分；多消失对一新增→合并），**提议 → 用户确认、绝不自动认**。改动限于 §4，`prd-update §2/§3/§5/§6`（检测/落盘/三态/路由）**不动**。
- **AC2（认亲落法·守 slug 终身 + 松边退化）**：成文——**改名**认亲 = 保留旧 slug、只更新标题/章节（守 `references-schema §4` slug 终身、换门牌不换身份证）；**合并/拆分** = 按确认落 slug 关系 + 登记表状态。**松边红线**：拿不准就退回"新增/消失"两条独立记录，**宁可不认也不误并**（认错身份比不认更坏）。

## 块2 · 非回归门

- **AC3（非回归门·常驻可验证红线）**：`references-schema` 新增一节，显式列出 PRD 子系统作为 opt-in 加层**不得触碰**的非 PRD 流——对话驱动 / `origin/` brief / 普通 references 注入（`api-`/`design-`/`insight-`）/ 核心 P1–P5 状态机 / 里程碑非 PRD brief 合成；**验证判据成文 = 改本子系统时这些文件/路径 `git diff` 为空**。把散落各迭代 AC 的口头承诺固化成一处可核对契约。

## 块3 · 收尾（用法 · flip · 说人话）

- **AC4（HUMAN_GUIDE 加"PRD 先行"用法节）**：HUMAN_GUIDE §5 扩展模式加一节，人话讲清 `/prd update`（改版同步：给新版 + 说改了啥 → 检测/重切/冻旧版/报三态影响面，每步确认）+ `/prd status`（只读看板），摆在里程碑节附近；口径与规则真源一致、不新造语义。
- **AC5（flip R6 收口指针）**：`references-schema §4`（合并/拆分/改名认亲边缘那句）+ `§8` 前向指针表 R6 行 flip 为 **✅ 已落地**（指 `prd-update §4`）。至此 §8 表 R1–R6 全绿。
- **AC6（全子系统说人话自检·dogfood）**：`references-schema` / `prd-split` / `prd-update` 三份过说人话三条（术语先解释 / 比喻落地 / 别让英文·变量裸奔），发现问题当场修；本迭代四件套同守。认亲 / 改名 / 合并 / 拆分 / 非回归门 / opt-in 加层等首现带解释。
- **AC7（scope 守恒 + 非回归 + 分层 + 收官核对）**：改动集限于 `prd-update.md §4`（认亲对账）+ `references-schema.md`（加非回归节 + flip §4·§8）+ `HUMAN_GUIDE.md`（PRD 用法节）+ 说人话自检触发的零星修正。**不改** R1–R5 主体（契约结构/切分算法/钉版字段/改版主流程 §2/§3/§5/§6）；**不做**全自动认亲；**不碰**非 PRD 流（本轮亲自守）/ `project-digest` / `context-persistence` / hook / `VERSION`；**不切版**（收口 MILE-0004 + 切版是独立发布动作、待放行）。分层不破坏（改动在 SOP Core `40` + 仓根 HUMAN_GUIDE）。收官核对：MILE-0004 §5.3 路线图 R1–R6 全部 ✅、`references-schema §8` 表全绿。
