# TECH_PLAN — ITER-0021

# Goal

- 支撑 AC1-AC8：`testing-strategy.md` 升级为自动化优先 + 分道口径；`verify-schema.md` 增双道回填；同步 README / rule-card / PROJECT。

# Files / Modules to Change

- `Coder/30_Quality_Gate/testing-strategy.md`（核心）：§2 建议→纪律；新增「分道口径」节（作新 §3，原 §3-6 顺移 §4-7）；frontmatter scope 补分道。
- `Coder/20_Workflow_Lifecycle/verify-schema.md`（核心）：§3 模板 `AC Status` 加 lane 标记 + 新增「人测道小结」字段；§4 编写规则补分道回填要求。**只在 §3/§4 内追加、不 renumber**（护 `changelog-schema.md §4` 引用不断）。
- `templates/rule-card.md`：「执行纪律」段加一句"能自动化的验证必须自动化，人测只留机器不可测残余"。
- `Coder/README.md`：§99 群组描述补自动化优先；§134 verify 描述补分道回填。
- `HUMAN_GUIDE.md`：testing-strategy / verify-schema 两处注释同步（指针一致，AC6 spirit）。
- `.ai/PROJECT.md`：收口前滚，现行纪律补自动化优先一句。

# Interface / Contract

- 分道口径契约（新增）：每条 AC ∈ {auto 道, human 道}；human 道 = 机器不可测残余；判定**默认归 auto 道**，仅确证不可测才 human；human 道类目锚点 = {主观审美, 物理设备, 真人感知, 外部人工闸}。
- VERIFY_REPORT 回填契约（扩写）：`AC Status` 行内标 `(auto)` / `(human)`；新增「人测道小结」段列 human 项 + 待测 / 结论。既有 6 必填字段结构不变。

# State / Boundary

- 只动规则正文 + 指针；不动 hook 代码、四件套字段脊柱、P1-P5 状态机、correction-contract。
- verify-schema 不 renumber（护 §4 引用）；testing-strategy 顺移安全（无 §N 外部引用，已 grep 验证）。
- 弱视觉 / 代理验证 / 分级置信 / 依赖感知准入 = R2，不写入；「交付自测」桥 = R3，不实现。

# Design Decisions

- DD1（Q1）：分道口径作 testing-strategy **新 §3**（§2 立纪律 → §3 给判定，动线顺），原 §3-6 顺移 §4-7。testing-strategy 无 §N 外部引用（grep 确认），顺移安全。
- DD2（Q2）：verify 分道回填 = 行内 lane 标记 `[x] AC1 (auto) ✓` + 独立「人测道小结」段。理由：行内最省、合现有紧凑式；小结段集中列残余，给 R3 桥 JSON 输入预留结构锚点。
- DD3（Q3）：rule-card 收录一句到「执行纪律」段（非新卡、非机械门）。与 ITER-0020 提交规约不入 rule-card 不冲突——那是格式约定，这是执行纪律，执行纪律段正是其家。
- DD4（Q4）：给 human 道**类目锚点清单**（主观审美 / 物理设备 / 真人感知 / 外部人工闸），作"允许落人测"的封闭性锚，防随手推人。
- DD5：verify-schema 只在 §3/§4 内追加、不 renumber，保护 `changelog-schema.md §4` 引用。
- DD6：README 更新落 §99（quality gate 自动化优先）+ §134（verify 分道）；HUMAN_GUIDE 两注释同步（指针一致）。

# Execution Steps

- [ ] T1 testing-strategy §2：建议措辞 → 自动化优先硬纪律（能自动必自动 + UI/交互纳入自动道：浏览器自动化 / headless / 可编程视觉断言）→ AC1
- [ ] T2 testing-strategy §3"关键路径手动验证" → "默认自动、人测例外残余"→ AC1
- [ ] T3 testing-strategy 新增「分道口径」节（新 §3）：auto/human 判定 + 默认归 auto + human 类目锚点清单；原 §3-6 顺移 §4-7；frontmatter scope 补分道 → AC2
- [ ] T4 verify-schema §3 模板 `AC Status` 加 `(auto)`/`(human)` 标记 + 新增「人测道小结」字段 → AC3
- [ ] T5 verify-schema §4 编写规则补分道回填要求（auto 给可复现证据 / human 说明为何不可测）；确认 6 必填字段不增删 → AC4, AC5
- [ ] T6 rule-card 执行纪律段加自动化优先一句 → AC7
- [ ] T7 README §99 + §134 描述同步 + HUMAN_GUIDE 两注释同步 → AC6
- [ ] T8 PROJECT.md 收口前滚补自动化优先纪律一句 → AC7
- [ ] T9 P5：git diff 核对不变量未动 + 无 R2/R3 混入 + 逐 AC 回填 VERIFY（首次带分道）→ AC8

# Verification Plan

- AC1/2：读改后 testing-strategy §2/§3。
- AC3/4/5：读改后 verify-schema §3/§4；比对 6 必填字段未增删。
- AC6：grep README / HUMAN_GUIDE。
- AC7：rule-card diff + PROJECT diff。
- AC8：`git diff --stat` + 通读无 R2/R3 混入。

# Risks / Open Questions

- 顺移断引用风险 → 缓解：T3 后 grep `testing-strategy.md §`（已知外部无 §引用）+ 文件内 grep `§`。
- R1/R2 边界混淆 → 缓解：DD 只写确定性自动化，弱信号显式留 R2（AC_LIST 风险项已记）。
- Q1-Q4 已在 DD1-DD4 定案，无遗留。
