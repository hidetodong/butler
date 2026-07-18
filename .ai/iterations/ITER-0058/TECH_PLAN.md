# TECH_PLAN — ITER-0058 · CI 与可复现验证

## Goal

- 用一个 `scripts/verify-ci.sh` 同时服务开发机和 GitHub Actions，依赖、validator、运行时和 workflow 引用都有固定真源。
- 让 macOS/Linux、Markdown 链接、Codex plugin/skills 与现有完整矩阵成为稳定 check；对 GitHub 远端 required 状态保持证据边界。

## Files / Modules to Change

- **ADD `.github/workflows/ci.yml`**：PR、`main` push 与 `v*` tag 的双系统矩阵；只读权限、并发取消、超时和稳定汇总 check。
- **ADD `pyproject.toml`、`uv.lock`、`.python-version`**：固定 Python 3.12.12、pytest 8.4.2、PyYAML 6.0.3；`uv.lock` 是跨 macOS/Linux 的依赖真源。
- **ADD `scripts/verify-ci.sh`**：唯一 CI/local 入口，检查 uv 0.9.28，`uv sync --locked` 后调用完整矩阵。
- **ADD `scripts/check-markdown-links.py`、`scripts/test-check-markdown-links.py`**：离线 Markdown 相对目标与 GitHub 风格 fragment 检查及 fixture。
- **ADD `scripts/test-ci-contract.py`**：静态核 workflow 的触发、权限、runner、固定 action SHA、唯一入口、无宽泛放行和稳定 check 名。
- **ADD `tools/codex-validators/`**：OpenAI Codex 官方 `validate_plugin.py` / `quick_validate.py` 固定快照、`PROVENANCE.json`、上游 Apache-2.0 `LICENSE` 与完整性测试。
- **EDIT `scripts/verify-codex-workflows.sh`**：只调用仓内固定 validators；缺文件/摘要错立即失败，不再从 `$HOME/.codex/skills/.system` 发现或静默跳过。
- **EDIT `scripts/verify-dual-host.sh`**：在锁定 venv 中直接用 `python3 -m pytest` 与仓内 validator；纳入链接、CI contract、vendor integrity 专项。
- **EDIT `.gitignore`**：忽略 `.venv/` 与 uv/Python 本地缓存，不忽略锁文件、workflow 或 validators。
- **EDIT `README.md`、`HUMAN_GUIDE.md`、`docs/codex-compatibility.md`**：登记唯一验证命令、双系统 check、固定 validator 来源及 required-check 外部配置边界。
- **EDIT 本迭代 `.ai/` 热数据**：CHANGELOG、task-state、handoff、P5 VERIFY 与 evidence。

## Interface / Contract

### 1. 固定工具链

- Python：`.python-version` 精确为 `3.12.12`；workflow 和本地入口都传同一版本，不使用 `3.12`/`3.x` 浮动范围。
- uv：`scripts/verify-ci.sh` 要求 `uv 0.9.28`；workflow 用固定 SHA 的 `astral-sh/setup-uv` 安装同一版本。
- Python 依赖：`pyproject.toml` 只声明验证所需的 `pytest==8.4.2` 与 `PyYAML==6.0.3`，由 uv 0.9.28 生成并提交 `uv.lock`；执行统一使用 `uv sync --locked` / `uv run --locked`，lock 不一致即失败。
- Actions：全部 `uses:` 固定 40 位 commit SHA并在行尾标注版本：
  - `actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd`（v6.0.2）
  - `astral-sh/setup-uv@08807647e7069bb48b6ef5acd8ec9567f424441b`（v8.1.0），输入 `version: 0.9.28`、`python-version: 3.12.12`。

### 2. 固定 Codex validators

- 从 OpenAI `openai/codex` commit `5c0e582c59892dbec89af78ae62c784d3da6c9cb` 机械快照：
  - `plugin-creator/scripts/validate_plugin.py`，SHA-256 `ebda00d55d7518b127f675f062fb5c6e7a1ffdc0a99df1a55ac594400d7d3228`
  - `skill-creator/scripts/quick_validate.py`，SHA-256 `6cc9dc3199c935916cf6f73fcbbbb0e3bb1b58c8f5109fefa499978908164f51`
