---
状态: ack-frozen
ACK 日期: 2026-07-06
迭代: ITER-0028
里程碑: MILE-0003 R2
---

> 监督态自驱：本迭代由用户"下一步继续"委托执行（非 `/dangerous`），P1–P3 自驱、不设自审门横幅、不写 RUN_LOG；P5 起独立复核子 agent 守质量（重点核对预研设计保真 + R2/R3/R5/R6/R8 scope 边界）；用户可随时叫停 / 回退（ITER-0028，2026-07-06）。

# Goal

- 把 `project-digest-schema.md` 从 `.ai/PROJECT.md` 单文件契约改写成 `.ai/project/` 知识文件夹契约：结构 + 00_INDEX 入口 + topic 集 + 每份边界 + 密度口径 + 折叠模型（声明）+ 受控扩展。目标细节见 `CONCEPT.md`，不重述。

# In Scope

- 整篇重写 `Coder/40_Context_Management/project-digest-schema.md` 为文件夹 schema。
- 定 `.ai/project/` 结构 + `00_INDEX.md` 入口契约 + 推荐核心 topic 集 + 每份边界 + 写作密度（digest-and-point）+ 折叠维护模型（声明）+ 受控扩展登记 + 模板骨架 + 与其他规则关系（含对 R3/R5/R6 的前向指针）。
- 钉哲学切换的三条矛盾消解。
- 更新 `Coder/README.md` 对本 schema 的描述行。

# Out of Scope

- 不改 `.ai/PROJECT.md`（butler 自身单文件，转换=R8）。
- 不改 `iteration-schema §5.5` / `milestone-schema §7.4`（强制折叠接线=R3）、`context-persistence §6`（读序切换=R5）、`mcv-deployment` / `migrations/`（部署种子+迁移=R6）。
- 不 rename schema 文件、不改 P1–P5 状态机 / 四件套字段 / hook / 迭代里程碑双层 / VERSION。
- 不做自动生成（本里程碑只定 schema + 手工折叠，自动化留后续）。

# Acceptance Checklist

- [ ] AC1（结构·文件夹契约）: 改写后 schema 定义 `.ai/project/` 知识文件夹——`00_INDEX.md` 入口 + 按主题分文件；§定位讲清它是"整体/积分取向、随迭代越补越全的知识地图"，替换旧的"单文件薄索引"定位；四产物边界表保留（project/ vs ITERATIONS vs handoff vs MILESTONE）。
- [ ] AC2（结构·INDEX 契约）: 定 `00_INDEX.md` 契约——冷启动第一读、一段话讲清项目是什么 + 文件夹读序/地图 + topic 登记表（每 topic 一行 + 边界）；新 topic 必须登记进 00_INDEX（承"注册即真源、无隐式依赖"老不变量）。
- [ ] AC3（结构·topic 集 + 边界）: 给出推荐核心 topic 集（照预研 §7：identity / architecture / capabilities / invariants / constraints / debt / frontier，标"推荐核心、可受控扩展"）；每份边界写明"有界、可整篇读完、满则拆新文件"；体积∝项目复杂度不∝迭代数。
- [ ] AC4（口径·密度 digest-and-point）: 写作密度口径写清——装消化过的真内容（每项 + 它到底干什么 + 真源），不是关键词占位、也不是复制代码/逐字抄已有真源（digest-and-point：已有真源只摘全貌 + 补现状/成熟度层 + 指针）；给一段密度校准样例。
- [ ] AC5（哲学·矛盾消解）: 明写三条消解——①完整=广度覆盖≠细节深度（地图≠疆域）②完整≠变长（overwrite 当前真相、禁历史层、被取代内容删除不叠）③知识地图（要完整）≠ harness 机器（要精简）正交；并点名最大风险"陈旧的完整比诚实的薄更毒"。
- [ ] AC6（维护·折叠模型声明 + 强制留 R3）: 声明折叠维护模型（收口时本迭代 delta 按主题路由折进对应文件、overwrite、成本∝改动量不∝文件夹大小）；**明确标注**强制化（泛化收口步为必做）+ 漂移自检不变量的**接线由后续路线项 R3 落**，本轮 schema 只声明模型、不改 iteration/milestone 收口步——不制造"要求了但没强制"的假象。
- [ ] AC7（边界·前向指针不越位）: schema §关系段用前向指针如实标注 R3（强制折叠 + 漂移自检）/ R5（冷启动读序切换 context-persistence §6）/ R6（部署种子 mcv-deployment + 迁移配方 migrations）/ R8（butler 自身适配）为"后续路线项待接线"，本轮不实现；`git diff` 证明未改这些文件。
- [ ] AC8（质量·合规 + 守恒 + 注册）: frontmatter audience/scope 更新反映文件夹；措辞必须/不得/应、中文说明英文标识符；模板骨架含 00_INDEX + 一个 topic 骨架、H1/H2 规则明确；`Coder/README.md` 描述行改准（文件夹契约）；`git status` 证明改动集=schema + README（+ .ai 台账），未触 R3/R5/R6/R8 文件、未 rename、未改 .ai/PROJECT.md 结构。

# Verification Method

- AC1–AC6: 逐条读改写后 `project-digest-schema.md` 正文确认要素齐全、与预研设计（`docs/research/MILE-0003-project-knowledge-folder.html` §4/§5/§7）保真、措辞到位。
- AC7: 读 schema §关系段确认前向指针如实（标"待 R3/R5/R6/R8"）；`git status --short` 证明 iteration-schema / milestone-schema / context-persistence / mcv-deployment / migrations / .ai/PROJECT.md 未在改动集。
- AC8: 读 frontmatter + 模板骨架 + README 描述行；`git status` 核文件集 = schema + README + .ai 台账，无 rename、无越界。
- 全程 P5 起独立复核（fresh-context 子 agent，验证者≠实现者）：逐 AC + 预研保真 + scope 边界 + 对抗探测（越界改 R3/R5 文件 / 折叠模型伪强制 / 密度口径自相矛盾 / 历史层复活）。

# Open Questions / Risks

- 风险：schema 声明折叠模型但强制在 R3——若表述含糊会读成"已强制"，AC6 专项标注 + 独立复核核。
- 风险：文件夹契约 vs butler 自身仍单文件 PROJECT.md 的暂态不一致——schema 定为"采用知识文件夹时的契约"、butler 自身 R8 适配，§关系段说清。
- 已定（承 CONCEPT 三默认）：topic 集照预研 §7；折叠模型只声明、强制留 R3；文件不 rename。
