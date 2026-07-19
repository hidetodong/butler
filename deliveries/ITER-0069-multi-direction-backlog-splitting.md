# ITER-0069 · 多方向候办拆分

## 本次交付目标

- 让一次讨论里的多个独立方向进入不同候办块，并分文件存放。
- 保证每个方向能够独立修改、删除或提升为正式里程碑。

## 已完成内容

- 定义“候办块 = 一个可独立决定开工的版本方向”，同一里程碑内部路线项不会被误拆。
- 锁定一方向一个候办键、一行台账索引、一份候办草稿文件。
- Claude 命令、Codex skill、workflow registry 与规则卡同步多方向拆分语义。
- 状态审计改为要求草稿只有一个且与文件名一致的候办键，以及唯一 `deferred` 状态。

## 关键变更 / 用户可感知变化

- 同时讨论 A、B、C 三个独立方向时，会形成三个平级候办块和三份草稿，而不是一份混合文档。
- 之后执行 `start <候办键>` 只提升指定方向，不会把其他待办一起带入正式里程碑。

## 高层影响范围

- 里程碑候办与部署规则真源。
- Claude/Codex 里程碑入口和 registry 生成投影。
- 项目状态审计及其回归测试。

## 验证方式与结果摘要

- 状态审计专项 20 项通过，包含双候办分文件正例和三类身份混装负例。
- workflow registry 对账及 `git diff --check` 通过。
- 完整 CI 通过，覆盖双宿主、Markdown、147 项 hooks、Goal 和统一安装/入口矩阵。
- Goal adjudicator 十项检查全部通过，裁决为 `eligible`。

## 已知剩余风险 / 延后事项

- 本轮无未关闭实现风险。
- 方向是否真正可以独立开工仍需 AI 做语义判断；机械审计只负责落盘和身份隔离。
- 本轮不切版本、不发布、不推送，也不升级外部项目。

## 引用

- `.ai/iterations/ITER-0069/AC_LIST.md`
- `.ai/iterations/ITER-0069/TECH_PLAN.md`
- `.ai/iterations/ITER-0069/VERIFY_REPORT.md`
- `.ai/iterations/ITER-0069/CHANGELOG.md`
- `.ai/iterations/ITER-0069/evidence/`
