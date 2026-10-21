# CI 与可复现验证

> ITER-0058 · MILE-0007 R3 · 用户双 ACK · P5 机器证据与风险复核 · 2026-07-18

## 本次交付目标

把 Butler 的完整本地验证接入可审计的 macOS/Linux CI 合同，并固定运行时、依赖、Actions 与 Codex validators，避免合并质量依赖操作者记得手跑或用户 HOME 恰好装了什么。

## 已完成内容

- 新增 `bash scripts/verify-ci.sh` 唯一 local/CI 入口，固定 Python 3.12.12、uv 0.9.28、pytest/PyYAML 与 `uv.lock`。
- 新增 GitHub Actions：PR、`main`、`v*` tag 触发 Ubuntu/macOS 同一矩阵，Actions 固定完整 SHA，只读权限、并发取消、超时和稳定 `Butler required checks` 汇总。
- 将 OpenAI Codex 官方 plugin/skill validators 按完整 commit 与 SHA-256 快照入仓，保留 provenance 和 Apache-2.0 LICENSE；空 HOME、缺失、篡改和坏 manifest/frontmatter 均 fail-closed。
- 新增零网络 Markdown 检查器：验证仓内相对文件、目录和 GitHub 风格 fragment，跳过 fenced/inline code 与外部 URL；全仓 930 个 Markdown 文件通过。
- README、HUMAN_GUIDE、Codex 兼容文档明确区分 `check-provided` 与远端 `required-enabled`。
- 收口 dogfood 修复多迭代 fold receipt 误报：历史 topic hash 作为折叠时快照保留，只有最新 receipt 与当前知识文件比较；归档 CHANGELOG 仍逐迭代持续校验。

## 关键变更 / 用户可感知变化

开发机与 CI 不再各维护一份测试清单，只需运行 `bash scripts/verify-ci.sh`。插件校验不再依赖 `~/.codex/skills/.system`，该目录缺失也不会静默漏测。GitHub 保护规则只需绑定稳定名称 `Butler required checks`，将来扩展 matrix 不需要改 required 名称。

## 高层影响范围

- CI/工具链：`.github/workflows/ci.yml`、`.python-version`、`pyproject.toml`、`uv.lock`、`scripts/verify-ci.sh`。
- 确定性校验：`tools/codex-validators/`、Markdown checker、CI contract tests。
- 既有矩阵：`verify-codex-workflows.sh`、`verify-dual-host.sh`。
- 人读与宿主入口：README、HUMAN_GUIDE、AGENTS、Codex compatibility 文档。
- 未修改 plugin/marketplace 本体，因此没有 cachebuster/reinstall；未提交、发布或推送。

## 验证方式与结果摘要

- 21 份 evidence record 全部通过摘要/路径校验；其中 20 份 passed，1 份 `remote-required-state` 为如实保留的失败诊断。
- Darwin/arm64 以 Python 3.12.12、uv 0.9.28 完整入口通过：renderer 8、resolver 7、installer 16、evidence 11、auditor 12、Markdown 3、CI contract 5、validator 3、127 hook pytest 和 Codex 三层检查全绿。
- 风险抽样重新执行链接越界、validator 篡改和 CI fail-closed，三个 `review-*` record passed。
- 第一次收口审计发现历史 receipt 永久漂移 Must Fix，退回 active/reopen evidence 后修复，并由 `review-fold-history` reproduced；最终 Must Fix 0、Should Fix 0。
- 未执行 fresh-context 独立复核；主 agent 同上下文审查，不冒称独立。

## 已知剩余风险 / 延后事项

- workflow 尚未提交/推送，真实 GitHub Linux/macOS job 没有运行证据；双系统运行态只能给弱置信，不能宣称远端已跑绿。
- GitHub API 返回 403：当前私有仓库需升级 GitHub Pro 或改公开才能使用 required status checks。该外部变更需要用户授权，本轮不擅自调整套餐或可见性。
- GitHub runner 镜像内部仍会维护更新；固定工具链不等于整台 VM 字节级可复现。
- vendored validators 需按 provenance 中的显式 commit/diff/hash 流程受控更新。

## 引用（只引用，不嵌入）

- `.ai/iterations/ITER-0058/AC_LIST.md`
- `.ai/iterations/ITER-0058/TECH_PLAN.md`
- `.ai/iterations/ITER-0058/VERIFY_REPORT.md`
- `.ai/iterations/ITER-0058/CHANGELOG.md`
- `.ai/iterations/ITER-0058/evidence/`
