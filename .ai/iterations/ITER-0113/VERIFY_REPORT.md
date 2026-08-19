<!-- butler-artifact-template: 1.0.0 artifact=verify_report -->
# VERIFY_REPORT — ITER-0113

## Verification Summary

- 12 条验收标准全部达成。9 条机器证据（`ac1-source` / `ac2-projection-sha` / `ac3-ac4-ac5-budget` / `ac6-ac7-cleanup` / `ac8-ac11-ac12-proxy` / `ac9-tests` / `ac10-verify-ci` / `ac10-audit-final`）全部 passed；另有 1 条失败记录 `ac10-audit` 按纪律保留作诊断，失败原因是捕获时 handoff 因源文件变动转 `stale`，`sync` 后重捕即绿。
- 置信档分布：AC1–AC7、AC9、AC10 为 auto·可靠（确定性断言，含实造负例）；AC8、AC11、AC12 为 auto·弱档——机器只查得出这几段话写没写、指针互指在不在，判不了写得对不对，最终仍靠人读。无 human·待人 档。
- 部署路径端到端验过：实跑 `render-project-entrypoints.py` 渲染到临时目录，渲染出的 `CLAUDE.md` 与 `AGENTS.md` 中读序块与真源逐字节相同（sha256 前缀 `36c5eb971a515b03`，1194 字节）。

## AC Status

- [x] AC1 (auto·可靠): 读序为五步语义阶段结构，全仓 `butler-context-order` 标记对数为 5（真源 1 + 投影 4）；三条硬约束分别落在第 2 / 3 / 4 步正文内，定向命中。证据 `ac1-source`。
- [x] AC2 (auto·可靠): 四处投影与真源 sha256 全等；`templates/CLAUDE.md.template` 的块位于新增「会话起始：恢复项目状态」章节下；渲染后的两份部署入口同样逐字节相同。证据 `ac2-projection-sha`。
- [x] AC3 (auto·可靠): 四处投影各自被单独篡改时报 `order projection mismatch: <文件名>` 且不连坐其他三处；改真源时四处同时报失配；`AGENTS.md` 抽掉起始标记时 fail-closed 抛错且诊断带文件名。证据 `ac3-ac4-ac5-budget`。
- [x] AC4 (auto·可靠): 三条结构断言各造一次负例——编号断开报 `order steps must be`、某步无 `.ai/` 路径报 `has no .ai/ pointer`、抽掉锚点报 `missing anchor`，诊断均指名缺的是哪一条。证据 `ac3-ac4-ac5-budget`。
- [x] AC5 (auto·可靠): 实测 `order_bytes` 1194 / `order_nonempty_lines` 6 / `order_pointers` 7，三项均在 1400 / 9 / 10 上限内；metrics 另含 `order_projections` = 4。证据 `ac3-ac4-ac5-budget`。
- [x] AC6 (auto·可靠): `scripts/verify-codex-foundation.sh` 退出码 0；旧 9 项硬编码列表里的 `.ai/MILESTONES.md` / `.ai/ITERATIONS.md` / `.ai/task-state.md` / `.ai/CONCEPT.md` / `.ai/VERIFY_REPORT.md` 全部零命中；改为校验读序块起止标记。证据 `ac6-ac7-cleanup`。
- [x] AC7 (auto·可靠): `context-persistence.md` 与 `handoff-spec.md` 两文件 `R2` 零命中、`R3` 各至少一处，保留的是「全貌产物由 R3 定形态」那半。证据 `ac6-ac7-cleanup`。
- [x] AC8 (auto·弱): `grep -c '派生视图' templates/rule-card.md` 为 1、读序块内为 0；读序块指向规则卡「强制工作流」，规则卡指向宿主入口的读序块；规则卡未自列读序步骤。证据 `ac8-ac11-ac12-proxy`。
- [x] AC9 (auto·可靠): 新增 7 个用例方法覆盖 10 个负例场景（四处投影单独篡改 4 条 + 真源改致四处同时失配 + 标记缺失 fail-closed + 体量超限 + 编号断开 + 某步无 `.ai/` 路径 + 锚点挪出指定步），远超「不少于 6 条」的门槛；每条断言具体诊断字符串。全套 19 个用例通过。证据 `ac9-tests`。
- [x] AC10 (auto·可靠): `bash scripts/verify-ci.sh` 退出码 0，无跳过无豁免（32 项 pytest 全过）；`audit-project-state.py --allow-unreleased` 退出码 0，812 项 OK，非 OK 行只剩两条 `UNRELEASED` 发布态亮牌与若干历史诊断 `INFO`。证据 `ac10-verify-ci` / `ac10-audit-final`。
- [x] AC11 (auto·弱): `.ai/MILESTONE.md §5.4` 的 R2 发布处置登记在场，含两份模板名、`[regen-entrypoints]` 与滞后归属 R15。证据 `ac8-ac11-ac12-proxy`。
- [x] AC12 (auto·弱): `deliveries/ITER-0113-cold-start-read-order.md` 的「已知剩余风险」首条如实写明覆盖面变化不是等价替换、结构断言是唯一兜底且兜不住语义顺序错误。证据 `ac8-ac11-ac12-proxy`。

