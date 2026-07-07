# TECH_PLAN — ITER-0027（独立迭代）

> 监督态自驱（非 `/dangerous`）：本产物由用户"帮我吸纳进来"委托、模型自驱产出，P5 起独立复核守质量（ITER-0027，2026-07-06）。

# Goal

- 支撑 AC1–AC8：建 `implementation-discipline.md`（阶梯 + 简化标记 + 修根因 + 不许偷懒边界 + 关系）、单源收口（rule-card 压缩条 + correction-contract 互引 + README 注册）。

# Files / Modules to Change

**新增**

- `Coder/30_Quality_Gate/implementation-discipline.md` — frontmatter(audience/scope) + §1 定位（P4 常驻底线、与 correction-contract 并列）+ §2 最小实现阶梯（7 级 + 停在第一个成立的档 + 理解在前）+ §3 有意简化标记（`butler-min:` + 天花板/升级路径 + 双语言示例）+ §4 修根因不修症状（grep 全 caller / 守卫放共享函数一处）+ §5 何时不许偷懒（边界清单 + 不对理解偷懒）+ §6 与其他规则关系。→ AC1/AC2/AC3/AC4/AC5

**修改**

- `templates/rule-card.md` — 「执行纪律」段（`- 不混入无关变更` 一带）追加一条压缩纪律 bullet：最小实现阶梯一行 + 简化标记 + 修根因 + 不许偷懒边界，末尾 `（详见 implementation-discipline.md）`；不重抄阶梯全文。→ AC7
- `Coder/30_Quality_Gate/correction-contract.md` §3 — 追加一条 bullet：修根因 / 最小改动定位互引 `implementation-discipline.md`（增量、不 renumber）。→ AC7
- `Coder/README.md` — ①目录结构树 `/30_Quality_Gate` 块加 `implementation-discipline.md`；②目录说明 `30_Quality_Gate/` 那段（line 104 一带）补"+ 最小实现纪律"；③分文件说明（correction-contract 条 line 136 一带）加一条 implementation-discipline 说明。→ AC6

**收口前滚（close 步④）**

- `.ai/PROJECT.md` 现行约束 — 加"最小实现纪律"一条。→ 非 AC，收口仪式

# Interface / Contract

- **阶梯是反射不是研究项**：先理解问题与它触及的代码、走通真实流程，再爬阶梯；两级都成立取更高级、别纠结。
- **简化标记契约**：`butler-min:` 前缀注释 = 有意简化的信号，正文必须含"已知天花板 + 升级触发条件"两要素（例：`// butler-min: 全局锁，吞吐吃紧再拆按账户锁`）。
- **单一来源**：阶梯 / 标记 / 修根因全文只在 `implementation-discipline.md`；rule-card 与 correction-contract 只放压缩条 + 指针，不重抄。沿用 butler 文件名互引惯例、不写绝对路径。

# State / Boundary

- 落点 `Coder/30_Quality_Gate/`（与 correction-contract 平级的常驻质量门禁）；非扩展模块、无 `/命令` 触发。
- **不改**：P1–P5 状态机、四件套字段、迭代 / 里程碑机制、hook、桥代码、maintenance-boundaries、tech-plan-schema §71、其它 30_Quality_Gate 文件（linting / testing-strategy / review-standard 正文）。
- 独立迭代、不归属 MILE-0003、不进其路线图、不切版。

# Design Decisions

- **DD1（落点）**：进 `30_Quality_Gate/`（交付质量门禁），与 correction-contract 并列——写新码纪律 vs 纠错底线，性质相邻、职责不同。不进 `20_Workflow_Lifecycle`（那是流程状态机，非写码手法）。→ AC5
- **DD2（修根因同住不拆）**：修根因本质是"最小改动"论证（一处守卫 < 每 caller 各补），与阶梯同源，放 `implementation-discipline §4`；不搬进 correction-contract（避免与其"修到真过 / 诚实停"混层），correction-contract §3 只加一行互引保发现性。→ AC3/AC7
- **DD3（边界硬钉）**：`§5 何时不许偷懒` 与阶梯同等篇幅强调——信任边界校验 / 防丢数据 / 安全 / 无障碍 / 用户明确要求不得砍；"绝不对理解问题偷懒"单列，防止阶梯被误用为跳过读代码的借口。→ AC4
- **DD4（品牌解耦）**：只吸收内容、用 butler 语气重写，不出现 "ponytail"、不照抄英文；标记词自定 `butler-min:`（不沿用来源的 `ponytail:`）。→ AC8
- **DD5（压缩不重抄）**：rule-card 只放一条压缩纪律 + 指针（rule-card 是 ~800 token 卡、装不下阶梯全文），全文单源在新文件。→ AC7
- **DD6（不进冷启动必读）**：新文件随 `30_Quality_Gate/` 常规读序生效（P4 前读质量门禁），不单列冷启动必读——与 correction-contract 一致。→ AC6

# Execution Steps

- [ ] T1 写 `implementation-discipline.md`（§1–§6 全量）→ AC1/AC2/AC3/AC4/AC5
- [ ] T2 改 `rule-card.md` 执行纪律加压缩条（依赖 T1 定稿措辞）→ AC7
- [ ] T3 改 `correction-contract.md §3` 加互引 bullet（依赖 T1）→ AC7
- [ ] T4 注册 `Coder/README.md` 三处（目录树 + 目录说明 + 分文件说明）→ AC6
- [ ] T5 自检：读全文逐 AC 核 + `git diff --stat` 核文件集 + grep `ponytail`（新文件应 0 命中）+ grep 新文件名（注册无遗漏）→ AC8
- [ ] T6 P5 起独立复核子 agent（fresh-context，验证者≠实现者）→ 全 AC

# Verification Plan

- AC1–AC5: 读 `implementation-discipline.md` 正文逐条核要素 + frontmatter + 落点 + §关系边界。
- AC6/AC7: 读 README 三处 + rule-card + correction-contract；grep 文件名确认注册、互引可解析。
- AC8: `git diff --stat` 仅 4 文件（+ 收口产物）；grep `ponytail` 新文件 0 命中；核未触 schema/hook/桥。
- P5 独立复核逐 AC 裁决 + 对抗探测（越界 / 与既有规则职责重叠 / 假绿 / 品牌词残留）。

# Risks / Open Questions

- **职责重叠风险**：与 correction-contract / maintenance-boundaries / tech-plan §71 边界若切不净 → DD1/DD2 分层 + §关系段明述 + 独立复核 refute 兜底。
- **误当无脑砍码**：阶梯被误读为"能砍就砍" → DD3 边界段硬钉 + "理解在前"反射化解。
- 已定：标记词 `butler-min:`；新文件不进冷启动单列必读。
