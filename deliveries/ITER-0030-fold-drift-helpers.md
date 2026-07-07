# 更新说明 + 查过时两帮手定义成型 + 接线（帮手名册补齐至三）

> ITER-0030 · 迭代交付（小版本）· 收口 2026-07-07 · MILE-0003 R4 · 监督态自驱（用户"继续吧"委托，非 /dangerous；P5 起独立复核守质量）

## 本次交付目标

- R1 立起帮手名册骨架（总述 + 复核帮手），另两个帮手（更新说明 / 查过时）只在名册表占位、等 R4 补完整定义；R3 又刚把折叠维护回路 + 冷启动漂移自检接成活跃仪式，但那套回路"谁来执行"还悬着。
- R4 把另两个帮手补成完整中立定义、接到 R3 的回路上：**更新说明 `knowledge-fold`** 接收口步④折叠、**查过时 `drift-check`** 接冷启动/收口第 6 漂移不变量。**核心定位**：折叠必做（R3）不变、两帮手是**推荐唤起的 fresh-context 专职执行者**（避免主线刚干完活、快没精力时顺手折导致质量差、说明过时），opt-in 非强制。**边界**：不改 R3 强制语义、不碰读序切换（R5）/ 部署迁移（R6）/ butler 自身迁移（R8）/ 说人话（R7）。

## 已完成内容

- **新建更新说明帮手定义** `Coder/62_Extension_Agents/knowledge-fold.md`（六段式镜像 `independent-review`）：§1 一句话 + §2 中立定义表（角色=Folder / 输入=本迭代 CHANGELOG delta + 当前 `.ai/project/` / 输出=更新后 topic 文件 overwrite 禁历史层 / 禁止=改 `.ai/project/` 外 · 叠历史 · 凭空编 · 逐字复制 / 隔离=fresh-context G1 / **权限=只准写 `.ai/project/`**）+ §3 触发（收口步④文件夹态、折叠必做时推荐唤）+ §4 定向折叠路由（承 `project-digest-schema §6`）+ §5 输出衔接 + §6 诚实兜底（回指 G2）。
- **新建查过时帮手定义** `Coder/62_Extension_Agents/drift-check.md`（同款六段）：角色=Checker（**不是** Folder）/ 输入=`.ai/project/` + 真实代码 + 近期 CHANGELOG delta / 输出=**漂移清单**（哪几处对不上、哪条 delta 漏折、有无被取代结论残留，带证据指针）/ **权限=只读** / 隔离=fresh-context；§3 触发接第 6 不变量（冷启动/收口抽查、单文件项目 N/A）；§5 漂移清单落 `.ai/references/insight-drift-check.md`（同复核帮手 `insight-*` 命名族）。
- **`overview.md §2` 名册表 co-edit**：更新说明 / 查过时两行状态 🔜 R4 落地 → ✅ 本轮立，"只准碰"列与定义文件权限逐字一致；删占位说明句、替换为三帮手接线摘要句。名册从"1 已立 + 2 占位"成"**3 帮手均完整定义**"。
- **最小回指接线**（只加可发现性、不重复正文）：`iteration §5.5 步④` 文件夹态折叠句加"推荐唤 `knowledge-fold.md` 帮手 fresh-context 执行、起不了则主线自折并如实标注（G2）、不因此跳过折叠"；`context-persistence 第 6 不变量` 加"推荐唤 `drift-check.md` 帮手抽查、起不了则主线自查（G2）"。两处 R3 强制正文（折叠必做 / 第 6 不变量）未删改。
- **`Coder/README.md` 注册**：目录树 `/62_Extension_Agents` 补两文件 + 分文件说明更新为"住册三帮手"（回指真源）。

## 关键变更 / 用户可感知变化

- 帮手名册从 1 个完整帮手（复核）扩成 **3 个**（复核 / 更新说明 / 查过时）——R3 建好的折叠回路 + 漂移自检回路，现在都有了专职的隔离执行者定义可唤。
- **opt-in 非强制是核心设计约束**（不是随口一提）：折叠本身 R3 已定"必做"，但"谁折"必须是**推荐**唤帮手、**不能**写成"必须唤帮手"——否则起不了子 agent 的环境（含 butler 仓自己）会在收口时卡死。接线两处 + 两帮手 §诚实兜底逐处保证"推荐唤 + 起不了则主线自做并如实标注（G2）、绝不冒称已由帮手做、绝不因此跳过折叠/自检本身"。
- 帮手仍**不下发到项目**（承 R1）：定义只住 butler `62_Extension_Agents/`，目标项目用时读定义、临时起干净子 agent，不存副本、不日久漂移。权限（只写 `.ai/project/` / 只读）本轮靠**契约约定 + G2 诚实兜底**，工具层硬拦留后续。
- 向后兼容：不改 R3 折叠必做 / 第 6 不变量强制性、未切读序第一读（仍 PROJECT.md，切 00_INDEX 是 R5）、未加部署种子（R6）、未迁移 butler 自身（R8）、未切版；未动状态机 / 四件套 / hook / 迭代里程碑双层。

