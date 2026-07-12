# TECH_PLAN — ITER-0042（PRD 先行触发加固）

> 监督态。目标见 CONCEPT、验收见 AC_LIST，不重述。两处规则文本改（①②）+ 一套新 PostToolUse hook（③，含代码/测试/部署接线）。

## 设计决策（DD）

- **DD1 · 注入表改「两拍」结构（AC1/2）**：`logic-protocol §外部参考资料注入` 从"按来源信号一步定落点"改成"先提取内容 → 再按内容类型定落点"。表保留（读者仍要一眼看到映射），但在表前加一句总纲、表列语义从「输入信号→落点」重解为「取内容手段 / 内容类型→落点」，并显式加「经 MCP 直读的结构化文档」一行 + 点死「来源 ≠ 落点」。装 PRD 的 Confluence 因此走 `prd/` 而非 `api-`。
- **DD2 · §6.4 分类闸前移（AC3/4）**：把原步 6「大 PRD 并进分支（默认跳过）」的**判定动作**上提到合成协议开头（新步 0 或改写步 1）——"收集输入后、合成三段前，先判 brief 是不是大 PRD"。判是 → 先走 `prd-split` 再合成 + 落交叉指针；判否 → 走原步 1–5。原步 6 的**切分执行细节**保留（回指 prd-split 不复述），只是"要不要走"的开关从末尾前移到开头、从 opt-in 附录变必过闸。非大 PRD 路径逐字等价原流程。
- **DD3 · 新增独立 PostToolUse advisory 通道（AC5/6）**：**不碰** PreToolUse `butler_gate.py`（保持纯 deny、fail-closed）。新增平行的 `butler_advisor.py`（PostToolUse dispatcher，**fail-open**：任何异常静默 exit 0，advisory 绝不破坏流程）+ `rules/prd_split_reminder.py`（advisory rule）。`lib/io.py` 加 `Advisory` 轻量类型（rule_id + message，message="" 即静默）。dispatcher 收集非空 message → `{"hookSpecificOutput":{"hookEventName":"PostToolUse","additionalContext": …}}` stdout + exit 0。
- **DD4 · advisory 判据（AC6）**：`prd_split_reminder` 匹配写 `.ai/MILESTONE.md` 且 `.ai/references/prd/` 目录不存在 → 注入条件式提醒；`prd/` 已存在 / 目标非 MILESTONE.md → 静默。提醒措辞条件式（外部权威规格才需切、否则忽略），非 PRD 里程碑读一句即可判忽略。
- **DD5 · 部署接线（AC8）**：`mcv-deployment §5` 标题与首段从"PreToolUse hook 体系"扩为"PreToolUse + PostToolUse"；§5.1 拷贝清单加 `butler_advisor.py`（`rules/` 已整目录拷、自动含新 rule）；§5.2 settings 合并加 PostToolUse 键的幂等规则；§5.3 验证加一条 advisory 冒烟。`settings.hooks-snippet.json` 加 PostToolUse 条目。`templates/hooks/README.md` + `Coder/README.md`（line 172 枚举）同步。

## 影响面（文件级）

| 文件 | 改动 | AC |
|---|---|---|
| `Coder/00_System_Prompt/logic-protocol.md` | §注入表两拍重构 + MCP 直读行 + 来源≠落点 | AC1/2 |
| `Coder/20_Workflow_Lifecycle/milestone-schema.md §6.4` | PRD 分类闸从步6附录前移为合成前必过 | AC3/4 |
| `templates/hooks/lib/io.py` | 加 `Advisory` dataclass | AC5 |
| `templates/hooks/butler_advisor.py` | **新增** PostToolUse dispatcher（fail-open） | AC5 |
| `templates/hooks/rules/prd_split_reminder.py` | **新增** advisory rule | AC6 |
| `templates/hooks/tests/test_prd_split_reminder.py` | **新增** rule 单测 | AC7 |
| `templates/hooks/tests/test_advisor_integration.py` | **新增** dispatcher subprocess 测试 | AC7 |
| `templates/settings.hooks-snippet.json` | 加 PostToolUse 条目 | AC8 |
| `Coder/20_Workflow_Lifecycle/mcv-deployment.md §5` | PostToolUse 拷贝 + settings 合并 + 验证 | AC8 |
| `templates/hooks/README.md` | 结构/机制/退出码补 advisor | AC8 |
| `Coder/README.md` line 172 | hook 枚举加 advisory | AC8 |

**不碰**：`butler_gate.py` 及现有 PreToolUse rules、`references-schema` 契约结构、`prd-split` 切分算法、`prd_version` 字段、`prd-update` 改版认亲主流程、核心 P1–P5、非 PRD 流语义；不做全自动 PRD 识别；不改 `VERSION`、不切版。

## Execution Steps（可勾选）

- [ ] S1 · `lib/io.py` 加 `Advisory` 类型 → AC5
- [ ] S2 · 新建 `rules/prd_split_reminder.py`（MILESTONE 写 + prd/ 缺失 → 条件式提醒） → AC6
- [ ] S3 · 新建 `butler_advisor.py` PostToolUse dispatcher（fail-open、emit additionalContext） → AC5
- [ ] S4 · 新建 `tests/test_prd_split_reminder.py` + `tests/test_advisor_integration.py`；跑 `pytest tests/` 全绿 → AC7
- [ ] S5 · `logic-protocol §注入` 两拍重构 + MCP 行 + 来源≠落点 → AC1/2
- [ ] S6 · `milestone-schema §6.4` 分类闸前移（非大 PRD 路径逐字等价） → AC3/4
- [ ] S7 · `settings.hooks-snippet.json` + `mcv-deployment §5` + `templates/hooks/README.md` + `Coder/README.md` 部署/文档接线 → AC8
- [ ] S8 · scope 守恒 + `references-schema §9` 非回归核对（非 PRD 流/契约/切分/钉版/改版主流程 git diff 为空）+ 说人话自检 → AC9/10
- [ ] S9 · P5 独立复核（干净上下文子 agent、对抗式）→ 收口

## 验证策略

hook 部分＝确定性 auto·可靠：`pytest tests/` 全绿（新 rule 三分支 + advisory 永不 deny + 现有测试非回归）+ `butler_advisor.py` subprocess 冒烟（emit 合法 additionalContext JSON / 非 MILESTONE 静默 / 坏 stdin fail-open exit 0）。规则文本部分＝读改后正文核语义 + `git diff` 核非回归。核心对抗点：**③ 绝不 deny**（构造上 PostToolUse + fail-open，测试断言无 exit 2 路径）+ **非回归**（老 `butler_gate` 及其测试零改动、非 PRD 里程碑写结果不变）+ **来源解耦**（Confluence+PRD 落 `prd/` 非 `api-`）+ **不越界**（契约结构/切分算法/钉版/改版主流程未碰、不切版）。无人测道残余。
