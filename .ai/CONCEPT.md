# Goal

- 修复 Butler Should Fix Bucket A（命名与读取顺序一致性）4 条问题：`/ideation` 触发词不一致、README 读取顺序与 architecture-overview 启用顺序冗余、mcv-deployment 标题层级偏差、mcv-update 升级后目录结构命名风格裂痕。

# Current Understanding

- 本任务是 Butler 规则仓维护的第二轮。上一轮 Must Fix 修复的决策链产物已随 commit `8febaf3` 归档到 git 历史，本轮覆写 `.ai/` 下的 CONCEPT/AC_LIST/TECH_PLAN/VERIFY_REPORT 作为新任务决策链。
- Bucket A 4 条问题都属"表述对齐/格式统一"，无契约变更、无跨模块行为影响，属低风险。
- 其中 2 条存在设计取舍，需在 P2 AC_LIST 中请用户拍板：
  - AC-2（README vs architecture-overview 的 SSOT 归属）
  - AC-4（归档命名策略是否作为规则落地）

# Constraints

- 显性约束：
  - 不破坏三层分工（SOP Core / Domain Profiles / Business Extension）。
  - 不破坏产物链（CONCEPT → AC_LIST → TECH_PLAN → VERIFY_REPORT）。
  - 不扩张到 Bucket B/C/D/E 的修复范围。
  - 保留 AC-4 方案 A 的结果（`.md` 路径引用统一带 `02_` 前缀）。
- 隐性约束：
  - 中文行文，标识符与文件名保持英文。
  - 每个规则文件的 frontmatter 必须保留 audience / scope（由 Must Fix 修复后已成立）。

# Impact Scope

预计修改文件：
- `Coder/00_System_Prompt/logic-protocol.md`（AC-1 触发词同步）
- `Coder/50_Extension_Ideation/ideation-engine.md`（AC-1 作为 SSOT，可能不需改，仅核对）
- `HUMAN_GUIDE.md`（AC-1 触发词同步）
- `Coder/README.md`（AC-2 取决于方案）
- `Coder/architecture-overview.md`（AC-2 取决于方案）
- `Coder/20_Workflow_Lifecycle/mcv-deployment.md`（AC-3 标题层级 + 可能 AC-4 命名策略说明）
- `Coder/20_Workflow_Lifecycle/mcv-update.md`（AC-4 目录示例修复）

不影响：除上述文件之外的所有规则文件、templates/、scripts/、.ai/ 产物链结构本身。

# Project Type / Active Profiles

- 项目类型：Markdown 规则仓库（butler 自举维护）。
- 未命中任何 Domain Profile。
- 仅按通用 SOP 推进。

# Open Questions

- **AC-2** README 与 architecture-overview 谁做 SSOT 需要用户拍板。
- **AC-4** 归档命名是否作为新规则落到规则文件里需要用户拍板。
