<!-- butler-artifact-template: 1.0.0 artifact=verify_report -->
# VERIFY_REPORT — ITER-0114

## Verification Summary

- 15 条验收标准全部达成。10 条机器证据（`ac1-ac2-generate` / `ac3-ac4-check` / `ac5-ci` / `ac6-ac7-invariants` / `ac8-ratchet` / `ac9-ac10-frontier` / `ac11-order` / `ac12-ac13-sweep` / `ac14-tests` / `ac15-audit-delivery`）全部 passed，无失败记录留存。
- 置信档分布：AC1–AC6、AC8–AC11、AC14 为 auto·可靠（确定性断言，负例全部在临时仓副本上现造）；AC7、AC12、AC13、AC15 为 auto·弱档——机器只查得出条目改没改、字样在不在、段落写没写，判不了写得对不对，最终仍靠人读。无 human·待人 档。
- 本轮有两条验收标准在执行中发现缺陷，都按 `iteration-schema.md §5.3` 退回 `draft` 重新 ACK，没有偷改冻结后的标准；修订记录写在 `.ai/AC_LIST.md` 的 frontmatter `修订记录:` 键里（`## 修订记录` 二级标题会被产物合同判 drift，这条冲突已记入 `.ai/debt.md`）。

## AC Status

- [x] AC1 (auto·可靠): `scripts/sync-project-overview.py` 在位；`--check` 与 `--write` 互斥必选（同传抛 `SystemExit`），`--project-root` 与 `--butler-root` 各自可指定。五个源头逐个删除后 `--write` 均报 `missing source: <被删路径>` 且不产出残缺页，另加 `tools/` 整个不在的第六个负例。证据 `ac1-ac2-generate`、`ac14-tests`。
- [x] AC2 (auto·可靠): 页首两行含「请勿手改」与生成命令原文，正文零手写标记区。五节数字逐一与源头实测比对：版本 3.6.0 = `VERSION`；里程碑 16 行 = 台账 16 行；工作流 13 行 = `registry.json` 的 `workflows` 长度 13；驻留工具 22 项 = `tools/` 实际子目录 22 个；规则目录 12 个 = `Coder/` 实测 12 个，且各目录规则文件数逐个对上。证据 `ac1-ac2-generate`。
- [x] AC3 (auto·可靠): 真仓 `--check` 退出码 0；五节各改一处后退出码 1 且诊断为 `overview section drift: <该节标题>`，并断言**不连坐**其余四节；改节标题报 `overview section set mismatch`；产物整个删掉报 `overview missing`。证据 `ac3-ac4-check`。
- [x] AC4 (auto·可靠): `OVERVIEW_MAX_BYTES = 12000` 写死在生成器常量；实测 8902 字节（`ac3-ac4-check` 捕获时刻），收口写盘改动双台账后重算为 8897 字节，余 3103。造 400 个合成工具目录撑爆上限后诊断含 `overview too large:` 与实测值、上限，且不写盘。证据 `ac3-ac4-check`、`ac14-tests`。
- [x] AC5 (auto·可靠): `scripts/verify-ci.sh` 含 `sync-project-overview` 两行（L41 测试 / L42 `--check --project-root .`），与 artifact-pipeline（L37/L38）、context-budget（L39/L40）、domain-contract（L43/L44）三组排成同一类「先跑测试、紧跟校验」的成对形状，四组校验行 L38→L44 连续。完整 `bash scripts/verify-ci.sh` 退出码 0。证据 `ac5-ci`。
- [x] AC6 (auto·可靠): `.ai/invariants.md` 在位，`.ai/project/invariants.md` 与 git 索引里均已无该路径；条目数迁移前 47、迁移后 47；暂存区记为 `R100 .ai/project/invariants.md → .ai/invariants.md`（全等重命名，提交后 `git log --follow` 即可穿透）；正文条目级改动仅 4 行（两条各一删一增），其余为文件头新增。证据 `ac6-ac7-invariants`。
- [x] AC7 (auto·弱档): 「收口是原子仪式」改为指向 `iteration-schema.md §5.5`，不再出现 `fold receipt`、不再写步数；「冷启动读序固定且只有一处真源」改为指向 `context-persistence.md §6`，不再出现旧四步措辞；两条都保留 `*为什么*` 半句。另反向核对指针指得对：`§5.5` 实测 4 步、第 4 步是收口自检。**口径说明见下方 Verification Results**——AC7 里「写四步」这半由指针指向的真源承担，条目自身按同一条 AC 的第三句要求不复述步骤清单。证据 `ac6-ac7-invariants`。
- [x] AC8 (auto·可靠): 文件头三条写作纪律齐备，登记基线 16 并点名卡它的 `scripts/sync-project-overview.py --check`，声明「16 是欠账不是允许额度」并指向 `.ai/debt.md`；实测无指针条目 16 条，与生成器常量 `INVARIANT_POINTER_EXEMPT = 16` 一致。加第 17 条后退出码 1、诊断含 `invariants without source pointer: 17 > 16` 并把无指针条目逐条列出；删一条降到 15 则放行——棘轮只往紧的方向走。证据 `ac8-ratchet`、`ac14-tests`。
- [x] AC9 (auto·可靠): `.ai/project/frontier.md` 与 `.ai/project/` 目录均不存在，git 索引也已移除。退役前原文实测「当前形态 15 条 / 活跃战线 6 条 / 下一个瓶颈 7 条 = 28 条」，与变更流 DELETE 段声称的数字逐节对上；三类去向（并入生成段 6 处 / 迁入 `.ai/debt.md` 3 处 / 可弃 6 处）在段内齐备，无一条无交代。证据 `ac9-ac10-frontier`。
- [x] AC10 (auto·可靠): `.ai/debt.md` 删除行 0、新增行 6，条目数 3 → 9；4 条迁入项各写明来源 `.ai/project/frontier.md` 与迁入日期 2026-08-20（ITER-0114）；本轮新记的两条不冒充迁入项。证据 `ac9-ac10-frontier`。
- [x] AC11 (auto·可靠): 读序第 5 步含 `.ai/OVERVIEW.md` 与 `.ai/invariants.md` 两个指针，措辞为「按需读 … 不是必读」两句并存；五步语义结构未增删；`context_budget.py check` 退出码 0，`order_bytes` 1284（上限 1400）、`order_nonempty_lines` 6、`order_pointers` 9、`order_projections` 4；重跑 ITER-0113 的 `ac2-projection-sha.py` 8 项全 OK，五处仍逐字节相同（sha256 前缀 `29fd7f826b14500c`）；context-budget 19 个用例全过。证据 `ac11-order`。
- [x] AC12 (auto·弱档): 按「零活引用」口径扫描，`.ai/project/invariants.md` 与 `.ai/project/frontier.md` 均零活引用；叙述性提及逐处白名单登记（生成器 docstring、`context-persistence.md`、`.ai/invariants.md`、`.ai/debt.md`、`.ai/RUN_LOG.md`、`.ai/milestone-backlog/`、`.ai/milestones/`），并反向断言白名单不是空转（三处确有出处说明）。`.ai/project/workspaces.md` 的 11 处引用按 Out of Scope 有意保留。`Coder/README.md` 已注册生成器，`context-persistence.md` 写了重算命令与三份产物的性质分工。证据 `ac12-ac13-sweep`。
- [x] AC13 (auto·弱档): `.ai/MILESTONE.md §5.4` 末尾三条在场——前提修正一（`frontier.md`，实测证据为停更 commit `0cf01e9` 与正文 v3.5.1，规律表述「整体覆写只在有东西强制触发重写时才活得下来」）、前提修正二（`invariants.md`，实测证据为第 47 / 42 两条已假与 16 条无指针，规律表述「纯追加只保证新条目不覆盖旧条目，不保证旧条目描述的东西没变」）、R3 发布处置追记（两份入口模板再次改动，`[regen-entrypoints]` 要求不变；`.ai/project/` 命名去留归 R9）。证据 `ac12-ac13-sweep`。
- [x] AC14 (auto·可靠): `scripts/test-sync-project-overview.py` 10 个测试方法全过，负例场景 11 个（五源缺失 5 个子例 + tools/ 整个不在 + 逐节漂移 + 节集不匹配 + 体量超限 + 棘轮超基线 + 目录无说明），≥ AC 要求的 8 条。七类负例逐一对上具体用例；七条诊断串各自被 `assertIn` 精确断言，7 个负例方法体内全部有诊断内容断言，没有一条只断言退出码。正例三条齐备。证据 `ac14-tests`。
- [x] AC15 (auto·弱档): `scripts/audit-project-state.py --project-root . --allow-unreleased` 退出码 0，非 OK 行只剩两条 `UNRELEASED` 发布态亮牌与历史迭代的 `INFO` 诊断留存行，零 `DRIFT` / `ERROR`。交付总结双格式在位、HTML 占位符全填、ROADMAP 块按迭代级删除、单文件自包含无外链；覆盖面事实、估数与实测的差、两条 amend 均在正文中逐句可查；引用段 10 条路径指针，未嵌四件套全文。证据 `ac15-audit-delivery`。

