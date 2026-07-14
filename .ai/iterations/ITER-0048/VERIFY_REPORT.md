# VERIFY_REPORT — ITER-0048（批量落 3 个 butler 命名空间命令 · MILE-0005 R2）

> 标准模式：P2 AC_LIST 经用户 ACK（三默认全收——MINOR / `/butler-upgrade` 触发名迁 / capabilities 转换）。低风险纯机械（3 薄壳命令 + 触发名迁 + 文档 + 切版），P5 走标准复核（自评 + 客观隔离 HOME 实跑），未升格强制独立复核——无 shaky 处、不触发升格。

# Verification Summary
- 覆盖：新建 3 薄壳命令（`milestone.md`/`upgrade.md`/`ideation.md`）套 R1 范本、`/butler-upgrade`→`/butler:upgrade` 触发名全仓迁移、capabilities 命令表转换 + 顺清 `/review` 冗余、README 目录树补 3 命令、`migrations/v2.8.0.md`（`[no-op]`+`[restamp]`）、MINOR 切版三载体。
- 总体结论：**AC1–AC9 全过**。P4 实测：隔离假 HOME 实跑 `setup.sh` ×2（首装 + 幂等）**5/5 命令经目录软链可达**、`git diff --stat` 边界守恒、真源 section 锚点逐一回真源核无捏造、`/butler-upgrade` 全仓残留普查零裸旧名。
- **计划-实际差异 1 处（记录·非缺陷）**：TECH_PLAN DD3/T4 写「`butler-upgrade.md` 只改 §2 一行触发词」，但 AC3 要「全仓无残留裸 `/butler-upgrade`」——实际迁了 **6 处**命令名（见 §计划对齐）。6 处**全是触发名、非算法**，与 DD3 原则（触发名非算法、与 R1 一致）一致，只是覆盖面比字面「一行」宽。

# AC Status（道 + 置信档）
- [x] AC1（三命令成立·可达）(auto·可靠)：`.claude/commands/butler/` 下 `milestone.md`+`upgrade.md`+`ideation.md` 三文件建立；隔离 HOME 实跑 `setup.sh` 报「5 个 /butler:* 命令」、命名空间映射 `butler/<name>.md`→`/butler:<name>` 结构正确。
- [x] AC2（`/butler:milestone` 薄壳）(auto 结构核 + 人读)：委托 `milestone-schema.md`（§6.1 启动信号 / §6.4 录入〔含大 PRD 并进 `prd-split`〕/ §6.5 只读看板 / §7.1 开启）；`$ARGUMENTS` 分派留空-brief→录入、`status`→看板；第 0 步无 `.ai/` 优雅降级不报错；DRY 不复述；frontmatter 两行说人话；跨 cwd 路径约定段在。收口/废弃/演进走语义（§7.3-7.5）已注明。
- [x] AC3（`/butler:upgrade` 薄壳 + 触发名迁移）(auto·可靠)：委托 `butler-upgrade.md`（§3 侦察 / §4 首次 / §5 常规区间队列 / §6 落地〔§6.3 不纳入〕/ §7 验证回退 / §5·§8 保护区契约）；升级对象=当前项目、第 0 步降级（无 `CLAUDE.md`/`.ai/`→指向 `mcv-deployment`）；不复述配方算法；触发名 `/butler-upgrade`→`/butler:upgrade` 全仓迁移，普查零裸旧名残留（历史归档 + `butler-upgrade.md` 文件名引用除外，合法）。
- [x] AC4（`/butler:ideation` 薄壳）(auto 结构核 + 人读)：委托 `ideation-engine.md §3`（§3.1 意图探测 / §3.2 需求展开 / §3.3 压力测试 / §3.4 收敛）；第 0 步降级（无 `.ai/` 也能脑暴、有则接 P1）；不复述脑暴流程；frontmatter 两行说人话；跨 cwd 路径约定段在。
- [x] AC5（范式一致性）(人读同构核)：三命令与 `prd.md`/`review.md` 同构——薄壳声明 + DRY 红线 ✓ / 跨 cwd 路径约定段 ✓ / 第 0 步优雅降级 ✓ / frontmatter 说人话无裸术语 ✓ / `$ARGUMENTS` 路由（milestone 有 status 分支、upgrade·ideation 无参数但结构一致）✓ / 委托真源 section 锚点**全部真实存在**（回真源逐一核，零捏造）✓。**良性变体 1 处**：`ideation.md` 声明「只做两件事」（读规则 + 委托），无「按参数分派」「守保护区」——因脑暴无多分支路由、无保护区concern，是真实差异非漏写，薄壳与 DRY 精神不变。
- [x] AC6（目录软链自动托管·实跑）(auto·可靠)：隔离假 HOME 实跑 `setup.sh`，3 新命令 `~/.claude/commands/butler/{milestone,upgrade,ideation}.md` 经**目录软链**全部 `test -e` 通过、R1 的 prd+review 仍可达、**未改 `setup.sh` 一行**——R1 「整目录软链」红利兑现。幂等重跑 5/5 复现、无 `butler/butler` 套娃。
- [x] AC7（文档更新）(auto + 人读)：`capabilities.md` 命令表把 `/ideation`·`/milestone`·`/butler-upgrade` 三行**转换**为 `/butler:*` 一等入口（真源列指命令文件、路径 `.claude/commands/butler/<name>.md`）+ **删** `/review` 旧行（并入既有 `/butler:review`）；`README.md` `butler/` 子树补 milestone/upgrade/ideation 三命令。
- [x] AC8（切版三载体对齐）(auto·可靠)：判 **MINOR**（纯新增 3 命令、无破坏面）；`VERSION`=2.8.0、`CHANGELOG.md` 顶条 `[2.8.0]`、`migrations/v2.8.0.md` 区间 `v2.7.0→v2.8.0` 三者一致；git tag v2.8.0 于发布提交时打（见 Handoff）。
- [x] AC9（边界守恒）(auto·可靠)：`git diff --stat` — 改动仅落 `.claude/commands/butler/**`（3 新）+ 6 处触发名文档 + `capabilities.md`/`README.md` + 发布层（VERSION/CHANGELOG/migrations）+ `.ai/` 本迭代产物/台账；`Coder/**` 规则**算法**、`templates/**`、四件套 schema、hook、`setup.sh` 一行未动（触发名迁移只改 `butler-upgrade.md §2`+`logic-protocol.md §activation`+`migration-schema.md` 引用，均非算法）。

