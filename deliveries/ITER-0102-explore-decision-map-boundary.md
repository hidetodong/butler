# Explore / Decision Map 边界合同

## 本次交付目标

把 Wayfinder 式探索能力以 opt-in 方式接入 Butler，同时守住普通需求快路径和现有 P1→P5 交付纪律，避免模型自行判断需求大小或静默创建流程状态。

## 已完成内容

- 为 Standard lifecycle 增加统一的 suggest-only 边界：只有具体 blocker 才能建议 Explore，建议零写并等待用户同意。
- 把既有 Ideation 深化为唯一 Explore 真源；Decision Map 只记录已确认决定、开放问题和参考依据。
- 固定唯一交接：用户显式 promotion 后从 Iteration P1 开始，不再自动生成 `CONCEPT.md` 后直入 P2。
- 统一 Router、workflow registry、Claude/Codex 薄适配器及人读文档，并增加防回归合同测试。

## 关键变更 / 用户可感知变化

- 用户主动说“先脑暴 / 还没想清”时仍可直接进入 Ideation；普通任务不会因为模型觉得“可能复杂”而被自动拉进长流程。
- `/butler:ideation`、`$butler-ideation` 和 legacy `/ideation` 继续指向同一个 workflow，没有新增 `/explore` 或第二套算法。
- 探索完成但尚未 promotion 时不会占用 Iteration；进入交付后，Decision Map 降为理由、证据和历史参考，不覆盖 Milestone 或冻结 AC。

## 高层影响范围

影响 lifecycle、Ideation engine、语义 Router、workflow registry、Claude/Codex 入口、相关人读文档和 registry 回归测试；未实现 Decision Map schema、DAG、Frontier、分类器、promotion 工具或 Milestone/Iteration admission 接线。

## 验证方式与结果摘要

- `explore-contract`：专项合同测试通过，覆盖 AC1–AC6。
- `full-ci`：锁定 `uv 0.9.28` / Python `3.12.12` 的完整 CI 退出 0。
- `review-explore-contract`：P5 风险核心合同重跑通过，简评无 Must Fix / Should Fix。
- 详细证据见 `.ai/iterations/ITER-0102/VERIFY_REPORT.md` 与 `.ai/iterations/ITER-0102/evidence/`。

## 已知剩余风险 / 延后事项

自由文本 blocker 的质量仍无法由静态测试完全判断；本轮已经把其权限限制为可见、零写、需用户同意的建议。清晰度分类器及 Decision Map 确定性状态机继续由 MILE-0014 后续路线承接，本次不自动启动。

## 引用

- `.ai/iterations/ITER-0102/AC_LIST.md`
- `.ai/iterations/ITER-0102/TECH_PLAN.md`
- `.ai/iterations/ITER-0102/VERIFY_REPORT.md`
- `.ai/iterations/ITER-0102/CHANGELOG.md`
- `.ai/iterations/ITER-0102/evidence/`
