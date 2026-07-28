---
title: 本地化约束模板
audience: AI / 开发者
scope: .ai/local-constraints.md 的人类可读字段定义、编写口径与 legacy 兼容边界
---

# Local Constraints Schema

## 1. 目标

用于记录当前项目相对于 butler 通用 SOP 的**人类可读本地化适配**：项目类型、项目特有的放宽或收紧、范围例外和外部资源指针。

项目级机器配置已拆到 `.ai/butler.config.json`：Active Profiles 与 `dangerous` / `independent_review` / `preference` 不再写进本文件。旧项目的 Markdown 机器段只作为兼容输入，由 `tools/project-config/` 读取并经 `butler-upgrade` 事务迁移；新 JSON 存在时它是唯一真源。

## 2. 交付约定

- 必须产出：`.ai/local-constraints.md`
- 产出时机：基地车部署的 `mcv-deployment.md § 4 本地化适配` 步骤
- 必填字段：`Project Type`
- 可选字段：`Local Constraints`、`Scope Exceptions`、`External References`
- 配套机器产物：`.ai/butler.config.json`（schema 与读写真源：`tools/project-config/`）

## 3. 标准模板

```md
# Project Type
- 项目类型描述（Web 应用 / CLI / 库 / 规则仓等）
- 主要语言、框架与构建工具

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
- **机器配置不双写**：profile 和持久开关只写 `.ai/butler.config.json`；本文件不保留其镜像、注释版或状态摘要。
- **适度松散**：可选字段无内容时可省略，不强行凑内容。
- **更新而非追加**：任务执行中发现新 local 约束或例外时应回到此文件更新，不得仅在对话中声明。

### 4.1 机器配置与 legacy 兼容

- **新项目**：机器配置只写 `.ai/butler.config.json`。安全默认是 `dangerous=false`、`independent_review=false`、`preference=true`、`profiles=[]`；字段合同与命令见 `tools/project-config/README.md`。
- **兼容读取**：JSON 存在时必须完整合法并作为唯一真源；旧 Markdown 段仍在时逐字段比较并显式报告冲突，不用旧值覆盖 JSON。JSON 缺失时才回退旧 `Active Profiles`、「Butler 功能开关」和 `Review Policy`。
- **迁移**：`butler-upgrade` 的 `migrate_config` action 复用 project-config 纯迁移计划，在同一事务内创建 JSON，并从本文件删除上述机器段；其他段和原始字节保持不变。模糊 profile、非法值、重复段、冲突/损坏 JSON 或 symlink 首写前拒绝。
- **兼容期不双写**：迁移完成后命令只回写 JSON；旧 Markdown 回退只为尚未迁移项目保留，不长期维护两份状态。

## 5. 与执行流程的关系

- **会话起始**：持久模式与 profile 由项目配置兼容读取器提供；具体消费端接线见 `logic-protocol.md`，危险模式为 true 时仍须 announce-on-read。
- **基地车部署时**：按 `mcv-deployment.md §4` 同时生成本文件和 `.ai/butler.config.json`；本文件只含人类可读差异。
- **任务执行中**：若发现新 local 约束或例外区域，应回到此文件更新，再继续推进。
- **P2 AC_LIST / P3 TECH_PLAN**：若任务命中某 local 约束，相关 AC / Design Decisions 应显式引用本文件中的对应条目。
- **P5 VERIFY_REPORT**：`Gate Coverage` 的 Active Profiles 对 `.ai/butler.config.json`（或兼容期 legacy 投影）核对；Tech Plan Alignment 的本地约束仍与本文件对齐。
