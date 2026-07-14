# VERIFY_REPORT — ITER-0049（`/butler:preference` 最宽参数薄壳命令 · MILE-0005 R3）

> 标准模式：P2 AC_LIST 经用户 ACK（三默认全收——MINOR / `/preference` 触发名全迁 `/butler:preference`〔含用户可见同意披露文案〕/ 空参采纳只读状态回声）。风险集中在**触发名迁移面**（比 R2 宽）与 `reback` **二级嵌套参数**分派两点，其余为复制 R1/R2 已验范式。P5 走标准复核（自评 + 客观隔离 HOME 实跑 + 全仓残留普查），未升格强制独立复核——迁移面已 T5 普查 + P5 复查双清、`reback` 分派已按路径清单逐条核，无 shaky 处、不触发升格。

# Verification Summary
- 覆盖：新建薄壳命令 `.claude/commands/butler/preference.md`（全批**参数面最宽**：4 子命令 + 二级嵌套参数 + 空参只读回声）套 R1 范本；`/preference`→`/butler:preference` 活规则/人读文档触发名全迁（引擎 §2.x 11 处 + logic-protocol/local-constraints-schema/dangerous-engine/Coder README/HUMAN_GUIDE/README/项目 digest）；`templates/` **刻意保留** `/preference`（DD5，部署面边界）；capabilities 命令表转换 + README 目录树补 preference.md；`migrations/v2.9.0.md`（`[no-op]`+`[restamp]`）；MINOR 切版三载体。
- 总体结论：**AC1–AC9 全过**。P4 实测：隔离假 HOME 实跑 `setup.sh` **6/6 命令经目录软链可达**、`git diff --stat` 边界守恒（`templates/` 与 `scripts/setup.sh` 零改动）、真源 section 锚点（§2.2/§2.3/§2.4/§6/§7）逐一回真源核无捏造、`/preference` 全仓残留普查零裸旧命令名。
- **计划-实际差异 1 处（记录·非缺陷）**：ACK 时口径「引擎约 7–8 处」，T1 普查实测触发名分布 **约 13 处**（引擎 11 + 5 份活文档）。已按 TECH_PLAN DD3 上前枚举全集迁移，**且按 DD5 刻意不碰 `templates/`**——差异是 ACK 口径低估了触发名在活文档的分布面，非范围外扩张（仍在 ACK 的「全迁活文档」意图内、`templates/` 保留是 ACKed「不碰 templates」边界的直接落实）。

# AC Status（道 + 置信档）
- [x] **AC1（命令成立·可达）**(auto·可靠)：`.claude/commands/butler/preference.md` 建立；命名空间映射 `butler/preference.md`→`/butler:preference` 结构正确；隔离 HOME 实跑 `setup.sh`（exit 0）经 `~/.claude/commands/butler` 目录软链 `test -e` 报 **6 个 /butler:* 命令**（prd/review/milestone/upgrade/ideation/preference）全绿。
- [x] **AC2（参数分派完整·本迭代脊柱）**(人读路径清单核 + auto 锚点核)：薄壳按 `$ARGUMENTS` 覆盖全路径逐条委托对的真源——
  - 空参 → 只读状态回声（读 `$PREF/config.md` consent + reback 态 + 本项目抑制态，**不写**）；
  - `on` / `off` → §2.3 隐私总开关（`on` 首触发 §2.4 同意协议，委托不复述）；
  - `reback on` / `reback off` → §2.2/§7 影响回路开关（**二级参数**：首 token `reback` 再读第二 token on/off）；
  - `distill` → §6 手动蒸馏（§8 安全边界）；
  - 裸 `reback`（缺第二 token）→ 兜底回声当前 reback 态 + 提示补 on/off、**不误开关**；
  - 未知参数 → 兜底列合法参数集、不瞎猜执行。
  委托锚点 §2.2/§2.3/§2.4/§6/§7 回引擎逐一**真实存在**。
