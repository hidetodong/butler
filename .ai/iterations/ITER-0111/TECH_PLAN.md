<!-- butler-artifact-template: 1.0.0 artifact=tech_plan -->
# TECH_PLAN — ITER-0111

方案状态: pass

## Design Decisions

### Goal（支撑哪些 AC）

- 支撑 AC1–AC9。四条接线各自落在已有真源上，不新建工具：评审口径进 `review-standard.md` + `review-engine.md`（AC1），覆盖门进 `domain_contract.py`（AC2/AC3），L0 投影与一致性校验进 `context_budget.py`（AC4/AC5），升级处置口径进 `migration-schema.md`（AC6），fixture 进两个工具已有测试目录（AC7），计量与结论进 VERIFY 与 `MILESTONE.md`（AC8），完整 CI 收口（AC9）。

### Files / Modules to Change

- `Coder/30_Quality_Gate/review-standard.md`：新增 `## 5. 领域变更`，现有 `## 5. 领域专项审计` 顺延为 `## 6.`。全仓只有一份已归档的历史交付引用过 `review-standard.md §2.3`，不受顺延影响，归档不追改。
- `Coder/60_Extension_CodeReview/review-engine.md`：`§3.3 多维评审`维度列表加一项「领域变更」并指回 review-standard；`§7 与其他模块的关系`补一行。只登记维度名与指针，口径正文不复制。
- `tools/domain-contract/domain_contract.py`：新增 `_validate_coverage`，接进 `check`。
- `tools/domain-contract/domains.v1.json`：给两条目前无覆盖的条目补真断言（见下）。
- `tools/domain-contract/tests/test_domain_contract.py`：补覆盖门正负例。
- `Coder/README.md`：把 `### 核心概念渐进读取（L0）` 标题移到 `begin` 标记之外，标记内只留 5 条 bullet。
- `AGENTS.md`：冷启动小节第 7 步后插入同名 `###` 标题 + L0 标记块。
- `templates/rule-card.md`：`## 角色` 之后插入 `## 核心概念渐进读取（L0）` + L0 标记块。
- `tools/context-budget/context_budget.py`：L0 提取改为可复用函数，新增三处字节一致校验，metrics 增投影计数。
- `tools/context-budget/tests/test_context_budget.py`：`setUp` 拷贝清单补 `AGENTS.md` 与 `templates/rule-card.md`；补三处各自被改的负例。
- `Coder/20_Workflow_Lifecycle/migration-schema.md`：新增「领域变更的升级处置」小节。
- 收口面：`.ai/01_CHANGELOG.md`、`.ai/VERIFY_REPORT.md`、`.ai/MILESTONE.md`、`.ai/project/`、`deliveries/ITER-0111-*`。

### Interface / Contract

- **覆盖判定**（新增，`domain_contract.py`）：一条 `entries[]` 视为被覆盖，当且仅当满足其一——① 存在 `assertions[]` 的 `file` 等于该条目的 `owner` 或 `source`；② 该条目 id 出现在任一 `relations[]` 的 `left` 或 `right`。都不满足则报 `{id}: not covered by any assertion or relation`，退出码 1。注册表 schema 不变，不新增字段。
- **L0 投影**（新增，`context_budget.py`）：`Coder/README.md` 是唯一真源。三份文件各自必须恰好一对 `<!-- butler-context-l0:begin -->` / `<!-- butler-context-l0:end -->`；标记之间的正文按字节严格相等。不等时报 `L0 projection mismatch: <file>`；标记数量或顺序不对时按现有 `markers` 路径 fail-closed（退出码 2）。预算上限仍只对真源计量，不变。

### State / Boundary

- 覆盖门只读注册表与仓内文件，不改注册表结构、不新增合同种类、不复制任何执行枚举。
- L0 一致性校验只比较标记之间的字节，不管三份文件各自的标题层级与上下文，因此不同宿主入口可以有自己的排版。
- 本轮不采集运行时遥测，不判断某宿主实际读过哪层；计量是一次性人工口径。
- 不动 `tech_plan` 的 manifest 与 schema 段数漂移，不动 MILE-0014 状态机，不改任何命令与路径。

### 关键设计取舍 + Plan Admission

