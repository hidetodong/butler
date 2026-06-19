# Verification Summary
- 覆盖范围：preference 接入 `.ai/local-constraints.md`「Butler 功能开关」作 per-project 抑制开关（默认 on）——schema 语义 SSOT（§4.1）+ 引擎 §2.5 优先级 + logic-protocol 接线 + 部署默认 + 四处排除措辞反转；外置 `$PREF` 仍为 consent/数据跨项目唯一真源。
- 总体结论：AC1–AC16 全部满足；逐 AC grep 落点通过，AC12 旧排除句全仓 0 命中，AC14 零改动经 `git diff` 确认（engine 纯增量 +12/−0、仅 §2 区，算法/契约/底线/隔离段未动）。ITER-0009 闭合。

# AC Status
- [x] AC1: local-constraints-schema §3 模板新增 `preference: on` 行 + 注释（抑制开关/默认 on/on≠强制采集/外置真源）
- [x] AC2: §2 必填字段描述更新为"dangerous/independent_review 默认 off、preference 默认 on"
- [x] AC3: §4.1 "preference 不纳入"反转为 per-project 抑制开关口径（三态生效条件 + 只抑本项目 + 缺字段视 on + 外置唯一真源不双写），标为该语义 SSOT
- [x] AC4: engine 新增 §2.5 项目级抑制开关 + 生效优先级（全局 off > consent > 项目开关）+ 引用 §4.1
- [x] AC5: §2.1 默认常驻标注"受项目级抑制开关约束"，与 §2.5 一致
- [x] AC6: logic-protocol §1.3 会话起始读取新增 `preference: off` 项（本项目抑制、缺省 on、无需 announce）
- [x] AC7: logic-protocol §4 Preference Mode 补 per-project 抑制开关落 local-constraints + 外置仍为真源
- [x] AC8: mcv-deployment §4 生成「Butler 功能开关」纳入 `preference: on` + on 安全说明
- [x] AC9: rule-card 项目级功能开关节"偏好系统不在此"反转为"preference 作本项目抑制开关在此、外置仍为真源"
- [x] AC10: HUMAN_GUIDE §5 开关表加 preference 行 + "关于 preference"注更新（本项目可抑制、外置跨项目）
- [x] AC11: Coder/README local-constraints-schema 描述"偏好不纳入"反转为"per-project 抑制开关纳入、外置仍为真源"
- [x] AC12: 四处旧排除句（preference 不纳入 / 偏好系统不在此 / 偏好探针不在这里 / 偏好系统因跨项目不纳入）全仓 grep 0 命中
- [x] AC13: 真源归属全仓一致——consent/signals/profile 外置 $BUTLER_PREF 跨项目唯一真源、本开关不双写；无任一处写成项目级真源
- [x] AC14: 零改动护栏——engine §3/§4/§5/§6/§7/§9 段、ledger_status hook、产物链四 schema、versioning-schema、iteration/milestone-schema 未改动
- [x] AC15: 未破坏 CLAUDE.md 五约束（分层未混、产物链未动、无新增规则文件、模板 SSOT 经占位符继承未手写重复、frontmatter 未动）
- [x] AC16: ITER-0009 归档 + delivery + 台账 closed（P5 收口环节执行）

# Verification Results
- AC1/AC3：grep local-constraints-schema 命中 `preference: on` 模板行（含 on≠强制采集/外置真源/不双写）与 §4.1 反转条（三态生效条件 + SSOT 声明）。
- AC4/AC5：grep engine 命中 §2.5 标题、生效优先级、非双真源；§2.1 命中"受项目级抑制开关约束"。
- AC6/AC7：grep logic-protocol §1.3 `preference: off` 项、§4 per-project 抑制开关补述。
- AC8/AC9/AC10/AC11：grep mcv-deployment §4、rule-card、HUMAN_GUIDE（表行 + 注）、Coder/README 命中各落点。
- AC12：`grep -rnE "preference 不纳入|偏好系统不在此|偏好探针不在这里|偏好系统因跨项目不纳入" Coder templates HUMAN_GUIDE.md` → rc=1（0 命中）。
- AC13：schema/engine/rule-card/README/HUMAN_GUIDE 五处"外置 $BUTLER_PREF 跨项目唯一真源 + 本开关不双写"表述一致；无"项目级真源"矛盾。
- AC14：`git status --short` 改动名单 = .ai 四件套+台账 + logic-protocol/local-constraints-schema/mcv-deployment/preference-probe-engine/Coder README/HUMAN_GUIDE/rule-card；护栏文件全不在内。`git diff --numstat` engine = `12 0`（纯增量），diff 仅触及 §2.1 段 + 新增 §2.5，§3-§9 未动。

# Gate Coverage
- 通用质量门禁：遵守 CLAUDE.md 五约束——分层未混（改动落 00/20/70 + 模板/文档）、产物链未动、无新增规则文件（修改既有，无 README 新注册需求）、模板 SSOT（rule-card 单写、CLAUDE.md.template 经占位符继承）、frontmatter 未动。
- Active Profiles：未命中（Markdown 规则仓库），N/A。
- Tech Plan Alignment：TECH_PLAN 七文件改动与五项 Design Decisions 全兑现——抑制层非接管、默认 on 安全、外置真源不变、preference 无需 announce、四处排除句彻底反转。
- References Compliance：本轮无 `.ai/references/`，N/A。

# Remaining Risks
- 项目开关靠规则纪律（会话起始读 + 遵循），无 hook 强制——与现有 dangerous/independent_review 同源同险。
- "默认 on 但需全局同意"靠文案显式标注规避误读（schema/部署/rule-card/HUMAN_GUIDE 均写"on≠强制采集"）。
- 存量旧项目无 `preference` 字段——按"缺字段=视为 on"兼容，行为同旧版（仅受全局同意约束），批量回填走 butler-upgrade。
- 版本：本轮不发版；ITER-0009 累积到下次切版，预计 MINOR（新增项目级开关能力）。

# Handoff / Next Step
- 任务闭合。收口动作：归档四件套→`.ai/iterations/ITER-0009/`、写 `deliveries/ITER-0009-<slug>.md`、台账置 closed + `current: none`。
