# ITER-0011 对话输出呈现协议

## 本次交付目标
解决一个使用体验问题：butler 每次输出方案时格式不固定——标号忽 `ABC` 忽 `123` 忽 `a)`，且开场堆大段概念、不易读。补一条常驻的「对话输出呈现协议」，把 P1-P3 的方案 / 分析 / 选项类对话输出统一为「结论先行 + 统一标号 + 选项表格」，默认固定 + 弹性、仅管较长输出，与现有 `delivery-summary §8`（P5 交付摘要散文化）分场景共存。

## 已完成内容
- **新增协议 SSOT** `Coder/00_System_Prompt/presentation-protocol.md`（8 节）：目标、适用范围（适用 P1-P3 较长输出 / 豁免简短问答·澄清·进度·P5 摘要）、结论先行（BLUF）、统一标号（可执行口径：无序 `-`、有序 `1.`、禁字母标号作层级）、选项表格化、概念后置 + 收尾下一步、弹性条款、与 §8 边界 + 标准骨架样例。
- **入口接线**：`identity.md §2` 加指针引用；`logic-protocol.md §1.1` 读取顺序把协议纳入 00_System_Prompt 序列（第 3 项）；`Coder/README.md` 目录结构 + 读取顺序（重编号 1-8）+ 规则目录说明三处登记。
- **高注意力区落地**：`templates/rule-card.md` 新增精简「## 输出呈现」节——规则卡会内联到目标项目 CLAUDE.md，确保协议被 AI 实际读到、不是「写了但不遵守」。
- **边界互指 + 指南**：`delivery-summary.md §8.5` 加分工句（过程结构化、交付散文化）；`HUMAN_GUIDE.md §1` 加统一呈现格式说明。

## 关键变更 / 用户可感知变化
- 从现在起，AI 呈现方案 / 选项 / 分析时会**结论先行**（开头一句话结论/建议）、**标号统一**（不再 `ABC`/`123`/`a)` 混用）、**多方案用表格**、**结尾给下一步**。
- 这套格式是**默认固定 + 弹性**：简短问答、纯澄清、进度汇报不强行套骨架，避免轻量交流变重。
- 与 P5 交付摘要**分工**：交付摘要继续走 §8 散文口径，本协议只管过程中的方案呈现，两者不打架。
- 协议放在最高注意力区（`00_System_Prompt/` + rule-card），更可能被实际遵守。

## 高层影响范围
- 新增：`Coder/00_System_Prompt/presentation-protocol.md`。
- 改：`Coder/00_System_Prompt/{identity,logic-protocol}.md`、`Coder/README.md`、`templates/rule-card.md`、`Coder/20_Workflow_Lifecycle/delivery-summary.md`（§8.5 边界句）、`HUMAN_GUIDE.md`。
- 零改动护栏：产物链四件套 schema、hook 体系（phase_gate/ledger_status）、`VERSION`/`CHANGELOG.md`、iteration/milestone/versioning-schema、各扩展模块、`deliveries/` 历史与 ITER-0010 的 HTML 模板。

## 验证方式与结果摘要
- AC1–AC9（协议）：`grep` 确认 8 节齐全、适用/豁免清单、标号可执行口径、骨架样例，且样例自身遵守协议（自洽）。
- AC10–AC13（接线 + 高注意力区）：`grep -l` 命中 identity/logic-protocol/README/rule-card；README 读取顺序重编号 1-8 无重号。
- AC14–AC16（边界 + 一致性）：分工句在 protocol / delivery-summary / rule-card 三处一致、无矛盾。
- AC17（护栏）：`git status` + `git diff --stat` 确认护栏文件零改动。
- 详见 `.ai/iterations/ITER-0011/VERIFY_REPORT.md`。

## 已知剩余风险 / 延后事项
- 协议靠会话起始读取 + 遵守，无 hook 强制——与 identity/logic-protocol 同源同险。
- 「较长输出 vs 豁免」边界靠语义判断，有模型自由度——用「默认套 + 豁免清单」兜底。
- 版本：本轮不发版，ITER-0011 累积到下次切版，预计 MINOR。

## 引用
- `.ai/iterations/ITER-0011/CONCEPT.md`
- `.ai/iterations/ITER-0011/AC_LIST.md`
- `.ai/iterations/ITER-0011/TECH_PLAN.md`
- `.ai/iterations/ITER-0011/VERIFY_REPORT.md`
- `Coder/00_System_Prompt/presentation-protocol.md`（协议 SSOT）
