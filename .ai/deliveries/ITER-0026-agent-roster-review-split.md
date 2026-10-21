# 帮手名册骨架 + 复核三拆 + 通用规矩单源化

> ITER-0026 · 迭代交付（小版本）· 收口 2026-07-05 · 所属 MILE-0003（R1，开篇）· /dangerous 危险模式自治执行（P2/P3 自审门替代 ACK，P4→收口自治，P5 升格独立复核）

## 本次交付目标

- MILE-0003 R1 开篇。butler 派出去的"帮手"一直是散的——真正的帮手只有"复核"一个，它的说明摊在 5 个文件里各写一遍，通用规矩（干净上下文、叫不起来如实说、权限约定、定义资料用时读）没有唯一真源。R1 立起**帮手名册骨架**（新建 `Coder/62_Extension_Agents/`），把复核帮手按性质**三拆**，通用规矩 **G1–G4** 提到总述当唯一真源。
- 兼作后续主体（知识文件夹）"总述 + 分文件 + 登记"模式的**内部预演**——先在帮手名册这个小场景把这套结构跑顺。

## 已完成内容

- **新建 `62_Extension_Agents/` 簇**：`overview.md`（帮手是什么 + 名册表三帮手 + 通用规矩 G1–G4 唯一真源 + 触发式加载 + 生态校准）+ `independent-review.md`（复核帮手完整中立定义：角色 Checker≠Maker / 输入 spec-only / 输出 confirm·refute·无法验证 / 禁止 / 隔离 / 只读权限）。
- **复核三拆**（按性质拆、带地址搬家）：`review-engine.md` 的共享审查流程（多维评审 / 评级 / 闭环 / 简评）留原地；通用规矩提总述；复核专有契约（触发 / 断言核对 / 输出衔接 / 诚实兜底）进 `independent-review.md`。保留 §1–§7 编号骨架不 renumber，防跨文件 §引用断裂。
- **通用规矩单源化**：G1–G4 完整正文现只在 `overview.md §3`；`dangerous-engine §7.3`、`verify-schema §4`、`logic-protocol §90`、`review-engine §6` 的 G2 引用全部改指总述。
- **注册**：`Coder/README.md` 三处登记（目录树 + 目录说明 + 详细说明），标明触发式加载、不进冷启动必读。

## 关键变更 / 用户可感知变化

- butler 的帮手从"散落 5 文件的复核一个"升级为**名册化、有唯一真源的通用规矩**；后续从 1 扩到 3（R4 更新说明 + 查过时）有骨架可挂。
- G2「叫不起来如实说、绝不假装做过」等通用规矩现在**只有一处正文**，其它文件回指——改一处即全仓生效，不再多处双写漂移。
- 向后兼容：纯规则文档重构，复核的对外行为语义（触发 / Checker 契约 / 断言核对 / 闭环 / 评级）逐条守恒，只是定义搬了家；未动阶段状态机 / 四件套字段 / AC 脊柱 / hook / 迭代里程碑双层 / VERSION。

## 高层影响范围

- 新增：`Coder/62_Extension_Agents/overview.md`、`Coder/62_Extension_Agents/independent-review.md`。
- 改（章节级）：`60_Extension_CodeReview/review-engine.md §1–§7`、`65_Extension_Dangerous/dangerous-engine.md §7.3`、`20_Workflow_Lifecycle/verify-schema.md §4`、`00_System_Prompt/logic-protocol.md §90`、`Coder/README.md`（三处注册）。
- 没碰：P1–P5 状态机、四件套 schema、AC 验收脊柱、hook 门禁、迭代/里程碑双层、`VERSION` / 根 `CHANGELOG.md`。

## 验证方式与结果摘要

- **8/8 AC 通过**，全 **auto·可靠**（规则文档一致性靠读正文 + grep 对账，确定性可复现）；无人测道。
- 危险模式 §7.3：P5 升格**独立复核**（fresh-context 子 agent，验证者≠实现者）——逐 AC **8/8 confirm、0 refute、0 Must Fix、0 Should Fix**，判定可收口；4 条 Nice-to-Have 均不阻断。复核另独立确认 P4 的 §6.3 误引修正属实。
- grep 对账：`§6.4` 全仓无一指向 review §6.4（全为无关处）；G1/G2 完整正文单源 `overview.md`；62 指针在 6 个文件铺开有效；AGENTS.md / Agent Skills 事实校准正确。

## 已知剩余风险 / 延后事项

- 三拆是"带地址搬家"，无机器手段防写岔——已用 grep + 独立复核兜底。
- P4 修正：`independent-review §5` 去掉了从旧 `review §6.3` 照搬的不准引用（§3.2 实为口径合并）。
- 独立复核 4 条 Nice-to-Have（均不阻断、多属本迭代 scope 外既有项）：历史归档 `ITER-0019/VERIFY_REPORT.md` 悬挂 review §6.4 指针（冻结快照不回改）/ `Review Policy` 与 `independent_review` 双名（改前既有，留后续统一）/ `review §1`·`logic §90` 的 G1 压缩回声（正文仍单源 overview，维护勿养回全文）/ 占位 `knowledge-fold`·`drift-check` 待 R4 落定。
- 已知遗留（非本迭代 scope）：`verify-schema` 一处 `review-engine §71` 引用疑为 §7.1/§4 笔误，原文既有，记待后续顺修。
- 本轮按危险模式北极星只自治到 **R1 单迭代收口**、未提交推送 / 未切版；MILE-0003 R2–R8 及收口切 **v2.0.0** 留后续指令。

## 引用（只引用路径，不嵌全文）

- 归档四件套 + 切片：`.ai/iterations/ITER-0026/CONCEPT.md` / `AC_LIST.md` / `TECH_PLAN.md` / `VERIFY_REPORT.md` / `CHANGELOG.md`
- 改动：`Coder/62_Extension_Agents/overview.md`、`Coder/62_Extension_Agents/independent-review.md`、`Coder/60_Extension_CodeReview/review-engine.md`、`Coder/65_Extension_Dangerous/dangerous-engine.md`（§7.3）、`Coder/20_Workflow_Lifecycle/verify-schema.md`（§4）、`Coder/00_System_Prompt/logic-protocol.md`（§90）、`Coder/README.md`
- 审计轨迹：`.ai/RUN_LOG.md` ITER-0026
- 里程碑：`.ai/MILESTONE.md`（MILE-0003 R1，开篇路线项）
