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

  /Coder
    README.md
    /00_System_Prompt
    /10_Engineering_Standard
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
