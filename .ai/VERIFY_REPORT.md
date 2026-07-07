# Verification Summary

> 监督态自驱（非 `/dangerous`）：本迭代由用户"下一步继续"委托执行，P1–P3 自驱、AC ack-frozen；P5 起独立复核子 agent（fresh-context，验证者≠实现者）守质量。无 RUN_LOG 审计条（非无人值守）。

- ITER-0028（MILE-0003 R2）：把 `project-digest-schema.md` 从"`.ai/PROJECT.md` 单文件薄索引契约"整篇改写为"`.ai/project/` 知识文件夹契约"——§1 定位（知识地图 / 整体积分 / 四产物边界）+ §2 核心哲学（三条矛盾消解 + 最大风险）+ §3 结构 + `00_INDEX` 契约 + 推荐核心 topic 集 + §4 每份边界 + §5 digest-and-point 密度（含校准样例）+ §6 折叠维护模型（**只声明**、强制接线明标留 R3）+ §7 受控扩展登记 + §8 模板骨架 + §9 关系（R3/R5/R6/R8 前向指针）；并改准 `Coder/README.md` 描述行。
- 总体结论：**8/8 AC 通过**，可收口。全部为文档类 AC=读文件确认 + `git status` / grep 核守恒（`auto·可靠`，确定性可复现）。scope 守恒：diff 仅 2 规则文件（`project-digest-schema.md` 改写 + `README.md` 描述行）+ `.ai/` 台账；未 rename、未触 R3/R5/R6/R8 目标文件（iteration-schema / milestone-schema / context-persistence / mcv-deployment / migrations）、未改 `.ai/PROJECT.md` 结构。

# AC Status

- [x] AC1（auto·可靠）✓ §1 定义 `.ai/project/` 为"整体 / 积分取向、随迭代越补越全的知识地图"、明写取代旧单文件 `.ai/PROJECT.md`；四产物边界表保留（project/ vs ITERATIONS vs handoff vs MILESTONE）
- [x] AC2（auto·可靠）✓ §3「00_INDEX.md 契约」三块齐（一段话讲清项目 + 读序/地图 + 主题登记表每行含边界）+ 冷启动第一读 + "新建主题必须登记"承"注册即真源、无隐式依赖"老不变量
- [x] AC3（auto·可靠）✓ §3 推荐核心 topic 集七份（identity/architecture/capabilities/invariants/constraints/debt/frontier，标"推荐核心、可受控扩展"）；§4"有界、能一次整篇读完、满则拆新文件"+ 体积∝复杂度不∝迭代数
- [x] AC4（auto·可靠）✓ §5 digest-and-point 密度口径（名 + 它到底干什么 + 真源指针）+ 三种不合格写法（关键词占位 / 逐字复制 / 空泛套话）+ "已有真源不逐字抄" + architecture.md 密度校准样例
- [x] AC5（auto·可靠）✓ §2 三条矛盾消解齐（①完整=广度≠深度 地图≠疆域 ②完整≠变长·overwrite·禁历史层·删除不叠 ③知识地图≠harness机器正交）+ 点名最大风险"陈旧的完整比诚实的薄更毒"
- [x] AC6（auto·可靠）✓ §6 声明折叠模型（按主题路由 / overwrite / 成本∝改动量不∝文件夹大小）+ **明标**强制化+漂移自检"接线是 R3、本 schema 不实现"+ 兜底句"在 R3 接线前…不构成'要求了却没人强制'"——无伪强制假绿
- [x] AC7（auto·可靠）✓ §9 R3/R5/R6/R8 逐条标"后续路线项、本轮 R2 不实现"；`git status` 证明 iteration-schema / milestone-schema / context-persistence / mcv-deployment / migrations / `.ai/PROJECT.md` 均不在改动集
- [x] AC8（auto·可靠）✓ frontmatter audience/scope 反映文件夹、措辞必须/不得/应、中文说明英文标识符、§8 模板骨架含 00_INDEX + topic 骨架；`README.md` 描述行改准（知识文件夹契约）；`git status` 改动集=schema + README + `.ai/` 台账，无 rename、未改 PROJECT.md 结构

# Verification Results

