---
状态: ack-frozen
ACK 日期: 2026-07-14
---

# Goal

MILE-0005 R3：套薄壳路由器范本落 `/butler:preference`——全批**参数面最宽**的命令。把偏好探针 4 子命令（`on`/`off`/`reback on|off`/`distill`）+ 空参只读回声，用一个薄壳分派清楚、覆盖全路径、委托 `preference-probe-engine` 真源不复述算法、收尾回声状态。验证「薄壳范本能吃下二级嵌套参数」。

# In Scope

- 新建 1 个薄壳命令 `.claude/commands/butler/preference.md`，结构与 `prd.md`/`review.md`/`milestone.md` 同构，含**二级参数分派**（`reback` 后再收 `on`/`off`）。
- 参数分派覆盖 6 条路径：空参、`on`、`off`、`reback on`、`reback off`、`distill`，外加裸 `reback`（缺第二 token）兜底。
- 各分支委托真源对应章节：开关→§2.3、reback→§2.2/§7、distill→§6、同意协议→§2.4（首次 `on`）、状态回声→§2.3。空参→只读回声（默认 Q3）。
- **`/preference` 触发名一并迁 `/butler:preference`**（默认 Q2）：引擎 `preference-probe-engine.md` 里作命令引用的 `/preference`（约 7–8 处：§2.2/§2.3 命令表/§2.4 同意披露/§2.5/§4.1/§10）全迁 + 命令表主行加「旧名 `/preference`」注 + 更新 capabilities 对应行。保留「偏好/记住这条」自然语言触发。
- capabilities 命令表 `/preference` 行**转换**为 `/butler:preference` 一等入口；README 目录树 `butler/` 子树补 preference.md。
- 切一版（默认判 MINOR，见 AC9）。

# Out of Scope

- **不改引擎算法**：`preference-probe-engine.md §1、§3–§10` 的采集/蒸馏/反哺/安全底线/隔离/存储契约一字不动；只动 §2.x 等处的触发**名**（非算法）。
- **不碰本项目级抑制开关**：`.ai/local-constraints.md` 的 `preference: on|off`（§2.5）由 `local-constraints-schema` 管，命令只**读**它作状态回声、**不 toggle**、不双写。
- **不动 `setup.sh`**：R1 目录软链已托管全套。
- **不碰存储骨架 / 初始化脚本**：`templates/preference/`、`preference-init.sh` 不动（惰性自举由引擎 §4.1 管）。
- **不下发目标项目**：命令不进 `templates/`、部署面零影响。
- **不新造能力**：只把散文 `/preference` 落成命名空间真命令，不发明新子命令、不扩语义。

# Acceptance Checklist

- [ ] **AC1（命令成立·可达）**：`.claude/commands/butler/preference.md` 建立；命名空间映射 `butler/preference.md`→`/butler:preference` 结构正确；隔离 HOME 实跑 `setup.sh` 报 **6 个 /butler:* 命令**、preference 经目录软链 `test -e` 可达。
- [ ] **AC2（参数分派完整·本迭代脊柱）**：薄壳按 `$ARGUMENTS` 覆盖全路径，逐条委托对的真源章节——
  - 空参 → 只读状态回声（读 `$PREF/config.md` consent + reback 态 + 本项目抑制态，不写）；
  - `on` / `off` → §2.3 隐私总开关（`on` 首次触发 §2.4 同意协议，委托不复述）；
  - `reback on` / `reback off` → §2.2/§7 影响回路开关（**二级参数**：首 token `reback` 再看第二 token）；
  - `distill` → §6 手动蒸馏+维护（§8 安全边界触发）；
  - 裸 `reback`（无第二 token）→ 兜底（回声当前 reback 态或提示补 on/off，不误开关）；
  - 未知参数 → 优雅提示合法参数集、不瞎猜执行。
