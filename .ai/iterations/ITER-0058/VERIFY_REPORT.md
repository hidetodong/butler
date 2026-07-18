# Verification Summary

- ITER-0058 已实现固定工具链、官方 validator 快照、离线 Markdown 链接门禁、单一 local/CI 入口与 macOS/Linux workflow 合同。
- 本机 Darwin/arm64 在 Python 3.12.12 + uv 0.9.28 锁定环境中完整矩阵通过；真实 GitHub Linux job 尚未运行，不能由本机或静态 YAML 替代。
- GitHub 只读查询证明远端尚无本 workflow；required-status API 返回 403，明确提示当前私有仓库需升级 GitHub Pro 或改为公开仓库才能使用该能力。仓内交付状态因此是 `check-provided locally / pending external capability`，不是 `required-enabled`。
- 第一次收口态 auditor 暴露 R2 fold receipt 多迭代误报：旧迭代 topic hash 被错误要求永久等于当前文件。已退回 active、整包 reopen evidence 并修根因；所有 receipt 持续核归档 CHANGELOG，只有最新 receipt 核当前 topic hash。

# AC Status（道 + 置信档合并标记）

- [x] AC1 (auto·可靠) ✓ `ci-contract-tests` 证明 workflow 只调用单一入口；`ci-local-matrix-platform` 在固定环境完整执行该入口。
- [x] AC2 (auto·弱) ✓ `ci-contract-tests` 机械验证 PR/main/tag、Ubuntu/macOS matrix、权限/并发/超时和稳定汇总 check；未取得 GitHub 双系统真实 run，运行态置信保持弱。
- [x] AC3 (auto·可靠) ✓ `ci-contract-tests` 覆盖 Python/uv/依赖/Action SHA、lock 一致性和错误 uv fail-closed；`ci-local-matrix-platform` 回声实际版本。
- [x] AC4 (auto·可靠) ✓ `validator-tests` 在空 HOME 真跑固定官方 plugin + 8 skills validators，并拒绝缺失、摘要漂移、坏 manifest/frontmatter。
- [x] AC5 (auto·可靠) ✓ `markdown-tests` 覆盖正常/坏路径、锚点、越界、代码块和外链；`markdown-scan` 全仓 930 个 Markdown 文件扫描通过。
- [x] AC6 (auto·弱) ✓ `ci-contract-tests` 证明两个 OS 强制调用同一入口、无 `continue-on-error`；真实 Linux 执行证据缺失，保持弱置信。
- [x] AC7 (auto·可靠) ✓ `ci-contract-tests` 固定 `Butler required checks`，README/HUMAN_GUIDE 记录精确配置/核验法；`remote-workflow-state` 与失败诊断 `remote-required-state` 证明当前远端未启用且能力受套餐/可见性限制。
- [x] AC8 (auto·可靠) ✓ `diff-check`、`state-audit-active`、完整矩阵与三项 `review-*` 均有 passed record；失败的远端 required 诊断保留且不覆盖假绿。

# Evidence Index

| Evidence ID | AC | 强度 | Outcome | Record |
|---|---|---|---|---|
| markdown-tests | AC5, AC8 | captured | passed | `.ai/iterations/ITER-0058/evidence/markdown-tests/record.json` |
| markdown-scan | AC5, AC8 | captured | passed | `.ai/iterations/ITER-0058/evidence/markdown-scan/record.json` |
| validator-tests | AC4, AC8 | captured | passed | `.ai/iterations/ITER-0058/evidence/validator-tests/record.json` |
| ci-contract-tests | AC1, AC2, AC3, AC6, AC7, AC8 | captured | passed | `.ai/iterations/ITER-0058/evidence/ci-contract-tests/record.json` |
| ci-local-matrix | AC1, AC3, AC4, AC5, AC8 | captured | passed | `.ai/iterations/ITER-0058/evidence/ci-local-matrix/record.json` |
| ci-local-matrix-platform | AC1, AC3, AC4, AC5, AC8 | captured | passed | `.ai/iterations/ITER-0058/evidence/ci-local-matrix-platform/record.json` |
| remote-workflow-state | AC2, AC7 | captured | passed | `.ai/iterations/ITER-0058/evidence/remote-workflow-state/record.json` |
| remote-required-state | AC7 | captured | failed (diagnostic) | `.ai/iterations/ITER-0058/evidence/remote-required-state/record.json` |
| review-markdown-boundaries | AC5 | reproduced | passed | `.ai/iterations/ITER-0058/evidence/review-markdown-boundaries/record.json` |
| review-validator-integrity | AC4 | reproduced | passed | `.ai/iterations/ITER-0058/evidence/review-validator-integrity/record.json` |
| review-ci-fail-closed | AC2, AC3, AC6, AC7 | reproduced | passed | `.ai/iterations/ITER-0058/evidence/review-ci-fail-closed/record.json` |
| diff-check | AC8 | captured | passed | `.ai/iterations/ITER-0058/evidence/diff-check/record.json` |
| state-audit-active | AC7, AC8 | captured | passed | `.ai/iterations/ITER-0058/evidence/state-audit-active/record.json` |
| ci-local-matrix-final | AC1, AC3, AC4, AC5, AC8 | captured | passed | `.ai/iterations/ITER-0058/evidence/ci-local-matrix-final/record.json` |
| diff-check-final | AC8 | captured | passed | `.ai/iterations/ITER-0058/evidence/diff-check-final/record.json` |
| state-audit-active-final | AC7, AC8 | captured | passed | `.ai/iterations/ITER-0058/evidence/state-audit-active-final/record.json` |
| auditor-tests-fold-fix | AC7, AC8 | captured | passed | `.ai/iterations/ITER-0058/evidence/auditor-tests-fold-fix/record.json` |
| state-audit-fold-fix | AC7, AC8 | captured | passed | `.ai/iterations/ITER-0058/evidence/state-audit-fold-fix/record.json` |
| review-fold-history | AC7 | reproduced | passed | `.ai/iterations/ITER-0058/evidence/review-fold-history/record.json` |
| ci-local-matrix-after-fold-fix | AC1, AC3, AC4, AC5, AC7, AC8 | captured | passed | `.ai/iterations/ITER-0058/evidence/ci-local-matrix-after-fold-fix/record.json` |
| diff-check-after-fold-fix | AC8 | captured | passed | `.ai/iterations/ITER-0058/evidence/diff-check-after-fold-fix/record.json` |

