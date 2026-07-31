<!-- butler-artifact-template: 1.0.0 artifact=tech_plan -->
# TECH_PLAN — ITER-0098

方案状态: pass

方案审查日期: 2026-07-31
方案审查方式: user-ack

## Design Decisions

**Goal**：支撑 AC1–AC7，用四个公开入口文件补齐 Butler 的授权、首次使用、贡献和安全报告闭环，不改变 Butler 本身的运行行为。

**Files / Modules to Change**

| 文件 | 改动性质 | 服务 AC |
|---|---|---|
| `LICENSE` | 新增 Apache License 2.0 标准全文 | AC1 |
| `CONTRIBUTING.md` | 新增 Issue/PR、本地准备、改动边界和验证要求 | AC2、AC7 |
| `SECURITY.md` | 新增支持版本、私密报告与协调披露策略 | AC3、AC7 |
| `README.md` | 重整顶部、目录、快速开始、最小示例及社区入口 | AC1–AC7 |

不动：`HUMAN_GUIDE.md` 正文、`scripts/setup.sh`、`Coder/` 规则算法、`templates/`、`plugins/`、`tools/`、`migrations/`、GitHub 仓库设置和历史归档。

**Interface / Contract**

- 公开仓库地址统一使用 `https://github.com/hidetodong/butler`；仓库内文档继续使用相对链接。
- 许可证采用用户已确认的 Apache-2.0 标准文本。README 写 `Apache-2.0 © 2026 hidetodong` 并链接根级 `LICENSE`；第三方子目录许可证保持独立，不扩张或覆盖其条款。
- 贡献策略采用用户已确认的公开 GitHub Issues 与 Pull Requests；普通支持也走 Issues。PR 必须说明动机/影响，并在提交前运行 `bash scripts/verify-ci.sh`。
- 安全问题走 GitHub Private Vulnerability Reporting。文档指向仓库 Security 页面和“Report a vulnerability”入口，同时明确禁止在公开 Issue 披露未修复漏洞；若外部开关尚未启用，交付时必须亮明，不能把文档链接当成设置证据。

**README 信息结构**

1. 标题、短描述和健康状态徽章。
2. 项目定位与解决的问题。
3. 目录。
4. 工作方式与 P1–P5 流程。
5. 快速开始：前置条件 → clone → 安装影响 → 执行 → 生效/验证 → 项目接入。
6. 一分钟最小示例：任务输入 → P2/P3 确认 → `.ai/` 与 `deliveries/` 结果。
7. 现有项目产物、功能清单、三宿主边界、仓库结构与维护验证。
8. 支持与维护、参与贡献、安全、许可证；许可证保持最后一个二级章节。

**State / Boundary**

- README 是新用户入口，不复制 `HUMAN_GUIDE.md` 的详细说明。首次安装所需的信息留在 README，故障排查、完整目录和高级工作流继续下沉。
- `setup.sh` 的主要影响按真实脚本描述：要求 Bash 与 Python 3；修改 shell/Claude 用户配置；检测到 Codex/Pi 时安装相应能力；安装后需要重启终端或重新加载 shell 配置。只陈述现有行为，不修改脚本。
- README 目录覆盖全部 H2；若实施中调整 H2，同步更新目录，避免手写目录漂移。
- 顶部徽章收敛为 CI、版本、许可证、宿主四类；CI 徽章指向 `.github/workflows/ci.yml`，不新增无法由仓库事实支撑的质量承诺。

**Plan Admission**

