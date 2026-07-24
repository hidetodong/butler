# PRD 改版到未启动里程碑路线项的确定性兑现闭环

候办键: prd-future-route-fulfillment
候办状态: deferred

## 范围评估

### In Scope（版本级）

- 把 PRD update receipt 中针对 `planned` 路线项的 future disposition，从“留痕决定”提升为可查询、可消费、可验证的待兑现义务。
- 在里程碑路线项启动并绑定真实迭代时，机械解析该路线关联的完整 `prd_id#module_slug` 锚点及适用的最新 update receipt。
- 对 `use-new-on-start`、`defer`、`not-applicable` 建立确定性启动语义；不得把三者都退化成提示文字。
- 在 AC 冻结前，对账路线项、disposition 与 `prd_refs`，确保应采用新版时钉住正确 `prd_id + prd_version + module_slugs`。
- 提供未兑现、已兑现、显式豁免和冲突状态的只读检查，并接入审计与回归测试。
- 对缺少完整 PRD 锚点、多个 receipt 冲突、路线改号或模块演进等情况 fail-closed，亮明可操作缺口。

### Out of Scope（版本级）

- 不自动改写已冻结 active 迭代的 AC；仍按 `amend-and-refreeze` 生命周期处理。
- 不回写 closed 迭代、closed 路线或已归档里程碑历史。
- 不让 PRD update 直接重写 `.ai/MILESTONE.md` 的业务语义或替用户重新规划路线。
- 不把非 PRD 路线强制纳入 `prd_refs`。
- 不在本候办阶段分配正式里程碑号、迭代号或建立 Goal 投影。

### 关键交付目标

- `use-new-on-start` 不再依赖 AI 记忆：对应路线项启动时，未正确绑定新版 PRD 就不能静默进入冻结态。
- `defer` 会明确阻止或暂停受影响路线的无提示启动；`not-applicable` 有可审计依据且不会制造伪阻塞。
- 每项 future disposition 都能回答“尚未兑现、由哪个迭代兑现、何时兑现、凭什么判定完成”。
- 既有 active/closed 钉版边界保持不变，未使用 PRD 的项目流程不受影响。

## 理解阐释

当前 PRD 更新链已经能扫描 `.ai/MILESTONE.md` 中带完整模块锚点的路线项，并把 `planned` 路线识别为 `future`；apply 也会要求选择 `use-new-on-start`、`defer` 或 `not-applicable`，随后把决定写入 update receipt。

问题出在后半程：receipt 是记录，不是执行者。路线项后来启动时，没有机械步骤读取这项决定，也没有门禁确认新迭代的 `AC_LIST.md` 已按决定绑定正确 PRD 版本。因此“已经决定以后用新版”仍可能因 AI 漏读、上下文压缩或新会话接手而失效。

这个方向要补的是跨时间的义务消费链，而不是让 PRD 更新越权修改里程碑或历史 AC。里程碑路线项继续负责方向，PRD receipt 负责改版决定，迭代 AC 负责冻结本轮规格；新增机制只在路线项启动和 AC 冻结之间完成三者对账。

系统影响主要落在 PRD update/status、里程碑路线绑定、迭代开启与 AC 冻结门、状态审计和双宿主工作流。实现必须处理连续多次 PRD 更新、模块拆并、路线项重排及重复启动，避免只支持“单次 receipt + 单模块”的理想样例。

## 拆分路线图

预计 3 个迭代承接；实际迭代号在启动时绑定。

| 路线项 | 主题 / 范围切片 | 实际 ITER | 状态 |
|---|---|---|---|
| R1 | Future disposition 义务契约与确定性解析：定义待兑现/已兑现/豁免/冲突状态、receipt 选择顺序、模块演进与幂等语义 | — | planned |
| R2 | 路线启动消费与 AC 冻结门：绑定真实迭代时读取义务，落实 `use-new-on-start` / `defer` / `not-applicable`，并机械对账 `prd_refs` | — | planned |
| R3 | 状态、审计与非回归闭环：暴露未兑现义务，覆盖多次改版、缺锚点、拆并冲突、双宿主接线与真实仓 dogfood | — | planned |

## 范围演进记录

- 2026-07-23：由“PRD 更新能发现未来路线、但启动时不保证兑现”的现状缺口建立未编号候办方向。
