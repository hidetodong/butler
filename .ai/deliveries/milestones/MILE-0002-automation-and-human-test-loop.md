# 自动化测试最大化 + 人测 web 回环（MILE-0002）

> MILE-0002 · 里程碑交付（大版本）· 收口 2026-07-03 · 随 v1.7.0 发布 · 含迭代 ITER-0021 / ITER-0022 / ITER-0023 / ITER-0024 / ITER-0025

## 本次交付目标

- 补 P5 验证的两处系统性断裂：① 缺"竭尽自动化"的硬纪律，本可自动化的项（尤其 UI / 交互，其实可用浏览器自动化覆盖）容易随手推给人；② 人测结果**没有回传通道**，闭环断在人这一侧，butler 无法据结果续跑。
- 大版本目标：P5 的人测从"butler 口头说一句、结果断在人这"变成"结构化分道 + web 桥四态回传 + 后台等待续跑"的可审计闭环；自动化覆盖最大化，人测道只剩机器确实不可测的极少残余。

## 已完成内容

- 五件闭环：**自动化优先纪律 + 分道**（R1）、**分级置信 + 代理验证 + 依赖感知准入**（R2）、**交付自测桥工具**（R3）、**等待-回收-续跑 SOP**（R4）、**部署 / 使用文档 + 真 dogfood**（R5），覆盖"竭尽自动化 + 人测残余可回传续跑"两端。逐路线项见下方回填。

## 关键变更 / 用户可感知变化

- P5 验证升级为"竭尽一切自动化"硬纪律：能自动化的（含浏览器自动化覆盖 UI / 交互）必须自动化，人测道仅留机器不可测残余；每条 AC 显式分「自动道 / 人测道」回填 `VERIFY_REPORT.md`。
- 验证结论叠**分级置信**「可靠 / 弱 / 待人」：感知类可造弱自动检查（截图 diff / VLM 判图）earned 弱档，**绝不假绿**。
- 人测残余走 **交付自测桥**（butler 驻留、Node 零依赖）：外部项目传 JSON 清单 → GitHub 风格分步流程页 → 每项**四态 + 备注**（通过 / 未通过 / 跳过 / 延后）→ 写 results.json → 自退；桥不拷进目标项目，按路径传参调用。
- 后台等待续跑闭环：`run_in_background` 起桥 + 阻塞等待，人提交后进程退出即续跑，按四态路由（通过→收口 / 未通过→纠错 / 跳过→N/A / 延后→入账不阻塞）；无人值守不起桥则走 `dangerous §7.4` 依赖感知准入闸。

## 高层影响范围

- 新增规则 / 产物 / 工具：`tools/delivery-selftest/`（butler 驻留桥，Node 零依赖）、`20_Workflow_Lifecycle/human-test-bridge.md`（P5 下游接线协议）、`mcv-deployment §6`（驻留工具调用）、`HUMAN_GUIDE §5`（人测回环）、`dangerous-engine §7.4`（无人残余依赖感知准入闸）。
- 接线 / 升级：`30_Quality_Gate/testing-strategy.md`（竭尽自动化 + 分道）、`20_Workflow_Lifecycle/verify-schema.md`（分道回填 + 分级置信）、`correction-contract`（人测 fail 接入纠错）、`Coder/README`（注册）、`templates/rule-card.md`（强制约束补入，随 v1.7.0 `[regen-claude]`）。
- 未动：P1-P5 阶段状态机、四件套字段结构、AC 验收脊柱、`templates/hooks/`（无 hook 变更）。

## 拆分路线图回填

| 路线项 | 主题 | 实际 ITER | 状态 | 落点 |
|---|---|---|---|---|
| R1 | 自动化优先纪律 + 分道口径（testing-strategy 竭尽自动化 + verify-schema 分道回填） | ITER-0021 | ✅ closed | `deliveries/ITER-0021-automation-first-testing-lanes.md` |
| R2 | 分级置信 + 代理验证 + 依赖感知准入（可靠 / 弱 / 待人 + 弱自动检查 + `dangerous §7.4` 准入闸） | ITER-0022 | ✅ closed | `deliveries/ITER-0022-graded-confidence-proxy-and-admission.md` |
| R3 | 交付自测桥工具（butler 驻留、Node 零依赖、GitHub 风格分步页、四态 + 备注、写 results 自退） | ITER-0023 | ✅ closed | `deliveries/ITER-0023-delivery-selftest-bridge.md` |
| R4 | 等待-回收-续跑接线（run_in_background 起桥 + 阻塞等待 + 四态路由 + 接 P5 / correction-contract / 外部调用） | ITER-0024 | ✅ closed | `deliveries/ITER-0024-human-test-bridge-wiring.md` |
| R5 | 部署 / 使用文档 + dogfood（mcv-deployment / HUMAN_GUIDE / README 注册 + 样例端到端跑通） | ITER-0025 | ✅ closed | `deliveries/ITER-0025-bridge-usage-docs.md` |

- 五路线项全部达成。执行顺序为 R1 → R2 → R3 → R4 → R5（先立自动化纪律与置信 / 准入口径，再造桥、接线，末位补文档 + dogfood）。路线项扁平原子（一项 ≈ 一迭代，不设子项）。

## 验证方式与结果摘要

- 五路线项其下迭代各自 P1-P5 闭环、各自收口交付（见上表链接）；里程碑收口前确认路线图各项均 closed、一致性自检 5 不变量全绿。
- dogfood（R5 · ITER-0025）：以外部调用形态端到端跑通交付自测桥——headless 起桥、四态齐全（pass/fail/defer/skip）回传、写 results.json、进程 exit 0、四态路由断言通过。真人点击层由 R3 的 Playwright 弱档覆盖（本环境无真实浏览器）。
- 本里程碑随 v1.7.0 聚合发布（聚合 ITER-0021 ~ ITER-0025），迁移配方 `migrations/v1.7.0.md`（`[regen-claude]` rule-card 补强制约束 + `[restamp]`；无 `[sync-hooks]`，hook 体系未动）。

## 已知剩余风险 / 延后事项

- **DD5 样例落点偏离（Should Fix，ITER-0025）**：TECH_PLAN 冻结计划样例落 `tools/delivery-selftest/sample/manifest.sample.json`，实际复用既有 `example/manifest.json`（补 MT-4 凑齐四态，DRY 优先）——已于 ITER-0025 `VERIFY_REPORT` Remaining Risks 留痕，冻结计划未改。
- dogfood 只在 headless / 机械回路验证；真实浏览器真人点击的端到端仅靠 R3 Playwright 弱档，本环境未起真浏览器（已知环境约束，非里程碑遗留缺陷）。
- `/butler-upgrade` 协议仍未在真实老项目实跑（跨里程碑历史 dogfood 债，非本里程碑范围）。

## 引用

- 里程碑产物快照：`.ai/milestones/MILE-0002/MILESTONE.md`
- 其下迭代交付：`deliveries/ITER-0021-automation-first-testing-lanes.md`、`deliveries/ITER-0022-graded-confidence-proxy-and-admission.md`、`deliveries/ITER-0023-delivery-selftest-bridge.md`、`deliveries/ITER-0024-human-test-bridge-wiring.md`、`deliveries/ITER-0025-bridge-usage-docs.md`
- 发布：`CHANGELOG.md` [1.7.0]、`migrations/v1.7.0.md`、`.ai/ITERATIONS.md`、`.ai/MILESTONES.md`
