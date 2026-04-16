# Goal

- 修复 Bucket A（命名与读取顺序一致性）4 条 Should Fix。

# In Scope

- AC-1: `/ideation` 触发词在三个文件中统一。
- AC-2: README 读取顺序与 architecture-overview 启用顺序去重，确立 SSOT。
- AC-3: mcv-deployment.md 标题层级对齐其他规则文件。
- AC-4: mcv-update.md 升级后目录结构命名风格裂痕修复，并（可选）补充热/冷数据命名策略规则。

# Out of Scope

- Bucket B/C/D/E（其余 7 条 Should Fix）。
- 新增规则文件、目录结构调整、模板合并。
- 对 Learner/Composer 的修改。

# Acceptance Checklist

- [ ] **AC-1** `/ideation` 触发词在 `logic-protocol.md`、`ideation-engine.md`、`HUMAN_GUIDE.md` 三处完全一致（以 `ideation-engine.md` 为 SSOT）
- [ ] **AC-2** README 读取顺序与 architecture-overview 启用顺序不再冗余，方案待拍板
- [ ] **AC-3** `mcv-deployment.md` 的章节标题统一为 `##`（与其他规则文件一致），不再孤立使用 `###`
- [ ] **AC-4** `mcv-update.md § 3` 升级后目录示例修复风格裂痕，方案待拍板

# Verification Method

- **AC-1**：grep 三个文件的 `/ideation` 触发词列表，关键词集合一致（脑暴 / 完善需求 / 想不清楚 / 还没想好）。
- **AC-2**：选定 SSOT 后，另一个文件不再重复列出读取顺序清单；交叉指针清晰。
- **AC-3**：`grep -n '^### [0-9]' Coder/20_Workflow_Lifecycle/mcv-deployment.md` 返回空，一级章节全为 `## [数字]`。
- **AC-4**：`mcv-update.md § 3` 热数据区命名带数字前缀，归档区命名策略明确（若方案选择把规则落地，需在 mcv-update.md 中补一条说明）。

# Open Questions / Risks

## ❓ 待拍板 - AC-2 方案选择

**问题**：`Coder/README.md § 读取顺序` 与 `Coder/architecture-overview.md § 3 启用顺序` 都描述了规则的读取与生效顺序，内容大面积重叠但细节有微差（architecture-overview 额外提到"在 P1 Analysis 识别项目类型"）。

### 方案 A（推荐）— README 做 SSOT

- `README.md § 读取顺序` 保持完整清单并吸收 architecture-overview 的补充细节（例如"P1 识别项目类型后再启用 10_Domain_Stack_Profiles"）。
- `architecture-overview.md § 3` 删除完整列表，改写为"具体读取顺序以 `README.md § 读取顺序` 为准"，自身只保留"三层分工"等概念性说明。
- **理由**：README 是入口文件（AI 必读），做 SSOT 天然路径最短；architecture-overview 定位为"补充说明"，应避免承担强约束。

### 方案 B — architecture-overview 做 SSOT

- `architecture-overview.md § 3 启用顺序` 保留完整清单。
- `README.md § 读取顺序` 改为指针"详见 architecture-overview.md § 3"。
- **理由**：architecture-overview 的描述更完整（含 P1 识别步骤）。
- **代价**：AI 读入口时还需跳转一次；README 的"读取顺序"章节消失会让入口显得单薄。

---

## ❓ 待拍板 - AC-4 方案选择

**问题**：AC-4 方案 A 把 `02_SESSION_HANDOFF.md` 统一加前缀后，`mcv-update.md § 3` 升级后目录示例出现风格裂痕：

```
.ai/
  /archive/
    CHANGELOG_2025.md
    BUG_LOG_v1.md
  CHANGELOG.md           ← 无前缀
  02_SESSION_HANDOFF.md  ← 带前缀
  BUG_LOG.md             ← 无前缀
  INDEX.md
```

### 方案 α（推荐）— 热数据统一带前缀，归档不强求；并把该命名策略写入规则

- 修改 `mcv-update.md § 3` 目录示例：热数据区（`.ai/` 根）的 `CHANGELOG.md` / `BUG_LOG.md` 都加前缀 → `01_CHANGELOG.md` / `03_BUG_LOG.md`；归档区（`.ai/archive/` 下）保持 `CHANGELOG_2025.md` / `BUG_LOG_v1.md`（按年份/版本分片，不强求前缀）。
- 在 `mcv-update.md § 3` 或 `mcv-deployment.md` 补一条命名策略说明：
  > 热数据（`.ai/` 根下）统一带数字前缀（`00_` / `01_` / `02_` / `03_`），与基地车部署命名一致。
  > 归档数据（`.ai/archive/` 下）按年份、版本或主题分片，命名可灵活处理，不强求前缀。
- **理由**：保留 AC-4 的一致性成果；归档命名的灵活性符合 mcv-update § 4.2 "Sharding" 的现有精神；同时把隐式约定变成显式规则。

### 方案 β — 只修目录示例，不落地命名策略规则

- 仅把 `CHANGELOG.md` / `BUG_LOG.md` 改为带前缀，不补充命名策略说明。
- **优点**：改动最小。
- **代价**：热/冷数据的命名差异仍然是隐式惯例，未来读者可能困惑。

### 方案 γ — 不加前缀、修 AC-4（回滚 SESSION_HANDOFF 带前缀决议）

- 本方案实质上是否定前一轮拍板，不推荐。

---

## 风险

- 本轮全部改动为规则文本，无运行时影响。
- `.ai/CONCEPT.md` 和 `.ai/AC_LIST.md` 覆写了上一轮 Must Fix 的产物；原版本在 git commit `8febaf3` 中可追溯。

---

# 请回复

1. **AC-2 方案选择**：A / B
2. **AC-4 方案选择**：α / β / γ

拍板后我进入 P3 TECH_PLAN 出具体 edit 清单，再等 ACK 进入 P4。
