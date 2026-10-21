# 自动验证证据链与只读状态审计

> ITER-0057 · MILE-0007 R2 · 用户双 ACK · P5 完整审查 · 2026-07-18

## 本次交付目标

把“测试/复核通过”从模型口头结论升级为能打开、校验和重跑的机器记录，并让收口状态由只读审计器机械对账。

## 已完成内容

- 新增 verification evidence runner：按真实 argv 执行，记录 cwd、时间、exit、AC、有界 stdout/stderr、字节数和 SHA-256。
- 新增只读 verifier 与 hot/archive/reopen 单真源流程；失败、超时、截断同样留证，但只有 passed record 能覆盖绿色 AC。
- `VERIFY_REPORT` 强制 Evidence Index；复核统一分为 reported、captured、reproduced，风险抽样以 `review-*` record 留痕。
- 新增 state auditor：对账迭代/里程碑台账、交付/归档、证据、runtime 指针、fold receipt 和 Butler 发布元数据。
- 标准、危险模式、收口、交接、项目知识、README/HUMAN_GUIDE 与完整双宿主矩阵均已接线。

## 关键变更 / 用户可感知变化

今后完整路径里只写“已运行”“全部通过”不能再关闭自动道 AC；可以沿 Evidence Index 打开 record 和日志复核。第一次失败会保留为纠错轨迹，修复后以新 ID 重跑，不覆盖历史。收口时审计器会给对象级 `[DRIFT]`，活动规则仓则明确亮 `UNRELEASED`，不会混称已发布。

## 高层影响范围

- 驻留工具：`tools/verification-evidence/`。
- 状态审计：`scripts/audit-project-state.py` 及专项测试。
- 规则链：P5 testing/VERIFY/review、迭代/里程碑收口、context fold、dangerous 与交付规范。
- 人读入口：README、HUMAN_GUIDE、Coder 导航与规则卡。
- 未建设 CI required checks；跨 OS 持续验证仍属 MILE-0007 R3。

## 验证方式与结果摘要

- runner 11 项、auditor 11 项专项回归通过；P5 又重跑安全 3 项、归档 1 项、状态/证据漂移 3 项并生成 `review-*` 记录。
- 完整矩阵首跑因新增文档 grep 写错而失败，失败 record 如实保留；修复后新 ID 重跑通过：renderer 8、resolver 7、installer 16、runner 11、auditor 11、127 pytest、Codex R1/R2/hook wrapper 与 plugin validator 全绿。
- 所有 12 份 evidence record 经 archive verifier 校验通过；绿色 AC 均由 passed record 覆盖。
- 未执行 fresh-context 独立复核；本轮是主 agent 同上下文完整审查，不冒称独立。

## 已知剩余风险 / 延后事项

- SHA-256 是漂移检查，不是签名或远程证明；不能抵抗 record 与日志被一起恶意重写。
- timeout 进程组终止以 macOS/Linux 为主要目标；非 POSIX 跨平台矩阵留给 R3。
- fold receipt 只能证明路径/hash 已登记，项目知识语义仍需人工或 fresh-context 漂移抽查。

## 引用（只引用，不嵌入）

- `.ai/iterations/ITER-0057/AC_LIST.md`
- `.ai/iterations/ITER-0057/TECH_PLAN.md`
- `.ai/iterations/ITER-0057/VERIFY_REPORT.md`
- `.ai/iterations/ITER-0057/CHANGELOG.md`
- `.ai/iterations/ITER-0057/evidence/`
