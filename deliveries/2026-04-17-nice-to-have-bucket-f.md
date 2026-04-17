# Butler 规则仓库 Nice to Have Bucket F 交付总结

> 日期：2026-04-17
> 任务：修复 Nice to Have Bucket F（低风险文档级精简与微调）5 条问题
> 状态：已完成，可交付

## 本次交付目标

在 Must Fix + Should Fix 全闭环（v0.0.8 里程碑）之后，推进低风险、低成本的 Nice to Have 批处理，让规则仓进一步收敛到"无空旷段、无硬编码枚举、无双形式选项"的状态。

## 已完成内容

| # | 问题 | 修复方式 |
|---|---|---|
| N-1 | `architecture-overview § 3` 只剩 3 行结构空旷 | 方案 B：合并 § 3 + § 4 为"启用顺序与生效规则"；原 § 5 / § 6 序号上移为 § 4 / § 5 |
| N-2 | `logic-protocol § 4.2` "表格 + 处理规则 + Fallback" 三段接近独立子节 | Fallback 段升级为 `#### Fallback（skill 不可用或调用失败时）` H4 标题 |
| N-3 | `architecture-overview § 2.2` 硬编码三个 profile 文件名 | 改为通用描述"`10_Domain_Stack_Profiles/` 下的所有 profile 文件，按当前项目命中的技术栈、语言或构建形态按需启用" |
| N-4 | `HUMAN_GUIDE § 8` 规则速查图对 30/40 子目录未展开 | 在速查图中展开 30（linting / testing-strategy / review-standard）与 40（context-persistence / handoff-spec / role-switch），每项附一句职责描述 |
| N-7 | `context-persistence § 3` 推荐载体 `task-state.json` 或 `.md` 双形式，实际部署只建 `.md` | 方案 α：单选 `.md`，删除 JSON 选项；措辞改为"载体：`.ai/task-state.md`" |

## 关键变更 / 用户可感知变化

- **architecture-overview 结构更紧凑**：从 6 章精简为 5 章；合并后的 § 3 既指向 README SSOT 又直接说清三层生效规则；原 3 行空旷段消失。
- **profile 清单不再硬编码**：未来新增 Vue 3.x、React、Rust 等任何 profile 都不必回头改 architecture-overview。
- **logic-protocol § 4.2 Fallback 段突出**：H4 标题让"skill 不可用时如何退化"这一分支更容易被 AI 和人类注意到。
- **HUMAN_GUIDE 速查图更完整**：新人查规则时 30/40 的子文件职责一目了然，不必再跳到 Coder/README.md 查。
- **task-state 载体统一**：规则与 mcv-deployment 部署实际一致，跨项目认知成本降低。

## 高层影响范围

**直接修改 4 个文件**：

- `Coder/architecture-overview.md`（§ 2.2 通用化 + § 3-§ 6 合并与序号重排）
- `Coder/00_System_Prompt/logic-protocol.md`（§ 4.2 Fallback 升 H4）
- `HUMAN_GUIDE.md`（§ 8 速查图 30/40 子展开）
- `Coder/40_Context_Management/context-persistence.md`（§ 3 载体单选）

**未影响**：lifecycle / mcv-deployment / mcv-update / 所有 schema / Extension / templates / scripts / Domain Profiles 目录本身。

## 验证方式与结果摘要

| 验证动作 | 结果 |
|---|---|
| `grep '^## [0-9]\.' architecture-overview.md` | 5 章节（§ 1/2/3/4/5），§ 3 为"启用顺序与生效规则" ✅ |
| `grep '^#### Fallback' logic-protocol.md` | L105 命中 ✅ |
| `grep 'vue3-standard\|typescript-rules\|build-tooling' architecture-overview.md` | 0 命中（已通用化） ✅ |
| HUMAN_GUIDE § 8 展开 6 个子文件 | L183-189 全部命中 ✅ |
| `grep 'task-state.json' context-persistence.md` | 0 残留 ✅ |

详细验证记录见 `.ai/VERIFY_REPORT.md`。

## 已知剩余风险 / 延后事项

### Nice to Have 剩余（2 条）

- **N-5** `.ai/local-constraints.md` 缺 schema — Bucket G（独立）
- **N-6** `10_Domain_Stack_Profiles/` 三个 profile 不同级（vue3 框架 / typescript 语言 / build-tooling 构建形态）— Bucket H（结构调整，最重）

### 可逆决策记录

N-7 把 `task-state` JSON 选项移除属可逆决策。如未来 butler SOP 引入自动化脚本读取 task-state 场景，可重新加回 JSON 选项。

## 可选引用

- 产物链：`.ai/CONCEPT.md`、`AC_LIST.md`、`TECH_PLAN.md`、`VERIFY_REPORT.md`
- 关联规则：
  - `Coder/architecture-overview.md`（§ 2.2 + § 3 合并）
  - `Coder/00_System_Prompt/logic-protocol.md § 4.2`（Fallback H4）
  - `HUMAN_GUIDE.md § 8`（速查图扩展）
  - `Coder/40_Context_Management/context-persistence.md § 3`（task-state 单选）
- 前 6 份交付：
  - `deliveries/2026-04-17-must-fix-repair.md`
  - `deliveries/2026-04-17-should-fix-bucket-a.md`
  - `deliveries/2026-04-17-should-fix-bucket-e.md`
  - `deliveries/2026-04-17-should-fix-bucket-b.md`
  - `deliveries/2026-04-17-should-fix-bucket-c.md`
  - `deliveries/2026-04-17-should-fix-bucket-d.md`
- 当前 milestone：`v0.0.8`（Must Fix + Should Fix 全闭环）