- [x] **AC3（触发名迁移无残留）**(auto·可靠)：`preference-probe-engine.md` 作命令引用的 `/preference` 全迁（11 处，含 §2.4 同意披露「怎么关」用户可见文案）+ 命令表主行加旧名注；logic-protocol / local-constraints-schema / dangerous-engine / Coder README / HUMAN_GUIDE / README / 项目 digest 一并迁。全仓活文档普查（`grep -rn '/preference' Coder .ai/project README.md HUMAN_GUIDE.md`，排除 `preference-probe-engine`/`preference-init` 文件名引用、`~/.butler/preferences/` 存储路径）**零裸旧命令名**。
- [x] **AC4（范式一致性）**(人读同构核 + auto 锚点核)：与 `prd.md`/`review.md`/`milestone.md` 同构——① 薄壳三件事声明 + DRY 不复述红线 ✓；② 跨 cwd 路径约定段（`Coder/…` 相对 `$BUTLER_PATH`、数据落外置 `$PREF` 而非 `.ai/`/butler 仓）✓；③ 第 0 步优雅降级（说清「实验性 + 数据外置 `$PREF`、开关全局、不强依赖当前项目 `.ai/`、引擎不可达→说 butler 未装」）✓；④ frontmatter 说人话无裸术语 ✓；⑤ `$ARGUMENTS` 路由（**含二级嵌套**）✓；⑥ 委托真源 section 锚点 §2.2/§2.3/§2.4/§6/§7 回真源核**真实存在**、零捏造 ✓。
- [x] **AC5（状态回声 + 只读默认）**(人读)：任何开关变更收尾**当回合回声当前状态**（§2.3 硬要求，收尾段在）；空参分支纯只读（读 `$PREF/config.md`，不写 `$PREF`、不写 `.ai/`）。
- [x] **AC6（边界守恒）**(auto·可靠)：`git diff --stat` — 改动仅落 `.claude/commands/butler/preference.md`（新）+ `preference-probe-engine.md`(§2.x 触发名) + 7 份活文档触发名 + `capabilities.md`/`README.md` + 发布层（VERSION/CHANGELOG/migrations）+ `.ai/` 本迭代产物/台账。引擎 §1、§3–§10 算法（采集/蒸馏/反哺/安全底线/隔离/存储契约）**一字未动**；`local-constraints-schema`（`preference:` 字段仍归它管）、`scripts/setup.sh`、`templates/**`（含 `preference/`、`rule-card.md`）、四件套 schema、hook、其他命令**一行未动**（`git diff --stat -- templates/` 与 `-- scripts/setup.sh` 均空）。
- [x] **AC7（文档更新）**(auto + 人读)：`capabilities.md` 命令表 `/preference` 行**转换**为 `/butler:preference` 一等入口（真源指命令文件 + 引擎 §2.2/§2.3/§2.4/§6/§7、注「参数面最宽·唯一二级参数·只管全局层」）；`README.md` `butler/` 子树补 `preference.md`（`└──` 收尾）+ 扩展模式表 `/butler:preference` + Coder 目录 `70_Extension_Preference` 行迁。
- [x] **AC8（目录软链自动托管·实跑）**(auto·可靠)：隔离假 HOME 实跑 `setup.sh`（exit 0），新命令 `~/.claude/commands/butler/preference.md` 经**目录软链**`test -e` 通过、R1/R2 的 prd+review+milestone+upgrade+ideation 仍可达（**6/6**）、**未改 `setup.sh` 一行**、软链目标指向仓库命名空间目录无 `butler/butler` 套娃——续验 R1「整目录软链」红利（这次 6 命令）。
- [x] **AC9（切版三载体对齐）**(auto·可靠)：判 **MINOR**（纯新增 1 命令、无破坏面）；`VERSION`=2.9.0、`CHANGELOG.md` 顶条 `[2.9.0] - 2026-07-14`、`migrations/v2.9.0.md` 区间 `v2.8.0→v2.9.0` 三者一致；git tag v2.9.0 于发布提交时打（见 Handoff）；migration 对部署面为 `[no-op]`+`[restamp]`。

# Verification Results
- AC1/AC8：隔离假 HOME `HOME=<tmp> bash scripts/setup.sh`（exit 0）——目录软链 `~/.claude/commands/butler`→仓库命名空间目录、`test -e` 6 命令全绿、无套娃。
- AC2/AC4：读命令文件核薄壳六要点齐 + 6 条路径 + 裸 reback 兜底 + 未知参数逐条核「有分支 + 委托对的 §」；委托真源锚点 §2.2/§2.3/§2.4/§6/§7 回 `preference-probe-engine.md` **逐一真实存在**。
- AC3：`grep -rn '/preference'`（Coder + .ai/project + README + HUMAN_GUIDE，排除文件名引用与存储路径）——活文档残留**全部合法**（`templates/rule-card.md` 部署面刻意保留、`~/.butler/preferences/` 存储路径、命令表旧名注解、本迭代规划稿讨论迁移本身、`.ai/iterations` 历史归档），**零裸旧命令名**。
- AC5：读命令收尾段确认回声状态 + 空参分支无写操作。
- AC6：`git diff --stat` 20 改 + 2 新（preference.md + migration）；`git diff --stat -- templates/` 空、`-- scripts/setup.sh` 空——边界守恒。
- AC7：读 capabilities 命令表（`/preference` 行已转换）+ README（`butler/` 子树 6 命令齐、扩展模式表 + Coder 目录已迁）。
- AC9：`cat VERSION`=2.9.0、CHANGELOG 顶条 `[2.9.0] - 2026-07-14`、`migrations/v2.9.0.md` 首行区间 `v2.8.0 → v2.9.0` 一致。

