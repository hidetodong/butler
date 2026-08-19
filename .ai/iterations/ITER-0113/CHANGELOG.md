<!-- butler-artifact-template: 1.0.0 artifact=changelog -->
# ITER-0113 变更流

> 冷启动读序正式定义与四载体对齐（MILE-0016 R2） · closed · 2026-08-19

## ADD

- `Coder/40_Context_Management/context-persistence.md §6`：读序正文由 `butler-context-order:begin/end` 一对标记圈定，成为唯一真源（1194 字节 / 6 非空行 / 7 个 md 指针）；块外补一段说明，写明四处投影与「改读序只改本节」的纪律 → AC1
- `templates/CLAUDE.md.template`「会话起始：恢复项目状态」章节：Claude 宿主入口首次带上冷启动读序块 → AC2
- `tools/context-budget/context_budget.py` `_marker_block()`：从 `_l0_block()` 提取出的通用标记块提取器，标记名可传入，两道 fail-closed 检查（各恰好一次 / 不得交错）不变 → AC3
- `tools/context-budget/context_budget.py` `_order_block()` / `_order_steps()` / `_order_structure_errors()`：读序块提取、步骤切分与三类结构断言（编号连续 `1..5`、每步至少一个 `.ai/` 路径、锚点绑定指定步骤） → AC3/AC4
- `tools/context-budget/context_budget.py` 常量：`ORDER_BEGIN` / `ORDER_END` / `ORDER_SOURCE` / `ORDER_PROJECTIONS`（4 处）/ `ORDER_LIMITS`（1400 字节 / 9 非空行 / 10 指针）/ `ORDER_STEP_RE` / `ORDER_ANCHORS` / `ORDER_STEPS` → AC3/AC5
- `tools/context-budget/context_budget.py` metrics：新增 `order_bytes` / `order_nonempty_lines` / `order_pointers` / `order_projections` 四项 → AC5
- `tools/context-budget/tests/test_context_budget.py`：新增 7 个用例方法覆盖 10 个负例场景——四处投影各自被单独篡改（subTest ×4，且断言不误报其他三处）、真源被改致四处同时失配、标记缺失 fail-closed、体量超限、编号断开、某步无 `.ai/` 路径、锚点挪出指定步 → AC9
- `.ai/MILESTONE.md §5.4`：R2 发布处置登记，写明下个发布版必须含 `[regen-entrypoints]` 与老项目升级前的滞后事实 → AC11

## EDIT

- `Coder/40_Context_Management/context-persistence.md §6` 读序正文：由「按 状态 → 时间线 → 断点 → 代码」的 5 条平铺改为五步语义阶段，三条此前被投影集体丢掉的硬约束写进对应步骤——第 2 步的 `state-index.json` 定向读单个冷分片与「禁止默认读取整个 `.ai/history/`」、第 3 步的 `check` 三态处置、第 4 步的 Goal state/reason/next 重算 → AC1
- `Coder/40_Context_Management/context-persistence.md §6` 过渡措辞：R1 留的引用块拆两半，「由 MILE-0016 R2 定读序」这半删除（本轮即 R2，说完即失效），「R3 定全貌产物形态与落点」这半移出标记块、并入块后的 `debt.md` 与 handoff 互补段 → AC7
- `AGENTS.md`「冷启动：先恢复 `.ai/` 状态」：原 7 步列表整段替换为读序块，段首改为指向真源的一句 → AC2
- `templates/AGENTS.md.template`「会话起始：恢复项目状态」：原 4 步列表 + 两段散文整段替换为读序块（Goal 重算内容已进块内第 4 步，不再另写） → AC2
- `Coder/README.md`：第 165 行那段冷启动散文替换为读序块，块前加一句区分 L0（撞上领域术语时怎么分层读）与读序（新会话从零恢复上下文的顺序） → AC2
- `templates/rule-card.md`：handoff 纪律那句末尾补反向指针「冷启动一共读哪些文件、按什么顺序，本卡不列——见宿主入口『会话起始：恢复项目状态』章节的读序块」；读序块第 3 步反向指回本卡「强制工作流」，两处互指不互抄 → AC8
- `tools/context-budget/context_budget.py` 模块 docstring：补两个受守护标记块的职责与「字节一致查不出真源写错、故另设结构断言」的理由 → AC3
- `tools/context-budget/tests/test_context_budget.py` `setUp()`：临时根拷贝清单补 `templates/AGENTS.md.template`、`templates/CLAUDE.md.template`、`Coder/40_Context_Management/context-persistence.md` → AC9
- `tools/context-budget/tests/test_context_budget.py` `test_repository_baseline_passes()`：增断言四项新 metrics 实测值（1194 / 6 / 7 / 4） → AC5
- `scripts/test-goal-host-wiring.py` `test_cold_start_restores_goal_inputs()`：断言 token 由 `方案 verdict` 改为 `` `.ai/TECH_PLAN.md` 的方案状态 ``——`方案状态` 是 TECH_PLAN 的实际字段名，读序改写后正文用的是它；断言守护的对象未变（读序必须点名 TECH_PLAN 的方案裁决），只是 token 跟上真实字段名 → AC10

## DELETE

- `scripts/verify-codex-foundation.sh` 第 45–66 行的 9 项硬编码路径列表（`.ai/debt.md` / `MILESTONES` / `ITERATIONS` / `task-state` / handoff / 四件套四份）与其行号递增断言：该列表是脚本里另抄的第五份读序真源，改真源不会让它红；替换为「`AGENTS.md` 含读序块起止标记各一次、且最终 Coder 真源步骤落在块内」两条。`require_text` 的 `不要全量读取 .ai/iterations/` 随读序正文改写为 `不全量读取 .ai/iterations/` → AC6
- **覆盖面变化（不是等价替换）**：删掉的那张列表守的是「读序路径在 `AGENTS.md` 里按行号递增」，接手的投影校验守的是「四处逐字节相同」。真源自己把顺序写错了，投影校验只会报四处一致；能兜的只有新增的三条结构断言，兜不住语义层面的顺序错误 → AC12
