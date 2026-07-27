<!-- butler-artifact-template: 1.0.0 artifact=tech_plan -->
> ⚠️ 危险模式：本方案由模型完成 Plan Admission 后自主 ACK，未经用户确认（ITER-0091，2026-07-25）
# TECH_PLAN — ITER-0091

方案状态: pass
方案审查日期: 2026-07-25
方案审查方式: dangerous-self-review

## Design Decisions

- 在 `evidence.py` 增加 `check-tdd` 只读子命令，直接复用 record 校验、hot/archive 定位和 iteration 约束，不建立新工具状态。
- TECH_PLAN `Test Strategy` 中的 `<!-- butler-tdd-cycles: v1 -->` 后接固定表头 `Cycle | AC | argv_json | cwd`；argv 只接受 JSON string array，cwd 只接受项目相对规范路径。
- cycle 名使用小写字母、数字和单连字符；配对 evidence ID 固定派生为 `tdd-<cycle>-red` / `tdd-<cycle>-green`。
- 检查顺序先验证声明，再复用 `validate_record` 验证两条 record，最后判断 outcome、时间、argv、cwd 与 AC；所有错误一次汇总，便于修复。
- R1 只提供显式 CLI 检查；R2 再把它接入 Goal/P5 和规则真源，避免一轮同时改合同与所有调用方。

## Failure Paths

- marker 缺失：判定未启用 TDD，零写并成功返回；marker 存在但表缺失、重复或字段非法：拒绝。
- 任一 record 缺失、损坏、iteration/AC 不一致、outcome 不符、时间重叠/颠倒或命令漂移：拒绝并点名 cycle 与原因。
- 时间比较使用 record 的 UTC RFC3339 字段；无法解析时按坏 record 拒绝，不猜顺序。

## Test Strategy

- 先为 `check-tdd` 写失败 fixture，再实现最小解析与校验；覆盖有效配对、无声明、声明非法、缺边、outcome、顺序、argv/cwd/AC 漂移和 archive source。
- R1 自身不声明 TDD cycle，避免用尚未实现的门验证自身；R2 用真实 pytest Red/Green evidence dogfood。
- 专项：`python3 -m unittest tools.verification-evidence.test_evidence`；收口前跑 artifact contract、完整 CI 与 diff check。

## References Compliance

- N/A
