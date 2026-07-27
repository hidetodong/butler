<!-- butler-artifact-template: 1.0.0 artifact=tech_plan -->
# TECH_PLAN — ITER-0092

方案状态: pass
方案审查日期: 2026-07-26
方案审查方式: dangerous-self-review

> ⚠️ 危险模式：本方案由模型完成 Plan Admission 后自主 ACK，未经用户确认（ITER-0092，2026-07-26）

## Design Decisions

- `goal.py` 通过受控子进程调用 Butler 驻留的 `evidence.py check-tdd`；路径从 `goal.py` 文件位置解析，目标项目根只作 `--project-root` 参数。这样 Goal 不复制 TDD 解析/验证算法。
- 子进程必须 `capture_output=True`；exit 0 投影为 `tdd_pairs_valid` 通过（detail 保留 `[N/A]` 或 `[OK]`），exit 1/2 均投影为不通过，stdout/stderr 收敛到 JSON check detail。
- `VERIFY_REPORT` 新增 `TDD Pair Status` 固定段：未声明写 N/A，已声明列出 cycle 与机械结果。Goal 仍以 TECH_PLAN + evidence record 自行裁决，不信任 VERIFY 的文字声明。
- 同步 `goal-contract.md`、`verify-schema.md`、`lifecycle.md`、浓缩规则卡和工具 README；工具测试直接进现有 CI，不新建 runner 或另一套门禁。

## Failure Paths

- evidence 工具缺失、运行异常或输出无法解析：Goal fail-closed，但仍输出合法单 JSON 和可操作诊断。
- 未声明 TDD：`check-tdd` 返回 0 + N/A，Goal 收口语义与旧项目保持一致。
- 已声明但 marker/table/record 缺失或漂移：`tdd_pairs_valid` 失败，即使 AC、review 和其他 evidence 均通过也不得 eligible。
- 真实 Red 失败证据作为预期失败保留；不得为了让总测试绿而删除或改写它。

## Test Strategy

- 先在 `test_goal.py` 增加“TECH_PLAN 声明 cycle 但 Goal 仍 eligible”的失败用例，用下表同一命令捕获 Red record；再实现 Goal 接线和有效配对 fixture，捕获 Green record。
- 专项覆盖：未声明 N/A、有效配对 eligible、缺配对/命令漂移 ineligible、CLI 单 JSON、只读、驻留工具跨根寻址。
- 完成后跑 verification-evidence 专项、goal-assurance 专项、artifact/state/handoff 检查、完整 CI 和 diff check。

<!-- butler-tdd-cycles: v1 -->
| Cycle | AC | argv_json | cwd |
|---|---|---|---|
| goal-gate | AC1,AC2,AC4,AC5 | `["env","UV_NO_SYNC=1","uv","run","--locked","--python","3.12.12","python","-m","pytest","tools/goal-assurance/test_goal.py","-q"]` | `.` |

## References Compliance

- N/A
