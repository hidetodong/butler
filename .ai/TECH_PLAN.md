<!-- butler-artifact-template: 1.0.0 artifact=tech_plan -->
# TECH_PLAN — ITER-0127

方案状态: pass
方案审查日期: 2026-10-22
方案审查方式: user-ack

## Design Decisions

- 本轮把 Grok CLI 接成和 Claude Code、Codex、Pi 并列的宿主。规则仍只在 `Coder/` 和 `templates/rule-card.md`。不新写规则算法，不为 Grok 再渲染一份规则卡，也不改入口渲染去消掉两份入口的重复。对应已冻结的 AC1 到 AC5。
- 技能只做目录软链。门禁只做工具名翻译，判断仍走现有 Python 规则。找不到 Grok 时这一支跳过，另外三家的安装保持原样。
- 不移动 `v4.0.0`，不改 `VERSION`，不推 GitLab，不处理升级、收件箱和候办。

### 目标

机器上只有 Grok 时，别的项目也能发现 Butler 技能。写文件仍走现有门禁。

### 要改的文件

- `scripts/setup.sh`：Pi 安装段之后加 Grok 技能软链。
- `scripts/verify-dual-host.sh`：在临时家目录里锁住装上、重跑、跳过、改错链和遇到真实目录时停下。文档三句话也放在这个脚本里断言。
- `templates/hooks/butler_gate.py`：入口处把 Grok 的两个写文件工具名译成现有名字。
- `templates/hooks/tests/test_grok_tool_names.py`：新建。比对退出码和规则号。
- `README.md` 的宿主表，以及同一条阅读路径上仍写只有三家宿主的徽章、环境前提和安装条目。
- `HUMAN_GUIDE.md` 第 3 节安装说明。
- `docs/codex-compatibility.md` 的适配层表，加一行 Grok。

不改这些：`scripts/render-project-entrypoints.py` 的产出名单、`templates/rule-card.md`、`scripts/configure-global-install.py`、`templates/hooks/butler_advisor.py`、`VERSION`、迁移配方、`.ai/debt.md`、收件箱、已关闭迭代。

### 接口

安装看 `command -v "${BUTLER_GROK_COMMAND:-grok}"`。验收测试不设置这个变量，只在临时 PATH 上放一个文件名就是 `grok` 的可执行文件。找不到就打印跳过，并且不创建 `$HOME/.grok/skills`。

找到时先 `mkdir -p "$HOME/.grok/skills"`。对 `$BUTLER_DIR/plugins/butler/skills/` 下每个目录，在 `$HOME/.grok/skills/` 下放同名软链，目标是仓库里的绝对路径。已经指向正确目标的软链保持不动。指向别处的软链改到正确目标，不复制技能正文。同名位置如果是真实文件或真实目录，打印错误并以退出码 2 停下，不删除。这里不用 Pi 那段的整目录删除。

门禁在 `butler_gate.py` 的 `main` 里、成员检查之前整理输入。没有 `tool_name` 时用 `toolName`。没有 `tool_input` 时用 `toolInput`。只把 `write` 译成 `Write`，把 `search_replace` 译成 `Edit`，写回后再走现有规则。`run_terminal_command` 不翻译，仍在成员检查处返回 0。不另造一个对应 MultiEdit 的名字。拒绝时打印的规则号来自原来的规则模块，所以和同一路径上的 `Write` 或 `Edit` 相同。

钩子继续用项目部署已经写下的 `.claude/settings.json`。Grok 默认会扫描这份 Claude 钩子配置。本轮不另写 `~/.grok/hooks`，避免同一次写入触发两遍。兼容开关关掉时项目钩子不会跑，这一点留在风险里，不靠第二套全局钩子补上。

三份文档都要写明三件事：技能用软链安装；找不到 Grok 就跳过；Grok 会同时读到 `CLAUDE.md` 和 `AGENTS.md`。使用指南只改第 3 节。兼容说明不改 R5 / ITER-0070 那一行的「进行中」。渲染器继续只维护 `CLAUDE.md` 和 `AGENTS.md`。

### 边界

不做插件市场，不写 Pi 那种扩展，不拦截终端命令里的写文件，不改规则卡，不消掉两份入口。不移动标签，不推 GitLab，不升版本，不跑升级器，不处理收件箱里的旧缺陷和其他候办。测试只用临时家目录，不改本机真实的 `~/.grok` 和 `~/.codex`。写文件之后的提醒脚本这次不动。

### 执行顺序

- [ ] T1 在 `scripts/setup.sh` 的 Pi 段之后加上面的软链分支，结束说明里补一句检测到 Grok 时会做软链 → AC1
- [ ] T2 在 `scripts/verify-dual-host.sh` 用临时家目录补上有 grok、重跑、无 grok、错误软链改目标、真实目录冲突这几路。无 grok 时断言没有 `$HOME/.grok/skills`，另外三家的原有断言仍过 → AC1 AC5
- [ ] T3 在 `templates/hooks/butler_gate.py` 加上面的名字翻译。新建比对测试：同一路径上 `write` 与 `Write`、`search_replace` 与 `Edit` 的退出码和规则号相同；只有驼峰字段名的一份也相同；`run_terminal_command` 退出码 0 → AC2 AC5
- [ ] T4 改 README 宿主表及同一阅读路径上的三家表述、使用指南第 3 节、兼容说明的适配层。在双宿主脚本里断言三处都有那三句话，且渲染器仍只列出两份入口 → AC3 AC5
- [ ] T5 跑新增测试和 `bash scripts/verify-ci.sh`。工作流文件和 `scripts/verify-ci.sh` 里不出现安装或调用 Grok 程序的步骤。人测留到实现之后，不放进 CI → AC4 AC5