# Verification Results
- AC1/AC6：隔离假 HOME `HOME=<tmp> bash scripts/setup.sh` ×2（首装 + 幂等）——软链报「5 个命令」、`test -e` 三新命令 + prd/review 全绿、目录软链 `~/.claude/commands/butler`→仓库命名空间目录、无套娃。
- AC2/AC3/AC4/AC5：读三命令文件核薄壳四要点齐 + 委托真源 section 锚点回真源核——milestone-schema §5.3/6.1/6.4/6.5/7.1/7.3-7.5、butler-upgrade §3/4/5/6/6.3/7/8、ideation-engine §3/3.1/3.2/3.3/3.4 **逐一真实存在**。
- AC3 触发名：`git grep '/butler-upgrade' -- '*.md'` — 活规则文档残留全部合法（新名 `/butler:upgrade` 带「旧名 `/butler-upgrade`」注解 / `butler-upgrade.md` 文件名引用 / 本迭代规划稿在讨论迁移本身 / `.ai/iterations` 与 RUN_LOG 历史归档），**零裸旧名**。
- AC7：读 capabilities 命令表（3 行已转换、`/review` 行已删）+ README `butler/` 子树（5 命令齐、`└──` 收尾正确）。
- AC8：`cat VERSION`=2.8.0、CHANGELOG 顶条 `[2.8.0] - 2026-07-14`、`migrations/v2.8.0.md` 首行区间一致。
- AC9：`git diff --stat` 18 改 + 4 新（3 命令 + migration），逐文件核无越界。

# Gate Coverage
- 通用质量门禁：不破坏分层（命令层改动不入 `Coder/` 算法、不入 `templates/`）✓ / 新命令 README 目录树注册（无隐式依赖）✓ / 文件名互引不写绝对路径 ✓ / 三命令 frontmatter 说人话无裸术语 ✓ / 产物链未动 ✓。
- Active Profiles：无（规则仓，未命中 domain profile）。
- Tech Plan Alignment：DD1/DD2/DD4/DD5/DD6 全兑现；**DD3 计划-实际差异**：DD3/T4 字面「只改 §2 一行」，实际按 AC3「全仓无残留」迁 6 处命令名——`butler-upgrade.md §2`（触发词列表）+ `logic-protocol.md §activation`（2 occurrence + 加旧名注）+ `migration-schema.md`（正文引用）+ `HUMAN_GUIDE.md` + `architecture.md` + `debt.md`。6 处全触发名、非算法，DD3 原则（触发名≠算法、与 R1 一致）不破；差异为计划低估了「触发名」在活文档里的分布面，非范围外扩张。T1–T8 全落。
- References Compliance：N/A（无外部参考资料）。

# Independent Review（标准模式·未升格）
- 本迭代低风险纯机械（3 薄壳复制 R1 已验范式 + 触发名字符串迁移 + 文档 + 幂等切版），P5 自评 + 客观隔离 HOME 实跑无 shaky 处，按标准模式**不强制**独立复核（区别于 R1 危险模式的强制升格）。若后续 R3/R4（`preference` 多子命令、`loop`/`dangerous` 加风险闸）复杂度上来，再按 dangerous/复核标准决定是否升格。

# Remaining Risks
- 命令菜单「可见性」headless 不可实敲——沿用 R1/R2 代理验法（文件存在 + 命名空间结构正确 + 经目录软链 `test -e` 可达 + `setup.sh` 报命令数）。命名空间机制经 R1 claude-code-guide 查证 + 两轮隔离 HOME 实跑，可靠。
- `[global-install]` / `[restamp]` 之外无部署面动作；`/butler:upgrade` 升级协议**仍从未在真实老项目端到端实跑**（历史欠债，见 `debt.md`，本迭代只是给它换了触发名 + 落命令文件，未消该债）。

# Handoff / Next Step
- P5 通过（AC1–AC9 全过、0 阻断项）→ 进原子收口五步（归档四件套 + 交付 md/html + 台账/路线图 + 知识文件夹前滚 + 收口自检）+ 切版 git 仪式（feat 提交 + 独立 chore(release) 提交 + 本地 tag v2.8.0）。
- MILE-0005 R2 达成即交还；R3（`preference`）/R4（`loop`+`dangerous`）设计未锁、不擅自连跑。标准模式授权范围：ACK 的 R2 scope 一路推到收口 + 提交 + 推分支 + PR #3 增长；**不合并 main、不推 tag v2.8.0 到远端**（待用户授权）。