## 人测道小结

- N/A（本轮无 human·待人 档 AC，人测道不适用）。AC7 / AC12 / AC13 / AC15 四条本可归人测，但都能造出弱检查（条目改没改、字样在不在、登记段落在不在、交付句子在不在），按 `testing-strategy.md §3` 仍归自动道弱档。

## Evidence Index

| Evidence ID | AC | 强度 | Outcome | Record |
|---|---|---|---|---|
| ac1-ac2-generate | AC1,AC2 | reproduced | passed | `.ai/iterations/ITER-0114/evidence/ac1-ac2-generate/record.json` |
| ac3-ac4-check | AC3,AC4 | reproduced | passed | `.ai/iterations/ITER-0114/evidence/ac3-ac4-check/record.json` |
| ac5-ci | AC5 | reproduced | passed | `.ai/iterations/ITER-0114/evidence/ac5-ci/record.json` |
| ac6-ac7-invariants | AC6,AC7 | reproduced | passed | `.ai/iterations/ITER-0114/evidence/ac6-ac7-invariants/record.json` |
| ac8-ratchet | AC8 | reproduced | passed | `.ai/iterations/ITER-0114/evidence/ac8-ratchet/record.json` |
| ac9-ac10-frontier | AC9,AC10 | reproduced | passed | `.ai/iterations/ITER-0114/evidence/ac9-ac10-frontier/record.json` |
| ac11-order | AC11 | reproduced | passed | `.ai/iterations/ITER-0114/evidence/ac11-order/record.json` |
| ac12-ac13-sweep | AC12,AC13 | captured | passed | `.ai/iterations/ITER-0114/evidence/ac12-ac13-sweep/record.json` |
| ac14-tests | AC14 | reproduced | passed | `.ai/iterations/ITER-0114/evidence/ac14-tests/record.json` |
| ac15-audit-delivery | AC15 | captured | passed | `.ai/iterations/ITER-0114/evidence/ac15-audit-delivery/record.json` |

