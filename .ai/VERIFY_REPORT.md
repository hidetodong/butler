# VERIFY_REPORT — ITER-0046（个人沟通风格常开正本 · communication-style.md + setup.sh @import + matrix 退休）

# Verification Summary
- 覆盖：新建收敛后的沟通风格唯一正本、给 `setup.sh` 接上「@import 正本进全局 CLAUDE.md 常开」这条分发线、注册文档、matrix 输出风格退休（本机迁移 + 拆 claudep 参数 + 查 settings）、三风格记忆掏薄壳、折叠收口 + 切版。
- 总体结论：**AC1–AC8 全过**。AC1–AC6 已实测全过（读文件核 + 隔离 HOME 实跑 setup.sh + 本机迁移后读文件核，非纸面）；AC7（migration 配方）与 AC8（收口五步 + 三载体对齐 + 两提交分离）于收口 / 发布阶段完成并核。
- 迁移前做了**内容不丢核验**：matrix 全部小节与关键 ❌/✅ 例子逐条确认已在正本，才删 matrix.md。

# AC Status（道 + 置信档）
- [x] AC1 (auto·可靠): 已满足 ✓（正本 8 节齐、说人话 4 条各带例、别抛菜单节带例、开篇定位在、边界干净）
- [x] AC2 (auto·可靠): 已满足 ✓（隔离 HOME 实跑，受管块内 @import 行恒=1、连跑两次仍=1、退出 0）
- [x] AC3 (auto·可靠): 已满足 ✓（抽出 @import 绝对路径 `test -f` 为真、目标文件存在）
- [x] AC4 (auto·可靠): 已满足 ✓（README 结构树登记 + 快速上手注释；HUMAN_GUIDE「四件事」第 4 条 + 说人话）
- [x] AC5 (auto·可靠): 已满足 ✓（matrix.md 已删；fish/zsh 两处 claudep 无 `--settings`/Matrix 残留、保留 proxyon+claude；settings.json 无 Matrix）
- [x] AC6 (auto·可靠): 已满足 ✓（三记忆掏薄壳、只留来龙去脉 + 指向正本；MEMORY.md 三索引改；MILE-0003 引用留存）
- [x] AC7 (auto·可靠): 已满足 ✓（`migrations/v2.6.0.md` 写清目标项目 `.ai/` 部署面 `[no-op]`+`[restamp]` + 机器级重跑 setup 装 @import + 本机一次性清理 matrix/claudep 可选手动步）
- [x] AC8 (auto·可靠): 已满足 ✓（收口五步齐：归档 `iterations/ITER-0046/` + 交付 `.md`+`.html` + 台账 `closed`/`current: none` + 折叠 `capabilities`+`frontier` + 6 不变量自检；三载体对齐 `VERSION`==tag `v2.6.0`==`CHANGELOG` 顶条 `## [2.6.0]`；feat 提交与 `chore(release)` 提交分离）