- AC1–AC6：逐条读改写后 `project-digest-schema.md` 正文（§1–§9）确认要素齐全、与预研设计（`docs/research/MILE-0003-project-knowledge-folder.html` §4/§5/§7）保真、措辞到位。
- AC7：读 §9 关系段确认前向指针如实标"待 R3/R5/R6/R8"；`git status --short` 证明四目标文件 + migrations/ + PROJECT.md 未在改动集。
- AC8（守恒）：读 frontmatter + §8 模板骨架 + README 描述行；`git status --short` 文件集=2 规则文件 + `.ai/` 台账，无 rename（`git diff --summary` 无 rename 行）、未改 PROJECT.md 结构。

# Gate Coverage

- 通用质量门禁：本迭代为规则文档（非可执行代码），验证=读正文确认存在且自洽 + git/grep 核守恒（`auto·可靠`）；无 UI / 交互残余、无人测道残余（人测道小结整段省略，8 条全 `auto·可靠`）。
- Active Profiles：无（Markdown 规则仓，未命中 `10_Domain_Stack_Profiles/`），N/A。
- Tech Plan Alignment：DD1–DD6 全兑现——哲学切换独立成 §2（DD1）、折叠模型声明 + 强制留 R3（DD2）、文件不 rename（DD3）、前向指针不越位（DD4）、topic 集照预研定稿（DD5）、butler 自身暂态不一致如实说（DD6，§9 暂态说明）。无偏离。
- References Compliance：本轮无 `.ai/references/`，N/A。

# Independent Review

- 复核方式：fresh-context general-purpose 子 agent（agentId af0d1bca6e353d279，验证者≠实现者），逐 AC + 预研保真 + scope 边界 + 对抗探测 4 项（越界改 R3/R5/R6 文件 / 折叠模型伪强制 / 密度口径自相矛盾 / 历史层复活）。
- 逐 AC 裁决：**confirm 8/8**。
- 对抗探测：四类全 negative——①未越界（diff 不含 R3/R5/R6 目标文件、migrations 未创建）②未伪强制（§6 标题+正文+兜底句+§2 最大风险四处一致标"声明/待 R3 强制"、显式否定假象）③密度口径不矛盾（"越补越全=多 topic + 折进旧位置，非往后叠历史"与"禁历史层/不变长"正交共存、体积口径钉死）④历史层未复活（两处"禁历史层""删除不叠""历史归 ITERATIONS/deliveries"）。
- 结论：**APPROVE-WITH-NITS，0 Must Fix、0 false-green**。3 项 Nit 中前两项**已就地修**：跨目录引用前缀不一致（§引言 / §6 / §9 的 iteration-schema / milestone-schema / mcv-deployment 补 `20_Workflow_Lifecycle/` 前缀，同目录 handoff-spec 反向去前缀，context-persistence 同目录裸名正确保留）；`implementation-discipline.md` 锚点略偏（去 §4 改指整篇）。第三项（R6 指向尚不存在的 `migrations/`）系前向指向未来产物、合理，不改。

# Remaining Risks

- **陈旧的完整比诚实的薄更毒**（最大风险）：知识文件夹立志完整，若无严格维护会变"自信的谎"。本 schema 已声明折叠模型对冲，但**强制 + 漂移自检的机器接线在 R3**——R2 收口后到 R3 落地前，折叠仍靠"收口按需前滚"人工执行，属已知阶段性缺口（§6 兜底句已如实标注，非伪绿）。
- **暂态不一致**：butler 仓自身 `.ai/PROJECT.md` 仍是单文件，与新文件夹契约并存，R8 才 dogfood 适配；§9 暂态说明已定为"采用知识文件夹时的契约"，非矛盾。
- schema 靠"约定 + 收口自检"生效，butler 仓不 live 跑自己的 hook（既有设计约束），无机器手段强制文件夹落地；与仓内其它纪律同层，属已知设计约束。

# Handoff / Next Step

- 本迭代闭合，进原子收口五步（归档 / 交付 md+html / 翻台账 current=none + ITER-0028 行 closed / PROJECT 前滚现行约束 / 收口自检 5 不变量）。北极星=ITER-0028（MILE-0003 R2·知识文件夹 schema）达成。
- 归属 MILE-0003 R2；收口后 MILE-0003 仍 active，剩 R3–R8（强制折叠 R3 / 更新说明+查过时帮手 R4 / 读序切换 R5 / 部署迁移 R6 / 说人话 R7 / butler 自身 dogfood + 切版 v2.0.0 R8），待用户指令。本轮按惯例收口即提交（不推送、不切版，除非用户另示）。
