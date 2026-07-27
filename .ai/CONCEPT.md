<!-- butler-artifact-template: 1.0.0 artifact=concept -->
# CONCEPT — ITER-0092 · TDD 配对收口接线与 pytest dogfood

> ⚠️ 危险模式：本产物由模型自主确认问题理解，未经用户逐项确认（ITER-0092，2026-07-26）

## Current Understanding

- R1 已能从 TECH_PLAN 读取 TDD cycle 声明，并机械验证同一测试命令先失败、后通过；但这项检查仍是手动 CLI，Goal 完成裁决不会自动拒绝缺失配对的迭代。
- R2 要把这个 opt-in 合同接入收口链：TECH_PLAN 未声明 TDD 时保持 N/A；一旦声明，P5 和 Goal 必须看到有效的 Red/Green 配对才能收口。
- Butler 自身将用 goal-assurance 的 pytest 用例完成真实 dogfood：先记录针对新收口行为的失败，再实现并记录同命令通过。

## Scope

- 在 Goal 完成资格裁决器中新增 TDD 配对检查，复用 verification-evidence 的声明解析和 record 完整性逻辑，不在 Goal 工具中复制第二套算法。
- VERIFY 结构明确投影 TDD 检查结果；规则真源、工具说明和 CI 入口同步这一收口义务。
- 增加 Goal 工具正负向测试，覆盖已声明且配对有效、配对缺失/漂移、未声明 N/A，以及工具安装路径与项目路径分离。
- 不增加 baseline、文件哈希、有效 Red 分类、防测试改弱或跨语言 adapter；这些仍属独立候办。

## Open Questions / Risks

- Goal 工具是 Butler 驻留工具，执行时项目根可能不是 Butler 仓根；跨工具调用必须从 `goal.py` 自身位置解析 evidence 工具，不能从目标项目相对寻址。
- Goal 裁决必须保持只读且 stdout 仍为单个 JSON；子检查输出只能被捕获后投影进 check detail，不能泄到 stdout 破坏调用方。
