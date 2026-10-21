# ITER-0010 交付总结增加固定格式 HTML 阅读视图

## 本次交付目标
让 butler 的迭代 / 里程碑交付总结，在现有 Markdown 之外**并列产出一份固定格式、单文件自包含的 HTML 阅读视图**，方便人类直接双击打开阅读。固定格式有唯一 SSOT（模板文件），不在每次收口手搓飘移；不破坏「交付总结只引用产物路径、不嵌入全文、体量恒定」的硬约束。

## 已完成内容
- **新增固定 HTML 模板 SSOT** `templates/delivery.html.template`：单文件自包含（内联 CSS、零外部 CSS/JS/字体依赖、双击可离线打开），12 个 `{{占位符}}` 槽位对应 `delivery-summary.md §4`（4 个头部元信息 + §4.1–§4.7 七段正文 + 里程碑专用 `{{ROADMAP}}`），含 `<!-- ROADMAP:START/END -->` 注释块供迭代级整段删除。
- **主规则贯通** `delivery-summary.md`：新增 §9「固定格式 HTML 阅读视图」（定位 / 模板 SSOT 与填槽协议 / 硬约束 / 边界）；§3 命名补 `.html` 同名兄弟文件；§7 收口三步措辞改为 step ② 双产出；§8.4 澄清对话引用行恒指 `.md`。
- **收口契约贯通**：`lifecycle.md` P5 收口、`iteration-schema.md`（§3 三层落盘行 + §5.5 step 2）、`milestone-schema.md`（§7.4 step 2 + §9 结构树）三处把「写交付总结」一步从产 `.md` 扩为产 `.md` + 同名 `.html`，仍是三步、不新增第四步。
- **传播一致**：`templates/rule-card.md`（ITER/MILE 两处收口三步）、`HUMAN_GUIDE.md`（交付描述 / 目录树 / 里程碑收口 / 规范注 四处）、`Coder/README.md`（delivery-summary 职责行）、仓库根 `CLAUDE.md`（templates/ 内容物描述）同步。
- **dogfood**：本份 ITER-0010 交付即用新模板产出首份 `.html`（同名兄弟文件），即时自校验排版与填槽协议。

## 关键变更 / 用户可感知变化
- 从 ITER-0010 起，每次迭代 / 里程碑收口都会在 `deliveries/` 下多出一份**同名 `.html`**：迭代级 `deliveries/ITER-NNNN-<slug>.html`、里程碑级 `deliveries/milestones/MILE-NNNN-<slug>.html`。
- `.html` 双击即可在浏览器读到统一排版的交付总结；`.md` 仍是**引用真源**，`.html` 只是它的固定格式阅读投影。
- 收口节奏不变：仍是「快照归档 + 写交付总结 + 更新台账」三步，只是「写交付总结」那步变成双产出。
- 历史 13 份交付**不回填**；未升级到本版的部署项目只产 `.md`，向后兼容、不报错。

## 高层影响范围
- 新增：`templates/delivery.html.template`。
- 改（规则语义 + 传播）：`Coder/20_Workflow_Lifecycle/{delivery-summary,iteration-schema,milestone-schema,lifecycle}.md`、`templates/rule-card.md`、`HUMAN_GUIDE.md`、`Coder/README.md`、仓库根 `CLAUDE.md`。
- 零改动护栏：产物链四 schema（concept/acceptance/tech-plan/verify）、hook 体系（phase_gate/ledger_status）、`VERSION`/`CHANGELOG.md`、`mcv-deployment.md`、历史 13 份 `deliveries/`、各扩展模块。

## 验证方式与结果摘要
- AC1–AC4（模板）：`grep` 确认零外链、12 占位符齐全、ROADMAP 注释块存在、REFERENCES 槽限定路径指针。
- AC5–AC13（规则 + 传播）：逐文件 `grep` 命中 §9、两级 `.html` 命名、三处 step ② 双产出、rule-card 2 处 / HUMAN_GUIDE 4 处 / README / 根 CLAUDE.md。
- AC14（一致性）：全仓无「HTML 替代 MD / 第二真源」措辞。
- AC15（护栏）：`git status --short` 确认护栏文件零改动。
- AC17（dogfood）：本份交付的 `.html` 用新模板填槽生成、浏览器可打开。
- 详见 `.ai/iterations/ITER-0010/VERIFY_REPORT.md`。

## 已知剩余风险 / 延后事项
- HTML 产出靠规则纪律（收口三步），无 hook 强制——与 delivery summary 同源同险。
- 部署项目收口填槽依赖 `$BUTLER` 可达；不可达时只能先产 `.md`、后补 `.html`（本仓库自身收口不受限）。
- 版本：本轮不发版，ITER-0010 累积到下次切版，预计 MINOR（向后兼容新增可选交付产物）。

## 引用
- `.ai/iterations/ITER-0010/CONCEPT.md`
- `.ai/iterations/ITER-0010/AC_LIST.md`
- `.ai/iterations/ITER-0010/TECH_PLAN.md`
- `.ai/iterations/ITER-0010/VERIFY_REPORT.md`
- `templates/delivery.html.template`（固定格式 SSOT）
- `Coder/20_Workflow_Lifecycle/delivery-summary.md` §9
