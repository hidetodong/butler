# Goal

- 修复 Bucket D（模板重复消除）1 条 Should Fix，确立 `templates/` 下的 SSOT 结构与部署流程的单一描述。

# In Scope

- `templates/CLAUDE.md.template` 与 `templates/rule-card.md` 的去重处理。
- `Coder/20_Workflow_Lifecycle/mcv-deployment.md § 3 规则注入` 的描述对齐。
- `CLAUDE.md`（仓库根）的"保持模板同步"约束如有必要也同步更新。

# Out of Scope

- 不改 lifecycle、其他 schema、Extension、scripts、context-persistence、role-switch。
- 不动浓缩规则卡的实质内容（角色 / 工作流 / 回退规则 / 基地车部署 / 执行纪律）；任一方案都保证内容等价。
- 不引入 Markdown include 之类的非标准机制。

# Acceptance Checklist

- [ ] **D-1** templates/ 下不再存在两份内容高度重复的模板，方案待拍板
- [ ] **D-2** `mcv-deployment.md § 3` 的部署描述与 templates/ 实际状态一致（不会出现"提到了不存在的模板文件"或"忽略了关键模板文件"）
- [ ] **D-3** `CLAUDE.md`（仓根）的"保持模板同步"约束按新结构调整或显式说明已自动满足

# Verification Method

- **D-1**：根据方案，`ls templates/` 输出符合预期；`diff templates/CLAUDE.md.template templates/rule-card.md`（如两者都保留）显示无强制约束段重复。
- **D-2**：通读 `mcv-deployment.md § 3`，提到的所有 templates/ 下文件都真实存在；流程步骤无 dangling reference。
- **D-3**：`CLAUDE.md` 第 20 行附近的"保持模板同步"约束措辞与新结构一致。

# Open Questions / Risks

## ❓ 待拍板 - D 方案选择

### 方案 X — 删除 `CLAUDE.md.template`，rule-card 作为唯一 SSOT

- 删除 `templates/CLAUDE.md.template`。
- `mcv-deployment.md § 3` 保持现状（已经只引用 rule-card.md），但补一条："深度阅读指针由 AI 在部署时按 mcv-deployment.md § 3 第 2 项的清单动态拼接，不依赖外部模板"；项目特定约束占位由 AI 按侦察结果生成。
- `CLAUDE.md` "保持模板同步" 约束改为"修改 rule-card.md 后无需手工同步其他模板（已无重复）"。
- **优点**：彻底消除重复；mcv-deployment 流程定义已经是 SSOT，不需要外部模板。
- **缺点**：人类失去一份"长这样的 CLAUDE.md"参考样例；新人接手时需读 mcv-deployment 推断最终输出。

### 方案 Y（推荐）— 保留 `CLAUDE.md.template` 作为骨架，强制约束段改为占位符

- `templates/CLAUDE.md.template` 改造：
  - 保留顶部说明、章节骨架、深度阅读指针、项目特定约束占位。
  - **删除**重复的"角色 / 工作流 / 回退规则 / 基地车部署 / 执行纪律"内容，替换为占位符 `<!-- {{RULE_CARD_CONTENT}} : 部署时由 AI 从 templates/rule-card.md 读取并替换此占位符 -->`。
- `mcv-deployment.md § 3` 部署描述更新为"读 `CLAUDE.md.template` 骨架 → 用 `rule-card.md` 内容替换 `{{RULE_CARD_CONTENT}}` → 替换 `{{BUTLER_PATH}}` → 填写项目特定约束 → 写入目标项目 CLAUDE.md"。
- `CLAUDE.md` "保持模板同步" 约束改为"修改强制约束只需改 rule-card.md，CLAUDE.md.template 通过占位符引用，无需手工同步"。
- **优点**：消除内容重复；保留模板的结构可读性；部署流程清晰；rule-card 仍是浓缩规则 SSOT。
- **缺点**：模板包含占位符，部署时多一步替换（成本极小）。

### 方案 Z — 保留两份，加同步约束 / pre-commit 检查

- 不去重，加一条"修改 rule-card 必须同步 CLAUDE.md.template 的强制约束段"的硬约束（可选 + pre-commit 脚本）。
- **缺点**：根本问题（重复）未解决；增加机制成本；不推荐。

### 方案 W — 反向：删除 rule-card.md，CLAUDE.md.template 作为唯一来源

- `mcv-deployment.md § 3` 改为"从 `CLAUDE.md.template` 读取，填空后写入目标 CLAUDE.md"。
- **缺点**：CLAUDE.md.template 包含项目特定约束占位等"目标项目特有"内容，作为浓缩规则 SSOT 不纯；mcv-deployment 描述需要大改；不推荐。

---

## 风险

- 任意方案都需要同步修改 `mcv-deployment.md § 3`（除方案 Z）。修改 mcv-deployment 是改部署主流程，但本轮只动 § 3 措辞，不变更部署语义。
- 选 X 后，未来如果想给人类提供"完整 CLAUDE.md 示例"，可以另起一份 `examples/example-CLAUDE.md`，不算本轮范围。

---

# 请回复

1. **方案选择**：X / Y / Z / W

拍板后进 P3 出具体 edit 清单。
