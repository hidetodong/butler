---
description: 给当前迭代的改动做代码 / 产物复核——默认当前上下文快速自检，或另起干净上下文做更狠的独立复核
argument-hint: "[independent=另起 fresh 子 agent 独立复核（验证者≠作者）| 留空=当前上下文快速自检]"
---

你正在执行 butler 的 **代码 / 产物复核**动作。本命令是**薄壳路由器**——只做三件事：① 保证把对的审查规则读进上下文，② 按参数选复核强度，③ 委托真源规则执行。**具体审查口径（变更识别 / 多维评审 / 评级 / 闭环）一律以被指向的规则文件为准，本文件不复述**（守 butler DRY 红线）。

> **路径约定（本命令可在任意项目里运行，当前目录不一定是 butler 仓）**：下文引用的 `Coder/…` 都是 **butler 规则仓库**里的文件，一律相对 `$BUTLER_PATH`（`setup.sh` 全局安装时写入的环境变量；编辑 butler 仓本身时就是仓库根）解析。复核**对象**是**当前项目**的迭代产物与代码改动（`.ai/AC_LIST.md`、`git diff` 等），绝不是 butler 仓。

## 第 0 步（强制）先确认有东西可复核
复核建立在**当前项目的迭代产物**之上。开跑前先看当前目录有没有 `.ai/AC_LIST.md`（验收尺子）与待审改动（`git diff` 或本轮变更文件）：
- **都在** → 正常往下走。
- **没有 `.ai/`（当前项目没接 butler）或没有进行中的迭代产物** → 别硬跑，一句话告诉用户「当前项目没接 butler / 没有进行中的迭代产物可复核；复核需要 `.ai/AC_LIST.md` 与待审改动」，并提示要么先部署基地车、要么确认在对的目录。**不报错、不空跑。**

## 按 `$ARGUMENTS` 路由

**分支 A ─ 留空 → 默认快速自检（同上下文）**
读 `Coder/60_Extension_CodeReview/review-engine.md §5`（P5 简要自评），在**当前上下文**做轻量自检：只挑 Must Fix / Should Fix、不做全量多维打分，快速拦收口前的明显问题。这是默认底线、便宜快，但本质是「作者换口吻自评」、盲点可能仍在——要结构性独立请走分支 B。

**分支 B ─ 以 `independent` 开头 → 独立复核（fresh-context 子 agent）**
读 `Coder/62_Extension_Agents/independent-review.md`（复核帮手完整定义）+ `Coder/62_Extension_Agents/overview.md §3`（通用规矩 G1 隔离 / G2 诚实兜底），起一个**不带本会话上下文的干净子 agent**执行：spec-only 输入（`AC_LIST` / `TECH_PLAN` / `git diff` / `VERIFY_REPORT`，刻意不喂作者推理链）、**只读**、逐条 AC 出 confirm / refute / 无法验证 + 多维审查意见；**被 refute 的 AC 等同 Must Fix、阻断收口**。裁决落 `.ai/references/insight-independent-review.md`、回填 `VERIFY_REPORT` 的 `Independent Review` 字段（衔接见 independent-review §5）。**起不了干净子 agent 时按 G2 如实标注「独立复核未执行（环境不支持）」、当风险暴露，绝不退回同上下文自评再冒称「已独立」。**

## 收尾
执行完，一句话回报用户：走了哪条分支（快速自检 / 独立复核）、结论摘要（Must Fix / Should Fix / Nice 各几条、是否阻断收口）。