- **覆盖门发现的真实缺口（AC2）**：门写完先跑一遍，6 条登记条目里 `four-state-machine-code` 和 `bridge-manifest-results-json` 两条**当前完全没有覆盖**——它们的所有者 `tools/delivery-selftest/README.md` 从来没有被任何断言引用过，也不在任何关系里。这正是这道门要抓的东西。处理方式是补两条真断言，不是放宽判定：四态条目断言 README 里那行机器码枚举原文仍在，桥输入输出条目断言输入契约与输出契约两个小节标题仍在。任何人改名或删段都会被抓住。
- **覆盖判定按文件路径而非条目 id（AC2）**：断言的载体是文件，条目的锚点也是文件（owner / source），用路径匹配不需要给断言新增 `entry` 字段，注册表 schema 保持不动。代价是同一文件上的断言会同时覆盖共享该文件的多个条目——可接受，因为断言本来就是对文件内容的约束。
- **复用裁决（AC4/AC5）**：一致性校验放进 `context_budget.py` 而不是新建投影检查器。它已经拥有 L0 标记契约与预算口径、已在 CI 里、已有测试骨架；再开一个工具会把「谁拥有 L0」重新劈成两半，正好是这个里程碑要消灭的那类问题。
- **标题移出标记（AC4）**：现状标记块里含 `### 核心概念渐进读取（L0）` 标题。三处宿主入口的标题层级本该不同（rule-card 的内容注入到目标项目 `CLAUDE.md` 顶层，用 `##`），若把标题一起做字节比较就只能强行统一层级。把标题移出标记之外，比较范围收敛为纯规则正文，三处排版各自自由。L0 实测从 694 字节降到更小，预算上限（1600 字节 / 18 非空行 / 4 指针）不受影响。
- **rule-card 插入位置（AC5）**：放在 `## 角色` 之后、`## 输出呈现` 之前。`render_project_entrypoints.rule_card_content` 从 `## 角色` 起截取，插在它之后才会进部署项目；同时这是高注意力区，读取纪律应该早于具体产物规则出现。
- **评审口径不双写（AC1）**：`review-standard.md` 拥有维度正文，`review-engine.md` 只在多维评审列表登记名字加一个指针。这与两份文件现有的分工一致（通用准则 vs 审查流程），也避免再造一处会漂移的副本。
- **升级处置只补口径不补配方（AC6）**：`migrations/vX.Y.Z.md` 是切版时按发布版产出的，本迭代不是发布。所以本轮写判据 + 写本次结论，实际配方在下次切版时按判据生成。结论是明确的：因为 L0 进了 rule-card，下个发布版必须带重新生成宿主入口的动作，不能记 `[no-op]`。
- **Alternatives（已否）**：① 给注册表加 `covered_by` 字段显式声明覆盖——等于让登记者自证，门就白装了，弃；② 用 git diff 驱动的「改了领域文件必须同批改 fixture」门——CI 没有稳定 base ref，本地与远端行为会不一致，且容易被一次合并绕过，弃；③ 新建 `tools/domain-projection/` 专管投影——违反复用优先，且把 L0 所有权劈成两处，弃；④ L0 也投影进 Pi 扩展——Pi 现在没有规则注入面，得先建，超出本轮，弃（已写进 Out of Scope）。
- **Assumptions**：`rule_card_content` 从 `## 角色` 起截取的行为不变（有 `scripts/test-render-project-entrypoints.py` 覆盖）；`context_budget` 测试用的是固定拷贝清单的临时根，新增被检查文件必须同步进清单，否则会报缺文件——这是已知项，不是意外。
- **Impact / Scope Challenge**：影响面是 2 份规则正文 + 1 份规则入口 + 1 份宿主入口 + 1 份模板 + 2 个已在 CI 的检查器及其测试。更小可行方案是「只做覆盖门」，但那样评审、投影、升级三处仍然零接线，R5 等于没做；反过来更大的方案（运行时遥测）已明确划给候办。当前切法是能闭合 R5 定义的最小集合。
- **Verification Blind Spots**：能证明三处 L0 字节一致、能证明覆盖门抓得住未覆盖条目、能证明部署入口生成后带上 L0；**不能**证明任何宿主在真实会话里确实按 L0 分层读取了——那需要运行时遥测。AC8 的成本收益结论必须把这条写成局限，不能含糊过去。
- **Verdict**：`pass`（已获用户确认 2026-08-17）——AC1–AC9 均有设计与验证映射，无已知 Must Fix。

