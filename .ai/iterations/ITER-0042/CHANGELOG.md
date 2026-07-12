# 01_CHANGELOG — ITER-0042（PRD 先行触发加固）

> 本文件是**当前活跃迭代 ITER-0042** 的对象级变更流（ADD/EDIT/DELETE）。P4 执行时回填；收口时切片归档至 `iterations/ITER-0042/CHANGELOG.md`。

## EDIT · `Coder/00_System_Prompt/logic-protocol.md`（注入表两拍重构 → AC1/AC2）

- §外部参考资料注入：单张「输入信号→处理→存储位置」表拆成**两拍**——第一拍「来源→取内容手段」（Confluence / **经 MCP 直读的文档** / MasterGo / 独立 agent 报告 / 粘贴文本·项目文件），第二拍「内容类型→落点」（逐字权威规格 PRD→`prd/`、API 契约→`api-`、UI 规格→`design-`、分析报告→`insight-`、其他→`<name>`）。
- 新增命门引述块「**来源 ≠ 落点**」：装 PRD 的 Confluence / MCP 文档走 `prd/` 切分、绝不因来源默认落 `api-` 扁平；`api-` 只给内容本身是 API 契约的。
- 新增「经 MCP 直读的文档」入口行 + "MCP 读进来一样走第二拍分类落盘、不因来自 MCP 就跳过"。Fallback 段（skill 不可用人工粘贴）未动。

## EDIT · `Coder/20_Workflow_Lifecycle/milestone-schema.md`（§6.4 PRD 分类闸前移 → AC3/AC4）

- §6.4 合成协议开头新增「**合成前必过 · PRD 分类闸（不可跳）**」callout：收集 brief 后、合成三段前先判是不是大 PRD；判是→PRD 派生里程碑（切分方案与路线图合并一次呈交）、判否→常规合成到步 5 即止；点明外部结构化文档（含 MCP 直读）尤其不可略过、判据只看内容不看来源。
- 原步 6 opener 从"大 PRD 并进分支（仅当…才走，否则跳过本步）"改为"大 PRD 并进**执行细则**（承上方分类闸判'是'时执行；判'否'则本步整体不适用）"——判定动作前移，本步只留切分执行细则（步 6 子要点 + 非回归 bullet 保留未动）。

## ADD · `templates/hooks/butler_advisor.py`（PostToolUse 提醒 dispatcher → AC5）

- 新增与 `butler_gate.py`（PreToolUse 门禁、fail-closed）平行的 PostToolUse dispatcher：收集 advisory rule 的非空 message → 经 `hookSpecificOutput.additionalContext` 注入模型；**永远 exit 0、fail-open**（任何异常静默放行）；只 gate `Edit/Write/MultiEdit`。

## ADD · `templates/hooks/rules/prd_split_reminder.py`（MILESTONE 落盘自检 rule → AC6）

- 新增 advisory rule：写 `.ai/MILESTONE.md` 且 `.ai/references/prd/` 目录不存在 → 返回条件式提醒 message（brief 若源自外部权威规格先经 prd-split 落盘再推进、否则忽略）；`prd/` 已存在 / 目标非 MILESTONE.md → message 空（静默）。返回 `Advisory`（无 verdict），构造上无 deny 路径。

## EDIT · `templates/hooks/lib/io.py`（Advisory 类型 → AC5）

- 新增 `Advisory` frozen dataclass（`rule_id` + `message`）：与 `Decision`（allow/deny 门禁）刻意分开，无 verdict、不能 deny、message 空即静默。

## ADD · `templates/hooks/tests/test_prd_split_reminder.py` + `test_advisor_integration.py`（→ AC7）

- rule 单测 6 条（prd/ 缺失→提醒、存在→静默、非 MILESTONE 目标→静默、Edit 同触发、Advisory 无 verdict 字段）。
- dispatcher subprocess 测试 6 条（注入合法 additionalContext JSON / prd 存在静默 / 非 MILESTONE 静默 / 非 gate 工具 exit0 / 坏 stdin fail-open exit0 / 缺 tool_name exit0）。
- `pytest tests/` 109 passed（原 97 + 新 12），现有测试零回归。

## EDIT · `templates/settings.hooks-snippet.json`（→ AC8）

- 新增 `hooks.PostToolUse` 键（matcher `Edit|Write|MultiEdit` → `python3 .claude/hooks/butler_advisor.py`），与既有 PreToolUse 并列。

## EDIT · `Coder/20_Workflow_Lifecycle/mcv-deployment.md §5`（部署接线 → AC8）

- 首段从"PreToolUse hook 体系"拆为两类 hook（PreToolUse 门禁 fail-closed / PostToolUse 提醒 fail-open）+ 为何分开（风险方向相反）。
- §5.1 拷贝清单加 `butler_advisor.py`（PostToolUse 入口）+ 注明 `rules/` 含 advisory rules。
- §5.2 settings 合并从只处理 PreToolUse 改为「对每个 hook 键各自幂等合并」+ 升级既有项目补 PostToolUse 键。
- §5.3 验证加 advisor 冒烟命令（MILESTONE 写 → exit0 + additionalContext）。

## EDIT · `templates/hooks/README.md`（→ AC8/AC10）

- 标题 Butler Hook Gate → Butler Hooks；intro/目录结构/运行机制/退出码契约全部补 PostToolUse advisor（含 `Advisory` 类型、`prd_split_reminder`、fail-open vs fail-closed 对照）。

## EDIT · `Coder/README.md`（line 172 hook 枚举 → AC8）

- 使用原则的 hook 拦截段补一句 PostToolUse 提醒 hook（`butler_advisor.py`、advisory-only、绝不拦截、`prd_split_reminder`）。

## EDIT · `Coder/00_System_Prompt/logic-protocol.md`（Fallback 落点分类 → 独立复核 Nit 1）

- §注入 Fallback 段：落点枚举从"命名前缀保持一致（`api-`/`design-`/`insight-`/无前缀）"改为"仍按第二拍内容类型→落点分类落盘"——粘贴的内容是逐字权威规格 PRD 一样走 `prd/` 切分，别因"是粘贴进来的"就一律落 `api-`/无前缀。堵住洞 B 在人工粘贴路径上的残留。

## 自检 · 说人话（AC10）

- advisory / PostToolUse / additionalContext / fail-open·fail-closed / 来源≠落点 首现即释；无裸英文变量。零星修正：无。
