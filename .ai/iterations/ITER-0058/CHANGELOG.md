# 01_CHANGELOG — ITER-0058

> 当前迭代变更热数据；仅记录本迭代实际发生的 ADD / EDIT / DELETE。

## ADD

- `.github/workflows/ci.yml`：PR、main、release tag 的 Ubuntu/macOS 同入口矩阵和稳定 `Butler required checks` 汇总门禁。
- `.python-version`、`pyproject.toml`、`uv.lock`：固定 Python 3.12.12、pytest 8.4.2、PyYAML 6.0.3 及跨平台传递依赖/hash。
- `scripts/verify-ci.sh`：检查 uv 0.9.28、同步 lock 并运行完整矩阵的唯一 local/CI 入口。
- `scripts/check-markdown-links.py`、`scripts/test-check-markdown-links.py`：离线仓内 Markdown 路径/锚点检查和正常/异常 fixture。
- `scripts/test-ci-contract.py`：机械核对 workflow、双 OS、Actions SHA、权限、汇总 check、工具链版本、lock 漂移和错误 uv fail-closed。
- `tools/codex-validators/`：OpenAI Codex 固定 commit 的 plugin/skill 官方 validator 快照、provenance、SHA-256、Apache-2.0 LICENSE 和空 HOME/篡改测试。

## EDIT

- `.ai/CONCEPT.md`、`.ai/AC_LIST.md`、`.ai/TECH_PLAN.md`、`.ai/VERIFY_REPORT.md`：整体覆写为 ITER-0058 工作区四件套。
- `.ai/ITERATIONS.md`、`.ai/MILESTONES.md`、`.ai/MILESTONE.md`、`.ai/task-state.md`、`.ai/02_SESSION_HANDOFF.md`：开启 ITER-0058 并绑定 MILE-0007 R3。
- `scripts/verify-codex-workflows.sh`：validator 来源改为仓内固定快照，缺失/摘要漂移 fail-closed，不再发现/静默跳过用户 HOME 内容。
- `scripts/verify-dual-host.sh`：改用锁定环境中的 Python/pytest，接入 Markdown 和 CI contract 专项，删除临时 `uv --with` 依赖解析与重复 validator 调用。
- `.gitignore`、`AGENTS.md`、`README.md`、`HUMAN_GUIDE.md`、`docs/codex-compatibility.md`：登记锁定环境、唯一验证入口、validator 来源和 `check-provided`/`required-enabled` 边界。
- `scripts/audit-project-state.py`、`scripts/test-audit-project-state.py`：修复多迭代 fold receipt 误报；所有 receipt 校验归档 CHANGELOG，只有最新 receipt 对比当前 topic hash，补历史快照/最新漂移回归。
- `Coder/40_Context_Management/project-digest-schema.md`、`context-persistence.md`：明确旧 topic hash 是折叠时快照，后续迭代合法更新同一 topic 不得让历史 receipt 永久漂移。

## DELETE

- 无。
