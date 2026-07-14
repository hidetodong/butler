---
状态: ack-frozen
ACK 日期: 2026-07-14
---

# Goal

MILE-0005 R4（收官）：把最后两个高风险能力落成 `/butler:*` 命令——`/butler:loop`（收敛闭环死磕）+ `/butler:dangerous`（无人值守自治）。**唯一新面是风险闸**：命令化后敲一下就触发的便利**绝不能**降低它们「该被郑重、显式触发」的门槛。薄壳不复述护栏算法（守 DRY），改用 frontmatter ⚠️ 标记 + 第 0 步前置风险提醒 + 把真正的闸交回引擎。收口即整体收 MILE-0005。

# In Scope

- 新建 2 个薄壳命令 `.claude/commands/butler/loop.md` + `dangerous.md`，结构与 `prd.md`/`review.md`/`preference.md` 同构。
- **`/butler:loop`**：一次性 P4 升档，委托 `convergence-loop-engine.md`（§3 闭环 / §6 定量熔断）；无持久状态、无 off、近乎无参数；风险提醒=高强度 / 长时 / 消耗大。
- **`/butler:dangerous`**：持久开关，委托 `dangerous-engine.md`（§3 激活/关闭 + §3.1 跨会话 announce-on-read + §7 护栏）；空参=开启（走引擎 §3 回声闸）/ `off`=关闭 / `status`=只读回声当前 `dangerous` 开关态；状态外化 `.ai/local-constraints.md`「Butler 功能开关」`dangerous`（命令只读写开关值、不改 schema）。
- **风险闸**（本迭代脊柱）：两命令 frontmatter `description` 带显式 ⚠️；第 0 步前置一句风险提醒（dangerous 点明「实验性 + 无人值守 + 建议可隔离/可回滚环境」、loop 点明「高强度死磕 + 长时」）+ 委托引擎自己的闸（**不复述护栏 / 熔断 / 自审门算法**）。
- **`/loop`·`/dangerous` 触发名迁 `/butler:*`**（策略待 ACK，默认全迁外科式）：作命令引用的散文触发词迁 `/butler:*`，**精确排除** `dangerous-engine.md:21` 的 harness-`/loop`（Claude Code 自带）；logic-protocol §89/§92 加「旧名仍识别」注 + 保留自然语言触发。
- capabilities 命令表补两行；README 扩展模式表 + `butler/` 子树补两命令 + Coder 目录 `55/65` 行迁。
- 切一版（默认判 MINOR → v2.10.0，见 AC9）。

# Out of Scope

- **不改引擎算法**：`convergence-loop-engine.md §1–§8`、`dangerous-engine.md §1–§10` 的闭环 / 熔断 / 自治 / 自审门 / 护栏 / checkpoint 一字不动；只动触发**名**（非算法）。
- **不碰 `.ai/local-constraints.md` 的 `dangerous:` 字段 schema**：由 `local-constraints-schema` 管；命令只按引擎 §3 读写开关值，不改字段定义、不双写 schema。
- **不动 `setup.sh`**：R1 目录软链已托管全套。
- **不下发目标项目**：命令不进 `templates/`（含 rule-card 里 `/loop`·`/dangerous` 散文——同 R3，命令不下发、目标项目靠散文旧名兜底）、部署面零影响。
- **不新造能力 / 不改风险语义**：只把散文触发词落成命名空间真命令，不发明新子命令、不降低也不加码引擎既有的风险门槛（薄壳只把闸交回引擎、不自造确认对话）。

# Acceptance Checklist

- [ ] **AC1（两命令成立·可达）**：`.claude/commands/butler/loop.md` + `dangerous.md` 建立；命名空间映射 `butler/<name>.md`→`/butler:<name>` 结构正确；隔离 HOME 实跑 `setup.sh` 报 **8 个 /butler:* 命令**、两新命令经目录软链 `test -e` 可达。
- [ ] **AC2（风险闸·本迭代脊柱）**：命令化不降低「郑重显式触发」门槛，逐条可核——
  - 两命令 frontmatter `description` 均含显式 ⚠️ 风险标记（说人话、菜单可见）；
  - 第 0 步前置风险提醒：`dangerous` 点明「实验性 / 无人值守自治 / 风险显著高于标准 / 建议可隔离·可回滚环境」、`loop` 点明「高强度死磕 / 长时 / 消耗大」；
  - **闸交回引擎、不复述**：`dangerous` 委托 §3（回写 `on`+对话层回声）+ §3.1（announce-on-read）+ §7（审计 / checkpoint / P5 强制完整审查），`loop` 委托 §6（定量熔断）——薄壳**不重写**确认对话 / 护栏 / 熔断算法（守 DRY），也**不省略**风险提醒（不降门槛）。