## 人测道小结

- N/A（本轮无 human·待人 档 AC，人测道不适用）。AC8 / AC11 / AC12 三条本可归人测，但都能造出弱检查（指针互指在场、登记关键词在场、交付段落在场），按 `testing-strategy.md §3` 仍归自动道弱档。

## Evidence Index

| Evidence ID | AC | 强度 | Outcome | Record |
|---|---|---|---|---|
| ac1-source | AC1 | reproduced | passed | `.ai/iterations/ITER-0113/evidence/ac1-source/record.json` |
| ac2-projection-sha | AC2 | reproduced | passed | `.ai/iterations/ITER-0113/evidence/ac2-projection-sha/record.json` |
| ac3-ac4-ac5-budget | AC3,AC4,AC5 | reproduced | passed | `.ai/iterations/ITER-0113/evidence/ac3-ac4-ac5-budget/record.json` |
| ac6-ac7-cleanup | AC6,AC7 | reproduced | passed | `.ai/iterations/ITER-0113/evidence/ac6-ac7-cleanup/record.json` |
| ac8-ac11-ac12-proxy | AC8,AC11,AC12 | captured | passed | `.ai/iterations/ITER-0113/evidence/ac8-ac11-ac12-proxy/record.json` |
| ac9-tests | AC9 | reproduced | passed | `.ai/iterations/ITER-0113/evidence/ac9-tests/record.json` |
| ac10-verify-ci | AC10 | reproduced | passed | `.ai/iterations/ITER-0113/evidence/ac10-verify-ci/record.json` |
| ac10-audit | AC10 | captured | failed | `.ai/iterations/ITER-0113/evidence/ac10-audit/record.json`（诊断留存：handoff 转 stale） |
| ac10-audit-final | AC10 | reproduced | passed | `.ai/iterations/ITER-0113/evidence/ac10-audit-final/record.json` |

## Verification Results

