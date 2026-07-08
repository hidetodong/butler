# TECH_PLAN — ITER-0035（补 [split] 升级接线缺口）

> 监督态自驱（非 /dangerous）。目标见 CONCEPT、验收见 AC_LIST，不重述。全为规则文档接线改动。

## 设计决策（DD）

- **DD1 · `[split]` = opt-in 结构迁移步**（AC3/AC4）：机械标签升级时静默自动跑；`[split]` 执行器碰到时把它抛成一道用户选择（迁 / 继续单文件），选后者跳过、单文件继续支持。类比既有 `[add-field]` 草稿 ACK / 漂移即停 ACK——结构性 / 高风险步骤自带确认闸，不破坏幂等。
- **DD2 · 语义真源不搬家**（AC5）：`[split]` 拆什么 / 判据 / 冲突即停仍以 `migration-schema §4` 为真源；`butler-upgrade §6.5` 只写"执行器怎么落地"（起始态校验 + opt-in 闸 + git 动作），回指 §4 不重述。新增 §6.5 与既有 §6.1/6.2/6.4（rename/add-field/sync-hooks 落地细则）同构、编号顺延。
- **DD3 · 最小改动接线**（AC8）：不动 `[split]` 语义、不动其它标签逻辑；只在 `§5.1` 枚举补一项 + 新增一个 §6.x 小节 + `§7` 加一行 + `migration-schema §4` 加一句指针。

## 影响面（章节级）

| 文件 | 改动 | AC |
|---|---|---|
| `butler-upgrade.md §5.1` | typed 标签枚举补 `[split]`（指 §6.5） | AC1 |
| `butler-upgrade.md` 新 `§6.5` | `[split]` 落地细则（起始态校验 + opt-in 选择闸 + 拆分动作 + 冲突即停 + 暂缓分支 + 回指 §4） | AC2/AC3/AC4 |
| `butler-upgrade.md §7` | 验证清单加一行（`[split]` 结果二选一如实报告） | AC6 |
| `migration-schema.md §4`（`[split]` 条） | 补一句执行语义交叉引用（指 `butler-upgrade §6.5`），语义真源仍 §4 | AC5 |
| `migrations/v2.0.0.md`（若需） | 核措辞与新口径自洽（已写"可暂缓"，预计无需改或微调） | AC7 |

**不碰**：`[split]` 语义定义（§4 真源）、其它 typed 标签执行逻辑、`mcv-deployment` 部署种子、`.ai/project/` 结构契约、hook、`VERSION`、rename、README（butler-upgrade 已注册）。不真跑 `/butler-upgrade`。

## Execution Steps（可勾选）

- [ ] S1 · `butler-upgrade §5.1` 标签枚举补 `[split]` → AC1
- [ ] S2 · 新增 `butler-upgrade §6.5 [split] 落地细则`（起始态校验 + opt-in 选择闸 + 拆分 git add + 冲突即停 + 暂缓分支 + 回指 §4）→ AC2/AC3/AC4
- [ ] S3 · `butler-upgrade §7` 验证清单加一行 → AC6
- [ ] S4 · `migration-schema §4` `[split]` 条补一句执行语义交叉引用 → AC5
- [ ] S5 · 核 `migrations/v2.0.0.md` 措辞与新口径自洽（微调或确认无需改）→ AC7
- [ ] S6 · scope 守恒核对（`git status`）+ dogfood 说人话三条自检 → AC8/AC9
- [ ] S7 · P5 独立复核（干净上下文子 agent，对抗式：opt-in 口径是否真守两态 / 语义无双写 / 起始态校验与冲突即停齐 / 枚举无遗漏）
- [ ] S8 · 原子收口（归档四件套 + 交付 md+html + 翻台账 + 文件夹态按主题折叠 + 6 不变量自检）+ `feat` 提交

## 验证策略

全 auto·可靠（规则文档）：每 AC 读改后正文确认 + `git grep` 核守恒。核心对抗点＝**opt-in 口径真守两态**（选继续单文件则单文件分支不被砸）+ **语义不双写**（§6.5 只写执行落地、语义回指 §4）+ **起始态校验 + 冲突即停齐全**（不拆丢用户内容）。dogfood：四件套过说人话三条。无人测道残余。