## Verification Results

- **负例全部现造，不是走过场**。AC1 / AC3 / AC4 / AC8 的负例都在临时仓副本上现场制造再跑，逐条断言诊断字符串。逐节漂移那组还额外断言另外四节**不**被报出，防止诊断退化成「一律全报」；棘轮那组另加一个反向用例（删一条无指针条目应当放行），证明它只防增量、不是简单的等值校验。
- **AC7 的口径如实说明**。AC7 第一句要求「收口仪式那条写四步且第四步是自检」，第三句要求「两条都不再复述完整步骤清单」——两句在字面上互斥。本轮按第三句执行：条目本身不写步数，只指向 `iteration-schema.md §5.5` 并留下「为什么」。第一句由指针承担，证据脚本因此加了一条反向核对——真源 `§5.5` 实测确实是 4 步、第 4 步确实是收口自检，指针指得对。这是解释而非豁免：如果真源不是四步，这条证据就会红。没有为此再走一次 amend，是因为同一条 AC 的第三句已经给出了唯一自洽的读法。
- **两条 AC 走了 §5.3 的 amend，没有偷改冻结标准**。AC2 的「驻留工具清单（24 项）」是冻结时把 `ls` 输出里的 `.` 与 `..` 数了进去，实际 22，改成对源头的引用「与 `tools/` 实际子目录一致，当前 22」；AC12 的「零命中」无法达成——Decision Map 的 `frontier`（依赖 DAG 的可推进前沿）与本轮退役的知识文件同名不同物，且迁出留痕本身必须提到旧文件名，改为「零活引用 + 叙述性提及逐处白名单登记」，同时把 `migrations/`（已发布配方冻结，改了 manifest 一致性校验会红）与 `.venv/` 排除出扫描面。两次都退回 `draft` 重新 ACK。
- **fail-closed 逼出两个漏登记的目录**。生成器要求 `Coder/` 下每个目录在 `Coder/README.md` 里有职责说明，否则拒绝出页。第一次 `--write` 当场撞上 `55_Extension_ConvergenceLoop/` 与 `60_Extension_CodeReview/` 两个此前没写说明的目录，补上后才通过——这条约束在第一次使用时就抓到了真问题，不是摆设。
- **一处实现缺陷由证据脚本抓出**。生成器最初读 `registry.json` 的 `claude.command` / `codex.command`，实际字段是 `claude.name` / `codex.name`，导致工作流节渲染成 0 行；`ac1-ac2-generate` 的「工作流行数与 registry 一致」断言直接报出「registry 13 / 页面 0」。修好生成器与合成夹具后重生成，产物由 8583 字节变为 8902 字节（收口写盘改动双台账后重算为 8897）。
- **与 TECH_PLAN 的偏差如实记录**。方案 Test Strategy 估「新增 fixture 不少于 9 条」，实测是 10 个测试方法覆盖 11 个负例场景；AC14 的真实门槛是「不少于 8 条」，达标。方案原列 `ac5-ac15-ci-audit` 一条证据，实际拆成 `ac5-ci` 与 `ac15-audit-delivery` 两条——AC15 依赖交付总结文件存在，必须排在交付写完之后。AC 覆盖未变，未回头改已 ACK 的方案。
- **交付 HTML 在真实浏览器里验过渲染**。用 ego-browser 打开渲染结果核对：7 个二级标题齐备、101 个 `<code>` 与 44 个列表项正常渲染、无残留 `{{占位符}}`、无未转义标签或实体外泄、页面无横向溢出（`scrollWidth` = `clientWidth`）。第一版曾把模板自身的填槽说明注释一起填了槽（30920 字节），剥掉注释后为 16479 字节。

