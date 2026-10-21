# Butler 偏好探针拆包交付总结

> 日期：2026-06-14
> 任务：诊断偏好探针"攒不出通识"的冷启动死亡螺旋，按拆包思路重构其默认态与消费边界
> 状态：已完成，可交付

## 本次交付目标

紧接收敛闭环重构，对偏好探针做同源体检，发现同一种病：一条本应低摩擦常驻的**数据回路（采集 + 蒸馏）**被和高风险的**影响回路（反哺）**打包在一个默认关、且唯一消费方挂在 `/dangerous` 上的模块里。三重锁死（默认关 × 需 ≥2 项目背书 × 反哺只在 `/dangerous` 触发）形成冷启动死亡螺旋：偏好永远攒不够、攒够也用不上。同时存在概念错误——把"模型在无人值守下的自主决策"当作偏好来源，会把"模型对你的猜测"记成"你的偏好"，结构性回声室污染。

本次按 Loop Engineering 的"数据回路要早开长开"理念拆包，并彻底厘清"偏好是人在回路的产物"这一边界。

## 已完成内容

| # | 改动 | 落地 |
|---|---|---|
| 1 | 引擎两层化 | `70_Extension_Preference/preference-probe-engine.md` 全文重写：§1 重构为数据回路 / 影响回路两分；§2 数据回路经同意默认常驻、影响回路 opt-in；§2.4 一次性同意协议（方案 A）；§3 七条安全底线新增 §3-7"只学真人选择" |
| 2 | 消费方反转 | 删除 `/dangerous` 作为反哺主消费方的旧设计：dangerous-engine.md 删 §5.3 偏好维度、§9 改写为"完全隔离"；引擎 §9 标注"`/dangerous` 从主要消费方反转为完全隔离" |
| 3 | 消费方收窄 | 反哺唯一消费方收窄为**有监督工作的 P2/P3 提案 / 选项排序**；模型自决（含 `/dangerous` 自审门自主 ACK）一律不采集 |
| 4 | 惰性初始化 | 取消"先跑 `/preference on` 或脚本才有存储"的前置：取得同意后首次采集时引擎惰性初始化 `$BUTLER_PREF`；`preference-init.sh` 降级为可选显式初始化 |
| 5 | 同意状态落盘 | `templates/preference/config.md` 新增 `## 同意状态 (consent)` 段（unset / granted / declined） |
| 6 | 口径同步 | logic-protocol §4 Preference Mode、Coder/README×2、根 README、HUMAN_GUIDE、profile.md 模板全部对齐新口径 |
| 7 | 注入层触达 | `templates/rule-card.md` 新增"偏好采集（实验性·默认开·经同意）"段，经 `{{RULE_CARD_CONTENT}}` 占位符自动注入新项目 |

## 关键变更 / 用户可感知变化

- **采集从"默认关"变"经同意默认常驻"**：首次命中可采集决策时全局问一次，同意后后台常驻、不再打断；`/preference off` 随时全关。这是攒出跨项目通识的前提。
- **反哺仍默认关、且语义收窄**：`/preference reback on` 才开，且**只作用于有监督工作**（P2/P3 提案 / 选项排序），绝不在 `/dangerous` 下自动按你的偏好替你做决定。
- **`/dangerous` 与偏好完全隔离**：既不读偏好档案（对齐靠自审门 / 审计 / 回滚 / P5 强审），也不把模型自主决策采集为偏好。修正了旧设计中"危险模式是偏好主要消费方"的方向性错误。
- **只学真人选择**：信号源只记用户本人的决策倾向抽象，模型自决一律不入信号，结构性消除回声室。
- **零前置存储**：不再要求先初始化才能用；同意后自动惰性建档。

## 高层影响范围

- **修改**：`Coder/00_System_Prompt/logic-protocol.md`、`Coder/65_Extension_Dangerous/dangerous-engine.md`、`Coder/70_Extension_Preference/preference-probe-engine.md`、`Coder/README.md`、根 `README.md`、`HUMAN_GUIDE.md`、`scripts/preference-init.sh`、`templates/preference/README.md`、`templates/preference/config.md`、`templates/preference/profile.md`、`templates/rule-card.md`（共 11 个文件）
- **未动**：`deliveries/`（本文件除外）、`Coder/30_Quality_Gate/`、`Coder/55_Extension_ConvergenceLoop/`、`Coder/10/20/40/50/60`、`templates/preference/signals.example.md`（无 dangerous 引用）、`Learner/`、`Composer/`
- **概念边界确立**：偏好 = 人在回路产物；自治模式（`/dangerous`）= 无偏好。两者隔离写入七条安全底线 §3-7 与引擎 §9。

## 验证方式与结果摘要

| 验证动作 | 结果 |
|---|---|
| 全仓 grep `dangerous` ∩ `反哺/偏好` | 仅余"完全隔离 / 不参与"的正确叙事，0 处旧"消费方"残留 ✅ |
| 全仓 grep `自治反哺` / `无监督反哺` / `dangerous.*唯一读取` / `偏好.*默认关` | 0 残留 ✅ |
| `templates/preference/profile.md` 旧叙事修正 | 第10行"`/dangerous` 唯一读取"→"反哺(有监督)唯一读取、dangerous 完全不读" ✅ |
| `signals.example.md` 检查 | 无 dangerous / 无监督引用 ✅ |
| rule-card SSOT 注入确认 | 经 `{{RULE_CARD_CONTENT}}` 占位符注入，无需双写 ✅ |
| CLAUDE.md#3 注册检查 | 引擎文件原已注册，目录结构无新增文件 ✅ |

## 已知剩余风险 / 延后事项

- **已部署老项目不自动更新**：需各自跑 `/butler-upgrade` 才能拿到新 rule-card 的采集段与新口径。
- **同意态是会话级判断**：`consent` 字段落在 `$BUTLER_PREF/config.md`，跨会话持久；但首次询问的触发依赖引擎在命中可采集决策时主动发问，若长期无高信号决策则不会打扰——这是设计取舍。
- **采集质量仍依赖"高信号决策"判定**：何为值得记的决策由模型自判，早期可能偏多或偏少；蒸馏阈值（≥2 项目）作为后置过滤兜底。
- **延后未做**：跨项目通识的隐私审查 / 导出工具未做；偏好与 Domain Profile 的优先级仲裁未细化，留待实际使用暴露需求后立项。

## 引用

- 核心规则：`Coder/70_Extension_Preference/preference-probe-engine.md`、`Coder/65_Extension_Dangerous/dangerous-engine.md` §9
- 同源前序：`deliveries/2026-06-14-convergence-loop-refactor.md`（同一轮 Loop Engineering 体检的另一拆包）
- 规范依据：`Coder/20_Workflow_Lifecycle/delivery-summary.md`
