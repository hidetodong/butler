# ITER-0004 控制状态外化：ACK 冻结 + 入口分流可审计

## 本次交付目标
针对生命周期 review 暴露的两条结构性缺陷收口：D1——ACK/冻结是全流程锁范围的枢纽，却只活在对话里、hook 管不到、产物无字段记录；D4——入口分流（完整 vs 简化）全靠 AI 自评且不留记录，三档却只定义一个阈值、缺"简化→完整"升级转换。两者都违反系统"不依赖对话记忆、一切外化"的根本原则。

## 已完成内容
- **D1 ACK/冻结外化**：AC_LIST 顶部新增 `状态: draft | ack-frozen` + `ACK 日期` 字段；写完置 `draft`、用户 ACK 后置 `ack-frozen` 方可进 P3；迭代内 amend 须退回 `draft` 重新 ACK。`phase_gate` hook 扩展为：AC_LIST 处于 `draft` 时拦截源码写，无该字段的旧产物按 legacy 放行（向后兼容）。
- **D4 分流可审计 + 三档 + 升级**：`lifecycle §2` 重构为 升级信号 / 三档边界（极小·简化·完整，各有明确进入条件与产物要求）/ 一行分流记录（完整→CONCEPT、简化→AC_LIST、极小→口头）/ 低档→高档升级转换。
- 规则卡（SSOT）、logic-protocol、concept/acceptance schema、README 与 mcv-deployment 的 hook 描述同步。
- hook 新增测试覆盖 draft/frozen/legacy/未知值/英文 key 五种情形。

## 关键变更 / 使用者可感知变化
- 部署了 butler hook 的项目：AC_LIST 没被置 `ack-frozen` 之前，改源码会被机制拦截——"等 ACK"从口头纪律变成可校验状态。已部署的旧项目不受影响（无字段=legacy 放行）。
- 每个非极小任务现在要在产物顶部留一行分流记录，分流判定从隐形变为可审计。
- "极小任务"首次有了明确边界（单文件 / 纯文案 / 零契约 / 单轮闭合）。

## 高层影响范围
- 规则层：`Coder/20_Workflow_Lifecycle/{lifecycle,acceptance-schema,iteration-schema,concept-schema,mcv-deployment}.md`、`Coder/00_System_Prompt/logic-protocol.md`、`Coder/README.md`、`templates/rule-card.md`。
- hook 层：`templates/hooks/rules/phase_gate.py` + `templates/hooks/tests/{test_phase_gate,test_integration}.py`。
- 不涉及：里程碑机制、Domain/Stack Profiles、Composer/Learner。

## 验证方式与结果摘要
- 真实 `butler_gate.py` 子进程实测三态：draft→exit 2（phase_gate 拦截）、ack-frozen→exit 0、legacy→exit 0，均符合设计。
- `uv run --with pytest pytest` → 69 passed，新增用例通过、既有 legacy 用例不回归。
- 规则文件逐项 grep 交叉核对：章节重编号无重复、跨文件 `状态`/`ack-frozen` 引用一致。
- 详见 `.ai/iterations/ITER-0004/VERIFY_REPORT.md`。

## 已知剩余风险 / 延后事项
- 已知局限（如实标注、本轮不解决）：hook 只能校验"字段写了 frozen"，不能校验"人是否真的 ACK"；`/dangerous` 模式由模型自置 `ack-frozen`，属自校验。
- 简化路径 AC_LIST 的 `状态` 字段可选——有意取舍，避免轻量任务被 hook 拖累。
- review 另四条缺陷 D2 / D3 / D5 / D6 未动，留作后续迭代候选。

## 引用
- `.ai/iterations/ITER-0004/CONCEPT.md`
- `.ai/iterations/ITER-0004/AC_LIST.md`
- `.ai/iterations/ITER-0004/TECH_PLAN.md`
- `.ai/iterations/ITER-0004/VERIFY_REPORT.md`
