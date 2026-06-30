---
状态: ack-frozen
ACK 日期: 2026-06-30
---

> ⚠️ 危险模式：本产物由模型过 dangerous-engine §5.1 自审门后自主 ACK 冻结，未经用户确认（ITER-0014，2026-06-30）。

# Goal

- 把"已部署项目升级到最新 butler"从"模型每次现场推导差异"变成"照已记录的迁移配方执行"——版本升级成为确定性 SOP。

# In Scope

- 新增迁移配方格式规范 + 配方台账目录 + 三份回填配方。
- 改写 `butler-upgrade` 为配方执行器，并补 `.claude/hooks/` 副本同步。
- 把"切版时记录迁移配方"写进版本治理流程。
- 危险模式护栏（审计 / 横幅 / P5 强审 / 披露）。

# Out of Scope

- 不实际把 butler 切版到下一个版本号（切版属用户门控动作，收口后另行建议）。
- 不改 hook 代码（`templates/hooks/`）本身。
- 不迁移 / 重写历史 `deliveries/`，不处理目标项目自身的业务版本。
- 不改四件套字段结构、lifecycle 分流、对话层规则。

# Acceptance Checklist

- [ ] AC1: 新增 `Coder/20_Workflow_Lifecycle/migration-schema.md`，定义配方文件位置（`migrations/vX.Y.Z.md`）与命名、每份必含字段（区间 / 聚合 ITER / 对部署项目影响 / 迁移步骤 / 无需动作）、以及"幂等 + 起始态校验 + 冲突退回真人 ACK"的契约。
- [ ] AC2: migration-schema 明确定义 typed 操作标签集（至少 `[rename]` / `[add-field]` / `[regen-claude]` / `[sync-hooks]` / `[restamp]` / `[no-op]`），每个写清何时用 + 幂等判据（先校验起始态再动）。
- [ ] AC3: 建立 `migrations/` 目录并回填 `v1.1.0.md` / `v1.2.0.md` / `v1.3.0.md` 三份配方，各自如实反映该版对部署项目的真实影响，均含起始态校验与冲突处理：v1.1.0=新增 `ledger_status` hook 需同步 hook 副本 + `local-constraints` 补 `preference` 字段 + delivery HTML 模板；v1.2.0=rule-card 变更需重生成 `CLAUDE.md` 内联段；v1.3.0=rule-card 变更需重生成 + concept-schema 新增可选块（无强制动作）。
- [ ] AC4: `butler-upgrade.md` 改写——侦察阶段读版本戳后**收集 (目标, 当前] 区间配方**；执行阶段**按序幂等应用配方**而非现场推导；内容 diff 降级为"应用前校验 + 冲突兜底"；显式新增 `.claude/hooks/` 副本同步步骤（覆盖 `mcv-deployment.md §5.4` 缺口）。
- [ ] AC5: `butler-upgrade.md` 保留无版本戳 / 前版本化老项目的**全量兜底路径**——无配方链起点时回退到现状全量对账，不被新执行器逻辑卡死。
- [ ] AC6: `versioning-schema.md §5` 切版流程新增一步"记录迁移配方"（产出 `migrations/vX.Y.Z.md`；本版对部署项目无影响也必须写 `[no-op]` 配方），并指针引用 `migration-schema.md`。
- [ ] AC7: `Coder/README.md` 注册 `migration-schema.md`（目录树、"其中"逐文件说明、与 versioning / butler-upgrade 的关系）三处齐全。
- [ ] AC8: VERIFY 中对照说明——"配方为主干 + 幂等 + 起始态校验 + 冲突退回真人 ACK"与现有"版本号为辅、内容差异为主"原则不冲突（配方不取代 diff，而是把 diff 从"主驱动"降为"冲突兜底"）。
- [ ] AC9: 四件套 + 新规则文件正文符合 `artifact-style.md`（讲人话、反啰嗦、CONCEPT 顶部分层）；收口前自检无 §2 反面词残留在字段正文。
- [ ] AC10: 本仓 CLAUDE.md 五约束自检通过（分层不混 / 产物链不破 / 新文件已注册 / 模板单一来源 / frontmatter audience+scope 合规）。
- [ ] AC11: 危险模式护栏落实——`.ai/RUN_LOG.md` 记录每处自主 ACK、三件套顶部带危险横幅、P5 强制完整审查（含独立复核尝试）、交付总结显式披露自治事实。

# Verification Method

- AC1 / AC2: 读 `migration-schema.md`，核对位置 / 命名 / 必含字段 / 契约 / 六个标签语义齐全。
- AC3: 读三份配方，逐一比对该版实际改了什么（对照 `CHANGELOG.md` 与各 ITER），确认步骤如实、含起始态校验。
- AC4 / AC5: 读 `butler-upgrade.md`，确认执行器流程 + hook 同步步骤 + 无戳老项目兜底路径在位。
- AC6: 读 `versioning-schema.md §5`，确认新步骤 + 指针。
- AC7: grep `Coder/README.md` 命中 migration-schema 的三处注册。
- AC8: VERIFY 写一段对照论证，引 `versioning-schema.md §7` 与新执行器的冲突处理逻辑。
- AC9: 收口前自检扫四件套 + 新文件，grep 反面词；通读 CONCEPT 确认分层。
- AC10: 对照本仓 CLAUDE.md 五条逐项自检，写进 Gate Coverage。
- AC11: 核对 `RUN_LOG.md` 条目、三件套横幅、P5 章节、交付总结披露段均在位。

# Open Questions / Risks

- 风险：配方靠"切版时记录"这条规则纪律维持，无 hook 机械强制——若漏记，升级又退回现推。用 §5 必做步 + `[no-op]` 兜底降低漏记概率，但不能根除（同版本治理本身"无 hook 强制"的已知取舍）。
- 风险：回填配方依赖我对历史版本影响的判断，可能漏项；用 P5 独立复核对照 `CHANGELOG` 交叉验证。
- 风险：危险模式自治，无人逐阶段把关——靠 P5 强制完整审查 + 独立复核 + RUN_LOG 留痕兜底。
