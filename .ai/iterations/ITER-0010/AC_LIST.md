---
状态: ack-frozen
ACK 日期: 2026-06-20
---

# Goal
- 让迭代 / 里程碑收口在产出 Markdown 交付总结的同时，**额外产出一份固定格式、单文件自包含的 HTML 阅读视图**；固定格式以 `templates/` 下唯一模板为 SSOT，收口时填槽生成。MD 仍为引用真源，HTML 只是其渲染投影，遵守「只引用不嵌入、体量恒定」硬约束。

# In Scope
1. 新增固定 HTML 模板 SSOT（`templates/delivery.html.template`）：单文件自包含、内联 CSS、`{{占位符}}` 槽位对应 `delivery-summary.md §4` 结构，含 MILE 可选「拆分路线图回填」段。
2. `delivery-summary.md`：新增「固定格式 HTML 阅读视图」规则小节 + §3 命名/存放补 `.html` 同名兄弟文件 + §8 对话引用口径澄清。
3. `iteration-schema.md`、`milestone-schema.md`、`lifecycle.md`：把收口「写交付总结」那一步的产出契约由单 `.md` 扩为 `.md`（真源）+ 同名 `.html`（阅读视图）。
4. 传播面：`templates/rule-card.md`、`HUMAN_GUIDE.md`、`Coder/README.md`、仓库根 `CLAUDE.md` 中涉及收口产出 / deliveries 结构 / templates 内容物的描述同步。

# Out of Scope
- 不回填历史 13 份 `deliveries/` 为 HTML（仅 ITER-0010 起生效）。
- 不引入 md→html 转换脚本或任何 node/python/pandoc 运行时依赖（用户裁定为模板手填）。
- 不用 HTML 替代 MD、不引入第二真源、不把四件套全文嵌进 HTML。
- 不为 HTML 产出加 hook 校验（与 delivery summary 同等，靠规则纪律）。
- 不改产物链四 schema 字段、不改 hook 脚本/契约、不切版本（累积到下次切版）。

# Acceptance Checklist

## A. 模板 SSOT（固定格式）
- [ ] AC1: 新增 `templates/delivery.html.template`，是**单文件自包含** HTML（`<style>` 内联、零外部 CSS/JS/字体依赖），双击可直接在浏览器打开。
- [ ] AC2: 模板含覆盖 `delivery-summary.md §4.1–§4.7` 的 `{{占位符}}` 槽位（交付目标 / 已完成内容 / 关键变更 / 高层影响范围 / 验证方式与结果 / 剩余风险 / 引用），并含头部元信息槽（交付标题、迭代或里程碑号、收口日期、层级类型）。
- [ ] AC3: 模板含 MILE 专用的**可选「拆分路线图回填」段**（对应 §4.8），ITER 级填槽时该段可整体省略，结构上不强迫 ITER 产生空段。
- [ ] AC4: 模板的「引用」槽位在注释或结构上明确只放**路径指针**（如 `.ai/iterations/ITER-NNNN/AC_LIST.md`），不放四件套全文——HTML 与 MD 同守 §4.7 体量恒定硬约束。

## B. delivery-summary.md 主规则
- [ ] AC5: `delivery-summary.md` 新增一节（如 §4.9 或独立「固定格式 HTML 阅读视图」节）定义：HTML 模板 SSOT 路径（`templates/delivery.html.template`）、收口时按 §4 结构填槽生成、单文件自包含、MD 仍为引用真源、HTML 同守只引用不嵌入。
- [ ] AC6: §3「存放位置与命名」补：迭代级产 `deliveries/ITER-NNNN-<slug>.html`、里程碑级产 `deliveries/milestones/MILE-NNNN-<slug>.html`，与同名 `.md` 同目录同 slug 并列。
- [ ] AC7: §8 对话层澄清：§8.4 收尾「正式版：」引用行仍指向 `.md`（引用真源），HTML 为其同名兄弟阅读视图（不改 §8.4 既有格式契约）。

## C. 收口契约贯通（三步不变、step 2 双产出）
- [ ] AC8: `lifecycle.md` P5 收口 step ②（生成 `deliveries/ITER-NNNN-<slug>.md`）措辞扩为「同时产出同名 `.html` 固定格式阅读视图」，仍是三步、不新增第四步。
- [ ] AC9: `iteration-schema.md` §3 三层落盘「人类交付」行 + §5.5 收口三步 step 2 同步为 `.md` + 同名 `.html` 双产出。
- [ ] AC10: `milestone-schema.md` §7.4 收口三步 step 2 同步双产出；§9 交付文档结构树补 `.html` 兄弟文件示意。

