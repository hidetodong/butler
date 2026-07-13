---
状态: ack-frozen
ACK 日期: 2026-07-13
---

# Goal
- 把散在 matrix 输出风格与多个记忆文件里的「沟通风格」规矩，收敛成 butler 仓根的**唯一正本** `communication-style.md`，经 `setup.sh` 写 `@import` 进全局 CLAUDE.md **常开、跨机器同步**；matrix 输出风格退休（本机迁移，同步拆 `claudep` 参数）；记忆掏薄壳。边界与迁移动作如实记录。

# In Scope
- 新增 `communication-style.md`（仓根）：收敛 matrix 7 节 ＋ 记忆两条真增量（话砍到骨头折进「详略」、别抛选择菜单独立成节），说人话每条留一对 ❌/✅，开篇写清定位（唯一正本 / 常开 / 跨机器同步 / 只管说话方式 / 反馈往这写）。
- 改 `scripts/setup.sh`：受管 heredoc 加一行 `@$BUTLER_DIR/communication-style.md`（绝对路径、幂等）。
- 注册 `README.md`（结构树登记根文件，不进 Coder SOP 阅读顺序）+ `HUMAN_GUIDE.md`（安装节点明 setup 装全局常开沟通风格）。
- 折叠 `capabilities`/`frontier`；独立发布提交切 MINOR v2.6.0（VERSION / CHANGELOG / migration）。
- 本机迁移（不进仓提交）：删 matrix.md、拆两处 claudep 参数、查 settings.json、掏薄壳三记忆 + 改 MEMORY.md。

# Out of Scope
- 不改任何 `Coder/**` 规则正文、不动 `templates/`（不进逐项目部署面）、不改四件套 schema / hook / `.gitignore`、不碰既有「偏好探针」子系统。
- 不把沟通风格逐项目下发（是**全局**能力，非 per-project；与基地车部署无关）。
- 不给 matrix 留指路空壳（过渡产物直接删）；不在本轮做软链/文件自愈。

# Acceptance Checklist
- [ ] AC1: `communication-style.md` 存在于 butler 仓根，作为**唯一正本**，含全部约定各节：基调 / 详略（含「话砍到骨头」）/ 抓重点 / 说人话（**4 条、每条一对 ❌/✅**）/ 别抛选择菜单（新增节，含一对 ❌/✅）/ 格式 / 结尾决策块 / 边界；开篇声明定位（唯一正本·常开·跨机器同步·只管说话方式·以后反馈往这写）。正文**不含**任何工程/任务/工具执行规矩（边界干净）。
- [ ] AC2: `setup.sh` 在 `<!-- butler-global-config -->` 受管 heredoc 内写入一行 `@$BUTLER_DIR/communication-style.md`（绝对路径展开）；隔离 HOME 实跑后 `~/.claude/CLAUDE.md` 受管区内**恰好一行**该 `@import`，且**连跑两次仍恰好一行**（awk 删旧块重写、幂等无重复）。
- [ ] AC3: @import 路径**解析得到真文件**——`setup.sh` 写入的绝对路径指向的位置确实存在 `communication-style.md`（隔离 HOME 实跑：从 `~/.claude/CLAUDE.md` 抽出 `@` 路径、`test -f` 该路径为真）。Claude Code 运行时是否真把它并入属运行时行为，验证止于「路径绝对正确 + 目标文件存在 + 受管块合法」（对齐 ITER-0045「止于文件落位」边界）。
- [ ] AC4: 文档注册齐——`README.md` 结构树登记 `communication-style.md`（标注为个人全局配置、**不进** Coder SOP 阅读顺序）；`HUMAN_GUIDE.md` 安装节点明「重跑 `setup.sh` 即装上全局常开的沟通风格配置」。措辞守 `artifact-style §2` 说人话。
- [ ] AC5: matrix 退休（本机迁移，验证读本机文件）——`~/.claude/output-styles/matrix.md` 已删除；`~/.config/fish/config.fish` 与 `~/.zshrc` 两处 `claudep` 均**不再含** `--settings '{"outputStyle":"Matrix"}'`（保留 `proxyon` + `claude <args>`）；`~/.claude/settings.json` 无残留 `outputStyle: Matrix`。**前置**：迁移前 matrix 全部规矩已确认并入 `communication-style.md`（内容不丢）。
- [ ] AC6: 记忆掏薄壳（本机迁移）——`style-concise` / `style-plain-language` / `discussion-mode-no-forced-menus` 三文件的**规矩正文删除**、只留「哪天因为什么事定的」来龙去脉 + 一句「规矩正文见 `communication-style.md`」；`MEMORY.md` 索引三行同步改为薄壳描述；`style-plain-language` 里指向 butler 内部 MILE-0003 的引用**原样保留**。
- [ ] AC7: 边界与迁移如实——`migrations/v2.6.0.md` 写清：对目标项目 `.ai/` 部署面 `[no-op]`+`[restamp]`；一个**机器级动作**「重跑 `./scripts/setup.sh` 装上 @import」；以及本机一次性手动清理（删 matrix.md / 拆 claudep 参数 / 掏薄壳记忆）如实列为可选手动步。不夸大不隐瞒。
- [ ] AC8: 收口 + 切版一致性——四件套说人话、收口五步齐（归档 / 交付 .md+.html / 台账 closed·current:none / 折叠产物 / 6 不变量自检）；v2.6.0 三处版本载体对齐（`VERSION` == tag `v2.6.0` == `CHANGELOG` 顶条 `## [2.6.0]`）；迭代 feat 提交与 chore(release) 提交分离。

