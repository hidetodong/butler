---
description: 只读聚合当前项目的 Butler 进度——里程碑、迭代、Goal、验收、执行、验证、风险一页看完
argument-hint: "[brief=一行摘要 | 留空=完整结构化报告]"
---

你正在执行 Butler 的**项目进度聚合**动作。本命令是**只读聚合器**——读当前项目 `.ai/` 下的状态文件，按固定格式输出结构化进度报告。**不修改任何文件、不执行任何写入**（守只读红线）。

> **路径约定（本命令可在任意项目里运行，当前目录不一定是 butler 仓）**：下文引用的 `Coder/…` 都是 **butler 规则仓库**里的文件，一律相对 `$BUTLER_PATH` 解析。读取对象是**当前项目**的 `.ai/` 台账。

> **项目根硬门**：读台账前先按 `$BUTLER_PATH/Coder/20_Workflow_Lifecycle/mcv-deployment.md §0.1` 解析 `PROJECT_ROOT`。下文"当前项目"一律指该绝对路径。

## 第 0 步（强制）先确认当前项目已接 butler

检查 `$PROJECT_ROOT/.ai/` 是否存在：
- **有 `.ai/`** → 继续。
- **没有 `.ai/`** → 一句话告诉用户「当前项目没接 butler，进度报告需要 `.ai/` 台账；请先 `/butler:init` 部署基地车」。不报错、不空跑。

## 按 `$ARGUMENTS` 路由

### 分支 A ─ 以 `brief` 开头 → 一行摘要

读 `.ai/task-state.md`，提取当前迭代号、阶段和状态，输出一行：

```
<项目名> │ <迭代号 或 "无活跃迭代"> │ <阶段 或 "—"> │ <状态>
```

结束。不读其他文件。

### 分支 B ─ 留空（或其他参数）→ 完整结构化报告

按下面 9 个段落（§1–§9）**依次**读取并输出。每段缺失数据时如实标注「无」或「不适用」，**不编造、不推测**。

先运行 `python3 "$BUTLER_PATH/tools/project-config/config.py" resolve --project-root "$PROJECT_ROOT"`。成功时后续报告复用这一个 JSON 结果，不另行解析配置；失败时项目配置标为错误，危险/独立复核/偏好均显示 fail-closed，报告仍可只读聚合其余台账。`legacy_conflicts` 非空必须在 §1/§8 亮牌。

---

#### §1 项目概况

| 项 | 值 |
|---|---|
| 项目 | 从 `git remote -v` 取 origin URL 的 repo 名；无 remote 则取目录名 |
| Butler 版本 | 优先读 `$PROJECT_ROOT/CLAUDE.md` / `AGENTS.md` 的 managed Butler 版本戳（两者冲突必须亮牌）；无戳再读 `$PROJECT_ROOT/VERSION`；都没有写「未知」 |
| 部署状态 | `.ai/` 存在即 ✅ |
| 项目配置 | resolve 的 `source`、`dangerous`、`independent_review`、`preference`、`profiles` 与 `legacy_conflicts` |

#### §2 里程碑

读 `.ai/MILESTONES.md`：
- `current` 指针非 `none` → 报里程碑号、标题、状态、开启日期、含迭代数
- `current: none` → 报「当前无活跃里程碑」
- 附候办区数量（有待办区时）

#### §3 当前迭代

读 `.ai/task-state.md`：
- 当前迭代号（非「无 active」时）
- 当前里程碑归属
- 当前阶段（P1–P5 + 阶段名）
- 状态描述
- 下一动作

无活跃迭代时整段报「当前无活跃迭代」。

#### §4 Goal 状态

读 `.ai/task-state.md` 的 Goal Calibration 表：
- 有信号行 → 逐条列 ID、信号类型、状态、Goal 影响、路由
- 表空或标注 N/A → 报「当前无未闭合运行时信号」

再按 `goal-contract.md §3` 的推导优先级，从已有事实派生 Goal 状态（active / at-risk / blocked / completion-candidate / complete / abandoned），回声派生结果和一句话理由。

#### §5 验收进度

读 `.ai/AC_LIST.md`（不存在则报「无验收标准文件」）：
- 统计总条数
- 按状态分组计数（已确认 / 待验证 / 未通过 / 其他）
- 若文件头部有 `状态: ack-frozen`，标注「AC 已冻结」

#### §6 执行进度

读 `.ai/TECH_PLAN.md`（不存在则报「无技术方案文件」）：
- 方案状态（pass / draft / revise / 其他）
- 执行步骤：已勾 / 总数（从 `[x]` / `[ ]` 计数）
- 无 TECH_PLAN 时报「不适用（可能尚在 P1/P2）」

#### §7 验证状态

读 `.ai/VERIFY_REPORT.md`（不存在则报「无验证报告」）：
- 自动道状态
- 人测道状态
- 整体置信档
- 未完成的验证项数

#### §8 风险与阻塞

汇总来源：
- `.ai/task-state.md` Goal Calibration 表中 status 非 closed 的信号
- `.ai/TECH_PLAN.md` 的 verdict 非 pass
- `.ai/VERIFY_REPORT.md` 中未通过的验证项

有风险 → 逐条列出，标来源。无风险 → 报「当前无已知风险或阻塞」。

#### §9 最近变更

读 `.ai/01_CHANGELOG.md`（不存在则跳过此段）：
- 取最近 5 条变更条目
- 每条一行：日期 + 类型 + 描述

---

## 输出格式要求

1. **固定段落顺序**：§1–§9 始终按此顺序输出，不跳段（缺数据标注「无」而非省略段落）。
2. **表格优先**：§1 用表格，§5/§6/§7 有可量化数据时用表格或进度条。
3. **状态 emoji 一致**：✅ 完成/通过、⏳ 进行中/待验证、❌ 未通过/失败、⚠️ 风险/注意、— 不适用。
4. **不解释 butler 概念**：报告是给已在使用 butler 的用户看的，不需要解释什么是 P1/P5、AC 等。
5. **报告开头一行总览**：`<项目名> │ <迭代号 或 "无活跃迭代"> │ <阶段 或 "—"> │ <Goal 状态 或 "—">`

## 收尾

输出完整报告后不再附加额外说明。报告本身就是最终产物。
