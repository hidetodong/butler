# TECH_PLAN — ITER-0057 · 验证证据链与状态审计

## Goal

- 实现“真实执行 → 有界捕获 → 原子封存 → 独立校验 → VERIFY 引用 → 收口归档”的证据链。
- 实现只读状态 auditor，把版本、台账、交付、归档、证据和知识折叠的确定性漂移变成非零退出，而不是依赖模型口头自检。

## Files / Modules to Change

- **ADD `tools/verification-evidence/evidence.py`**：标准库 CLI，提供 `run`、`verify`、`archive`、`reopen` 四个子命令；目标项目按 `$BUTLER` 路径调用，不复制工具副本。
- **ADD `tools/verification-evidence/README.md`**：record schema、退出码、敏感输出、热区/归档与调用契约真源。
- **ADD `tools/verification-evidence/test_evidence.py`**：真实子进程、失败/超时/截断、并发 ID、路径越界、篡改和归档回归。
- **ADD `scripts/audit-project-state.py`**：只读状态审计器；通用项目检查与 Butler 仓特有发布元数据检查分层启用。
- **ADD `scripts/test-audit-project-state.py`**：正常/漂移 fixture，覆盖台账、交付、归档、证据、里程碑、handoff/task-state 指针、知识折叠 receipt 和 Butler 发布元数据。
- **EDIT 证据规则链**：`Coder/30_Quality_Gate/testing-strategy.md`、`Coder/20_Workflow_Lifecycle/verify-schema.md`、`Coder/60_Extension_CodeReview/review-engine.md`、`Coder/62_Extension_Agents/independent-review.md`，固化“无机器证据不打绿”和 reported/captured/reproduced 三级措辞。
- **EDIT 收口/部署/状态链**：`iteration-schema.md`、`mcv-deployment.md`、`context-persistence.md`、`project-digest-schema.md`、`delivery-summary.md`、`dangerous-engine.md`，接入证据热区、归档、状态审计与无人值守同口径。
- **EDIT 高注意力/人读入口**：`templates/rule-card.md`、`README.md`、`HUMAN_GUIDE.md`，注册工具和最小硬纪律。
- **EDIT `scripts/verify-dual-host.sh`**：接入 runner/auditor 单测和本仓 dogfood 校验。

## Interface / Contract

### 1. Evidence runner

调用形态：

```bash
python3 "$BUTLER/tools/verification-evidence/evidence.py" run \
  --project-root "$PROJECT_ROOT" \
  --iteration ITER-NNNN \
  --id unit-tests \
  --ac AC1,AC3 \
  --timeout 900 \
  --max-output-bytes 1048576 \
  -- python3 -m pytest
```

- `--` 后按 argv 直接传给 `subprocess.Popen(..., shell=False)`；不接受拼好的 shell 字符串。
- `--project-root` 必须是已解析的真实项目根；`cwd` 默认项目根，可用 `--cwd <项目内相对路径>`，解析后越界即拒绝。
- evidence ID 只接受 `[a-z0-9][a-z0-9._-]{0,63}`；AC 只接受 `AC[1-9][0-9]*`，至少一个；同一迭代 ID append-only，重复即拒绝，不覆盖历史证据。
- 热区固定为 `<PROJECT_ROOT>/.ai/verification-evidence/`；每项独立目录，避免并发命令争写单一 manifest：

```text
.ai/verification-evidence/
└── unit-tests/
    ├── record.json
    ├── stdout.log
    └── stderr.log
```

- runner 用临时目录写完整 record/log 后以同文件系统原子 rename 发布证据目录；异常清临时目录，不留下半份 record。
- stdout/stderr 分管道持续 drain，分别统计原始字节数、只保存上限内字节并计算保存内容 SHA-256；任一截断则 outcome=`incomplete`，不能作为通过证据。
- record 至少包含：`schema_version`、`evidence_id`、`iteration`、`ac_ids[]`、`command.argv[]`、项目相对 `cwd`、UTC 起止时间、duration、`process_exit_code`、outcome、stdout/stderr 的 path/bytes/captured_bytes/sha256/truncated。
- 不序列化环境变量；调用方只可捕获适合入仓的验证命令。工具不做“猜 token”的不可靠自动脱敏，疑似敏感输出必须换成安全机器摘要或不捕获并记风险。

