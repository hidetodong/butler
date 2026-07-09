# VERIFY_REPORT — ITER-0041（MILE-0004 R6 · 认亲边缘 + 非回归门 + 收尾）

> 逐条对 AC_LIST 核。验证 = 读改后正文核契约 + `git --no-pager diff` 核守恒（规则文档、确定性可复现）。

## 逐条

| AC | 结论 | 证据 |
|---|---|---|
| **AC1** 认亲扩 `prd-update §4`·松边·不改改版主流程 | ✅ | §4 拆为 §4.1 基础态 + §4.2 松边（改名/合并/拆分：启发式提候选 → 用户确认、绝不自动认）。diff 证 §2/§3/§5/§6 一行未动（改动全在 §4 区块 @@ -47,14）。 |
| **AC2** 认亲落法·守 slug 终身 + 松边退化 | ✅ | §4.2 成文：改名 = 保留旧 slug 只更新标题/章节（守 `references-schema §4`）；合并/拆分 = 用户确认后发新 slug + 旧置 removed；**松边红线**"拿不准退回 §4.1 基础态、宁可不认也不误并"落字，并给出误并代价论证。 |
| **AC3** 非回归门·常驻可验证红线 | ✅ | `references-schema §9` 新增：列五条非 PRD 流（对话驱动 / `origin/` brief / 扁平 references / 核心 P1–P5 / 里程碑合成）+ 真源；判据成文"这些文件/路径 `git diff` 为空"。**本轮亲自守**：diff --stat 证这五类文件零改动（见收官核对）。 |
| **AC4** HUMAN_GUIDE 加"PRD 先行"用法节 | ✅ | §5 里程碑与 `/review` 之间插入「PRD 先行（大规格版本化）」：首切随 `/milestone`、`/prd update` 改版同步（清单优先+diff 防漏、先冻后更、三态影响面、每步确认）、`/prd status` 只读、绝不静默动冻结工作；真源回指 `prd-update.md`。人话口径、无新造语义。 |
| **AC5** flip R6 收口指针 | ✅ | `references-schema §4` 认亲边缘句 flip 为"已由 `prd-update.md §4.2` 落地"；`§8` R6 行 flip 为"**R6 ✅ 已由 `prd-update.md §4.2` 落地**"。§8 表 R1–R6 六行全绿（R1✅/R2✅/R3✅/R4✅/R5✅/R6✅）。 |
| **AC6** 全子系统说人话自检·dogfood | ✅ | 三份过说人话三条：**松边**（"边界模糊、宁松勿错"/"拿不准就不硬认"）、**非回归门**（"回归=老功能被带崩"）、**opt-in 加层**（"要用才用"）、**启发式**（"只是猜"）首现即释；slug/soft 对齐/认亲在既有正文已释。裸英文变量：无。零星修正：无（旧文本已合规）。四件套同守。 |
| **AC7** scope 守恒 + 非回归 + 分层 + 收官核对 | ✅ | 见下"守恒 / 非回归 / 收官核对"。 |

## 守恒 / 非回归核对

- **scope 守恒**：`git diff --stat` = `.ai/*`（四件套 + 台账，迭代记账）+ `prd-update.md`（§4）+ `references-schema.md`（§9 + flip §4·§8）+ `HUMAN_GUIDE.md`（用法节）。**恰是 R6 change set，无越界文件**。
- **非回归（§9 门自检，本轮亲自守）**：`logic-protocol.md` / `milestone-schema.md` / `acceptance-schema.md` / `tech-plan-schema.md` / `verify-schema.md` / `prd-split.md` / `project-digest-schema.md` / `context-persistence.md` / hooks / `VERSION` **均不在 diff 中** → 非 PRD 流与 R1–R5 主体（契约结构 §3/切分算法/钉版字段/改版主流程 §2/§3/§5/§6）一行未动。
- **两 Coder 文件删除行审计**：全为 flip/heading/scope 的**整行替换**，无正文内容丢失（逐行比对 diff 确认）。
- **不越界**：认亲只扩 `prd-update §4`（新增 §4.1/§4.2 子节）；未做全自动认亲（一律"提候选 → 确认"）；未切版。

## 收官核对（MILE-0004）

- `MILESTONE.md §5.3` 路线图 R1–R6 **六项全部绑定实际 ITER**（R6 = ITER-0041，收口时补 ✅）。
- `references-schema §8` 前向指针表 R1–R6 **全绿**（R6 本轮 flip）。
- MILE-0004 六块（R1 契约基座 / R2 切分 / R3 首切入口 / R4 钉版 / R5 改版同步 / R6 认亲+非回归+收尾）**齐**，可收口里程碑 + 独立切版（发布动作、待放行、非本迭代）。

## 残余风险

- **无人测道残余**：全为规则文档，无运行时/视觉/外部通道验证项。
- **认亲启发式是"提候选"非"判定器"**：本轮只定"怎么提、怎么落、拿不准怎么退"，不追求配对算法精度——精度靠用户确认兜底，与"绝不自动认"一致，非缺陷。
- **端到端老项目 PRD 升级未实跑**：既有 dogfood 债（MILE-0004 §5.1 Out of Scope 已声明），另论。

## 结论（自评）

七条 AC 全绿，scope 守恒、非回归门本轮亲自守通过、MILE-0004 收官核对齐。**自评 PASS**，待独立复核确认后收口。

---

## 独立复核结论

**干净上下文子 agent、对抗式、验证者≠实现者、只读**。结论 **APPROVE-with-nits**——七条 AC 逐条核过：AC1/AC2 松边成文且 §2/§3/§5/§6 字节未动、AC3 非回归门本轮亲自守（门内文件 diff 全空）、AC4/AC5/AC6/AC7 均 PASS，slug 终身 / 松边不硬认 / scope 守恒 / 新增 §-锚点（§4.2、§9）全解析。整改：

- **Must Fix（已改）**：`MILESTONE.md §5.3` R6 行绑了 ITER-0041 但缺 ✅，与 AC7"R1–R6 全绿"收官核对冲突 → **收口仪式步 ⑤补 ✅**（本迭代收口时落定）。
- **Should Fix（已改）**：`Coder/README.md` prd-update 行"合并/拆分/改名留 R6"过时指针 → 已 flip 为"§4.2 松边、R6 落地"。属 R6"README 注册"收尾职责、README 非 §9 非回归门内文件，改动合规。
- **Nit（不改·合理保留）**：`prd-split.md §4/§25`、`references-schema §4` 的 R6/"R2–R6"是路线槽 / scope 排除的路由陈述（认亲仍是 R6 的活、已落 prd-update、"不在此"依旧准），非过时未办声明，保留。

整改后复评：Must Fix 由收口步 ⑤ 落定、Should Fix 已 flip，无遗留阻断。**准予收口。**