- `PROVENANCE.json` 记录仓库、commit、上游路径、内容摘要和更新命令；同目录保留上游 Apache-2.0 LICENSE。
- `test-vendored-validators.py` 先核摘要，再在临时空 HOME 中对 `plugins/butler` 和 8 skills 真跑；删文件、改摘要或 validator 返回非零都使完整入口失败。
- 这是 validator 的固定官方快照，不复制规则算法；将来升级必须显式更新 commit、文件、摘要、锁定测试并单独审查 diff。
- 本迭代不修改 `plugins/butler/` 内容或 marketplace，因此不触发 cachebuster/reinstall；交付前仍通过固定官方 validator 完整校验插件。

### 3. 单一验证入口

调用：

```bash
bash scripts/verify-ci.sh
```

- 入口检查仓根、uv 精确版本和锁文件，运行 `uv sync --locked --python 3.12.12`，再在锁定环境执行 `scripts/verify-dual-host.sh`。
- `verify-dual-host.sh` 是逐项矩阵内核；workflow 只出现上述一条验证命令，不能另抄 pytest/validator/link 命令。
- 内核使用 venv PATH 中的 `python3`；删除现有 `uv run --with ...`，避免子命令重新解析依赖。
- 所有脚本 `set -euo pipefail`，任何专项失败立即非零；不使用 `continue-on-error`。

### 4. Markdown link checker

调用：

```bash
python3 scripts/check-markdown-links.py --root .
```

- 递归扫描仓库 Markdown，排除 `.git/`、`.venv/` 和缓存目录，不排除 `Coder/`、`.ai/iterations/` 或 `deliveries/` 来换绿。
- 跳过 fenced code 与 inline code；识别 inline link/image 的 destination。`http(s)`、`mailto`、协议相对 URL 与纯外部 scheme 只分类跳过，不联网。
- 对相对文件/目录先 URL decode、按来源文档目录解析、拒绝逃出仓根；目标必须存在。
- 对 `#fragment` / `path#fragment` 构造目标 Markdown 的 GitHub 风格 heading slug 集，处理 Unicode、行内格式和重复标题 `-1/-2`；目标非 Markdown 却带 fragment 时失败。
- 诊断格式固定为 `relative/file.md:line: target: reason`，输出按路径/行排序；全部通过输出扫描文件/链接计数。
- fixture 覆盖正常路径、目录、空格/编码、同页/跨页 fragment、Unicode/重复标题、坏目标、坏 fragment、越界、fenced/inline code 与外链忽略。

### 5. GitHub Actions 与稳定 required check

- workflow 名 `Butler CI`，触发 `pull_request`、`push.branches: [main]`、`push.tags: ['v*']`。
- 顶层 `permissions: contents: read`；无 secrets、无写权限；`concurrency` 按 workflow + ref 分组并 `cancel-in-progress: true`。
- matrix job `verify`：runner 精确使用 `ubuntu-24.04` 与 `macos-14`，`fail-fast: false`，每个 leg `timeout-minutes: 30`；两端只 checkout、setup uv/Python、运行 `bash scripts/verify-ci.sh`。
- 汇总 job 的稳定显示名固定为 **`Butler required checks`**，`needs: verify`、`if: always()`；只有全部 matrix success 才 exit 0。管理员只需将该汇总名配置为 branch/ruleset required，未来矩阵扩展不改保护名称。
- `scripts/test-ci-contract.py` 用 PyYAML BaseLoader 解析，避免 YAML 1.1 把 `on` 当布尔值；机械断言触发、权限、两个 runner、完整 SHA、唯一入口、稳定汇总、无 `continue-on-error`。

### 6. required-check 远端边界

- 文档明确分两态：仓内 workflow 交付后是 `check-provided`；GitHub ruleset/branch protection 查到 `Butler required checks` 后才是 `required-enabled`。
- 给管理员的配置步骤包括：先让 workflow 至少跑一次产生 check 名，再在 `main` ruleset/branch protection 中要求 `Butler required checks`，最后从保护设置或 API 复核。
- 本迭代默认只验 `check-provided`。若当前凭据能只读查询远端则保存机器摘要；没有权限/尚未推送时在 VERIFY 标 `pending external configuration`，不阻断仓内代码验收但保留发布治理风险。

## State / Boundary

