---
title: 基地车 (MCV) 部署协议
trigger: 新项目接入 或 显式指令 "Deploy Base Vehicle"
priority: High
---

# 基地车部署协议 (MCV Deployment)

### 1. 落地前侦察 (Scouting)

在创建任何目录前，AI 必须执行以下动作并简要汇报：

- 扫描根目录判断技术栈 (`package.json`, `tsconfig.json`)。
- 识别项目结构 (`src`, `packages`, `docs`)。
- **批判性任务：** 如果发现当前项目环境与 `10_Engineering_Standard` 冲突，必须在部署报告中指出。

### 2. 基础设施展开 (Scaffold)

在项目根目录强制创建 `.ai/` 文件夹，并初始化以下“黑匣子”组件：

- `01_CHANGELOG.md`：需求增量与架构决策。
- `02_SESSION_HANDOFF.md`：跨会话状态锚点。
- `03_BUG_LOG.md`：高价值逻辑坑位记录。

### 3. 本地化适配 (Local Adaptation)

- 生成 `.ai/local-constraints.md`。
- **逻辑：** 不要复制通用规则，而是通过“指针”引用。例如：“本项目遵循通用 Vue 3 规范，但针对旧代码引用，允许在 `/legacy` 目录下局部放宽类型检查。”
