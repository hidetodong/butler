# Goal
- 支撑 AC1–AC17：新增固定 HTML 模板 SSOT，并把迭代/里程碑收口「写交付总结」一步从产 `.md` 扩为产 `.md`（引用真源）+ 同名 `.html`（固定格式阅读视图），贯通所有引用该契约的规则/模板/指南；MD 仍为引用真源，HTML 同守「只引用不嵌入」。下文给精确锚点。

# Files / Modules to Change

| # | 文件 | 改动 | 覆盖 AC |
|---|---|---|---|
| 1 | **新增** `templates/delivery.html.template` | 固定 HTML 模板 SSOT（单文件自包含、内联 CSS、`{{占位符}}` + MILE 可选路线图段） | AC1–4 |
| 2 | `Coder/20_Workflow_Lifecycle/delivery-summary.md` | §3 命名补 `.html`；新增 §9「固定格式 HTML 阅读视图」；§7 补一行；§8 引用口径澄清（§8.4 仍指 `.md`） | AC5–7 |
| 3 | `Coder/20_Workflow_Lifecycle/iteration-schema.md` | §3 三层落盘「人类交付」行 + §5.5 收口三步 step 2 双产出 | AC9 |
| 4 | `Coder/20_Workflow_Lifecycle/milestone-schema.md` | §7.4 收口三步 step 2 双产出 + §9 交付文档结构树补 `.html` | AC10 |
| 5 | `Coder/20_Workflow_Lifecycle/lifecycle.md` | P5 收口 step ②（L163/L165 一带）措辞双产出 | AC8 |
| 6 | `templates/rule-card.md` | §迭代化需求 ITER 收口三步（L25）+ MILE 收口三步（L27）补「写交付总结 = `.md` + 同名 `.html`」 | AC11 |
| 7 | `HUMAN_GUIDE.md` | L60 交付描述、L118–120 deliveries 目录树、L165 里程碑收口、L276 delivery-summary 职责注 补 HTML 阅读视图 | AC12 |
| 8 | `Coder/README.md` | L131 delivery-summary 职责一行补「含固定格式 HTML 阅读视图」 | AC13 |
| 9 | 仓库根 `CLAUDE.md` | templates/ 内容物描述补 `delivery.html.template` | AC13/AC16 |

零改动护栏（AC15）：`concept/acceptance/tech-plan/verify-schema.md`、`templates/hooks/`、`settings.hooks-snippet.json`、`VERSION`、`CHANGELOG.md`、`deliveries/` 历史 13 份、各扩展模块、mcv-deployment.md（不复制模板进目标项目，见 Design Decisions）一律不动。

# Interface / Contract

## 收口产出契约（扩展，向后兼容）
- 旧：迭代收口 step ② = 写 `deliveries/ITER-NNNN-<slug>.md`。
- 新：迭代收口 step ② = 写 `deliveries/ITER-NNNN-<slug>.md`（引用真源）**＋同名** `deliveries/ITER-NNNN-<slug>.html`（固定格式阅读视图）。里程碑同构于 `deliveries/milestones/MILE-NNNN-<slug>.{md,html}`。
- 收口仍是**三步**（快照归档 / 写交付总结 / 更新台账），step ② 由单产出变双产出，不新增第四步。
- 向后兼容：历史无 `.html` 的旧交付照常有效（不回填）；未升级到本版的部署项目只产 `.md`，不报错。

