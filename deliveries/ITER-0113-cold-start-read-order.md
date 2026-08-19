# ITER-0113 · 冷启动读序正式定义与四载体对齐（MILE-0016 R2）

- 交付级别：迭代交付（小版本）
- 收口日期：2026-08-19
- 所属里程碑：MILE-0016（Butler 瘦身与重造）

## 本次交付目标

「新会话从零开始，先读哪些文件、按什么顺序读」这件事，butler 仓里同时躺着五份不一样的答案：规则真源写 5 步，仓根入口写 7 步，Codex 部署模板写 4 步，`Coder/README.md` 写成一段 3 步散文，而 Claude 的部署入口一步都没有。五份互相抄、抄漏了没人发现，因为没有任何机器检查能看出它们不一致。这一轮把读序收成一份真源加四份受校验的字节投影，顺手把三条被所有投影集体丢掉的硬约束写回步骤里，并给 Claude 宿主补上它一直缺的那一段。

## 已完成内容

- 读序改成五步语义阶段（欠债与边界 → 时间线 → 断点 → Goal 状态 → 产物与代码），正文用 `butler-context-order:begin/end` 一对标记圈起来，`Coder/40_Context_Management/context-persistence.md §6` 是唯一真源，全文 1194 字节、6 个非空行、7 个 md 指针。
- 三条以前只写在散文里、投影一份没带上的硬约束，这次写进对应步骤本身：查旧迭代要先跑 state-ledger `check`、再沿 `.ai/state-index.json` 定向读命中的那一个冷分片，禁止默认读整个 `.ai/history/`；断点要先跑 `handoff.py check` 看三态（`fresh` 才读、`stale` 先 `sync`、`error` 先修权威状态）；Goal 状态要按三份产物重算，宿主原生 Goal 只是可重建投影。
- 四处载体各投一份，正文与真源逐字节相同：仓根 `AGENTS.md`、`Coder/README.md`、`templates/AGENTS.md.template`、`templates/CLAUDE.md.template`。最后一份是净新增的「会话起始：恢复项目状态」章节——Claude 宿主此前完全没有读序。
- `tools/context-budget/context_budget.py` 接手守这四份投影：任一份与真源不一致就报 `order projection mismatch: <文件名>`，指名到具体是哪一份；任一载体缺标记直接 fail-closed 抛错，不静默跳过。这套提取与比对路径是从 ITER-0111 的 L0 投影机制里抽出来复用的，不是新造的第二套。
- 光比字节抓不到「真源自己写错」，所以另加三条结构断言：步骤编号必须连续 `1.`–`5.`、每步至少含一个 `.ai/` 路径、三条硬约束的锚点字符串各自绑死在指定步骤里。
- `scripts/verify-codex-foundation.sh` 里那张 9 项硬编码路径列表删了——它其实是读序的第五份真源，改了真源它也不会红；换成校验读序块标记与最终 `Coder/` 真源步骤的位置。
- 规则卡与读序块的分工写死：读序块独占「按什么顺序读哪些文件」，规则卡独占「handoff 是派生视图、什么时候 sync」，两边各留一句指向对方，不互相复述。

## 关键变更 / 用户可感知变化

- **Claude 宿主的每次会话多约 1194 字节**。这是净新增，不是改写；换来的是 Claude 侧终于和 Codex 侧读同一份读序。
- **改读序只改一个地方**：`context-persistence.md §6` 的标记块内。改完必须跑一次 `context_budget.py check`，四处投影同步不上 CI 就红，指名是哪一份没跟上。
- **已部署的老项目暂时拿不到新读序**。改的是模板，老项目要等 `/butler:upgrade` 带 `[regen-entrypoints]` 才会重新渲染入口。这段时间里 butler 仓自己和新部署的项目有新读序，老项目还是旧的——Codex 侧是旧 7 步，Claude 侧仍然没有。
- **同源投影点从三处变成七处**（L0 三处 + 读序四处）。一致性由机器保证，但每次改真源都要跑一遍同步，这是有意付的代价。

## 高层影响范围

