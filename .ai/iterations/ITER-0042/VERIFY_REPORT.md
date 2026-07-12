# VERIFY_REPORT — ITER-0042（PRD 先行触发加固）

> 逐条对 AC_LIST 核。hook 部分 = `pytest` 全绿 + subprocess 冒烟（确定性 auto·可靠）；规则文本部分 = 读改后正文核语义 + `git diff` 核非回归。

## 逐条

| AC | 结论 | 证据 |
|---|---|---|
| **AC1** 注入表两拍重构·来源→提取、内容→定落点 | ✅ (auto·可靠) | `logic-protocol §外部参考资料注入` 改为两拍表：第一拍「来源→取内容手段」、第二拍「内容类型→落点」；命门句"来源 ≠ 落点"落字，明写 Confluence/MCP 装 PRD 走 `prd/` 非 `api-`、`api-` 只给内容本身是 API 契约的。 |
| **AC2** 补「MCP 直读文档」入口覆盖 | ✅ (auto·可靠) | 第一拍表新增「经 MCP 直读的文档」行 + "MCP 读进来的一样要走第二拍分类落盘、绝不因来自 MCP 就跳过"；Fallback（skill 不可用人工粘贴）保留未动。 |
| **AC3** §6.4 PRD 分类闸前移为合成前必过 | ✅ (auto·可靠) | `milestone-schema §6.4` 合成协议开头加「合成前必过·PRD 分类闸（不可跳）」callout：收集 brief 后、合成三段前先判是不是大 PRD；原步 6 opener 从"仅当…才走否则跳过"改为"承分类闸判是时执行"。判定动作从末尾 opt-in 附录前移为前置必过闸。 |
| **AC4** 非回归·非大 PRD brief 流不变 | ✅ (auto·可靠) | 分类闸"判否 → 普通 brief 走常规合成到步 5 即止" = 原行为；步 1–5 正文一字未改；step 6 非回归 bullet"非大 PRD 到步 5 即止"保留。非 PRD 路径语义等价。 |
| **AC5** 新增 PostToolUse advisory 机制·与 gate 分离·fail-open | ✅ (auto·可靠) | 新增 `butler_advisor.py`（PostToolUse dispatcher，异常静默 exit 0）+ `lib/io.py` 加 `Advisory` 类型（无 verdict、不能 deny）；`butler_gate.py` 及其 rules diff 全空（分离）。冒烟3：坏 stdin → exit 0 静默（fail-open 实证）。 |
| **AC6** MILESTONE 落盘自检 rule·绝不 deny | ✅ (auto·可靠) | `rules/prd_split_reminder.py`：MILESTONE 写 + `prd/` 缺失 → 注入条件式提醒；`prd/` 存在/非 MILESTONE 目标 → 静默。冒烟1（注入 additionalContext）/冒烟2（源码写静默）exit 均 0。返回 `Advisory` 无 verdict，构造上无 deny 路径。 |
| **AC7** hook 测试·dogfood | ✅ (auto·可靠) | 新增 `test_prd_split_reminder.py`（6）+ `test_advisor_integration.py`（6，含 advisory 永不 deny/fail-open）；`pytest tests/` **109 passed**（原 97 + 新 12），现有测试零回归。 |
| **AC8** 部署 / 文档接线 | ✅ (auto·可靠) | `settings.hooks-snippet.json` 加 PostToolUse 键；`mcv-deployment §5` 首段拆两类 hook + §5.1 拷贝清单加 `butler_advisor.py` + §5.2 每键幂等合并（含升级补 PostToolUse）+ §5.3 双 hook 冒烟；`templates/hooks/README.md` 结构/机制/退出码补 advisor；`Coder/README.md` line 172 补 PostToolUse 提醒句。 |
| **AC9** scope 守恒 + 非回归门 + 分层 | ✅ (auto·可靠) | 见下"守恒 / 非回归核对"。 |
| **AC10** 说人话自检·dogfood | ✅ (auto·可靠) | advisory / PostToolUse / additionalContext / fail-open·fail-closed / 来源≠落点 首现即释（README 两套 hook 段 + mcv §5 + 提醒文案）；四件套同守。无裸英文变量。 |

## 守恒 / 非回归核对

