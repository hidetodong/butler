# 吸纳最小实现纪律（反过度工程写码底线）

> ITER-0027 · 迭代交付（小版本）· 收口 2026-07-06 · 独立迭代（不归属 MILE-0003）· 监督态自驱（用户"帮我吸纳进来"委托，非 /dangerous；P5 起独立复核守质量）

## 本次交付目标

- butler 一直只零散提过"少写代码、别过度工程"（rule-card"先复用再新增、先最小改动"、maintenance-boundaries"防过度工程"），却没有一条给 P4 写实现时照着爬的**操作纪律**。这一迭代把外部 `ponytail` 技能里三样能落地的写码反射，用 butler 自己的话吸纳成一条常驻规则。
- 只吸内容、不绑品牌：新文件用 butler 语气（必须 / 不得 / 应）重写，不出现 "ponytail" 字样、不照抄英文。

## 已完成内容

- **新建 `Coder/30_Quality_Gate/implementation-discipline.md`**（P4 常驻写码底线，与 `correction-contract.md` 并列）：
  - **§2 最小实现阶梯**：需要存在吗(YAGNI)→本仓已有吗(复用)→标准库→平台原生→已装依赖→一行→才轮到最小新代码，停在第一个成立的档；且"理解在前、爬阶梯在后"。
  - **§3 有意简化标记**：用可 grep 的 `butler-min:` 注释标明"这是有意简化"，正文必须含**已知天花板 + 升级路径**（配 JS/Python 示例）。
  - **§4 修根因不修症状**：动手前 grep 全部 caller、守卫放共享函数一处（diff 更小且不漏兄弟调用点）。
  - **§5 何时不许偷懒**：信任边界校验 / 防丢数据 / 安全 / 无障碍 / 用户明确要求不得砍；且绝不对"理解问题"偷懒。
- **单源收口**：`rule-card.md` 执行纪律加一条压缩纪律（指过去、不重抄全文）；`correction-contract.md §3` 加一行互引；`Coder/README.md` 三处注册（目录树 + 目录说明 + 分文件说明）。

## 关键变更 / 用户可感知变化

- P4 执行现在有一条**可照着爬的最小实现纪律**：写新码先爬阶梯少写、有意简化要留天花板+升级路径、修 bug 挖根因。以后 AI 在任何部署了 butler 的项目里写代码，都默认吃这条约束（随 rule-card 内联进 CLAUDE.md）。
- 与既有规则**并列不重叠**：纠错契约管"修到真过 / 诚实停"，本纪律管"写新码少写、修 bug 定位根因"，两者已双向互引。
- 向后兼容：纯新增 + 增量追加，未动状态机 / 四件套 schema / AC 脊柱 / hook / 迭代里程碑双层 / `VERSION`；既有条目无 renumber。

## 高层影响范围

- 新增：`Coder/30_Quality_Gate/implementation-discipline.md`。
- 改（章节级）：`templates/rule-card.md`（执行纪律加一条）、`Coder/30_Quality_Gate/correction-contract.md §3`（加一行互引）、`Coder/README.md`（三处注册）。
- 收口前滚：`.ai/PROJECT.md` 现行约束加"最小实现纪律"一条。
- 没碰：P1–P5 状态机、四件套 schema、AC 脊柱、hook、桥代码、迭代/里程碑双层、`VERSION` / 根 `CHANGELOG.md`、其它 30_Quality_Gate 文件正文。

## 验证方式与结果摘要

- **8/8 AC 通过**，全 **auto·可靠**（规则文档：读正文确认 + `git status` / grep 核守恒，确定性可复现）；无人测道残余。
- P5 **独立复核**（fresh-context 子 agent，验证者≠实现者）：逐 AC **8 confirm**、对抗探测 5 项（职责重叠 / 假绿 / 越界 / 分层 / 可读性）全过——**可收口，0 Must Fix、1 Should Fix、0 Nit**。
- Should Fix **已就地修**：§6 三处跨目录引用补 `20_Workflow_Lifecycle/` 前缀（与姊妹文件 testing-strategy.md 约定对齐；同目录裸名未动）。
- 守恒核对：`git status` 改动集=4 规则文件 + `.ai/` 台账，无计划外文件；新文件 grep `ponytail` 0 命中。

## 已知剩余风险 / 延后事项

- 素材源 `ponytail` 是外部技能、非 butler 契约；本迭代有意只吸内容 + 品牌解耦，未来该技能演进与 butler 无绑定（非风险）。
- 本纪律靠"约定 + 收口自检"生效，butler 仓不 live 跑自己的 hook（既有设计约束），无机器手段强制 `butler-min:` 标记——与仓内其它纪律同层。
- 本轮按惯例收口即提交，**未推送、未切版**；独立迭代不牵动 MILE-0003（仍 active、R2+ 待指令）。

## 引用（只引用路径，不嵌全文）

- 归档四件套 + 切片：`.ai/iterations/ITER-0027/CONCEPT.md` / `AC_LIST.md` / `TECH_PLAN.md` / `VERIFY_REPORT.md` / `CHANGELOG.md`
- 改动：`Coder/30_Quality_Gate/implementation-discipline.md`、`templates/rule-card.md`、`Coder/30_Quality_Gate/correction-contract.md`（§3）、`Coder/README.md`
- 素材源（外部、仅内容参考）：`ponytail` 技能 `skills/ponytail/SKILL.md`
