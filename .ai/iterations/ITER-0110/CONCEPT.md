<!-- butler-artifact-template: 1.0.0 artifact=concept -->
# CONCEPT — ITER-0110 · 最小可执行领域合同与双冲突试点（MILE-0015 R4）

分流: 完整 | 命中升级信号: 多文件改动、契约变更、跨模块影响、设计取舍 | 2026-08-05

## Current Understanding

- **一句话**：把 R1–R3 已经讲清的高风险领域边界变成能自动抓回归的最小合同，并用两个现存冲突证明合同真的能约束实现，而不是再增加一套大而全的术语系统。
- **Goal**：让高风险身份、状态和引用具备唯一所有者和可执行检查；解除 Dangerous Mode 与 Convergence Loop 的模式包含关系，并让 VERIFY 人测段落、桥输入输出和四态路由各归一个真源。
- 当前证据确认 Dangerous Mode 与 Convergence Loop 都属于宿主运行时，但应是并列能力。现状把 Loop 写成 Dangerous 的必然组成，会把“全生命周期无人值守”和“P4 高强度纠错”混成一个模式。
- 为避免解耦后削弱无人值守质量，建议抽取或明确一层共享的“有界 P4 收敛策略”：Dangerous 与 Loop 可以分别复用同一重试、熔断纪律，但激活、状态和用户语义互不包含；普通 P4 仍只走常驻纠错契约。
- 当前证据确认 `tools/artifact-pipeline/artifacts.v1.json` 应独占五件套段落结构，`tools/delivery-selftest/README.md` 独占桥的 manifest/results JSON 与四态机器码，`verify-schema.md` 只解释人测段何时回填以及四态如何影响验收。现状 manifest 缺“人测道小结”，而 verify schema 又自行声明条件结构，需要兼容迁移并补负向 fixture。
- 最小机器合同只登记需要跨模块判断的稳定元信息，例如概念身份、所属上下文、合同种类、唯一所有者和真源指针；状态枚举、桥字段和执行算法继续留在已有 manifest、README、registry 或规则真源，不复制正文。
- 本仓是 Markdown 规则仓，附带 Python、Shell、JavaScript/TypeScript 驻留工具；未命中业务 Domain / Stack Profile，仅按通用 SOP 和现有仓库门禁推进。

## Scope

- **In Scope**：结构化少量高风险身份、状态和引用元信息，校验身份唯一、所有者唯一、真源存在、引用不悬空以及禁止复制执行枚举。
- **In Scope**：把 Dangerous Mode 与 Convergence Loop 改为并列模式；共享 P4 纠错/熔断策略但不共享激活状态，不改变公开入口，不降低无人值守现有安全门。
- **In Scope**：由 artifact manifest 统一拥有 VERIFY 的“人测道小结”结构，由桥 README 继续拥有 JSON 输入输出，由 verify schema / human-test bridge 只消费并解释；为现有 strict 产物提供确定性兼容迁移。
- **In Scope**：补重复所有者、悬空真源、非法类型、旧模式包含措辞、模板/manifest 漂移和人测段迁移的正负 fixture，并接入完整 CI。
- **Out of Scope**：不重做 MILE-0014 的 Decision Map、Decision Work、Decision Promotion 或 Explore Router；领域合同只能引用它们的现有边界。
- **Out of Scope**：不建设完整术语 DSL、知识图谱、全仓领域对象化重构，也不把所有局部状态枚举迁入统一 registry。
- **Out of Scope**：不提前实现 R5 的 review 工作流接线、双宿主投影、升级兼容 dogfood 和效果度量；不吞并状态可信门、多 active iteration 或并行 P4 候办。

## Open Questions / Risks

- **待用户确认的关键建议**：Dangerous 继续保留当前 P4 重试/熔断强度，但通过共享底层策略实现，不再把 Convergence Loop 模式本身视为自动开启。若用户希望 Dangerous 下只有显式 `/butler:loop` 才启用定量熔断，范围和验收需要相应调整。
- **实现落点留到 P3裁决**：优先复用已有检查器和 manifest；只有现有真源无法表达“身份—所有者—指针”关系时才新增独立薄 registry，并且不得复制状态值或算法。
- **兼容风险**：artifact manifest 的严格 H2 顺序会影响已有带 marker 的 live 产物；P3 必须先核现有 migration 机制，不能靠放宽检查或追改全部历史归档解决。
- **验证边界**：本轮能证明静态合同、迁移和工具行为一致，不声称已经获得各宿主运行时的领域读取遥测；该观测仍属于 R5。