- **scope 守恒**：`git status` change set = `.ai/*`（四件套 + 台账，迭代记账）+ `logic-protocol.md`（AC1/2）+ `milestone-schema.md`（AC3/4）+ `mcv-deployment.md`/`Coder/README.md`/`templates/hooks/README.md`/`settings.hooks-snippet.json`/`lib/io.py`（AC8/5）+ 新增 `butler_advisor.py`/`prd_split_reminder.py`/两测试（AC5/6/7）。**恰是 TECH_PLAN 影响面，无越界文件**。
- **非回归（`references-schema §9` 门自检，机器核对）**：`references-schema.md` / `prd-split.md` / `prd-update.md` / `acceptance-schema.md` / `tech-plan-schema.md` / `verify-schema.md` / `lifecycle.md` / `butler_gate.py` / `phase_gate.py` / `protected_paths.py` / `ledger_status.py` / `single_active_iteration.py` / `VERSION` — 逐一 `git diff --quiet` **全部 clean**（见 S8 核对输出）。即：契约结构 / 切分算法 / 钉版字段 / 改版认亲主流程 / 核心 P1–P5 / 现有 PreToolUse 门禁 / 版本号 一行未动。
- **milestone-schema 改动合规性**：§6.4 属 PRD 录入接线（AC3/4 明列在范围）、非"非 PRD brief 分支"本身；非 PRD 路径（步 1–5）语义等价（AC4 已核）。符合 §9"opt-in 加层叠在老路之上、不改老路语义"。
- **③ 绝不 deny 实证**：PostToolUse + fail-open 双重构造保证；测试断言无 exit 2 路径 + 三态冒烟 exit 全 0。

## 残余风险 / 诚实边界

- **hook 只兜可观测的 MILESTONE 落盘点**：纯注入路径（贴 PRD / 给链接但不开里程碑）没有可 hook 的写点，仍靠 ①②（注入表 + 分类闸）+ AI 识别，无 hook backstop。此限制 CONCEPT 已明写，非缺陷、是 PRD 识别不可机械化的固有边界。
- **提醒在每次开里程碑都会触发**：里程碑罕见（全项目史 4 个）、措辞条件式，非 PRD 一句即可判忽略；非阻塞、不改流程，噪音可忽略。
- **pytest 依赖临时 venv**：本机默认 python 无 pytest，验证用 scratchpad venv（pytest 9.1.1）跑通；不影响交付物（hook 零三方依赖，运行时只用标准库）。
- **无人测道残余**：无运行时 UI / 视觉 / 外部通道验证项。

## 结论（自评）

十条 AC 全绿（全 auto·可靠）：注入表来源解耦 + MCP 覆盖、§6.4 分类闸前移且非 PRD 等价、PostToolUse advisory 机制分离且 fail-open 绝不 deny、pytest 109 全绿零回归、部署/文档接线齐、非回归门机器核对全 clean。**自评 PASS**，待独立复核确认后收口。

---

## 独立复核结论

**干净上下文子 agent、对抗式、验证者≠实现者、只读**。结论 **APPROVE-with-nits**——十条 AC 逐条核过全成立，六个对抗点全部**证实、无 REFUTE**：③ 绝不 deny（源码全 `return 0` + 11 个畸形 stdin 实测全 exit 0，覆盖 rule 循环内抛错）、非回归 diff（14 个关键真源 + VERSION 逐一 `git diff --quiet` 全 clean，复核亲跑非信 VERIFY）、AC4 非 PRD 步 1–5 逐字未改、AC1/2 来源解耦成文无歧义、settings §5.2 每键幂等、无 AC 虚报 / 无说人话硬伤。独立复跑 `pytest tests/` = **109 passed**（system python 3.14.6，hook 零三方依赖实证）。

- **Must-Fix**：无。**Should-Fix**：无。
- **Nit 1（已改）**：`logic-protocol.md` Fallback 段落点枚举漏 `prd/`——人工粘贴一份 PRD 时未指向切分，洞 B 在 Fallback 路径残留。虽 AC2 原写"Fallback 保留不动"，但这正是本迭代要堵的入口 → **已修**：Fallback 改为"仍按第二拍内容类型分类落盘、粘贴 PRD 一样走 `prd/`"（强化 AC1 内容路由、不回归；诚实记：此处小幅超出 AC2"保留不动"的字面，方向与迭代意图一致）。
- **Nit 2（不改·记录）**：`prd_split_reminder.py:40` 若 `.ai/references/prd` 是**文件**（非目录）时 `is_dir()` 假 → 仍注入提醒。属项目异常态、非阻塞、无害；复核判无需修，保留记录。

整改后无遗留阻断。**准予收口。**
