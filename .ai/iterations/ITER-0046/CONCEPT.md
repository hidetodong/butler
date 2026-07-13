> 分流: 完整 | 命中升级信号: 新增仓内资产（个人沟通风格正本文件）+ 改 setup.sh 装法（全局 @import）+ 整合去重（散在 matrix 输出风格与多个记忆文件的风格规矩收敛为单一正本）| 2026-07-13

# 一句话
- 我「该怎么跟用户说话」的规矩现在**散在两处**：`~/.claude/output-styles/matrix.md`（一个**只有切到该输出风格才生效**的本机文件，装了整套基调/详略/说人话/结尾块）＋ 几个**记忆文件**（话砍到骨头、别抛选择菜单，说人话还和 matrix 各写一份）。散、条件生效、还双写。
- 本迭代把这套规矩**收敛成一份唯一正本** `communication-style.md`（住 butler 仓根、随 git 跨机器同步），由 `setup.sh` 写一行 `@import` 进全局 `~/.claude/CLAUDE.md`，**每个会话每个项目常开**；matrix 输出风格作为过渡产物**退休**（本机一次性迁移）；记忆文件掏成只记来龙去脉的薄壳。

# Goal
- 让「用户要我怎么沟通」有**唯一正本、常开、可跨机器同步**：一处写、全局生效、不再依赖「有没有切到某个输出风格」。
- 收敛去重：matrix 的 7 节（基调/详略/抓重点/说人话/格式/结尾决策块/边界）＋记忆里两条真增量（话砍到骨头、别抛选择菜单）并进 `communication-style.md`；规矩正文只此一份，记忆只留原因。
- 交付走**全局 @import**（与 butler「全局引用、不逐项目拷贝」同模型），不进 `templates/`、不改逐项目部署面——与 ITER-0045 全局软链同构。
- matrix 退休时**同步拆掉 `claudep` 里为启用它加的 `--settings` 参数**（fish + zsh 两处），否则命令指向一个已不存在的风格。

# Current Understanding
- **散在哪、怎么生效（已核）**：matrix.md 是**输出风格文件**，官方机制是「切到该风格时整块塞进系统提示」，**不支持 `@import`**（已查证，见 mem S1325）——所以两条分发路子（输出风格 vs 全局 CLAUDE.md 导入）没法共享同一物理文件，要单一正本就得选一条路。
- **常开 vs 条件生效**：全局 `~/.claude/CLAUDE.md` **每个会话都加载**；输出风格只有被选中才加载。用户要的是「说话规矩永远在」，且**跨机器同步**——正本必须落进随 git 走的 butler 仓 + 走常开的 CLAUDE.md 导入，不能只留在本机输出风格里。
- **setup.sh 受管块机制（已读）**：第 2 步用 `<!-- butler-global-config -->` 双标记把 butler 区块包起来（awk 删旧块、heredoc 追加新块，用绝对 `$BUTLER_DIR`）。把 `@$BUTLER_DIR/communication-style.md` 加进这个 heredoc 即可——路径天然绝对、跨机器正确、随 setup 重跑幂等刷新。
- **claudep 现状（已读）**：`~/.config/fish/config.fish:73` 与 `~/.zshrc:177` 各定义一份 `claudep`，都是 `proxyon` + `claude --settings '{"outputStyle":"Matrix"}' <args>`。matrix 退休后删掉 `--settings` 段，剩 `proxyon` + `claude`（纯开代理起 claude 的启动器，仍有用）。
- **「偏好」一词已被占（已核）**：`Coder/70_Extension_Preference/preference-probe-engine.md` + `templates/preference/` 是**学习用户工程决策倾向**的另一套（存仓外 `~/.butler/preferences/`、喂 P2/P3 提案）。与本文件（手写的说话方式、存仓内、常开）是两码事——**新文件绝不叫 preference**，避免概念混淆。

