---
title: 问题理解模板
audience: AI / 开发者
scope: P1 Analysis 阶段的问题理解说明模板、字段约束与编写口径
---

# Concept Schema

## 1. 目标

用于在进入验收与设计前，先把“我理解的问题是什么”说清楚。

## 2. 交付约定

- 必须产出：`.ai/CONCEPT.md`
- 必填字段：`Goal`、`Current Understanding`、`Constraints`、`Impact Scope`、`Project Type / Active Profiles`、`Open Questions`

## 3. 标准模板

```md
# Goal
- 本次任务要解决什么问题

# Current Understanding
- 我当前对问题的理解
- 预期产出是什么

# Constraints
- 显性约束
- 隐性约束

# Impact Scope
- 会影响哪些模块、目录、角色或流程
- 明确不影响哪些区域

# Project Type / Active Profiles
- 当前项目属于哪类工程形态
- 已命中的 Domain / Stack Profiles
- 未命中时说明仅按通用 SOP 推进

# Open Questions
- 进入 P2 前仍需澄清的问题
```

## 4. 编写规则

- 重点是澄清问题，不是提前进入方案设计。
- 约束、影响范围与待确认问题必须显式写出。
- 若已识别到 profile，应在此处记录；若未识别到，不得强行套用领域规则。
- 不记录失败尝试与冗长调查日志，只保留当前有效理解。

## 5. 与执行流程的关系

- P1 阶段必须产出 `.ai/CONCEPT.md`，讨论结束后结晶为文件，不依赖对话记忆。
- P2 阶段从 `.ai/CONCEPT.md` 读取，AC 必须建立在这里已确认的目标与范围之上。
- 若目标理解变化，应回退到 P1 更新此文件。
- 简化路径下，P1 与 P2 合并，不单独产出 `CONCEPT.md`，结论直接折叠进 `AC_LIST.md`。