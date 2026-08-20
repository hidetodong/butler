<!-- butler-artifact-template: 1.0.0 artifact=changelog -->
# ITER-0114 变更流

> 项目全貌产物重建：按内容性质分家（MILE-0016 R3） · active · 2026-08-20

## ADD

- `scripts/sync-project-overview.py`：新建全貌生成器，`--check` / `--write` 互斥必选、`--project-root` 与 `--butler-root` 分开传（沿用 `sync-workflow-registry.py` 的形状与 `atomic_write`）；五个机器源头缺任意一个都在渲染前抛 `missing source: <path>`，不产出残缺页 → AC1
- `scripts/sync-project-overview.py` 五个渲染函数（`section_version` / `section_milestones` / `section_rules` / `section_workflows` / `section_tools`）：分别派生自 `VERSION` + 双台账 current、`.ai/MILESTONES.md` + `.ai/state-index.json` 冷片计数、`Coder/README.md` 目录段、`workflows/registry.json` 的 Router + 13 条业务工作流、`tools/` 子目录清单 → AC2
- `scripts/sync-project-overview.py` `check()`：逐节 sha256 比对，诊断指名 `overview section drift: <节标题>`；另有 `overview section set mismatch` / `overview header drift` / `overview missing` 三类，不合并成一句「文件有差异」 → AC3
- `scripts/sync-project-overview.py` `OVERVIEW_MAX_BYTES = 12000`：体量上限写死为常量，`--write` 与 `--check` 两侧都校验，超限诊断给出实测值与上限且不写盘 → AC4
- `scripts/sync-project-overview.py` `invariant_pointer_errors()`：无真源指针条目的棘轮，基线常量 `INVARIANT_POINTER_EXEMPT = 16`，只拦增量；超基线时把全部无指针条目逐条列进诊断 → AC8
- `.ai/OVERVIEW.md`：生成物本体，收口时 8897 字节 / 五节；页首两行写明由哪五个源头经哪条命令生成、请勿手改，并声明「只装可派生的事实，长期决策见 `.ai/invariants.md`，会过期的判断见 `.ai/debt.md`」；正文零手写槽位 → AC2
- `scripts/test-sync-project-overview.py`：合成夹具单测，10 个测试方法覆盖 11 个负例场景——五个源头各自缺失（subTest ×5）、`tools/` 整个不在、逐节漂移、节集不匹配、体量超限（400 个合成工具目录）、棘轮超基线、目录在 `Coder/README.md` 无说明；外加三个正例（写后 check 干净、二次写幂等、`--check --write` 同传报互斥） → AC14
- `.ai/invariants.md` 文件头「写作纪律」三条：只写决策与理由不复述机制形状 / 每条至少一个反引号真源指针 / 还成立才留作废即删；同段登记棘轮基线 16 并声明「16 是欠账不是允许额度」，指向 `.ai/debt.md` → AC8
- `Coder/README.md` 目录结构段：补上此前缺说明的 `55_Extension_ConvergenceLoop/` 与 `60_Extension_CodeReview/` 两条——生成器对无说明目录 fail-closed，缺说明会直接让 `--write` 报错 → AC1/AC2
- `Coder/README.md` 工具注册段：登记 `scripts/sync-project-overview.py` 的职责与两种模式 → AC12
- `scripts/verify-ci.sh`：新增两行——先跑 `test-sync-project-overview.py`，再跑 `sync-project-overview.py --check --project-root .`，位置与既有 `--check` 类检查一致 → AC5
- `.ai/debt.md`：追加 6 条——4 条从 `frontier.md`「下一个瓶颈」迁入（运行时观测缺位 / 远端 required check 未启用 / 双宿主语义入口未经真实安装人测 / 危险模式规则真源仍把 P4 与 `/butler:loop` 绑定），每条注明来源与迁入迭代；2 条本轮新记（`.ai/invariants.md` 16 条无指针的存量欠账、`iteration-schema.md §5.3` 修订记录要求与产物合同的冲突） → AC10
- `.ai/MILESTONE.md §5.4`：登记 R3 两条前提修正与一条发布处置追记 → AC13

## EDIT

