---
description: 把权威 PRD 拆进项目知识库，并随改版保持同步——首次拆分 / 改版对齐 / 只读看板
argument-hint: "[status=只读看板 | update=改版同步 | 贴 PRD 或路径；留空=首次拆分]"
---

你正在执行 butler 的 **PRD 先行**动作。本命令是**薄壳路由器**——只做三件事：① 保证把对的规则读进上下文（治"该响应时没响应"的老病），② 按参数分派，③ 委托真源规则执行。**具体算法一律以被指向的规则文件为准，本文件不复述**（守 butler DRY 红线）。

> **路径约定（本命令可在任意项目里运行，当前目录不一定是 butler 仓）**：下文引用的 `Coder/…` 都是 **butler 规则仓库**里的文件，一律相对 `$BUTLER_PATH`（`setup.sh` 全局安装时写入的环境变量；编辑 butler 仓本身时就是仓库根）解析——**不是**当前项目下的路径。若当前目录没有 `Coder/`，就去 `$BUTLER_PATH/Coder/…` 读。反过来，一切产出（`.ai/references/prd/…` 等）一律落**当前项目**，绝不落 butler 仓。

## 第 0 步（强制）先读契约
无论走哪条分支，先读 `Coder/40_Context_Management/references-schema.md`——PRD 切片的**契约层**：`prd/` 结构、slug 终身身份、逐字无损红线、live/`.archive` 落盘形态、§2 "是不是大 PRD"的判据。这是所有分支的公共地基，不可跳。

## 按 `$ARGUMENTS` 路由

**分支 A ─ 留空，或给了一段 PRD 文本 / 一个 PRD 文件路径 → 首切**
读 `Coder/40_Context_Management/prd-split.md`，按其程序把这份 PRD 切成 `.ai/references/prd/` 知识文件夹：按 PRD 自身模块边界切（**绝不切碎一条完整规则**）、每模块分终身 slug、写 `00_INDEX`/登记表、每片逐字保真。**soft 对齐红线**：先提议切分方案 → 用户确认 → 才落盘，**绝不擅自硬切**；小 PRD 走单模块退化态、不退扁平。
　└ 若 `$ARGUMENTS` 为空且对话里也没有 PRD 材料 → 先问用户 PRD 从哪来（粘贴 / 文件路径 / `origin/`），拿到材料再切。

**分支 B ─ 以 `update` 开头 → 改版同步**
读 `Coder/40_Context_Management/prd-update.md`，按其程序同步一份**已切进来**的 PRD 的新版本：变更检测（修改项清单优先 + old/new diff 兜底 + 对账，分歧必亮）→ 重新派生受影响模块 →**先冻旧版 `.archive/v<旧版>/` 全量快照、再更 live**（硬顺序，不可颠倒）→ 登记表认亲（新增/消失/合并/拆分/改名）→ 三态影响面报告（没开工/进行中/已收口，**亮牌不自动默认**）→ 受影响工作路由。

**分支 C ─ 以 `status` 开头 → 只读看板**
读 `Coder/40_Context_Management/prd-update.md §7`，**只读汇总、不改盘**：当前 `prd/` 有哪些 slug、各自版本/状态、最近一次 update 的三态影响面快照。定位同 `/milestone status`——只读看板，不是改版入口；真要改版走分支 B。

## 收尾
执行完，一句话回报用户：走了哪条分支、动了哪些 `.ai/references/prd/` 下的文件。
