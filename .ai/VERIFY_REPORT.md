# Verification Summary

- 提交与切版 SOP 就地扩写进 `versioning-schema.md`：新增 §5「提交规约」（commit message 格式 + 发布形态 + 何时提交 + 非门禁声明 + 署名 trailer），原 §5 切版流程顺移 §6 并扩到 git 操作层（预检 + git 序列 + 切版后自检 + 两路径 + 里程碑引用），原 §6-8 顺移 §7-9。
- 改动恰好 7 文件：1 核心（versioning-schema）+ 3 顺移引用修正（migration-schema / butler-upgrade / mcv-deployment）+ 3 指针（README / CLAUDE / HUMAN_GUIDE）。未碰任何不变量文件。
- 总体结论：11 条 AC 全部满足，可收口。

# AC Status

- [x] AC1 ✓ §5.1 定义 `type(scope): 中文描述 (ITER-NNNN)`，列出 7 类 type / scope 口径 / 中文描述 / 迭代号尾注。
- [x] AC2 ✓ §5.2 定义 `chore(release): vX.Y.Z — 聚合 ITER-A~B (级别)`，与日常提交分列。
- [x] AC3 ✓ §5.3 何时提交 / 一次装什么 / body 引用不复述；§5.4 显式声明非 hook 门禁、靠纪律 + 收口自检。
- [x] AC4 ✓ 抽 6 条历史提交（`chore(release): v1.5.0…`、`feat(lifecycle): …(ITER-0017,0018,0019)`、`feat(hook): …(ITER-0019)` 等）逐条套规约，全含 `Co-Authored-By` trailer，零冲突。
- [x] AC5 ✓ §6 扩为完整仪式：§6.2 预检复用一致性自检 5 不变量 + 区间 closed / 无悬挂 active；§6.3 git 精确序列（add→commit→tag→push）；§6.4 切版后自检（VERSION==tag==CHANGELOG 顶条）。
- [x] AC6 ✓ §6.1「提交 ≠ 切版」两路径：日常收口 commit+push 不切 tag / 发布按需聚合切版。
- [x] AC7 ✓ §6.3 step5 里程碑发布引用 `milestone-schema.md` 收口机制，不重写。
- [x] AC8 ✓ frontmatter title 改「提交与版本治理协议」、scope 补提交规约 + 切版仪式。
- [x] AC9 ✓ README §139 / CLAUDE.md VERSION 行 / HUMAN_GUIDE 注释均同步新范围。
- [x] AC10 ✓ rule-card 裁决=不改（理由见下）；PROJECT.md 现行约束收口前滚补提交规约一句。
- [x] AC11 ✓ 不变量文件 git diff 名单核对未动（详见 Gate Coverage）。

# Verification Results

- AC1/2/3/5/6/7: 读改后 versioning-schema §5/§6，逐段核对格式 / 两形态 / 何时提交 / 非门禁 / 预检 / git 序列 / 后检 / 里程碑引用齐备。
- AC4: `git log -6 --format` 抽样，逐条对照 §5.1/§5.2 格式，全部命中（type(scope) + 中文描述 + (ITER-NNNN) + Co-Authored-By；release 用 chore(release) + 聚合区间 + 级别）。
- AC8/9: 读 frontmatter；`grep versioning-schema.md` 在 README/CLAUDE/HUMAN_GUIDE 三处描述均已含提交规约 + 切版仪式。
- AC10: rule-card 未改（DD7 理由：提交规约非产物链硬门、非封闭枚举、不进 phase_gate，属纪律类，收录会稀释 rule-card"强制产物集 + 机械约束"定位）；PROJECT.md 现行约束段补一行。
- AC11: `git diff --name-only` 确认 VERSION / CHANGELOG.md / rule-card / CLAUDE.md.template / concept·acceptance·tech-plan·verify schema / templates/hooks 全部无输出（未碰）；migration-schema 仅 §编号引用修正、正文语义不变。

# Gate Coverage

- 通用质量门禁：改后 versioning-schema §1-9 编号连续无断层；全仓 `versioning-schema.md §N` 引用复查——外部 6 处已正确指向 §6/§7/§8，无旧指向残留（唯一 `§5` 出现在 `.ai/AC_LIST.md`，系冻结验收记录、非活引用）。
- Active Profiles：无（纯规则正文，未动 hook Python）。
- Tech Plan Alignment：DD1-DD7 全部兑现——DD1 §5 插入 + 顺移 + 修引用；DD2 type 集借鉴声明；DD3 两路径；DD4 复用一致性自检；DD5 里程碑引用；DD6 非门禁 + 署名；DD7 rule-card 不改。
- References Compliance：N/A（本轮无 `.ai/references/` 参考资料）。

# Remaining Risks

- Should Fix（不阻断）：提交规约作用域限 butler 仓自身，目标项目提交规约推广未做——已在 §9 边界显式声明，留作后续按需扩展。
- 提交规约非机械门禁，与"会话起始必读""切版靠纪律"同源，靠纪律 + 收口自检兜底（已在 §5.4/§9 写明，属既有同类风险，不新增）。

# Handoff / Next Step

- 任务闭合，进入收口（archive + delivery + 台账 close + PROJECT 前滚 + 自检）。
- 提交推送 / 是否聚合切版 MILE-0001 等外发动作，待用户显式指令。
