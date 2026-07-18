# CONCEPT — ITER-0057 · 验证证据链与状态审计

> 分流: 完整 | 命中升级信号: 新增驻留工具、修改 P5/收口契约、跨规则与脚本 | 2026-07-18

## 一句话

把“测试通过、复核通过”从模型的一句话，升级为能打开、能校验、能重跑的机器证据；没有证据就不能打绿勾。

## Goal

- G1：为自动测试和代码复核建立机器生成的证据记录，至少包含实际命令、工作目录、时间、退出码、输出文件与摘要校验。
- G2：让 `VERIFY_REPORT.md` 按 AC 引用证据 ID；只写“已运行/已通过”不再构成验收依据。
- G3：让复核区分“作者声称”“已有捕获证据”“复核者重新执行”三种强度，不把前两者冒充独立复现。
- G4：收口时把本迭代证据归档，并由状态审计器检查引用、文件、摘要、台账、交付和项目知识是否一致。
- G5：用 Butler 自身测试 dogfood 新证据链，交付时给出真实证据包而不是再次口头宣称。

## Current Understanding

- 现有 `testing-strategy.md` 和 `verify-schema.md` 已要求“可复现证据”，但允许在 Markdown 里手写命令与“passed”；这仍是模型自述，不证明命令在本轮真的执行过。
- 当前终端输出只存在工具会话里，最终对话会折叠，仓库内没有可复核的退出码、输出和摘要记录。
- 人测道已有 `results.json` 回传证据；缺口主要在自动道及 review 的机器证据链。
- 单纯保存全量终端流水会泄露环境信息、无限膨胀且噪声很大；应只捕获明确的验证命令，限制体量，不记录环境变量值，并把截断/缺失如实标出。
- 摘要校验能发现证据文件漂移，但不是防恶意篡改的签名；R2 解决可追溯与可复跑，不冒充密码学证明。

## Constraints

- 证据必须由 runner 根据真实子进程结果生成，不能让 AI 手填 exit code 冒充机器记录。
- runner 不经 shell 拼接命令，参数以 `--` 后 argv 传入；证据路径限制在当前项目根，不允许目录穿越。
- 只允许持久化适合入仓的验证输出；可能含 token、密钥、用户数据的命令不得直接捕获，需改成安全的机器摘要或显式记为不可归档风险。
- 日志必须有大小上限；发生截断、超时、启动失败或非零退出时，manifest 必须诚实记录，不能仍标通过。
- 不强制历史迭代补证据，不在本轮建立 CI required checks，不把独立复核改成默认强制。

## Impact Scope

- 规则：`testing-strategy.md`、`verify-schema.md`、`review-engine.md`、`iteration-schema.md`、`mcv-deployment.md` 及必要的交叉引用。
- 工具：新增 Butler 驻留的 verification evidence runner 与状态审计脚本/测试。
- 产物：新增当前迭代证据热区和收口归档约定；`VERIFY_REPORT` 增 Evidence Index。
- 文档：README/HUMAN_GUIDE 登记如何捕获、核验和引用证据。
- 非影响：不回写 ITER-0056 归档，不改业务工作流语义，不建设 GitHub Actions（留 R3）。

## Project Type / Active Profiles

- 项目类型：Markdown 规则仓 + Python 标准库工具。
- Active Profiles：无；遵循通用安全、测试和最小实现纪律。

## Open Questions

- P3 需在“每命令一个 manifest”与“迭代级 manifest 索引多个证据项”之间选定单一格式；默认倾向迭代级索引 + 每项独立日志，便于 VERIFY 按 ID 引用。
- P3 需明确证据热区如何在收口时原子归档并清空，避免当前态与历史态双真源。
