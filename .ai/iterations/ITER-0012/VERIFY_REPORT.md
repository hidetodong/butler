# Verification Summary

- 给四件套补了一份书写口径（讲人话 + 反啰嗦），并接线进四个 schema、rule-card、README；字段结构没动。
- AC1–AC10 全部满足，grep 复核 + 通读自证。本迭代自己的四件套即按新口径写（dogfood）。

# AC Status

- [x] AC1 ✓ `artifact-style.md` 已建，frontmatter 有 audience 与 scope。
- [x] AC2 ✓ §2 写了讲人话原则 + 点名反面词（护栏 / 正交 / 高注意力区 / BLUF / fresh-context）+ 真要指机制就点名加解释。
- [x] AC3 ✓ §3 写了反啰嗦六条（bullet / 嵌套≤2 / 不复述 / 宁缺毋滥 / 信号只列名 / VERIFY 紧凑式）。
- [x] AC4 ✓ §4 给了两组 before/after（分流行、AC 回填），可照抄。
- [x] AC5 ✓ §5 写明边界——和四 schema、对话层两规则各管各的。
- [x] AC6 ✓ 四个 schema 编写规则各加一行指针（`grep -l artifact-style` 四个全中）。
- [x] AC7 ✓ rule-card 新增「## 产物书写」节，口径与新文件一致。
- [x] AC8 ✓ README 三处注册（目录树 / 目录职责 / 逐文件说明）全中。
- [x] AC9 ✓ 本迭代四件套无黑话 filler、无整段重述；反面词只在"谈论它们"处出现（CONCEPT 举病、AC2 举例）。
- [x] AC10 ✓ 本仓 CLAUDE.md 五约束自检通过（见 Gate Coverage）。

# Verification Results

- AC1–5：读 `artifact-style.md`，六节齐全（目标 / 讲人话 / 反啰嗦 / before-after / 边界 / 自检），反面词与 before/after 块 grep 在位。
- AC6：`grep -l artifact-style` 命中 concept / acceptance / tech-plan / verify 四个 schema。
- AC7：`grep '## 产物书写'` 命中 rule-card；措辞与新文件正文一致、不矛盾。
- AC8：`grep artifact-style Coder/README.md` 命中第 51 行（目录树）、95 行（目录职责）、130 行（逐文件说明）。
- AC9：`grep` 反面词只命中 CONCEPT:12（举病）与 AC_LIST:27（AC2 举例），无 filler 用法。

# Gate Coverage

- 通用质量门禁：新文件自洽（自己也讲人话、不啰嗦）、措辞用"必须 / 不得 / 应"、frontmatter 标 audience / scope。
- Active Profiles：未命中（Markdown 规则仓库），省略。
- Tech Plan Alignment：四项设计决策全兑现——独立文件落 20 层、原则+点名不写硬禁用清单、给 before/after、rule-card 同步。
- References Compliance：N/A（本轮无 `.ai/references/`）。
- CLAUDE.md 五约束：①分层不混（口径归 20 层 SOP）；②产物链字段未动（只改"怎么写"）；③新文件已在 README 双注册；④rule-card 与新文件单一来源、不双写矛盾；⑤各文件 frontmatter 合规。

# Remaining Risks

- 口径靠会话起始读取 + 遵守，没有 hook 强制——和 identity / presentation-protocol 一样，可接受。
- "讲人话 vs 必要机制名"边界靠语义判断——用 before/after 例兜底。
- 本轮不切版，ITER-0012 累积到下次发布，预计 MINOR（新增可选书写口径、向后兼容）。

# Handoff / Next Step

- 任务已闭合，进入收口三步（归档 + 写 `deliveries/ITER-0012-artifact-plain-language.{md,html}` + 台账置 closed）。
