# VERIFY_REPORT — ITER-0038（MILE-0004 R3 · 首切入口并进 /milestone + 两海拔交叉指针）

> 监督态自驱。全为规则文档接线（改 3 份 + flip 1 指针，无新文件）。验证 = 读改后正文核契约 + `git diff` 核非回归 + `git status` 核守恒，确定性可复现（**auto·可靠**）· 无人测道残余。

## 验收结果（逐 AC · auto·可靠）

- [x] **AC1 ✓** `milestone-schema §6.4` 合成协议新增**步 6"大 PRD 并进分支"**——brief/`origin/` 材料判为大 PRD（判据**回指 `references-schema §2`**）时额外触发 `prd-split.md` 切成 `references/prd/`；切分机制"以 prd-split 为准、此处不复述"显式成文；"非大 PRD 到步 5 即止、不进本步"写死。现有五步字面**零改动**（`git diff` 无删除行佐证）。
- [x] **AC2 ✓** `§6.4 brief 定位`补一条——大 PRD **同时喂两个海拔**（brief→路线图有损 / prd-split→references/prd 无损）；`origin/` 那份是**非权威原始输入**（AI 只读不归档可清理）vs `references/prd/` 是**权威投影**（供 P2/P3/P5 对账、跨迭代常驻），身份区分回指 `references-schema §1`。
- [x] **AC3 ✓** 步 6 显式"**两次 soft 对齐合并成一次**"——步 5 路线图方向对齐 + prd-split §6 切分方案提议**并作一次呈交**，"不让用户分两轮点"成文。
- [x] **AC4 ✓（方向→细节）** `§5.3` 拆分路线图新增**可选「相关 slug」标注**（路线项主题后标 `→ prd: <slug>`，下钻 `references/prd/<slug>.md`）；标为"PRD 派生里程碑专用、非 PRD 无需"；显式声明"模块↔路线项映射以此处为**单一真源**"。
- [x] **AC5 ✓（细节→方向）** `prd-split §3` 补 blockquote——`/milestone` 触发首切时 `00_INDEX` 入口叙述记**所属里程碑号**（"本 PRD 服务 MILE-NNNN，映射见其 §5.3"），**只回指不重列映射**（真源单一在路线图）；手动注入无此句。
- [x] **AC6 ✓** `references-schema §8` R3 前向指针 flip 为"**✅ 已由 `milestone-schema §6.4/§5.3` 落地**"。
- [x] **AC7 ✓（守恒 + 非回归 + 分层）** 源改动集 = `milestone-schema.md` + `prd-split.md §3` + `references-schema.md §8` + `README.md`（末者为复核挑出的 flip 连带指针同步、非范围蔓延，见独立复核）。**非回归红线**：`git diff milestone-schema` 无任何删除行——非 PRD brief 五步合成路径字面逐字不变、分支纯增量 opt-in。**不做** `prd_version` 钉版(R4)/`/prd update` 同步(R5)/认亲(R6)；**不改** R2 注入表手动入口/`prd-split` 切分算法(§2/§4/§6)/`references-schema` 登记表字段(§3 未加列)/`project-digest`/`context-persistence`/hook/`VERSION`；**不切版**。改动仍在 SOP Core（`20`/`40`），未破坏分层。
- [x] **AC8 ✓（dogfood·说人话）** "一份输入喂两个海拔"（§6.4 步6 括注"方向层路线图 + 细节层切片"）/ 所属里程碑（改用中文、去裸英文 owning，配"这份 PRD 归哪个里程碑"释义）/ 交叉指针（"下钻""回指"方向说明）均首现带解释；无裸英文/变量残留。

## 独立复核

- **执行**：干净上下文子 agent，验证者≠实现者、只读、对抗式；四对抗点（分支真不动主干/非回归 · 触发引用不复述 · 交叉映射单一真源不双写 · 不越界做 R4–R6）逐点核。
- **结论**：**APPROVE-with-nits**。四对抗点全过——① `git diff` 证 milestone-schema 纯增量（7 行新增、零删除），五步字面未动、普通 brief 隔离；② 步 6 只触发不抄算法、判据回指 §2（目标真实存在）；③ 映射单一真源在 §5.3，prd-split §3 只回指不重列、两侧"谁是真源"声明一致；④ R4/R5/R6 的 §8 指针未 flip、切分算法未动、登记表未加字段、logic-protocol R2 行 diff 为空、未切版。交叉引用全自洽。Must Fix 无。
- **Should Fix 处置（已修）**：复核挑出 `README.md` prd-split 描述（原写"/milestone 并进入口…属 R3–R5"）未随本轮 R3 落地更新——是 flip 引入的可发现漂移。已改为"手动注入(R2) + /milestone 并进入口(R3 已落地，指 milestone-schema §6.4 步 6) / 钉版·改版同步属 R4–R5"，与 §8 flip 同源对齐。**README 因此纳入本轮改动集**（scope 从 3 文件 → 4 文件，属落地必然的指针同步、非范围蔓延）。
- **Nit（未改）**：示例 slug 不统一（`signal-list` vs `signal-save`），纯观感、不影响正确性，本轮不动。

## Remaining Risks

- R3 只接了 `/milestone` 这一入口的"并进"，"一份输入喂两个海拔"闭环成型；但**钉版（R4）未接**——切出的 slug 尚不能被 AC frontmatter `prd_version` 锚定引用，故"里程碑→切片"指针目前指向的是 live 最新、未版本化。
- 交叉映射"单一真源在路线图"靠规则约束——真到 R4/R5 版本化后，路线项 slug 标注与 `00_INDEX` 回指是否始终一致，取决于执行遵从（同既有回指不复述信任模型）。
