# Butler 统一语义 Router 与会话转迭代入口

## 本次交付目标

让 Claude 与 Codex / ChatGPT 共用一套 Butler 语义路由规则，并把高频的「总结当前会话后领取一个迭代」变成可重复、可审计、失败可回滚的标准工作流。

## 已完成内容

- 新增宿主无关 Router 真源、四态返回合同和覆盖 13 个业务工作流的共享语义样例。
- 新增 Claude `/butler`、`/butler:iteration` 与 Codex / ChatGPT `$butler-router`、`$butler-iteration` 薄入口。
- 将 workflow registry 升级为 schema v2，加入优先级、排除词、冲突和前置关系的严格校验与幂等投影。
- 新增 `iteration-intake` 零写 plan / 事务 apply：区分用户决定、模型建议和开放问题，拒绝双 active，并支持里程碑路线绑定和故障回滚。
- 扩展 Claude 全局安装器，以相同所有权规则同时管理根命令文件和命名空间目录软链。

## 关键变更 / 用户可感知变化

- 在 Claude 中可以用 `/butler <自然语言>` 让 Butler 选择一个主工作流；具体 `/butler:*` 命令仍直接执行，不绕 Router。
- 在 Codex / ChatGPT 中，选择 Butler 后可由 `$butler-router` 按语义分发；直接选择具体 `$butler-*` Skill 仍有更高确定性。
- 用户说「总结这次讨论，然后领一个迭代做」时会进入独立 iteration 工作流；只说「总结」不会写项目。
- `loop` 和 `dangerous` 仍不能被普通语义隐式打开，只会返回显式调用要求。

## 高层影响范围

改动覆盖共享规则、workflow registry、Claude commands、Codex plugin skills、全局安装器、确定性 iteration 工具、生成文档与双宿主测试。没有增加 Pi Router，也没有改变既有业务工作流算法或宿主平台自身的 `@` / slash / `$` 交互机制。

## 验证方式与结果摘要

- Registry / Router：11 项测试通过，覆盖严格 schema、四态样例、13 工作流、显式高风险边界、投影幂等和失败回滚。
- Iteration intake：5 项测试通过，覆盖复合台账取号、active 拒绝、里程碑绑定、内容结晶与全 `.ai` 回滚。
- 全局安装器：17 项测试通过，覆盖双软链幂等、旧 checkout 迁移、用户文件冲突和 TOCTOU 拒绝。
- 两个新 Skill 均通过官方 quick validator；完整 `bash scripts/verify-ci.sh` 在 uv 0.9.28 / Python 3.12.12 下通过。

## 已知剩余风险 / 延后事项

- 仓内能可靠验证文件发现结构和路由合同，但没有在真实 Claude Code 会话里确认 `/butler` 与 `/butler:*` 的 UI 同时展示。
- ChatGPT App 的真实 `@Butler` 选择和隐式 Skill 注入由宿主版本决定，本轮没有可用界面端到端证据，因此保持弱验证口径。
- 新入口已进入源码和安装流程；现有机器要实际使用，需要另行显式运行 Butler setup / refresh。

## 引用

- 验收清单：`.ai/iterations/ITER-0100/AC_LIST.md`
- 技术方案：`.ai/iterations/ITER-0100/TECH_PLAN.md`
- 验证报告：`.ai/iterations/ITER-0100/VERIFY_REPORT.md`
- 对象级变更流：`.ai/iterations/ITER-0100/CHANGELOG.md`
- 证据目录：`.ai/iterations/ITER-0100/evidence/`
