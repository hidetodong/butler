# PRD 先行触发加固——修 Confluence/MCP 入口漏切 + 里程碑并进闸前移 + MILESTONE 落盘自检

> ITER-0042 · 独立迭代（MILE-0004 已收、无所属里程碑，仿 ITER-0035 先例）· 监督态 · 修已发布 MILE-0004 的实战缺陷 · 不切版（MINOR 发布待放行）

## 一句话

MILE-0004 建成的「PRD 先行」全生命周期链，实战里被一条真实通道穿透了：用户给 Confluence 文档地址、AI 经 MCP 直读当 `/milestone` brief，结果 **MILESTONE.md 合成了，但从没提切分、`references/prd/` 从没建**——PRD 的逐字规格蒸发进了上下文、没落盘。根因是整条切分链**软触发零强制**，而「Confluence + MCP 直读 + /milestone」恰好同时穿过三层最薄的纸。本迭代三层一起补：把软触发**挪到难错过的位置** + 给唯一可观测的落盘点**加一道非阻塞自检**。

## 背景（缺口在哪，为什么现在做）

实战复现的流程：给 Confluence 地址 → AI 用 mcp-atlassian 读进上下文 → 合成 `MILESTONE.md` → 完事。全程没有任何机制叫停。拆成三个独立的洞：

- **洞 A · 里程碑并进分支是「默认跳过」**：`milestone-schema §6.4 步 6` 明写「仅当 brief 是逐字权威规格才走，否则跳过本步」。默认动作 = 跳过。要触发切分，AI 得主动①记得步 6 存在 ②把 Confluence 内容**认定为**大 PRD（而非普通 brief 素材）③动手——三个软开关，走「读链接给我建里程碑」这条阻力最小的路时一个没翻。
- **洞 B · 注入表按「来源」路由、不按「内容」**：`logic-protocol.md §外部参考资料注入` 的表按输入信号排。一个装着 PRD 的 Confluence 链接**同时命中两行**——「Confluence 链接 → `api-<name>.md` 扁平」和「大 PRD → `prd/` 切片」——而「Confluence 链接」是更字面的匹配，天然赢过「这内容算不算 PRD」的语义判断。更糟：用户用的是 **MCP 直读**，连那行假设的 `confluence-api-extractor` skill 通道都没走，等于内容从一个**规则没覆盖的入口**溜了进来。
- **无 hook 兜底 · 漏了静默**：P1–P3 产物链拦得住是因为有 PreToolUse hook（`phase_gate` 等）。**references/PRD 这条路上一个 hook 都没有**，「外部权威规格进了项目、但 `references/` 是空的」这件事没有任何机器会叫。软规则 + 零强制 + 恰好走了没覆盖的入口 = 缺陷静默发生。

一句话根因：**P1–P3 靠 hook 立着，PRD 切分只靠散文立着；散文在「顺手把链接读进来建个里程碑」的压力下必然被绕过。**

## 做什么（DD）

- **DD1 · 注入表按内容分类（改 `logic-protocol.md §外部参考资料注入`）**：把路由从「按来源信号」改成两拍——**先按来源提取**（Confluence/MCP/MasterGo/文件都是取内容的手段），**再按内容类型定落点**（逐字权威规格 PRD → `prd/` 切分；API 契约 → `api-` 扁平；设计规格 → `design-`；分析报告 → `insight-`）。补上「**MCP 直读的文档**」这一入口（不再假设 Confluence 只走 skill）——凡经 MCP 读进来的结构化文档，同样过这道内容分类。明确写死：**来源 ≠ 落点，落点由内容类型决定**。
- **DD2 · 并进闸前移（改 `milestone-schema §6.4`）**：把「是不是大 PRD」的判断从**末尾跳过式的步 6 附录**，提成**合成 MILESTONE 之前的必过分类检查点**：任何外部结构化文档进来当 brief（不论来自对话、`origin/`、还是 MCP 直读），**合成路线图之前先过一道分类闸**——判定是大 PRD 就先经 `prd-split` 切、再合成；判定不是就照旧到步 5 即止。把「PRD 分类」从可选分支变成前置动作。
- **DD3 · 新增 PostToolUse advisory hook（唯一可观测落盘点的非阻塞兜底）**：新增一套 **PostToolUse** hook（与现有 PreToolUse `butler_gate` 分离、老 gate 一行不动）——写 `.ai/MILESTONE.md` 后，若 `.ai/references/prd/` 不存在，经 `hookSpecificOutput.additionalContext` 向模型注入一句**条件式自检**（"此里程碑 brief 若源自外部权威规格，先经 prd-split 落 `references/prd/` 再合成；若只是对话/普通 brief，忽略本提醒"）。**非阻塞是构造保证的**（PostToolUse 在写之后跑），绝不 deny、绝不改写操作结果。配套：新 dispatcher + rule + pytest + `mcv-deployment §5` 部署接线 + settings 片段 + README 枚举同步。

## 边界（不做）

- **不改 R1–R6 已建的主体**：`references-schema` 契约结构 / `prd-split` 切分算法 / `prd_version` 钉版字段 / `prd-update` 改版认亲主流程——一律不动，本轮只修**触发接线**，不碰切分/改版逻辑本身。
- **不做全自动 PRD 识别**：识别「这算不算 PRD」本质是语义判断、不可机械化；DD1/DD2 是把软触发**挪到更难错过的位置**，DD3 只兜**唯一可观测的 MILESTONE 落盘点**。纯注入路径（贴 PRD / 给链接但不开里程碑）没有可 hook 的写点，仍靠 DD1 + AI 识别，无 hook backstop——本迭代**如实承认这条限制**、不假装 hook 能全覆盖。
- **不碰非 PRD 流**（守 `references-schema §9`）：对话录入 / `origin/` 非 PRD brief 合成 / 扁平态注入 / 核心 P1–P5 状态机——语义一行不变。DD3 的 advisory **绝不 deny**（一 deny 就会拦正常的非 PRD 里程碑写 = 回归）。
- **不切版**：加 PostToolUse hook = 新能力 + 需 `[sync-hooks]`/settings 合并迁移 → 判 **MINOR（v2.2.0）**；但切版是收口后的独立 `chore(release)` 发布动作，待用户放行，不混进本迭代。

## 关键设计约束

- **来源与落点解耦**：这是洞 B 的病根——修法就是让落点只由内容类型决定，任何来源（含 MCP 直读）都先提取、再分类。
- **③ 必须 advisory、绝不 block**：PostToolUse + `additionalContext` 是唯一能「非阻塞 + 让模型看到」的正道（PreToolUse 的 `permissionDecisionReason` 在 allow 时不进模型、也无 `additionalContext`）。老 `butler_gate`（deny-based PreToolUse）保持纯净、不掺 advisory。
- **提醒是条件式、低频、可秒忽略**：里程碑本身罕见（全项目史 4 个），且提醒措辞让非 PRD 里程碑一句话即可判定忽略——false-positive 成本趋零，不构成噪音、不改流程。
- **诚实标注 hook 覆盖边界**：hook 只兜 MILESTONE 落盘点，纯注入路径无 backstop——写进文档，不制造「全覆盖」的错觉。
