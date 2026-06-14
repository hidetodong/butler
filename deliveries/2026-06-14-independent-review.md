# Butler 独立复核交付总结

> 日期：2026-06-14
> 任务：引入 Loop Engineering 构件5（Maker/Checker 分离）——给 butler 加一个真·独立的 reviewer 审查产物
> 状态：已完成，可交付

## 本次交付目标

butler 的验证一直是"自己验自己"：P5 简评、VERIFY_REPORT 回填、correction-contract"修到真过"、/dangerous 自审门，全由实现者自身判定——review-engine 虽要求"以第三方视角"，但同一上下文里换口吻自评，盲点照样在，正是 Loop Engineering 点名的"自己给自己打分"反模式。

本次引入构件5的精髓 **"验证者 ≠ 实现者"**：一个 fresh-context 子 agent，只喂规格与产物、不喂作者推理链，拿验收清单逐条独立核对。关键洞察——**单模型（Opus）下独立性不来自"更强的模型"，而来自上下文隔离**。经讨论定为**纯 opt-in**（用户：不是每个项目都要深入复核），双触发：手动 `/review` + 项目级配置。

## 已完成内容

| # | 改动 | 落地 |
|---|---|---|
| 1 | 独立 Checker 引擎 | `60_Extension_CodeReview/review-engine.md` 整篇重写：§1 区分同上下文简评 vs 真·独立复核（上下文隔离）；§6 新立"独立复核"——形态(fresh-context 子 agent)、Checker 契约(spec-only 输入 / 逐 AC confirm-refute / 拿不准判 refute / 不重写实现)、输出衔接、§6.4 诚实 fallback |
| 2 | 双触发路径 | §2：手动 `/review`（一次性）+ 项目 `.ai/local-constraints.md` 设 `Review Policy: independent_review: on` → 每次 P5 收口自动起；默认 off |
| 3 | 项目级配置字段 | `20_Workflow_Lifecycle/local-constraints-schema.md` 加可选字段 `Review Policy`（independent_review on/off）+ 编写规则 |
| 4 | 验证报告回填位 | `20_Workflow_Lifecycle/verify-schema.md` VERIFY_REPORT 加**可选** `Independent Review` 字段 + §6.4 诚实标注规则 |
| 5 | 牙齿与闭环 | refute 的 AC ≡ Must Fix，阻断收口 → 退回 P4 走 correction-contract（修到真过、禁止降级修复）/ `/loop` |
| 6 | 口径同步 | logic-protocol Review Mode、Coder/README review-engine 说明、根 README + HUMAN_GUIDE（用户向新增"`/review` 与独立复核"小节） |
| 7 | /dangerous 衔接 | dangerous §7.3 P5 强审"建议升格为独立复核"、§9 关系补一句；自审门自评本轮不动 |

## 关键变更 / 用户可感知变化

- **`/review` 升级为真·独立**：不再是同上下文角色扮演第三方，而是另起 fresh-context 子 agent，只看规格+产物+自评结论、看不到原推理链，拿 AC 逐条核对、拿不准判 refute。
- **可项目级常开**：`.ai/local-constraints.md` 写 `Review Policy: independent_review: on`，则该项目每次 P5 收口自动独立复核，不用每轮重输；默认关，不为每个项目强加成本。
- **P5 简评不变**：同上下文轻量自评照旧默认开，独立复核是叠加的 opt-in，不替代。
- **诚实边界**：环境起不了子 agent 时，不许用自评冒充独立复核，须如实标"未执行"并暴露为 Remaining Risk。
- **correction-contract / rule-card / 30 层未动**：因为是 opt-in，不下沉为默认纪律、不注入 rule-card——分类落在 60_Extension（正确）。

## 高层影响范围

- **修改**：`Coder/60_Extension_CodeReview/review-engine.md`（整篇重写）、`Coder/20_Workflow_Lifecycle/local-constraints-schema.md`、`Coder/20_Workflow_Lifecycle/verify-schema.md`、`Coder/00_System_Prompt/logic-protocol.md`、`Coder/README.md`、`Coder/65_Extension_Dangerous/dangerous-engine.md`、`HUMAN_GUIDE.md`、根 `README.md`（共 8 个文件）
- **顺带修正**：根 README 特性表"偏好蒸馏…反哺无监督自决"——上轮偏好拆包遗漏的残留（新设计反哺绝不无监督），本次一并改为"有监督工作里改进提议"。
- **未动**：`30_Quality_Gate/`（correction-contract 不下沉）、`templates/rule-card.md`（不注入）、`55_Extension_ConvergenceLoop/`、`70_Extension_Preference/`、`scripts/`、`Learner/`、`Composer/`
- **架构落位**：opt-in 复核归 `60_Extension_CodeReview`（分类正确），避免重蹈"默认纪律错配进 opt-in 模块"的旧病。

## 验证方式与结果摘要

| 验证动作 | 结果 |
|---|---|
| `independent_review` 字段名跨文件一致性 | 6 个规则文件统一，无拼写分叉 ✅ |
| `Review Policy` / `独立复核` / `insight-independent-review` 交叉引用 | review-engine ↔ local-constraints-schema ↔ verify-schema 三方对齐 ✅ |
| `反哺无监督 / 无监督自决` 残留扫描 | 0 残留（含修掉上轮遗漏的 README 特性表）✅ |
| 默认态确认 | 独立复核默认 off、P5 简评默认 on、未注入 rule-card ✅ |
| CLAUDE.md#3 注册检查 | 无新增文件；改动均在既有已注册文件内 ✅ |

## 已知剩余风险 / 延后事项

- **自审门仍自评**：`/dangerous` 中途替代 P2/P3 ACK 的自审门仍是模型自评，本轮不动（双层管的是产物复核，非中途门），记为后续接缝。
- **依赖 harness 子 agent 能力**：独立复核需运行环境支持 fresh-context 子 agent；不支持时按 §6.4 降级为"未执行 + 暴露风险"，而非静默自评——这是设计选择，但意味着部分环境拿不到独立性。
- **已部署老项目不自动更新**：新 review-engine 口径需各自 `/butler-upgrade` 同步；但因未改 rule-card，注入层无变化，升级面较小。
- **延后未做**：Checker 与 review-standard 多维口径的权重细化、独立复核报告的留存/对比工具未做，留待实际使用暴露需求后立项。

## 引用

- 核心规则：`Coder/60_Extension_CodeReview/review-engine.md` §6、`Coder/20_Workflow_Lifecycle/local-constraints-schema.md`（Review Policy）
- 概念来源：`/Users/xingzidong/Documents/Developer/Loop-Engineering.md` 构件5（Maker/Checker 分工）
- 规范依据：`Coder/20_Workflow_Lifecycle/delivery-summary.md`