- CI artifact/log 是 GitHub 运行事实；只有 evidence runner 生成的 record 才进入本迭代 Evidence Index，两者不能互相冒充。
- 本机 macOS 运行只能证明 macOS；Linux 必须引用真实 GitHub run 或其他 Linux 机器 record。没有时 AC2 的“workflow 契约”可机器验证，但 AC6 的“Linux 实跑”保持未验证风险。
- vendored validator 是固定上游快照，不自动追随 Codex；安全收益是可复现，代价是需要显式更新机制和定期审查。
- runner label 固定 OS 大版本但 GitHub 镜像内部仍会维护更新；依赖/Action/validator 固定不等于完整 VM 镜像字节级可复现，文档不得夸大。
- Active Profiles：无。

## Design Decisions

- **用 `uv.lock`，不维护带多平台 wheel hash 的手写 requirements**：一个 lock 同时覆盖两 OS 与传递依赖，入口仍检查 uv/Python 精确版本。代价是首次本地验证要下载固定工具链。
- **vendor 官方 validator 固定快照，不在 CI 运行时 curl**：消除用户 HOME 和网络源分支漂移，并让上游变更可 code review。代价是仓库多约 750 行上游代码，靠 provenance/hash/license 管理。
- **稳定汇总 check，不把两个 matrix 名直接设为保护契约**：管理员只绑定一个名称，矩阵增加时保护不失效；汇总必须 `always()` 且检查 `needs.verify.result`，不能掩盖失败。
- **离线检查本地链接，不探活外链**：相对目标是仓库可决定的事实，外网存活受限流/网络影响，不适合作 required gate。
- **CI workflow 只编排，不复制测试算法**：所有测试清单留在 `verify-dual-host.sh`，避免本地绿、CI 跑另一套。

## Execution Steps

- [x] **T1** 提交 `pyproject.toml`、`.python-version`、`uv.lock`，实现精确工具链检查与单一 `verify-ci.sh` → AC1、AC3
- [x] **T2** 快照官方 validators、许可证/来源/摘要，改 workflow 校验脚本并补空 HOME/篡改测试 → AC4
- [x] **T3** 实现 Markdown link checker 与 fixture，修复真实仓库暴露的坏链接/锚点 → AC5
- [x] **T4** 新增 workflow 与 contract test，锁双 OS、Actions、权限、并发、超时和稳定汇总 check → AC2、AC6、AC7
- [x] **T5** 把专项接入 `verify-dual-host.sh`，删除临时依赖解析，更新 README/HUMAN_GUIDE/Codex 文档 → AC1–AC7
- [x] **T6** 用 evidence runner 捕获专项、完整入口、diff-check、state audit；复核失败样例、链接越界、validator 篡改和汇总失败语义 → AC8
- [x] **T7** 若可用只读凭据，查询 GitHub workflow/ruleset 状态并保存安全摘要；否则明确登记外部 pending，不伪造远端完成 → AC6、AC7

## Verification Plan

- **锁定环境**：故意改 pyproject 不更新 lock、模拟 uv 版本不符、空 HOME 运行入口，分别断言 fail-closed。
- **validators**：对正常 plugin/8 skills 真跑；临时删除 validator、篡改文件、构造坏 manifest/SKILL frontmatter，断言摘要或官方校验非零。
- **Markdown**：运行 fixture 和全仓扫描；诊断精确到行，扫描前后仓库摘要不变。
- **workflow contract**：解析 YAML 并逐项断言触发/权限/runner/action SHA/入口/required 汇总；fixture 改成浮动 tag、单 OS、`continue-on-error` 时测试失败。
- **完整矩阵**：`bash scripts/verify-ci.sh`；确认 renderer/root/setup/evidence/auditor/Codex/hook/link/CI/validator 全部由同一入口覆盖。
- **P5 evidence**：至少捕获 `markdown-tests`、`validator-tests`、`ci-contract-tests`、`ci-local-matrix`、`diff-check`、`state-audit-active`；再对链接越界、validator 篡改、required 汇总失败各抽一条 reproduced。

## Risks / Open Questions

- 上游 validator 固定后会落后于 Codex 新 schema；文档必须给受控更新步骤，后续可由依赖更新任务定期检查，但本轮不引入自动 PR bot。
- 当前工作树叠加尚未提交的 R1/R2；所有 P4 修改必须保留其内容，并由 CHANGELOG 精确区分 ITER-0058 增量。
- GitHub Actions 只有推送后才能真实运行；若本轮不获提交/推送授权，Linux 和远端 required 状态只能留证据缺口，不能用静态 YAML 全勾绿。
- 当前无方案阻塞；等待 P3 ACK 后进入 P4。
