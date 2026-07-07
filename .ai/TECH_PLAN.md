# TECH_PLAN — ITER-0031（MILE-0003 R5）

> 监督态自驱（非 `/dangerous`）：本产物由用户"继续吧"委托、模型自驱产出，P5 起独立复核守质量（ITER-0031，2026-07-07）。

## 设计决策（DD）

- **DD1 两态用显式分支、单文件分支绝不隐去**（对 AC1/AC8，make-or-break）：`§冷启动读序` 第 1 项写成两个显式分支——"采用 `.ai/project/` → 00_INDEX + 按需主题"与"仍单文件 `.ai/PROJECT.md` → 读 PROJECT.md"。绝不写成无条件 `00_INDEX`。与 R3 收口步④/第 6 不变量同款两态措辞，全仓一致。
- **DD2 读侧 digest-and-point 只在读序真源写一次**（对 AC2）：读侧纪律（读地图→按需钻主题→指针钻代码、不 slurp）写进 `context-persistence §冷启动读序` 文件夹态分支；写侧密度仍以 `project-digest-schema §5` 为真源、不重抄，只在必要处回指。
- **DD3 翻指针不删声明、三处齐翻**（对 AC4，吸取 R3 教训）：`project-digest-schema` 的 R5 指针在**介绍段 line 9 + §9 路线项 + §9 header** 三处，必须一次齐翻"待→已"，避免像 R3 那样只翻 §9 漏了介绍段。翻后指向真实落点（`context-persistence §冷启动读序` 两态第 1 项），不动 §1 定位（§1 描述文件夹态读法、本就是文件夹态、无需改）。
- **DD4 README/handoff 只同步措辞、不重写读序**（对 AC5/AC6）：README §读取顺序 + handoff §1 均**指** `context-persistence §6` 为读序真源，本轮只把它们的两态措辞对齐，不在这两处复述完整读序（DRY、避免多处读序漂移）。
- **DD5 R5 边界硬钉**（对 AC7）：不碰 `mcv-deployment`（R6 部署仍种单文件，与单文件分支自洽）、`migrations/`（R6）、`VERSION`（R8 切版）、`logic-protocol §1.1`（规则加载序、正交）；不改 R3 强制条与 `.ai/project/` 结构契约。
- **DD6 收口前滚 butler 自身**（对 AC8）：`.ai/PROJECT.md`「冷启动读序固定」条改两态措辞（butler 自身单文件、走 PROJECT.md 分支）+ 知识文件夹条 R5 指针翻已接线；butler 仍单文件、不拆文件夹（那是 R8）。

## 目标文件与改法

1. `Coder/40_Context_Management/context-persistence.md §冷启动读序`（第 1 项两态分支 + 读侧 digest-and-point 纪律 + 收尾互补句两态）→ AC1/AC2/AC3
2. `Coder/40_Context_Management/project-digest-schema.md`（介绍段 line 9 + §9 R5 路线项 + §9 header 翻"已接线（两态）"）→ AC4
3. `Coder/README.md §读取顺序`（冷启动读序描述两态）→ AC5
4. `Coder/40_Context_Management/handoff-spec.md §1`（状态全貌承载产物措辞两态）→ AC6
5. `.ai/PROJECT.md`（收口前滚：读序固定条两态 + R5 指针已接线）→ AC8（收口步④落地）

## Execution Steps（可勾选任务清单，镜像 task-state）

- [ ] T1 改 `context-persistence §冷启动读序`：第 1 项两态分支 + 读侧 digest-and-point 纪律 + 互补句两态（AC1/AC2/AC3）
- [ ] T2 翻 `project-digest-schema` R5 指针三处（介绍段 + §9 路线项 + §9 header）（AC4）
- [ ] T3 改 `Coder/README.md §读取顺序` 两态（AC5）
- [ ] T4 改 `handoff-spec §1` 承载产物措辞两态（AC6）
- [ ] T5 自检：两态分支齐 + 单文件分支显式 + R5 指针三处齐翻 + R3 强制语义未动 + `git status` 未越 R6/R8/R7（AC7/AC8）
- [ ] T6 P5 独立复核子 agent（fresh-context，验证者≠实现者）

## 验证与守恒

- `git status --short` 证明改动集=4 改规则文件（context-persistence/project-digest-schema/README/handoff-spec）+ `.ai/` 台账 + PROJECT.md 前滚，无新增规则文件、无 rename、未触 `mcv-deployment`/`migrations/`/`VERSION`/`logic-protocol`。
- `/usr/bin/grep` 核：R3"必做"折叠 + 第 6 不变量强制语义未被本轮改动；`.ai/project/` 不存在＝butler 自身仍单文件（未越 R8）。
- 模拟单文件项目（如 butler 自身）走单文件分支：第一读 `.ai/PROJECT.md`、不被指向不存在的 `00_INDEX`、不踩空。