### Plan Admission

- **AC Coverage**：AC1 由 T1 和 T2 覆盖。AC2 由 T3 覆盖。AC3 由 T4 覆盖。AC4 只写进人测步骤，实现并确认方案之后在本机另做，不由 CI 代替。AC5 由 T2、T3、T4、T5 覆盖。
- **Assumptions**：Grok 的钩子输入带 `tool_name` 或 `toolName`，文件路径在 `tool_input.file_path` 或 `toolInput.file_path`。项目钩子来自已部署的 `.claude/settings.json`，且 Grok 默认开启 Claude 钩子兼容。技能目录名就是要链过去的名字。验收测试可以用假的 `grok` 可执行文件。
- **Alternatives / Trade-offs**：用目录软链，不用插件市场。接受两份入口都被读到，不新增第三份规则卡，也不改渲染器去消重。复用已经部署的 Claude 钩子，不另写一套扩展，也不另装一份全局钩子。不拦截终端命令。遇到用户已有的真实目录时停下，不整段删除。
- **Failure Modes**：找不到 `grok` 时不创建技能目录。软链目标不对时改到仓库原目录。同名真实文件或目录时退出码 2，原内容还在。未翻译的工具名直接放行。门禁内部异常仍按现有逻辑退出码 2。人测若没先信任项目目录，钩子不跑，这次观察无效。
- **Impact / Scope Challenge**：只改文档不能让别的项目发现技能，门禁也不认识 Grok 的工具名。本轮到软链、名字翻译和三份文档为止。顾问脚本、终端拦截、全局配置脚本，以及这三份文档以外仍写着三家宿主的历史句子，都不顺手改。
- **Verification Blind Spots**：CI 没有 Grok 程序。假可执行文件只能证明安装脚本的分支。真会话能否列出技能、信任之后钩子是否收到 `write`，要等人测。兼容开关关掉时项目钩子会被跳过，本轮看不到。两份规则卡多占的上下文是这版接受的代价，不测 token。
- **Verdict**：pass。用户在 2026-10-22 说「继续吧」。没有必须先改的设计缺陷。

## Failure Paths

- PATH 上没有名为 `grok` 的可执行文件，也没有把 `BUTLER_GROK_COMMAND` 指到别处：打印跳过，不创建 `$HOME/.grok/skills`。Claude、Codex、Pi 该做的仍做。
- 软链已经指向仓库里的原目录：再跑一次保持这一条，不复制出第二份技能正文。
- 软链指向别的路径：改到仓库原目录。
- `$HOME/.grok/skills/<技能名>` 是真实文件或真实目录：退出码 2，不删除。此前已经完成的 Claude、Codex、Pi 安装保留。
- `write` 或 `search_replace` 指向的路径，若改成 `Write` 或 `Edit` 会被拒绝：同样退出码 2，规则号相同，目标文件字节不变。
- `run_terminal_command`，以及任何不在翻译表里的工具名：退出码 0，不进入写文件判断。
- 标准输入不是合法 JSON，或门禁内部抛错：仍按现有门禁退出码 2。
- 项目目录还没被信任，或 Claude 钩子兼容被关掉：Grok 不会执行项目钩子。人测必须先信任，否则不能把这次没拦住记成 AC4 失败。
- CI 环境没有 Grok 程序：不下载、不调用。只有双宿主脚本自己的临时 PATH 里可以放一个名叫 `grok` 的假可执行文件。

## Test Strategy

- AC1：`scripts/verify-dual-host.sh` 继续用它已经隔离的临时家目录。有 `grok` 的一路断言每个技能目录都是软链，链接目标等于仓库原目录，再跑一次仍然只有这一份。没有 `grok` 的一路断言 `$HOME/.grok/skills` 不存在，Claude、Codex、Pi 的原有断言仍过。错误软链会被改到仓库原目录。真实目录冲突时退出码 2，目录还在。这些用例不读写本机真实的 `~/.grok` 和 `~/.codex`。
- AC2：新测试放在 `templates/hooks/tests/test_grok_tool_names.py`，沿用现有 `run_gate`。临时项目的验收未冻结，使现有阶段门禁拒绝源码写入。同一路径分别送 `Write` 与 `write`、`Edit` 与 `search_replace`，退出码都是 2，标准错误里的规则号相同。再送只有 `toolName` 和 `toolInput.file_path` 的一份，结果相同。`run_terminal_command` 退出码 0。
- AC3：读 README 宿主表、使用指南第 3 节、`docs/codex-compatibility.md`。三处都能找到软链安装、找不到就跳过、两份入口都会被读到。`scripts/render-project-entrypoints.py` 的文件名单仍只有 `CLAUDE.md` 和 `AGENTS.md`。这四件事由双宿主脚本里的断言锁住。
- AC4：不放进 CI。方案确认并且实现完成后，在本机另建临时 Git 项目。里面没有 `.agents/skills/`，也没有项目级 `.grok/skills/`。先跑现有安装和基地车部署，让项目带上钩子配置，以及会拒绝源码写入的阶段状态。先信任该目录。新开 Grok 会话，调用 `butler-inbox`，只确认技能能被调用。再准备一份已知字节的文件，让这次写入走 `write` 或 `search_replace`，不走终端命令。拒绝前后字节相同。没先信任导致钩子没跑时，这次人测记为无效。
- AC5：上面的新测试通过，并且 `bash scripts/verify-ci.sh` 退出码 0。`.github/workflows/ci.yml` 和 `scripts/verify-ci.sh` 不包含安装或调用 Grok 程序的步骤。

## References Compliance

- N/A
