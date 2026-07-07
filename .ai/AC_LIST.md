---
状态: ack-frozen
ACK 日期: 2026-07-06
迭代: ITER-0027
里程碑: 无（独立迭代）
---

> 监督态自驱：本迭代由用户"帮我吸纳进来"委托执行（非 `/dangerous` 无人值守），P1–P3 自驱、不设自审门横幅、不写 RUN_LOG；P5 起独立复核子 agent 守质量；用户可随时叫停 / 回退（ITER-0027，2026-07-06）。

# Goal

- 新建 `Coder/30_Quality_Gate/implementation-discipline.md`（P4 最小实现纪律），收进最小实现阶梯 + 有意简化标记 + 修根因，钉"何时不许偷懒"边界，并单源收口（rule-card 压缩条 + correction-contract 互引 + README 注册）。目标细节见 `CONCEPT.md`，不重述。

# In Scope

- 新建 `implementation-discipline.md`：定位 + 最小实现阶梯 + 有意简化标记约定 + 修根因不修症状 + 不许偷懒边界 + 与其他规则关系。
- `rule-card.md` 执行纪律段加一条压缩纪律（指向新文件、不重抄阶梯全文）。
- `correction-contract.md §3` 加一行互引指针。
- `Coder/README.md` 三处注册新文件（目录树 + 目录说明 + 分文件说明）。

# Out of Scope

- 不动 `maintenance-boundaries.md`（维护文件更新边界）、`tech-plan-schema §71`（任务粒度）——各守其位，只呼应不搬。
- 不把 correction-contract 的"修到真过 / 诚实停"搬进新文件（那是纠错底线、留原地）。
- 不改 P1–P5 状态机 / 四件套字段 / 迭代·里程碑机制 / hook / 桥代码。
- 不切版、不归属 MILE-0003。

# Acceptance Checklist

- [ ] AC1（功能·阶梯）: `implementation-discipline.md` 存在且含"最小实现阶梯"——需要存在吗(YAGNI)→本仓已有吗(复用)→标准库→平台原生→已装依赖→一行→才轮到最小新代码，明确"停在第一个成立的档"且"理解在前、爬阶梯在后"。
- [ ] AC2（功能·简化标记）: 含"有意简化标记"约定——用可 grep 的注释标明"这是有意简化"，且必须写清已知天花板 + 升级路径；给出标记词（`butler-min:`）与至少两语言（JS `//` / Python `#`）示例。
- [ ] AC3（功能·修根因）: 含"修 bug 挖根因不打症状补丁"——动手前 grep 全部 caller、守卫放共享函数一处（比每个 caller 各补 diff 更小且不漏兄弟调用点）、不得只补工单点名的那条路径。
- [ ] AC4（边界·不许偷懒）: 含"何时不许偷懒"清单——信任边界输入校验 / 防丢数据的错误处理 / 安全 / 无障碍基线 / 用户明确要求，均不得简化掉；并明确"绝不对理解问题偷懒（阶梯只缩短解决方案、不缩短读代码）"。
- [ ] AC5（质量·分层合规）: 文件落 `30_Quality_Gate/`、frontmatter 标 audience/scope、措辞用必须/不得/应（中文说明、标识符英文）；不破坏三层分工；§关系段点明与 correction-contract / maintenance-boundaries / tech-plan §71 职责边界（并列不重叠）。
- [ ] AC6（结构·注册）: `Coder/README.md` 目录结构树 + 目录说明（30_Quality_Gate 那段）+ 分文件说明三处均登记 `implementation-discipline.md`；冷启动读序处理明确（随 30_Quality_Gate 常规读、不单列必读）。
- [ ] AC7（结构·单源收口）: `rule-card.md` 执行纪律加一条压缩纪律（指向新文件、不重抄阶梯全文）；`correction-contract.md §3` 加一行互引指针；两处均增量追加、不 renumber、不与既有条目语义冲突。
- [ ] AC8（质量·守恒 + 解耦）: diff 仅限本迭代 4 文件（新建 1 + 改 rule-card / correction-contract / README）+ 收口产物；未改状态机 / 四件套字段 / hook / 桥代码 / 其它无关规则；新文件用 butler 自己的话表达、不出现 "ponytail" 品牌词、不照抄英文原文。

# Verification Method

- AC1–AC4: 读 `implementation-discipline.md` 正文逐条确认要素齐全、措辞到位（确定性可复现）。
- AC5: 读 frontmatter + 落点层级 + §关系段，对照 `CLAUDE.md` 三层约束与既有三文件职责。
- AC6/AC7: 读 README 三处 + rule-card + correction-contract；grep 新文件名确认注册无遗漏、互引可解析。
- AC8: `git diff --stat` 核文件集；grep `ponytail` 确认新文件无品牌词；核对未触及 schema / hook / 桥。
- 全程 P5 起独立复核（fresh-context 子 agent，验证者≠实现者）逐 AC 核 + 对抗探测（越界 / 与既有规则重叠 / 假绿）。

# Open Questions / Risks

- 风险：新文件与 correction-contract / maintenance-boundaries 职责若切不净会重叠——AC5 专项核 + 独立复核 refute 兜底。
- 已定（承 CONCEPT 两默认）：标记词 `butler-min:`；新文件不进冷启动单列必读、随 30_Quality_Gate 常规读。