# Constraints
- **单一正本 / DRY**：规矩正文只在 `communication-style.md`。matrix 清空退休、记忆掏薄壳，杜绝三处各写、杜绝漂移。
- **收敛不改味**：matrix 里已被用户调过的措辞与 ❌/✅ 例子尽量**逐字保真**搬进正本；只新增两条（话砍到骨头折进「详略」、别抛选择菜单独立成节）。说人话每条留一对 ❌/✅（用户拍板：带例子，规矩才咬得住）。
- **边界守恒**：正本**只管说话方式**；任务怎么做、用什么工具、butler 工程规矩、交付正式文档语气，一律不进（matrix 的「边界」节保留强化——因为它现在是全局常开，更要防它渗进工程行为）。
- **仓内改动最小**：只动 `communication-style.md`（新增）+ `setup.sh`（加 @import 行）+ `README.md`/`HUMAN_GUIDE.md`（注册）+ `.ai/` 收口折叠 + 发布载体；**不**改 `Coder/**` 规则正文、**不**动 `templates/`（不进逐项目部署面）、**不**改四件套 schema / hook / `.gitignore`。
- **本机迁移与仓改动分离**：删 matrix.md、改两处 claudep、查 settings.json、掏薄壳记忆——这些落在**本机 dotfile / `~/.claude` 配置**，不在 butler 仓、不进本次提交；作为一次性**手动迁移步**在 migration 配方里如实写清（与 ITER-0045「机器级重跑 setup.sh」同类）。

# Impact Scope
- 新增（仓内正本）：`communication-style.md`（butler 仓根）——收敛后的唯一沟通风格正本。
- 改（分发装法）：`scripts/setup.sh`（第 2 步受管 heredoc 加一行 `@$BUTLER_DIR/communication-style.md`）。
- 改（文档注册）：`README.md`（结构树登记根文件一行，**不进** Coder SOP 阅读顺序）、`HUMAN_GUIDE.md`（安装节点明「重跑 setup 即装上全局常开的沟通风格配置」）。
- 折（知识文件夹，收口）：`.ai/project/capabilities.md`（加「个人沟通风格全局常开正本 + setup @import 能力」）、`frontier.md`（刷 v2.6.0）。
- 本机迁移（**不进仓提交**，migration 配方记为手动步）：删 `~/.claude/output-styles/matrix.md`；`~/.config/fish/config.fish` + `~/.zshrc` 两处 `claudep` 去掉 `--settings '{"outputStyle":"Matrix"}'`；查 `~/.claude/settings.json` 无残留 `outputStyle:Matrix`；重跑 `setup.sh` 写入 @import；`~/.claude/.../memory/` 三个风格记忆掏薄壳 + 改 `MEMORY.md` 索引。
- 明确不影响：`Coder/**` 规则正文、`templates/**`、四件套 schema、`templates/hooks/**`、`.gitignore`、核心 P1–P5 状态机、基地车逐项目部署产物、既有「偏好探针」子系统。
- 发布层（独立 chore(release) 提交）：`VERSION` 2.5.0→2.6.0、`CHANGELOG.md` 顶条、`migrations/v2.6.0.md`。

# Project Type / Active Profiles
- butler 规则仓库自身 dogfood——新增并接线一份仓内资产（沟通风格正本）+ 改分发脚本 + 文档 + 本机迁移；非用规则开发软件。
- 无 Domain / Stack Profile 命中；按通用 SOP + 仓库 `CLAUDE.md` 编辑约定推进。核心改动含一段 bash（setup.sh @import），验证走隔离 HOME 实跑。

# Open Questions
- 正本该不该也把「结尾决策块」这种较重的格式常开？→ **保留**：它本就写「需要我拍板时才这样收尾」，非每条触发，常开成本低（用户已拍板先留、要砍再说）。
- 记忆薄壳留还是删？→ 已定**留薄壳**（只记原因/教训 + 指向正本，不抄规矩），保住「为什么」又不双写。
- 是否把 matrix 也留个空壳指路？→ 已定**不留**：matrix 是过渡产物，直接删；claudep 同步拆参数，settings 查残留。
