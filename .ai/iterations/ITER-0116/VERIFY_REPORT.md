<!-- butler-artifact-template: 1.0.0 artifact=verify_report -->
# VERIFY_REPORT — ITER-0116

## Verification Summary

十一条验收全部通过，8 条证据记录覆盖 AC1–AC11 无遗漏。完整 CI 退出码 0，状态审计退出码 0（836 条 OK，仅两条 `[UNRELEASED]` 未发布标记，符合预期），两组扫描器 PASS。

**有三处要先摆明，不藏在细节里**：

1. **AC3 的「删除行恰为 1 行」实际是 2 行**。第 2 行是把新末条的句末 `；` 改成 `。`——删掉激活清单第三条后，原倒数第二条成了末条，`；` 收尾就成了 `Coder/` 全仓的首例（实测 0 例先例）。这一个字符的改动是被批准的那次删除的机械后果，不是新决定；但它确实超出了 AC3 的字面，故不当作「AC3 原样达成」，按偏差记在这里。
2. **AC7 写的「条目数由 10 减为 9」在收口态观测不到**。删一条加一条在同一批完成，最终仍是 10 条。证据脚本断言的是等价的强命题：总数为 10、被删那条的关键字全文零命中、其余 9 条首句逐条仍在、新增那条三要素齐备。过程中的瞬时 9 没有单独留证。
3. **`plugin.json` 的零改动基线是 P4 开始后才录的**。开工前录基线时漏了它。补录时它已在 T1–T7 全程未被打开，且对 HEAD 的全部差异只有 ITER-0115 那一处 `longDescription` 删词（先于本轮），故补录值即 P4 前的值。该说明写在 `loop-entities.baseline` 文件里，不是事后补的口头解释。

## AC Status

| AC | 结论 | 依据 |
|---|---|---|
| AC1 · 候办两侧删净 | ✅ | `ac1-backlog`：草稿文件不存在、索引零命中、索引行与实际文件同为 9、审计 `milestones.backlog_set` 集合一致性 OK |
| AC2 · §5.4 三条登记 | ✅ | `ac2-registration`：三条在场，14 处关键措辞逐个 `grep -qF` 命中 |
| AC3 · 冻结声明三要素 | ⚠️ 达成·有 1 字符偏差 | `ac3-ac5-freeze`：三要素齐备且落在 H1 与 §1 之间，§3–§8 章节齐全零改动；删除行为 2 行而非 1 行，第 2 行是句末标点，见 Verification Summary 第 1 条 |
| AC4 · loop 实体零改动 | ✅ | `ac4-ac10-sweep` B 组：六处实体哈希与 P4 前基线逐一相同，软链可解析，registry 仍 12、loop 的 `allow_implicit_invocation` 仍 false、`risk` 仍 high |
| AC5 · 两处镜像清除 | ✅ | `ac3-ac5-freeze`：两处原句全文零命中，§2 激活恰 2 条且显式命令与显式语义都在，模式清单仍 8 条；`ac4-ac10-sweep` A 组另查「检测到 + 复杂度 + 收敛闭环」等价组合，全仓 0 命中 |
| AC6 · dangerous 拆纸面依赖 | ✅ | `ac6-dangerous`：全文零 `convergence-loop-engine`，§8 新指针在场，§9 并列陈述保留，diff 恰 1 增 1 删 |
| AC7 · 删已还清的旧账 | ✅（口径见下） | `ac7-ac8-debt`：「自动绑定」全文零命中，其余 9 条首句逐条仍在；瞬时 9 未单独留证，见 Verification Summary 第 2 条 |
| AC8 · 记新欠账 | ✅ | `ac7-ac8-debt`：新条目在场，缺口 / 有意不加检查的理由 / 自然消解路径三要素逐个命中，净额 10 |
| AC9 · OVERVIEW 重算 | ✅ | `ac9-overview`：`--check` 退出码 0、8798 字节、工作流清单 12 行、loop 行在场；相对 HEAD 只有台账跟随行与 ITER-0115 的 progress 删除 |
| AC10 · 两组扫描零命中 | ✅ | `ac4-ac10-sweep`：扫 392 份文本，A 组 4 类模式 0 命中，B 组 30+ 条在场断言 0 失败 |
| AC11 · CI 与审计全绿 | ✅ | `ac11-ci-audit`：`verify-ci.sh` 退出码 0；审计退出码 0、836 条 OK、`[UNRELEASED]` 恰 2 条 |