退出码：

- `0`：子进程 exit 0、日志完整、record 已原子封存。
- `1`：子进程正常结束但非零；失败证据仍封存。
- `2`：参数/schema/路径/重复 ID/启动错误。
- `3`：输出被截断，证据状态 incomplete。
- `124`：超时，杀掉子进程组并封存 timeout 证据。

### 2. Verify 与 archive

- `verify --project-root ... --iteration ... [--source hot|archive]` 只读扫描 record，核对 schema、路径边界、日志存在、captured bytes、SHA-256、outcome 与 process exit；任一漂移退出 1，工具错误退出 2。
- P5 完成捕获并通过 hot verify 后，`archive --iteration ITER-NNNN` 把整个热区原子移动到 `.ai/iterations/ITER-NNNN/evidence/`；目标已存在或迭代号与台账 current 不符时拒绝。
- archive 后立刻对 archive source 再校验；若后续 P5 需要修复重跑，先用显式 `reopen` 子命令把整包原子移回热区并留下审计回声，不允许同时存在两份真源。
- `VERIFY_REPORT.md` 的 `Evidence Index` 只引用最终路径 `.ai/iterations/ITER-NNNN/evidence/<id>/record.json`；交付总结只引用 VERIFY/证据目录，不嵌日志。

### 3. Review evidence strength

- `reported`：只有作者/模型描述或命令文本，没有可校验证据；不能关闭自动道 AC。
- `captured`：reviewer 已运行 `verify` 并核对证据包，但未重跑命令。
- `reproduced`：reviewer 在隔离/适当环境重新执行命令，产生新的 reviewer evidence ID；只有这一档可写“复核者复现”。
- Must Fix / Should Fix 都附文件/行或 evidence ID；风险相关验证至少抽样 `reproduced`，未抽样时在 Remaining Risks 说明，不冒充。

### 4. State auditor

调用形态：

```bash
python3 "$BUTLER/scripts/audit-project-state.py" --project-root "$PROJECT_ROOT"
```

- 只读，不自动修；输出按对象列 `[OK]` / `[DRIFT]`，有任何确定性漂移退出 1，参数/解析错误退出 2。
- 通用检查：current↔active、active 唯一、closed 的日期/交付/四件套/changelog、里程碑路线状态、VERIFY Evidence Index ↔ record、日志摘要、task-state/handoff 的 current 指针、`.ai/project/fold-state.json` receipt。
- `fold-state.json` 只证明“哪个归档 changelog 摘要已折到哪些 topic 文件及其摘要”，不宣称机器理解语义；语义过时仍由 drift review 检查。receipt 由收口动作根据真实文件 hash 生成，auditor 校验路径与摘要。
- Butler 仓特有检查仅在检测到 `VERSION` + `plugins/butler/.codex-plugin/plugin.json` 时启用：VERSION、当前 release tag、plugin version、CHANGELOG 最新版本和 migration 文件一致；未发布工作树允许显式 `--allow-unreleased`，但必须报告为 unreleased 而非 published。
- 新证据口径以归档 VERIFY 含 `Evidence Index` 为启用信号，不追罚 ITER-0056 及更早历史。

## State / Boundary

- 证据 record 是机器执行事实；`VERIFY_REPORT` 是对事实的验收解释。前者不由后者反向生成。
- SHA-256 检测文件漂移，不提供签名或恶意篡改防护；文档统一称“可追溯证据”，不称“可信证明”。
- 日志上限保护仓库体量；截断证据可以用于诊断，但不能关闭 AC。
- 证据热区同一时刻只属于一个 active 迭代；开启新迭代前必须为空。
- auditor 只机械判断确定性事实，不用脆弱关键词猜测 Markdown 语义；不能机械证明的项目知识正确性继续显式留给 drift review。
- R3 才把 runner/auditor 接入 CI；R2 只交付本地确定性命令、规则接线和 dogfood 证据。

