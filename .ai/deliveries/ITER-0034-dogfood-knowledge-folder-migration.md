# butler 自身 dogfood：单文件迁知识文件夹（.ai/project/）

> ITER-0034 段A · 迭代交付 · 收口 2026-07-08 · MILE-0003 R8（压轴·段A）· 监督态自驱（用户"继续 / 开始"接力，非 /dangerous；P5 起独立复核守质量）· 注：v2.0.0 切版为独立发布段（段B），切 tag 前另请用户放行

## 本次交付目标

- MILE-0003 前七轮（R1–R7）把知识文件夹的一整套规则——契约、维护回路、冷启动读序、部署种子、迁移配方、帮手名册、说人话——全给**别的项目**建好了，但 butler **自己**还在用旧的单文件 `.ai/PROJECT.md`（一份一千多字的薄索引）。规则从没在真实项目上验证过。
- R8 让 butler 拿自己当第一个真实用户（这就是"dogfood"，自己吃自己做的狗粮）：按 R2 契约把自身全貌产物迁成 `.ai/project/` 知识文件夹、对齐全仓"butler 还是单文件"的旧说法。**段A（本交付）只做迁移 + 对齐**；聚合切 v2.0.0、收口整个里程碑是随后的独立发布段（段B），切版不可逆、单独等用户放行。

## 已完成内容

- **建起 `.ai/project/` 知识文件夹（8 个文件）**：
  - `00_INDEX.md` 入口——一段话讲清 butler 是什么 + 冷启动读序地图（想知道 X 就读哪份）+ 7 主题登记表。
  - 7 个主题文件：`identity`（定位）/ `architecture`（三层模块地图）/ `capabilities`（现在能做的命令、SOP、工具）/ `invariants`（不能碰的长期决策）/ `constraints`（干活的硬边界）/ `debt`（欠债）/ `frontier`（当前在攻什么、下一个瓶颈）。
  - 旧单文件 6 段无遗漏迁入，并补上 R2 契约新增的两层——`capabilities`（旧薄索引根本没有的"现在到底能干什么"清单）和 `frontier`（变得最快的那层）。
- **删掉旧单文件 `.ai/PROJECT.md`**：内容已按主题拆走，这一步就是迁移配方里 `[split]`（把一份切成一个文件夹）动作作用在 butler 自己身上。
- **对齐现实（把"butler 还是单文件"的旧说法翻新）**：改了 3 处规则文件里拿 butler 自身当"单文件例子"的地方（部署协议 `mcv-deployment §2`、冷启动读序 `context-persistence §6`、知识文件夹契约 `project-digest-schema §9` 的路线状态），标明 butler 已转文件夹态。
- **红线守住**：两态规则（"用文件夹的项目这样读、还用单文件的项目那样读"）的**单文件分支逻辑一行没删**——R6 之前部署的老项目仍然是单文件，规则得继续支持它们；这次只是把 butler 自己从"单文件例子"里挪出来，不是砍掉单文件支持。

## 关键变更 / 用户可感知变化

- **butler 冷启动方式变了**：以后 AI 从零接手 butler 仓，第一读不再是那份薄索引，而是 `.ai/project/00_INDEX.md`——先拿地图，再按手头任务钻相关主题，不用一次性读完整个项目摘要。
- **知识文件夹设计第一次真实落地**：R2–R6 都是纸面规则，这次 butler 自己吃下去，验证了"AI 迁完能不能真读懂自己"。独立复核确认：从入口出发能定位到任一主题、指针不踩空。
- **butler 从此进入"漂移自检"范围**：迁成文件夹态后，一致性自检第 6 条（知识文件夹和真实代码有没有脱节）对 butler 自身开始生效，每次收口按主题折叠新变化。

## 高层影响范围

- 新增（`.ai/project/` 8 文件）：`00_INDEX` + 7 主题。
- 删除：`.ai/PROJECT.md`（迁走）。
- 改（3 个规则文件对齐 butler 自身现状，分支逻辑不动）：`mcv-deployment.md §2`、`context-persistence.md §6`、`project-digest-schema.md §9`；`.ai/task-state.md` 冷启动入口。
- 没碰（守边界）：两态规则的单文件分支逻辑、知识文件夹结构契约（R2）/ 折叠语义（R3）/ 读序逻辑（R5）/ 说人话定义（R7）、hook 代码、四件套字段结构、`Learner`/`Composer`、无任何改名；**VERSION / CHANGELOG / migrations 属发布段（段B），本段不碰**。

## 验证方式与结果摘要

- **段A 11 项验收（AC1–9、AC16–17）全过**，全 **auto·可靠**（规则 / 文档 / 台账：读产物核契约 + `git`/`grep` 核守恒 + dogfood 冷启动走查，确定性可复现）；无人测残余（纯文档、无运行时）。
- **独立复核 APPROVE、零 Must Fix**（另起干净上下文子 agent、验证者≠实现者、只读、对抗式挑毛病）：迁移无遗漏、`architecture` 只摘全貌不抄 README 目录树、单文件分支逻辑未误删、指针不踩空、`00_INDEX` 三块齐 + 登记表对账、说人话无裸奔黑话、scope 无越界。

## 已知剩余风险 / 延后事项

- **段B（v2.0.0 切版）待用户放行**：VERSION 1.7.0→2.0.0（大版本，因冷启动核心产物契约破坏性重构）+ CHANGELOG 聚合 + `migrations/v2.0.0.md` 配方实例 + 收口 MILE-0003 + `git tag v2.0.0`。tag 不可逆、对外发布锚点，单独等放行。
- **`/butler-upgrade` 仍未真跑**（既存欠债，见 `.ai/project/debt.md`）：本轮迁移就是段B `migrations/v2.0.0.md` 的 `[split]` 配方要覆盖的场景，但真实老项目端到端升级验证仍悬着。

## 引用（只引用路径，不嵌全文）

- 归档四件套 + 切片：`.ai/iterations/ITER-0034/CONCEPT.md` / `AC_LIST.md` / `TECH_PLAN.md` / `VERIFY_REPORT.md` / `CHANGELOG.md`
- 新增产物：`.ai/project/00_INDEX.md` + `identity/architecture/capabilities/invariants/constraints/debt/frontier.md`
- 对齐改动：`Coder/20_Workflow_Lifecycle/mcv-deployment.md §2`、`Coder/40_Context_Management/context-persistence.md §6`、`Coder/40_Context_Management/project-digest-schema.md §9`
- 相关契约：`project-digest-schema.md`（知识文件夹结构真源）、`migration-schema.md §4/§6`（`[split]` 配方形态）