## TDD Pair Status

- N/A（TECH_PLAN 未声明 TDD cycle）。

## Goal Calibration

- 当前无未闭合运行时信号（N/A）。开工前的两条前提证伪已在 P1 阶段回流到 `.ai/CONCEPT.md` 与 `.ai/MILESTONE.md §5.4`，不作为遗留信号带出本迭代。

## Completion Inputs

- Review Verdict: pass
- Completion Blockers: none

## Gate Coverage

- 质量门禁：`bash scripts/verify-ci.sh` 退出码 0，新增的两行（单测 + `--check`）与既有三组 `--check` 成对排列，无跳过、无单点豁免。
- 状态审计：`python3 scripts/audit-project-state.py --project-root . --allow-unreleased` 退出码 0。非 OK 行为两条 `UNRELEASED` 发布态亮牌（工作树有未发布改动、v3.6.0 tag 不指向 HEAD）与历史迭代的 `INFO` 诊断留存行，零 `DRIFT`。OK 计数随收口写盘继续变动，此处记录的是 `ac15-audit-delivery` 捕获时刻的状态。
- 产物契约：四件套与变更流均通过 `tools/artifact-pipeline/contract.py` 的章节与字段校验。
- 上下文预算：`tools/context-budget/context_budget.py check` 退出码 0，L0 与读序两个受守护块的体量均在上限内（读序 1284 / 1400）。
- 全貌产物自校验：`python3 scripts/sync-project-overview.py --check --project-root .` 退出码 0，五节逐节 sha256 与源头一致，棘轮未触发。

## References Compliance

- 本迭代无 `.ai/references/` 外部参考资料，无引用合规项需核（AC_LIST「External References」为 N/A）。
- 内部规则引用一致：`.ai/OVERVIEW.md` 的源头标注、`.ai/invariants.md` 两条修正的指针、`.ai/debt.md` 迁入项的出处，均指向实际存在的文件与章节；生成器对 `Coder/README.md` 缺说明目录 fail-closed，覆盖了目录侧的存在性。

## Remaining Risks

- **`--check` 证明不了「有人读过」**（本轮最实的缺口，已写进交付）。它只能证明生成段与机器源头一致；`.ai/OVERVIEW.md` 按 AC11 的定位是按需读、不在冷启动必读路径上，「生成得再准也可能永远没人打开」这个风险坐实了。运行时观测归 MILE-0016 R11。
- **生成器只在 butler 仓自己验过**。`registry.json` / `Coder/README.md` / `tools/` 是规则仓的源头，双台账与 `VERSION` 才是项目侧的；`--butler-root` 与 `--project-root` 已把这层区分做进接口，但两者不同的目标项目场景本轮未验、也未接部署链，归 R15。
- **12000 字节上限没有依据**。读序块的 1400 有依据（每次会话都付），全貌产物按需读，没有同等的成本锚点。当前 8897，余量 3103，防的是无上限膨胀那类失控，真实合理值要等有人实际读过才知道。
- **16 条无指针的旧账留着**。棘轮只防增量，这批恰恰是最容易悄悄变假的一类（实测已假掉两条）。已记入 `.ai/debt.md`，不补真源就永远是「基线」而不是「欠账」。
- **`iteration-schema.md §5.3` 与产物合同打架**。修订记录本轮写进 frontmatter，ITER-0112 则是直接改正文没留记录——两次绕法不一致，已记入 `.ai/debt.md`，要么放宽合同要么改 §5.3 措辞。
- **`.ai/project/` 这个名字仍在目标项目侧活着**。butler 仓自己删干净了，`workspace-scope-schema.md` 仍把 `.ai/project/workspaces.md` 当规格落点，名不副实，归 R9。

## Handoff / Next Step

- ITER-0114 收口，MILE-0016 R3 置 `closed`；`.ai/ITERATIONS.md` current 归 `none`。
- 下一项按里程碑路线是 MILE-0016 R4（`/butler:progress` 相关整理），本轮未触碰。
- 发布侧未动：未切版、未打 tag。下个发布版的迁移配方必须含 `[regen-entrypoints]`（R2 已登记，R3 只追记，不重复开条目）。
