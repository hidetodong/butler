---
状态: ack-frozen
ACK 日期: 2026-08-19
---
<!-- butler-artifact-template: 1.0.0 artifact=acceptance -->
# AC_LIST — ITER-0113

## Goal

- 让冷启动读序从「五处载体各说各的、没有任何机器检查能发现」变成「一份真源、四处受校验的字节投影」，并让真源里那三条今天被投影集体丢掉的硬约束（handoff 先 `check`、台账定向读冷分片、Goal 状态重算）进到步骤本身；同批给 Claude 宿主的部署入口补上它一直没有的读序段落，清掉 R1 留下的读序过渡措辞。

## In Scope

- 改写 `context-persistence.md §6 冷启动读序`：按语义阶段分五步，每步内列具体文件，三条硬约束写进对应步骤而非留在步骤外的散文里；用 `butler-context-order:begin/end` 标记把读序正文圈成可投影块，`context-persistence.md` 为唯一真源。
- 四处载体各投一份读序块、正文与真源逐字节相同：butler 仓 `AGENTS.md`、`templates/AGENTS.md.template`、`templates/CLAUDE.md.template`（新增「会话起始」章节）、`Coder/README.md`（第 165 行那段散文换成投影块）。
- `tools/context-budget/context_budget.py` 增读序投影一致性校验与体量上限（沿用 L0 那套 `_l0_block()` 提取与比对路径），配负例 fixture。
- 读序块加结构断言：五步编号连续、每步至少含一个 `.ai/` 路径、三条硬约束各自的关键锚点必须在场。
- `scripts/verify-codex-foundation.sh` 删掉自抄的 9 项路径列表，改为只校验 Codex 入口含读序块标记与最终 `Coder/` 真源步骤。
- 清掉属于读序的过渡措辞：`context-persistence.md §6` 第 1 步下引用块的读序那半、`handoff-spec.md` 第 15 行的读序那半；全貌产物那半原样留给 R3。
- `templates/rule-card.md` 第 45 行与读序块分工写死：读序块独占「按什么顺序读哪些文件」，rule-card 独占「handoff 是派生视图、什么时候 sync」，两边互指不互抄。
- 在 `.ai/MILESTONE.md §5.4` 登记本轮改了两份部署入口模板、下个发布版必须含 `[regen-entrypoints]`。

## Out of Scope

- 不定义全貌产物的形态、派生源与落点（R3）；`.ai/project/` 剩下的 `invariants.md` 与 `frontier.md` 一字不动。
- 不改 `handoff-spec.md` 的 `02_SESSION_HANDOFF.md` 格式契约，不改双台账结构与 `state-index.json` 路由公式，不改 `handoff.py` / `state_ledger.py` 的行为。
- 不改冷启动一致性自检那 5 条不变量的判定口径。
- 不改 L0 渐进读取内核的正文、上限与既有三处投影。
- 不动 `/butler:progress`（R4）、`/butler:loop`（R5）、旧 inbox 全链（R8）、根布局改名与迁位（R9）。
- 不改升级器动作类型与 CLI 参数（R14），不写 `migrations/v4.0.0.md`（R15）。
- 不切版、不发布。

## Acceptance Checklist

- [ ] AC1: `context-persistence.md §6` 的读序为五步语义阶段结构，三条硬约束在对应步骤正文内可读到——第 2 步含 `state-index.json` 定向读单个冷分片与「禁止默认读取整个 `.ai/history/`」，第 3 步含 `check` 三态处置（`fresh` 读 / `stale` 先 `sync` / `error` 先修权威状态），第 4 步含 Goal state/reason/next 重算与「宿主投影不是真源」；读序正文被 `butler-context-order:begin/end` 一对标记圈定，全仓该标记对数为 5（真源 1 + 投影 4）。
- [ ] AC2: `AGENTS.md`、`templates/AGENTS.md.template`、`templates/CLAUDE.md.template`、`Coder/README.md` 四处各含一份读序块，块内正文与 `context-persistence.md` 真源**逐字节相同**（sha256 全等）；`templates/CLAUDE.md.template` 的块位于新增的「会话起始：恢复项目状态」章节下。
- [ ] AC3: `context_budget.py` 增 `ORDER_SOURCE` / `ORDER_PROJECTIONS` 与比对逻辑，任一投影与真源不一致时报 `order projection mismatch: <文件路径>`，指名是哪一份；任一载体缺标记走 fail-closed 抛错并带文件名，不静默跳过。
- [ ] AC4: 读序块结构断言进 `context_budget.py`：步骤编号为连续 `1.`–`5.`、每步至少含一个 `.ai/` 路径、三条硬约束的锚点字符串（`state-index.json`、`check`、`Goal`）各自在场；任一条不满足时诊断指名缺的是哪一条。
- [ ] AC5: 读序块体量在新定上限内——`bytes ≤ 1400`、`nonempty_lines ≤ 9`、md 指针 `≤ 10`；`context_budget.py` 的 metrics 输出含 `order_bytes` / `order_nonempty_lines` / `order_pointers` 三项实测值。
- [ ] AC6: `scripts/verify-codex-foundation.sh` 不再出现 `.ai/MILESTONES.md` / `.ai/ITERATIONS.md` / `.ai/task-state.md` / 四件套那张 9 项硬编码列表；改为校验 `AGENTS.md` 含 `butler-context-order` 标记对与最终 `Coder/` 真源步骤，脚本整体退出码 0。
- [ ] AC7: 过渡措辞按半清理——`context-persistence.md §6` 第 1 步下的引用块与 `handoff-spec.md` 第 15 行中「读序由 R2 定」那半已删，「全貌产物由 R3 定形态」那半仍在且措辞未被改动。
- [ ] AC8: `templates/rule-card.md` 第 45 行的 handoff 纪律与读序块第 3 步不互相复述：rule-card 不列读序步骤，读序块不重复「handoff 是派生视图、不是 AI 手写真源」的定性；两处各有一句指向对方。
- [ ] AC9: 新增 fixture 不少于 6 条，覆盖四类负例——四处投影各自被单独篡改（4 条）、真源被改致四处同时失配（1 条）、任一处标记缺失 fail-closed（1 条）；每条断言具体诊断字符串，不只断言非零退出。
- [ ] AC10: `bash scripts/verify-ci.sh` 一次跑完全绿，无跳过、无单点豁免；`scripts/audit-project-state.py --project-root . --allow-unreleased` 退出码 0，非 OK 行只剩两条 `UNRELEASED` 亮牌。
- [ ] AC11: `.ai/MILESTONE.md §5.4` 含本轮的 `[regen-entrypoints]` 登记，写明改了哪两份模板、已部署项目在升级前拿不到新读序这一滞后事实。
- [ ] AC12: 交付总结如实记录一项覆盖面变化——`verify-codex-foundation.sh` 原先守的是「AGENTS.md 里读序路径按行号递增」，换成投影校验后守的是「四处逐字节相同 + 结构断言」，真源本身写错了投影校验抓不到，只有结构断言那几条能兜；这不是等价替换。

