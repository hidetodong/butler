<!-- butler-artifact-template: 1.0.0 artifact=tech_plan -->
# TECH_PLAN — ITER-0096

方案状态: pass

方案审查日期: 2026-07-29
方案审查方式: dangerous-self-review

> ⚠️ 危险模式：本方案由模型完成 Plan Admission 后自主 ACK，未经用户确认（ITER-0096，2026-07-29）

## Design Decisions

- 以 `Coder/40_Context_Management/sidework-receipt.md` 为规则单一真源，负责语义、边界、固定章节、生产/消费步骤与失败处理；`templates/sidework-receipt.md` 只保留可复制骨架，不另写第二套算法。
- 回执使用一个 Markdown 文件承载代码与调研混合成果。成果位置表使用 `类型 | 路径 / 提交 / 补丁 | 说明` 固定表头；长内容留在代码、报告或 evidence 真源，回执只写结论和指针。
- `.ai/sidework/` 在第一次写回执时按需创建，不进入基地车部署种子，也不建立索引。文件名优先 `<YYYY-MM-DD>-<slug>.md`；冲突时检查现有文件并追加 `-2`、`-3`，禁止覆盖。
- 旁路执行者是回执生产者，只写自己的工作成果与 `.ai/sidework/<receipt>.md`；不得碰主线四件套、task-state、ITER/MILE 台账或 `02_SESSION_HANDOFF.md`。主 Agent 是消费者，但只有用户给出路径时才读取，不做冷启动扫描。
- 回执不产生任何额外代码写权限。旁路工作的实际修改继续受用户、宿主和 Butler 当前范围约束；范围外代码只能停在研究/补丁建议，或进入用户已授权的隔离分支/工作树，禁止 `BUTLER_BYPASS`。
- 在 `Coder/README.md` 注册规则与触发式读取，在 `HUMAN_GUIDE.md` 增加按需目录和两句可复制用法；不改 rule-card、双宿主入口、workflow registry 或 plugin skill 数量，因为本轮没有新增宿主命令或冷启动强制规则。
- 新增标准库静态检查脚本并接入唯一完整 CI，机械锁定规则 frontmatter、模板 H2/表头、入口和禁止事项。脚本只验证稳定结构，不逐字锁死大段自然语言。
- AC Coverage：AC1→规则定位/职责边界；AC2→固定模板；AC3→生产消费协议；AC4→路径/命名/可信度；AC5→Coder/HUMAN_GUIDE；AC6→专项脚本、CI 与审查，全部有设计落点。
- Assumptions：用户能把回执路径带回主会话；通过人类指南示例验证。目标项目能从 Butler 规则仓读取模板；通过 `$BUTLER_PATH` 指针写法和链接检查验证。无需自动发现即可闭合原始场景；通过 Out of Scope 与用户显式回钩路径锁定。
- Alternatives / Trade-offs：否决复用 session handoff，因为它是主线唯一断点派生视图；否决复用 references，因为它承载项目外部权威资料；否决贡献箱/状态机，因为用户已经授权旁路工作且模型无审批权。独立 `.ai/sidework/` 多一个按需目录，换来职责清楚和互不争写。
- Impact / Scope Challenge：最小可用能力只需一份规则、一份模板、两个入口和一项结构检查；命令、生成器、索引与自动扫描均无真实证据支撑，留在范围外。
- Verification Blind Spots：静态检查能证明结构和接线，不能证明所有模型都一定写出高质量摘要；该质量由规则示例、实际 dogfood 和主 Agent 对账承担，不冒称机器完全覆盖。
- Verdict：pass。AC 全覆盖、失败边界明确、无已知 Must Fix，且未越过协议级 MVP。

## Failure Paths

- 目标项目根未唯一解析、`.ai/sidework/` 或目标文件是符号链接、路径逃出项目根：停止写入并回报，不换路径猜测。
- 目标文件已存在：读取目录后选下一个短序号，新建文件；绝不覆盖既有回执。
- 并发执行者同时选择同名文件：使用 create-only 写入；竞争失败的一方重新读取目录并选择下一短序号，不把失败降级成更新已有文件。
- 回执缺关键章节、成果 locator 不存在或基线已漂移：主 Agent 明确缺口，只消费仍可核实的事实，不把生产者声明升级成已验证结论。
- 旁路成果与当前 AC、方案或代码冲突：主 Agent列出冲突和影响；若涉及方向选择，等待用户决定。不能用模型的“接受/拒绝”状态掩盖冲突。
- 共享脏工作区无法证明作者归属：按低归属强度披露并由主 Agent重验；不得反推或编造 commit 身份。
- 专项结构检查或完整 CI 失败：按 P4 常驻 `correction-contract.md` 修根因并复测，不能删除断言或绕开 CI。危险模式不自动开启 Loop；只有用户显式激活 `/butler:loop` 才使用其标记与定量熔断。

## Test Strategy

- AC1–AC5：运行 `python3 scripts/test-sidework-receipt.py`，核规则 frontmatter、固定章节、模板表头、生产/消费禁止项与两个入口。
- AC5：运行 `python3 scripts/check-markdown-links.py`，证明新增规则和模板链接有效。
- AC6：通过 verification evidence runner 捕获专项、`bash scripts/verify-ci.sh`、`python3 scripts/audit-project-state.py --project-root . --allow-unreleased` 和 `git diff --check`。
- P5 完整审查逐项核实际 diff 的逻辑健壮性、可读性、性能、安全和规则分层；项目 `independent_review=false`，不冒称 fresh-context 独立复核。
- TDD cycle：N/A。核心交付是声明式规则与模板，专项检查与实现同迭代落地，不声明 Red/Green 配对。
- 执行模式校准：用户明确危险模式与 Loop 正交；本迭代 P4 只使用常驻纠错收口契约，不使用 `[Loop #N]` 或五轮熔断。

## References Compliance

- N/A（本迭代无外部参考资料；`.ai/00_IDEATION.md` 是本项目内部构思输入，不属于 `.ai/references/` 外部资料）。
