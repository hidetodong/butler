# butler

一个面向个人助理协作的 Markdown 仓库。

当前仓库包含三个可独立引用的子系统：

- `Coder/`：工程开发与 AI 协作规则体系
- `Learner/`：学习事务管理入口
- `Composer/`：除开发与学习之外的杂项事务入口

## 子系统入口

每个子系统目录都可以被其他应用或文件直接引用作为入口，入口文件如下：

- `Coder/README.md`
- `Learner/README.md`
- `Composer/README.md`

根目录 `README.md` 只负责总览与分流，不替代各子系统自己的入口说明。

## 目录结构

```txt
/butler
  README.md
  CLAUDE.md
  HUMAN_GUIDE.md

  /scripts
    setup.sh

  /templates
    CLAUDE.md.template
    rule-card.md

  /Coder
    README.md
    architecture-overview.md
    /00_System_Prompt
    /10_Domain_Stack_Profiles
    /20_Workflow_Lifecycle
    /30_Quality_Gate
    /40_Context_Management
    /99_Business_Extension

  /Learner
    README.md

  /Composer
    README.md
```

## 使用方式

- 当目标是软件工程、编码协作、规则执行时，从 `Coder/` 进入。
- 当目标是学习计划、知识沉淀、学习事务管理时，从 `Learner/` 进入。
- 当目标属于其他生活/事务性杂项时，从 `Composer/` 进入。

## 快速上手

1. **一次性安装**：`./scripts/setup.sh` — 写入全局配置，之后所有项目自动发现 butler
2. **接入新项目**：直接给任务 — AI 自动从入口读取规则，检测到新项目后自动部署基地车
3. **详细说明**：阅读 `HUMAN_GUIDE.md`

> 开发按**迭代**推进：每个迭代有递增迭代号 `ITER-NNNN`，需求 ACK 后冻结，对应文档落盘并归档到 `.ai/iterations/`。机制详见 `Coder/20_Workflow_Lifecycle/iteration-schema.md`，用法详见 `HUMAN_GUIDE.md`。
