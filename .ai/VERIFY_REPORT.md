# VERIFY_REPORT — ITER-0033（MILE-0003 R7）

> 监督态自驱（非 `/dangerous`）· 全为规则文档改动，验证=读改后正文确认 + `git diff`/`git grep` 核守恒，确定性可复现（**auto·可靠**）· 无人测道残余。

## 验收结果（逐 AC）

- [x] **AC1 ✓** `artifact-style §2` 已改写为「说人话三条硬标准」，三条各有名字 + 一句话判据（术语先解释 / 比喻要落地 / 别让英文·变量裸奔），line 17 声明"跨对话与文档通则"、line 19 声明"单一真源"；line 28 交叉引用 §4.3 去重、不冗余。
- [x] **AC2 ✓** `git grep "比喻\|类比" HEAD -- Coder/ templates/` pre-R7 零命中——"比喻要落地"确为全仓新增，非旧条改名。
- [x] **AC3 ✓** frontmatter `scope`（line 4）+ §1（line 11）从"四件套字段正文"扩到"所有面向人落地文档"，明列四件套 + 交付总结 + 知识文件夹 + handoff；旧"仅四件套"被取代非并列。
- [x] **AC4 ✓** §8（line 122）从"收口前自检"扩为"发长文 / 收口前自检"，含逐条扫三条 + 保留反啰嗦/超 2 层嵌套检查，适用所有面向人长文档。
- [x] **AC5 ✓** `presentation-protocol` 新 §7（line 55–61）只引用 `artifact-style §2`、显式"不重述定义"；三条完整定义 header 仅在 artifact-style 出现（git grep 证）。顺移编号后引用全解析、无悬空：(见 §9)、§3–§7 均对，旧 (见 §8)/§3-§6(指本文件) 已清；line 69/73/76 的 §8 均指外部 `delivery-summary §8`（非本文件节号）。
- [x] **AC6 ✓** `rule-card.md` 对话条 + 产物条均同步收录三条、标"真源 artifact-style §2"、压缩不新增语义、与 §2 不漂移。
- [x] **AC7 ✓** `README` line 105（presentation-protocol 条增说人话应用）+ line 146（artifact-style 条改"面向人落地文档 + 三条真源"），两处与改后文件自洽。
- [x] **AC8 ✓** `git status` 改动集=4 规则文件（artifact-style / presentation-protocol / rule-card / README）+ `.ai/` 台账与四件套 + `.ai/PROJECT.md` 前滚；无 `identity`/`delivery-summary`/四 schema/hook/`VERSION`/`CHANGELOG`/rename（`^R`=0）/`migrations/` 新增 / R2·R3·R5·R6 目标语义改动。
- [x] **AC9 ✓** dogfood 扫查已跑（见下）；四件套自身命中的反面词逐条改过。

## dogfood 自检（AC9）

- 独立复核抽查四件套，命中标准一自列的反面词 3 项，逐条改：
  - `BLUF`（CONCEPT / AC_LIST）→ 改"结论先行"。
  - `fresh-context 子 agent`（TECH_PLAN）→ 改"干净上下文的子 agent[不带本轮记忆去复核]"。
  - `dogfood`（CONCEPT / AC_LIST / TECH_PLAN）→ 首现加"自己先照做"大白话解释。
- 命中即改，改后四件套自身守三条；本 VERIFY + 交付总结同守三条书写。

## 独立复核（P5·验证者≠实现者）

- 干净上下文子 agent 对抗式逐 AC 核对：初判 **REQUEST-CHANGES**，2 条 Must Fix 均为"收口步该做未做"——MF1（VERIFY 未写 R7）、MF2（四件套 dogfood 反面词未改）；规则改动本身 AC1–AC8 全 confirm。
- 对抗点全过：**单一来源真单一**（三条完整定义只在 `artifact-style §2` 一处、别处均引用或压缩指针）、**§7 边界矛盾已消解**（`artifact-style §7` line 119 从"不管对话层"收窄为"不管对话层呈现结构" + 显式例外挑明三条为跨层通则）。
- MF1（本 VERIFY）/ MF2（dogfood 反面词已改）已在本收口步修复，复核放行。

## scope 守恒（守恒核对）

- `git status` 改动集与 AC8 列名一致；`^R`（rename）=0；`migrations/` 零新增；`VERSION`/`CHANGELOG` 未动（切版属 R8）；hook 未动。
- **未越界**：`identity.md` 未触、`delivery-summary.md` 字段与散文定性未动、四件套字段结构（四 schema）未动、R2 `.ai/project/` 结构契约 / R3 折叠语义 / R5 读序 / R6 部署迁移目标均未触。
- 6 不变量自检（收口仪式第 5 步）：butler 自身仍单文件态、第 6 条知识文件夹漂移 N/A；其余 5 条随收口翻台账时一并核过（current↔状态 / 至多一 active / closed 有交付 / closed 有归档 / 路线项对账）。

## 已知剩余风险 / 延后事项

- 说人话三条落规则层已定、可自检；真正"输出更好懂"要靠后续每次迭代照做 + 收口自检兜底（书写质量不做 hook 机械门禁，见 `artifact-style §7`）。
- 本轮按惯例收口即提交，**未推送、未切版**；MILE-0003 仍 active，剩 R8（butler 自身 dogfood 迁 `.ai/project/` + 切 v2.0.0），待用户指令。

## 引用（只引用路径，不嵌全文）

- 归档四件套 + 切片：`.ai/iterations/ITER-0033/CONCEPT.md` / `AC_LIST.md` / `TECH_PLAN.md` / `VERIFY_REPORT.md` / `CHANGELOG.md`
- 改动：`Coder/20_Workflow_Lifecycle/artifact-style.md`、`Coder/00_System_Prompt/presentation-protocol.md`、`templates/rule-card.md`、`Coder/README.md`
- 相关契约：`artifact-style.md §2`（说人话三条真源）、`presentation-protocol.md §7`（对话层引用）
