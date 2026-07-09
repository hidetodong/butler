# TECH_PLAN — ITER-0039（MILE-0004 R4 · AC 钉版 + P2/P3/P5 接线）

> 监督态自驱。目标见 CONCEPT、验收见 AC_LIST，不重述。全为规则文档接线（扩展 3 schema + flip 1 指针，无新文件）。

## 设计决策（DD）

- **DD1 · 可选字段守非回归**：`prd_version` 挂在 `acceptance-schema §3` frontmatter，与 `状态`/`ACK 日期` 并列但**标可选**——非 PRD 迭代不写此行、frontmatter 逐字不变；hook 不校验它（旧 AC 无字段按 legacy）。这是 AC7 非回归红线的结构保证。
- **DD2 · 版本单一存 frontmatter、引用不重复**：版本化锚点 = slug + frontmatter 全局 `prd_version`；正文引用 `prd/<slug>.md` 不带版本后缀，解析时用 frontmatter 补齐。同 R3"映射单一真源"手法，防多处写漂移。
- **DD3 · 解析/核对靠回指、不复述落盘**：解析规则（live vs `.archive/vN/`）与"执行读最新"读侧纪律**回指 `references-schema §5 步骤 2/§7`**，acceptance/verify 侧只写"取哪一版核"、不重抄快照落盘契约。
- **DD4 · P3 跟 AC 走、不自立版本**：`tech-plan-schema` External References 引用 prd 切片时版本**继承 AC 钉住的 `prd_version`**、口径回指 `acceptance-schema`，技术方案不另记版本。
- **DD5 · P5 兑付点对钉住版核**：`verify-schema` References Compliance 从"对 `.ai/references/` 核"细化为"prd 切片对 AC 钉住 `prd_version` 核"；同迭代内 live 即钉住版（读 live），仅回溯复核历史迭代才读 `.archive/vN/`——不给 P5 常规路径加负担。
- **DD6 · amend 重冻只加一句**：`acceptance-schema §4` 补"amend 重冻可重绑 `prd_version`"，接 `iteration-schema §5.3` 既有退回-重 ACK 流程，不改 amend 本身；改版同步完整协议属 R5。
- **DD7 · flip 用既有翻牌手法**：`references-schema §7` bullet + §8 R4 行由待落地 → ✅ 已由三 schema 落地，与 R1/R2/R3 翻 §8 指针一致。

## 影响面（章节级）

| 文件 | 改动 | AC |
|---|---|---|
| `Coder/20_Workflow_Lifecycle/acceptance-schema.md` | §2 交付约定列 `prd_version` · §3 模板 frontmatter 加 `prd_version: —` 行 + 版本化 External References 示例 · §4 绑定/钉住语义 + amend 重绑 · §5 编写规则（版本取 frontmatter/不重复、标 AC↔slug） | AC1–3 |
| `Coder/20_Workflow_Lifecycle/tech-plan-schema.md` | §2 可选字段口径 · §3 模板 External References 版本化示例 · §4 编写规则（引用 prd 切片继承 AC 钉住版、回指 acceptance） | AC4 |
| `Coder/20_Workflow_Lifecycle/verify-schema.md` | §3 模板 References Compliance 行注钉住版 · §4 编写规则（对钉住 `prd_version` 核，回溯读 `.archive/vN/`，回指 references §5 步骤 2/§7） | AC5 |
| `Coder/40_Context_Management/references-schema.md` | §7 `prd_version` bullet flip 为已落地（指 acceptance）· §8 R4 行 flip ✅ | AC6 |

**不碰**：`milestone-schema`（R3 入口）、`prd-split` 切分算法、`references-schema §3` 登记表字段（不加列）、`logic-protocol`、`project-digest`、`context-persistence`、hook、`VERSION`、`/prd update` 同步/快照产生/认亲动作。

## Execution Steps（可勾选）

- [ ] S1 · `acceptance-schema §2` 交付约定加 `prd_version`（可选、引用 prd/ 时必填）+ §3 模板 frontmatter 加 `prd_version: —` 行 + 注释 → AC1
- [ ] S2 · `acceptance-schema §3` External References 示例补 prd 切片版本化引用 + §5 编写规则写"版本取 frontmatter/正文不重复 + 解析 live/.archive 回指 references §5 步骤 2/§7 + 标 AC↔slug" → AC2/AC1
- [ ] S3 · `acceptance-schema §4` 冻结字段补 `prd_version` 绑定/钉住语义 + amend 重冻可重绑（接 iteration §5.3）→ AC3
- [ ] S4 · `tech-plan-schema §2/§3/§4` External References 接线——引用 prd 切片继承 AC 钉住 `prd_version`、口径回指 acceptance、不自立版本 → AC4
- [ ] S5 · `verify-schema §3/§4` References Compliance 接线——对 AC 钉住 `prd_version` 核（同迭代 live 即钉住版 / 回溯读 `.archive/vN/`）、读侧回指 references §5 步骤 2 → AC5
- [ ] S6 · flip `references-schema §7` bullet + `§8` R4 行为 ✅ 已落地（指三 schema）→ AC6
- [ ] S7 · scope 守恒核对（`git status` 限 4 文件）+ **非回归核对**（`git diff` 无删除、非 PRD frontmatter 字面未动、hook 未碰）+ 说人话三条自检 → AC7/AC8
- [ ] S8 · P5 独立复核（干净上下文子 agent、对抗式）→ 收口

## 验证策略

全 auto·可靠（规则文档）：每 AC 读改后正文确认 + `git grep`/`git diff` 核守恒。核心对抗点＝**非回归**（`prd_version` 纯增量可选、非 PRD frontmatter 字面不变、hook 未动）+ **版本单一真源**（版本只在 frontmatter、正文/P3/P5 不重复）+ **引用不复述**（解析/落盘回指 references §5 步骤 2/§7、P3 版本回指 acceptance）+ **不越界**（只接钉版记录+核对，不做 R5 同步/快照产生、不碰 R3 入口/切分算法/契约结构）。dogfood：四件套 + 改动正文过说人话三条。无人测道残余。
