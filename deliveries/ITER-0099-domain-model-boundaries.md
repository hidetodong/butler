# Butler 领域地图与统一语言审计

## 本次交付目标

Butler 的核心概念分散在生命周期、质量门禁、上下文治理、宿主适配和驻留工具中。目录能说明规则放在哪里，却不能稳定回答一个词由谁定义、在哪个范围成立，以及跨模块引用时有没有悄悄改变含义。

本次先建立领域边界和统一语言的可查地图，为后续跨上下文合同与机器治理打地基，同时保持现有运行行为不变。

## 已完成内容

- 新增 `Coder/domain-model.md`，划分需求与范围、交付生命周期、可信保证、宿主运行时、知识连续性五个限界上下文。
- 审计 20 个高风险概念，逐项标明上下文限定、白话定义、唯一所有者、定义真源、允许别名、非职责与冲突状态。
- 用 dangerous/loop 错误绑定和人测残余 schema/manifest 冲突做反向验证，两个问题均保留为 `open → R3`，本轮没有偷改行为。
- 在 `Coder/README.md` 与 `Coder/architecture-overview.md` 注册领域地图，并明确领域上下文与 SOP Core / Domain Profiles / Business Extension 规则分层是正交视角。

## 关键变更 / 用户可感知变化

- 后续设计遇到 `active`、`pass`、Goal、Evidence、Dangerous Mode 等词时，可以先从领域地图确认命名空间和真源，不再靠目录位置或对话记忆猜语义。
- 地图只保存边界、所有权和指针，不复制 schema、状态枚举或算法；原规则文件和机器合同仍是唯一执行真源。
- MILE-0014 的后续工作现在有清晰切面：R2 建跨上下文合同，R3 再做术语 registry、门禁和已知冲突修复。

## 高层影响范围

规则功能面只新增 `Coder/domain-model.md`，并修改 `Coder/README.md`、`Coder/architecture-overview.md` 两处导航。DDD 来源摘要保存在 `.ai/references/domain-driven-design-fowler.md`。

本轮没有修改 P1→P5、Goal Assurance、PRD、Workspace Scope、hook、工具、公开命令、状态值或 dangerous/loop 的现有运行逻辑。对象级变更见 `.ai/iterations/ITER-0099/CHANGELOG.md`。

## 验证方式与结果摘要

- `domain-model-contract` 与 `review-domain-model-contract`：确认五个上下文、恰好 20 项术语、八列完整、22 个真源/导航指针存在、两个冲突仍路由 R3，且 Coder 改动集合严格等于计划三文件。
- `artifact-contract`、`markdown-links`、`diff-check`：阶段产物合同、仓库内 Markdown 链接和 diff 格式均通过。
- `reproduced-full-ci`：完整 `bash scripts/verify-ci.sh` 通过。首次 `full-ci` 因沙箱拒绝读取本机 uv 缓存失败，原失败记录保留，获准环境按同一 argv 重跑后转绿。
- 危险模式完整多维审查 verdict=`pass`，Must Fix=0、Should Fix=0；AC1–AC7 均有 passed evidence 覆盖。

## 已知剩余风险 / 延后事项

- 五个上下文是当前证据下的稳定切法，仍需在 R2/R3 dogfood 中持续演进；未来真实冲突可能要求改名、合并或拆分。
- 本轮完成了同上下文完整审查，但项目配置 `independent_review=false`，且当前协作约束未授权子 agent，因此没有执行 fresh-context 独立复核。
- dangerous/loop 错误绑定与人测残余容器冲突仅完成定位，实质修复按路线图留给 R3。

## 引用

- 验收清单：`.ai/iterations/ITER-0099/AC_LIST.md`
- 技术方案：`.ai/iterations/ITER-0099/TECH_PLAN.md`
- 验证报告：`.ai/iterations/ITER-0099/VERIFY_REPORT.md`
- 对象级变更流：`.ai/iterations/ITER-0099/CHANGELOG.md`
- 证据目录：`.ai/iterations/ITER-0099/evidence/`
- 里程碑路线图：`.ai/MILESTONE.md`