## 人测道小结

本迭代无人测道。改的是规则散文与状态台账，没有任何界面、命令行为或交互变化——`/butler:loop` 的行为一字未改，人去点它看到的东西和昨天完全一样。没有可供人观察的差异，就没有值得人测的东西。

## Evidence Index

| Evidence ID | AC | 强度 | Outcome | Record |
|---|---|---|---|---|
| ac1-backlog | AC1 | reproduced | passed | `.ai/iterations/ITER-0116/evidence/ac1-backlog/record.json` |
| ac2-registration | AC2 | reproduced | passed | `.ai/iterations/ITER-0116/evidence/ac2-registration/record.json` |
| ac3-ac5-freeze | AC3,AC5 | reproduced | passed | `.ai/iterations/ITER-0116/evidence/ac3-ac5-freeze/record.json` |
| ac4-ac10-sweep | AC4,AC10 | reproduced | passed | `.ai/iterations/ITER-0116/evidence/ac4-ac10-sweep/record.json` |
| ac6-dangerous | AC6 | reproduced | passed | `.ai/iterations/ITER-0116/evidence/ac6-dangerous/record.json` |
| ac7-ac8-debt | AC7,AC8 | reproduced | passed | `.ai/iterations/ITER-0116/evidence/ac7-ac8-debt/record.json` |
| ac9-overview | AC9 | reproduced | passed | `.ai/iterations/ITER-0116/evidence/ac9-overview/record.json` |
| ac11-ci-audit | AC11 | reproduced | passed | `.ai/iterations/ITER-0116/evidence/ac11-ci-audit/record.json` |

各条记录的具体内容：
- `ac1-backlog`（AC1）：候办文件不存在 / 索引零命中 / 两侧同为 9 / MILESTONES diff 逐行 / 审计 backlog 段落
- `ac2-registration`（AC2）：§5.4 三条登记的 14 处关键措辞逐条断言（只能证字样在场，证不了写得对）
- `ac3-ac5-freeze`（AC3,AC5）：冻结声明三要素 / §2 激活清单 / 两处镜像零命中 / 模式清单 8 条 / 两份文件完整 diff
- `ac4-ac10-sweep`（AC4,AC10）：两组扫描器；A 组残留 0 命中，B 组在场断言 0 失败（含六处实体哈希比对）
- `ac6-dangerous`（AC6）：零引用 / 新指针 / §9 保留 / diff 恰 1 增 1 删
- `ac7-ac8-debt`（AC7,AC8）：条目数 / 旧账零命中 / 新账三要素 / 其余 9 条首句逐条
- `ac9-overview`（AC9）：--check 退出码 / 体量 / 工作流 12 行 / loop 行 / diff
- `ac11-ci-audit`（AC11）：完整 CI 输出尾段 + 审计 OK 计数与非 OK 行全文

辅助文件（非证据记录，但脚本依赖）：`.ai/iterations/ITER-0116/loop-entities.baseline` —— P4 前的六处实体哈希。

## Verification Results

**扫描面与排除面，全数摊开。** 扫描器实扫 392 份文本文件，覆盖 `tools/`（191）、`templates/`（158）、`Coder/`（62）、`scripts/`（41）、`.ai/` 活跃面（38）、`plugins/`（32）、`docs/`（22）、仓根人读文档（15）、`.claude/`（14）、`workflows/`（2）、`.github/`（1）——**机器接线面与人读文档全部在扫描面内，逐个 0 命中**。

