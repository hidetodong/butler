---
title: 迁移配方规范
audience: AI / 开发者
scope: 已部署项目升级时的"迁移配方"格式、台账位置、typed 操作标签与幂等 / 漂移契约
---

# Migration Schema（迁移配方规范）

## 1. 目标与定位

一份**迁移配方**回答一个问题：从上一发布版升级到本版，已部署的目标项目要做哪几步。

- 它是 `butler-upgrade.md` 升级执行器的**输入单一来源**——升级时不再现场推导差异，而是照配方执行。
- 与 `CHANGELOG.md` 分工：CHANGELOG 记"butler 自己改了什么"（给人读的发布史），配方记"已部署项目要做什么才能跟上"（给执行器照做）。二者不复述。
- 与 `versioning-schema.md` 分工：后者管版本号 / semver / 切版流程；本规范管切版时顺带产出的那份迁移步骤长什么样。

## 2. 台账位置与命名

- 配方落在仓库根 `migrations/` 目录——它是 butler 发布元数据（与 `deliveries/`、`CHANGELOG.md`、`VERSION` 同级），**不**放 `templates/`（那是给目标项目的模板）。
- 每个**对部署项目有结构影响**的发布版一份，命名 `migrations/vX.Y.Z.md`，版本号与该发布的 `VERSION` 一致。
- 对部署项目**无影响**的版本也必须建文件，内容为单条 `[no-op]`（见 §4）——"无影响"是显式结论，不是漏记。

## 3. 配方文件必含字段

每份 `migrations/vX.Y.Z.md` 必须含：

- 顶部一行：`> 区间: v<上一版> → vX.Y.Z · 聚合 ITER-NNNN[ ~ NNNN]`。
- `## 对已部署项目的影响`：一两句白话说清本版改了什么、影响落在 `CLAUDE.md` / `.ai/` / `.claude/hooks/` 的哪一处；无影响直说"无"。
- `## 迁移步骤`：有序列表，每步以 typed 标签（§4）起头，并写明**起始态校验**与**冲突处理**；无影响时只列一条 `[no-op]`。
- `## 不需要动作`：列出本版改了、但部署项目无需跟进的部分（如只改了 `Coder/` 规则正文——运行时实时读，不进目标项目），避免执行器误判漏迁。

## 4. typed 操作标签

每个迁移步骤必须以下列标签之一起头。所有标签**必须幂等**：先校验起始态，满足才动，重复执行不重复改。

- `[rename]`：重命名 `.ai/` 下过时文件。判据=旧名存在才改；git 项目走 `git mv` 保血缘。
- `[add-field]`：给 `.ai/` 下 schema 文件补新增的必填字段。判据=字段缺失才补；草稿值交用户 ACK。
- `[regen-claude]`：rule-card 内容变更时，重生成目标 `CLAUDE.md` 的 `{{RULE_CARD_CONTENT}}` 内联段。判据=始终重建 butler 管理区，`<!-- user-managed -->` 保护区内容原样保留。**漏判防线**：切版时只要本版聚合的**任一**迭代改动过 `templates/rule-card.md` 或 `templates/CLAUDE.md.template`，配方就**必须**含本步——rule-card 内联进每个目标 `CLAUDE.md`，漏掉会让目标规则卡停留旧文（用 `git log -- templates/rule-card.md` 核区间内提交）。
- `[sync-hooks]`：hook 体系变更时，按 `mcv-deployment.md §5.1` 重新拷贝 `.claude/hooks/` 副本（以 butler 版本为准覆盖）。判据=比对副本与仓库版本，不一致才覆盖。
- `[restamp]`：把 `CLAUDE.md` 版本戳重戳为目标版本。每份配方的 `[restamp]` 目标是该配方所属版本；多版队列连续执行时，逐版重戳或仅在队列末尾一次性戳到仓库当前 `VERSION` 均可，**最终以戳到当前 `VERSION` 为准**。每次升级末尾必做。
- `[no-op]`：本版对部署项目无结构影响，仅需末尾 `[restamp]`。

## 5. 幂等与漂移契约

- **幂等**：每步先校验起始态；已是目标态则跳过。重复升级、重复跑同一配方都安全。
- **漂移即停**：起始态与配方预期不符（目标项目被手工改过），执行器**不得**强行套用，必须停下、报告差异、退回用户 ACK 决定。
- **配方为主干、diff 为兜底**：配方给出确定步骤；内容 diff 用来在每步校验起始态、发现漂移——不是抛弃 diff，而是把它从"主驱动"降为"冲突哨兵"，与 `versioning-schema.md §8`"内容差异为主"一致。

## 6. 与切版 / 升级流程的关系

- **产出端**：配方在切版时产出，是 `versioning-schema.md §6` 的必做步（定 bump → 改 `VERSION` → 加 `CHANGELOG` → **写 `migrations/vX.Y.Z.md`** → 打 tag）。
- **消费端**：升级时由 `butler-upgrade.md` 收集"目标版本戳 < vV ≤ 仓库 `VERSION`"的全部配方、按版本号升序逐条应用。
