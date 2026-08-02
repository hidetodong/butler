<!-- butler-artifact-template: 1.0.0 artifact=tech_plan -->
# TECH_PLAN — ITER-0106

方案状态: pass

## Design Decisions

- 采用“扩充现有元数据与契约样本，不新增分类引擎”的最小 Router 接线：
  - `workflows/registry.json` 的唯一 `ideation` workflow 增加显式 Explore 语料，包括 `explore`、`探索`、`Decision Map`、`跨会话决策`、`Wayfinder`；已有 brainstorm / 脑暴 / 未想清 / refine idea 保留。
  - `workflows/router-examples.json` 增加冻结 AC3 六类代表场景和 Standard 建议后同意的 follow-up 场景；每例固定预期 status / primary workflow / 零写边界。
  - `Coder/00_System_Prompt/workflow-router.md` 继续是算法真源，只把“用户原始请求显式表达 Explore”与“Standard 后验建议”写成两个不可混用的 admission 分支，不复制到宿主入口正文。
- 不实现关键词分类器。Router 仍按 registry 的 `semantic_triggers` 与自然语言含义选择唯一 workflow；机器测试只锁住明确触发语料、代表样本、冲突和禁止写集，不能把有限词表冒充通用语义理解。这样可降低显式入口漂移，同时不重新引入“模型给清晰度/大小打分”的脆弱门。
- 宿主边界保持现状：Claude `/butler` 与 Codex `$butler-router` 继续薄读同一 Router/registry；Ideation 的命令/Skill 由 registry 投影更新。Pi 目前只有共享写入门禁而无独立语义 Router，本轮只验证 `plugins/butler-pi/index.ts` 不出现 workflow trigger 表或 Explore 状态写入，不新造 Pi 入口。
- 新增 `tools/explore-dogfood/` 作为内部、非用户 workflow 的可重复场景 harness：
  - `scenario.py` 只编排现有 Decision Map / Work / Promotion 公共 CLI 或引擎边界，不复制三者 schema、validator 或写逻辑；输出一个机器 JSON 观测对象，不作为新状态真源。
  - `tests/` 在临时项目中从 Map 创建、依赖 Frontier、两项 Research sidecar、显式 absorb、fresh-process inspect、live-style promotion 拒绝到隔离 fixture 合法 apply 完成一条端到端链路。
  - `README.md` 说明这是 R5 dogfood/回归 harness，不是 Explore 入口、agent scheduler 或外部 tracker。
- 在 Butler 当前项目中用正式 CLI 建立一张真实 dogfood Map，输入只来自 `.ai/milestone-backlog/codex-structured-question-cards.md`：
  - `DEC-0001`：哪些确认点适合结构化卡片，哪些必须保留文字/HITL；
  - `DEC-0002`：Claude / Codex / Pi 当前可诚实承诺的能力边界；
  - `DEC-0003`：什么证据才足以建设自定义 UI / 外部协调层，依赖前两项；
  - 至少一个 Fog 保存尚未获得的真实使用效率数据。候办仍为 deferred，Map 不创建或提升它的 Milestone/Iteration。
- Decision Work 对 `DEC-0001`、`DEC-0002` 建立同一 Research batch，但因本轮没有用户授权创建子 agent，实际执行采用 `serial`、`fresh_context=false` 并如实回声；结果基于当前仓库一手文件检查。协调器逐项审阅并显式 `absorb_result`，再处理依赖后的 `DEC-0003`。测试只证明可安全并行的结构条件；本轮不伪造真实并行节时收益。
- 跨会话恢复观测使用一个新 Python 进程执行 `decision_map inspect` 与 `decision_work inspect`，不读对话和 CONCEPT。机器报告固定记录：命令数、持久对象数、人工选择动作数、恢复出的 destination / Frontier / work relation / next action，以及无法恢复的语义。
- Promotion dogfood 分两段：
  - live Butler 项目对 resolved `DEC-0003` slice 执行 `iteration-start` 或 `route-reference` plan，预期因 ITER-0106 active / R5 已绑定而确定性拒绝；保存拒绝码和项目树 hash，证明不为演练篡改路线。
  - 临时项目由 harness 建立 active Milestone + planned route，执行一个合法 `route-reference` 的 plan→apply→幂等重放→verify，证明三模块可交接。
