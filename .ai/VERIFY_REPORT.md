# Verification Summary

- 覆盖范围：Bucket D 的 1 条 Should Fix（模板重复消除，方案 Y），涉及 3 个文件 4 处改动（含 P5 阶段暴露的占位符鲁棒性修复）。
- 总体结论：**全部通过**。Bucket D 完成后，全部 11 条 Should Fix 已 100% 闭环。

# AC Status

- [x] **D-1** templates/ 下不再存在内容高度重复的两份模板 — 已满足
- [x] **D-2** mcv-deployment.md § 3 部署描述与 templates 实际状态一致 — 已满足
- [x] **D-3** CLAUDE.md（butler 仓根）的"保持模板同步"约束按新结构调整 — 已满足

# Verification Results

- **D-1**：
  - `wc -l templates/CLAUDE.md.template` = 38 行（原 70 行，缩减 ~46%）。
  - `grep -c '强制工作流\|回退规则\|执行纪律' templates/CLAUDE.md.template` = 0（重复段已删除）。
  - 占位符精确性：`{{RULE_CARD_CONTENT}}` 出现 1 次（仅在替换位置）；`{{BUTLER_PATH}}` 出现 10 次（6 个深度阅读路径 + 4 个阶段产物路径）。
  - 顶部注释改为文字描述，避免部署时占位符字面被误替换（P5 阶段暴露并修复，详见 Remaining Risks）。
- **D-2**：
  - `mcv-deployment.md § 3` 重写为 5 步明确流程，每步可独立执行。
  - 通读 § 3，提到的 `templates/CLAUDE.md.template` 与 `templates/rule-card.md` 都真实存在；占位符 `{{RULE_CARD_CONTENT}}` / `{{BUTLER_PATH}}` 与模板字面一致。
- **D-3**：
  - `CLAUDE.md` L20 命中"模板单一来源"新约束；旧"保持模板同步"措辞已无残留。
- **整体内容等价性自检**：
  - rule-card.md 的 H2 章节齐全：`## 角色 / ## 强制工作流 / ## 回退规则 / ## 基地车部署（新项目接入时）/ ## 执行纪律` —— 部署后这些 H2 会平铺在 CLAUDE.md 顶层，与现行 CLAUDE.md.template 中"### 强制工作流 / ### 回退规则 / ### 基地车部署 / ### 执行纪律"在内容上等价（仅 H 层级降一级，部署后所有顶级章节同为 H2，结构反而更平整）。

# Gate Coverage

- **通用质量门禁**：改动聚焦、可全部映射回 3 条 AC；frontmatter 完整性保持；模板占位符语法（`{{...}}`）与 mcv-deployment 描述完全一致。
- **Active Profiles**：本轮无命中。
- **Tech Plan Alignment**：
  - Design Decisions 1（占位符位置：H1 直下，不外包 H2）→ template 实际结构 ✅
  - Design Decisions 2（rule-card 不动）→ 文件未修改 ✅
  - Design Decisions 3（mcv-deployment § 3 改写为 5 步）→ L65-73 五步骤齐全 ✅
  - Design Decisions 4（CLAUDE.md "模板单一来源"）→ L20 已就位 ✅
  - Design Decisions 5（Write vs Edit 选择）→ template 用 Write 重写、其他两个用 Edit ✅
- **References Compliance**：N/A（本轮无 `.ai/references/` 下的外部参考资料）。

# Remaining Risks

## 🔍 P5 阶段已暴露并修复的 1 个问题

**问题**：初版 CLAUDE.md.template 顶部注释中字面写了 `{{RULE_CARD_CONTENT}}` 与 `{{BUTLER_PATH}}` 作描述。部署时若 AI 用简单 `str.replace_all`，会把注释里的占位符也替换掉，导致最终 CLAUDE.md 的注释里塞入大段 rule-card 内容（不影响 AI 行为，但模板鲁棒性差）。

**修复**：注释改为纯文字描述（"下方的规则卡占位符 / 深度阅读指针中的 butler 路径占位符"），并附一行说明："占位符字面（双花括号包裹）只出现在需要被替换的位置"。修复后占位符字面计数从模糊变为精确（1 + 10）。

**评级**：本应在 P3 TECH_PLAN 阶段就预见到的边角情况。归类为"P5 自评的合理产出"，不构成回退到 P1/P2 的依据。

## 无其他遗留风险

# Handoff / Next Step

- 本轮任务已完整闭合。
- 产物链：`.ai/CONCEPT.md` → `.ai/AC_LIST.md` → `.ai/TECH_PLAN.md` → 本文件。
- 交付总结：`deliveries/2026-04-17-should-fix-bucket-d.md`（也是 Should Fix 全闭环总收尾）。
- **Should Fix 全部完成**：原 11 条（10 + 1 新暴露）已全部修复，覆盖 5 个 bucket（A / B / C / D / E）。
- 可选后续工作：
  - 4 条 Nice to Have（可挑选处理）
  - 引入 CI 检查 / 自动化 lint（如 markdown 链接检查、占位符未替换检查等）
  - butler 自身使用 dogfooding 经验沉淀为新规则（如"跨任务产物管理"规则，已在 dogfooding 过程中通过覆写 + commit 历史 implicitly 解决）
