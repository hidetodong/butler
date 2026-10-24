---
状态: ack-frozen
ACK 日期: 2026-10-22
---
<!-- butler-artifact-template: 1.0.0 artifact=acceptance -->
# AC_LIST — ITER-0127

## Goal

- 机器上只有 Grok 时，别的项目也能用 Butler。
- 写文件仍走现有判断，不新写一套规则。
- 找不到 Grok 时，原来三家宿主的安装保持原样。

## In Scope

- 安装脚本发现 Grok 时，把 `plugins/butler/skills/` 里的技能软链到 `~/.grok/skills/`。找不到 Grok 就跳过这一支。
- 把门禁接到 Grok 的 `write` 和 `search_replace`。同一路径若用现有的 `Write` 或 `Edit` 会被拒绝，这两个名字也必须被拒绝，而且规则号相同。
- README、使用指南和 `docs/codex-compatibility.md` 写明 Grok 是宿主，并写明软链安装、找不到就跳过、两份入口都会被读到。
- 契约测试锁住安装和门禁。CI 不安装 Grok 程序。
- 在另一个没有 Butler 技能目录的项目里做人测。

## Out of Scope

- 不新写规则算法，不加第三份规则卡，不改入口渲染来消掉双份注入。
- 不做 Grok 插件市场，不照 Pi 再写一套扩展。
- 不拦截 `run_terminal_command` 里的写文件。
- 不移动 `v4.0.0` 标签，不推 GitLab。
- 不处理真实老项目升级、收件箱缺陷和其他候办。

## Acceptance Checklist

- [ ] AC1: 临时 HOME 里，PATH 上有一个名为 `grok` 的可执行文件时，安装脚本把 `plugins/butler/skills/` 下每个技能目录软链进 `$HOME/.grok/skills/`，链到仓库里的原目录，不复制技能正文。再跑一次，软链还在，不产生第二份。PATH 上没有 `grok` 时，不创建这些软链，Claude、Codex、Pi 原有的安装结果不变。测试不改本机真实的 `~/.grok` 和 `~/.codex`。
- [ ] AC2: 用现有门禁读一份标准输入。`tool_name` 为 `write` 或 `search_replace`，`tool_input.file_path` 指向的路径若改成 `Write` 或 `Edit` 会以退出码 2 拒绝，这两个名字也以退出码 2 拒绝，规则号与对应的 `Write` 或 `Edit` 相同。`tool_name` 为 `run_terminal_command` 时仍直接退出码 0，不进入这套写文件判断。
- [ ] AC3: README 的宿主表、使用指南的安装说明、`docs/codex-compatibility.md` 都写了 Grok。三处都写明技能用软链安装、找不到 Grok 就跳过，以及 Grok 会同时读到 `CLAUDE.md` 和 `AGENTS.md`。仓库里没有第三份规则卡模板，入口渲染仍然只维护这两份。
- [ ] AC4: 在本机另建一个没有 `.agents/skills/`、也没有 `.grok/skills/` 的临时项目。安装完成后新开 Grok 会话，能调用一个 Butler 技能。再对一次现有门禁应拒绝的文件写入，文件内容保持拒绝前的字节。这次人测不作为 CI 的一步。
- [ ] AC5: 新增的安装和门禁测试通过。`bash scripts/verify-ci.sh` 退出码 0。CI 日志里没有安装或调用 Grok 程序。

## Verification Method

- AC1: 在临时 HOME 和临时 PATH 下跑安装脚本，检查软链目标和跳过行为。
- AC2: 用临时项目构造两份只差工具名的门禁输入，比对退出码和规则号。
- AC3: 读这三份文档和入口渲染脚本，确认没有新增规则卡模板。
- AC4: 人在本机 Grok 里做。项目先信任钩子，否则门禁不会跑，这次失败不能算产品没拦住。
- AC5: 跑对应测试和 `bash scripts/verify-ci.sh`，并在 CI 脚本里确认没有 Grok 安装步骤。

## External References

- N/A

## Open Questions / Risks

- Grok 会把两份规则卡都读进去，常驻上下文会重复。这是这版接受的代价。
- 项目钩子要先信任该目录才会执行。人测必须在已信任的项目里做。
- 人测依赖这台机器上的 Grok，CI 绿了也不等于 AC4 已经做过。
