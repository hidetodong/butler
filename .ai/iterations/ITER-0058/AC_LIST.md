---
状态: ack-frozen
ACK 日期: 2026-07-18
---

# Goal

让 Butler 的完整验证在干净 macOS/Linux 环境与开发机上可重复执行，并作为 PR/主分支的稳定 CI check；任何绿色结论都不得依赖未固定的工具或用户目录。

# In Scope

- 单一 local/CI 验证入口与 macOS/Linux GitHub Actions 矩阵。
- Python 测试依赖、运行时、Actions 和 validator 来源固定。
- 离线 Markdown 仓内链接/锚点检查及专项测试。
- 稳定 check 名称、最小 CI 权限、超时/并发策略和 required-check 配置说明。
- 用 ITER-0057 evidence runner dogfood 本迭代本地验证与状态审计。

# Out of Scope

- 不代替仓库管理员直接修改 GitHub branch protection/ruleset；未查询远端状态不得写“required check 已启用”。
- 不把外部 URL 在线可达性作为合并门禁，不引入网络抖动型测试。
- 不支持 Windows，不推进可执行升级器 R4 或工作流注册表 R5。
- 不发布新版本、不提交或推送，除非用户后续明确要求。
- 不把 CI artifact 冒充 ITER-0057 定义的仓内 evidence record。

# Acceptance Checklist

- [x] **AC1（单一验证入口）**：仓库提供一条明确的 CI/local 验证命令；GitHub workflow 只调用该入口，不复制测试清单；现有完整双宿主矩阵全部纳入且失败立即返回非零。
- [x] **AC2（双系统 CI）**：GitHub Actions 在 pull request 与 `main` push 上触发，macOS 与 Linux 执行同一必需验证入口；job/check 名稳定可配置为 required check，并设置最小只读权限、并发取消和合理超时。
- [x] **AC3（工具链可复现）**：Python 版本、pytest/PyYAML 等测试依赖与所有 Actions 引用显式固定并有单一锁定来源；CI 和本地入口使用同一依赖集合，不出现 `latest`、无版本 `--with` 或隐式解析当前最新版。
- [x] **AC4（validator 不依赖用户目录）**：plugin manifest 与 8 个 skill 的完整校验在空 HOME/干净 CI 中仍会执行；validator 来源/版本（或 schema 契约）在仓内固定并可审计，缺失时必须失败，不能像当前脚本一样静默跳过。
- [x] **AC5（Markdown 链接门禁）**：提供零网络、确定性的 Markdown 检查，至少校验仓内相对文件、目录和本地 `#fragment`/`path#fragment`；忽略 fenced code、inline code 与外部 URL，失败报告文件、行号和目标；正常仓库与坏目标/坏锚点 fixture 均有测试。
- [x] **AC6（跨平台诚实性）**：macOS/Linux 不使用宽泛 `continue-on-error` 或平台静默跳过；确需差异的步骤有窄条件、原因和专项断言；现有 shell/Python 测试在两平台的 workflow 设计中均被强制调用。
- [x] **AC7（required-check 边界）**：README/HUMAN_GUIDE 给出管理员配置 PR/发布保护的精确 check 名与核验方法；仓内验证只证明“check 已提供”，只有查询远端 ruleset/branch protection 得到证据后才能声称“required 已启用”，否则明确标记 pending external configuration。
- [x] **AC8（证据与非回归）**：链接检查、validator/空 HOME 专项、完整 CI/local 入口、`git diff --check` 和 `audit-project-state.py --allow-unreleased` 均由本迭代机器 record 捕获并校验；P5 逐 AC 引用 passed evidence，失败首跑保留且不得覆盖假绿。

# Verification Method

- AC1–2：静态检查 workflow 触发/权限/job/矩阵，并在本地运行 workflow 调用的唯一入口；必要时用 YAML 解析测试防键名误写。
- AC3–4：在隔离 HOME 和仅使用仓库锁定文件的环境运行完整入口，断言 validator 缺失/篡改会失败、依赖版本与锁定源一致。
- AC5：对真实仓库与临时 Markdown fixture 运行链接检查器，覆盖文件、目录、Unicode/重复标题锚点、坏路径、坏 fragment、code 和外链忽略。
- AC6：检查 workflow 无宽泛放行，并让两个 OS matrix 都指向相同入口；真实 GitHub 双系统结果若本轮不可查询，必须作为未验证风险保留，不能由本地 macOS 代替。
- AC7：核对文档中的稳定 check 名与 workflow 一致；只有远端 API/设置证据存在时才勾选“已启用”子结论。
- AC8：用 evidence runner 捕获专项与完整矩阵，校验 hot/archive 单真源和 record hash，再运行状态 auditor。

# Open Questions / Risks

- GitHub-hosted runner 与 Actions revision 会更新；P3 要固定到明确版本/SHA，并设计受控升级方式，避免“固定后永不更新”的供应链债。
- 本地当前是 macOS，真实 Linux 结果只能由 CI 或容器提供；没有远端 run 证据时 P5 必须诚实区分“workflow 配置已验证”和“Linux 已实际运行”。
- 仓库既有 Markdown 可能包含历史坏锚点；实现时应修真实链接或建立窄而有理由的排除，不得全局忽略目录来换绿。