## 模板占位符契约（`templates/delivery.html.template` 的槽位）
| 槽位 | 对应 delivery-summary | 内容 |
|---|---|---|
| `{{DELIVERY_TITLE}}` | 文件首行标题 | 如「ITER-0010 交付总结增加固定格式 HTML 阅读视图」 |
| `{{DELIVERY_ID}}` | — | `ITER-NNNN` 或 `MILE-NNNN` |
| `{{DELIVERY_LEVEL}}` | — | 「迭代交付（小版本）」或「里程碑交付（大版本）」 |
| `{{DELIVERY_DATE}}` | 收口日期 | `YYYY-MM-DD` |
| `{{DELIVERY_GOAL}}` | §4.1 本次交付目标 | HTML 渲染 |
| `{{COMPLETED}}` | §4.2 已完成内容 | HTML 渲染 |
| `{{KEY_CHANGES}}` | §4.3 关键变更/用户可感知变化 | HTML 渲染 |
| `{{IMPACT_SCOPE}}` | §4.4 高层影响范围 | HTML 渲染 |
| `{{VERIFICATION}}` | §4.5 验证方式与结果摘要 | HTML 渲染 |
| `{{RISKS}}` | §4.6 已知剩余风险/延后事项 | HTML 渲染 |
| `{{REFERENCES}}` | §4.7 引用 | **仅路径指针**（`<a>`/`<code>`），不嵌全文 |
| `{{ROADMAP}}` | §4.8 拆分路线图回填 | **里程碑专用**，含在 `<!-- ROADMAP:START/END -->` 注释块内；迭代级填槽时整段删除 |

# State / Boundary
- **HTML = MD 的渲染投影，不是第二真源**：收口时 AI 已写好 `.md`（§4 结构），随即读模板把同一内容填进对应槽位生成 `.html`。两者同源（同一收口内容）、MD 为引用真源。
- **体量恒定边界**：`{{REFERENCES}}` 只放路径指针（同 §4.7 硬约束）；HTML 不嵌四件套全文，故 HTML 体量随 §4 摘要恒定，不随迭代膨胀。
- **模板读取边界**：填槽时从 `templates/delivery.html.template`（butler 仓库 SSOT，部署/升级语境即 `$BUTLER/templates/`）读取。**不在基地车部署时复制进目标项目**——避免每个项目存一份会漂移的副本，与 rule-card SSOT「占位符继承、不双写」同纪律。故 `mcv-deployment.md` 不改。
- **不在范围内的扩展点**：md→html 转换脚本、HTML 主题切换、目录索引页（如 `deliveries/index.html`）、历史回填——均 Out of Scope。

# Design Decisions
1. **模板手填而非脚本**（用户裁定）：纯 markdown 规则仓库不引入 node/python/pandoc 运行时；固定格式靠单一模板文件保证一致，AI 收口时填槽。复用现有 `{{RULE_CARD_CONTENT}}` 占位符范式。
2. **单模板 + MILE 可选路线图段**，而非 ITER/MILE 两个变体：减少 SSOT 数量、避免两份模板漂移；路线图段用 `<!-- ROADMAP:START/END -->` 注释界定，ITER 填槽时整段删除，不产生空段。
3. **新增 §9 而非插入 §4.9/§5**：delivery-summary.md 现有 §4.7/§4.8/§8.4 被其他文件交叉引用，**插入中间会迫使重号、断引用**；故 HTML 阅读视图作为新 top-level §9 追加在末尾，§1–§8 编号与现有交叉引用全部不动。§3、§4 处加前向指针「见 §9」。
4. **§8.4 收尾引用行仍指 `.md`**：对话层「正式版：deliveries/...md」是既有格式契约且 MD 是引用真源，不改其格式；HTML 作为同名兄弟阅读视图，在 §9 与 §8 注里说明，不挤进 §8.4 那一行。
5. **单文件自包含内联 CSS**：双击即开、可离线、可随 `deliveries/` 一起归档/拷贝；CSS 走系统字体栈 + 简洁卡片排版，零外部依赖。
6. **不复制模板进目标项目**：见 State/Boundary，保 SSOT 唯一、避免副本漂移；代价是收口需 `$BUTLER` 可达（与部署/升级同源假设，可接受）。
7. **active profiles 约束**：无（Markdown 规则仓库，未命中任何 Domain/Stack Profile）；HTML 内联 CSS 是排版资产，不引入前端工程栈。

