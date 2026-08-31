---
description: 按独立需求身份拆分、更新或查询 PRD——日期化 prd_id / 工作区筛选 / 版本同步
argument-hint: "[status [prd_id] [--workspace key] | update <prd_id> <新版材料> | split [--first-seen YYYY-MM-DD] <PRD材料>]"
---

你正在执行 butler 的 **PRD 先行**动作。本命令是**薄壳路由器**——只做三件事：① 保证把对的规则读进上下文（治"该响应时没响应"的老病），② 按参数分派，③ 委托真源规则执行。**具体算法一律以被指向的规则文件为准，本文件不复述**（守 butler DRY 红线）。

> **路径约定（本命令可在任意项目里运行，当前目录不一定是 butler 仓）**：下文引用的 `Coder/…` 都是 **butler 规则仓库**里的文件，一律相对 `$BUTLER_PATH`（`setup.sh` 全局安装时写入的环境变量；编辑 butler 仓本身时就是仓库根）解析——**不是**当前项目下的路径。若当前目录没有 `Coder/`，就去 `$BUTLER_PATH/Coder/…` 读。反过来，一切产出（`.ai/references/prd/…` 等）一律落**当前项目**，绝不落 butler 仓。

> **项目根硬门**：读写 PRD 项目状态前先按 `$BUTLER_PATH/Coder/20_Workflow_Lifecycle/mcv-deployment.md §0.1` 解析 `PROJECT_ROOT`。所有 `.ai/` 路径都相对它，不相对会话 `cwd` 或 butler 仓。

## 第 0 步（强制）先读契约
无论走哪条分支，先读 `Coder/40_Context_Management/references-schema.md`——PRD 集合、`prd_id`/`module_slug`、身份四态、逐字无损与独立版本的公共契约，不可跳。

## 按 `$ARGUMENTS` 路由

**分支 A ─ 以 `split` 开头、留空，或给了一段 PRD 文本 / 文件路径 → 身份判断与首切**
读 `Coder/40_Context_Management/prd-split.md`。先判 `new-requirement/new-version/duplicate/ambiguous`；只有全新需求才用有证据的首次进入日期提议 `prd_id`，并把身份、模块边界和 Workspace Scope 一次 soft 对齐后写到 `<prd_id>/`。`--first-seen YYYY-MM-DD` 是显式日期证据，不等于跳过身份闸；未给且项目证据不足就停问，不能拿当前日期补。
　└ 若 `$ARGUMENTS` 为空且对话里也没有 PRD 材料 → 先问用户 PRD 从哪来（粘贴 / 文件路径 / `.ai/references/raw/`），拿到材料再切。

**分支 B ─ 以 `update` 开头 → 指定需求改版**
`update` 后必须给唯一 `prd_id` 与新版材料；省略或 identity 不匹配就停止。读 `Coder/40_Context_Management/prd-update.md`，先完成 diff/认亲/影响处置 soft 对齐并生成 update spec，再调用 `$BUTLER_PATH/tools/prd-update/prd_update.py plan`；只有 `apply_ready` 才调用 apply。不得在宿主侧手工覆盖 live 或伪造 receipt。

**分支 C ─ 以 `status` 开头 → 只读看板**
读 `Coder/40_Context_Management/prd-status.md`，调用 `$BUTLER_PATH/tools/prd-status/prd_status.py status --project-root "$PROJECT_ROOT"`；后续可带 `--prd-id <id>` 与/或 `--workspace <key>`。必须保留工具退出码和 legacy/malformed 提示，不能在宿主侧另扫目录或写缓存。

## 收尾
执行完，一句话回报用户：走了哪条分支；split/update 说明动了哪些文件，status 明确说明零写入。
