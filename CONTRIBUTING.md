# 参与贡献

感谢你愿意改进 Butler。这里说明什么适合提交、怎样准备改动，以及合并前必须通过哪些检查。

## 可以贡献什么

- 修正规则、模板或使用文档中的错误、歧义和失效链接。
- 修复安装、升级、验证、Hook、plugin 或驻留工具的问题。
- 为现有行为补充测试、边界检查和可复现样例。
- 提议新的协作流程；涉及多个模块或公开契约时，请先开 Issue 对齐问题和范围。

安全漏洞不要提交公开 Issue，按 [安全策略](SECURITY.md) 私下报告。

## 提交 Issue

提交前请先搜索现有 [Issues](https://github.com/hidetodong/butler/issues)，避免重复。新 Issue 至少说明：

- 你遇到的问题或希望达到的结果。
- 使用的 Butler 版本、宿主（Claude Code、Codex 或 Pi）和操作系统。
- 最小复现步骤、实际结果与预期结果。
- 可公开的日志或截图；提交前删除令牌、内网地址和业务数据。

普通使用问题也可以通过 Issues 提交，并在标题或正文标明这是使用咨询。

## 提交 Pull Request

1. 从 `main` 创建范围单一的分支。
2. 先读根目录 [AGENTS.md](AGENTS.md) 和 [Coder/README.md](Coder/README.md)，按任务涉及的规则定向展开，不要一次改写整套 SOP。
3. 修改规则时守住分层、P1→P5 产物链、模板单一来源和双宿主边界。
4. 为行为变化补充对应测试或验证脚本；纯文档改动至少运行链接检查。
5. 在 Pull Request 中写清动机、改动范围、验证结果和仍未解决的风险。

仓库可能已有维护者正在修改其他文件。请不要顺手格式化或重写无关内容，也不要覆盖别人尚未提交的改动。

## 本地环境

首次安装 Butler 只要求 Git、Bash 和 Python 3，详见 [README 快速开始](README.md#快速开始)。开发和完整验证使用仓库固定工具链：

- `uv 0.9.28`
- `Python 3.12.12`
- 仓库提交的 `uv.lock`

完整验证入口会拒绝不匹配的 `uv` 或 Python 版本，避免本地和 CI 使用不同依赖结果。

## 验证

文档改动先运行：

```bash
python3 scripts/check-markdown-links.py --root .
git diff --check
```

提交 Pull Request 前必须运行与 CI 相同的完整入口：

```bash
bash scripts/verify-ci.sh
```

如果环境限制导致某项无法运行，请在 Pull Request 中明确写出未运行的命令和原因，不要把未执行描述成已通过。

## 提交范围

- 一次 Pull Request 解决一个明确问题。
- 新增规则文件必须在 `Coder/README.md` 的目录结构和读取顺序中注册。
- 强制规则卡以 `templates/rule-card.md` 为唯一来源，宿主模板只保留占位符。
- `CLAUDE.md`、`.claude/**` 服务 Claude Code；`AGENTS.md`、`plugins/butler/**` 服务 Codex；共同算法仍回指 `Coder/`。
- 不提交密钥、令牌、真实业务数据、本机绝对私有路径或未经授权的第三方内容。

## 维护者

当前维护者是 [@hidetodong](https://github.com/hidetodong)。方向性问题可以在 Issue 中先讨论；是否合并仍以项目范围、兼容边界和验证结果为准。