- **投影一致性**：五处块正文 sha256 全等于 `36c5eb971a515b03…`，长度 1194 字节。四处投影是 `AGENTS.md`、`Coder/README.md`、`templates/AGENTS.md.template`、`templates/CLAUDE.md.template`。
- **负例不是走过场**：AC3 / AC4 的 8 个负例都在临时仓副本上现造，逐条断言诊断字符串，不只断言非零退出。其中「篡改单一投影」还额外断言另外三处**不**被报出，防止诊断退化成一律全报。
- **fail-closed 路径**：任一载体缺 `butler-context-order` 标记时 `context_budget.py` 抛错并带上文件名与标记名，不静默跳过——这条是从 L0 的 `_l0_block()` 提取成通用 `_marker_block()` 时原样继承的，行为未变。
- **CI 修复一处连带失败**：`scripts/test-goal-host-wiring.py` 原先断言 `context-persistence.md` 含 token `方案 verdict`，读序改写后正文用的是 TECH_PLAN 的真实字段名 `方案状态`。断言守护的对象没变（读序必须点名 TECH_PLAN 的方案裁决），只把 token 跟上真实字段名，已在变更流 EDIT 段记录理由。
- **与 TECH_PLAN 的偏差如实记录**：方案里写「用例计数不少于 21」是拍脑袋的估数，实测 19 个用例方法 / 10 个负例场景。AC9 的真实门槛是「新增 fixture 不少于 6 条」，实际 10 条，达标。未回头改已 ACK 的方案。
- **证据 ID 与方案略有并合**：方案原列 `ac6-codex` 与 `ac7-transition` 两条，实际合成 `ac6-ac7-cleanup` 一条（两者都是同类的删除后残留检索，同脚本跑更便宜）；AC 覆盖未变。

## TDD Pair Status

- N/A（TECH_PLAN 未声明 TDD cycle）。

## Goal Calibration

- 当前无未闭合运行时信号（N/A）。

## Completion Inputs

- Review Verdict: pass
- Completion Blockers: none

## Gate Coverage

- 质量门禁：`bash scripts/verify-ci.sh` 退出码 0，32 项 pytest 全过，无跳过、无单点豁免。
- 状态审计：`python3 scripts/audit-project-state.py --project-root . --allow-unreleased` 退出码 0，812 项 OK。非 OK 行为两条 `UNRELEASED` 发布态亮牌（工作树有未发布改动、v3.6.0 tag 不指向 HEAD）与历史迭代的 `INFO` 诊断留存行。OK 计数随收口写盘会继续变动，此处记录的是 `ac10-audit-final` 捕获时刻的数字。
- 产物契约：四件套与变更流均通过 `tools/artifact-pipeline/contract.py` 的章节与字段校验。
- 上下文预算：`tools/context-budget/context_budget.py check` 退出码 0，L0 与读序两个受守护块的体量均在上限内。

## References Compliance

- 本迭代无 `.ai/references/` 外部参考资料，无引用合规项需核（AC_LIST「External References」为 N/A）。
- 内部规则引用一致：读序块内的指针均指向实际存在的 `.ai/` 文件与工具路径，`context_budget.py` 的 md 指针存在性校验覆盖这一点。

## Remaining Risks

- **投影校验守不住真源本身写错**（本轮最实的缺口，已写进交付）。逐字节相同只证明「没人偷偷改其中一处」，证明不了「这五步本身是对的」。三条结构断言兜住编号断开、指针缺失、锚点挪位，兜不住语义层面的顺序错误。运行时观测归 MILE-0016 R11。
- **老项目拿不到新读序**。改的是模板，已部署项目要等带 `[regen-entrypoints]` 的发布版重新渲染入口；实际迁移配方归 R15。这段窗口期内 butler 仓自己与新部署项目有新读序、老项目没有，是已登记的已知不一致。
- **1400 字节上限的余量是成本不是额度**。实测 1194，余 206 字节；每一字节都落在主力宿主的每次会话上。
- **同源投影点增至七处**（L0 三处 + 读序四处）。R9 的根布局改名会同时撞上这七处，改不齐 CI 会红——机制按设计工作，但要预留返工时间。

## Handoff / Next Step

- ITER-0113 收口，MILE-0016 R2 置 `closed`；`.ai/ITERATIONS.md` current 归 `none`。
- 下一项按里程碑路线是 MILE-0016 R3（全貌产物的形态、派生源与落点），`.ai/project/` 剩下的 `invariants.md` 与 `frontier.md` 等它接手。
- 发布侧未动：未切版、未打 tag。下个发布版的迁移配方必须含 `[regen-entrypoints]`，登记在 `.ai/MILESTONE.md §5.4`。
