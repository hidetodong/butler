<!-- butler-artifact-template: 1.0.0 artifact=tech_plan -->
# TECH_PLAN — ITER-0113

方案状态: pass
方案审查日期: 2026-08-19
方案审查方式: user-ack

## Design Decisions

**总体形状**：搬 ITER-0111 的 L0 投影机制，不新造轮子。真源一份、标记圈定、四处字节投影、CI 逐字节比对，外加一层 L0 没有的结构断言。分四段推进，每段结束跑一次完整 CI，不留半绿状态。

**第一段 · 定真源（`context-persistence.md §6`）**

- 读序正文改写成五步语义阶段，用 `<!-- butler-context-order:begin -->` / `<!-- butler-context-order:end -->` 一对标记圈定。块内定稿正文（实测 1127 字节 / 6 非空行 / 7 个 md 指针）：

  ```
  冷启动 / clean-slate 重启时按下列五步恢复上下文，不依赖对话记忆；每步读完即停，不顺着引用递归展开。

  1. **欠债与边界** —— 读 `.ai/debt.md`：还悬着什么账、哪些边界不能碰。
  2. **时间线** —— 只读 `.ai/MILESTONES.md` 与 `.ai/ITERATIONS.md` 的热表；需要旧身份时先跑 `state-ledger check`，再沿 `.ai/state-index.json` 用 `lookup` 定向读命中的那一个冷分片，禁止默认读取整个 `.ai/history/`。
  3. **断点** —— 先跑 `tools/handoff/handoff.py check`：`fresh` 才读 `.ai/02_SESSION_HANDOFF.md`，`stale` 先 `sync` 重建后再读，`error` 先修权威状态。
  4. **Goal 状态** —— 读 `.ai/task-state.md` 的 Goal Calibration、当前 `.ai/TECH_PLAN.md` 的方案状态与 `.ai/VERIFY_REPORT.md` 的 Completion Inputs，重算 state / reason / next；宿主原生 Goal 只是可重建投影，不是真源。
  5. **产物与代码** —— 按前四步给出的指针钻取工作区四件套、`Coder/` 真源与代码；不全量读取 `.ai/iterations/`、`.ai/milestones/` 或 `deliveries/` 历史归档。
  ```

- **块内不放任何 butler 仓专有内容**。R1 留的过渡引用块要拆成两半：「由 MILE-0016 R2 定读序」这半直接删（R2 就是本轮，说完即失效）；「R3 定全貌产物形态与落点、在那之前只能靠这五步加 `Coder/README.md` 建立全貌」这半保留，但移到**标记块外面**、作为 §6 的一段说明。理由是块要投到部署项目的入口模板里去，里程碑路线项编号是 butler 自己的内务，不该出现在别人项目的 `CLAUDE.md` 里。
- `handoff-spec.md` 第 15 行经核只提 R3、不提 R2，本轮不动它的正文，只确认 AC7 的 `grep 'R2'` 零命中成立。

**第二段 · 投四处载体**

| 载体 | 落点 | 动作 |
|---|---|---|
| `AGENTS.md` | `## 冷启动：先恢复 .ai/ 状态` 段内 | 现有 7 步列表整段替换为标记块 |
| `templates/AGENTS.md.template` | `## 会话起始：恢复项目状态` 段内 | 现有 4 步列表整段替换为标记块；「恢复时先重算 Goal…」那段散文删除（内容已进块内第 4 步） |
| `templates/CLAUDE.md.template` | `{{RULE_CARD_CONTENT}}` 之后、`## 完整规则参考（深度阅读）` 之前 | **新增** `## 会话起始：恢复项目状态` 章节并放入标记块 |
| `Coder/README.md` | 第 165 行那段散文所在位置 | 散文整段替换为标记块，块前加一句区分 L0 与读序的过渡 |

- `Coder/README.md` 里 L0 块与读序块会相邻。过渡句写死为：L0 管「撞上领域术语时怎么分层读」，读序管「新会话从零恢复上下文的顺序」，两者是不同触发条件下的两套动作，不是一件事的两半。
- 两份入口模板的读序块**不进 `templates/rule-card.md`**。rule-card 现在 13457 字节、每次会话必进上下文，把读序塞进去等于给所有部署项目每次会话加成本；模板各投一次多一个投影点，但由 CI 管住。rule-card 只在第 45 行末尾补一句指向读序块，反向由块内第 3 步指回 rule-card 的 handoff 纪律——两边互指、互不复述。

**第三段 · 机器校验（`tools/context-budget/context_budget.py`）**

