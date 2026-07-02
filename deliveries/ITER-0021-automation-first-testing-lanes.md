# 自动化优先纪律 + 分道口径：testing-strategy 升级 + verify-schema 双道回填

> ITER-0021 · 迭代交付（小版本）· 收口 2026-07-02 · MILE-0002 R1 · ⚠️ 危险模式（P2/P3 用户 ACK，P4 起自治 + P5 独立复核）

## 本次交付目标

- MILE-0002 首个路线项 R1（扁平原子）。
- 现状两处缺口：① `testing-strategy.md` 是"分层**建议**"（§2 建议措辞、§3 写"关键路径**手动**验证完成"），没有"能自动就必须自动"的硬纪律，UI/交互容易随手推给人；② `verify-schema.md` 的 `AC Status` 只记通过/未通过、**不分道**，人测残余无结构化落点。
- 目标：测试纪律升级为**自动化优先**（竭尽自动化，含浏览器自动化覆盖 UI/交互）+ 验证报告引入**自动道/人测道双道回填**，人测道界定为机器不可测残余。

## 已完成内容

- `testing-strategy.md` §2「测试分层建议」→「自动化优先（硬纪律）」：措辞由建议升级为"凡机器能测的必须自动化"，UI/交互显式纳入自动道（浏览器自动化/headless/可编程视觉断言）；§4（原§3）"关键路径手动验证"→"默认自动验证、人测例外残余"。
- `testing-strategy.md` 新增 §3「分道口径」：自动道/人测道判定 + **默认归自动道**纪律（拿不准先自动化、说不出人测类目即回自动道、"暂时没写自动化"是自动道欠债不是人测残余）+ 人测道**类目锚点清单**（主观审美/物理设备/真人感知·决策/外部人工闸）；原 §3-6 顺移 §4-7。
- `verify-schema.md`：§3 模板 `AC Status` 每条 AC 加 `(auto)`/`(human)` lane 标记 + 新增「人测道小结」条件字段；§4 编写规则补分道回填要求（自动道给可复现证据 / 人测道说明为何不可测）；既有 6 必填字段不变（只加不改）。
- 接线：`rule-card.md` 执行纪律段加"自动化优先"一句；`Coder/README.md`（30_Quality_Gate 群组 + verify schema 描述）、`HUMAN_GUIDE.md`（两注释）同步；`.ai/PROJECT.md` 现行约束前滚补自动化优先纪律一句。

## 关键变更 / 用户可感知变化

- 测试从"可以手动验"变成"**能自动必自动**"的硬纪律；UI/交互默认走浏览器自动化，不再随手推人。
- 验证报告首次带**分道**：每条 AC 标 `(auto)`/`(human)`，人测残余集中进「人测道小结」——这为后续 R2（分级置信/代理验证）与 R3（交付自测桥）预留了结构锚点。
- 人测道有了**封闭类目**（主观审美/物理设备/真人感知/外部人工闸）+ 默认归自动道纪律，防止"能自动却推人"。
- 向后兼容：纯规则正文 + 指针同步，未动状态机/四件套字段脊柱/hook 代码/correction-contract。

## 高层影响范围

- 改（核心）：`Coder/30_Quality_Gate/testing-strategy.md`、`Coder/20_Workflow_Lifecycle/verify-schema.md`。
- 改（接线）：`templates/rule-card.md`、`Coder/README.md`、`HUMAN_GUIDE.md`。
- 前滚：`.ai/PROJECT.md` 现行约束。
- 没碰：P1-P5 状态机、四件套字段脊柱、hook 体系、correction-contract、其余 30_Quality_Gate 文件；R2/R3 内容（分级置信/代理验证/依赖感知准入/交付自测桥）未提前塞入。

## 验证方式与结果摘要

- 8 条 AC 全部满足（逐项见 VERIFY_REPORT），**全属自动道**（读文件/grep 可复现），无人测道残余 →「人测道小结」按规则省略（正好 dogfood 新条件字段路径）。
- **危险模式 P5 §7.3 独立复核**：fresh-context general-purpose 子 agent、spec-only 逐 AC + 多维审查（一致性/可读性/边界/dogfood）、验证者≠实现者。结论：8/8 confirm、0 Must Fix、0 Should Fix、2 Nit（PROJECT 前滚=收口债本次已办；verify 模板自洽=确认）。
- 顺移安全：testing-strategy §1-§7 编号连续；外部 §引用 2 处（rule-card/verify-schema）+ 内部 3 处均指向新 §3；verify-schema 未 renumber（§4 完好，护 `changelog-schema §4` 引用）。
- 不变量：`git diff --name-only` 确认 hook/correction-contract/lifecycle/四件套 schema 未在变更内；R2/R3 关键词全仓 grep 零命中。

## 已知剩余风险 / 延后事项

- R1/R2 边界：本迭代只写"确定性自动化必自动"，弱视觉/代理验证/分级置信显式留 R2；"弱信号项归哪道"要待 R2 分级置信落地才完全清晰。
- 分道口径非 hook 机械门，靠纪律 + 收口自检兜底（与 butler 既有"提交规约/自动化优先均非机械门禁"同源，非新增风险）。

## 引用

- 归档四件套 + 切片：`.ai/iterations/ITER-0021/CONCEPT.md` / `AC_LIST.md` / `TECH_PLAN.md` / `VERIFY_REPORT.md` / `CHANGELOG.md`
- 核心改动：`Coder/30_Quality_Gate/testing-strategy.md`（§2 自动化优先 / §3 分道口径）、`Coder/20_Workflow_Lifecycle/verify-schema.md`（§3 模板 lane + 人测道小结 / §4 分道回填）
- 接线改动：`templates/rule-card.md`、`Coder/README.md`、`HUMAN_GUIDE.md`
- 前滚：`.ai/PROJECT.md`
- 危险模式审计：`.ai/RUN_LOG.md`（ITER-0021 段）