## D. 传播一致性
- [ ] AC11: `templates/rule-card.md` 的 ITER 收口三步（L25 一带）与 MILE 收口三步（L27 一带）描述补「写交付总结 = `.md` + 同名 `.html`」。
- [ ] AC12: `HUMAN_GUIDE.md` 的 deliveries 结构说明（含目录树）与交付总结描述补「每份交付另有同名固定格式 `.html` 阅读视图」。
- [ ] AC13: `Coder/README.md`（delivery-summary 职责一行）与仓库根 `CLAUDE.md`（templates/ 内容物描述）同步提及 HTML 阅读视图 / `delivery.html.template`。

## E. 一致性与零改动护栏
- [ ] AC14: 全仓表述一致——HTML 处处被定位为「MD 的固定格式阅读投影、与 MD 并列、MD 为引用真源」，无任一处把 HTML 写成替代 MD 或第二真源；「单文件自包含 + 模板 SSOT」口径各处一致。
- [ ] AC15: 零改动护栏——产物链四 schema（concept/acceptance/tech-plan/verify）字段、hook 脚本与契约（phase_gate/ledger_status）、`VERSION`/`CHANGELOG.md`、历史 13 份 deliveries、各扩展模块未被改动（`git diff` 确认）。
- [ ] AC16: 未破坏 `CLAUDE.md` 五条编辑约束——分层未混（模板归 templates/、语义归规则）、产物链未动、新增模板文件已在仓库根 `CLAUDE.md`/`Coder/README` 适当登记、固定格式经模板 SSOT 单一来源（规则不重述其 HTML 结构）、各文件 frontmatter 未破坏。

## F. 收口
- [ ] AC17: ITER-0010 四件套快照归档 `.ai/iterations/ITER-0010/`，写 `deliveries/ITER-0010-<slug>.md` **及同名 `.html`**（首份按本迭代新规生效——dogfood 自校验），台账置 closed + 收口日期 + 交付链接，`current: none`。

# Verification Method
- AC1/AC2/AC3/AC4: 读 `templates/delivery.html.template`，确认无 `http(s)://`/外链 `<link>`/外链 `<script>`/外链字体；占位符清单覆盖 §4.1–§4.7 + 头部元信息 + 可选路线图段；引用槽注释限定路径指针。可在浏览器打开样例确认排版。
- AC5/AC6/AC7: grep `delivery-summary.md` 命中新节、`.html` 命名、§8.4 引用行仍指 `.md`。
- AC8/AC9/AC10: grep `lifecycle.md`/`iteration-schema.md`/`milestone-schema.md` 对应小节，确认 step 2 双产出措辞 + 仍为三步。
- AC11/AC12/AC13: grep `rule-card.md`/`HUMAN_GUIDE.md`/`Coder/README.md`/根 `CLAUDE.md` 命中 HTML 阅读视图描述。
- AC14: 全仓 grep HTML/阅读视图相关表述，人工核对定位一致、无「替代 MD/第二真源」措辞。
- AC15: `git diff --stat` 确认护栏文件不在改动名单；四 schema、hooks/、VERSION、CHANGELOG、deliveries/ 历史文件零 diff。
- AC16: 对照 `CLAUDE.md` 五约束逐条自检；确认 `delivery.html.template` 已登记。
- AC17: 收口时执行三步并核对台账、归档目录、双产出文件齐全。

# External References
- 无（本轮不涉及外部 API 文档 / 设计稿；HTML 模板的固定排版为自带资产）。

# Open Questions / Risks
- 模板单模板 + 可选路线图段 vs ITER/MILE 两薄变体：倾向单模板 + 可选段，P3 TECH_PLAN 定稿。
- HTML 模板填槽时从 `$BUTLER/templates/delivery.html.template` 读取（与部署/升级读 $BUTLER 同源假设）；是否需部署时复制进目标项目留待 P3（默认不复制，避免副本漂移），不影响本仓库自身收口。
- 本轮 dogfood：ITER-0010 自身收口将产出**首份** `.html`，等于用新规即时自校验；若模板有排版问题，收口前即可发现。
- HTML 靠规则纪律产出，无 hook 强制——与 delivery summary 同源同险。
