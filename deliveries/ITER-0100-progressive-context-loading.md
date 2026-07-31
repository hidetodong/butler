# 上下文预算与渐进注入

## 本次交付目标

把 R1 的完整领域审计从每次冷启动的潜在常驻负担，改造成有预算、可按需下钻、证据不足时能够继续续批的渐进知识入口，同时保留原执行真源和必要门禁。

## 已完成内容

- 建立 L0 最小路由、L1 五上下文地图、L2 20 项术语查询和 L3 历史审计四层结构。
- 明确普通任务、术语消歧、跨上下文设计和历史审计四种读取路径；首批最多读取 3 份直接真源，仍不足时以可见回执继续下一批。
- 新增上下文预算检查器、6 个负向测试和完整 CI 接线，覆盖体量、结构、术语迁移、越界路径及软链逃逸。

## 关键变更 / 用户可感知变化

- 新上下文不再默认完整读取 `domain-model.md` 或递归展开全部指针；普通任务从 694 bytes 的 L0 路由直接进入目标专项规则。
- `domain-model.md` 收敛为 3894 bytes 的 L1 地图，20 项定义移到可定向查询的 L2；与 R1 综合文档相比正文 bytes 缩减约 68.6%。
- “最多 3 份”只是首批上限而不是总上限：证据不足时必须公开已读内容、剩余缺口、下一批文件和继续理由，因此不会因预算机械截断复杂问题。

## 高层影响范围

- 规则导航：`Coder/README.md`、`Coder/domain-model.md`、`Coder/domain-glossary.md`、`Coder/architecture-overview.md`。
- 工程门禁：`tools/context-budget/` 与 `scripts/verify-ci.sh`。
- 项目知识：`.ai/project/architecture.md`、`.ai/project/invariants.md`、`.ai/project/frontier.md`。

## 验证方式与结果摘要

- AC1–AC8 均有 passed 机器证据；16 个 evidence ID 的 hash/record 完整性校验通过并已归档。
- 上下文预算合同、6 个负向单测、Markdown 链接、artifact contract、state audit、`git diff --check` 和完整 `scripts/verify-ci.sh` 均通过。
- Goal Assurance 裁决为 `eligible`；同上下文审查最终 Must Fix=0、Should Fix=0。本轮 `independent_review=false`，没有冒称 fresh-context 独立审查。

## 已知剩余风险 / 延后事项

- 当前使用 bytes、非空行和指针数作为稳定预算代理，不等同于不同模型 tokenizer 下的精确 token 数。
- 尚无宿主运行时读取遥测，不能证明每个模型会话都严格遵守路由；只有后续观察到实际偏离时，才在 R3 评估是否增加追踪。
- 跨上下文主链的输入、输出、保真和失效合同属于 MILE-0014 R3，本轮没有提前实现。

## 引用（只引用，不嵌入）

- `.ai/iterations/ITER-0100/AC_LIST.md`
- `.ai/iterations/ITER-0100/TECH_PLAN.md`
- `.ai/iterations/ITER-0100/VERIFY_REPORT.md`
- `.ai/iterations/ITER-0100/CHANGELOG.md`
- `.ai/iterations/ITER-0100/evidence/`