排除面共 16 份文件、64 处命中，逐组说明它们为什么是记录而不是活引用：

- **本迭代四件套与变更流 · 4 份 / 27 处**（`AC_LIST.md` 12、`CONCEPT.md` 6、`01_CHANGELOG.md` 5、`TECH_PLAN.md` 4）。它们的职责就是写清这次删了什么，命中即预期。
- **状态台账与 handoff · 3 份 / 9 处**（`02_SESSION_HANDOFF.md` 3、`MILESTONE.md` 3、`handoff-state.json` 3）。`MILESTONE.md` 那 3 处分别是 MILE-0016 的 In Scope 原文、R5 路线行、本轮新写的 §5.4 登记；handoff 两份是会话交接快照。
- **历史归档 · 9 份 / 28 处**（ITER-0112 / ITER-0113 的审计 stdout 各 5、ITER-0112 的 TECH_PLAN 1、本迭代自己的三份脚本 4、`ac1-backlog` 的 stdout 3）。往轮证据是已冻结的历史事实，不该也不能改。
- **`.ai/MILESTONES.md` 命中数为 0**，虽在排除名单里但事实上已清干净。

**自查出并修掉的两个证据脚本缺陷**（都会让日志看起来正常、实则掩盖关键行）：

- `cut -c1-N` 在 UTF-8 locale 下遇多字节会 `Illegal byte sequence` 报错，把整条流水线拖成非零退出。全部换成 `awk substr`。
- `grep -v '^[-+][-+]'` 本意是滤掉 diff 的 `---` / `+++` 文件头，实际把 `-- **P4 熔断交还**…`、`-- 用户提到"死磕"…` 这类「diff 前缀 + markdown 列表符」的正文行也一并吃了——**正好是最该留证的那些行**。改成只滤 `^(\+\+\+|---) `。修之前 `ac3-ac5-freeze` 是「通过」的，日志里却看不到激活清单被删的那两行；修完才补上。

**收口第二步补记（写完本报告后发现，如实追记）**：交付 HTML 的渲染脚本有一处缺陷——它先按反引号把 `code` 段切开再做加粗替换，导致**跨 code 段的粗体**（形如 `**` + 行内代码 + 文字 + `**`）断在两半，两个星号原样漏到页面上。ITER-0116 的页面上有 3 处，**回查发现 ITER-0115 的交付页也有 2 处**——上一轮的浏览器实测只查了占位符、标题与横向溢出，没查残留的 markdown 标记，漏了。已改成「先把 code 段抠出占位、再转义加粗、最后还原」，两份 HTML 重新渲染并在真实浏览器复验：裸星号 0、裸反引号 0、占位符 0、无横向溢出，加粗与代码块均正常。**两份 `.md` 正文一字未改，只重出 HTML 投影**；ITER-0115 已收口，此处仅修其阅读视图的渲染缺陷，不改其内容与结论。

**观察到但本轮未动的一处措辞**：`dangerous-engine.md §8` 那句仍写「某迭代 P4 触发**收敛闭环熔断**」，而 ITER-0110 之后 dangerous 用的是 `bounded-convergence.md` 的「有界收敛纪律」（同文件 §6 与 §9 都是这个说法）。这是同一行里的措辞不统一，不是错误——上下文足以让读者知道指的是哪个熔断。AC6 把改动面限定在「这一处指针」，故未顺手改；记在这里，等后续动 dangerous 时一并收。

## TDD Pair Status

不适用。本迭代零新增可执行逻辑——改的全是规则散文与状态台账，唯一的新脚本是一次性的验收扫描器（`ac4-ac10-sweep.py`），它本身就是验证工具，不是被验证的产物。没有可先失败后通过的测试对象。

## Goal Calibration

无未闭合运行时信号。P4 执行期间未触发熔断、未产生 RCA、无中途改道。P3 定的 T1–T8 八步按序完成，无跳步、无追加动作。

## Completion Inputs

