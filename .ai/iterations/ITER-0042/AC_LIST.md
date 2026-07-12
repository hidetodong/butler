---
状态: ack-frozen
ACK 日期: 2026-07-12
迭代: ITER-0042
里程碑: —（MILE-0004 已收、独立迭代）
---

# AC_LIST — ITER-0042（PRD 先行触发加固）

> 监督态。三层修触发接线：①注入表按内容分类（规则文本）②里程碑并进闸前移（规则文本）③新增 PostToolUse advisory hook（代码 + 测试 + 部署接线）。验证 = 读改后正文核语义 + `git diff` 核非回归 + `pytest` 跑 hook 测试（auto·可靠）。**待 ACK 冻结后方可进 P4。**

## 块1 · 注入表按内容分类（洞 B）

- **AC1（`logic-protocol §外部参考资料注入` 重构为「来源→提取、内容→定落点」）**：注入表/说明改为两拍——先按来源提取内容（Confluence/MCP/MasterGo/文件皆为取内容手段），再按**内容类型**定落点（逐字权威规格 PRD → `prd/` 切分；API 契约 → `api-`；设计规格 → `design-`；分析报告 → `insight-`；其他 → `<name>`）。成文点死「**来源 ≠ 落点，落点由内容类型决定**」。装 PRD 的 Confluence 不再默认落 `api-` 扁平。
- **AC2（补「MCP 直读文档」入口覆盖）**：注入规则显式覆盖「经 MCP 直读进来的结构化文档」——不再假设 Confluence 只走 `confluence-api-extractor` skill；凡 MCP 读进来的同样过 AC1 的内容分类。原 Fallback（skill 不可用时人工粘贴）保留不动。

## 块2 · 里程碑并进闸前移（洞 A）

- **AC3（`milestone §6.4` 把 PRD 分类从跳过式步6附录前移为合成前必过闸）**：`§6.4 合成协议`改为——任何外部结构化文档当 brief（对话/`origin/`/MCP 直读），**在合成路线图之前先过一道 PRD 分类闸**：判定大 PRD → 先经 `prd-split` 切 `references/prd/` 再合成；判定非 PRD → 照旧到步 5 即止。「PRD 分类」由末尾 opt-in 附录变为前置动作。切分机制仍以 `prd-split` 为准、此处不复述（回指）。
- **AC4（非回归·非大 PRD brief 流不变）**：非大 PRD 的普通 brief 合成路径（步 1–5）语义与改前一致——分类闸判否即等价于原流程，不新增阻塞、不改产物。`milestone-schema` 除 §6.4（必要时 §6.5 命令说明）外不动。

## 块3 · PostToolUse advisory hook（洞 C·无 hook 兜底）

- **AC5（新增 PostToolUse advisory 机制·与 `butler_gate` 分离）**：新增独立 PostToolUse dispatcher（不改现有 PreToolUse `butler_gate.py` 及其 rules），承载「放行 + 向模型注入 `additionalContext`」的 advisory 能力；零三方依赖、advisory 自身出错 fail-open（绝不因 advisory 异常而阻塞或报错升级）。
- **AC6（MILESTONE 落盘自检 rule）**：新 rule——匹配 Write/Edit/MultiEdit 写 `.ai/MILESTONE.md`，若 `.ai/references/prd/` 不存在 → 经 `hookSpecificOutput.additionalContext` 注入**条件式自检提醒**（brief 若源自外部权威规格则先 `prd-split` 落盘再合成、否则忽略）；`references/prd/` 已存在或目标非 MILESTONE.md → 静默不注入。**绝不 deny、绝不阻塞**（非 PRD 里程碑写结果与加 rule 前逐字一致）。
- **AC7（hook 测试·dogfood）**：新 rule 有 pytest 覆盖——`references/prd/` 缺失→注入 advisory、存在→静默、非 MILESTONE 目标→静默、advisory 永不 deny；现有 hook 测试全绿（非回归）。
- **AC8（部署 / 文档接线）**：`mcv-deployment §5` Hook 注入节补 PostToolUse dispatcher 拷贝 + settings 合并（新增 `PostToolUse` 键，幂等去重）+ 冒烟自检加一条；`templates/settings.hooks-snippet.json` 加 PostToolUse 条目；`Coder/README.md`（line 172 hook 枚举 + 若引入新文件的目录注册）同步。

## 块4 · 守恒 · 非回归 · 说人话

- **AC9（scope 守恒 + 非回归门 + 分层）**：改动集限于 `logic-protocol.md §注入`（AC1/2）+ `milestone-schema.md §6.4`（AC3/4）+ `templates/hooks/`（新 PostToolUse dispatcher + rule + 测试，AC5–7）+ `templates/settings.hooks-snippet.json` + `mcv-deployment.md §5` + `README.md`（AC8）。守 `references-schema §9` 非回归——对话录入 / `origin/` 非 PRD brief 合成 / 扁平态注入 / 核心 P1–P5 状态机 / `references-schema` 契约结构 / `prd-split` 切分算法 / `prd-update` 改版认亲主流程 / `prd_version` 字段的**语义** `git diff` 为空（除本 AC 明列的 PRD 相关触发接线改动）。不切版、不改 `VERSION`。分层不破坏（SOP Core `00`/`20` + templates + README）。
- **AC10（说人话自检·dogfood）**：改动的规则文本过说人话三条（术语先解释 / 比喻落地 / 别让英文·变量裸奔）；本迭代四件套同守。advisory / PostToolUse / additionalContext / 来源解耦 等首现带解释。
