# VERIFY_REPORT — ITER-0039（MILE-0004 R4 · AC 钉版 + P2/P3/P5 接线）

> 监督态自驱。全为规则文档接线（扩展 3 schema + flip 1 指针，无新文件）。验证 = 读改后正文核契约 + `git diff` 核非回归 + `git status` 核守恒，确定性可复现（**auto·可靠**）· 无人测道残余。

## 验收结果（逐 AC · auto·可靠）

- [x] **AC1 ✓** `acceptance-schema §2` 新增 `prd_version` 可选 frontmatter 说明（引用 `references/prd/` 切片时必填、记 ACK 冻结那刻 PRD **全局版本号**、冻结绑定之后钉住）；**全局非逐片编版** + **非 PRD 迭代不写/frontmatter 逐字不变**两点均显式成文；§3 模板 frontmatter 加 `prd_version: —` 行 + 注释同步体现。
- [x] **AC2 ✓** `acceptance-schema §5` 写死**版本化锚点 = slug + frontmatter 全局 `prd_version`**、**版本号只存 frontmatter 一处**、正文引用 `prd/<slug>.md` 不逐条重复；解析规则成文（PRD 仍在该版 → live 即钉住版 / 已改版超过 → 读 `.archive/v<prd_version>/<slug>.md`），落盘与读侧**回指 `references-schema §5 步骤 2/§7`、不复述**；§3 External References 示例佐证（切片行标"版本＝frontmatter、正文不重复"）。
- [x] **AC3 ✓** `acceptance-schema §4` 补 `prd_version` 绑定/钉住语义（置 `ack-frozen` 绑当刻全局版、之后钉住＝锁死不随后续改版漂移）+ **amend 重冻可重绑**（接 `iteration-schema §5.3` 退回 draft 重 ACK、不改 amend 流程本身，改版完整同步明确划归 `/prd update`）；§5 编写规则补"引用取 frontmatter/不重复 + 标 AC↔slug"。
- [x] **AC4 ✓** `tech-plan-schema §3/§4` External References 接线——引用 prd 切片版本**继承 AC 钉住的 `prd_version`**、技术方案**不自立版本**、口径**回指 `acceptance-schema §5`**、对着钉住版设计；模板示例同步（切片行标"版本继承 AC frontmatter"）。
- [x] **AC5 ✓（核心兑付点）** `verify-schema §3/§4` References Compliance 接线——PRD 切片**对着 AC 钉住 `prd_version` 核、非对 live 最新核**；成文口径"同迭代内 live 即钉住版（读 live 即可）/ 仅回溯复核历史迭代（PRD 此后已改版）才按 `prd_version` 读 `.archive/vN/<slug>.md`"，语义/读侧**回指 `acceptance-schema §4` / `references-schema §5 步骤 2`**、不复述。
- [x] **AC6 ✓** `references-schema §7` `prd_version` bullet flip 为"**已由 `acceptance-schema §4/§5` 落地**"；`§8` 边界表 R4 行 flip 为"**✅ 已由 `acceptance-/tech-plan-/verify-schema` 落地**"。
- [x] **AC7 ✓（守恒 + 非回归 + 分层）** 源改动集 = 恰 **4 文件**（`acceptance-schema` + `tech-plan-schema` + `verify-schema` + `references-schema`），`git status` 佐证无越界。**非回归红线**：`git diff` 全 4 处删除均系 flip/接线**行替换**（旧文本语义全保留、只增补），无纯删除、无内容丢失；`prd_version` 为可选纯增量字段——旧 AC_LIST 无此行按 legacy、非 PRD frontmatter 字面不变；**hook 未碰**（不给 `prd_version` 加机械校验）。**不做** `/prd update` 同步/快照产生(R5)/认亲(R6)；**不改** R3 入口（`milestone-schema` diff 空）/`prd-split` 切分算法/`references-schema §3` 登记表字段（未加列）/`logic-protocol`/`project-digest`/`context-persistence`/`VERSION`；**不切版**。改动仍在 SOP Core（`20`/`40`），分层未破坏。
- [x] **AC8 ✓（dogfood·说人话）** `prd_version`（配"记 PRD 哪一版"释义 + 示例 `v1.1`）/ 钉版（"给验收清单钉版"）/ 钉住（"锁死不随 PRD 后续改版漂移"）/ 全局版本（"一份 PRD 一个版本号、非逐片编版"）/ 锚点（"slug + 全局版本"）均首现带解释；英文字段名 `prd_version` 在中文语境有释义包裹；无裸英文/变量残留。

## 独立复核

- **执行**：干净上下文子 agent，验证者≠实现者、只读、对抗式；四对抗点（可选字段真非回归/hook 未碰 · 版本单一真源不双写 · 引用/解析靠回指不复述 · 不越界做 R5 同步/R6 认亲）逐点核。
- **结论**：**APPROVE-with-nits**。四对抗点全过——① `prd_version` 确为可选、非 PRD frontmatter 逐字不变、`grep` 证 hook 目录零改动、4 处删除全系 flip 行替换旧语义存活；② 版本只存 frontmatter，改后 3 文件字面 `v1.1` 皆示例、`.archive` 路径用占位、P3/P5 皆回指 frontmatter 不各自存版本；③ 解析/落盘回指 references §5/§7、P3 版本回指 acceptance §5，被回指目标全部真实且内容对得上；④ `git diff --stat` 证 milestone-schema/prd-split/iteration-schema/logic-protocol/hooks/project-digest/context-persistence/VERSION 全零改动，§3 登记表未加列，§8 R5/R6 行未 flip。AC1–AC8 逐条 confirm。Must Fix 无。
- **Should Fix 处置（已修）**：复核挑出两规则文件（acceptance §5 / verify §4）引 `references-schema §5.2`——但 references §5「读纪律」是无子节编号的有序列表，"执行读最新"实为 §5 步骤 2，`5.2` 子节不存在（本仓库 ITER-0035 有同款判例定为悬空指针）。已按判例改为 `§5 步骤 2`，并同步四件套产物同款标号；acceptance §5 的 `§5.2/§7` 拆写为"§5 步骤 2 见读侧 / §7 见落盘"。
- **Nit（未改）**：`.archive` 占位两处写法不同（verify `.archive/vN/` vs acceptance `.archive/v<prd_version>/`），语义等价、均与 references §7 约定相容，纯观感、不动。

## Remaining Risks

- 钉版协议本轮**只定"怎么记 / 怎么解析 / 怎么核"**，尚未有产生 `.archive/vN/` 快照的动作——AC5 回溯读 `.archive/vN/` 的路径要到 **R5 `/prd update`** 真正冻出快照后才走得通；在此之前钉住版永远 == live（同迭代无改版），钉版的跨改版审计价值**待 R5 才首次实战兑付**。
- "版本单一存 frontmatter、正文不重复"靠执行遵从守（同 R3 回指不复述信任模型）；真到多 slug、多 AC 引用同一 PRD 时是否始终不在正文私自补版本号，取决于遵从。