- [ ] **AC3（触发名迁移无残留）**：`preference-probe-engine.md` 里作命令引用的 `/preference` 全迁 `/butler:preference`（含同意披露「怎么关」文案）；命令表主行加旧名注；全仓无残留裸 `/preference`（历史归档冻结快照 + `preference-*.sh`/`preference-probe-engine.md` 文件名引用除外）。
- [ ] **AC4（范式一致性）**：与 `prd.md`/`review.md`/`milestone.md` 同构——① 薄壳三件事声明 + DRY 不复述红线；② 跨 cwd 路径约定段；③ 第 0 步优雅降级（说清「实验性 + 数据外置 `$PREF`、开关全局、不强依赖当前项目 `.ai/`」）；④ frontmatter 说人话无裸术语；⑤ `$ARGUMENTS` 路由；⑥ 委托的真源 section 锚点（§2.2/§2.3/§2.4/§6/§7）回真源核**真实存在**、无捏造。
- [ ] **AC5（状态回声 + 只读默认）**：任何开关变更收尾**当回合回声当前状态**（§2.3 硬要求）；空参分支纯只读（不写 `$PREF`、不写 `.ai/`）。
- [ ] **AC6（边界守恒）**：引擎 §1、§3–§10 算法、`local-constraints-schema`、`setup.sh`、`templates/**`（含 `preference/`）、`preference-init.sh`、四件套 schema、hook、其他命令一行未动；`git diff` 佐证改动仅落 `.claude/commands/butler/preference.md`、`preference-probe-engine.md`(§2.x 触发名)、`capabilities.md`/`README.md`、发布层。
- [ ] **AC7（文档更新）**：`capabilities.md` 命令表 `/preference` 行转换为 `/butler:preference` 一等入口（真源指命令文件 + 引擎）；`README.md` `butler/` 子树补 preference.md。
- [ ] **AC8（目录软链自动托管·实跑）**：隔离 HOME 实跑 `setup.sh`，确认 preference 经 `~/.claude/commands/butler` 目录软链可达、`setup.sh` 未改一行、无 `butler/butler` 套娃——续验 R1 红利（这次 6 命令）。
- [ ] **AC9（切版三载体对齐）**：判 **MINOR**（纯新增 1 命令、无破坏面）；`VERSION` bump、`CHANGELOG.md` 顶条、git tag 三者一致；`migrations/vX.Y.Z.md` 为部署面 `[no-op]`+`[restamp]`。

# Verification Method

- **AC1/AC8**：`test -f` 命令文件 + 隔离 HOME `bash scripts/setup.sh` → `test -e ~/.claude/commands/butler/preference.md` + 报 6 命令（auto·可靠）。
- **AC2**：读命令文件，对 6 条路径 + 裸 reback 兜底 + 未知参数逐条核「有分支 + 委托对的 §」（人读路径清单核）。
- **AC3**：`grep -rn '/preference' Coder .ai/project README.md`（历史归档 + 文件名引用除外）应零裸旧名（auto·可靠）。
- **AC4**：与三前例命令结构逐要点对照 + 真源 §2.2/§2.3/§2.4/§6/§7 锚点回引擎核（人读同构核 + auto 锚点核）。
- **AC5**：读命令收尾段确认回声状态 + 空参分支无写操作（人读）。
- **AC6/AC7**：`git diff --stat` 无越界（auto）+ 读 capabilities/README 核更新到位（人读）。
- **AC9**：`cat VERSION` == tag == CHANGELOG 顶条（auto·可靠）。

# Open Questions / Risks（呈 ACK 时请一并确认三默认）

1. **切版号**：默认 **MINOR**（纯新增命令能力，与 R1/R2 同类）。
2. **`/preference` 触发名一并迁 + 迁移面**（AC3）：默认**全迁**（引擎作命令引用的约 7–8 处 + capabilities，触发名非算法、与 R2 一致；保留自然语言触发）。比 R2 面宽，普查要到位。若想保守只加命令、不碰引擎正文，可否掉、`/preference` 散文名与 `/butler:preference` 命令并存。
3. **空参默认 = 只读状态回声**（AC2/AC5）：引擎 §2.3 未定义空参 / `status`；薄壳给空参加「只读回声 consent/reback/本项目抑制态」默认，与 milestone/review 只读默认同构、纯读不写。默认**采纳**；若想严格照引擎命令面、空参报「用法提示」，可否掉。
- **风险**：命令菜单「可见性」headless 不可实敲，沿用 R1/R2 代理验法（文件/软链存在 + 结构正确 + 经软链可达）；`reback` 二级参数是分派最易漏的点，AC2 路径清单专盯。
