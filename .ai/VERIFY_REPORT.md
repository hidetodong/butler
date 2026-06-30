> ⚠️ 危险模式：本验证报告由模型在无人值守自治下产出，P5 经强制完整审查 + 独立复核（dangerous-engine §7.3），未经用户确认（ITER-0014，2026-06-30）。

# Verification Summary

- 把"已部署项目升级到最新 butler"从"现场推导差异"改为"照迁移配方执行"：新增 `migration-schema.md` + `migrations/` 三份回填配方，`butler-upgrade` 改执行器并补 hook 同步，`versioning-schema §5` 加"记配方"必做步，README 三处注册。
- 独立复核（fresh-context 子 agent）查出 1 个实质 bug（v1.1.0 漏 `[regen-claude]`），已修复并定点复查通过；其余 AC 满足，无遗留 Must Fix。

# AC Status

- [x] AC1 ✓ migration-schema §2/§3/§5 把位置、命名、必含字段、幂等/漂移契约都定清楚了。
- [x] AC2 ✓ §4 六个 typed 标签每个都写了何时用 + 幂等判据。
- [x] AC3 ✓（修复后）三份配方如实；独立复核查出 v1.1.0 漏 `[regen-claude]`（`git log -- templates/rule-card.md` 证实 ITER-0008/0009/0010 均改过 rule-card），已补步 + 影响段，复查通过。
- [x] AC4 ✓ butler-upgrade §3.5 收集区间配方、§5 按序幂等执行、diff 降为冲突兜底、§6.4 补 hook 同步。
- [x] AC5 ✓ 无版本戳老项目走 §4 全量首次升级兜底，完整可走、不被执行器卡死。
- [x] AC6 ✓ versioning §5 第 4 步"写迁移配方" + `[no-op]` 兜底 + 指针引用 migration-schema。
- [x] AC7 ✓ README 目录树（行 55）、逐文件说明、butler-upgrade 关系行三处注册（独立复核确认）。
- [x] AC8 ✓ 见 Gate Coverage 的"配方/diff 不冲突"论证。
- [x] AC9 ✓ 新文件 + 四件套字段正文 grep 无 §2 反面词；CONCEPT 顶部带"一句话"分层。
- [x] AC10 ✓ 本仓 CLAUDE.md 五约束自检通过（见 Gate Coverage）。
- [x] AC11 ✓ RUN_LOG 五条审计（含 P5-review）、三件套横幅、P5 强审 + 独立复核、本交付总结披露自治——收口产出后齐全。

# Verification Results

- AC3：独立复核交叉对照 `deliveries/ITER-0008~0010` 与 `git log -- templates/rule-card.md`，证实三迭代均改 rule-card → v1.1.0 必须含 `[regen-claude]`；已修 `migrations/v1.1.0.md`，并在 `migration-schema.md §4` 加"漏判防线"判据（区间内任一迭代动过 rule-card 即必须 regen）防复发。
- AC4/AC5：通读 `butler-upgrade.md`，§5 引用的 §6.1/§6.2/§6.4 均存在、无悬空引用；§4 兜底六步在位且末尾建立配方链起点。
- AC7：grep `Coder/README.md` 命中目录树、逐文件说明、butler-upgrade 关系行三处。
- 其余 AC：读对应文件逐项核对，证据见 AC Status。

# Gate Coverage

- 通用质量门禁：新规则文件 frontmatter 合规、措辞用"必须/不得/应"、节号连续；三份配方格式统一。
- Active Profiles：未命中（Markdown 规则仓），省略。
- Tech Plan Alignment：六项设计决策全兑现——配方为主干/diff 兜底、`migrations/` 放仓库根、纯 Markdown + typed 标签、补 hook 同步、无戳兜底、本迭代不切版。
- References Compliance：N/A（本轮无 `.ai/references/`）。
- AC8「配方/diff 不冲突」论证：现有"版本号为辅、内容差异为主"（versioning §7）防的是"盲目按版本号判定是否升级"。新执行器不抛弃 diff——每步 `[regen-claude]`/`[rename]`/`[add-field]` 都先校验起始态（migration-schema §5），与配方预期不符即停、退回 ACK。配方只是把 diff 从"主驱动"降为"冲突哨兵"，§7 安全性不变；versioning §7 已同步改写为这一表述，两处口径一致。
- CLAUDE.md 五约束：①分层不混（新 schema 归 20 层 SOP）；②产物链不破（四件套字段未动）；③新文件 migration-schema 已在 README 三处注册；④模板单一来源（配方不碰 rule-card SSOT）；⑤frontmatter audience+scope 合规。

# Independent Review

- 复核方式：fresh-context 子 agent（general-purpose，不带本会话上下文，spec-only 逐 AC + 交叉验证配方/CHANGELOG）。
- 逐 AC 裁决：confirm 7（AC1/2/4/5/6/7）；refute 4（AC3 实质 bug；AC8/9/10/11 因 P5/收口产物当时未产出）。
- refute 处置：AC3 Must Fix（v1.1.0 漏 `[regen-claude]`）已修复 + 加防复发判据，定点复查通过；AC8–AC11 由本 P5 报告 + 收口三步补齐，复查通过。
- 结论：Must Fix 全部关闭，通过、可收口。

# Remaining Risks

- 配方靠"切版时记录" + `[regen-claude]` 漏判防线维持，无 hook 机械强制——降低漏记概率但不根除（同版本治理"无 hook 强制"既有取舍）。
- 回填配方覆盖 v1.1.0~v1.3.0；更早的前版本化项目走 §4 全量兜底，不依赖配方链。

# Handoff / Next Step

- 任务闭合，进入收口三步（归档 `iterations/ITER-0014/` + `deliveries/ITER-0014-migration-ledger.{md,html}` + 台账置 closed）。
- 建议（用户门控、非本迭代范围）：把本迭代发为 v1.4.0 并按新 §5 必做步写 `migrations/v1.4.0.md` 做 dogfood。本迭代只新增 `migration-schema` + `migrations/` 数据 + 改 `Coder/` 规则正文（运行时读、不进目标项目），未动 `templates/rule-card.md`，故 v1.4.0 配方应为 `[no-op]` + `[restamp]`——正好演示 `[no-op]` 场景。
