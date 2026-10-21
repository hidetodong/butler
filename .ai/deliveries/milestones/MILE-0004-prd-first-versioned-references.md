# PRD 先行 + references 版本化改版同步（MILE-0004）

> MILE-0004 · 里程碑交付（大版本）· 收口 2026-07-09 · 随 v2.1.0 发布（**MINOR·向后兼容能力新增**）· 含迭代 ITER-0036 / ITER-0037 / ITER-0038 / ITER-0039 / ITER-0040 / ITER-0041

## 本次交付目标

- 一条主线，补 butler 一直缺的**外部权威规格（典型即 PRD）全生命周期**能力。缺口有三层：① 参考资料区 `.ai/references/` 一直没享受 MILE-0003 给 `.ai/project/` 的"索引 + 渐进读"待遇，一份大 PRD 要么整份糊进上下文、要么靠对话记忆，细节（精确文案、校验规则）留不住；② 里程碑是**有损路线图**，扛不住组件级实现细节，PRD 一挂进来就被磨平；③ PRD 天然按"修改项"迭代改版（V1.1→V1.2），却没有任何**改版同步协议**——一改版，切片/引用/已冻结的验收工作全无章可循。
- 大版本目标：把 PRD 先行做成**一等入口**，让一份 PRD 从导入 → 切片 → 挂里程碑 → 钉版 → 实现验收 → 改版同步全链路可走，且三条命门成立——**细节逐字保真**（切片是原文镜像不是摘要）、**跨改版可审计**（旧版冻快照、AC 钉版可回溯）、**已冻结/已收口工作不被静默破坏**（改版影响面亮牌不自动改）。因全部是新增能力（新 schema / 新命令 / 新模块 / 可选字段），且**不动任何既有非 PRD 流**（非回归门显式保证），按 semver 属 **MINOR**，收口切 **v2.1.0**。

## 已完成内容

- 六个路线项（R1~R6）一条主线闭环，逐项见下方回填表。链路顺序：**契约地基（R1）→ 首切动作（R2）→ 挂进里程碑入口（R3）→ AC 钉版接进 P2/P3/P5（R4）→ 改版同步协议（R5）→ 认亲边缘 + 非回归门 + 收尾（R6）**。全程"几乎复用既有仪式"（`/milestone` 录入、`ack-frozen` + amend 重冻、closed 不可改 + 变更开新迭代、收口快照），真新增只在切分机制 / 模块登记表 / `prd_version` 字段 / `/prd` 命令族 / 变更检测 + 影响面 / `.archive/vN/` 快照——无平行机器。

## 关键变更 / 用户可感知变化

- **`.ai/references/` 升级为支持知识文件夹态**（R1）：`prd/` 索引（`00_INDEX` 入口 + **模块登记表** slug↔标题/章节↔首见/当前版本↔状态）+ digest-and-point 渐进读 + `live` 目录 / `.archive/vN/` 版本落盘。硬区分：**索引可摘要、PRD 切片必逐字原文**（命门红线，禁套用 `.ai/project/` 的有损 overwrite 语义）。
- **大 PRD 切成无损切片**（R2）：`prd-split.md` 按 PRD 自身语义/模块边界切 `prd/<slug>.md`，**绝不切碎一条完整规则**、逐字保真、每模块发终身 slug（换版不换身份）、小 PRD 走单模块退化态、soft 对齐（提议→确认→落盘）。
- **首切随 `/milestone` 并进**（R3）：里程碑录入认出"brief 是大 PRD"就触发切分——一份输入同时喂**方向层路线图**和**细节层切片**，路线项 ↔ 模块 slug 双向交叉指针，焊上里程碑→references 的源指针缺口。
- **AC 钉版 `prd_version`**（R4）：验收清单 frontmatter 加可选字段，冻结那刻绑定 PRD 全局版本、之后钉住；P3 继承、P5 **对钉住版核而非 live 最新**（回溯读 `.archive/vN/`）。跨改版审计从此有据。
- **`/prd update` 改版同步协议**（R5）：出新版走一套确定性流程——变更检测（**修改项清单优先 + 逐字 diff 兜底 + 对账，分歧必亮**）→ 重新派生受影响切片 → **先冻旧版全量快照再更新 live**（顺序不可颠倒）→ **三态影响面报告**（没开工/进行中/已收口，**亮牌不自动**，绝不静默动已冻结工作）→ 受影响活路由（进行中 amend 重冻 / 已收口开新迭代 / 没开工无动作）。外加 `/prd status` 只读看板。
- **跨版认亲 + 非回归门 + 收尾**（R6）：改版时模块**改名/合并/拆分**跨版本认亲（启发式提候选→用户确认、**绝不自动认**、改名保留旧 slug 只换门牌、拿不准退回"新增/消失"基础态、宁可不认也不误并）；**非回归门**把"不碰非 PRD 流"从散落各迭代的口头承诺固化成 `references-schema §9` 一条**可验证红线**（判据 = 非 PRD 流文件 `git diff` 为空）；HUMAN_GUIDE 补 PRD 先行用法节 + 全子系统说人话自检。
- **不用 PRD 的人完全无感**：整套是 opt-in 加层，对话驱动流 / `origin/` brief / 普通 references 注入 / 核心 P1–P5 状态机一字未改——非回归门本轮亲自守住。

## 高层影响范围

