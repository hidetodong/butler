# MILE-0004 R4 · AC 钉版 + P2/P3/P5 接线

> ITER-0039 · 里程碑 MILE-0004 第四块 · 监督态自驱（承 R1 契约 + R2 切分 + R3 入口）· 不切版（纯规则接线）

## 一句话

R3 让 butler 会把大 PRD 一份输入喂两个海拔了，但里程碑指向切片的指针指的都是"当前最新"——PRD 一改版（V1.1→V1.2），就无从锚定"当初冻结这条 AC 时对的是哪一版"。R4 给验收清单**钉版**：AC 顶部加一个 `prd_version` 字段，在 ACK 冻结那一刻绑定当时的 PRD 全局版本号、之后**钉住**（钉住＝锁死不随 PRD 后续改版漂移）；再把这个钉住版接进 P2/P3/P5——P3 对着钉住版设计、**P5 对着钉住版核**（不是对 live 最新核）。这样"验收对的是当初冻结时那一版规格"跨改版可审计，也给 R5 的改版同步铺好前置。

## 背景（为什么现在做、缺口在哪）

- R1–R3 已让"一份 PRD → 切片 → 挂进里程碑"闭环成型，但**全都指向 live 最新**：`references/prd/<slug>.md` 永远是 PRD 当前态。真实项目 PRD 天然按"修改项"迭代改版，一旦改版，之前已冻结/已验收的 AC 引用的那条精确规则可能已经变了——却**没有任何锚点**记住"这条 AC 当初核的是 V1.1 的规格"。
- 缺的正是**把引用钉到版本**这一块。grilling 十节点已定死方向：**全局版本**（一份 PRD 一个版本号，不给每片单独编版）+ **执行读最新、留版本可回溯**（Q2=b）+ **冻结绑定**（Q3=ii，ACK 那刻绑、之后钉住）。R4 就是把这三条决议物化成 AC 字段 + P2/P3/P5 接线。

## 做什么（DD）

- **DD1 · AC frontmatter 加 `prd_version`（全局版本 · 冻结绑定 · 之后钉住 · 可选字段）**：`acceptance-schema` 的 AC_LIST 顶部 frontmatter 增一个 `prd_version` 字段。语义——当本迭代引用了 `references/prd/` 切片时，此字段记 **ACK 冻结那一刻 PRD 的全局版本号**（如 `v1.1`），冻结即绑定、之后钉住。**全局**＝一份 PRD 一个版本号（非逐片编版，守 Q2=b）。字段**可选**：只有引用 prd/ 知识文件夹的迭代才填；对话驱动 / 普通 references（api-/design-/insight-）/ 非 PRD 迭代**不带**此字段（非回归红线——绝大多数迭代 frontmatter 一字不变）。
- **DD2 · 版本化引用锚点 = slug + frontmatter 的全局版本（版本单一存 frontmatter、引用处不重复）**：引用锚点概念上是 (slug, 版本) 对，但**版本号只存 frontmatter 一处**（全局、单一真源），正文引用 `prd/<slug>.md` 时不逐条重复版本号——解析时用 frontmatter 的 `prd_version` 补齐。这守"版本单一真源"（同 R3 映射不双写）。解析规则：(slug, prd_version) → PRD 仍在该版则 live `prd/<slug>.md` 即钉住版；PRD 已改版超过它则回溯读 `.archive/v<prd_version>/<slug>.md`（§7 全量快照自包含、一定取得到当年原文）。
- **DD3 · P2 `acceptance-schema` 接线**：§2 交付约定 + §3 模板 frontmatter 增 `prd_version`（可选、引用 prd/ 时必填）；§4 冻结状态字段补一条绑定语义（冻结绑当前全局版、之后钉住；amend 重冻可重绑，见下）；§5 编写规则补"引用 prd 切片时版本取 frontmatter、不逐条重复 + 标哪些 AC 源自哪个 slug"。
- **DD4 · P3 `tech-plan-schema` 接线**：`External References` 引用 prd 切片时**继承 AC 钉住的 `prd_version`**（跟 AC 走、技术方案不自立版本），回指 `acceptance-schema`。方案对着钉住版设计。
- **DD5 · P5 `verify-schema` 接线（核心兑付点：对钉住版核、不对 live 最新核）**：`References Compliance` 逐项对照 prd 切片时，**对着 AC frontmatter 钉住的 `prd_version` 核**。同一迭代内 live 通常就等于钉住版（读 live 即可）；只有**回溯复核历史迭代**（PRD 此后已改版）才按 `prd_version` 读 `.archive/vN/` 核。这是钉版的兑付——保证验收对的是当初冻结那一版。
- **DD6 · references-schema 收口指针**：§7 落盘契约里"`prd_version` 如何在 AC 里记/绑定——属 R4"那条 flip 为已落地、指 `acceptance-schema`；§8 边界表 R4 行 flip 为 ✅。

## amend 重冻可重绑（钉版与既有仪式的接点）

`iteration-schema §5.3` amend（迭代内小修）把 `状态` 退回 `draft` 重新 ACK 时，若 PRD 期间恰好改了版，`prd_version` **可随重冻重绑到新的当前版**（重冻＝重新绑定当刻）。这是 R4 与既有 amend 仪式的唯一接点，R4 只加"重绑"一句、不改 amend 流程本身；改版**同步**的完整协议（重新派生 + 影响面 + 主动重冻路径）属 R5。

## 边界（不做）

- 不做 `/prd update` **改版同步** / 变更检测 / `.archive/vN/` 快照**产生**动作——R5。R4 只定钉版"怎么记 / 怎么解析 / 怎么核"，**消费**既有落盘契约（§7 已定 `.archive/vN/` 存在）、**不造**快照。
- 不做模块**合并 / 拆分 / 改名认亲**——R6。
- **不改 R3 已建的入口**（`milestone-schema §6.4/§5.3` 一字不动）、不改 `prd-split` 切分算法、不改 `references-schema` 契约**结构**（§3 登记表字段不加列，只 flip §7/§8 指针）。
- **不动 hook**：`prd_version` 是可选字段、旧 AC 无它按 legacy 放行；不给它加机械校验（守非回归、旧 AC_LIST 不被误杀）。
- 不碰 `project-digest` / `context-persistence` / `logic-protocol` / `VERSION`；**不切版**。

## 关键设计约束

- **版本单一存 frontmatter**：全局版本号只在 AC frontmatter 记一次，正文引用、P3 方案、P5 核对全跟它走、不重复——同 R3"映射单一真源"，防多处写将来漂移。
- **执行读最新、核对读钉住**（Q2=b + Q3=ii 的兑现）：P4 干活正常读 live `prd/<slug>.md`（同一迭代内 live 即钉住版，读侧规则回指 `references-schema §5 步骤 2`）；钉版的价值在 **P5 核对**（对钉住版核）与**跨迭代 / R5 改版影响面对账**，不在 P4——所以 R4 不改 P4 读法。
- **可选字段守非回归**：`prd_version` optional，非 PRD 迭代 frontmatter 逐字不变、hook 不校验它——这是 MILE-0004"不碰非 PRD 流"承诺在 R4 的落点。
