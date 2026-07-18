---
状态: ack-frozen
ACK 日期: 2026-07-18
---

# Goal

让测试与复核结论都有机器生成、可校验、可重跑的证据；口头或手写“通过”不能再单独关闭 AC。

# In Scope

- 自动道验证证据 runner、manifest、受控日志与摘要校验。
- `VERIFY_REPORT` 的 Evidence Index 和逐 AC 证据引用硬要求。
- review 对捕获证据、摘要校验和风险抽样重跑的分级裁决。
- 证据热区到迭代归档的收口机制。
- 原定 R2 的版本、台账、归档、交付、handoff、project 知识与证据一致性审计。
- Butler 自身 dogfood、单元测试、异常夹具和人读使用说明。

# Out of Scope

- 不提供防恶意篡改的签名、远程证明或可信执行环境。
- 不回填 ITER-0056 及更早历史迭代的测试证据。
- 不把所有开发命令或完整终端会话录屏/录日志。
- 不捕获可能包含密钥、token 或用户敏感数据的原始输出。
- 不建设 GitHub Actions / required checks；持续验证属于 R3。
- 不强制所有项目开启 fresh-context 独立复核。

# Acceptance Checklist

- [x] **AC1（机器证据而非口述）**：每条自动验证证据由 runner 根据真实子进程生成，记录稳定 evidence ID、argv、项目相对 cwd、开始/结束时间、退出码、状态、关联 AC、stdout/stderr 文件、字节数与 SHA-256；手写“passed”或仅贴命令文本不算证据。
- [x] **AC2（安全且有界的捕获）**：runner 不经 shell 拼接，拒绝项目根外路径和重复/非法 ID；输出原子落盘、有明确大小/超时上限，截断、启动失败、超时和非零退出都进入 manifest，且不记录环境变量值或伪装成功。
- [x] **AC3（证据可独立校验）**：提供只读校验入口，能核对 manifest schema、日志存在性、字节数、SHA-256、退出状态与引用一致性；日志或 manifest 被改、缺失或路径越界时非零退出并指出具体证据项。
- [x] **AC4（VERIFY 强绑定）**：`VERIFY_REPORT.md` 增加必填 `Evidence Index`；每条 `(auto·可靠)` / `(auto·弱)` 的已通过 AC 必须引用至少一个有效 evidence ID 和归档路径，没有证据或只有口头总结时不得勾选。
- [x] **AC5（复核强度诚实）**：P5 review/独立复核必须区分“reported（仅声称）/captured（证据已校验）/reproduced（复核者重跑）”；Must Fix/Should Fix 结论给证据指针，风险相关命令至少抽样重跑，未重跑不得写成独立复现。
- [x] **AC6（证据收口归档）**：当前迭代证据只存在单一热区；收口时随四件套归档到 `.ai/iterations/ITER-NNNN/evidence/` 并清空热区，交付只引用不嵌日志；closed 迭代的新口径证据缺失或摘要不符时状态审计失败。
- [x] **AC7（R2 状态审计）**：新增一条只读审计命令，机械检查版本/tag/plugin manifest/CHANGELOG、迭代与里程碑 current/状态、归档/交付、task-state/handoff、项目知识折叠及本迭代证据引用；漂移时非零退出并给对象级报告，正常仓库重复运行无写入。
- [x] **AC8（dogfood 与非回归）**：用 runner 捕获本迭代的专项测试和完整双宿主矩阵，校验器通过且 `VERIFY_REPORT` 能逐 AC 追到证据；异常/篡改夹具、全仓测试、`git diff --check` 全绿，README/HUMAN_GUIDE 说明“无证据不算通过”和敏感输出边界。

# Verification Method

- AC1–3：隔离临时项目运行真实成功/失败/超时/大输出命令，检查 manifest、日志、exit、hash、原子性及篡改检测。
- AC4–6：构造有/无/坏 evidence ID 的 VERIFY 与收口夹具，验证规则/审计器拒绝假绿并正确归档热区。
- AC5：review fixture 分别覆盖 reported/captured/reproduced，检查措辞与证据指针。
- AC7：对正常仓库快照和逐类漂移 fixture 运行状态审计，验证只读、对象级报错和幂等。
- AC8：使用新 runner 捕获专项测试与 `bash scripts/verify-dual-host.sh`，再运行证据校验、全仓矩阵和 `git diff --check`。

# Open Questions / Risks

- 原始测试日志可能很大或含敏感信息；P3 必须给出默认上限、拒绝/截断语义和“只捕获可入仓命令”的操作边界。
- 仓内 SHA-256 只能证明 manifest 与日志当前一致，不能证明两者没有被一起伪造；规则必须称其为可追溯证据，不夸大成可信远程证明。
- R2 同时承接原定状态审计，影响面较宽；P3 应把证据 runner 与状态 auditor 拆成清晰模块，共享 schema 但不做上帝脚本。