- 规则文件 3 份：`context-persistence.md`（读序正文与过渡措辞）、`Coder/README.md`（散文换投影块）、`templates/rule-card.md`（补反向指针）。
- 入口模板 2 份：`templates/AGENTS.md.template`、`templates/CLAUDE.md.template`——两份都改了，下个发布版必须带 `[regen-entrypoints]`，已登记在 `.ai/MILESTONE.md §5.4`。
- 机器侧 3 处：`tools/context-budget/context_budget.py`（通用标记块提取器 + 读序投影校验 + 结构断言 + 四项 metrics）、其测试套（12 → 19 个用例，新增 7 个方法覆盖 10 个负例场景）、`scripts/verify-codex-foundation.sh`（删列表换标记校验）。
- 顺带修 1 处：`scripts/test-goal-host-wiring.py` 里断言的 token 从 `方案 verdict` 改成 `` `.ai/TECH_PLAN.md` 的方案状态 ``。后者才是 TECH_PLAN 的真实字段名，读序改写后正文用的是它；这条断言守护的对象没变，只是 token 跟上了真实字段名。
- 未触碰：`handoff-spec.md` 的 `02_SESSION_HANDOFF.md` 格式契约、双台账结构与 `state-index.json` 路由公式、L0 渐进读取内核及其既有三处投影、`.ai/project/` 剩下的两份文件。未切版、未发布。

## 验证方式与结果摘要

- 12 条验收标准全部达成，9 条机器证据全部 passed，1 条失败记录按纪律保留作诊断。
- 投影校验的负例是实打实造出来的，不是只断言「报错了」：四处投影各自被单独篡改时诊断指名该文件且不连坐其他三处，改真源时四处同时报失配，抽掉标记时 fail-closed 且诊断带文件名，三条结构断言各自被破坏时诊断指名缺的是哪一条。
- 部署路径端到端验过：真的跑了一遍 `render-project-entrypoints.py` 渲染到临时目录，渲染出来的 `CLAUDE.md` 与 `AGENTS.md` 里的读序块与真源逐字节相同。
- 完整 `scripts/verify-ci.sh` 退出码 0（32 项 pytest 全过），状态审计退出码 0，除「工作树有未发布改动」「tag 不指向 HEAD」两条发布态亮牌外无漂移。
- 技术方案里估的「用例计数不少于 21」是拍脑袋的估数，实际是 19 个用例方法覆盖 10 个负例场景。验收标准的真实门槛是「新增 fixture 不少于 6 条」，实际 10 条，达标；这里如实记下估数与实测的差，没有回头改方案。

## 已知剩余风险 / 延后事项

- **覆盖面变化，不是等价替换**。删掉的那张硬编码列表守的是「读序路径在 `AGENTS.md` 里按行号递增」；接手的投影校验守的是「四处逐字节相同」。真源自己把步骤顺序写错了，投影校验只会报四处一致——它证明的是「没人偷偷改其中一处」，证明不了「这五步本身是对的」。能兜的只有新增的三条结构断言，而结构断言兜得住编号断开、指针缺失、锚点挪位，兜不住语义层面的顺序错误。真要守住这一层得有运行时观测，归 MILE-0016 R11。
- **老项目的滞后本轮没有兜底**。只登记了 `[regen-entrypoints]`，实际让老项目拿到新入口要等 R15 的 v4.0.0 迁移配方。
- **1400 字节的上限不是免费额度**。实测 1194，留的 206 字节余量是给后续增补的缓冲，不是可以填满的空间——每多一个字节，主力宿主的每次会话都要付。
- **七处投影会和 R9 撞上**。MILE-0016 后面的根布局改名要同时动这七处同源投影，届时一次改不齐 CI 就会红——这是机制在按设计工作，但要预留返工时间。

## 引用

- `.ai/iterations/ITER-0113/CONCEPT.md`
- `.ai/iterations/ITER-0113/AC_LIST.md`
- `.ai/iterations/ITER-0113/TECH_PLAN.md`
- `.ai/iterations/ITER-0113/VERIFY_REPORT.md`
- `.ai/iterations/ITER-0113/CHANGELOG.md`
- `.ai/iterations/ITER-0113/evidence/`