- 新增（3 份规则）：`Coder/40_Context_Management/references-schema.md`（R1 契约 + R6 §9 非回归门）、`prd-split.md`（R2 首切动作层）、`prd-update.md`（R5 改版同步动作层 + R6 §4.2 认亲松边）。
- 接线 / 扩展：`acceptance-schema`（`prd_version` 可选字段 + 绑定语义，R4）、`tech-plan-schema` / `verify-schema`（版本化引用继承 + 对钉住版核，R4）、`milestone-schema §6.4/§5.3`（大 PRD 并进分支 + 路线项↔slug 交叉指针，R3）、`logic-protocol` 注入表（大 PRD 走切分 / 改版走 `/prd update`）、`HUMAN_GUIDE §5`（PRD 先行用法节，R6）、`Coder/README`（注册三文件）。
- 未动（守非回归门）：对话驱动 / `origin/` brief / 扁平态 references 注入（`api-`/`design-`/`insight-`）/ 核心 P1–P5 产物链 / 里程碑非 PRD 合成 / `project-digest` / `context-persistence` / hook 体系 / 四件套必填字段结构（`prd_version` 是可选、非 PRD 迭代逐字不变）。
- 部署面模板（`rule-card` / `hooks` / `snippet` / `CLAUDE.md.template`）**零改动** → 老项目升级无结构迁移，见 `migrations/v2.1.0.md`。

## 拆分路线图回填

| 路线项 | 主题 | 实际 ITER | 状态 | 落点 |
|---|---|---|---|---|
| R1 | references 索引化基座（`prd/00_INDEX` 契约 + 模块登记表 + 读纪律 + 无损/有损硬区分 + 落盘契约） | ITER-0036 | ✅ closed | `deliveries/ITER-0036-references-index-schema.md` |
| R2 | PRD 切分机制（按边界切、逐字保真、slug 首切、小 PRD 退化、soft 对齐） | ITER-0037 | ✅ closed | `deliveries/ITER-0037-prd-split-mechanism.md` |
| R3 | 首切并进 `/milestone` + 两海拔交叉指针 | ITER-0038 | ✅ closed | `deliveries/ITER-0038-milestone-prd-entry.md` |
| R4 | AC 钉版 `prd_version` + P2/P3/P5 版本化引用接线 | ITER-0039 | ✅ closed | `deliveries/ITER-0039-ac-prd-version-pinning.md` |
| R5 | 改版同步 `/prd update`（变更检测 + 快照 + 三态影响面 + amend 重冻 + `/prd status`） | ITER-0040 | ✅ closed | `deliveries/ITER-0040-prd-update-revision-sync.md` |
| R6 | 登记表认亲边缘（松边）+ 非回归门 + 收尾（用法 / flip / 说人话 / dogfood） | ITER-0041 | ✅ closed | `deliveries/ITER-0041-recognition-edge-and-nonregression-gate.md` |

- 六路线项全部达成。执行顺序 R1 → R2 → R3 → R4 → R5 → R6（先立契约地基，再切分动作、挂里程碑入口、钉版接产物链、改版同步协议，末位收认亲边缘 + 非回归门 + 收尾收官）。全程单主线、无正交子项。

## 验证方式与结果摘要

- 六路线项其下迭代各自 P1–P5 闭环、各自收口交付（见上表链接），均经 P5 独立复核（干净上下文子 agent、验证者≠实现者、对抗式）：R4 APPROVE-with-nits→修 Should Fix、R5 APPROVE clean、R6 APPROVE-with-nits→修 Must/Should Fix，其余各轮通过。多轮专查悬空 §-锚点（承 ITER-0035/0039 教训）。
- 里程碑收口前确认拆分路线图 R1–R6 六项全 closed、`references-schema §8` 前向指针表 R1–R6 全绿、一致性自检 6 不变量全绿。
- **非回归门本轮亲自守**：MILE-0004 全程改动集限于 PRD 子系统 + 接线点 + 文档，非 PRD 流 / 核心 P1–P5 / 部署模板 `git diff` 为空，逐迭代核过。

## 已知剩余风险 / 延后事项

- **整条链从未真跑**：R1–R6 全靠执行遵从守，命门红线（切片逐字无损、绝不切碎、映射/版本单一真源、亮牌不自动改已冻结、松边不硬认、非回归门 git diff 为空）都还没在真实"拿一份大 PRD 开里程碑 + 改一次版"里实战检验——这是 R4 钉版回溯、R5 冻快照的首次兑付点，风险最高的一步待一次真实端到端使用兜底。
- **认亲是"提候选"非"判定器"**：改名/合并/拆分靠启发式候选 + 用户确认，不追求配对算法精度（极端诡异改法退回基础态）——精度靠人确认兜底，与"绝不自动认"一致。
- **三态影响面依赖引用如实标注**：影响面靠"迭代引用了变更切片 + 钉了 `prd_version`"来判，取决于 R4 钉版纪律的遵从；漏标则可能漏判。
- 说人话落规则层、可自检，但"输出真的更好懂"仍靠每次迭代照做 + 收口自检兜底（非机器可判真假的封闭项）。

## 引用

- 里程碑产物快照：`.ai/milestones/MILE-0004/MILESTONE.md`
- 其下迭代交付：见上方回填表 6 条 `deliveries/ITER-00NN-*.md`
- 发布：`CHANGELOG.md` [2.1.0]、`migrations/v2.1.0.md`、`.ai/ITERATIONS.md`、`.ai/MILESTONES.md`