- 新增 `docs/explore-dogfood-r5.md` 作为人读 dogfood 结果与架构裁决。固定四个观测章节分别写“口径 / 原始观测 / 结论 / 局限”，再给外部 tracker 单一 verdict：`go | no-go | defer`。原始命令、stdout、hash 和测试日志只进入 verification evidence，文档仅引用 evidence ID，避免复制日志。
- 外部 tracker 的裁决规则预先固定：只有观测到本地文件方案在跨机器协作、多人并发写、可查询通知或长期规模中的实际阻塞，才允许 `go`；只存在理论可能时为 `defer`，本地流程已足够且无近期待办时为 `no-go`。R5 不实现裁决后的后续方向。
- 计划修改范围：
  - Router/registry：`workflows/registry.json`、`workflows/router-examples.json`、`Coder/00_System_Prompt/{workflow-router,logic-protocol}.md`、`scripts/test-workflow-registry.py`，以及 `scripts/sync-workflow-registry.py --write` 生成的 Claude/Codex frontmatter 和 `docs/workflows.md`。
  - Explore 合同与说明：`Coder/50_Extension_Ideation/ideation-engine.md`、`plugins/butler/skills/butler-ideation/SKILL.md` 正文必要的最小 handoff 说明、`README.md`、`Coder/README.md`、`CONTEXT.md`。
  - Dogfood：`tools/explore-dogfood/`、`docs/explore-dogfood-r5.md`、`.ai/decision-maps/DMAP-0001/`、`.ai/decision-work/DMAP-0001/`；promotion 只允许预演/临时 fixture，不在 live 项目留下成功 receipt。
  - CI/项目状态：`scripts/verify-dual-host.sh`、`.ai/01_CHANGELOG.md`、P5 evidence 与收口所需台账/知识文件；不修改 Decision Map / Work / Promotion 的公开 schema，除非实现时发现真实缺陷并回退 P3。

### Plan Admission

- **AC Coverage**：显式 admission 与 trigger corpus→AC1；唯一 registry workflow / 宿主薄适配→AC2；六类 router examples 与零写 hash→AC3；live dogfood 输入与台账 hash→AC4；真实 Map CLI 轨迹→AC5；serial honest-mode Research + absorb→AC6；fresh-process inspect→AC7；live 拒绝 + fixture apply→AC8；固定报告结构→AC9；预声明裁决规则→AC10；既有模块回归/状态审计→AC11；CI、evidence 与里程碑资格检查→AC12。无未映射 AC。
- **Assumptions**：registry 的 `semantic_triggers` 是 Router 当前唯一元数据输入，但实际任意自然语言匹配仍由宿主模型执行；Pi 没有语义 Router，故只验证不复制；当前无子 agent 授权，Research 如实 serial；R5 active 状态会使 live promotion apply 非法。以上均由静态检查或运行前探测验证，不把假设写成成功事实。
- **Alternatives / Trade-offs**：放弃新建确定性关键词 Router，因为有限词表会形成第二算法且无法可靠判断语义；放弃新增 `explore` workflow，因为会制造多入口；放弃只用合成 fixture，因为无法验证真实恢复维护成本；放弃直接建外部 tracker，因为尚无证据。保留一张真实本地 Map 会增加仓内状态，但能验证跨会话恢复，且不污染候办所有权。
- **Failure Modes**：trigger 过宽误路由、Standard 建议被当成原始请求、registry 投影漂移、Pi 被误加路由逻辑、dogfood 直接改候办、Research 模式虚报、result 自动 resolve、fresh-process 依赖对话、live promotion 产生部分写、报告选择性遗漏负面结果、外部 tracker 结论超出证据，均有对应负向测试、hash 对比或 P5 人工复核。
- **Impact / Scope Challenge**：最小产品改动是扩充现有 ideation metadata/规则和测试；`tools/explore-dogfood/` 只为可重复验证，不进入 registry。不开新 workflow、不改三 Decision Module schema、不实现 classifier/tracker，也不提升 dogfood 候办。
- **Verification Blind Spots**：静态 corpus 不能证明所有自然语言都被正确理解；serial Research 不能证明宿主真实并行节时；一次本地仓内 dogfood不能证明多人跨机器规模；Pi 仅能证明没有复制/破坏，不能证明其拥有不存在的交互入口。这些盲区必须进入报告并允许 verdict=`defer`。
- **Verdict**：`pass`；2026-08-02 经用户 ACK，AC1–AC12 均有设计与验证映射，当前无已知 Must Fix，允许进入 P4。

