<!-- butler-artifact-template: 1.0.0 artifact=verify_report -->
# VERIFY_REPORT — ITER-0111

## Verification Summary

- 9/9 AC 全绿（auto·可靠），7 条 evidence record 全部 `passed`，完整 `scripts/verify-ci.sh` 退出码 0，`git diff --check` 无输出。
- 本轮把领域模型接进了此前够不着的三条路径：评审多了一维「领域变更」并要求四项声明；CI 多了一道条目覆盖门；L0 渐进读取内核从只存在于 `Coder/README.md` 变成三处字节一致、并随部署入口流进目标项目；发布侧多了一段领域变更的升级处置判据。
- 覆盖门写完立刻抓到两条真缺口：`four-state-machine-code` 与 `bridge-manifest-results-json` 此前完全没有任何断言或关系锚住，等于登记了却没有任何回归能抓。已补两条真断言（四态机器码枚举原文、桥输入/输出契约小节标题），不是放宽判定。
- 顺带修掉一处会被章节顺延打断的活引用：`project-digest-schema.md` 两处 `migration-schema.md §6` 因新增小节顺延，已改为 `§7`。

## AC Status

- [x] AC1 (auto·可靠): `review-standard.md` 新增 `## 5. 领域变更 (Domain Change)`，列出触发范围（4 份领域文件 + 3 份 L0 载体）与四项强制声明；`review-engine.md §3.3` 多维评审列表登记该维度并指回 `review-standard.md §5`，`§7` 关系表注明口径由 review-standard 独占。两处为引用关系，无双写。这不是靠人读确认——两处都注册成了常驻断言（章节标题 + 四项声明标签 + 回指锚点），进 CI 每次跑（`domain-contract-coverage`）。
- [x] AC2 (auto·可靠): `_validate_coverage` 已接进 `check`；6 条条目全通过（`domain-contract-coverage`）。未覆盖负例断言诊断含条目 id 与 `not covered by any assertion or relation`（`domain-contract-tests`）。补的是真断言不是放宽门——抽掉两条新断言即复现原缺口，有专门测试锁住。
- [x] AC3 (auto·可靠): 既有 11 条负例 fixture 全部复跑通过，诊断文本未变；覆盖门是追加校验，不改动 `_validate_entries` / `_validate_relations` / `_validate_assertions` 任一行为。
- [x] AC4 (auto·可靠): 三处 L0 正文 sha256 前缀均为 `0daab2d8`、均 656 字节。`context_budget.py` 以 `Coder/README.md` 为 `L0_SOURCE`，逐份比对 `L0_PROJECTIONS`，不等时报 `L0 projection mismatch: <file>`。三个负例分别篡改三份文件，诊断各自指名被改文件；标记缺失走 fail-closed 抛错并带文件名。
- [x] AC5 (auto·可靠): 临时目录跑 `render-project-entrypoints.py` 生成的 `CLAUDE.md` 与 `AGENTS.md` 各含 1 对标记，正文 sha 与真源全等。`test-render-project-entrypoints.py` 8 项、`verify-dual-host.sh` 与入口矩阵全绿。L0 实测 656 字节 / 5 非空行 / 2 指针，三项均在上限（1600 / 18 / 4）内。
- [x] AC6 (auto·可靠): `migration-schema.md` 新增 `## 5. 领域变更的升级处置`，用一张判据表区分「运行时实时读、不进目标项目」与「注入目标项目、必须重生成入口」，并额外给出术语改名要多判一层旧名是否进过 `.ai/` 产物。本次结论已落文：因 L0 进了 `templates/rule-card.md`，下个发布版必须含 `[regen-entrypoints]`，不得记 `[no-op]`。同样注册成常驻断言，章节或判据被删会被 CI 抓住。
- [x] AC7 (auto·可靠): 新增 9 条 fixture——覆盖门 5 条（未覆盖负例 / owner 锚点 / source 锚点 / relation 锚点 / 桥条目回归锁），L0 投影 3 条（两处投影各自被改、真源被改、标记缺失 fail-closed），治理接线断言 1 条（三份文件注册齐全 + 篡改即失败）。每条负例断言具体诊断字符串，不只断言非零退出。测试总数：domain-contract 11→17，context-budget 9→12。
- [x] AC8 (auto·可靠): 计量见下「dogfood 记录」，数字来自 `dogfood-layer-size`（`wc -c` 实测）与 `context-budget-projection`（metrics 输出）两条 record；token 数为换算值并已标注口径，不冒充实测。继续 / 缩减 / 停止的判断已写进 `.ai/MILESTONE.md §5.4`。
- [x] AC9 (auto·可靠): `bash scripts/verify-ci.sh` 退出码 0（`verify-ci`）；`git diff --check` 无输出。

