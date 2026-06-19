# Goal
- 支撑 AC1–AC16：preference 接入 local-constraints 作 per-project 抑制开关（默认 on），外置 $PREF 仍为跨项目真源，反转四处排除措辞。下文给精确锚点。

# Files / Modules to Change

### 1. `local-constraints-schema.md` 【AC1/AC2/AC3】
- §2 line 19 必填字段：`Butler 功能开关`（部署时即以安全默认全 off 生成）→ 改为"（部署时生成：dangerous / independent_review 安全默认 off、preference 默认 on）"。
- §3 模板「Butler 功能开关」段：在 `independent_review` 行后加 `- preference: on            # on|off，默认 on。本项目偏好探针采集抑制开关；on≠强制采集（实际采集仍需全局同意），off 即本项目不采集/蒸馏/反哺。consent/数据真源在外置 $BUTLER_PREF（跨项目），本开关不双写（见 70_Extension_Preference §2.5）`。
- §4.1：把 line 65「**preference 不纳入**」整条反转为「**preference（per-project 抑制开关）**」——本项目是否运行探针 = 全局未 `/preference off` ∧ 外置 `$PREF` consent=granted ∧ 本项目 `preference ≠ off`，三者全真才采集/蒸馏/反哺；`preference: off` 只抑制本项目，不改全局 consent、不动 $PREF 数据、不影响他项目；缺字段=视为 on；外置 $PREF 仍是 consent/signals/profile 跨项目唯一真源，本开关不双写。此条为该语义 SSOT。

### 2. `preference-probe-engine.md` 【AC4/AC5】
- §2.1 末尾加一句：默认常驻**受项目级抑制开关约束**——本项目 `.ai/local-constraints.md` `preference: off` 时不在本项目采集/蒸馏/反哺（见 §2.5）。
- 新增 §2.5「项目级抑制开关（per-project）」：定义 local-constraints「Butler 功能开关」`preference: on|off`（默认 on）为本项目采集闸；**生效优先级**：全局 `/preference off`（§2.3 隐私总开关）> 外置 `$PREF` consent（§2.4）> 项目 `preference` 开关；三层全放行才在本项目运行。强调它与全局 consent 分管不同层面（全局=能不能、项目=要不要），故非双真源；真源归属与读写口径以 `local-constraints-schema §4.1` 为准。

### 3. `logic-protocol.md` 【AC6/AC7】
- §1.3：在 `independent_review: on` 项后加 `preference: off` → 本项目抑制偏好探针（不采集/蒸馏/反哺）；默认/缺省视为 on；语义以 `local-constraints-schema §4.1` 为准。
- §4 Preference Mode 条目（line 91）末尾补：per-project 抑制开关持久在 `.ai/local-constraints.md`「Butler 功能开关」`preference`（默认 on）；外置 `$BUTLER_PREF` 仍为 consent/数据跨项目真源。

### 4. `mcv-deployment.md` §4 【AC8】
- line 95「必含「Butler 功能开关」段」描述：原"安全默认全 off（dangerous: off、independent_review: off）"→ 改为"dangerous: off、independent_review: off、preference: on（preference 默认 on 安全：实际采集仍需全局同意，未同意时不采集）"。

### 5. `rule-card.md` 【AC9】
- line 44 末「偏好系统不在此（跨项目、外置 `$BUTLER_PREF`）」→ 反转为「preference 作**本项目抑制开关**也在此段（默认 on；on≠强制采集，仍需全局同意）；consent/数据真源仍在外置 `$BUTLER_PREF`（跨项目），本开关不双写」。

### 6. `HUMAN_GUIDE.md` 【AC10】
- §5「项目级功能开关」表（line 142-145）加行：`| `preference: on\|off` | 本项目偏好探针采集开关（默认 on；off 即本项目不采集） |`。
- line 149 注「（注：偏好探针不在这里——它是跨项目的……）」→ 更新为「偏好探针的总开关/数据是跨项目的（外置 `$BUTLER_PREF`），但**本项目可用 `preference: off` 单独抑制**；on≠强制采集，仍需全局同意」。

### 7. `Coder/README.md` 【AC11】
- line 130「偏好系统因跨项目不纳入」→ 反转为「preference 以 per-project 抑制开关纳入本段（默认 on），但 consent/数据真源仍在外置 `$BUTLER_PREF`（跨项目）」。

# Design Decisions
1. 抑制层而非接管：项目开关=本项目采集闸，与全局 consent 分管不同层面 → 非双真源（AC3/AC4/AC13）。
2. 默认 on 安全：on≠强制采集，仍需全局同意（AC1/AC8 文案显式写明）。
3. 真源不变：外置 $PREF 仍 SSOT，schema/engine 反复申明（AC13）。
4. 不需 announce-on-read：preference 低风险，读到即遵循（区别于 dangerous）。
5. 反转彻底：四处排除句全改写，grep 校验旧句消失（AC12）。

# Test / Verify Strategy
- AC1-AC11：逐 AC grep 各目标文件命中新句。
- AC12：全仓 grep 旧排除句「preference 不纳入 / 偏好系统不在此 / 偏好探针不在这里 / 偏好系统因跨项目不纳入」应 0 命中。
- AC13：grep "真源/外置 $BUTLER_PREF/不双写" 在 schema·engine·rule-card·README 表述一致；无"项目级真源"矛盾。
- AC14：`git diff --name-only` 确认 engine §5/§6/§7（算法）、§4（存储契约）、§3、§9 段未被改动（仅 §2 区域变更）；ledger_status/四 schema/versioning-schema 不在改动名单。验证手段：diff 仅触及 §2.1/§2.5 区。
- AC15：人工核对五约束。
- AC16：归档/delivery/台账核对。

# Rollback
- 纯文档/模板改写，无运行态副作用。回退 = `git revert` 本迭代提交。
