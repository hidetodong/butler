# PRD 先行触发加固：堵住 Confluence + MCP + /milestone 的漏切通道

> ITER-0042 · 独立迭代（MILE-0004 已收、无所属里程碑）· 收口 2026-07-12 · 监督态 · 修已发布 v2.1.0 PRD 子系统的实战缺陷（P5 起独立复核守质量）· 不切版（判 MINOR·v2.2.0，发布待放行）

## 本次交付目标

- MILE-0004 建成的「PRD 先行」全生命周期链，**实战里被一条真实通道穿透**：用户给一份 Confluence 文档地址、AI 经 MCP 直读当 `/milestone` brief，结果 **MILESTONE.md 合成了，但从没提切分、`references/prd/` 从没建**——PRD 的逐字规格蒸发进上下文、没落盘。
- 根因是整条切分链**软触发、零强制**，而「Confluence + MCP 直读 + /milestone」恰好同时穿过三层最薄的纸。本轮三层一起补：把软触发**挪到难错过的位置** + 给唯一可观测的落盘点**加一道非阻塞自检**。

## 已完成内容

- **① 注入表按内容分类（改 `logic-protocol.md`）**：把外部资料注入从"按来源信号一步定落点"改成**两拍**——第一拍按来源取内容（Confluence / **经 MCP 直读的文档** / MasterGo / 粘贴文本…都只是取内容的手段），第二拍**按内容类型定落点**（逐字权威规格 PRD → `prd/` 切分、API 契约 → `api-`、设计 → `design-`、分析报告 → `insight-`）。落一条命门：**来源 ≠ 落点，落点只由内容是什么决定**。装 PRD 的 Confluence 从此走 `prd/`，绝不因"它是 Confluence / 来自 MCP"默认落 `api-` 扁平。Fallback（skill 不可用人工粘贴）同样改为按内容分类——粘贴一份大 PRD 一样走切分。
- **② 里程碑分类闸前移（改 `milestone-schema §6.4`）**：把"这份 brief 是不是大 PRD"的判断，从**末尾一个默认跳过的附录步**，提成**合成 MILESTONE 之前必过的分类闸**：任何外部结构化文档当 brief（对话 / `origin/` / MCP 直读），合成路线图前先判——是 PRD 就先切再合成，不是就照旧。判定动作从"可选、易漏"变成"前置、必过"。
- **③ 新增 PostToolUse 落盘自检 hook（兜唯一可观测点）**：新增一套与现有门禁**分离**的 PostToolUse 提醒 hook（`butler_advisor.py` + `prd_split_reminder` 规则）——写完 `.ai/MILESTONE.md` 后，若 `references/prd/` 还不存在，就经 `additionalContext` 给模型注入一句条件式自检（"brief 若源自外部权威规格，先切 `references/prd/` 再推进；否则忽略"）。配套：`Advisory` 类型 + pytest 覆盖 + 部署/settings/README 接线。

## 关键变更 / 用户可感知变化

- **给一份 Confluence/PRD 链接开里程碑，不再只建 MILESTONE 就完事**：内容是 PRD 就会被识别、提议切成 `references/prd/` 逐字切片，后续验收能对着真源核。
- **落点跟"从哪来"脱钩**：同一份 PRD，无论来自对话粘贴、`origin/` 文件、还是 MCP 直读，都走同一条内容分类——不再有"从 MCP 进来就漏切"的暗门。
- **漏了会被当场提醒**：万一还是没切，写 MILESTONE 时 hook 会注入一句自检提醒，把"漏切"从静默变可见。
- **提醒绝不挡路**：这道 hook 只提醒、永远放行（PostToolUse + fail-open），非 PRD 的普通里程碑读一句即可忽略，写操作结果一字不变。
- **不用 PRD 的人完全无感**：老门禁一行没动，对话录入 / 普通 brief 合成 / 扁平态注入全程未变。

## 高层影响范围

