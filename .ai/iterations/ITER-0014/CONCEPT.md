> ⚠️ 危险模式：本产物由模型自主推进、未经用户逐阶段 ACK（已过 dangerous-engine §5 自审门，ITER-0014，2026-06-30）。
> 分流: 完整 | 命中升级信号: 新增规则文件、多文件改动、升级流程改写 | 2026-06-30

# 一句话

现在每次在不同项目里跑 `butler-upgrade`，模型都得现场比对"目标项目 vs butler 最新仓"、自己拼出"哪些文件改了名、哪些字段要补、rule-card 变没变"——同样的活每次重做、还因人/因模型而异，所以你感觉"每次都要模型自己整理流程"。这次把它 SOP 化：每次 butler 切版时顺手写一份"这一版升级要做哪几步"的**迁移配方**存进 `migrations/`；升级时不再现推，直接取"目标版本号到当前版本之间"每一版的配方、按序照做。模型从"想"变成"执行"。

# Goal

- 新增"迁移配方"产物：每个发布版一份机器可照做的幂等步骤清单，是"升级要做什么"的单一来源。
- 把 `butler-upgrade` 从"侦察 + 现场推导差异"改写成"执行器"：读目标版本戳 → 取区间配方 → 按序幂等应用 → 重戳 → 验证。
- 把"切版时必须产出迁移配方"写进版本治理流程，让配方不会漏记。
- 给已发布的 v1.1.0~v1.3.0 补齐配方，让台账不是空的、老项目能立刻用。

# Current Understanding

- 现状不是"没流程"：`butler-upgrade` 已有侦察 / 首次 / 常规 / `.ai/` 升级 / 验证五段。缺的是"每版具体迁什么"没被记录，只能每次现推。
- 唯一的具体迁移知识是 §6.1 那张"已知重命名"手列表——半手工、无维护机制、迟早漂。
- 部署到目标项目的东西其实只有三类会变：① `CLAUDE.md`（含内联的 rule-card 内容 + 版本戳）② `.ai/` 的文件命名与必填字段 ③ `.claude/hooks/` 的副本（`mcv-deployment.md §5.4` 明说升级要同步 hook 副本，但 `butler-upgrade` 至今没做——这次一并补）。Coder/ 规则正文是运行时实时读 butler 仓的、不进目标项目，所以多数版本对部署项目"无结构影响"。
- 配方设计成"幂等 + 先校验起始态"，和现有"版本号为辅、内容差异为主"不冲突：配方做主干，diff 退化成"应用前确认现状、冲突就停下问人"的兜底。

# Constraints

- 不改四件套字段结构、不改 hook 代码、不改 lifecycle 分流。
- 新增规则文件必须在 `Coder/README.md` 注册（本仓 CLAUDE.md 约束 3）。
- `migrations/` 是 butler 仓发布元数据（与 `deliveries/`、`CHANGELOG` 同级），放仓库根，不放 `templates/`（那是给目标项目的模板）。
- 配方对"已手工漂移的目标项目"必须安全：每步先校验起始态，冲突退回真人 ACK，不盲目按版本号套。
- 守本仓 CLAUDE.md 五约束。

# Impact Scope

- 会改 / 新增：
  - 新增 `Coder/20_Workflow_Lifecycle/migration-schema.md`：配方格式 + 台账位置 + 幂等 / 漂移契约的单一来源。
  - 新增 `migrations/` 目录 + `v1.1.0.md` / `v1.2.0.md` / `v1.3.0.md` 三份回填配方。
  - 改 `butler-upgrade.md`：侦察改为收集配方、升级改为执行器、补 hook 副本同步、保留无戳老项目的全量兜底。
  - 改 `versioning-schema.md`：§5 切版流程加"记录迁移配方"必做步 + 指针引用 migration-schema。
  - 改 `Coder/README.md`：注册 migration-schema。
- 不影响：四件套字段、对话层规则、迭代 / 里程碑机制、历史 `deliveries/`、hook 代码本身。

# Project Type / Active Profiles

- 形态：Markdown 规则仓库（butler 自己），改的是协作 SOP 规则。
- Profiles：无，按通用 SOP + 本仓 CLAUDE.md 编辑约束推进。

# Open Questions

- 配方文件用纯 Markdown + typed 步骤标签（`[rename]` / `[add-field]` / `[regen-claude]` / `[sync-hooks]` / `[restamp]` / `[no-op]`），不引入 YAML/JSON，保持人读 + AI 照做；标签集 P3 定。
- 是否给本次发布（拟 v1.4.0）也写一份配方做 dogfood——切版属用户门控动作，收口后建议、不在本迭代自动切。