- `.ai/project/invariants.md` → `.ai/invariants.md`：`git mv` 迁位，47 条正文原样带走，git 记为 R100 全等重命名（提交后 `git log --follow` 可穿透） → AC6
- `.ai/invariants.md`「收口是原子仪式」条：删掉五步清单与已作废的 `fold receipt`，改为「步骤、顺序与哪几步必做以 `iteration-schema.md §5.5` 为准」+ 原有的为什么。**按新纪律它不再写步数**——AC7 里「写四步」这半由指针指向的真源承担（§5.5 实测 4 步、第四步是收口自检），条目自身只留决策与理由 → AC7
- `.ai/invariants.md`「冷启动读序固定且只有一处真源」条：删掉旧四步措辞，改为「步骤与顺序以 `context-persistence.md §6` 的读序块为准，其余载体只能是它的字节投影」+ 为什么（实测曾有五份不同版本共存） → AC7
- `Coder/40_Context_Management/context-persistence.md` 读序块后那段：替换 R1 留的占位措辞，写清三份产物的性质分工表（`.ai/OVERVIEW.md` 机器派生 / `.ai/invariants.md` 长期决策 / `.ai/debt.md` 会过期的判断）、重算命令原文，以及 `frontier.md` 的教训——整体覆写只在有强制触发时才活得下来 → AC12
- `Coder/40_Context_Management/context-persistence.md §6` 读序块第 5 步（真源）：句尾补「需要项目全貌时按需读 `.ai/OVERVIEW.md` 与 `.ai/invariants.md`，不是必读」，措辞明确为按需不是必读；五步语义结构未动 → AC11
- `AGENTS.md`、`templates/AGENTS.md.template`、`templates/CLAUDE.md.template`、`Coder/README.md` 四处读序投影：同步真源改动，五处仍逐字节相同；块体量 1284 字节（上限 1400），指针 9 个、非空行 6 行 → AC11
- `tools/context-budget/context_budget.py` 必读文件清单：`.ai/project/invariants.md` 改为 `.ai/invariants.md` → AC6/AC12
- `tools/context-budget/tests/test_context_budget.py`：夹具拷贝清单同步改路径，读序块基线由 1194 字节 / 7 指针改为 1284 字节 / 9 指针 → AC11
- `.ai/ITERATIONS.md` / `.ai/MILESTONE.md`：`current` 置 ITER-0114，R3 路线行置 active 并绑本迭代 → 无对应 AC（收口台账维护）

## DELETE

- `.ai/project/frontier.md`：整份退役，三节 28 条逐条处置，无一条无交代 → AC9
  - **当前形态 15 条**：版本那条并入 `OVERVIEW`「版本与当前状态」生成段；MILE-0010/0011、Explore 与 Decision Map 四条、领域模型治理、开源入口、升级器摘要口径共 9 条是里程碑完成陈述，并入「里程碑时间线」生成段（源头是双台账，不再手抄）；三宿主 / 工程化加固 / 双宿主治理 3 条里可派生的部分并入「工作流清单」与「驻留工具清单」生成段，其余成就叙述可弃——历史归 `.ai/ITERATIONS.md` 与 `deliveries/`；「语义入口」待人测那条迁入 `.ai/debt.md`；「远端保护」那条迁入 `.ai/debt.md`（与「下一个瓶颈」的远端 required check 合并成一条，原本是重复表述）
  - **活跃战线 6 条**：MILE-0013 / MILE-0009 链路 / MILE-0014 / 危险模式与 MILE-0015 收口状态 4 条全部可从双台账派生，并入「里程碑时间线」与「版本与当前状态」生成段；真实 `WorkCode.nosync/apps` 验证那条可弃——它是 ITER 级执行记录，真源在 `deliveries/`；ITER-0098 那条前半（已关闭）并入生成段，后半 GitHub Private Vulnerability Reporting 待核验并入 `.ai/debt.md` 的远端条
  - **下一个瓶颈 7 条**：运行时观测缺位 / 远端 required check / 危险模式与 Loop 绑定 3 条迁入 `.ai/debt.md`；语义入口人测那条已在「当前形态」计入迁入；MILE-0009 已随 v3.0.0 发布那条可弃——它陈述的是已发布事实不是瓶颈，且台账可派生；milestone backlog「当前有 11 个独立候办」可弃——`.ai/MILESTONES.md` 候办索引与 `.ai/milestone-backlog/` 是真源，这里是会过期的副本（实测已不是 11）；项目自有 hook 共存那条可弃——`.ai/debt.md` 早有同一条，属重复；`[regen-entrypoints]` 切版提醒可弃——`.ai/MILESTONE.md §5.4` 已在 R2 接手登记
- `.ai/project/` 目录：`invariants.md` 迁出、`frontier.md` 退役后目录已空，随之移除；butler 仓自己不再有 `.ai/project/` → AC9/AC12
- **覆盖面变化（不是等价替换）**：`frontier.md` 声称「整体覆写、一直准确」，实测停更两个迭代——因为没有任何机器检查强制它重写。接手它的 `.ai/OVERVIEW.md` 补上了这个强制触发（`--check` 进 CI，源头一动就红）；但 `--check` 只能证明「生成段与机器源头一致」，证明不了「这份全貌被任何会话读过」，后者仍要等 MILE-0016 R11 的运行时观测 → AC15
