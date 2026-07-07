# 项目知识文件夹 schema（薄索引 → 知识地图）

> ITER-0028 · 迭代交付（小版本）· 收口 2026-07-07 · MILE-0003 R2 · 监督态自驱（用户"下一步继续"委托，非 /dangerous；P5 起独立复核守质量）

## 本次交付目标

- 冷启动"整体"产物一直是 `.ai/PROJECT.md`——一份 ≤1500 tokens 的**薄索引**（几个关键词 + "细节看代码"），AI 读完并不真知道"项目里有什么"，容易沦为"报几个关键词假装体系有用"。MILE-0003 R2 把它的格式契约 `project-digest-schema.md` 整篇改写为 `.ai/project/` **知识文件夹**契约：AI 读完就真懂项目、且随迭代越补越全。
- R2 边界：**只定 schema 文档**。强制折叠接线 / 冷启动读序切换 / 部署迁移 / butler 自身适配都是后续路线项（R3/R5/R6/R8），本轮用前向指针标注、不实现。

## 已完成内容

- **整篇改写 `Coder/40_Context_Management/project-digest-schema.md`**（单文件薄索引契约 → 知识文件夹契约，文件名不改以免破坏全仓 5+ 处引用）：
  - **§1 定位**：`.ai/project/` = 按主题分文件的常驻知识地图、整体/积分取向、冷启动第一读 `00_INDEX`；保留四产物边界表（project/ vs ITERATIONS vs handoff vs MILESTONE）。
  - **§2 核心哲学**：钉三条**矛盾消解**——①完整=广度覆盖≠细节深度（地图≠疆域）②完整≠变长（overwrite 当前真相、禁历史层、被取代内容删除不叠）③知识地图（要完整）≠ harness 机器（要精简）正交；点名**最大风险**"陈旧的完整比诚实的薄更毒"。
  - **§3 结构 + `00_INDEX` 契约 + 推荐核心 topic 集**：`00_INDEX`（一段话讲清项目 + 读序/地图 + 主题登记表）+ 七份推荐核心主题（identity/architecture/capabilities/invariants/constraints/debt/frontier，可受控扩展）。
  - **§4 每份边界**：有界、能一次整篇读完、满则拆新文件；体积∝项目复杂度、不∝迭代数。
  - **§5 写作密度 digest-and-point**：名 + 它到底干什么 + 真源指针；已有真源不逐字抄（只摘全貌 + 补现状/成熟度 + 指针）；配 architecture.md 校准样例。
  - **§6 折叠维护模型**：声明"收口时本迭代 delta 按主题路由折进对应文件、overwrite、成本∝改动量"；**明确标注**强制化 + 漂移自检的接线由 **R3** 落、本 schema 只声明不实现——不制造"要求了却没强制"的假象。
  - **§7 受控扩展登记** + **§8 模板骨架**（00_INDEX + topic 骨架）+ **§9 关系**（R3/R5/R6/R8 前向指针）。
- **改准 `Coder/README.md`** 对本 schema 的分文件描述行（单文件 → 知识文件夹契约）。

## 关键变更 / 用户可感知变化

- 冷启动"整体"产物的**目标形态**从"薄索引"翻转为"随迭代越补越全、读完真懂的知识地图"——这是一次有意的哲学切换（反转旧的 ≤1500t / 指针化 / 按需微调三条价值），换"真能用"、代价是更高维护纪律。
- 用户现在能看到一份**可照着建知识文件夹的契约**：建哪些主题文件、`00_INDEX` 写什么、每份写多满、密度什么标准、收口怎么折叠。
- **但本轮只是 schema**：真正让文件夹落地并保持不腐的强制折叠（R3）、冷启动改读它（R5）、部署/迁移带上它（R6）、butler 自己用起来（R8）都还没接线——已用前向指针如实标注。
- 向后兼容：`.ai/PROJECT.md` 自身仍是单文件（R8 才适配），schema 定为"项目采用知识文件夹时的契约"，暂态并存、非矛盾；未动状态机 / 四件套 schema / hook / 迭代里程碑双层 / `VERSION`；文件未 rename。

## 高层影响范围

- 改（整篇）：`Coder/40_Context_Management/project-digest-schema.md`。
- 改（描述行）：`Coder/README.md`（分文件说明 project-digest-schema 一行）。
- 收口前滚：`.ai/PROJECT.md` 关键长期决策与不变量加"知识文件夹产物契约升级"一条。
- 没碰（R2 边界）：`iteration-schema.md §5.5` / `milestone-schema.md §7.4`（强制折叠=R3）、`context-persistence.md §6`（读序切换=R5）、`mcv-deployment.md` / `migrations/`（部署种子+迁移=R6）、`.ai/PROJECT.md` 结构（butler 自身适配=R8）；P1–P5 状态机 / 四件套 schema / hook / 桥代码 / `VERSION` / 根 `CHANGELOG.md`。

## 验证方式与结果摘要

- **8/8 AC 通过**，全 **auto·可靠**（规则文档：读正文确认 + `git status` / grep 核守恒，确定性可复现）；无人测道残余。
- P5 **独立复核**（fresh-context 子 agent，验证者≠实现者）：逐 AC **8 confirm**、预研保真核对、对抗探测 4 项（越界改 R3/R5/R6 文件 / 折叠模型伪强制 / 密度口径自相矛盾 / 历史层复活）全 negative——**APPROVE-WITH-NITS，0 Must Fix、0 false-green**。
- Nit **已就地修**：跨目录引用前缀不一致（iteration-schema / milestone-schema / mcv-deployment 补 `20_Workflow_Lifecycle/` 前缀，同目录 handoff-spec 反向去前缀、context-persistence 裸名保留）；`implementation-discipline` 锚点去 §4 改指整篇。
- 守恒核对：`git status` 改动集=2 规则文件（schema + README）+ `.ai/` 台账，无 rename、未触 R3/R5/R6/R8 目标文件与 `.ai/PROJECT.md` 结构。

## 已知剩余风险 / 延后事项

- **陈旧的完整比诚实的薄更毒**（最大风险）：schema 已声明折叠模型对冲，但**机器强制 + 漂移自检在 R3**——R2 收口到 R3 落地前，折叠靠人工"收口按需前滚"，属已知阶段性缺口（§6 已如实标注，非伪绿）。
- butler 自身 `.ai/PROJECT.md` 仍单文件、R8 才 dogfood，暂态并存。
- 本轮按惯例收口即提交，**未推送、未切版**；MILE-0003 仍 active，剩 R3–R8（v2.0.0 切版在 R8），待用户指令。

## 引用（只引用路径，不嵌全文）

- 归档四件套 + 切片：`.ai/iterations/ITER-0028/CONCEPT.md` / `AC_LIST.md` / `TECH_PLAN.md` / `VERIFY_REPORT.md` / `CHANGELOG.md`
- 改动：`Coder/40_Context_Management/project-digest-schema.md`、`Coder/README.md`
- 设计基准（预研，未追踪）：`docs/research/MILE-0003-project-knowledge-folder.html`（§4/§5/§7）
