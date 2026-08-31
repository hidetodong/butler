---
description: 在新项目部署 Butler 基地车——侦察技术栈、展开 .ai/ 基础设施、注入规则入口与 hooks
argument-hint: "[留空=部署当前目录项目]"
---

你正在执行 Butler 基地车首次部署。本命令是**薄壳路由器**——只做三件事：① 解析项目根，② 判断是否已部署，③ 委托 `mcv-deployment.md` 执行完整部署流程。**侦察、展开、注入、适配、hook 拷贝的具体规则一律以被指向的规则文件为准，本文件不复述**（守 butler DRY 红线）。

> **路径约定（本命令可在任意项目里运行，当前目录不一定是 butler 仓）**：下文引用的 `Coder/…` 都是 **butler 规则仓库**里的文件，一律相对 `$BUTLER_PATH` 解析。产出（`.ai/`、`CLAUDE.md`、`AGENTS.md`、`deliveries/`、`.claude/hooks/` 等）一律落**当前项目**。

## 第 0 步（强制）先确认 Butler 路径与项目根

1. 按 `$BUTLER_PATH/Coder/20_Workflow_Lifecycle/mcv-deployment.md §0` 发现 Butler 路径，记为 `$BUTLER_PATH`。
2. 按 `$BUTLER_PATH/Coder/20_Workflow_Lifecycle/mcv-deployment.md §0.1` 解析唯一 `PROJECT_ROOT`，回声绝对路径。

## 第 1 步（强制）判断是否已部署

检查 `$PROJECT_ROOT/.ai/` 目录是否存在：
- **已存在** → 「当前项目已部署 Butler（`.ai/` 已存在），无需重复初始化。如需升级请用 `/butler:upgrade`。」终止。
- **不存在** → 继续。

## 第 2 步 执行完整部署

按 `$BUTLER_PATH/Coder/20_Workflow_Lifecycle/mcv-deployment.md` 顺序执行全部章节：

1. **§1 侦察**：扫描技术栈、项目结构、命中 profile，汇报摘要。
2. **§2 基础设施展开**：创建 `.ai/` 与 `deliveries/` 两个目录。
3. **§3 规则注入**：运行 `python3 "$BUTLER_PATH/scripts/render-project-entrypoints.py" --target "$PROJECT_ROOT" --butler-root "$BUTLER_PATH"` 生成 `CLAUDE.md` + `AGENTS.md`。
4. **§4 本地化适配**：生成只含人类可读差异的 `.ai/local-constraints.md`，并用驻留 project-config 工具生成安全默认 `.ai/butler.config.json`；profile 只写 JSON。
5. **§5 Hook 注入**：拷贝 `$BUTLER_PATH/templates/hooks/`（除 `tests/`）到 `$PROJECT_ROOT/.claude/hooks/`，并配置 `.claude/settings.json`。

## 第 3 步 委托 setup（机器级）

部署完项目后，提醒用户可用 `/butler:setup` 安装机器级命令/扩展。若用户同意，按 `$BUTLER_PATH/Coder/20_Workflow_Lifecycle/butler-setup.md` 委托 setup 工作流；本命令不复制其路径、授权、执行或结果判断算法。

若跳过，明确告知「全局命令（/butler:*）和 Pi/Codex 扩展可稍后用 `/butler:setup` 安装；完全空白机器的首次 bootstrap 仍需从 Butler 仓运行 `bash scripts/setup.sh`」。

## 收尾

逐条汇报：项目根路径、技术栈/命中 profile、已创建目录、入口文件、hooks 状态、全局安装结果。最后一句：「基地车部署完成，可以开始工作了。」