# Verification Results
- **AC1**: `communication-style.md`（仓根）通读——开篇 `>` 定位块（唯一正本 / 常开 / 跨机器同步 / 只管说话方式 / 反馈往这写）在；8 节齐：基调 / 详略〔含「话往短里写」折入的「话砍到骨头」〕/ 抓重点 / 说人话〔术语先解释·比喻要落地·别让英文变量裸奔·别把词掐短，4 条各一对 ❌/✅〕/ 别急着抛选择菜单〔讨论 + 执行两侧 + 一对 ❌/✅ + grill 例外〕/ 格式 / 结尾决策块 / 边界〔强化「只改说话方式、全局常开更要守」〕；边界节确认无工程 / 工具 / 任务执行规矩混入。✓
- **AC2**: `env HOME=<tmp> bash scripts/setup.sh` 首跑退出 0；`<tmp>/.claude/CLAUDE.md` 受管标记 `<!-- butler-global-config -->` 恰 2 行（一对包裹）、块内 `@…communication-style.md` 恰 1 行；连跑第二次退出 0、该行仍恰 1（awk 删旧块重写、幂等无重复）。✓
- **AC3**: 从受管块抽出 `@` 行去掉前缀得绝对路径 `…/communication-style.md`，`test -f` 为真——路径绝对、指向真实存在的正本文件。Claude Code 运行时是否真并入属运行时行为，验证止于「路径正确 + 文件存在 + 受管块合法」（对齐 ITER-0045「止于文件落位」边界）。✓
- **AC4**: `README.md` 目录结构树新增 `communication-style.md` 行（标个人全局配置 / setup @import 常开 / 不进 Coder 阅读顺序）+ 快速上手第 1 条注释补「@import 沟通风格常开」；`HUMAN_GUIDE.md` §3 安装从「三件事」改「四件事」、第 4 条讲清 @import 沟通风格正本 + 一句它管什么、结尾补「AI 也按你的沟通风格说话」。措辞说人话。✓
- **AC5**: 迁移前逐节核 matrix→正本无遗漏（21 个关键锚点全 ✓）；`rm ~/.claude/output-styles/matrix.md` 后 `test -e` 为假、目录空；`~/.config/fish/config.fish` 与 `~/.zshrc` 两处 `claudep` 去掉 `--settings '{"outputStyle":"Matrix"}'`、现为 `proxyon` + `claude <args>`，grep `outputStyle`/`Matrix`/`--settings` 零命中；`~/.claude/settings.json` 无 Matrix（无该配置项）。✓
- **AC6**: `style-concise` / `style-plain-language` / `discussion-mode-no-forced-menus` 三文件规矩正文（How to apply 块）删除、首段改「规矩正文已迁到唯一正本 communication-style.md …本文件只留来龙去脉」薄壳声明 + 保留出处 incident；`MEMORY.md` 三索引行改薄壳描述；`style-plain-language` 内 `[[mile-0003-agent-doc-design]]` 引用原样保留。✓

# Gate Coverage
- 通用质量门禁：核心改动含一段 bash（`setup.sh` 受管 heredoc 加 @import 行）——已隔离 HOME 端到端实跑（首跑 / 幂等连跑两次 / 抽路径 test -f 三路径）+ `bash scripts/setup.sh` 退出 0。文件类改动（正本 / 文档 / 记忆薄壳 / claudep）经读文件 + grep 逐条核，含**迁移前内容不丢核验**。
- Active Profiles：无命中（butler 规则仓自身 dogfood），N/A。
- Tech Plan Alignment：6 条 Design Decisions 全兑现——决策 1（走 @import 非输出风格）✓、决策 2（收敛去重单一正本）✓、决策 3（直接删 matrix + 拆 claudep + 查 settings）✓、决策 4（带 ❌/✅ 例子）✓、决策 5（名 communication-style、仓根、不进 SOP 读序）✓、决策 6（MINOR + 部署面 `[no-op]`+`[restamp]` + 机器级重跑 + 本机手动清理）→ AC7 发布回填。
- References Compliance：本轮无 `.ai/references/`，N/A。

# Independent Review
- 未触发独立复核：改动是一段幂等 bash（@import 行）+ 一份手写风格正本 + 文档 + 本机配置迁移，无跨多规则的契约面 / 哲学底座变更；核心风险（bash 正确性 + 内容不丢）已由隔离 HOME 实跑与迁移前逐节核验覆盖。opt-in 复核按需，本轮 N/A。

# Remaining Risks
- **@import 运行时并入属 Claude Code 行为**：非本仓可断言，验证止于路径绝对正确 + 目标文件存在 + 受管块合法（AC3 已记此边界）。真正生效需用户在**主检出**重跑一次 `setup.sh`（本机迁移动作，migration 配方写清）。
- **本机迁移跨机器不自动传播**：matrix.md 与 claudep 都是本机配置；换机器若也有旧的同样设置需同样清一遍。但新机器的沟通风格来源已是同步的正本 + setup 的 @import，本身不依赖 matrix。
- **全局常开的常驻 token 开销**：正本约 matrix 量级（几百 token），每会话加载。用户已拍板「带例子换规矩能落地，值」，接受。

# Handoff / Next Step
- 已达可交付闭环（AC1–AC6 实测过，AC7/AC8 待发布回填）。收口五步 → feat 提交（communication-style.md + setup.sh + 文档 + `.ai/` 产物）→ 独立 `chore(release)` 切 v2.6.0（含 migration）→ push 分支 + 开 draft PR。