## Failure Paths

- registry 增加未知字段、重复 workflow 或不安全路径：现有 schema/check 拒绝，生成投影不写或事务回滚。
- 原始请求未显式 Explore、仅由 Standard 内部推断：只返回带具体 blocker 的建议，状态树 hash 不变；没有用户同意不得调用 Ideation/Map。
- 显式 Explore 与其他 workflow materially tied：Router 返回 `ambiguous`，只问一个问题，不用 priority 强压。
- dogfood Map/Decision/Attempt ID 已存在或内容冲突：同请求幂等返回；不同 request fail-closed，不删除旧状态或换号绕过。
- Research 不能 fresh-context/parallel：降级 serial 并记录，AC6/AC9 仍可通过；禁止把结构上的可并行性写成实际时间收益。
- Result failed/needs-input/late/stale：保存为参考但不 absorb；报告保留失败或无结论，必要时新 Attempt，不直接改 Map。
- 新进程 inspect 无法恢复 next action：AC7 失败并登记 calibration signal，不能靠阅读本对话补齐后打绿。
- live promotion plan 因 active Iteration/R5 bound 拒绝：这是预期安全结果；若出现任何 receipt/台账/Map 部分写入则 AC8 Must Fix。
- 隔离 fixture apply 出现 pending/incomplete 状态：verify fail-closed，保留测试失败证据；不得自动修复或在 live 项目重试。
- dogfood 暴露现有 Decision Module schema 缺陷：停止 P4、在 task-state 登记并退回 P3；不得顺手扩大成 R2–R4 重构。
- 完整 CI 或状态审计失败：保留失败 evidence，修复后重跑新 record；失败记录不覆盖绿色 AC。

## Test Strategy

- [ ] T1 扩充 ideation 显式 trigger、router examples 与 Router/logic 边界文本，生成投影并建立表驱动负向测试 → AC1、AC2、AC3、AC11。
- [ ] T2 建立 `tools/explore-dogfood/` harness 和临时项目端到端测试，先让场景测试因缺实现失败，再实现最小编排 → AC5、AC6、AC7、AC8。
- [ ] T3 用正式 Decision Map CLI 在 live Butler 创建真实 Map、DAG 与 Fog，并保存 create/add/verify 操作 evidence → AC4、AC5。
- [ ] T4 对两个 Research Decision 执行 claim→prepare→serial local research→record→review→absorb，再解决依赖 Decision；记录实际模式与负面/未知 → AC6、AC9。
- [ ] T5 在新进程完成恢复观测；对 live promotion 保存确定性拒绝与树 hash，并由 harness 完成隔离合法交接 → AC7、AC8、AC11。
- [ ] T6 生成 `docs/explore-dogfood-r5.md`，按固定四项口径回填原始观测/结论/局限并给 tracker verdict；检查候办、台账和最大号未被 dogfood 改动 → AC4、AC9、AC10。
- [ ] T7 更新 Ideation/README/部署说明与项目索引，将 dogfood 测试接入 `verify-dual-host.sh`；不新增 workflow/入口 → AC2、AC11、AC12。
- [ ] T8 运行 Router/registry、Decision Map/Work/Promotion、dogfood harness、三宿主静态边界、Markdown links、artifact/state audit 与完整 `scripts/verify-ci.sh`，用 verification-evidence 保存逐 AC record → AC1–AC12。
- P5 复核重点：Router 是否仍依赖隐性模型判断、harness 是否复制生产 schema、live dogfood 是否污染候办/路线、报告是否夸大 serial/单机结果、tracker verdict 是否由证据支持。

## References Compliance

- 外部参考资料：N/A。本迭代只使用冻结 `.ai/AC_LIST.md`、项目内候办和 Butler 当前代码/规则，不把候办当逐字 PRD。
- 内部真源：`Coder/00_System_Prompt/workflow-router.md`、`workflows/registry.json`、`Coder/50_Extension_Ideation/ideation-engine.md`、`tools/decision-{map,work,promotion}/README.md`。harness 只能调用这些公开边界，不复制其算法。
- Profile：未命中特定语言/前端/构建 profile；实现按通用 SOP、Python 测试和现有 registry/CI 合同推进。
