---
title: 本地化约束模板
audience: AI / 开发者
scope: .ai/local-constraints.md 的字段定义、编写口径与最小模板
---

# Local Constraints Schema

## 1. 目标

用于记录当前项目相对于 butler 通用 SOP 的本地化适配：启用了哪些 profile、有哪些项目特有的放宽或收紧、哪些区域例外、关联的外部资源指针。

它不是规则复制器 —— 通用规则继续从 butler 仓读取；`.ai/local-constraints.md` 只记录"本项目与通用 SOP 的差异"。

## 2. 交付约定

- 必须产出：`.ai/local-constraints.md`
- 产出时机：基地车部署的 `mcv-deployment.md § 4 本地化适配` 步骤
- 必填字段：`Project Type`、`Active Profiles`
- 可选字段：`Local Constraints`、`Scope Exceptions`、`External References`

## 3. 标准模板

```md
# Project Type
- 项目类型描述（Web 应用 / CLI / 库 / 规则仓等）
- 主要语言、框架与构建工具

# Active Profiles
- 命中的 Domain / Stack Profiles，按 `10_Domain_Stack_Profiles/` 下实际文件列出
- 若未命中任何 profile，显式写"无，仅按通用 SOP"

# Local Constraints
- 本项目相对于通用 SOP 的放宽或收紧
- 每条附一句原因

# Scope Exceptions
- 不受某类通用规则约束的目录或文件
- 每条附适用的例外规则与原因

# External References
- 外部资源指针（API 文档平台、设计稿、issue tracker 等）
- 此处仅做高层指针；实际参考资料提取产物在 `.ai/references/` 下
```

## 4. 编写规则

- **不复制通用规则**：通用 SOP 继续从 butler 仓读取，`local-constraints.md` 只记"与通用 SOP 的差异"。
- **放宽/收紧必须附原因**：例如"`/legacy` 目录允许 `any`，原因：旧代码迁移中，阶段性降低类型门禁"。
- **引用而非复制**：profile 用文件名引用（如 `typescript-rules`），不复制 profile 内容。
- **适度松散**：可选字段无内容时可省略；`Active Profiles` 未命中 profile 时写"无"，不强行凑内容。
- **更新而非追加**：任务执行中发现新 local 约束或例外时应回到此文件更新，不得仅在对话中声明。

## 5. 与执行流程的关系

- **基地车部署时**：按 `mcv-deployment.md § 4 本地化适配` 生成初版，必填字段须完整。
- **任务执行中**：若发现新 local 约束或例外区域，应回到此文件更新，再继续推进。
- **P2 AC_LIST / P3 TECH_PLAN**：若任务命中某 local 约束，相关 AC / Design Decisions 应显式引用本文件中的对应条目。
- **P5 VERIFY_REPORT**：`Gate Coverage` 的 Active Profiles / Tech Plan Alignment 子项验证时，应与本文件的 Active Profiles / Local Constraints 对齐。
