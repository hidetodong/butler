# 更新日志 (Changelog)

本文件记录 butler 规则仓库的发布历史。版本号遵循[语义化版本](Coder/20_Workflow_Lifecycle/versioning-schema.md)：`MAJOR.MINOR.PATCH`。

每个版本聚合自上次发布以来收口的若干迭代（ITER），**只引用** `.ai/ITERATIONS.md` 与 `deliveries/`，不复述迭代细节。版本号机器真源是仓库根 `VERSION` 文件。

## [1.0.0] - 2026-06-19

首个正式版本基线。聚合 ITER-0001 ~ ITER-0007，为 butler 规则仓库确立硬版本概念（VERSION / CHANGELOG / git tag），并把版本接入部署产物与升级协议。

### 能力基线（本版已具备）

- **三层规则体系**：SOP Core（00/20/30/40）+ Domain / Stack Profiles（10）+ Business Extension（99），职责分明不混层。
- **五阶段产物链**：P1 CONCEPT → P2 AC_LIST → P3 TECH_PLAN → P4 Execute → P5 VERIFY_REPORT，阶段间经文件传递、不依赖对话记忆。
- **迭代化需求管理**：ITER-NNNN 台账 + 工作区/归档/交付三层落盘 + "固定需求"锁定纪律；**里程碑**（MILE-NNNN）作为松耦合、可选、方向性不冻结的大版本范围层，支持对话 / `origin/` 双通道录入与 `/milestone` 命令。
- **控制状态外化**：ACK 冻结门禁、入口分流可审计、项目级 butler 功能开关（`dangerous` / `independent_review`）统一落 `.ai/local-constraints.md` 并跨会话持久。
- **基地车生命周期三协议**：部署（mcv-deployment）/ 升级（butler-upgrade）/ 维护（mcv-update），配合 PreToolUse hook 机械门禁（产物缺失 / AC 未冻结拦截源码写）。
- **扩展模块**：ideation（脑暴）/ convergence-loop（死磕闭环）/ code-review（含 opt-in 独立复核，验证者≠实现者）/ dangerous（无人值守长程自治）/ preference（偏好探针，外置存储）。
- **本版新增（ITER-0007）**：硬版本概念落地——根 `VERSION` 为版本号 SSOT、`CHANGELOG.md` 为人读发布史、git tag `vX.Y.Z` 为发布锚点；部署把规则源版本戳进目标 `CLAUDE.md`（`{{BUTLER_VERSION}}`）；`butler-upgrade` 升级为版本感知（读目标戳 vs 仓库 VERSION 报 gap、升级后重戳，版本号为辅、内容差异为主）。

聚合迭代清单见 `.ai/ITERATIONS.md`，各迭代人类可读交付见 `deliveries/`。

[1.0.0]: 基线版本（无前序版本可比较）
