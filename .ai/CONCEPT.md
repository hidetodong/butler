> 分流: 完整 | 命中升级信号: 多文件改动、契约变更、跨模块影响、设计取舍 | 2026-07-05

# 一句话

butler 派出去干活的"帮手 AI"现在只有"复核"一个，它的说明还摊在 5 个文件里各写一遍。这一迭代给帮手立个"名册"——新建一个专门放帮手定义的目录，先把总述（帮手是什么 + 所有帮手通用的规矩）和"复核"这一个帮手的完整定义搭起来；同时把现在写在复核规则里、其实属于"所有帮手通用"的话，搬进总述当唯一出处，别处改成指过去。这是 MILE-0003 的第一步，也替后面两个新帮手和大知识文件夹探好"总述 + 分文件 + 登记"这套结构。

# Goal

- G1 新建帮手名册目录 `Coder/62_Extension_Agents/`，含总述 `overview.md`（帮手是什么 + 通用规矩 G1–G4 + 名册表 + 加载方式）与复核帮手完整定义 `independent-review.md`。
- G2 把所有帮手通用的规矩提炼进总述当唯一真源；`60_review`、`dangerous`、`verify-schema` 里原来各自写或引的地方，改成指向总述。
- G3 复核帮手"三拆"：`60_review` 里的内容按性质分家——共享审查流程留原地、通用规矩上提总述、复核专有契约进 `independent-review.md`，每处留清晰指针。
- G4 名册在 `Coder/README.md` 注册（目录结构 + 目录说明 + 是否进读取顺序）。

# Current Understanding

- 现状：真正的帮手只有"复核"（`/review`），其说明散在 5 个文件（logic-protocol / review-engine / verify-schema / local-constraints / dangerous）各写或引一遍。
- 帮手的落地方式已定（预研拍板）：帮手 = 一份中立定义资料，用时读它、临时起一个干净子 agent 执行，跟现在 `/review` 一模一样；不把帮手文件下发到每个项目。
- 三拆的搬家地址（预研 `MILE-0003-agent-doc-design.md §6` 给了带地址清单，已与 `review-engine.md` 现状核对一致）：
  - 留 `60_review`：§1 通用审计视角、§3 审查流程、§4 闭环、§5 简评。
  - 上提总述（通用规矩 G1/G2）：§1"独立性 = 上下文隔离"那段、§6.4 诚实性 fallback。
  - 进 `independent-review.md`（复核专有）：§2 两个独立复核触发、§3.3 断言核对、§6.1 隔离形态、§6.2 Checker 契约、§6.3 输出衔接。
- 一个防搬错的关键事实：G2"叫不起来就如实说"的**正文现在只在 `review-engine §6.4` 一处**，`dangerous §7.3`、`verify-schema §4` 是**引用它**、不是各写一遍。上提总述后，这两处引用目标改指总述，改完全仓核对没有漏网还指着 `review §6.4` 的引用。
- 预期产出：一个能用的帮手名册骨架（总述 + 复核定义），后续 R4 照它套"更新说明""查过时"另两个帮手。

# Constraints

- 落点 `Coder/62_Extension_Agents/`（顶层扩展簇，挨着 60_review）；**不放** `00_System_Prompt/`——那层是会话协作身份，名册是"能派哪些帮手"的能力目录，性质不同，混入会破坏分层。落点开题已定、本迭代最终坐实。
- 夹内文件**不带数字前缀**（`overview.md` 而非 `00_overview.md`）：`Coder/` 目录惯例是夹内零前缀、顺序交 README 排。
- 总述**触发式加载、不进冷启动必读**（与全体扩展模块一致）；主线用一行很轻的指针知道"有哪些帮手可用"即可，不占冷启动预算。
- 三拆写成**带地址的搬家清单**（哪段搬哪、原地留指针），不只口头说"互相引用"——butler 没有机器手段能发现两处内容写岔。
- 权限靠**约定 + 如实说**兜底，本迭代**不做**工具层硬拦（可选增强、留后续）。
- 不改帮手的对外行为，也不改 `/review` 现有触发方式与产出——只重新组织定义 + 立名册，复核功能等价。
- 顺手改准两处事实错（预研 §7）：`AGENTS.md` 起源（Sourcegraph 的 Amp 团队发起、非 OpenAI）、Agent Skills 采用数加时间点"截至 2026 上半年"。
- 遵守 butler 编辑规则（CLAUDE.md）：不破坏分层、新文件必须在 `Coder/README.md` 注册、frontmatter 标 audience/scope。

# Impact Scope

- 新增：`Coder/62_Extension_Agents/overview.md`、`Coder/62_Extension_Agents/independent-review.md`。
- 改 `Coder/60_Extension_CodeReview/review-engine.md`：三拆搬家 + 原地留指针。
- 改 `Coder/65_Extension_Dangerous/dangerous-engine.md §7.3`、`Coder/20_Workflow_Lifecycle/verify-schema.md §4`：G2 引用目标改指总述。
- 改 `Coder/README.md`：注册新目录（目录结构 + 目录说明 + 读取顺序判断）。
- 待核（P3 逐一确认）：`00_System_Prompt/logic-protocol.md`、`local-constraints-schema.md` 里是否有复核 / 独立性表述需回指总述。
- 明确不影响：P1–P5 状态机、四件套字段、迭代 / 里程碑机制、`/review` 的触发与产出行为、hook（butler 仓不跑 hook；本迭代也不碰 hook 模板）。

# Project Type / Active Profiles

- 项目形态：Markdown 规则仓库（butler 自身），非应用代码工程。
- 未命中任何 `10_Domain_Stack_Profiles/`；按通用 SOP + butler 自身编辑约束（CLAUDE.md）推进。

# Open Questions

- 总述那条"有哪些帮手可用"的轻指针，放 `Coder/README.md` 目录说明里就够，还是也要在冷启动读序提一句？（倾向只进 README 目录说明、不进冷启动必读——待 P2 定。）
- 三个帮手文件名定 `independent-review` / `knowledge-fold` / `drift-check`？本迭代只落 `independent-review`，另两个 R4 落；总述名册表要不要先把三个都列上（后两个标"R4 落地"占位）？（倾向先列全三个——待 P2 定。）