# Gate Coverage
- 通用质量门禁：不破坏分层（命令层改动不入 `Coder/` 算法、不入 `templates/`）✓ / 新命令 README 目录树注册（无隐式依赖）✓ / 文件名互引不写绝对路径 ✓ / frontmatter 说人话无裸术语 ✓ / 产物链未动 ✓。
- Active Profiles：无（规则仓，未命中 domain profile）。
- Tech Plan Alignment：DD1/DD2/DD4/DD6/DD7/DD8 全兑现；**DD3 计划-实际差异**：ACK 口径「引擎约 7–8 处」，实测触发名分布约 13 处（引擎 11 + 5 份活文档），已按 DD3 上前枚举全集迁移；**DD5 边界刻意执行**：`templates/rule-card.md`、`templates/preference/*` 的 `/preference` **保留不迁**——`/butler:preference` 是靠全局软链的个人命令、不下发目标项目，目标项目里保证生效的是散文旧名（logic-protocol 迁后仍认作旧名触发），迁 templates 会破「命令不下发目标项目」边界 + 触发 `[regen-claude]` + 违反 ACKed「不碰 templates」。故引擎正文说 `/butler:preference`、templates 保留 `/preference` 是**有意的分层**，靠 logic-protocol 保留旧名识别把两者接住。T1–T8 全落。
- References Compliance：N/A（无外部参考资料）。

# Independent Review（标准模式·未升格）
- 本迭代主体为复制 R1/R2 已验薄壳范式 + 触发名字符串迁移 + 幂等切版，两处真实新面——`reback` 二级嵌套参数分派、比 R2 宽的迁移面——均已定向复核（AC2 路径清单逐条核 `reback` 分派、T5+P5 双轮普查清迁移残留）。P5 自评 + 客观隔离 HOME 实跑无 shaky 处，按标准模式**不强制**独立复核（区别于 R1 危险模式的强制升格）。若后续 R4（`loop`/`dangerous` 加风险闸）复杂度上来，再按 dangerous/复核标准决定是否升格。

# Remaining Risks
- 命令菜单「可见性」headless 不可实敲——沿用 R1/R2 代理验法（文件存在 + 命名空间结构正确 + 经目录软链 `test -e` 可达 + `setup.sh` exit 0）。命名空间机制经 R1 claude-code-guide 查证 + 多轮隔离 HOME 实跑，可靠。
- **引擎说 `/butler:preference`、templates 保留 `/preference` 的双名并存**：靠 logic-protocol 保留旧名识别接住（自然语言触发 + 旧名散文触发照常）。目标项目侧规则卡文案不变、旧名仍工作；风险已由 DD5 决策记录 + migration 说明覆盖，非缺陷。
- `[global-install]` / `[restamp]` 之外无部署面动作；偏好探针**反哺回路**（reback）与**蒸馏**（distill）标实验性，命令只落触发入口、未改引擎算法，端到端行为由引擎 §2/§6/§7 既有实现保证（本迭代未新验其运行时行为）。

# Handoff / Next Step
- P5 通过（AC1–AC9 全过、0 阻断项）→ 进原子收口五步（归档四件套 + 交付 md/html + 台账/路线图 + 知识文件夹前滚 + 收口自检）+ 切版 git 仪式（feat 提交 + 独立 chore(release) 提交 + 本地 tag v2.9.0）。
- MILE-0005 R3 达成即交还；R4（`loop`+`dangerous` 加风险闸）设计未锁、不擅自连跑。标准模式授权范围：ACK 的 R3 scope 一路推到收口 + 提交 + 推分支 + PR #3 增长；**不合并 main、不推 tag v2.9.0 到远端**（待用户授权）。