- [ ] **AC3（参数分派）**：`/butler:dangerous` 按 `$ARGUMENTS`——空参→开启（走引擎 §3 回声闸，**与 preference 空参=只读回声有意不同**，因引擎 §3 已定义 bare=开启）、`off`→关闭（§3）、`status`→只读回声当前 `dangerous` 开关态（不改开关）、未知参数→兜底列合法参数不瞎猜；`/butler:loop`→开启闭环（无 off、无持久态），有多余参数则一句提示 loop 无子命令、仍按开启处理或提示。
- [ ] **AC4（触发名迁移 + harness 撞车排除）**：`/loop`·`/dangerous` 作命令引用处按 ACK 策略迁 `/butler:*`；**`dangerous-engine.md:21` 的 harness-`/loop`（Claude Code 自带）保留不迁**（专项核对）；logic-protocol §89/§92 加旧名注；全仓活文档无残留裸命令名（历史归档 + `convergence-loop-engine.md`/`dangerous-engine.md` 文件名引用 + harness-`/loop` + 刻意保留的 templates 除外）。
- [ ] **AC5（范式一致性）**：两命令与 `prd.md`/`review.md`/`preference.md` 同构——① 薄壳声明 + DRY 红线；② 跨 cwd 路径约定段；③ 第 0 步优雅降级（没接 butler → 一句话说清、不报错不空跑）；④ frontmatter 说人话无裸术语；⑤ 委托真源 section 锚点（loop §3/§6、dangerous §3/§3.1/§7）回真源核**真实存在**、无捏造。**良性差异如实**：`loop` 无参数分派（一次性升档、无子命令），是真实结构差异非漏写。
- [ ] **AC6（边界守恒）**：两引擎 §1–§8 / §1–§10 算法、`local-constraints-schema`、`setup.sh`、`templates/**`、四件套 schema、hook、其他命令一行未动；`git diff --stat` 佐证改动仅落两新命令 + 触发名活文档 + `capabilities.md`/`README.md` + 发布层。
- [ ] **AC7（文档更新）**：`capabilities.md` 命令表补 `/butler:loop`·`/butler:dangerous` 两行（真源指命令文件 + 引擎、注风险闸）；`README.md` 扩展模式表两行迁 `/butler:*` + `butler/` 子树补两命令（`└──` 收尾正确）+ Coder 目录 `55/65` 行迁。
- [ ] **AC8（目录软链自动托管·实跑）**：隔离 HOME 实跑 `setup.sh`，两新命令经 `~/.claude/commands/butler` 目录软链可达、`setup.sh` 未改一行、无 `butler/butler` 套娃——续验 R1 红利（这次 **8 命令**）。
- [ ] **AC9（切版三载体对齐）**：判 **MINOR → v2.10.0**（纯新增 2 命令、无破坏面）；`VERSION` bump、`CHANGELOG.md` 顶条、git tag 三者一致；`migrations/v2.10.0.md` 为部署面 `[no-op]`+`[restamp]`。里程碑收官——本版收口后 MILE-0005 整体收、聚合交付 `deliveries/milestones/`。

# Verification Method

- **AC1/AC8**：`test -f` 两命令文件 + 隔离 HOME `bash scripts/setup.sh` → `test -e` 两新命令 + 报 8 命令（auto·可靠）。
- **AC2/AC3/AC5**：读两命令文件，对风险闸三要点（frontmatter ⚠️ / 第0步风险提醒 / 闸交回引擎不复述）+ dangerous 参数四路径 + 委托锚点逐条核（人读 + auto 锚点核）。
- **AC4**：`grep -rn '/loop' '/dangerous'`（历史归档 + 文件名 + harness-`/loop` + templates 除外）应零裸旧命令名；**专项核** `dangerous-engine.md:21` harness-`/loop` 仍在（auto·可靠）。
- **AC6/AC7**：`git diff --stat` 无越界（auto）+ 读 capabilities/README 核更新到位（人读）。
- **AC9**：`cat VERSION` == tag == CHANGELOG 顶条（auto·可靠）。

# Open Questions / Risks（呈 ACK 时请一并确认三默认）

1. **切版号**：默认 **MINOR → v2.10.0**（纯新增 2 命令能力，与 R1–R3 同类）。
2. **`/loop`·`/dangerous` 触发名迁移策略**（AC4）：默认**全迁外科式**（作命令引用的 71 处迁 `/butler:*`、保命名空间统一，精确排除 harness-`/loop`）。备选保守=只迁面向人文档（README/HUMAN_GUIDE/capabilities）+ 命令文件 + 旧名注，引擎正文密集交叉引用留散文（避 71 处大改 + 撞车风险）。二者都不改算法。
3. **一迭代做完两命令 + `/dangerous` 空参=开启**（AC1/AC3）：默认**一个迭代 ITER-0050 做完 loop+dangerous**、收口即收 MILE-0005；`/butler:dangerous` 空参=开启（走引擎 §3 闸）、`status` 只读——与 preference 空参=只读回声有意不同。若想拆两迭代分开切版、或让 dangerous 的 bare 也走「只读回声、要 `on` 才开」更保守姿态，可否掉。
- **风险**：① 触发名迁移面 71 处最宽 + harness-`/loop` 撞车，普查最易漏，AC4 专项核对兜底；② 「命令化不降门槛」是本迭代成败点，AC2 把「frontmatter ⚠️ + 第0步风险提醒 + 闸交回引擎不复述」写成可核检查点；③ 命令菜单「可见性」headless 不可实敲，沿用 R1–R3 代理验法（文件/软链存在 + 结构正确 + 经软链可达）。