- `_l0_block(text, label)` 泛化为 `_marker_block(text, label, begin, end, name)`，保留原有的「标记各恰好出现一次」与「不得交错」两道 fail-closed 检查；`_l0_block` 改为薄包装，L0 现有行为与诊断字符串一字不变。
- 新增常量：`ORDER_BEGIN` / `ORDER_END`、`ORDER_SOURCE = "Coder/40_Context_Management/context-persistence.md"`、`ORDER_PROJECTIONS = ("AGENTS.md", "Coder/README.md", "templates/AGENTS.md.template", "templates/CLAUDE.md.template")`、`ORDER_LIMITS = {"bytes": 1400, "nonempty_lines": 9, "pointers": 10}`。
- 比对诊断沿用 L0 句式：`order projection mismatch: <文件路径> differs from <ORDER_SOURCE>`，一次报全部不一致的文件，不在第一处就短路。
- 结构断言 `_order_structure_errors(block)`，三类各自独立报错、互不掩盖：
  - **编号连续**：块内匹配 `^(\d+)\. ` 的行按序取号，必须恰为 `[1,2,3,4,5]`；否则报 `order steps must be 1..5, got <实际>`。
  - **每步有路径**：每步正文至少含一个 `.ai/` 开头的路径；否则报 `order step <n> has no .ai/ pointer`。
  - **锚点在位**：第 2 步含 `state-index.json`、第 3 步含 `check`、第 4 步含 `Goal`。断言的是**该锚点落在指定步骤内**，不是「块里某处有」——只查全块会被一次挪位骗过。缺失报 `order step <n> missing anchor: <锚点>`。
- metrics 增 `order_bytes` / `order_nonempty_lines` / `order_pointers` / `order_projections` 四项。
- **不新增领域合同条目**。读序块的回归由本节的常驻校验直接守住，再往 `domains.v1.json` 登记一条只会多一处双写；等 R3 定出全貌产物形态、读序真的成为跨上下文引用时再登记。`Coder/domain-glossary.md` 同理不动，L2 术语仍为 19 条、精确条数校验不改。

**第四段 · 拆 codex 脚本、去过渡措辞、登记**

- `scripts/verify-codex-foundation.sh` 第 45–66 行那张 9 项硬编码路径列表整段删除，替换为两条：`AGENTS.md` 含 `butler-context-order:begin` 与 `:end` 各一次；最终 `Coder/` 真源步骤仍在读序块之后。`require_text` 对 `Coder/README.md` 与「不全量读取 `.ai/iterations/`」两条保留——后者现在落在块内第 5 步，仍能命中。
- `.ai/MILESTONE.md §5.4` 追加一条登记：本轮改了 `templates/CLAUDE.md.template` 与 `templates/AGENTS.md.template` 两份部署入口模板，下个发布版必须含 `[regen-entrypoints]`、不得记 `[no-op]`；老项目在跑 `/butler:upgrade` 之前 Codex 侧仍是旧读序、Claude 侧仍然没有读序，这段滞后归 R15 的 v4.0.0 配方收尾。
- **本轮的「领域变更」四项声明**（ITER-0111 新增的评审维度，本轮命中 `Coder/README.md` 与 `AGENTS.md` 两份 L0 载体）：
  - **唯一所有者**：读序正文归 `context-persistence.md §6` 独占，另四处是受 CI 校验的字节投影；handoff 的「派生视图、何时 sync」定性归 `templates/rule-card.md` 独占。无第二真源。
  - **兼容影响**：`AGENTS.md` 与两份模板的章节标题不变，只换段内内容；`Coder/README.md` 换掉一段散文、不动 L0 块字节。`verify-codex-foundation.sh` 的断言口径变了（见 Failure Paths 第 6 条），这是本轮唯一的行为面变化。
  - **迁移路径**：butler 仓自身立即生效；已部署项目须重新生成入口才拿得到，故下个发布版必须含 `[regen-entrypoints]`。
  - **负向样例**：6 条 fixture（见 Test Strategy），覆盖四处投影各自被改、真源被改、标记缺失三类；结构断言另配 3 条。

## Failure Paths

