<!-- butler-artifact-template: 1.0.0 artifact=concept -->
# CONCEPT — ITER-0127 · 把 Grok CLI 做成正式宿主

## Current Understanding

- Grok 已经能读到本仓库的技能和项目入口，但安装脚本和门禁都不认它。这次把它收成正式宿主：机器上只有 Grok 时也能在别的项目里用 Butler，写文件仍走现有判断，不新写一套规则。
- 已确认：Grok CLI 要成为和 Claude Code、Codex、Pi 并列的正式宿主，不是只在文档里补一句。
- 已确认：现在领一个新迭代开始做这件事。
- 已确认：不新写规则正文，也不为 Grok 再渲染一份规则卡。
- 已确认：安装时把现有技能软链到用户目录的 Grok 技能目录，不另建一套插件市场。
- 已确认：第一版接受 Grok 同时读到 CLAUDE.md 和 AGENTS.md，不改三家共用的入口来消掉重复。
- 已确认：门禁只把 Grok 的 write 和 search_replace 译成现有判断认识的工具名，终端命令仍然不拦截。
- 已确认：CI 不安装 Grok。换一个没有 Butler 技能目录的项目做人测，证明技能能调用，并且一次应该拒绝的写入被拦住。
- 已确认：不移动 v4.0.0 标签，也不推 GitLab。

## Scope

- 安装脚本发现 Grok 时装上机器级技能入口，找不到就跳过，不影响 Claude、Codex、Pi。
- 把 Grok 写文件的工具名接到现有 Python 门禁。
- README、使用指南和兼容说明登记 Grok。
- 用契约测试锁住适配文件，不把 Grok 程序放进 CI。
- 在另一个没有 Butler 技能目录的项目里做人测。

## Open Questions / Risks

- N/A
