# TECH_PLAN — ITER-0041（MILE-0004 R6 · 认亲边缘 + 非回归门 + 收尾）

> 监督态自驱。目标见 CONCEPT、验收见 AC_LIST，不重述。全为规则文档接线（扩 1 节 + 加 1 节 + 用法节 + flip，无新文件）。

## 设计决策（DD）

- **DD1 · 认亲对账扩在 `prd-update §4` 内、改版主流程零改动**：R5 的 §4 只有"新增/消失"两态；R6 在同节**追加**"改名/合并/拆分"认亲对账，§2 检测 / §3 落盘 / §5 三态 / §6 路由**一字不动**——认亲是 §4 内部的登记表处置细化，不是新流程。
- **DD2 · 认亲靠启发式候选 + 提议确认（松边）**：检测"slug 消失 + slug 新增"配对——标题/内容相近→改名候选、一消失对多新增→拆分候选、多消失对一新增→合并候选；一律**提议给用户确认**，不自动认。改名落法守 `references-schema §4`（保留旧 slug、只更新登记表标题/章节字段）。拿不准**退回 R5 新增/消失基础态**（宁可不认也不误并）——这是松边的兜底。
- **DD3 · 非回归门做成 `references-schema` 独立小节 + 硬判据**：不是散文，是"列举不得触碰的非 PRD 流 + 验证 = 这些文件/路径 `git diff` 为空"的可核对契约。放 `references-schema`（PRD 子系统的契约入口）最自然，作为整个子系统 R1–R6 的常驻边界声明。
- **DD4 · HUMAN_GUIDE 用法节口径回归则真源**：`/prd update`·`/prd status` 的人话说明摆在里程碑节之后（同属"大规格/大版本"入口族），只讲"怎么用、会发生什么"，机制真源仍指 `prd-update.md`、不在 HUMAN_GUIDE 重写规则。
- **DD5 · flip 用既有翻牌手法 + 收官核对**：`references-schema §4` 认亲边缘句 + `§8` R6 行由待→✅（指 `prd-update §4`），至此 §8 表 R1–R6 全绿；收口自检额外确认 MILE-0004 §5.3 路线图六项全 ✅。
- **DD6 · 说人话自检当场修**：三份 PRD 子系统文件通读，裸英文/悬空比喻当场修（属本迭代 dogfood 改动、记进 changelog）；无问题则只在 VERIFY 记"已自检通过"。

## 影响面（章节级）

| 文件 | 改动 | AC |
|---|---|---|
| `Coder/40_Context_Management/prd-update.md §4` | 追加改名/合并/拆分认亲对账（启发式候选 + 提议确认 + 守 slug 终身 + 松边退回基础态）；§2/§3/§5/§6 不动 | AC1–2 |
| `Coder/40_Context_Management/references-schema.md` | 加"非回归门"小节（列非 PRD 流 + git diff 为空判据）+ flip §4 认亲边缘句 + §8 R6 行 ✅ | AC3/AC5 |
| `HUMAN_GUIDE.md §5` | 加"PRD 先行（大规格版本化）"用法节：/prd update + /prd status 人话说明 | AC4 |
| `Coder/40_Context_Management/{references-schema,prd-split,prd-update}.md` | 说人话三条自检的零星修正（若有） | AC6 |

**不碰**：`references-schema §3` 登记表字段（不加列）、`prd-split` 切分算法、`prd_version` 钉版字段、`prd-update §2/§3/§5/§6`、核心 P1–P5、非 PRD 流、`project-digest`/`context-persistence`/hook/`VERSION`；不做全自动认亲；不切版。

## Execution Steps（可勾选）

- [ ] S1 · `prd-update §4` 追加改名/合并/拆分认亲对账（启发式候选→提议确认、绝不自动认、改名守 slug 终身、松边退回新增/消失）→ AC1/AC2
- [ ] S2 · `references-schema` 加"非回归门"小节（列 opt-in 不得碰的非 PRD 流 + 验证判据 git diff 为空）→ AC3
- [ ] S3 · `HUMAN_GUIDE §5` 加"PRD 先行"用法节（/prd update 改版同步每步确认 + /prd status 只读看板，真源指 prd-update.md）→ AC4
- [ ] S4 · flip `references-schema §4` 认亲边缘句 + `§8` R6 行为 ✅ 已由 prd-update §4 落地 → AC5
- [ ] S5 · 通读 `references-schema`/`prd-split`/`prd-update` 三份说人话三条自检、当场修 → AC6
- [ ] S6 · scope 守恒（`git status`）+ 非回归核对（`git diff` 非 PRD 流零改动、R1–R5 主体未碰）+ 收官核对（MILE-0004 §5.3 六项全 ✅、references §8 表全绿）→ AC7
- [ ] S7 · P5 独立复核（干净上下文子 agent、对抗式）→ 收口

## 验证策略

全 auto·可靠（规则文档）：每 AC 读改后正文确认 + `git grep`/`git diff` 核守恒。核心对抗点＝**松边不硬认**（认亲提议→确认、退回基础态、不自动误并）+ **slug 终身**（改名只换门牌）+ **非回归门可验证**（判据 git diff 为空、且本轮非 PRD 流真零改动）+ **不越界**（认亲只扩 §4、改版主流程/契约结构/钉版字段未碰、不切版）+ **收官完整**（六块全 ✅、§8 全绿）。dogfood：四件套 + 三子系统文件过说人话三条。无人测道残余。
