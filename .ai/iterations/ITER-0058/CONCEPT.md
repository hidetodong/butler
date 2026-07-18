# CONCEPT — ITER-0058 · CI 与可复现验证

> 分流: 完整 | 命中升级信号: 新增 CI、固定验证依赖、跨 macOS/Linux | 2026-07-18

## 一句话

把 Butler 现有的本地验证矩阵变成仓库内可复跑、GitHub PR/主分支自动执行的双系统门禁，并让每个绿色结论都能追到固定工具链和机器证据。

## Goal

- G1：建立单一的仓库验证入口，本地与 CI 调用同一套命令，不维护两份测试清单。
- G2：在 macOS 与 Linux 上运行完整双宿主矩阵，并增加仓内 Markdown 相对链接/锚点检查。
- G3：固定 Python、测试依赖、Actions 与 plugin/skill validator 来源，消除依赖操作者 `$HOME` 当前内容的隐式漂移。
- G4：提供稳定的 PR/主分支 check 名称和 required-check 配置说明；远端保护规则未实际核验时不宣称已经开启。
- G5：CI 失败时保留足够诊断信息；本迭代 P5 继续使用 ITER-0057 的 evidence runner 留下真实机器证据。

## Current Understanding

- `scripts/verify-dual-host.sh` 已覆盖 renderer、项目根解析、全局安装、evidence、状态 auditor、Codex foundation/workflows/hooks 和 hook pytest，是合适的单一验证内核。
- 当前完整矩阵用 `uv run --with pytest` / `--with pyyaml` 临时解析依赖，没有锁文件；不同时间可能取到不同版本。
- `verify-codex-workflows.sh` 会从 `~/.codex/skills/.system/` 发现官方 validator；干净 CI 不具备该用户目录，因此会静默跳过一部分校验，而矩阵末尾又硬依赖本机 `plugin-creator`。
- 仓库没有 `.github/workflows/`，所以 PR、主分支和发布都依赖操作者记得手跑。
- Markdown 中同时有仓内相对链接、锚点、外部文档链接和 badge；R3 应先机械校验可确定的仓内目标，不把网络波动变成合并门禁。
- GitHub branch protection / ruleset 属于远端状态；仓库文件只能提供稳定 check 和配置说明，不能单方面证明 required check 已启用。

## Constraints

- CI 与本地必须复用同一个仓库脚本；workflow 不复制逐项命令。
- Actions、运行时和 Python 依赖必须显式固定；不得使用浮动 `latest` 或依赖用户目录中的 validator 才获得完整覆盖。
- CI 默认只读权限、无 secrets 依赖、有并发取消与超时；PR 中的仓库代码不得获得额外写权限。
- Markdown 检查必须离线、确定性、给出文件/行/目标诊断；外部 URL 只做语法分类，不做联网存活门禁。
- macOS/Linux 必须跑同一必需矩阵；平台差异只能显式建模，不能用静默跳过伪装兼容。
- 本轮不发布、不修改 GitHub 远端保护设置、不推进 R4/R5。

## Impact Scope

- CI：新增 GitHub Actions workflow 与 required-check 操作说明。
- 验证：整理单一 CI/local 入口、固定依赖，消除本机 validator 隐式依赖。
- 工具：新增离线 Markdown 链接检查器及其 fixture 测试；必要时新增仓库自带的固定 validator 契约。
- 文档：README/HUMAN_GUIDE/Codex compatibility 登记本地与 CI 用法、远端 required-check 边界。
- 台账：ITER-0058 四件套、MILE-0007 R3 路线和最终机器 evidence。

## Project Type / Active Profiles

- 项目类型：Markdown 规则仓 + Bash/Python 工具 + GitHub Actions。
- Active Profiles：无；遵循通用安全、测试、依赖固定和最小实现纪律。

## Open Questions

- P3 需选择 validator 固定方式：仓库自带确定性校验器，或从可校验的固定 revision 获取官方 validator；选择标准是干净 CI 可复跑、来源可审计、失败不静默。
- P3 需确定发布触发是否只复用主 workflow，避免 tag/push 同一提交重复跑两套不同门禁。