## Failure Paths

- **覆盖门一开就红**：预期内，已确认是 2 条真实缺口。补断言而非放宽门；若补的断言字符串与 README 原文不匹配，`must_contain` 会直接失败并指名文件，当场可定位。
- **章节顺延打断引用**：`review-standard.md` 现有 §5 顺延为 §6。已全仓检索，只有一份历史归档交付引用过 §2.3，不受影响；归档按既有纪律不追改。
- **rule-card 变长破坏部署入口测试**：`scripts/test-render-project-entrypoints.py` 只断言截取内容与源文件一致，不断言长度，风险低；仍在执行步骤里显式重跑双宿主验证兜底。
- **context-budget 测试临时根缺文件**：新增两份被检查文件必须进 `setUp` 拷贝清单，否则 `_read` 抛 `missing required file` 并以退出码 2 结束。先改清单再改检查器。
- **三处 L0 后续被单独改坏**：这正是新校验要防的；负例覆盖三个文件各自被改的情况，诊断必须指名是哪一份不一致，而不是只说不一致。
- **已部署项目拿不到新 L0**：真实存在且无法在本轮消除——目标项目的 `CLAUDE.md` 只在部署或升级时重新生成。处置写进 migration 判据与本次结论，发布时兑现。

## Test Strategy

### Execution Steps（可勾选，绑 AC）

- [ ] T1 给 `domains.v1.json` 两条无覆盖条目补真断言（四态机器码枚举、桥输入/输出契约小节）→ AC2
- [ ] T2 在 `domain_contract.py` 实现 `_validate_coverage` 并接进 `check`，诊断指名条目 id → AC2/AC3
- [ ] T3 补覆盖门 fixture：未覆盖负例、按 owner 覆盖正例、按 source 覆盖正例；复跑既有全部负例断言诊断不变 → AC3/AC7
- [ ] T4 把 L0 标题移出标记块（`Coder/README.md`）→ AC4
- [ ] T5 在 `AGENTS.md` 与 `templates/rule-card.md` 插入标题 + L0 标记块（正文按字节复制）→ AC4/AC5
- [ ] T6 `context_budget.py` 新增三处一致性校验与 metrics；测试 `setUp` 拷贝清单补两份文件 → AC4
- [ ] T7 补三处 L0 各自被改的负例，断言诊断指名文件 → AC7
- [ ] T8 跑部署入口生成器与双宿主验证，确认两份产出都带 L0 且矩阵全绿 → AC5
- [ ] T9 `review-standard.md` 新增领域变更维度并顺延旧 §5；`review-engine.md` 登记维度与指针 → AC1
- [ ] T10 `migration-schema.md` 新增领域变更升级处置小节，并写明本次结论 → AC6
- [ ] T11 采集 dogfood 计量（路由层级、读取份数、L0/L1/L2 实测体量与换算口径、新增长期维护检查点数量），生成 evidence → AC8
- [ ] T12 跑完整 `verify-ci.sh` 与 `git diff --check`，回填 VERIFY，把成本收益结论写进 `MILESTONE.md` → AC8/AC9

### Verification Plan

- AC1：`grep` 两份规则的锚点，核对维度存在、四项声明齐全、两处为引用而非双写。
- AC2/AC3：`domain_contract.py check` 退出码 0；单测注入未覆盖条目断言诊断含条目 id；复跑既有负例断言诊断文本不变。
- AC4：`context_budget.py check` 退出码 0；单测分别篡改三份文件的 L0 正文，断言各自诊断指名被改文件。
- AC5：`scripts/test-render-project-entrypoints.py` + `scripts/verify-dual-host.sh`；在临时目录生成部署入口后 `grep` 两份产出的标记与正文；`context_budget` metrics 读出 L0 实测体量并核对上限。
- AC6：读 `migration-schema.md` 核对小节与判据；核对本次结论已落文。
- AC7：逐条运行新增 fixture，断言命中预期诊断字符串。
- AC8：evidence record 承载计量命令输出；VERIFY 与 MILESTONE 的数字必须能追到 record。
- AC9：`bash scripts/verify-ci.sh` 退出码 0；`git diff --check` 无输出。

## References Compliance

- N/A（本迭代不消费 `.ai/references/` 下的 PRD 或外部规格；输入来自 `.ai/MILESTONE.md` R5 路线项与仓内现状检索）