# Verification Method
- AC1: 读 `communication-style.md` 核各节齐、说人话 4 条各带 ❌/✅、别抛菜单节带 ❌/✅、开篇定位声明在；通读确认无工程/工具规矩混入。
- AC2/AC3: 隔离 HOME 实跑——`env HOME=<tmp> BUTLER via dirname bash scripts/setup.sh`；`awk`/`grep` 从 `<tmp>/.claude/CLAUDE.md` 受管区抽 `@…communication-style.md` 行核**计数=1**；连跑两次再核仍=1；抽出该行的绝对路径 `test -f` 为真。
- AC4: 读 README / HUMAN_GUIDE 改动段核注册句在、措辞说人话。
- AC5: `test ! -e ~/.claude/output-styles/matrix.md`；`grep -c 'outputStyle' ~/.config/fish/config.fish ~/.zshrc` 应为 0（在 claudep 段）；`grep outputStyle ~/.claude/settings.json` 无 Matrix。迁移前 `diff`/核对 matrix 各节均已在正本。
- AC6: 读三记忆文件核规矩正文已删、只剩来龙去脉 + 指向正本；读 `MEMORY.md` 核三索引行已改；核 MILE-0003 引用仍在。
- AC7: 读 `migrations/v2.6.0.md` 核 `[no-op]`+`[restamp]`+机器级重跑 setup 说明 + 本机手动清理清单。
- AC8: 收口后跑 6 不变量自检；切版后 `git tag --points-at HEAD` + 三载体比对；`git show --stat` 核两提交分离。

# Open Questions / Risks
- Claude Code 是否真按 `@` 导入并入全局 CLAUDE.md 的绝对路径：主流机制支持绝对路径/tilde/相对且跟随软链、4 跳内（已查证），AC3 实测「路径正确 + 文件存在」即证装法成立；能否在运行时真读入属运行时行为，非本仓可断言。
- 本机迁移动作跨机器不自动同步：matrix.md 与 claudep 都是本机配置，换机器若有旧的同样设置需同样清一遍；但新机器的沟通风格来源已是同步的正本 + setup 的 @import，本身不依赖 matrix（migration 配方写清）。
- 全局常开会给每个会话加一点 token（正本约 matrix 量级、几百 token）：用户已拍板「带例子换规矩能落地，值」，接受这笔常驻开销。
