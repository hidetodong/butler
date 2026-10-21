# Butler 规则仓库 Should Fix Bucket E 交付总结

> 日期：2026-04-17
> 任务：修复 Should Fix Bucket E（平台与回退健壮性）2 条问题
> 状态：已完成，可交付

## 本次交付目标

修复 Butler Should Fix Bucket E 的 2 条问题：`scripts/setup.sh` 仅在 macOS/BSD 可用的 `sed -i` 语法限制；`Coder/00_System_Prompt/logic-protocol.md` 参考资料注入规则在 skill 不可用时缺失回退路径。

## 已完成内容

| # | 问题 | 修复方式 |
|---|---|---|
| 1 | `setup.sh` 的 `sed -i ''` 在 GNU sed（Linux）会报 `extra characters at end of command` | 加 `[[ "$OSTYPE" == "darwin"* ]]` 分支：darwin 保留 `sed -i ''`，其他平台用 `sed -i` |
| 2 | `logic-protocol.md § 4.2` 参考资料注入表依赖 `confluence-api-extractor` / `mastergo-codegen` skill，未定义 skill 不可用时 AI 该怎么办 | 在 § 4.2 "处理规则"后追加 Fallback 段（方案 β）：skill 失败时 **不得**自行 WebFetch 越权，必须改为提示用户手动粘贴文本 |

## 关键变更 / 用户可感知变化

- **Linux 用户现在可正常执行 `scripts/setup.sh`**：之前 `sed -i ''` 会在 GNU sed 上报错导致 BUTLER_PATH 无法更新，现已修复。
- **参考资料处理路径显式化 fallback**：当 AI 环境没有 skill（如在非 Claude Code 环境）或 skill 调用失败时，AI 不会擅自跳过参考资料，也不会越权发起网络请求；会主动提示用户手动提取后粘贴文本。
- **安全/权限边界更明确**：对企业鉴权场景（Confluence 私域页面）友好 —— AI 不会无意中触发未授权的 WebFetch。
- **审计可追溯**：Fallback 路径产出的参考资料在 `AC_LIST.md` / `TECH_PLAN.md` 的 `External References` 中强制标注"用户手动提供"，区别于 skill 自动化产物。

## 高层影响范围

**直接修改 2 个文件**：

- `scripts/setup.sh`（L22-29：sed 调用扩展为 `$OSTYPE` 分支）
- `Coder/00_System_Prompt/logic-protocol.md`（§ 4.2 末尾追加 Fallback 段）

**未影响**：templates/、其他规则文件、`.ai/references/` 约定、现有参考资料存储路径。

## 验证方式与结果摘要

| 验证动作 | 结果 |
|---|---|
| `bash -n scripts/setup.sh` | 语法通过 ✅ |
| `grep -nE 'OSTYPE\|sed -i' scripts/setup.sh` | 命中 `$OSTYPE` 分支 + 两个 sed 调用 ✅ |
| `grep -n 'Fallback' logic-protocol.md` | L105 / L110 命中 ✅ |
| `grep -n '不得.*WebFetch' logic-protocol.md` | L107 命中核心约束 ✅ |

详细验证记录见 `.ai/VERIFY_REPORT.md`。

## 已知剩余风险 / 延后事项

### 代码评审替代真机（E-1）

本地无 Linux 环境，E-1 的 Linux 分支未经真机测试。`sed -i "s|...|...|"` 是 GNU sed 标准语法，代码评审足以判定正确性。若生产使用发现问题，回退成本极低。

### Nice to Have（观察）

`logic-protocol.md § 4.2` 现已有"表格 + 处理规则 + Fallback"三段，接近独立 H3 小节的信息量。未来若继续扩充，可拆分为 H4 子标题（`#### 主路径` / `#### Fallback`）。本轮保留现有结构。

### 未处理的 Should Fix（5 条）

- Bucket B（产物链字段补全，3 条）
- Bucket C（Mode 术语消歧，1 条）
- Bucket D（模板重复消除，1 条）

建议下一步推进 **Bucket B**（需新增 schema 字段，但修完后 P1→P5 产物链审计闭环会更完整）。

## 可选引用

- 产物链：`.ai/CONCEPT.md`、`AC_LIST.md`、`TECH_PLAN.md`、`VERIFY_REPORT.md`
- 关联规则：
  - `Coder/00_System_Prompt/logic-protocol.md § 4.2 外部参考资料注入`（新增 Fallback 段）
  - `scripts/setup.sh`（E-1 修复点）
- 前两轮交付：
  - `deliveries/2026-04-17-must-fix-repair.md`（Must Fix 修复）
  - `deliveries/2026-04-17-should-fix-bucket-a.md`（Bucket A 修复）
