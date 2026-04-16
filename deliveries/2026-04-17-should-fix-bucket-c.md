# Butler 规则仓库 Should Fix Bucket C 交付总结

> 日期：2026-04-17
> 任务：修复 Should Fix Bucket C（Mode 术语双关消歧）1 条问题
> 状态：已完成，可交付

## 本次交付目标

修复 Butler Should Fix Bucket C：消除 `logic-protocol.md` 的 Standard/Ideation/Loop/Review "Mode"（运行时能力激活）与 `mode-switch.md` 的 Architect/Coder/Reviewer "Mode"（同一执行者职责切换）的术语双关。

## 已完成内容

| # | 问题 | 修复方式 |
|---|---|---|
| 1 | `mode-switch.md` 与 `logic-protocol.md` 共用 "Mode" 术语，读者难以区分 | 方案 Alpha：保留 logic-protocol 的 Mode（运行时能力侧），把 mode-switch 侧改为 "Role"；文件重命名为 `role-switch.md`，全部引用同步 |
| 2 | 内部 7 处 `Mode` + 11 处 `模式` | 两次 `replace_all` 一把过：`Mode → Role`、`模式 → 角色` |
| 3 | 外部 2 处文件名引用 | `context-persistence.md:124` 与 `Coder/README.md:62` 同步更新到 `role-switch.md` |

## 关键变更 / 用户可感知变化

- **术语边界明确**：
  - **Mode** 现在专指 logic-protocol § 4 的运行时能力激活（Standard / Ideation / Loop / Review），与 `/xxx` 命令绑定。
  - **Role** 现在专指 role-switch.md 中的执行者职责切换（Architect / Coder / Reviewer），与 P1-P5 阶段映射。
- **文件名传达概念**：原 `mode-switch.md` 看名字易误读为"扩展模式切换"，新 `role-switch.md` 一眼能知其为"角色切换"。
- **git 历史血缘保留**：通过 `git mv` 重命名，commit 后 `git log --follow Coder/40_Context_Management/role-switch.md` 可完整追溯原 mode-switch.md 历史。

## 高层影响范围

**直接修改 3 个规则文件**（含 1 个重命名）：

- `Coder/40_Context_Management/mode-switch.md` → `Coder/40_Context_Management/role-switch.md`（rename + 内部全文术语替换 18 处）
- `Coder/40_Context_Management/context-persistence.md`（L124 引用更新）
- `Coder/README.md`（L62 目录结构更新）

**未影响**（保留区已显式声明）：
- `Coder/00_System_Prompt/logic-protocol.md § 4`（Standard / Ideation / Ralph-Loop / Review Mode 完整保留）
- `Coder/20_Workflow_Lifecycle/`、其他 schema、Extension 文件、`templates/`、`scripts/`、`Learner/`、`Composer/`
- `deliveries/` 下的历史交付文档（按惯例不改历史记录）

## 验证方式与结果摘要

| 验证动作 | 结果 |
|---|---|
| `ls Coder/40_Context_Management/` | role-switch.md 存在，mode-switch.md 不存在 ✅ |
| `grep 'Mode' role-switch.md` / `grep '模式' role-switch.md` | 0 / 0 命中 ✅ |
| `grep 'Role' role-switch.md` / `grep '角色' role-switch.md` | 7 / 11 命中 ✅ |
| `grep -rn 'mode-switch' Coder/` | 0（活跃文件无残留） ✅ |
| `grep -rn 'role-switch' Coder/` | 2（README + context-persistence） ✅ |
| `grep 'Standard Mode\|Ideation Mode\|Ralph-Loop Mode\|Review Mode' logic-protocol.md` | 4 处完整保留 ✅ |
| `git status` | RM 标记（rename + modified） ✅ |

详细验证记录见 `.ai/VERIFY_REPORT.md`。

## 已知剩余风险 / 延后事项

### 历史交付文档保留旧引用

`deliveries/2026-04-17-must-fix-repair.md:38` 仍含 `mode-switch.md` 字样，按"历史交付文档不修改"惯例保留。如未来需要批量重写历史，可单独处理。

### 未处理的 Should Fix（1 条）

- Bucket D（模板重复消除，1 条）

完成 Bucket D 后，**全部 11 条 Should Fix 即可全部闭环**。

## 可选引用

- 产物链：`.ai/CONCEPT.md`、`AC_LIST.md`、`TECH_PLAN.md`、`VERIFY_REPORT.md`
- 关联规则：
  - `Coder/40_Context_Management/role-switch.md`（重命名后的目标文件）
  - `Coder/40_Context_Management/context-persistence.md § 7`（同步引用点）
  - `Coder/00_System_Prompt/logic-protocol.md § 4`（保留区，Mode 术语未动）
- 前四轮交付：
  - `deliveries/2026-04-17-must-fix-repair.md`
  - `deliveries/2026-04-17-should-fix-bucket-a.md`
  - `deliveries/2026-04-17-should-fix-bucket-e.md`
  - `deliveries/2026-04-17-should-fix-bucket-b.md`
