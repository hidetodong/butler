> 分流: 完整 | 命中升级信号: 触碰 Coder 真源触发词（`/preference` 迁移面比 R2 宽）, 涉及发布切版, 参数分派最复杂 | 2026-07-14

# 一句话

给 MILE-0005 命名空间落 R3 那个**参数面最宽**的命令 `/butler:preference`：把偏好探针的 4 个子命令（`on`/`off`/`reback on|off`/`distill`）＋空参默认，用一个薄壳路由器分派清楚，委托 `70_Extension_Preference` 真源、不复述算法。

# Goal

MILE-0005 R3：验证薄壳范本能吃下**二级嵌套参数**。R2 的三命令都是 0–1 级扁平分支（milestone 顶多一个 `status`）；`/butler:preference` 是全批唯一带二级参数的——`reback` 后面还要再收 `on`/`off`。当初特意把它从 R2 拆出单开一迭代，就为把这套参数分派写扎实、不糊弄。

# Current Understanding

- **真源命令面**（`preference-probe-engine.md §2.3`，已读确认）：
  - `on` / `off` — **隐私总开关**：`off`=停采集+蒸馏+反哺、保留已存数据；`on`=恢复默认（数据回路开、反哺关）。
  - `reback on` / `reback off` — **影响回路开关**（默认关）；这是唯一的**二级参数**：首 token=`reback` 时再看第二 token 定 on/off。
  - `distill` — 手动触发一次蒸馏+维护（§6）。
- **薄壳新增的空参默认**（设计决策，见 Open Questions 3）：空参 → **只读状态回声**（读外置 `$PREF/config.md` 的 consent、reback 开关、本项目抑制态），不写任何文件。与 `/butler:milestone status`、`/butler:review` 默认自检同构；也顺 §2.3「开关变更必须当回合回声状态」的读侧延伸。
- **必须回声状态**：§2.3 硬要求任何开关变更在当回合对话层显式回声当前状态——薄壳收尾统一做这件事。
- **一次性同意协议**（§2.4）：`on` 首次在托管项目命中可采集决策且无 consent 记录时全局问一次——**命令不复述该协议，委托真源按 §2.4 走**。
- **边界：命令只管全局层开关**（consent/reback/distill），**不碰**本项目级抑制开关（`.ai/local-constraints.md` 的 `preference: on|off`，那是 §2.5 持久在 local-constraints、由 local-constraints-schema 管，命令只能**读**它做状态回声、不 toggle）。
- **范本已由 R1+R2 固化**：`prd.md` 三分支、`review.md` 两分支证明扁平骨架可复制；R3 是骨架第一次吃**二级参数**的检验。

# Constraints

- **不改引擎算法**：`preference-probe-engine.md §1–§10` 的采集/蒸馏/反哺/安全底线/隔离纪律一字不动（沿用 MILE-0005 Out of Scope）。唯一可能动的是把 §2.3 等处的触发词 `/preference` 迁成 `/butler:preference`——**触发名非算法**，要 P2 显式定（Open Questions 2）。
- **触发名迁移面比 R2 宽**：`/preference` 在引擎里出现约 7–8 处（§2.3 命令表 3 行、§2.2、§2.4 同意披露「怎么关」、§2.5、§10、§4.1），比 R2 `/butler-upgrade`（仅 butler-upgrade.md §2 一处触发词行）分布更广——迁移要普查到位、别漏。
- **不下发目标项目**：命令不进 `templates/`、目标项目部署面零影响（沿用 ITER-0044/0047/0048 边界）。
- **不动 `setup.sh`**：R1 目录软链已托管全套，R3 只往目录里加一个文件。
- **薄壳纪律**：只做「读对规则进上下文 + 按参数分派 + 委托真源 + 回声状态」，不复述同意协议 / 采集蒸馏算法 / 安全底线（DRY 红线）；带第 0 步优雅降级。

# Impact Scope

- **新增**（命令层）：`.claude/commands/butler/preference.md`（1 个薄壳，含二级参数分派）。
- **可能改**（待 P2 定，见 Open Questions）：`preference-probe-engine.md` 里的 `/preference` 触发词 → `/butler:preference`（约 7–8 处）、`.ai/project/capabilities.md` 命令表 `/preference` 行转换、README 子树补 preference.md。
- **发布层**：VERSION + CHANGELOG + `migrations/vX.Y.Z.md`（切版号待定，倾向 MINOR）。
- **不碰**：`setup.sh`、`templates/**`（含 `templates/preference/` 存储骨架，不动）、`preference-init.sh`、四件套 schema、hook、其他命令、引擎算法、`local-constraints-schema`。

# Project Type

Markdown 规则仓库 dogfooding（butler 编辑自身命令层）。无代码编译，验证靠：命令文件结构核（薄壳四要点齐 + 二级参数分派覆盖全 5 条路径 + 真源锚点真实）+ 隔离 HOME 实跑 `setup.sh` 确认新命令经目录软链可达（这次预期 6 命令）+ `/preference` 触发名残留普查 + `git diff` 边界守恒。

# Open Questions

1. **切版号**：R3 纯新增 1 命令、无破坏面，判 **MINOR**（新增能力，与 R1/R2 同类）。倾向 MINOR。
2. **`/preference` 触发名是否一并迁 `/butler:preference` + 迁到什么程度**：R2 已把 `/butler-upgrade`→`/butler:upgrade`（ACK 通过）。倾向**一并迁**（触发名非算法、与 R2 一致），保留「偏好/记住这条」自然语言触发。范围默认：引擎里作**命令引用**的 `/preference` 全迁（含 §2.4 同意披露的「怎么关: /butler:preference off」这类用户可见文案），命令表主行加「旧名 `/preference`」注。这比 R2 面宽，要普查干净。
3. **空参默认 = 只读状态回声**：引擎 §2.3 没定义 `status` 子命令或空参行为；薄壳给空参加一个「只读回声当前 consent/reback/本项目抑制态」的默认，与 milestone/review 的只读默认同构、纯读不写。倾向**采纳**（安全、符合 §2.3 回声精神）；若你觉得该严格照引擎命令面、空参就报「用法提示」，也可否掉。
