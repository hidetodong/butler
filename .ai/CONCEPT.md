<!-- butler-artifact-template: 1.0.0 artifact=concept -->
# CONCEPT — ITER-0098 · 开源就绪：README、许可证与社区协作入口

分流: 完整 | 命中升级信号: 多文件改动、设计取舍 | 2026-07-31

## Current Understanding

- **一句话**：当前 README 已能讲清 Butler 是什么、怎么工作，但仓库还缺少许可证、贡献指南、安全报告渠道和完整的零基础安装路径。本迭代补齐这些开源项目入口，让陌生用户能合法使用、顺利安装，也知道如何求助、贡献和报告漏洞。
- **Goal**：把 Butler 从“公开可读的项目说明”补齐为具备基本授权、使用和协作闭环的开源仓库入口。
- 当前优势保留：价值定位、P1–P5 工作方式、部署后目录结构、能力清单和维护验证入口都已成形，不做推倒重写。
- 当前缺口：根目录没有 Butler 自身 `LICENSE`、`CONTRIBUTING.md` 或 `SECURITY.md`；README 没有目录、完整获取步骤、前置依赖、安装影响、成功验证、贡献/安全/许可证入口。
- 项目形态是 Markdown 规则仓库，附带 Python、Shell 和 TypeScript 驻留工具；未命中现有 Domain / Stack Profile，仅按通用 SOP、文档规范和仓库验证门禁推进。

## Scope

- **In Scope**：新增根级许可证、贡献指南和安全策略；重整 README 的目录、快速开始、安装影响、验证步骤、支持与维护入口、徽章和最小使用示例；保持 `HUMAN_GUIDE.md` 作为详细操作说明，不把其全文搬回 README。
- **Out of Scope**：本迭代不新增 `CODE_OF_CONDUCT.md`，因为是否运营公开社区及其执行责任尚未决定；不做中英文双语 README，避免引入长期同步成本；不修改 Butler 的 P1–P5 规则算法、安装脚本行为、宿主适配或项目部署结构；不代替仓库管理员修改 GitHub 外部设置。
- README 只保留“让人开始使用和参与所必需”的内容，深层维护与架构细节继续通过相对链接下沉。
- 许可证、贡献政策和安全报告渠道是公开承诺，必须由用户确认后冻结，不能由实现者自行猜定。

## Open Questions / Risks

- **许可证**：推荐 Apache-2.0。相较 MIT，它多一层明确的专利授权与终止条款，适合同时包含工具和规则实现的项目；若团队更重视极简授权文本，可改选 MIT。
- **贡献政策**：推荐接受公开 GitHub Issues 和 Pull Requests，并要求提交前运行 `bash scripts/verify-ci.sh`；若仓库只打算公开发布、不接受外部改动，应在 CONTRIBUTING 中明确说明。
- **联系渠道**：推荐普通支持走 GitHub Issues，安全问题走 GitHub Private Vulnerability Reporting，维护者标为 `@hidetodong`。私密漏洞报告入口若尚未启用，需要仓库管理员另行开启，文档不能假称已可用。
- 根目录 `tools/codex-validators/LICENSE` 是第三方快照许可证，不代表 Butler 全仓授权；新增根级许可证时必须避免混淆二者。
