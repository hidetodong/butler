> 分流: 完整 | 命中升级信号: 多文件改动、设计取舍 | 2026-07-06

# 一句话

butler 现在把"少写代码、别过度工程"的态度只零散提了两句（rule-card"先复用再新增、先最小改动"、maintenance-boundaries"防过度工程"），但没有一条给 P4 执行时用的、可照着爬的"最小实现"操作纪律。这一迭代新建一份 `implementation-discipline.md`，把三样能落地的写码反射收进来：**最小实现阶梯**（需要存在吗→本仓已有吗→标准库→平台原生→已装依赖→一行→才轮到最小新代码）、**有意简化的标记约定**（注释写明天花板 + 升级路径，让人读作意图而非疏忽）、**修 bug 挖根因不打症状补丁**；同时钉死"何时不许偷懒"的边界，防止被当成无脑砍代码的借口。素材取自外部 `ponytail` 技能，但用 butler 自己的话表达、不绑品牌。

# Goal

- G1 新建 `Coder/30_Quality_Gate/implementation-discipline.md`：P4 执行期的最小实现纪律，与 `correction-contract.md` 并列的常驻底线（无需触发、每次迭代生效）。
- G2 收进三样净新增内容：最小实现阶梯（7 级、停在第一个成立的档）、有意简化标记约定（天花板 + 升级路径）、修根因不修症状（grep 全 caller、守卫放共享函数一处）。
- G3 钉边界：信任边界校验 / 防丢数据的错误处理 / 安全 / 无障碍 / 用户明确要求不得简化掉；且绝不对"理解问题"偷懒。
- G4 单源收口：`rule-card.md` 执行纪律加压缩条指过去、`correction-contract.md` 加一行互引、`Coder/README.md` 注册新文件。

# Current Understanding

- butler 已有的相邻表述（不重复、只呼应）：`rule-card §角色`"先复用已有模式再新增、先最小改动再结构优化"（态度层）、`maintenance-boundaries`"防过度工程化"（针对 `.ai/` 维护文件的更新边界，不是写码纪律）、`tech-plan-schema §71`"任务粒度避免过度工程"（针对拆任务粒度）。三者都不是"写实现代码时怎么少写"的操作纪律——这正是空档。
- 素材来源 `ponytail`（外部技能）净新增三样已在会话里对账清楚：阶梯的中间几级（标准库→平台原生→已装依赖→一行，butler 只有首尾）、有意简化标记（butler 完全没有）、修根因 + grep 全 caller（correction-contract 只覆盖"修到真过 / 诚实停"，没讲"改哪一处最小且不漏兄弟调用点"）。
- 落点定 `30_Quality_Gate/`：它是"通用质量门禁"，最小实现纪律属于"交付质量"的一环，与同目录 `correction-contract`（纠错底线）性质并列——一个管"写新码时少写、写准"，一个管"修错时挖根因、不假绿"。
- 修根因归属：ponytail 把它放在"懒惰哲学"里（最小 diff = 一处守卫胜过每个 caller 各补），本质是**最小改动**论证，故与阶梯同住 `implementation-discipline.md`，不拆去 correction-contract；correction-contract 只加一行互引保发现性。
- 素材解耦：新文件用 butler 语气（必须 / 不得 / 应）重写，不出现 "ponytail" 品牌词，不照抄英文原文——只吸收内容。

# Constraints

- 遵守 butler 编辑规则（`CLAUDE.md`）：不破坏 SOP Core / Domain / Business 三层分工；新文件必须在 `Coder/README.md` 目录结构 + 说明注册（无隐式依赖）；frontmatter 标 audience / scope。
- 与既有规则**职责不重叠、只互引**：不动 maintenance-boundaries（维护文件边界）、不动 tech-plan-schema §71（任务粒度）、不把 correction-contract 的"修到真过 / 诚实停"搬过来——各守其位。
- 措辞面向 AI 执行：必须 / 不得 / 应；中文说明、标识符与文件名用英文；文件名互引不写绝对路径。
- 不改 P1–P5 状态机、四件套字段、迭代 / 里程碑机制、hook 模板、桥代码。
- **独立迭代**：内容与 MILE-0003（知识文件夹 / 帮手名册 / 说人话）主题正交，不归属该里程碑、不进其路线图，避免稀释里程碑范围（precedent：ITER-0020 独立）。

# Impact Scope

- 新增：`Coder/30_Quality_Gate/implementation-discipline.md`。
- 改 `templates/rule-card.md`：执行纪律段加一条压缩纪律（指向新文件，不重抄阶梯全文）。
- 改 `Coder/30_Quality_Gate/correction-contract.md §3`：加一行互引指针（修根因 / 最小改动定位 → 新文件）。
- 改 `Coder/README.md`：目录结构树 + 目录说明 + 分文件说明三处注册新文件。
- 收口前滚 `.ai/PROJECT.md 现行约束`：加"最小实现纪律"一条（close 步④）。
- 明确不影响：P1–P5 状态机、四件套 schema、迭代 / 里程碑台账机制、`/review`·`/loop`·`/dangerous` 等扩展、hook、桥代码、MILE-0003 路线图。

# Project Type / Active Profiles

- 项目形态：Markdown 规则仓库（butler 自身），非应用代码工程。
- 未命中任何 `10_Domain_Stack_Profiles/`；按通用 SOP + butler 自身编辑约束（`CLAUDE.md`）推进。

# Open Questions

- 有意简化的标记词定什么？（倾向 `butler-min:` 前缀注释——可 grep、绑 butler；项目可自定义一致 token。待 P2 定。）
- 新文件进不进冷启动读序？（倾向随 `30_Quality_Gate/` 常规读、不单列冷启动必读——与 correction-contract 一致。待 P2 定。）
