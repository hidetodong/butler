# butler 自身 dogfood 迁 .ai/project/ + 切 v2.0.0

> 分流：完整迭代（P1–P5）+ 独立发布 · ITER-0034 · MILE-0003 R8（压轴）· 监督态自驱（用户"继续"接力，非 /dangerous；P5 起独立复核；**切版 tag 不可逆、执行前另请用户放行**）

## 一句话

MILE-0003 前七轮（R1–R7）把知识文件夹的契约、维护、读序、部署、迁移配方、帮手名册、说人话全建好了，但 butler **自己**还在用旧的单文件 `.ai/PROJECT.md`——R8 让 butler 拿自己当第一个真实用户：按 R2 契约把自己的全貌产物迁成 `.ai/project/` 知识文件夹、对齐所有"butler 还是单文件"的旧说法，然后聚合整个 MILE-0003 切 **v2.0.0**（大版本，因为这是对冷启动核心产物契约的破坏性重构）。

## 背景（为何现在做、为何是最后一轮）

- 前七轮全是"给别的项目用"的规则；butler 自己一直是 R8 前的**已知暂态**（单文件 + 第 6 不变量对自身 N/A）。不迁自己，知识文件夹设计就**从未在真实项目上验证过**（承 R5/R6 交付都点了这条风险）。
- v2.0.0 是 semver 的必然：本里程碑重写了冷启动第一读、全貌产物契约、维护回路——按 `versioning §2` 属 **MAJOR**（破坏性、要求老项目迁移）。切版是 MILE-0003 的收尾动作。

## 做什么（两段，迭代提交与发布提交分开）

### 段A · ITER-0034 迭代：迁自身 + 对齐现实

**A1 · 建 `.ai/project/` 知识文件夹**（按 R2 契约 `project-digest-schema` §3/§5/§8）：
- `00_INDEX.md`（入口三块：一段话是什么 + 读序地图 + 主题登记表）+ 推荐主题集拆分（把现单文件 6 段映射过去，补 R2 新增的两层）：

  | 主题文件 | 承载（源自单文件哪段） |
  |---|---|
  | `identity.md` | 目的 / 定位 / 使用者 / 边界 |
  | `architecture.md` | 架构与模块地图（**已有真源 README/architecture-overview，只摘全貌 + 补成熟度 + 指针**，不抄目录） |
  | `capabilities.md` | 当前能做什么：命令（`/ideation` `/loop` `/review` `/dangerous` `/preference` `/milestone` `/butler-upgrade`）+ P1–P5 SOP + 驻留工具（**R2 新增层**，源自单文件没有的现状清单） |
  | `invariants.md` | 关键长期决策与不变量（三层分层 / 产物链 / 迭代里程碑双层 / AC 脊柱 / 单一来源 / hook 门禁 / 冷启动读序 / 收口原子仪式 / 帮手名册 / 知识文件夹 / 说人话） |
  | `constraints.md` | 现行约束（写作面向 AI / 注册即真源 / semver / 提交规约 / 测试自动化 / 最小实现 / 无人残余） |
  | `debt.md` | 已知长期欠债（不 dogfood hook / `/butler-upgrade` 从未真跑） |
  | `frontier.md` | **R2 新增层**：当前形态（v2.0.0 在即、MILE-0003 收尾）+ 下一个瓶颈 |

- 密度守 digest-and-point（名 + 干什么 + 指针）、每份有界、**已有真源不逐字抄**（§5 明点 butler dogfood 最吃劲处）。

**A2 · 删旧单文件 `.ai/PROJECT.md`**（内容已迁走；这就是 `[split]` 作用在 butler 自身）。

**A3 · 对齐现实**（翻"butler 还是单文件"的旧说法，**两态规则本身不动**）：
- `.ai/task-state.md` 冷启动入口：单文件 → `.ai/project/00_INDEX.md`。
- 全仓"含 butler 仓自身（单文件例子 / R8 前暂态）"的括号例子翻为"已迁移"：`mcv-deployment §2`（line 47）、`context-persistence §6`（line 125 单文件分支去 butler）、`project-digest-schema §9`（line 149/152 + R8 指针 待→已）、`milestone-schema`（若点名）。
- **红线**：两态规则的**单文件分支保留**——R6 前部署的老项目仍是单文件，规则得继续支持；只把 butler 自己从"单文件例子"里挪走，不删单文件态支持。

**A4 · README 文档注册 + 收口**：README 读序/说明里 butler 自身现状对齐；ITER-0034 走**文件夹态**收口（第 6 不变量对 butler 转适用、收口步④按主题折叠进 `.ai/project/`——首次 dogfood 折叠）。段A 以 `feat` 提交。

### 段B · v2.0.0 发布（独立 `chore(release)`，`versioning §6.3`）

- **B1 定 bump**：MAJOR（冷启动产物契约破坏性重构）。
- **B2 改 `VERSION`**：1.7.0 → 2.0.0。
- **B3 加 CHANGELOG**：`## [2.0.0]` 聚合 ITER-0026~0034（含独立 ITER-0027）+ 收口 MILE-0003，只引用不复述。
- **B4 产 `migrations/v2.0.0.md` 实例**（R6 备的形态首次落地）：`[split]`（`PROJECT.md → .ai/project/`，起始态校验 + 冲突即停）+ `[regen-claude]`（区间内 rule-card 改过，ITER-0026/0033）+ `[restamp]` → v2.0.0；核对是否需 `[sync-hooks]`/`[add-field]`。
- **B5 收口 MILE-0003**（`milestone-schema §7`）：MILESTONE 快照进 `milestones/MILE-0003/` + 聚合交付 `deliveries/milestones/MILE-0003-*.md`+html + MILESTONES 台账 closed（补齐含迭代 ITER-0033/0034）。
- **B6 git**：`chore(release): v2.0.0 …` 提交 + `git tag v2.0.0`；**切版前预检 6 不变量、切版后核对三处版本载体对齐**。

## 边界（R8 不做）

- 不改两态规则的**逻辑**（单文件态支持保留给老项目；只迁 butler 自身 + 翻自身例子）。
- 不改 R2 `.ai/project/` 结构契约、R3 折叠语义、R5 读序逻辑、R7 说人话——本轮是**消费**它们，不重定义。
- 不动 hook 代码、不改四件套字段结构、不碰 `Learner/`/`Composer/`。
- 不在段A 的迭代提交里混发布元数据（`versioning §5.3`：发布提交独立）。

## 关键设计约束

- **迭代/发布两提交分离**（`versioning §5.3`）：段A `feat` 只装迁移 + 对齐 + `.ai/` 产物；段B `chore(release)` 只装 VERSION/CHANGELOG/migration/里程碑收口产物。
- **迁移后 butler 转文件夹态**：这是自洽的关键——迁完后 butler 冷启动第一读变 `00_INDEX`、第 6 不变量对自身转适用、收口折叠进 `.ai/project/`。对齐现实必须把这点在自身状态文件里翻到位，否则下次冷启动指向已删的 `PROJECT.md` 踩空（对照 R6 MF-1 教训）。
- **tag 不可逆**：v2.0.0 tag 是对外发布锚点、难撤回——段B 执行前另请用户明确放行（段A 迁移可先做、可复核）。
- **dogfood 即验收**：迁完 butler 自己冷启动能不能真读懂自己，是知识文件夹设计第一次真实检验。
