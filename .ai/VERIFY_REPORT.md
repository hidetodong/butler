# Verification Summary

- 覆盖范围：Bucket E 的 2 条 Should Fix，涉及 2 个文件 2 处 edit。
- 总体结论：**全部通过**。

# AC Status

- [x] **E-1** `scripts/setup.sh` 的 `sed -i` 跨平台兼容 — 已满足
- [x] **E-2** `logic-protocol.md § 4.2` 参考资料 skill 失败时的 Fallback 规则（方案 β）— 已满足

# Verification Results

- **E-1**：
  - `bash -n scripts/setup.sh` 语法检查通过；
  - `grep -nE 'OSTYPE|sed -i' scripts/setup.sh` 显示 `[[ "$OSTYPE" == "darwin"* ]]` 分支结构存在，sed 调用在 if 分支内（macOS 用 `sed -i ''`、非 darwin 用 `sed -i`）；
  - Linux 真机验证受限（本地无环境），以代码评审为准，`sed -i "s|...|...|"` 为 GNU sed 标准语法。
- **E-2**：
  - `grep -n 'Fallback' Coder/00_System_Prompt/logic-protocol.md` 命中 L105 和 L110，Fallback 段落结构完整；
  - `grep -n '不得.*WebFetch' logic-protocol.md` 命中 L107，核心约束"**不得**越权访问外部资源"明确落地；
  - 通读 § 4.2，Fallback 段与原表格"存储位置"口径一致（命名前缀 `api-` / `design-` / `insight-` / 无前缀 不变）；
  - `External References` 标注要求（"用户手动提供"）与 `acceptance-schema.md` / `tech-plan-schema.md` 现有字段兼容。

# Gate Coverage

- **通用质量门禁**（linting）：
  - 改动聚焦、无无关混入 ✅
  - 所有改动可映射回 2 条 AC ✅
  - setup.sh 仍满足 `set -euo pipefail` 严格模式 ✅
- **Active Profiles**：无命中。
- **Review 简要自评**（P5 默认触发）：
  - Must Fix：无。
  - Should Fix：无新发现。
  - Nice to Have（观察）：`logic-protocol.md § 4.2` 现在有"表格 + 处理规则 + Fallback"三段，已接近 H3 小节的信息量。未来若 § 4.2 继续扩充，可考虑拆成 H4 子标题（`#### 主路径 / #### Fallback`），本轮不处理。

# Remaining Risks

- **代码评审替代真机**：E-1 的 Linux 分支未经真机测试。生产中第一个 Linux 用户会是事实上的验证人；若发现问题，快速回退成本极低（加一条 `$OSTYPE` 分支）。
- 无其他新暴露风险。

# Handoff / Next Step

- 本轮任务已完整闭合。
- 产物链：`.ai/CONCEPT.md` → `.ai/AC_LIST.md` → `.ai/TECH_PLAN.md` → 本文件。
- 交付总结：`deliveries/2026-04-17-should-fix-bucket-e.md`。
- 后续 Should Fix 剩余：Bucket B（3 条，产物链字段补全）、Bucket C（1 条，Mode 术语消歧）、Bucket D（1 条，模板重复消除）。
- 建议下一步 **Bucket B**（需要 schema 字段新增，但在主产物链上，修完后审计闭环更完整）。