- **AC Coverage**：AC1 由 LICENSE + README 末节覆盖；AC2 由 CONTRIBUTING + README 入口覆盖；AC3 由 SECURITY + README 摘要覆盖；AC4–AC6 集中落在 README；AC7 由公开入口、链接检查、diff 检查和完整 CI 覆盖。
- **Assumptions**：① `hidetodong` 是许可证版权归属名；② GitHub 公共仓库 `hidetodong/butler` 是对外唯一入口；③ GitHub Private Vulnerability Reporting 已启用或可由仓库管理员在交付前启用。这三项中前两项来自用户 ACK/现有 remote，第三项尚未取得外部设置证据。
- **Alternatives / Trade-offs**：MIT 文本更短，但缺少 Apache-2.0 的明确专利授权；用户已选择 Apache-2.0。把全部安装说明搬进 README 能减少跳转，但会与 `HUMAN_GUIDE.md` 双写；本方案只保留首次成功链路。行为准则和双语入口后置，避免本迭代引入无法兑现的社区执法承诺和翻译同步成本。
- **Failure Modes**：见下节。
- **Impact / Scope Challenge**：四个文件足以闭合本轮目标；新增 GitHub Issue 模板、PR 模板、治理文件或修改外部设置都属于扩张，不在本迭代顺手做。
- **Verification Blind Spots**：离线工具能验证结构、链接和命令，不能证明开源许可证选择已通过公司法务，也不能证明 GitHub 私密漏洞开关已启用。前者由用户 ACK 承担选择责任，后者必须单列外部状态。
- **Verdict**：`pass` — 文件边界、AC 映射和验证路径完整，无已知实现级 Must Fix；用户已于 2026-07-31 ACK 方案及 `© 2026 hidetodong` 版权归属写法，可进入 P4。

**Execution Steps**

- [x] T1 新增 Apache-2.0 根级许可证，保留第三方子目录许可证边界 → AC1
- [x] T2 新增贡献指南，写清 Issue/PR、本地准备、修改规则和完整验证 → AC2
- [x] T3 新增安全策略，写清版本支持、私密报告和协调披露 → AC3
- [x] T4 重构 README 顶部、目录和快速开始，补 clone、依赖、安装影响、验证 → AC4、AC5
- [x] T5 增加一分钟示例与支持/维护、贡献、安全、许可证末节 → AC1、AC2、AC3、AC6、AC7
- [x] T6 对照真实脚本与仓库结构复核文案，运行链接检查、diff 检查和完整 CI，生成 evidence → AC1–AC7

## Failure Paths

- **许可证归属写错**：Apache-2.0 文本正确但 README 版权主体未经确认，会形成错误公开声明。P4 只按本方案写 `© 2026 hidetodong`；若用户在方案 ACK 时纠正，则先改方案再实施。
- **安全入口不可达**：GitHub 私密漏洞开关未启用时，SECURITY 的入口会失效。文档保留设置前提，P5 未取得外部证据则列 Remaining Risk，不宣称闭环已验证；本迭代不越权修改设置。
- **README 与 HUMAN_GUIDE 双写漂移**：快速开始只保留首次成功的最短路径，每个高级主题只给一句摘要和相对链接。
- **目录或徽章漂移**：P5 用 H2 提取结果对账目录，用 `VERSION` 对账版本徽章，并复跑仓库链接检查。
- **安装影响漏写或夸大**：逐段对照 `scripts/setup.sh` 和 `scripts/configure-global-install.py`，只写能从当前实现证明的影响。

## Test Strategy

- **文档结构**：检查四个目标文件存在；提取 README H2 与目录链接逐项对账；许可证章节必须为最后一个 H2。
- **许可证**：把根级 `LICENSE` 与 Apache-2.0 官方标准文本核对；README SPDX 标识为 `Apache-2.0`，第三方许可证路径保持不变。
- **安装链路**：逐条对照 `scripts/setup.sh` 与 `scripts/configure-global-install.py`；核对 clone URL、Bash/Python 3 前置条件、用户级写入、生效与验证命令。
- **链接**：运行 `python3 scripts/check-markdown-links.py --root .`；外部 URL 只检查格式与目标语义，网络可达性不冒充离线验证。
- **仓库质量**：运行 `git diff --check` 和 `bash scripts/verify-ci.sh`；用 verification-evidence 生成 `readme-open-source-readiness` record 覆盖 AC1–AC7。
- **人工走读**：按 README 从“这是什么”走到“安装成功”和“如何贡献/报告安全问题”，记录为弱验证，不冒充自动化证明。
- 本迭代不声明 TDD cycle，`TDD Pair Status` 写 N/A。

## References Compliance

- P2 的四份外部规范只作为结构和社区健康基线；实现不复制其大段原文。Apache-2.0 许可证全文属于必须原样采用的标准法律文本，单独落根级 `LICENSE`。