- 五件套合同校验：`concept` / `acceptance` / `tech_plan` / `changelog` / `verify_report` 全部 `status: ok`
- `AC_LIST.md`：`状态: ack-frozen`、`ACK 日期: 2026-08-20`，含一条 §5.3 修订记录（激活清单第三条是同一句话的镜像，原 AC3 会强制留下它）
- `TECH_PLAN.md`：`方案状态: pass`，用户审阅
- 证据热区 8 条全部 `passed`，`evidence.py verify --source hot` 全绿
- `handoff.py check` → `fresh`
- `sync-project-overview.py --check` → ok
- `sync-workflow-registry.py --check` → 随 `verify-ci.sh` 一并绿

## Gate Coverage

| 门禁 | 结果 |
|---|---|
| `bash scripts/verify-ci.sh` | 退出码 0 |
| `python3 scripts/audit-project-state.py --allow-unreleased` | 退出码 0，836 条 OK |
| `evidence.py verify --source hot` | 8/8 通过 |
| `handoff.py check` | fresh |
| 产物合同 ×5 | 全 ok |
| `ac4-ac10-sweep.py` | PASS（A 组 0 命中 / B 组 0 失败） |

`milestones.backlog_set` 是本轮唯一一处被既有 CI 直接卡住的删除动作——只删文件或只删索引行会立刻红。其余改动没有机器兜底，这一点在 `.ai/debt.md` 已如实登记。

## References Compliance

- 本迭代无 `.ai/references/` 外部参考资料。
- **分层不破**：改的三份规则文件各在自己那一层（SOP Core 的 `00_System_Prompt/`、扩展层的 `55_Extension_ConvergenceLoop/` 与 `65_Extension_Dangerous/`），没有把某层职责挪进另一层。共用真源 `bounded-convergence.md` 未动；AC6 的指针改动方向正是让 dangerous 更贴合 ITER-0110 立的分工。
- **产物链不破**：每条改动都追得到 AC，没有 AC 覆盖不到的附带动作。
- **DRY 不破**：两处镜像都删且不补替代话术，避免制造第三、第四个「什么时候开 loop」的真源；`dangerous-engine.md` 的指针改成直指真源，少一跳转述。
- **模板 SSOT 不破**：`templates/rule-card.md` 与两份入口模板本轮未动。按 `migration-schema.md §5` 判定**不触发 `[regen-entrypoints]`**——入口模板只引用 `logic-protocol.md` 的路径而不嵌其内容，`rule-card.md` 全文未提收敛闭环，改动没有流进目标项目的 `CLAUDE.md` / `AGENTS.md`。该判定已写入 `.ai/MILESTONE.md §5.4`。
- **升级处置**：目标项目侧无受管文件形态变化，无 `[global-install]`、无 `[restamp]`、不需要新增迁移配方。

## Remaining Risks

- **冻结靠自觉，没有机器能拦**。真正的强制只有删除，而删除正是本轮明确不做的。已按同口径记入 `.ai/debt.md`，随 MILE-0016 R13 的最终处置自然消解。
- **AC3 那 1 个字符的偏差已如实记录，但它暴露的是 AC 写法的一类通病**：把「删一条列表项」写成「删除行恰为 1 行」，忽略了列表末项标点会跟着变。下次写这类逐行断言时应留出机械后果的余地。
- **`dangerous-engine.md §8` 的「收敛闭环熔断」措辞未统一**（见 Verification Results），影响仅限阅读一致性，不改变行为。
- **R13 判 loop 去留时要的使用数据仍然不存在**。本轮堵住了模型自己制造使用数据的口子，但采集本身归 R11，尚未落地；在那之前 R13 没有判据。

## Handoff / Next Step

ITER-0116 已具备收口条件。MILE-0016 的 R5 完成后，下一路线项按 `.ai/MILESTONE.md §5.3` 的路线表继续。本轮不切版、不打 tag、不提交——工作树里同时躺着 ITER-0115 与 ITER-0116 两轮的未发布改动，何时发布由用户决定。