## Design Decisions

- **每 evidence ID 一个目录，不用共享可变 manifest**：避免并发测试互相覆盖；VERIFY 的 Index 充当人读聚合，auditor 扫目录做机器聚合。代价是小文件更多，但每项边界独立、归档简单。
- **stdout/stderr 原样有界保存，不做启发式脱敏**：自动脱敏容易漏秘密也会破坏证据；安全边界前移到“只运行适合持久化的验证命令”，并明确不记录环境变量。
- **runner 与 auditor 分离**：runner 记录事实，auditor 校验证据/状态；避免一个工具执行后自行给仓库整体盖章。
- **热区整包移动而非复制**：保证当前态/历史态只有一个证据真源；reopen 也整包回退，不做逐文件合并。
- **知识折叠只机械验 receipt，不伪装语义验证**：hash 能证明哪些输入/输出被登记，无法判断说明写得对不对；后者仍需 drift review。
- Active Profiles：无。

## Execution Steps

- [x] **T1** 固化 record schema、退出码和热区/归档契约，先写 runner 的成功/失败/超时/截断/安全边界测试 → AC1–3
- [x] **T2** 实现 `run/verify/archive/reopen`、原子目录发布、双流有界 drain 与篡改检测 → AC1–3、AC6
- [x] **T3** 修改 testing/VERIFY/review/independent-review 规则，加入 Evidence Index 与三级复核强度 → AC4–5
- [x] **T4** 实现只读 state auditor 与 fold receipt，覆盖通用状态和 Butler 发布元数据 fixture → AC6–7
- [x] **T5** 接入 iteration close、context self-check、deployment、delivery、dangerous 与 rule-card，保证标准/危险模式同守无证据不打绿 → AC4–7
- [x] **T6** 更新 README/HUMAN_GUIDE 与双宿主矩阵，说明证据捕获、敏感输出和未发布状态 → AC8
- [x] **T7** 用 runner dogfood 专项测试和完整矩阵，archive 后再 verify/audit；P5 review 抽样重跑并以 reviewer evidence ID 留证 → AC8

## Verification Plan

- **Runner**：临时项目中分别跑 exit 0/7、超时、stdout/stderr、大输出、非法 cwd/ID/AC、重复 ID、启动失败；逐字段核 record，并检查临时垃圾为零。
- **Verifier**：分别篡改 stdout、stderr、record hash/path/exit/outcome，删除日志，注入绝对路径/`..`，验证对象级报错与只读性。
- **Archive**：hot→archive→verify→reopen→新增 evidence→archive；每一步断言只有一个真源，冲突时零覆盖。
- **Auditor**：每类台账/交付/归档/evidence/fold/release 漂移一个 fixture；正常 fixture 重复运行 stdout/exit 稳定且文件摘要不变。
- **Dogfood**：至少捕获 runner tests、auditor tests、`bash scripts/verify-dual-host.sh`、`git diff --check` 四项；VERIFY 每条自动 AC 引用其中证据。
- **P5 review**：先 verify 全证据，再从安全/归档/状态漂移三类各抽一条重新执行，生成 `review-*` evidence ID，审查结论标 reproduced。

## Risks / Open Questions

- Python 跨平台子进程组终止与双 pipe drain 有差异；实现以 macOS/Linux 为目标，使用线程持续读取并对 timeout 做平台安全降级，R3 再放进双 OS CI。
- evidence archive 发生在最终四件套快照前；若收口后段失败必须 reopen 回 active 热区，规则和测试要锁住单真源，不能留半收口。
- Butler 发布元数据在“迭代已收口但尚未切版”时天然不等于最新 tag；`--allow-unreleased` 必须把该状态亮成 UNRELEASED，不能为了全绿忽略。
- 当前无阻塞问题；方案获 ACK 后进入 P4。