1. **四处投影漏改一处** —— `context_budget.py` 报 `order projection mismatch: <文件>` 并指名；进完整 CI，每次跑。这是本轮最可能发生的失误，也是整套机制存在的理由。
2. **标记写坏（缺一半、写两遍、两块交错）** —— `_marker_block` fail-closed 抛 `ValueError`，诊断带文件名与「markers must each occur exactly once」/「markers are malformed」。不静默跳过、不当成空块通过。
3. **`Coder/README.md` 的 L0 块与读序块互相污染** —— 该文件同时是 L0 真源与读序投影，两对标记若嵌套或交错，`_marker_block` 的 malformed 检查会抓住。已确认两块物理不相邻嵌套，中间隔一段过渡文字。
4. **读序块悄悄膨胀** —— 超过 `bytes 1400` / `nonempty_lines 9` / `pointers 10` 任一项即报 `order <指标>=<实际> exceeds <上限>`。定稿实测 1127 / 6 / 7，留的余量够加一步或两句，不够无节制扩写。
5. **结构断言被一次挪位骗过** —— 若只查「块里有没有 `state-index.json`」，把它从第 2 步挪到第 5 步照样绿。故锚点断言绑定步骤号，挪位即红。
6. **拆掉 codex 脚本那张列表 = 真实的覆盖面下降** —— 原先它守的是「读序路径在 `AGENTS.md` 里按行号递增」，换成投影校验后守的是「四处逐字节相同 + 结构断言」。**真源本身把顺序写错了，投影校验只会说四处一致**。能兜的只有结构断言那三条（编号连续、每步有路径、锚点在指定步内），兜不住语义层面的顺序错误。这不是等价替换，AC12 要求在交付里如实写明。
7. **改了所有会话的起手式，改错不会当场报错** —— 读序是每个新会话第一件事，写坏了只会让后续判断建立在错的上下文上，没有任何机器信号。本轮拿不到运行时观测证明宿主真按读序走了，这跟 ITER-0111「证明不了宿主真按 L0 分层读」是同一个缺口，确定性数据归 R11。P5 不得因为四处字节一致就写成「读序生效了」。
8. **老项目拿不到新读序** —— 已部署项目在升级前 Codex 侧是旧读序、Claude 侧没有读序。已知滞后，本轮只登记 `[regen-entrypoints]`，实际配方归 R15。

## Test Strategy

**新增 fixture 9 条**，全部进 `tools/context-budget/tests/test_context_budget.py`，每条断言具体诊断字符串、不只断言非零退出：

| # | 类型 | 造法 | 期望诊断 |
|---|---|---|---|
| 1–4 | 投影各自被改 | 依次篡改四处投影中的一处块内正文 | `order projection mismatch: <该文件>` 且只报这一份 |
| 5 | 真源被改 | 改 `context-persistence.md` 块内正文 | 四处投影同时失配，报四条 |
| 6 | 标记缺失 | 任一载体删掉 `:end` 标记 | fail-closed 抛错，含该文件名 |
| 7 | 编号断开 | 把第 3 步改成 `4.` | `order steps must be 1..5, got [1, 2, 4, 4, 5]` |
| 8 | 某步无路径 | 抽掉第 1 步的 `.ai/debt.md` | `order step 1 has no .ai/ pointer` |
| 9 | 锚点挪位 | 把 `state-index.json` 从第 2 步挪到第 5 步 | `order step 2 missing anchor: state-index.json` |

**回归保护**：L0 现有 12 条用例全部复跑，诊断字符串与 metrics 断言不得变化——`_l0_block` 泛化是纯重构，行为面必须零变化。`test_repository_baseline_passes` 增断言四项新 metrics 的实测值。

**证据捕获**（`tools/verification-evidence/evidence.py run`）：
- `ac1-source` (AC1)：`grep` 计标记对数为 5 + 三条硬约束定向命中
- `ac2-projection-sha` (AC2)：脚本提取五处块正文算 sha256 断言全等
- `ac3-ac4-ac5-budget` (AC3/AC4/AC5)：`context_budget.py check` 退出码 0 + metrics 三项实测
- `ac6-codex` (AC6)：`verify-codex-foundation.sh` 退出码 0 + 旧列表零命中
- `ac7-transition` (AC7)：两文件 `grep 'R2'` 零命中、`grep 'R3'` 各不小于 1
- `ac8-ac11-ac12-proxy` (AC8/AC11/AC12)：分工不重复、`[regen-entrypoints]` 登记在场、交付段落在场的弱档代理验证
- `ac9-tests` (AC9)：`python3 -m unittest` 跑 context-budget 测试套，用例计数不少于 21
- `ac10-verify-ci` (AC10)：完整 `verify-ci.sh` 退出码 0
- `ac10-audit` (AC10)：`audit-project-state.py --allow-unreleased` 退出码 0

AC8 / AC11 / AC12 原定人读，按 `testing-strategy.md §3`「能造出弱检查的项就不算人测残余」归自动道弱档，不起交付自测桥。

**不做 TDD 配对**：本轮机器侧改动是给既有校验器加一组同构检查，不是新造行为契约；红绿顺序按常规先写实现再补 fixture，`tech-plan-schema.md` 的 TDD cycle 不声明。

## References Compliance

- N/A（本迭代不消费 `.ai/references/` 下的 PRD 或外部规格）。
