# 冷启动可恢复性与收口知识固结（MILE-0001）

> MILE-0001 · 里程碑交付（大版本）· 收口 2026-07-02 · 随 v1.6.0 发布 · 含迭代 ITER-0017 / ITER-0018 / ITER-0019

## 本次交付目标

- 补两个在 butler 积累 16 个迭代后暴露的系统性缺口：① 冷启动信息源只有"瞬时断点"（handoff）和"变更流 delta"（ITERATIONS / deliveries），缺一份**状态积分取向的全貌**；② 收口纪律"有规则、无门槛"，台账 / 产物 / 交付三者漂移已实际发生。
- 大版本目标：长寿项目冷启动时先读到"系统现在是什么 + 长期约束与欠债"的全貌；收口不再容易半途而废，台账 / 产物 / 交付不再漂移。

## 已完成内容

- 全貌产物、每迭代变更流、收口门槛三件闭环，覆盖"冷启动读得到全貌 + 收口守得住一致"两端。逐路线项见下方回填。

## 关键变更 / 用户可感知变化

- 冷启动读序固定为 `PROJECT.md`（全貌）→ `ITERATIONS.md`（变更流）→ `02_SESSION_HANDOFF.md`（断点）→ 代码，不再从一堆迭代一句话倒推整只豹。
- 收口升级为原子仪式（五步，末步强制一致性自检）；部署项目"上一迭代没收口就开新"被 hook 当场拦下。
- 每迭代产出对象级 ADD/EDIT/DELETE 变更流，绑 AC、文件+章节级、收口归档。

## 高层影响范围

- 新增规则 / 产物：`40_Context_Management/project-digest-schema.md`、`20_Workflow_Lifecycle/changelog-schema.md`、`.ai/PROJECT.md`、hook 规则 `single_active_iteration`。
- 接线：`iteration-schema §5.5`（原子收口仪式）、`context-persistence`（冷启动读序 + 一致性自检 5 不变量）、`lifecycle §165`、`mcv-deployment §5`、`Coder/README`。
- 未动：P1-P5 阶段状态机、四件套字段结构、AC 验收脊柱、既有 hook 判据（phase_gate / ledger_status）。

## 拆分路线图回填

| 路线项 | 主题 | 实际 ITER | 状态 | 落点 |
|---|---|---|---|---|
| R1 | 新增 `.ai/PROJECT.md` 冷启动全貌产物（状态取向 + schema + 读序接线 + 收口前滚 + 部署种子） | ITER-0017 | ✅ closed | `deliveries/ITER-0017-project-digest.md` |
| R3 | 每迭代 changelog 正式化（严格 ADD/EDIT/DELETE + schema + 收编半成品） | ITER-0018 | ✅ closed | `deliveries/ITER-0018-changelog-formalization.md` |
| R2 | 收口门槛（执行门禁 hook + 冷启动一致性自检 + 原子收口仪式） | ITER-0019 | ✅ closed | `deliveries/ITER-0019-close-gate.md` |

- 三路线项全部达成。执行顺序为 R1 → R3 → R2（先补收口产出、再由 R2 给完整收口加门槛；R3 纯 markdown 风险低于动 hook 的 R2，故先行）。

## 验证方式与结果摘要

- 三路线项其下迭代各自 P1-P5 闭环、各自收口交付（见上表链接）；里程碑收口前确认路线图各项均 closed。
- dogfood：对 butler 自身 `.ai/` 跑冷启动一致性自检 5 不变量全绿。
- 本里程碑随 v1.6.0 聚合发布（与独立迭代 ITER-0020 同版），迁移配方 `migrations/v1.6.0.md`（`[sync-hooks]` 交付新 hook 规则）。

## 已知剩余风险 / 延后事项

- butler 仓自身不 dogfood 运行自己的 hook → live 机械门槛在 butler 内不触发，靠 pytest + prompt 级一致性自检覆盖（已知设计约束，非本里程碑遗留缺陷）。
- `/close` 原子收口命令未做（收口仪式已清单化 + 自检，命令化留后续 polish）。

## 引用

- 里程碑产物快照：`.ai/milestones/MILE-0001/MILESTONE.md`
- 其下迭代交付：`deliveries/ITER-0017-project-digest.md`、`deliveries/ITER-0018-changelog-formalization.md`、`deliveries/ITER-0019-close-gate.md`
- 发布：`CHANGELOG.md` [1.6.0]、`migrations/v1.6.0.md`、`.ai/ITERATIONS.md`、`.ai/MILESTONES.md`