## Verification Method

- AC1: 人读 `context-persistence.md §6` 全文；`grep -c 'butler-context-order:begin' -r` 全仓为 5；三条硬约束各用一次定向 `grep` 确认落在对应步骤段内。
- AC2: 脚本提取五处标记块正文，逐一算 sha256 并断言全等；`grep -n '会话起始' templates/CLAUDE.md.template` 命中且标记块在其后。
- AC3: `python3 tools/context-budget/context_budget.py check --project-root .` 退出码 0；四条篡改 fixture 各自断言诊断含被改文件名；标记缺失 fixture 断言抛错含文件名。
- AC4: 结构断言的三条负例各造一次（编号断开、某步无 `.ai/` 路径、抽掉一个锚点字符串），断言诊断指名缺的是哪一条。
- AC5: `context_budget.py` metrics 输出三项实测值并与上限比对；上限值同时写进 `context_budget.py` 常量与 AC1 描述，人读确认一致。
- AC6: `bash scripts/verify-codex-foundation.sh` 退出码 0；`grep -c '\.ai/MILESTONES\.md' scripts/verify-codex-foundation.sh` 为 0。
- AC7: `grep -n 'R2' Coder/40_Context_Management/context-persistence.md Coder/40_Context_Management/handoff-spec.md` 零命中；`grep -c 'R3' 同两文件` 各不小于 1，人读确认保留的是全貌产物那半。
- AC8: 人读两处；`grep -c '派生视图' templates/rule-card.md` 为 1 且读序块内为 0。
- AC9: `python3 -m unittest` 跑 `tools/context-budget/tests/`，新增用例计数不少于 6，全部通过。
- AC10: `bash scripts/verify-ci.sh` 与 `scripts/audit-project-state.py --allow-unreleased`，退出码均为 0，输出留证。
- AC11: 人读 `.ai/MILESTONE.md §5.4` 末条。
- AC12: 人读 `deliveries/ITER-0113-*.md` 对应段落。

## External References

- N/A（本迭代无 `.ai/references/` 外部参考资料）。

## Open Questions / Risks

- **风险 · 投影校验守不住真源本身写错**：这是本轮最实的一个缺口，也是 AC12 要如实记的东西。四处逐字节相同只能证明「没人偷偷改其中一处」，证明不了「这五步本身是对的」。AC4 的结构断言（编号连续、每步有 `.ai/` 路径、三个锚点在场）能兜住最粗的几类错，但兜不住语义层面的顺序错误。真要守住这一层得有运行时观测，归 R11。
- **风险 · 给主力宿主的每次会话净加约 1100 字节**：读序块进 `templates/CLAUDE.md.template` 是净新增，不是改写。按中文约 0.9 token/字符估约 626 token，占规则卡全文的比例要在 P5 实测后如实写，不能只报绝对值。上限定在 1400 字节是为了留一点后续增补空间，但这个空间本身就是成本，别当成免费额度用满。
- **风险 · 四处投影点是四个必须同步维护的地方**：L0 现在是三处，读序再加四处，同源投影的总数变成七处。投影校验能保证它们一致，但每次改真源都要跑一遍同步，人工改漏时 CI 会红——这是有意的代价，不是缺陷；只是要清楚 MILE-0016 后面还有 R9 的根布局改名，那一轮会同时撞上这七处。
- **待定 · `Coder/README.md` 换成投影块后，L0 块与读序块相邻**：两块都在同一份文件的同一区域，中间只隔一段说明。物理上没问题，但两块的职责边界要写清楚——L0 是「撞上领域术语时怎么分层读」，读序是「新会话从零恢复上下文的顺序」，别让读者以为是一件事的两半。P3 定两块之间那段过渡文字。
- **待定 · 已部署项目的滞后没有兜底**：改了两份模板，老项目跑 `/butler:upgrade` 之前仍是旧入口——Codex 侧是旧读序、Claude 侧仍然没有读序。本轮只登记 `[regen-entrypoints]`，实际让老项目拿到新入口要等 R15 的 v4.0.0 配方。这段时间里，butler 仓自己和新部署的项目有读序、老项目没有，是已知的不一致。