## 人测道小结

- N/A（本轮无 human·待人 档 AC，人测道不适用）。

## Evidence Index

| Evidence ID | AC | 强度 | Outcome | Record |
|---|---|---|---|---|
| domain-contract-coverage | AC1,AC2,AC3,AC6 | captured | passed | `.ai/iterations/ITER-0111/evidence/domain-contract-coverage/record.json` |
| domain-contract-tests | AC1,AC2,AC3,AC6,AC7 | captured | passed | `.ai/iterations/ITER-0111/evidence/domain-contract-tests/record.json` |
| context-budget-projection | AC4,AC5 | captured | passed | `.ai/iterations/ITER-0111/evidence/context-budget-projection/record.json` |
| context-budget-tests | AC4,AC7 | captured | passed | `.ai/iterations/ITER-0111/evidence/context-budget-tests/record.json` |
| render-entrypoints-tests | AC5 | captured | passed | `.ai/iterations/ITER-0111/evidence/render-entrypoints-tests/record.json` |
| dogfood-layer-size | AC8 | captured | passed | `.ai/iterations/ITER-0111/evidence/dogfood-layer-size/record.json` |
| verify-ci | AC9 | captured | passed | `.ai/iterations/ITER-0111/evidence/verify-ci/record.json` |

## Verification Results

- **覆盖门（AC2/AC3）**：`domain_contract.py check` 退出码 0，`errors: []`。覆盖判定为「存在断言的 file 等于条目的 owner 或 source」或「条目 id 出现在任一关系的 left/right」。实现时发现一个设计副作用并已验证：同一文件上的断言会同时覆盖共享该文件的多个条目——这与计划中记录的取舍一致，测试 fixture 因此改用无断言的文件作为孤儿条目锚点。
- **L0 投影（AC4/AC5）**：标题移出标记块后，比较范围收敛为纯规则正文，三份宿主入口各自保留自己的标题层级（`Coder/README.md` 与 `AGENTS.md` 用 `###`，`templates/rule-card.md` 用 `##`，因为它的内容注入到目标项目 `CLAUDE.md` 顶层）。L0 从 694 字节降到 656 字节。
- **部署侧（AC5）**：`render-project-entrypoints.py` 从 `## 角色` 起截取 rule-card，L0 插在其后，因此确实进入两份部署入口。临时目录实测两份产出正文 sha 与真源全等。
- **评审与升级（AC1/AC6）**：起初这两条只有规则正文、没有机器证据，Goal 裁决因此判 `ineligible`，拒绝按口头结论打绿。处理方式不是补一次性 grep，而是把三份文件的结构锚点注册成领域合同常驻断言——章节标题、四项声明标签、回指锚点、升级判据各自被 `must_contain` 守住，进 CI 每次跑。这也顺带说明覆盖门那套机制本身就能承载这类接线检查，不必为它再造工具。
- **本轮自查「领域变更」四项声明（新维度首次自用）**：
  - **唯一所有者**：L0 正文归 `Coder/README.md` 独占，另两处是受校验的字节投影；「领域变更」审计口径归 `review-standard.md §5` 独占，`review-engine.md` 只登记；领域变更的升级判据归 `migration-schema.md §5` 独占。无第二真源。
  - **兼容影响**：`review-standard.md` 旧 §5 顺延为 §6、`migration-schema.md` 旧 §5/§6 顺延为 §6/§7；全仓检索后只有 `project-digest-schema.md` 两处活引用受影响，已同步改；其余命中均在 `.ai/iterations/` 历史归档内，按既有纪律不追改。既有工具行为、命令、路径、状态值均未变。
  - **迁移路径**：领域正文改动对部署项目无影响（运行时实时读）；但 `templates/rule-card.md` 被改，按 `migration-schema.md §5` 判据，下个发布版必须含 `[regen-entrypoints]`。已部署项目在升级前仍是旧入口，这是已知且可接受的滞后。
  - **负向样例**：新增 9 条 fixture + 3 条常驻断言，覆盖门、三处 L0 一致性、评审维度与升级判据各自都有能在下次改坏时立刻失败的检查；缺口是「兼容影响」与「迁移路径」这两条**声明的内容质量**无法机器断言（能查它在不在，查不出它想没想对），已记入 Remaining Risks。