## 高层影响范围

- 新增（2 帮手定义文件）：`Coder/62_Extension_Agents/knowledge-fold.md`、`drift-check.md`。
- 改（章节级，4 规则文件）：`62_Extension_Agents/overview.md §2`（名册表 co-edit）、`20_Workflow_Lifecycle/iteration-schema.md §5.5 步④`、`40_Context_Management/context-persistence.md 第 6 不变量`、`Coder/README.md`（注册）。
- 收口前滚（本迭代自身，单文件态按需）：`.ai/PROJECT.md` 帮手名册条——从"1 已立 + 2 占位"更新为"3 帮手均完整定义 + opt-in 非强制"。
- 没碰（R4 边界）：R3 强制正文（`iteration §5.5 步④` 必做折叠 / `context-persistence 第 6 不变量`）、`context-persistence §冷启动读序`第一读（R5）、`mcv-deployment` / `migrations/`（R6）、butler 自身 `.ai/PROJECT.md → .ai/project/` 实体迁移（R8）、`presentation-protocol` / `artifact-style`（R7）、`VERSION`、状态机 / 四件套 / hook。

## 验证方式与结果摘要

- **8/8 AC 通过**，全 **auto·可靠**（规则文档：读正文确认 + `git`/`grep` 核守恒，确定性可复现）；无人测道残余。
- P5 **独立复核**（fresh-context 子 agent，验证者≠实现者）：**核心对抗点（opt-in 非强制）逐处过关**——接线 2 处 + 两帮手 §诚实兜底 2 处均"推荐唤"非"必须唤"、G2 兜底在；全仓 `grep 必须唤\|强制唤\|必须起` 0 命中；R3"必做"计数未减；G1–G4 两文件 0 重写（只回指 overview §3）；权限声明与名册表逐字一致；scope 未越 R5/R6/R8——**APPROVE，0 Must Fix、0 Should Fix**。
- 1 Nit（不阻断）：drift-check §5 输出落点文件名 `insight-drift-check.md` 系实现者自拟（AC 只说"落 `.ai/references/`"），与复核帮手 `insight-independent-review.md` 同族、命名合理，无需改。
- 守恒核对：`git status` 改动集=2 新增 + `overview`/`iteration`/`context-persistence`/`README` + `.ai/` 台账，无 rename、无越界（`mcv`/`migrations`/`VERSION`/butler `.ai/project/` 均未触）。

## 已知剩余风险 / 延后事项

- **opt-in 措辞依赖纪律**：折叠必做（R3）不变、"谁折"是推荐唤帮手；靠"推荐唤 + 起不了主线自做（G2）、绝不跳过折叠/自检本身"的显式兜底兜住无子 agent 环境。后续改动若误把某处写成"必须唤帮手"即会砸起不了子 agent 的环境收口——已由本轮两处"推荐"措辞 + 两 §诚实兜底 + P5 对抗核过兜底，属受控。
- **权限本轮靠约定 + G2**（承 R1）：knowledge-fold 只写 `.ai/project/` / drift-check 只读是契约约定、无工具层硬拦；硬拦留后续可选增强。
- 收口非 hook 门禁，butler 仓不 live 跑自己的 hook（既有设计约束）；本迭代不新增 hook 需求。
- 本轮按惯例收口即提交，**未推送、未切版**；MILE-0003 仍 active，剩 R5/R6/R7/R8（v2.0.0 切版在 R8），待用户指令。

## 引用（只引用路径，不嵌全文）

- 归档四件套 + 切片：`.ai/iterations/ITER-0030/CONCEPT.md` / `AC_LIST.md` / `TECH_PLAN.md` / `VERIFY_REPORT.md` / `CHANGELOG.md`
- 新增：`Coder/62_Extension_Agents/knowledge-fold.md`、`drift-check.md`
- 改动：`Coder/62_Extension_Agents/overview.md`、`Coder/20_Workflow_Lifecycle/iteration-schema.md`、`Coder/40_Context_Management/context-persistence.md`、`Coder/README.md`
- 设计基准（预研，未追踪）：`docs/research/MILE-0003-agent-doc-design.md`（更新说明 / 查过时两帮手职责 + 权限表）
