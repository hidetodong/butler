<!-- butler-artifact-template: 1.0.0 artifact=verify_report -->
# VERIFY_REPORT — ITER-0127

## Verification Summary

五条验收都有通过证据。安装脚本在发现 Grok 时把技能目录软链到 `~/.grok/skills/`，找不到就跳过。门禁把 `write` 和 `search_replace` 译成现有的 `Write` 和 `Edit`。三份文档写明了 Grok 是宿主。本机另开的会话能从用户技能目录读到 `butler-inbox`，该拒绝的写入没有改掉文件字节。持续集成退出码 0。没有新写规则，也没有第三份规则卡。

## AC Status

- [x] AC1 (auto·可靠): 双宿主脚本在临时家目录里检查了软链、重跑、跳过和真实目录冲突。持续集成把这段跑过，退出码 0。
- [x] AC2 (auto·可靠): `write` 与 `Write`、`search_replace` 与 `Edit` 的退出码都是 2，规则号相同。只有驼峰字段名的一份也相同。`run_terminal_command` 退出码 0。
- [x] AC3 (auto·可靠): README、使用指南和兼容说明都有那句软链安装、找不到就跳过、两份入口都会被读到。渲染器仍然只维护两份入口。
- [x] AC4 (auto·可靠): 临时项目没有自己的技能目录。新会话读了 `~/.grok/skills/butler-inbox/SKILL.md`，并报出用法标识 `workflow:inbox`。`search_replace` 和 `write` 都被阶段门禁拒绝，两份探针文件仍是原来的字节。
- [x] AC5 (auto·可靠): 工具名测试 4 项通过。`bash scripts/verify-ci.sh` 退出码 0。工作流文件和持续集成脚本里没有安装或调用 Grok 程序的步骤。

## 人测道小结

- N/A（本轮无 human·待人 档 AC，人测道不适用）。

## Evidence Index

| Evidence ID | AC | 强度 | Outcome | Record |
|---|---|---|---|---|
| ac-gate | AC2, AC5 | captured | passed | .ai/iterations/ITER-0127/evidence/ac-gate/record.json |
| ac-ci | AC1, AC3, AC5 | captured | passed | .ai/iterations/ITER-0127/evidence/ac-ci/record.json |
| ac-session | AC4 | captured | failed | .ai/iterations/ITER-0127/evidence/ac-session/record.json |
| ac-live | AC4 | captured | passed | .ai/iterations/ITER-0127/evidence/ac-live/record.json |

强度写 captured：这些命令是实现者这次录下来的，没有另请复核者重跑。`ac-session` 失败，不能用来勾 AC4。

## Verification Results

- `ac-gate`：`python -m pytest templates/hooks/tests/test_grok_tool_names.py -q` 退出码 0，4 passed，耗时 0.35 秒。
- `ac-ci`：`bash scripts/verify-ci.sh` 退出码 0，耗时约 42 秒。工具链是 Darwin/arm64、Python 3.12.12、uv 0.9.28。其中钩子 pytest 215 passed，升级器测试 36 项通过。标准错误里有三条 Grok 软链用例的通过行。Pi 扩展的 tsc 缺类型提示是既有的，脚本按既有口径跳过。三条 CRLF 提示也是既有的登录流程备份。
- `ac-session`：同一条人测脚本退出码 1。会话其实已经读到技能文件，核对转录时多要求了冒号后面的一个空格，所以判失败。这不是产品没拦住。
- `ac-live`：修正核对之后重跑，退出码 0。技能从 `~/.grok/skills/butler-inbox/SKILL.md` 读到，模型报出 `workflow:inbox`。新的门禁日志是 `phase_gate | Edit | src/probe.txt` 和 `phase_gate | Write | src/probe-write.txt`。两份文件都还是 `before` 加换行。
- P5 简评没有必须先改的问题。独立复核没开，项目配置里的 `independent_review` 仍是 false。

## TDD Pair Status

- N/A（TECH_PLAN 未声明 TDD cycle）。`check-tdd` 输出 `[N/A] TECH_PLAN 未声明 TDD cycle`，退出码 0。

## Goal Calibration

- 当前无未闭合运行时信号（N/A）。

## Completion Inputs

- Review Verdict: pass
- Completion Blockers: none

## Gate Coverage

- 通用质量门禁：`bash scripts/verify-ci.sh` 退出码 0。收口前再跑项目状态审计。
- Workspace Scope：N/A（本轮 AC 没有 `prd_refs`）。
- Tech Plan Alignment：安装脚本在 Pi 段之后加了软链，找不到 Grok 不创建技能目录，真实目录不删除。门禁只翻译 `write` 和 `search_replace`，终端命令不翻译。钩子仍用项目里的 `.claude/settings.json`，没有第二套 `~/.grok/hooks`。三份文档写了约定的那句话，渲染器没有第三份入口。`VERSION` 没改，`v4.0.0` 没挪。未声明 TDD。
- References Compliance：N/A

## References Compliance

- N/A

## Remaining Risks

- Grok 会把两份规则卡都读进去。这是这版接受的代价，没有测多出来的上下文。
- 项目目录要先信任，钩子才会跑。Claude 钩子兼容如果关掉，项目钩子会被跳过。本轮没有用第二套全局钩子去补。
- 终端命令里的写文件仍然不拦。
- 持续集成里没有真的 Grok 程序。假的可执行文件只证明安装脚本的分支。真会话只在这台机器上做过。
- 本轮不切版、不提交。工作区是脏的，发布标签 `v4.0.0` 不在当前 HEAD。审计会亮未发布，这是预期。
- 本机 `~/.grok/skills` 里已经有这 12 条技能软链。原来的 `ego-browser` 软链还在。自动测试仍然只用临时家目录。

## Handoff / Next Step

- 证据归档并收口 ITER-0127。
- 不提交，不推送，不移动 `v4.0.0`。
