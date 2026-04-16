# Goal

- 修复 Butler Should Fix Bucket D（模板重复消除）1 条问题：`templates/CLAUDE.md.template` 与 `templates/rule-card.md` 在"角色 / 工作流 / 回退规则 / 基地车部署 / 执行纪律"等内容上高度重复，且与 `mcv-deployment.md § 3` 的部署流程描述存在角色冲突。

# Current Understanding

- 本任务是 Butler 规则仓维护的第六轮（也是 Should Fix 最后一轮）。Bucket C 已随 commit `6ecffb6` 落地。
- **现有矛盾**：
  - `templates/rule-card.md` 自我定位为"浓缩规则卡，可直接内联到 CLAUDE.md / .cursorrules"。
  - `templates/CLAUDE.md.template` 顶部注释说"本文件是 AI 部署基地车时生成 CLAUDE.md 的参考模板"，且其"强制约束（内联规则卡）"段几乎复制 rule-card 的全部内容。
  - `mcv-deployment.md § 3 规则注入` 规定部署流程是"从 `templates/rule-card.md` 读取浓缩规则，直接写入文件正文" —— **完全没有提及** `CLAUDE.md.template` 的存在。
- **本质**：两份模板做同一件事，但 mcv-deployment 只指了 rule-card 一条线，CLAUDE.md.template 自称"由部署流程生成"却被孤立。这导致：
  - 修改强制约束需要双写
  - 不同读者会按不同模板执行（有人按 mcv-deployment + rule-card，有人按 CLAUDE.md.template）

# Constraints

- 显性约束：
  - 不破坏 `mcv-deployment.md § 3` 的部署语义（rule-card 内联 + 深度阅读指针 + 项目特定约束）。
  - 不破坏 `CLAUDE.md`（butler 仓自身的项目规则文件）的"保持模板同步"要求 —— 修复后这个要求要么自动满足（单一来源），要么显式说明在哪里同步。
  - 任何方案必须保证基地车部署后目标项目 CLAUDE.md 的产出**在内容上**与现行版本等价。
- 隐性约束：
  - 模板对人类的可读性（不应让"骨架 + 占位符"丢失"长这样"的直观感）。
  - mcv-deployment.md 的部署步骤如有变更，需同步更新。

# Impact Scope

预计修改文件（取决于方案选型）：
- `templates/CLAUDE.md.template`（删除 / 改造为骨架 / 不动）
- `templates/rule-card.md`（保留 / 合并 / 不动）
- `Coder/20_Workflow_Lifecycle/mcv-deployment.md § 3`（部署步骤可能更新）
- `CLAUDE.md`（项目根，"保持模板同步"约束语义可能变）

不影响：lifecycle 的 P1-P5 状态机、其他 schema、Extension 文件、scripts、context-persistence、role-switch 等。

# Project Type / Active Profiles

- 项目类型：Markdown 规则仓库。
- 未命中任何 Domain Profile。

# Open Questions

- **D-1** 4 个候选方案需要用户拍板（见 AC_LIST），关系到 templates/ 目录的最终结构与部署流程的措辞。
