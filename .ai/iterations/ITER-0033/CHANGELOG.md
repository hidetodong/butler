# CHANGELOG — ITER-0033（MILE-0003 R7 说人话三条硬标准 + 发长文前自检）

> 对象级变更流（ADD/EDIT/DELETE），绑 AC。收口归档切片。

## ADD

- `Coder/20_Workflow_Lifecycle/artifact-style.md §2` 标准二「比喻要落地」——全仓新增的说人话硬标准（比喻须落到具体对象、点明对应本任务里的谁；悬空比喻即删）。pre-R7 `git grep "比喻\|类比"` 零命中。→ AC1/AC2
- `Coder/00_System_Prompt/presentation-protocol.md §7`「对话也说人话（三条硬标准）」——新增节：声明对话层同守三条 + 对话层发长文前自检；只引用 `artifact-style §2` 真源、不重述定义。→ AC5

## EDIT

- `artifact-style.md` frontmatter + §1：`scope` 从"四件套字段正文"扩到"所有面向人落地文档"（四件套 + 交付总结 + 知识文件夹 + handoff）；三条定位为跨对话与文档的通则、本口径为单一真源；title 改「面向人落地文档书写口径」。→ AC3
- `artifact-style.md §2`：从「讲人话（反黑话）」就地改写为「说人话三条硬标准」——原判据 / 反面词 / 结构锚点归入标准一 & 三，交叉引用 §4.3 去重。→ AC1
- `artifact-style.md §7` 边界：「不管对话层」收窄为「不管对话层的呈现结构」+ 加显式例外（§2 三条为跨层通则、`presentation-protocol` 引用它），消解与新 §2 的表面矛盾。→ AC1
- `artifact-style.md §8`：标题「收口前自检」→「发长文 / 收口前自检」，加逐条扫三条、适用面从四件套扩到所有面向人长文档。→ AC4
- `presentation-protocol.md` frontmatter：`scope` 增"说人话三条硬标准的对话层引用（定义真源在 artifact-style §2）"。→ AC5
- `presentation-protocol.md` 顺移编号：原 §7 弹性条款→§8、原 §8 边界→§9；内部引用校正 §2 `(见 §8)`→`(见 §9)`、§8 `§3-§6`→`§3-§7`、样例注 `§3-§6`→`§3-§7`。→ AC5
- `templates/rule-card.md`：§输出呈现条 + §产物书写条同步收录说人话三条（标"真源 artifact-style §2"）；产物条 scope 从"四件套"扩到"面向人落地文档"。→ AC6
- `Coder/README.md`：§目录说明 `presentation-protocol` 条（增说人话三条对话层引用）+ `artifact-style` 条（改"面向人落地文档书写口径 + 说人话三条真源"）两处 scope 描述同步。→ AC7

## DELETE

- 无。旧 §2「讲人话（反黑话）」是**就地改写**为「说人话三条硬标准」（内容承接、非删除）；无文件 / 字段删除。
