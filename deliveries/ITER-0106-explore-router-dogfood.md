# Explore Router 接线与 Butler 真实 dogfood

## 本次交付目标

把已经完成的 Explore / Decision Map / Decision Work / Decision Promotion 接入 Butler 现有单一入口，并用 Butler 自身的一项真实大需求检验恢复、研究、交接和维护成本。

## 已完成内容

- 扩充既有 `ideation` workflow 的显式 Explore / Decision Map / Wayfinder 语料，没有新增入口或 workflow ID。
- 建立 24 个零写 Router 合同样本和六类快路径下界检查，保留明确小任务、独立 Iteration、直接 Milestone 与轻量 Ideation 的原行为。
- 新增 `tools/explore-dogfood/`，在临时项目中覆盖三 Decision、依赖 Frontier、两项 Research、显式 absorb、fresh-process 恢复和合法 promotion 全链路。
- 用 `codex-structured-question-cards` 候办建立真实 `DMAP-0001`；三个 Decision 已解决，一个 Fog 保留，候办继续 `deferred`。
- 增加 live verifier，确定性证明已占用 R5 的 promotion 返回 `route_unavailable`、没有 receipt 且语义状态零写。
- 形成四项观测报告，并将外部 tracker 建设裁决为 `defer`。

## 关键变更 / 用户可感知变化

- Explore 是既有 Ideation 的 opt-in 持久化深度，不是普通任务进入 P1 前的新必经阶段。
- Router 不用清晰度、体量或模型置信度静默开 Map、Milestone、Iteration；只有用户显式探索，或用户接受带具体 blocker 的零写建议，才进入 Explore。
- Decision Map 成为可参考、可恢复的决策来源；真正开工仍通过显式 promotion 回到现有 Milestone / Iteration，并从 P1 开始。
- 本次真实 Research 请求为 `parallel`，实际执行是 `serial`、非 fresh-context；系统如实记录，没有把结构上的可并行冒充成已提速。

## 高层影响范围

- Router / registry 与 Claude、Codex、Pi 薄适配的共同合同。
- Explore / Ideation 的生命周期边界与部署说明。
- 三个 Decision Module 的内部 dogfood harness、live verifier、回归矩阵和人读报告。
- Butler 当前项目的真实 Decision Map / Work 状态、P5 evidence 与知识文件夹。

## 验证方式与结果摘要

- Router 13 项、dogfood 4 项、Decision Map 18 项、Decision Work 17 项、Decision Promotion 18 项及双宿主/三宿主静态矩阵均通过。
- `explore-dogfood-live-r2` 核对三项 Decision resolved、两个 Attempt absorbed、候办 deferred、promotion 拒绝及零语义写。
- P5 同上下文简评发现的 Router 自证与 live 证据缺口已修复；`review-explore-risk-r2` 重新执行风险矩阵，最终 Must Fix 0、Should Fix 0。
- `full-ci-r3` 在锁定 Python 3.12.12 / uv 0.9.28 环境通过；先前环境和状态契约失败 record 均保留为纠错轨迹。
- Goal Assurance 返回 `eligible`；完整逐 AC 结论见归档 `VERIFY_REPORT.md` 与 evidence 目录。

## 已知剩余风险 / 延后事项

- 任意自然语言改写仍由宿主模型理解；本次锁住的是显式 trigger 下界和代表 corpus，不是生产误路由率。
- 本轮没有观察到 Research 并行提速，也没有覆盖跨机器、多人写入、查询通知和长期规模。
- 外部 tracker 因缺少实证阻塞保持 `defer`；开放 Fog 只作为未来参考，不阻塞本轮交付。
- 项目配置未启用独立复核，本次仅执行同上下文简评。

## 引用

- `.ai/iterations/ITER-0106/CONCEPT.md`
- `.ai/iterations/ITER-0106/AC_LIST.md`
- `.ai/iterations/ITER-0106/TECH_PLAN.md`
- `.ai/iterations/ITER-0106/VERIFY_REPORT.md`
- `.ai/iterations/ITER-0106/CHANGELOG.md`
- `.ai/iterations/ITER-0106/evidence/`
- `docs/explore-dogfood-r5.md`
- `tools/explore-dogfood/README.md`
