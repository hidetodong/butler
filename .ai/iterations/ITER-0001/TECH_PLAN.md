# Goal
- 支撑 AC1–AC10：新增 §8 对话层风格规则、补 lifecycle 引用、按 butler SOP 全链路产出 `.ai/` 与 `deliveries/`

# Files / Modules to Change
- `Coder/20_Workflow_Lifecycle/delivery-summary.md` — 追加 §8 对话内人话摘要，含 5 个子节
- `Coder/20_Workflow_Lifecycle/lifecycle.md` — P5 Verify 段"必须产物"条目后追加一句 §8 引用
- `.ai/CONCEPT.md` — 本任务 P1 决策记录（覆写）
- `.ai/AC_LIST.md` — 本任务 P2 决策记录（覆写）
- `.ai/TECH_PLAN.md` — 本任务 P3 决策记录（即本文件）
- `.ai/VERIFY_REPORT.md` — 本任务 P5 验证结果（覆写）
- `deliveries/2026-04-20-chat-recap-style.md` — 本任务 Delivery Summary（新建）

# Interface / Contract
- `delivery-summary.md §8` 对外承诺：任何 Delivery Summary 触发时刻，AI 的对话回应必须同时满足 §8.2 形式、§8.3 内容核心、§8.4 收尾引用三组约束
- `lifecycle.md` P5 段承诺：生成 Delivery Summary 的场景下，AI 对话层输出受 §8 约束，不只受 §4 约束
- `.ai/*.md` 承诺：严格符合各自 schema §2 必填字段清单
- `deliveries/<date>-<slug>.md` 承诺：严格符合 `delivery-summary.md §4` 七小节结构

# State / Boundary
- 状态边界：§8 仅在 Delivery Summary 触发时生效；不触发时沿用既有 checkpoint / handoff 口径
- 模块职责边界：§8 管对话层、§4 管文件层，两者同源不同表达，不得互相替代
- 不在范围内：P2 / P3 ACK、阶段 checkpoint、handoff、VERIFY_REPORT 本身的对话层风格

# Design Decisions
- 选择 A（§8 扩节）而非 B（delivery-summary.md 整体重构为对话层 + 文件层二分）或 C（新建 `chat-recap.md`）：改动成本最低、职责同源集中、不破坏既有锚点。若未来对话层约束 ≥ 3 条，再评估拆分到独立文件
- 硬上限 "3–6 句" 而非 "≤ 150 字"：句数约束更贴合散文节奏，用户已在 brainstorming 阶段显式确认
- "反模糊口径"（无风险必须显式写"本轮无剩余风险"）作为兜底，防止"讲人话"被误用为"可以不说风险"
- 未命中任何 Domain / Stack Profile；仅按通用 SOP 推进

# Execution Steps
- Task 0: 产出 .ai/ P1–P3 产物（本文件 + CONCEPT + AC_LIST）
- Task 1: 在 `delivery-summary.md` 追加 §8 完整内容，grep 验证字段覆盖，commit
- Task 2: 在 `lifecycle.md` P5 段追加 §8 引用句，grep 验证，commit
- Task 3: 产出 `.ai/VERIFY_REPORT.md` 与 `deliveries/2026-04-20-chat-recap-style.md`，按新 §8 输出对话摘要，commit

# Verification Plan
- AC1–AC4：grep `delivery-summary.md` 的 §8 字段、关键词、固定格式（Task 1 Step 3 / Step 4）
- AC5：grep `lifecycle.md` 的 §8 引用（Task 2 Step 3 / Step 4）
- AC6：`git diff` 未改动文件（Task 3 Step 1）
- AC7：人工通读 `delivery-summary.md`（Task 3 Step 2）
- AC8：对照各 schema §2 逐项核查 `.ai/` 四份文件（Task 3 Step 4）
- AC9：对照 `delivery-summary.md §4` 核查 deliveries 文件（Task 3 Step 5 前置）
- AC10：对照 §8 核查本轮对话摘要（Task 3 Step 5 收尾时）

# Risks / Open Questions
- 覆写 `.ai/` 会丢失 4/17 butler-upgrade 任务的产物内容，但 git 历史保留
- 规则密度增长：`delivery-summary.md` 从 7 节扩到 8 节；通过 §8 紧凑编号（5 子节）控制
- 无未决问题