- **dogfood 记录（AC8）**：

| 层 | 实测字节 | 字符 | 换算 token |
|---|---|---|---|
| L0 渐进读取内核 | 656 | 260 | ≈234 |
| L1 `domain-model.md` | 3966 | 2072 | ≈1865 |
| L2 `domain-glossary.md` | 5456 | 3290 | ≈2961 |
| L2 `context-map.md` | 6163 | 3393 | ≈3054 |

  - token 列是换算值，按中文约 0.9 token/字符估，不是 tokenizer 实测；字节与字符列来自 `wc -c` 与文件读取。
  - 部署项目冷启动新增约 234 token，占 rule-card 全文 3.8%（不是 P2 阶段估的一成——当时按 1600 字节上限估，实测只用了 656）。
  - 本迭代实际走过的路由：命中「跨模块所有权 + 新增核心检查」，按 L0 指引读 L1 定位上下文，未展开 L2 全表，只按需查了领域合同注册表与 3 份直接真源（`review-standard.md`、`migration-schema.md`、`context_budget.py`），首批 3 份预算未超，没有触发续批。
  - 新增长期维护检查点：2 个（覆盖门 1 个判定规则、L0 三处一致 1 个判定规则），配 9 条 fixture。领域合同现有 6 条目 / 3 关系 / 10 断言。

## TDD Pair Status

- N/A（TECH_PLAN 未声明 TDD cycle）。

## Goal Calibration

- 当前无未闭合运行时信号（N/A）。

## Completion Inputs

- Review Verdict: pass
- Completion Blockers: none

## Gate Coverage

- 自动道：9/9 AC 由 evidence record 支撑，无 `reported` 档口头结论。
- 机器门禁：domain-contract（含新覆盖门）、context-budget（含新投影一致性）、artifact contract、state audit、markdown 链接、双宿主与 Pi 扩展验证、全量单测，均在完整 CI 内通过。
- 人测道：不适用。

## References Compliance

- N/A（本迭代不消费 `.ai/references/` 下的 PRD 或外部规格）。

## Remaining Risks

- **证明不了宿主真的按 L0 分层读了**：能证明三处字节一致、能证明 L0 进了部署入口，但没有任何运行时观测能说明某个宿主在真实会话里确实照它分层读取。这是 R5 定义里「衡量歧义减少」最实的那一半，本轮拿不到；需要运行时遥测，已划给 `butler-slim-down` 候办的 usage instrumentation。
- **机器只能查声明在不在，查不出想没想对**：评审维度、四项声明标签、升级判据的**存在性**已由常驻断言守住；但「兼容影响」和「迁移路径」这两条写得对不对、有没有漏掉依赖方，机器判不了。门绿不等于这两条想清楚了，规则正文里写明了这一点，执行仍靠自觉。
- **覆盖门是文件级粒度**：同一文件上的断言会同时覆盖共享该文件的多个条目。目前 `tools/delivery-selftest/README.md` 上的两条断言分别对应两个条目，是真覆盖；但将来若有条目蹭同文件的无关断言，门会误判为已覆盖。
- **dogfood 样本只有一个迭代**：成本收益结论基于本迭代一次观察，不构成普遍结论。
- **token 列是换算不是实测**：仓内无 tokenizer 依赖，按中文 0.9 token/字符估算，与真实 `o200k_base` 计数可能有出入。

## Handoff / Next Step

- MILE-0015 五个路线项（R1–R5）全部完成，可进入里程碑收口。
- 下个发布版切版时必须含 `[regen-entrypoints]`（本轮改了 `templates/rule-card.md`），不得记 `[no-op]`。
