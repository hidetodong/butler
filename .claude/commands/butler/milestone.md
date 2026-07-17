---
description: 开一个里程碑（大版本范围单元，聚合多个迭代），或只读看板看当前里程碑进度——留空/贴一段方向说明=录入开题，status=只读看板
argument-hint: "[status=只读看板 | 贴里程碑 brief 或路径 | 留空=录入 / 开里程碑]"
---

你正在执行 butler 的 **里程碑录入 / 看板**动作。本命令是**薄壳路由器**——只做三件事：① 保证把对的规则读进上下文，② 按参数分派，③ 委托真源规则执行。**里程碑号分配、四层落盘、录入协议、看板汇报口径一律以被指向的规则文件为准，本文件不复述**（守 butler DRY 红线）。

> **路径约定（本命令可在任意项目里运行，当前目录不一定是 butler 仓）**：下文引用的 `Coder/…` 都是 **butler 规则仓库**里的文件，一律相对 `$BUTLER_PATH`（`setup.sh` 全局安装时写入的环境变量；编辑 butler 仓本身时就是仓库根）解析。产出（`.ai/MILESTONE.md`、`.ai/MILESTONES.md`、`.ai/references/prd/…` 等）一律落**当前项目**，绝不落 butler 仓。

> **项目根硬门**：读台账前先按 `$BUTLER_PATH/Coder/20_Workflow_Lifecycle/mcv-deployment.md §0.1` 解析 `PROJECT_ROOT`。上文“当前项目”一律指该绝对路径；用户点名路径优先，歧义时零写入。

## 第 0 步（强制）先确认当前项目已接 butler
里程碑建立在当前项目的 `.ai/` 台账之上。开跑前先看当前目录有没有 `.ai/`（尤其 `.ai/MILESTONES.md`）：
- **有** → 正常往下走。
- **没有 `.ai/`（当前项目没接 butler）** → 别硬建，一句话告诉用户「当前项目没接 butler，里程碑需要 `.ai/` 台账；请先部署基地车、或确认在对的目录」。**不报错、不空跑。**

## 按 `$ARGUMENTS` 路由

**分支 A ─ 留空，或给了一段里程碑方向说明 / brief 文件路径 → 录入 / 开里程碑**
读 `Coder/20_Workflow_Lifecycle/milestone-schema.md`——先按 **§6.1 启动信号** 判断这是不是该开里程碑（够大、跨多迭代才开；极小任务不开），再按 **§6.4 录入（Brief）** 把方向 brief 合成 `.ai/MILESTONE.md`（范围评估 + 理解阐释 + 拆分路线图），并按 **§7.1 开启** 从 `.ai/MILESTONES.md` 读最大号 +1 分配 `MILE-NNNN`、登记台账。**soft 对齐红线**：拆分路线图先提议 → 用户确认 → 才定稿，绝不擅自硬拆。
　└ **若 brief 材料本身是大 PRD**（逐字权威规格）：按 §6.4 合成协议**并进**触发 `Coder/40_Context_Management/prd-split.md` 切成 `.ai/references/prd/`——一份输入同喂方向层路线图 + 细节层切片（见 §5.3 路线项↔slug 交叉指针）。

**分支 B ─ 以 `status` 开头 → 只读看板**
读 `Coder/20_Workflow_Lifecycle/milestone-schema.md §6.5`（`/milestone status` 定义），**只读汇总、不改盘**：读 `.ai/MILESTONES.md` + `.ai/MILESTONE.md`，汇报当前里程碑标题/状态、范围评估摘要、拆分路线图各路线项进度、已含迭代、下一个 `planned` 路线项；无 active 里程碑时如实报「当前无 active 里程碑」。**不写任何文件、不改状态。**

> 收口 / 废弃 / 演进不走命令、走语义（`milestone-schema.md §7.3/§7.4/§7.5`）——命令面只覆盖最高频的开题 / status（§6.5 已定）。

## 收尾
执行完，一句话回报用户：走了哪条分支、动了哪些 `.ai/` 台账文件（录入分支报新里程碑号 + 路线项条数；status 分支报当前进度摘要）。
