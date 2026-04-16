# Goal

- 修复 Butler 规则全流程审计中发现的 7 条 Must Fix 问题。

# In Scope

- 7 条 Must Fix 的全部修复动作。
- 涉及 8-11 个规则文件的文本修改（具体以 AC-1 / AC-4 方案为准）。
- 修复后跨文件一致性校验。

# Out of Scope

- 10 条 Should Fix（后续迭代）。
- 4 条 Nice to Have（后续迭代）。
- 新增规则文件、目录结构调整、模板合并重构。
- 对 Learner / Composer 子系统的修改。

# Acceptance Checklist

- [ ] **AC-1** Ideation→P2 产物链闭合（方案待拍板）
- [ ] **AC-2** `identity.md` 和 `logic-protocol.md` 补齐 frontmatter（audience + scope）
- [ ] **AC-3** `Coder/README.md` 列表编号损坏修复（`95 - / 96 -` 等异常数字改为普通 bullet）
- [ ] **AC-4** SESSION_HANDOFF 命名在所有规则文件中统一（方案待拍板）
- [ ] **AC-5** `mcv-deployment.md` 中 `00_IDEATION.md` 的"部署时初始化"与"仅在 /ideation 激活后产生"消除矛盾
- [ ] **AC-6** `maintenance-boundaries.md` BUG_LOG 强制更新时机补充 "Ralph-Loop 熔断 RCA"
- [ ] **AC-7** `maintenance-boundaries.md` CHANGELOG 强制更新时机补充 "Review 产出的 Should Fix 条目"

# Verification Method

- **AC-1**：通读 `lifecycle.md` P2、`acceptance-schema.md` § 5/6、`ideation-engine.md` § 4，Ideation 路径到 P2 的输入源闭合，任一读者不产生"CONCEPT.md 是否存在"的歧义。
- **AC-2**：`grep -l '^---$' Coder/00_System_Prompt/*.md` 返回两个文件；frontmatter 字段包含 `audience` 和 `scope`。
- **AC-3**：`Coder/README.md` 列表项前缀统一为 `-`，无 `95 - / 96 -` 等异常编号；Markdown 渲染后视觉正常。
- **AC-4**：`grep -rn "SESSION_HANDOFF" Coder/ HUMAN_GUIDE.md` 所有出现处命名一致（全部带 `02_` 前缀 或 全部无前缀，取决于方案）。
- **AC-5**：`mcv-deployment.md` Section 2 中 `00_IDEATION.md` 的描述不再出现"部署时初始化"与"仅在 /ideation 激活后产生"并列的矛盾；任一读者能判断文件何时产生。
- **AC-6**：`maintenance-boundaries.md` BUG_LOG 行包含 "Ralph-Loop 熔断" 或等价 RCA 触发描述。
- **AC-7**：`maintenance-boundaries.md` CHANGELOG 行包含 "Review" 或 "Should Fix" 触发描述。

# Open Questions / Risks

## ❓ 待拍板 - AC-1 方案选择

**问题**：`/ideation` 收敛后产物为 `.ai/00_IDEATION.md`，但 `lifecycle.md` P2 强制"从 `.ai/CONCEPT.md` 读取"。Ideation 路径到达 P2 时存在输入源断链。

### 方案 A（推荐）— 在 Ideation 收敛时同步结晶 CONCEPT.md

- 改动：仅在 `ideation-engine.md` § 4 产物章节增加一条"收敛后必须将最终结论同步结晶为 `.ai/CONCEPT.md`，作为 P2 的标准输入"。
- 优点：保持 `lifecycle.md` 的 P2 单入口约定不变；产物链主干最干净。
- 代价：Ideation 路径产出两份文件（`00_IDEATION.md` 记录过程，`CONCEPT.md` 记录结论），但分工清晰。

### 方案 B — `lifecycle.md` P2 输入源扩展为双路径

- 改动：`lifecycle.md` P2 章节改为"从 `.ai/CONCEPT.md` 或 `.ai/00_IDEATION.md` 的已确认结论读取"；`acceptance-schema.md` § 6 同步更新。
- 优点：Ideation 产物仍为单文件。
- 代价：P2 的输入源变成双路径，规则复杂度外溢。

### 方案 C — `acceptance-schema.md` 内部处理

- 改动：仅在 `acceptance-schema.md` 补充一段"Ideation 路径下 P1+P2 折叠，可跳过独立 CONCEPT.md"。
- 优点：最小改动。
- 代价：跳过 CONCEPT.md 的规则分散在多处（简化路径、Ideation 路径），后续读者需跨文件理解；`lifecycle.md` 的强制规则出现隐式例外。

---

## ❓ 待拍板 - AC-4 SESSION_HANDOFF 命名统一

**问题**：`SESSION_HANDOFF.md` 在规则仓中同时以 `02_SESSION_HANDOFF.md`（有数字前缀）和 `SESSION_HANDOFF.md`（无前缀）两种形式出现：

| 文件 | 当前命名 |
|---|---|
| `mcv-deployment.md:41` | `02_SESSION_HANDOFF.md` |
| `HUMAN_GUIDE.md:100` | `02_SESSION_HANDOFF.md` |
| `mcv-update.md:44` | `SESSION_HANDOFF.md` |
| `handoff-spec.md` 全文 | `SESSION_HANDOFF.md` |
| `context-persistence.md:101` | `.ai/02_SESSION_HANDOFF.md` |
| `progressive-handoff.md:37` | `SESSION_HANDOFF.md` |

### 方案 A（推荐）— 统一 `02_SESSION_HANDOFF.md`（带前缀）

- 改动：`mcv-update.md`、`handoff-spec.md`、`progressive-handoff.md`、`delivery-summary.md`、`testing-strategy.md` 中所有无前缀引用改为带前缀。
- 优点：与 `00_IDEATION.md`、`01_CHANGELOG.md`、`03_BUG_LOG.md` 命名风格一致；新人看基地车目录一眼知道是运行态文件；数字前缀暗示读取顺序。
- 代价：更多文件需要改动。

### 方案 B — 统一 `SESSION_HANDOFF.md`（无前缀）

- 改动：`mcv-deployment.md`、`context-persistence.md`、`HUMAN_GUIDE.md` 中带前缀引用改为无前缀。
- 优点：规则文件改动点更少（主要规范文件已用无前缀）。
- 代价：整个 `.ai/` 命名风格分裂（为什么 HANDOFF 没前缀，其他都有？）；与基地车部署的视觉一致性被破坏。

---

## 风险

- **跨文件表述漂移**：修完后需做一次 grep 扫描（见 AC 验证方式），否则留下新不一致。
- **不涉及代码执行**：修改均为规则文本，验证只能靠人工阅读 + grep，无自动化门禁保障（这是本次可接受的限制）。

---

# 请回复

1. **AC-1 方案选择**：A / B / C
2. **AC-4 方案选择**：A / B

两个都拍板后，我进入 P3 TECH_PLAN 阶段给出具体的文件级 edit 清单，再等一次 ACK 进入 P4 执行。
