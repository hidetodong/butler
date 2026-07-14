> 分流: 完整 | 命中升级信号: 多文件新增（3 命令）, 可能触碰 Coder 真源触发词, 涉及发布切版 | 2026-07-14

# 一句话

套 R1 固化的「薄壳路由器」范本，一次批量落 3 个低风险纯薄壳命令 `/butler:milestone`、`/butler:upgrade`、`/butler:ideation`，把 MILE-0005 从「地基 + 1 命令」推进到「命名空间里住着一批命令」。

# Goal

MILE-0005 R2：验证 R1 范本可**批量复制**——不再一个一个精雕，而是照着 `prd.md`/`review.md` 的固定骨架（frontmatter 说人话 → 薄壳三件事声明 → 跨 cwd 路径约定 → 第 0 步优雅降级 → `$ARGUMENTS` 路由 → 一句话收尾）快速产出三个语义清晰、无风险闸的命令，各自委托既有真源规则、不复述算法。

# Current Understanding

- **三个命令的真源与路由**（都已读入口段确认）：
  - `/butler:milestone` → `20_Workflow_Lifecycle/milestone-schema.md`：留空/给 brief → 里程碑录入（含「brief 是大 PRD」并进 `prd-split` 的分支）；`status` → 只读看板。里程碑是方向性不冻结层，命令只路由、不碰 ACK。
  - `/butler:upgrade` → `20_Workflow_Lifecycle/butler-upgrade.md`：已部署项目按 `migrations/` 区间幂等升级；侦察 + 区间配方执行，升级对象是**当前项目**。真源 §2 现把 `/butler-upgrade`（连字符）列为显式触发词。
  - `/butler:ideation` → `50_Extension_Ideation/ideation-engine.md`：模糊需求多维压力测试 → AC 收敛；无子参数。
- **范本已由 R1 固化**：`prd.md`（三分支 + 第 0 步读契约）、`review.md`（两分支 + 第 0 步查有无对象、优雅降级）证明骨架可复制；R2 是范式的第一次「批量」检验。
- **命令是个人工具、全局软链**：新命令往 `.claude/commands/butler/` 一丢，就随 R1 改好的目录软链自动全局可用——**R2 不用再动 `setup.sh`、不用再改分发**（这是 R1 目录软链的红利）。
- **低风险**：三命令都无 `loop`/`dangerous` 那种「郑重显式触发」门槛，不需风险闸（那是 R4）。

# Constraints

- **不改真源规则算法**：三命令委托的 `Coder/**` 规则正文语义一律不动（沿用 MILE-0005 Out of Scope）。唯一可能的例外是 `/butler:upgrade` 是否顺带把 `butler-upgrade.md §2` 的触发词 `/butler-upgrade` 改成 `/butler:upgrade`——那是**触发名**更新、非算法，且要 P2 显式定（见 Open Questions）。
- **不下发目标项目**：命令不进 `templates/`、目标项目部署面零影响（沿用 ITER-0044/0047 边界）。
- **不新造命令能力**：只把既有散文触发词落成真实文件，不发明新命令、不扩既有命令语义。
- **不动 `setup.sh` 分发逻辑**：R1 的目录软链已托管全套，R2 只往目录里加文件。
- **薄壳纪律**：只做「读对规则进上下文 + 按参数路由 + 委托真源」，不复述算法（DRY 红线）；每个命令带第 0 步优雅降级。

# Impact Scope

- **新增**（命令层）：`.claude/commands/butler/milestone.md`、`upgrade.md`、`ideation.md`（3 个薄壳）。
- **可能改**（待 P2 定，见 Open Questions）：`butler-upgrade.md §2` 触发词、`.ai/project/capabilities.md` 命令表（转换/并列/顺清 R1 遗留冗余）、README 目录树（补 3 个命令）。
- **发布层**：VERSION + CHANGELOG + `migrations/vX.Y.Z.md`（切版号待定）。
- **不碰**：`setup.sh`、`templates/**`、四件套 schema、hook、任何规则算法、`/butler:prd`·`/butler:review`。

# Project Type

Markdown 规则仓库 dogfooding（butler 编辑自身命令层）。无代码编译，验证靠：命令文件结构核（薄壳四要点齐 + 真源锚点真实）+ 隔离 HOME 实跑 `setup.sh` 确认 3 新命令经目录软链可达 + `git diff` 边界守恒。

# Open Questions

1. **切版号**：R2 纯新增 3 个命令、无破坏面（不像 R1 有 `/butler-prd` 改名），判 **MINOR**（新增能力）还是可并入某个更小语义？倾向 MINOR（新增命令 = 新增可扩展能力，与 R1 同类）。
2. **`/butler-upgrade` 触发名是否一并迁 `/butler:upgrade`**：R1 已把同形的 `/butler-prd`→`/butler:prd`。`butler-upgrade.md §2` 明列 `/butler-upgrade` 为触发词，若不改则命名空间里有 `/butler:upgrade` 命令、真源却仍说触发 `/butler-upgrade`，不一致。倾向**一并迁**（改 §2 触发词 + capabilities，属触发名非算法、与 R1 一致），保留「升级 butler / 同步新版」自然语言触发。
3. **capabilities 命令表整理方式**：R1 给 `/butler:review` 加了新行、却留下 `/review` 旧行（并列小冗余）。R2 三命令是**转换**旧的 `/ideation`·`/milestone`·`/butler-upgrade` 行为 `/butler:*`，还是**并列**新增？倾向转换（命名空间命令是这些能力的一等入口，散文触发降为语义 fallback），并顺清 R1 遗留的 `/review` 冗余——但这会多动几行 capabilities，需确认是否纳入本迭代。