- 规则文本（2 处）：`Coder/00_System_Prompt/logic-protocol.md`（§注入两拍重构 + MCP 直读入口 + 来源≠落点 + Fallback 分类）、`Coder/20_Workflow_Lifecycle/milestone-schema.md §6.4`（PRD 分类闸前移）。
- 新 hook（4 新文件）：`templates/hooks/butler_advisor.py`（PostToolUse dispatcher）、`rules/prd_split_reminder.py`（advisory rule）、`tests/test_prd_split_reminder.py` + `tests/test_advisor_integration.py`。
- hook 接线（1 改）：`templates/hooks/lib/io.py`（加 `Advisory` 类型）。
- 部署 / 文档（4 处）：`templates/settings.hooks-snippet.json`（加 PostToolUse 键）、`Coder/20_Workflow_Lifecycle/mcv-deployment.md §5`、`templates/hooks/README.md`、`Coder/README.md`。
- 没碰（守非回归门 `references-schema §9`）：`references-schema` 契约结构、`prd-split` 切分算法、`prd_version` 钉版字段、`prd-update` 改版认亲主流程、核心 P1–P5、现有 PreToolUse 门禁（`butler_gate.py` 及全部 rules）、`VERSION`。**不做**全自动 PRD 识别（识别不可机械化），**不切版**。

## 验证方式与结果摘要

- **10 项验收（AC1–10）全过**，全 **auto·可靠**：`pytest tests/` **109 passed**（原 97 + 新 12，现有测试零回归）+ dispatcher subprocess 三态冒烟（MILESTONE 无 prd/→注入 additionalContext / 源码写→静默 / 坏 stdin→fail-open exit 0）+ 规则文本读正文核语义 + `git diff` 核非回归。无人测残余。
- **非回归门机器核对**：14 个关键真源（契约 / 切分 / 钉版 / 改版主流程 / 核心 P1–P5 / 现有门禁）+ `VERSION` 逐一 `git diff --quiet` 全 clean。
- **独立复核 APPROVE-with-nits**（另起干净上下文子 agent、验证者≠实现者、只读、对抗式）：十条 AC 逐条核过，六个对抗点全部**证实、无 REFUTE**——③ 绝不 deny（11 个畸形 stdin 实测全 exit 0）、非回归 diff 亲跑全 clean、AC4 非 PRD 步 1–5 逐字未改、来源解耦成文无歧义、settings 幂等、无 AC 虚报。无 Must-Fix / 无 Should-Fix；1 Nit 已改（Fallback 落点补 `prd/`）、1 Nit 记录保留（prd 若为文件的异常态、无害）。

## 已知剩余风险 / 延后事项

- **hook 只兜可观测的 MILESTONE 落盘点**：纯注入路径（贴 PRD / 给链接但**不开里程碑**）没有可 hook 的写点，仍靠 ①②（内容路由 + 分类闸）+ AI 识别，无 hook backstop。这是 PRD 识别不可机械化的固有边界，已明写、非缺陷。
- **提醒条件式、每次开里程碑触发**：里程碑罕见、非 PRD 一句可忽略、非阻塞——噪音可忽略。
- **PRD 全链端到端仍未走完**：本轮实战暴露并修掉了触发漏切，但那次没走到切分 / 钉版 / 改版；命门红线与 R4 钉版回溯、R5 冻快照仍待真"拿一份大 PRD 走导入→改版全程"检验。
- **切版待放行**：加 PostToolUse hook 属能力新增，判 **MINOR（v2.2.0）**，需 `[sync-hooks]` + settings 合并迁移；切版是收口后的独立 `chore(release)` 发布动作，待用户放行。

## 引用（只引用路径，不嵌全文）

- 归档四件套 + 变更流：`.ai/iterations/ITER-0042/CONCEPT.md` / `AC_LIST.md` / `TECH_PLAN.md` / `VERIFY_REPORT.md` / `CHANGELOG.md`
- 改动产物：`Coder/00_System_Prompt/logic-protocol.md`、`Coder/20_Workflow_Lifecycle/milestone-schema.md §6.4`、`templates/hooks/butler_advisor.py`、`templates/hooks/rules/prd_split_reminder.py`、`templates/hooks/lib/io.py`、`templates/hooks/tests/`、`templates/settings.hooks-snippet.json`、`Coder/20_Workflow_Lifecycle/mcv-deployment.md §5`、`templates/hooks/README.md`、`Coder/README.md`
- 被修复的前置真源：`Coder/40_Context_Management/references-schema.md`（§2 判据、§9 非回归门）、`Coder/40_Context_Management/prd-split.md`（R2 切分动作，触发指向它）