# Verification Results

- `ci-local-matrix-platform`：Darwin/arm64、Python 3.12.12、uv 0.9.28；renderer 8、root resolver 7、global installer 16、evidence 11、auditor 11、Markdown 3、CI contract 5、vendor validator 3、Codex foundation/workflow/hooks、127 hook pytest 全部通过。
- `markdown-scan`：扫描 930 个 Markdown 文件、34 个真实 Markdown link；外部 URL 不联网，本地目标/fragment 全部存在。
- `validator-tests`：3 组测试通过；官方快照来源固定在 OpenAI Codex commit `5c0e582c59892dbec89af78ae62c784d3da6c9cb`，两个 SHA-256 与 provenance 一致。
- `ci-contract-tests`：5 组测试通过；浮动 Action、单 OS、`continue-on-error`、错误 uv、stale lock 均被拒绝。
- `ci-local-matrix-final`、`diff-check-final`、`state-audit-active-final`：最终完整入口、whitespace 与 active 台账审计均 passed；状态审计明确亮牌 `UNRELEASED`。
- `auditor-tests-fold-fix`：12 项通过；新增多迭代 fixture 证明旧 receipt 的 topic 快照允许被后续合法折叠取代，同时最新 receipt 当前 hash 漂移仍会失败。
- `state-audit-fold-fix` 与 `review-fold-history`：真实 Butler active 状态及定点风险重跑 passed；ITER-0057 显示 `historical-snapshot`，ITER-0058 最新 receipt 保持 current 校验。
- `ci-local-matrix-after-fold-fix`：修复后完整唯一入口再次 passed，未以定点测试替代全仓非回归。
- `remote-workflow-state`：命令成功但列表为空，说明未提交/推送的 workflow 尚未存在于 GitHub 远端。
- `remote-required-state`：失败诊断被完整保留；GitHub API 返回 403，提示需升级 GitHub Pro 或将仓库公开才能启用该私有仓库功能。未把这个失败覆盖或改写成已启用。

# Gate Coverage

- 通用质量门：固定依赖/hash、供应链来源、路径越界、坏 fragment、空 HOME、篡改/缺失、双 OS 合同、只读权限、无持久 checkout 凭据、并发取消、超时、失败汇总和完整双宿主回归均有机器测试。
- Active Profiles：无。
- Tech Plan Alignment：T1–T5 已兑现；T6 正在收尾；T7 已执行只读查询并得到外部能力限制，不擅自升级套餐或公开仓库。
- References Compliance：N/A；本迭代未使用 `.ai/references/` 外部规格。

# Independent Review

- 未执行 fresh-context 独立复核；当前规则不允许未获用户明确要求时启动子 agent。本轮由主 agent 做同上下文风险审查，并将链接越界、validator 篡改和 CI fail-closed 另生成 `review-*` reproduced record。
- `review-markdown-boundaries`、`review-validator-integrity`、`review-ci-fail-closed` 均重跑通过。第一次收口审计新增 1 项 Must Fix（历史 fold receipt 永久漂移）并已由 `review-fold-history` reproduced 关闭；最终 Must Fix 0、Should Fix 0。远端 required 403 是外部能力限制，保留在 Remaining Risks，不归因成代码缺陷。

# Remaining Risks

- workflow 尚未提交/推送，GitHub Linux/macOS job 均无真实 run；AC2/AC6 只按静态合同 + 本机 macOS 给弱置信，不能对外声称“双系统 CI 已跑绿”。
- 当前 GitHub 私有仓库套餐/可见性不支持 required status checks；解决需要用户授权升级套餐或公开仓库，超出本迭代仓内写权限。
- runner label 固定 OS 大版本，但 GitHub 托管镜像内部仍会维护更新；本迭代固定的是 Python、依赖、Actions 和 validators，不是整台 VM 的字节级镜像。
- vendored validators 不会自动跟随 Codex schema；需按 README 的显式 commit/diff/hash 流程受控更新。

# Handoff / Next Step

- 最终重跑完整入口与 diff/state evidence、校验 hot 包；随后归档证据/四件套并收口 ITER-0058，MILE-0007 继续 R4 planned。
