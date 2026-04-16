# Butler 规则仓库 Should Fix Bucket D 交付总结（兼 Should Fix 全闭环）

> 日期：2026-04-17
> 任务：修复 Should Fix Bucket D（模板重复消除）1 条 + 完成 Should Fix 11 条全闭环
> 状态：已完成，可交付

## 本次交付目标

修复 Butler Should Fix Bucket D：消除 `templates/CLAUDE.md.template` 与 `templates/rule-card.md` 内容高度重复，同时澄清两者与 `mcv-deployment.md § 3 规则注入` 的角色关系（原描述只引用 rule-card，让 CLAUDE.md.template 在规则上孤立）。

## 已完成内容

### Bucket D 修复（方案 Y：模板骨架 + 占位符）

| # | 问题 | 修复方式 |
|---|---|---|
| 1 | 两份模板的强制约束段（角色 / 工作流 / 回退 / 部署 / 纪律）逐条复制 | `CLAUDE.md.template` 删除重复段，替换为 `{{RULE_CARD_CONTENT}}` 占位符；rule-card.md 不动作为浓缩规则 SSOT |
| 2 | mcv-deployment.md § 3 只提 rule-card 不提 template，描述与实际错位 | 重写 § 3 为 5 步流程（读模板 → 替换 RULE_CARD_CONTENT → 替换 BUTLER_PATH → 填项目约束 → 写入） |
| 3 | butler 项目根 CLAUDE.md 第 20 行"保持模板同步"约束（手工双写假设） | 改为"模板单一来源"，明确改强制约束只需改 rule-card.md |
| 4（P5 暴露）| 模板顶部注释字面写占位符，部署时会被误替换 | 注释改为文字描述，附一行鲁棒性说明 |

### Should Fix 11 条全闭环回顾

| Bucket | 数量 | 主题 | 关键决策 | 提交 |
|---|---|---|---|---|
| A | 4 | 命名与读取顺序一致性 | README 做 SSOT；mcv-update 显式化"热数据带前缀 / 归档灵活" | `d266acf fix(0.0.4)` |
| E | 2 | 平台与回退健壮性 | setup.sh 加 OSTYPE 分支；skill 失败禁止越权 WebFetch | `8d8d239 fix(0.0.5)` |
| B | 3 | 产物链字段补全 | Gate Coverage 扩 4 类；P4 task-state 硬约束；P5 → delivery-summary § 2 指针 | `b25c1b7 fix(0.0.6)` |
| C | 1 | Mode 术语消歧 | mode-switch.md → role-switch.md，Role/角色 替换 Mode/模式 | `6ecffb6 fix(0.0.7)` |
| D | 1 | 模板重复消除 | template 骨架 + rule-card SSOT + 占位符替换 | （本提交）|

## 关键变更 / 用户可感知变化

- **修改强制约束只需改一份**：今后调整 `角色 / 强制工作流 / 回退规则 / 基地车部署 / 执行纪律` 等内容，只编辑 `templates/rule-card.md` 即可，部署时自动注入到目标项目的 CLAUDE.md。
- **部署流程从"两部分组成"变为"5 步明确流程"**：每步动作可独立检查，AI 部署时能逐步推进；新人理解部署流程更直观。
- **模板鲁棒性提升**：占位符字面（双花括号）只出现在需要替换的位置，避免简单 `str.replace_all` 时注释被误污染。
- **dogfooding 验证**：本轮（以及前 4 轮）全程使用 butler 自己的 P1-P5 流程，包括 6 次完整产物链 + 6 份 Delivery Summary，证明 SOP 在自身维护场景下可执行。

## 高层影响范围

**Bucket D 直接修改 3 个文件**：

- `templates/CLAUDE.md.template`（Write 整体重写：38 行，原 70 行；2 次 Edit 含鲁棒性修复）
- `Coder/20_Workflow_Lifecycle/mcv-deployment.md § 3`（重写为 5 步流程）
- `CLAUDE.md`（butler 项目根，L20 约束更新）