# Execution Steps
1. **建模板**（AC1–4）：写 `templates/delivery.html.template`——`<!DOCTYPE html>` + 内联 `<style>` + 头部 meta 条（ID/层级/日期）+ §4.1–§4.7 各 `<section>` + `<!-- ROADMAP:START/END -->` 可选段 + `{{REFERENCES}}` 注释限定路径指针。浏览器开样例验排版。
2. **改主规则**（AC5–7）：`delivery-summary.md` §3 命名补 `.html` 同名兄弟；末尾加 §9「固定格式 HTML 阅读视图」（模板 SSOT 路径、填槽协议、单文件自包含、MD 为真源、同守只引用不嵌入、MILE 路线图段处理）；§7 加一行「收口同时产 `.md` + 同名 `.html`」；§8.5 末或 §8.4 后补一句澄清引用行仍指 `.md`、HTML 为同名兄弟。
3. **贯通收口契约**（AC8–10）：`lifecycle.md` P5 step ②、`iteration-schema.md` §3「人类交付」行 + §5.5 step 2、`milestone-schema.md` §7.4 step 2 + §9 结构树，全部改为 step ② 双产出措辞，强调「仍三步」。
4. **传播**（AC11–13）：`rule-card.md` L25/L27、`HUMAN_GUIDE.md` L60/L118-120/L165/L276、`Coder/README.md` L131、根 `CLAUDE.md` templates 描述同步。
5. **P5 验证**（AC1–16）：逐 AC grep + 浏览器开模板样例 + `git diff --stat` 核护栏。
6. **收口**（AC17）：四件套快照进 `.ai/iterations/ITER-0010/`；写 `deliveries/ITER-0010-delivery-html-view.md` **及用新模板填槽生成的同名 `.html`**（dogfood 首份自校验）；台账置 closed + 收口日期 + 交付链接，`current: none`。

# Verification Plan
- AC1/2/3/4: 读模板——grep 无 `http`/外链 `<link>`/外链 `<script>`/外链字体；占位符清单齐全（§4.1–§4.7 + 4 个 meta + `{{ROADMAP}}`）；ROADMAP 注释块存在；REFERENCES 槽注释限定路径指针。浏览器打开一份填好的样例确认排版。
- AC5/6/7: grep `delivery-summary.md` 命中 §9、`.html` 命名（ITER 与 MILE 两处）、§8 澄清句、§8.4 仍 `.md`。
- AC8/9/10: grep 三个 schema/lifecycle 对应小节确认「step ② 双产出 + 仍三步」。
- AC11/12/13: grep `rule-card.md`/`HUMAN_GUIDE.md`/`README.md`/根 `CLAUDE.md` 命中 HTML 阅读视图描述。
- AC14: 全仓 grep `阅读视图`/HTML 相关句，人工核对处处定位为「MD 投影、并列、MD 真源」，无「替代/第二真源」。
- AC15: `git diff --stat` 确认四 schema、hooks/、VERSION、CHANGELOG、deliveries/ 历史、mcv-deployment 零 diff。
- AC16: 对照 CLAUDE.md 五约束自检；确认 `delivery.html.template` 已在根 CLAUDE.md/README 登记。
- AC17: 收口三步执行后核台账行、归档目录、`deliveries/ITER-0010-*.{md,html}` 双文件齐全且 HTML 可浏览器打开。

# Risks / Open Questions
- 模板内联 CSS 的「固定排版」一旦定版即成 SSOT，后续改样式须改模板单点——可接受（正是 SSOT 目的）。
- 收口填槽依赖 `$BUTLER` 可达；目标项目若 `$BUTLER` 不可达则只能先产 `.md`、补产 `.html`——本仓库自身收口不受此限（模板即本地文件）。
- HTML 产出靠规则纪律（收口三步），无 hook 强制——与 delivery summary 同源同险，已在 Out of Scope 接受。
- 无外部参考资料（`External References` 空）。
