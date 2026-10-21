# 基地车只在对的项目展开

> ITER-0055 · 标准 P1–P5 · 用户双 ACK · P5 主 agent 完整审查 · 2026-07-17 · v2.16.0

## 交付目标

修复 Butler 把会话启动目录误当成施工项目根的问题，确保台账、四件套、入口和交付只落在任务实际对应的项目下。

## 已完成内容

- 新增无副作用项目根解析器：用户点名路径 → 最近已部署 Butler 根 → Git 根 → 拒绝。
- MCV、rule-card、主动升级、8 个 Claude commands 与 8 个 Codex skills 共用同一根目录契约。
- Codex patch adapter 支持绝对 target 跨 cwd 定位实际项目；相对路径不能从聚合目录偷渡选中子仓，一个 patch 也不能跨多项目根。
- renderer 拒绝不存在、非目录或不可读写的目标；历史升级队列先切到 `PROJECT_ROOT` 再执行旧配方。
- `research/.ai/iterations/ITER-0051` 误展开空残留已删除，`research/*/.ai` 各子项目台账未改动。

## 用户可感知变化

从包含多个仓库的父目录启动会话时，Butler 不再往父目录创建 `.ai`。任务已点名项目路径时直接使用它；没点名且无法唯一定位时，Butler 会先询问，不猜测子目录。

## 高层影响范围

- 共同内核：MCV/升级协议、rule-card、项目根算法、hook Context adapter。
- Claude 适配：8 个全局 commands 及部署 hook 副本。
- Codex 适配：8 skills、plugin hooks、双入口/兼容说明。
- 迁移：v2.16.0 重生成双入口、同步 hooks 并刷新机器级 plugin，不搬迁已有 `.ai`。

## 验证结果

- 8 个双入口渲染场景 + 7 个项目根场景全绿。
- 127 个 hook 测试全绿；真 wrapper 验证了跨 cwd 绝对 target 放行与聚合目录相对 `.ai` 拒绝。
- R1/R2/R3 结构脚本、隔离 setup 双分支、Python compile、shell syntax 与官方 plugin validator 全绿。
- P5 主 agent 审查发现 1 个 Must Fix 并修正；复审 0 Must Fix。未授权子 agent，故不宣称独立复核。

## 剩余边界

- PreToolUse 不是 sandbox，本迭代未声明覆盖 shell/MCP 通用写入。
- 无 Git/无 Butler 标记的新目录需用户明确点名，这是有意的 fail-closed 成本。

## 引用

- `.ai/iterations/ITER-0055/AC_LIST.md`
- `.ai/iterations/ITER-0055/TECH_PLAN.md`
- `.ai/iterations/ITER-0055/VERIFY_REPORT.md`
- `migrations/v2.16.0.md`