**未影响**：`templates/rule-card.md`（不动，作 SSOT）、其他规则文件、scripts、Extension、`.ai/` 产物链结构。

## 验证方式与结果摘要

| 验证动作 | 结果 |
|---|---|
| `wc -l templates/CLAUDE.md.template` | 38 行（原 70）✅ |
| 重复段关键字数 | 0 ✅ |
| `{{RULE_CARD_CONTENT}}` 字面计数 | 1（仅替换位置）✅ |
| `{{BUTLER_PATH}}` 字面计数 | 10（6 深度阅读 + 4 阶段产物）✅ |
| mcv-deployment § 3 五步骤完整 | ✅ |
| CLAUDE.md "模板单一来源"约束就位 | L20 ✅ |
| rule-card 章节齐全（角色 / 工作流 / 回退 / 部署 / 纪律）| ✅ |

详细验证记录见 `.ai/VERIFY_REPORT.md`。

## 已知剩余风险 / 延后事项

### Should Fix 全部清空

原审计 10 条 + Must Fix 修复中暴露的 1 条 = 11 条 Should Fix 已 100% 修复。

### Nice to Have（4 条，可选）

审计报告中列出的 Nice to Have 仍未处理：

1. `10_Domain_Stack_Profiles/` 三个 profile 不是同级概念
2. `HUMAN_GUIDE.md` 规则速查图仍偏粗
3. `context-persistence.md:35` `task-state.json` 与 `.md` 双形式建议统一
4. `architecture-overview.md:42-46` 硬编码三个 profile 文件名（变更时需同步）
5. `.ai/local-constraints.md` 没有 schema

（本次新增观察）`architecture-overview § 3` 简化后只剩 3 行，结构略空旷可考虑合并；本次 Bucket D 也观察到 `logic-protocol § 4.2` 已接近独立 H3 子节（"表格 + 处理规则 + Fallback"三段）。

### 其他可选后续工作

- 引入 CI / pre-commit 检查（markdown 链接、占位符未替换、frontmatter 完整性等）
- 跨任务产物管理规则（当前每轮覆写 `.ai/`，依赖 git 历史回溯；可显式落成规则）
- 验收 Linux 真机执行 setup.sh（Bucket E 因本地无环境只做了代码评审）

## 全 Should Fix 累计影响

- **修改文件总数**：约 18 个规则文件 + 1 个 shell 脚本（部分文件被多个 bucket 修改）
- **新增规则**：热/冷数据命名策略（Bucket A）、Fallback 段（Bucket E）、Tech Plan Alignment & References Compliance（Bucket B）、模板单一来源（Bucket D）
- **重命名文件**：1 个（mode-switch.md → role-switch.md，git mv 保留血缘）
- **术语契约固化**：Mode（运行时能力，与 /xxx 命令绑定）vs Role（执行者职责切换，与 P1-P5 阶段映射）
- **Delivery Summary 累计**：6 份（1 Must Fix + 5 Should Fix bucket）

## 可选引用

- 产物链：`.ai/CONCEPT.md`、`AC_LIST.md`、`TECH_PLAN.md`、`VERIFY_REPORT.md`
- 关联规则：
  - `templates/CLAUDE.md.template`（重写后骨架 + 占位符）
  - `templates/rule-card.md`（浓缩规则 SSOT，未改动）
  - `Coder/20_Workflow_Lifecycle/mcv-deployment.md § 3`（部署流程 5 步）
  - `CLAUDE.md`（butler 项目根，L20 模板单一来源约束）
- 全部 6 份 delivery：
  - `deliveries/2026-04-17-must-fix-repair.md`
  - `deliveries/2026-04-17-should-fix-bucket-a.md`
  - `deliveries/2026-04-17-should-fix-bucket-e.md`
  - `deliveries/2026-04-17-should-fix-bucket-b.md`
  - `deliveries/2026-04-17-should-fix-bucket-c.md`
  - `deliveries/2026-04-17-should-fix-bucket-d.md`（本文件）
