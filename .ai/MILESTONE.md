# 里程碑：冷启动可恢复性与收口知识固结（MILE-0001）

> butler 仓首个里程碑。方向性产物，可随推进演进（milestone-schema §7.3），不走 ACK 冻结门。

## 范围评估

### In Scope（版本级）

- 新增 `.ai/PROJECT.md` 常驻项目摘要：状态取向（写"系统现在是什么"）、有界、指针化、收口时前滚维护——补冷启动"全貌"缺口。
- 给"收口"加门槛：执行门禁（不收口就开不了下一迭代）+ 冷启动一致性探针 + 原子收口仪式；并把"前滚 PROJECT.md"纳入收口步。
- 每迭代 changelog 正式化：把 `iterations/ITER-NNNN/CHANGELOG.md`（活跃期 `.ai/01_CHANGELOG.md`）定为严格 ADD/EDIT/DELETE 的精确变更流，给它一份真 schema、收编现有半成品。

### Out of Scope（版本级）

- 不改 P1-P5 阶段状态机、四件套字段结构、AC 验收脊柱。
- 不强制 butler 仓自身 dogfood 运行自己的 hook（这是单独决策，必要时另立迭代）。

### 关键交付目标

- 长寿项目冷启动时，AI 先读到一份"系统现在是什么 + 长期约束与欠债"的全貌，不再从一堆迭代一句话 + 代码倒推整只豹。
- 收口不再容易半途而废；台账、产物、交付三者不再漂移。

## 理解阐释

### 核心问题

当前 `.ai/` 的冷启动信息源，要么**瞬时**（`02_SESSION_HANDOFF.md` 断点），要么**变更流 delta**（`ITERATIONS.md` / `deliveries/`），缺一份**状态 integral 取向**的全貌。同时收口纪律"有规则、无门槛"，台账/产物更新不及时。两个问题在"收口"处汇合——收口正是该把本轮长期知识固结进全貌、并翻台账的时刻。

### 背景与价值

butler 已积累 16 个迭代，冷启动管中窥豹；收口漂移已实际发生（本会话发现 v0.2.0 时代的陈旧 handoff，加上用户对"台账更新不及时"的观察）。

### 对系统的整体影响

- `40_Context_Management`：冷启动读序、PROJECT.md 维护触发。
- `20_Workflow_Lifecycle`：iteration-schema / milestone 收口步、mcv-deployment 部署创建、butler-upgrade 迁移配方。
- `Coder/README.md`：注册新 schema + 读序。
- 新增一个 schema 文件；可能联动 `rule-card.md`。
- R2 触及 hook 体系（`templates/hooks/`）与收口一致性探针。

## 拆分路线图

预计跨度：ITER-0017 ~ ITER-0019（3 个迭代承接）

| 路线项 | 主题 / 范围切片 | 实际 ITER | 状态 |
|---|---|---|---|
| R1 | 新增 `.ai/PROJECT.md` 全貌产物：schema + 字段 + 冷启动读序接线 + 纳入收口前滚 + 部署种子 + 迁移补建 | ITER-0017 | closed |
| R2 | 给收口加门槛：执行门禁（开下一迭代前校验上一迭代已收口）+ 冷启动一致性探针 + 原子收口仪式 | ITER-0019 | active |
| R3 | 每迭代 changelog 正式化：`iterations/ITER-NNNN/CHANGELOG.md`（活跃期 `.ai/01_CHANGELOG.md`）定为严格 ADD/EDIT/DELETE + 真 schema + 收编半成品 | ITER-0018 | closed |

## 范围演进记录

- 2026-06-30：开启 MILE-0001，确立 R1（全貌产物）/ R2（收口门槛）两路线项；方向经用户选项确认（开里程碑 + 拆 2 迭代 + 新增 `.ai/PROJECT.md`）。
- 2026-06-30：追加 R3（每迭代 ADD/EDIT/DELETE changelog 正式化），落点用户倾向复用 `iterations/ITER-NNNN/CHANGELOG.md` 槽位、收编现有 `01_CHANGELOG.md` 半成品；排在 ITER-0017 之后。
- 2026-06-30：R3 changelog 格式定调（经四方案对比后用户选回当前提案）——操作分组 bullet，三段 `## ADD` / `## EDIT` / `## DELETE`（严格三类、无内容写"无"不省段）；每条 `` `对象 §章节` — 一句话语义 → ACn ``；顶部 `> <标题> · <active|closed> · <收口日期>`。
- 2026-06-30：R1 收口（ITER-0017），开 R3（ITER-0018）。**执行顺序确定 R3 先于 R2**（R3=ITER-0018、R2=ITER-0019）——先用 R1+R3 补齐收口产出（前滚 PROJECT + 每迭代 changelog），再由 R2 给完整收口加门槛；且 R3 纯 markdown、可 dogfood、风险低于 R2（动 hook 代码）。
- 2026-06-30：R3 收口（ITER-0018）。R1+R3 完成、收口产出已补齐（前滚 + changelog）；里程碑仅剩 R2（收口门槛）待做，待其收口后聚合发布。
- 2026-06-30：开 R2（ITER-0019）——里程碑收尾路线项。三件：执行门禁 hook（单 active 迭代不变量）+ 冷启动一致性自检探针（prompt 级，butler 自身可跑）+ 原子收口仪式（§5.5 清单化 + 末尾自检）。
