# Verification Summary
- 覆盖范围：butler 持久运行模式外化为 `.ai/local-constraints.md`「Butler 功能开关」段、会话起始读取接线、dangerous 跨会话语义改写、里程碑 active 归属/closed 不写入显式化，及 SSOT/人类文档传播。
- 总体结论：AC1–AC13 全部满足；逐 AC grep 落点 15/15 通过，AC12 零改动经 `git diff` 确认，dangerous-engine 旧"不续开"生效规则已被改写（仅保留解释性风险引用）。ITER-0006 闭合。

# AC Status
- [x] AC1: local-constraints-schema 新增「Butler 功能开关」段 + 字段（dangerous / independent_review，默认 off）+ §1/§2 目标字段更新
- [x] AC2: §4.1 读写口径四条（会话起始读 / 命令回写 / 手改 / dangerous announce-on-read 自动生效）
- [x] AC3: preference 排除 + legacy 兼容（旧无段全 off、独立 Review Policy 作 legacy 仍尊重）
- [x] AC4: logic-protocol §1.3 会话起始读取功能开关并激活
- [x] AC5: logic-protocol §4 Dangerous 条目改写（外化 + 跨会话声明后自动进入）+ Review independent_review 落点
- [x] AC6: dangerous-engine §3 改写跨会话语义（声明后自动生效）+ §3.1 + 安全取舍风险标注
- [x] AC7: mcv-deployment §4 生成含功能开关段 + 安全默认全 off
- [x] AC8: lifecycle §P1 + milestone-schema §7.2/§7.4 显式化 active 归属 / closed 不写入
- [x] AC9: rule-card 补功能开关持久落点 + dangerous announce-on-read，SSOT 单写
- [x] AC10: HUMAN_GUIDE 新增「项目级功能开关」子节 + dangerous 跨会话行为/风险 + 里程碑归属边界
- [x] AC11: README local-constraints-schema 描述纳入"统一持久落点"
- [x] AC12: preference-engine / hooks / iteration-schema 零改动；台账 current 真源、preference 外置表述未被矛盾
- [x] AC13: ITER-0006 收口（本报告产出即完成最后一环）

# Verification Results
- AC1–AC11：逐 AC `grep` 关键句命中各目标文件（15/15 ✓，见 per-AC landing 批次）。
- AC2/AC6：announce-on-read 在 local-constraints-schema §4.1、dangerous-engine §3.1、logic-protocol §1.3/§4、rule-card、HUMAN_GUIDE 五处一致表述；dangerous-engine 旧"会话结束即回 Standard、不自动续开"生效规则已替换为 §3.1 跨会话声明后自动进入，仅 §3.1 风险说明保留对旧设计的解释性引用（非生效规则）。
- AC9 SSOT：`grep RULE_CARD_CONTENT templates/CLAUDE.md.template` = 1；`grep "Butler 功能开关|dangerous:" templates/CLAUDE.md.template` = 0 → 模板无手写功能开关内容，SSOT 单写成立。
- AC12：`git diff --name-only | grep -E preference-probe-engine|templates/hooks|iteration-schema` 空 → 三者零改动。
- AC8：lifecycle / milestone-schema 归属边界与台账 `current` 判定一致（`current=MILE` 归属、`current: none` 独立）。

# Gate Coverage
- 通用质量门禁：遵守 CLAUDE.md 五约束——未破坏三层分层（改动落 00/20/65 + 文档/模板）、未破坏产物链、新增功能开关配置已在 README 注册、模板 SSOT 单写、frontmatter 未动。
- Active Profiles：未命中（Markdown 规则仓库），N/A。
- Tech Plan Alignment：TECH_PLAN 六项 Design Decisions 全兑现——整合而非并列（Review Policy 并入功能开关 + legacy 保留）、读取接线写进 logic-protocol §1、dangerous 持久但每会话亮明、preference 排除、Ask A 仅澄清不改机制、rule-card 增量克制。
- References Compliance：本轮无 `.ai/references/`，N/A。

# Remaining Risks
- 危险模式跨会话自动生效削弱 dangerous-engine §3 原"不续开"安全冗余——以 announce-on-read（每会话起始强制显式声明 + `/dangerous off` 即关）兜底，§3.1 与 HUMAN_GUIDE 如实标注"忘关则新会话声明后自动进入自治"风险，并建议仅在可隔离/可回滚环境保留 on。用户知情拍板。
- 功能开关靠规则纪律保证"会话起始必读"（无 hook 强制），与现有读取顺序同源同险。
- 已部署旧项目未自动迁移功能开关段——靠 legacy 全 off 兼容，正式迁移属 `butler-upgrade` 范围，本轮未做。

# Handoff / Next Step
- 任务闭合，无遗留。后续可选项（非本轮）：把功能开关段纳入 `butler-upgrade.md` 迁移协议、或扩展更多项目级开关。
