---
title: 本地化约束模板
audience: AI / 开发者
scope: .ai/local-constraints.md 的字段定义、编写口径与最小模板
---

# Local Constraints Schema

## 1. 目标

用于记录当前项目相对于 butler 通用 SOP 的本地化适配：启用了哪些 profile、有哪些项目特有的放宽或收紧、哪些区域例外、关联的外部资源指针，以及**项目级 butler 功能开关的持久配置**（哪些持久模式当前开着）。

它是当前项目"对 butler 功能做项目级持久化配置"的**统一落点**——既记"与通用 SOP 的差异"，也记"本项目当前启用了哪些持久模式（如危险模式、独立复核）"。它不是规则复制器：通用规则继续从 butler 仓读取，本文件只记**配置与差异**，不复制引擎逻辑。

## 2. 交付约定

- 必须产出：`.ai/local-constraints.md`
- 产出时机：基地车部署的 `mcv-deployment.md § 4 本地化适配` 步骤
- 必填字段：`Project Type`、`Active Profiles`、`Butler 功能开关`（部署时即以安全默认全 off 生成）
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

# Butler 功能开关
# 项目级 butler 持久模式开关。AI 会话起始读取本段并据此激活/抑制模式；命令 NL 触发会回写，也可手改。
- dangerous: off            # on|off，默认 off。无人值守长程自治（见 65_Extension_Dangerous）。⚠️ on 时跨会话生效，AI 每会话起始须显式声明后才进入（announce-on-read），绝不静默
- independent_review: off   # on|off，默认 off。on 时每次 P5 收口自动起独立复核（fresh-context 子 agent，见 60_Extension_CodeReview §6）；始终可手动 /review 单跑，与本开关无关
```

## 4. 编写规则

- **不复制通用规则**：通用 SOP 继续从 butler 仓读取，`local-constraints.md` 只记"与通用 SOP 的差异"。
- **放宽/收紧必须附原因**：例如"`/legacy` 目录允许 `any`，原因：旧代码迁移中，阶段性降低类型门禁"。
- **引用而非复制**：profile 用文件名引用（如 `typescript-rules`），不复制 profile 内容。
- **适度松散**：可选字段无内容时可省略；`Active Profiles` 未命中 profile 时写"无"，不强行凑内容。
- **更新而非追加**：任务执行中发现新 local 约束或例外时应回到此文件更新，不得仅在对话中声明。

### 4.1 Butler 功能开关读写口径

- **会话起始必读**：已部署项目（存在 `.ai/local-constraints.md`）在会话起始**必须**读取本段，并据 `dangerous` / `independent_review` 的值激活或抑制对应持久模式，不依赖对话记忆（接线见 `00_System_Prompt/logic-protocol.md §1`）。
- **两种改法**：① 对话 NL 触发——模式命令（`/dangerous on|off`、收回/让渡把关权语义、项目级 `/review` 常开/关）触发时，模型**回写**本段对应开关；② 用户**手改**——直接编辑本段，模型下次读取即遵循。两条路等价、同一真源。
- **dangerous 安全（announce-on-read）**：`dangerous: on` **跨会话生效**，但 AI 每个会话起始读到 on 时**必须当回合显式声明**"危险模式当前 ON、本会话将按无人值守自治执行，要关说 `/dangerous off`"，声明后方自动进入，**绝不静默**。这是相对 `65_Extension_Dangerous/dangerous-engine.md §3` 原"会话结束不续开"的取舍：以可见性兜底替代不续开冗余，语义以该 §3 为准。
- **independent_review 默认 off**：仅在"本项目值得长期严格复核"时设 `on`；只影响 P5 收口是否自动起独立复核，不改变 P5 默认简评，也不妨碍随时手动 `/review`。
- **preference 不纳入**：偏好系统是**跨项目**的（状态与数据在外置 `$BUTLER_PREF`，见 `70_Extension_Preference/preference-probe-engine.md`），其 on/off 不是项目级配置，**不写入本段**。
- **legacy 兼容**：旧 `local-constraints.md` 无「Butler 功能开关」段时，所有开关按**默认 off** 处理；其中独立的 `Review Policy: independent_review` 字段是该开关的 legacy 形式，仍被尊重，不被误判。批量迁移走 `butler-upgrade.md`，不强制回填。

## 5. 与执行流程的关系

- **会话起始**：已部署项目在会话起始读取「Butler 功能开关」段并据此激活/抑制持久模式（接线见 `logic-protocol.md §1`）；`dangerous: on` 须按 §4.1 announce-on-read 显式声明。
- **基地车部署时**：按 `mcv-deployment.md § 4 本地化适配` 生成初版，必填字段须完整（含安全默认全 off 的功能开关段）。
- **任务执行中**：若发现新 local 约束或例外区域，应回到此文件更新，再继续推进。
- **P2 AC_LIST / P3 TECH_PLAN**：若任务命中某 local 约束，相关 AC / Design Decisions 应显式引用本文件中的对应条目。
- **P5 VERIFY_REPORT**：`Gate Coverage` 的 Active Profiles / Tech Plan Alignment 子项验证时，应与本文件的 Active Profiles / Local Constraints 对齐。
