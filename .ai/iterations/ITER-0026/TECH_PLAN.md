# TECH_PLAN — ITER-0026（MILE-0003 R1）

> ⚠️ 危险模式：本产物由模型自主 ACK（已过 `dangerous-engine §5.2` 设计自审门），未经用户确认（ITER-0026，2026-07-05）。

# Goal

- 支撑 AC1–AC8：建帮手名册（总述 + 复核完整定义）、复核三拆、G1/G2 通用规矩单源化、README 注册、两处事实校准。

# Files / Modules to Change

**新增**

- `Coder/62_Extension_Agents/overview.md` — 总述：帮手是什么 + 通用规矩 G1–G4（唯一真源）+ 名册表（三帮手，后两标 R4）+ 触发式加载 + 生态事实校准。→ AC1 / AC3(G1 正文) / AC4(G2 正文) / AC7
- `Coder/62_Extension_Agents/independent-review.md` — 复核完整定义（中立资料：角色 / 输入 / 输出 / 禁止 / 隔离 / 权限 + 触发 / Checker 契约 / 断言核对 / 输出衔接），共享流程回指 60_review。→ AC2 / AC8

**修改**

- `Coder/60_Extension_CodeReview/review-engine.md` — 三拆：①§1 独立性=上下文隔离段、②§6.4 诚实性 fallback 正文 → 上提总述、原地改回指；③§2 独立复核触发 / §3.3 断言核对 / §6.1 隔离形态 / §6.2 Checker 契约 / §6.3 输出衔接 → 搬 independent-review、原地留指针；④§1 审计身份 / §3 流程 / §4 闭环 / §5 简评 → 留原地。**保留 §1–§7 编号骨架**，搬走的小节替换为指针、不 renumber（避免连锁引用失效）。→ AC3 / AC4 / AC8
- `Coder/65_Extension_Dangerous/dangerous-engine.md` §7.3（line 119）— G2 引用"按其 §6.4"改指名册总述。→ AC4
- `Coder/20_Workflow_Lifecycle/verify-schema.md` §4（line 73）— G2 引用"review-engine §6.4"改指名册总述。→ AC4
- `Coder/00_System_Prompt/logic-protocol.md`（line 90）— /review 调度条目末尾加名册指针（轻触，不搬正文）。→ AC4 / AC8
- `Coder/README.md` — 目录结构树加 `62_Extension_Agents/`；目录说明加一段；读取顺序按"触发式加载、不进冷启动必读"处理。→ AC5

# Interface / Contract

- **帮手定义资料标准结构**：角色 / 输入 / 输出 / 禁止 / 隔离 / 权限——三帮手统一遵循，本轮 `independent-review` 立样板。
- **通用规矩 G1–G4 唯一真源在总述**；下游（review / dangerous / verify-schema / logic-protocol）改为引用，不再各写正文。
- **指针格式**：文件名 + 语义锚（如"见 `62_Extension_Agents/overview.md` 通用规矩 G2"），沿用 butler 文件名互引惯例、不写绝对路径。

# State / Boundary

- 落点 `Coder/62_Extension_Agents/`（顶层扩展簇，与 60_review 平级）；不进 `00` 层。
- 夹内文件零数字前缀；总述触发式加载、不进冷启动必读。
- **不改**：`/review` 触发方式与产出行为、P1–P5 状态机、四件套字段、hook、知识文件夹本体、其它无关 §6.4（preference / milestone / versioning / butler-upgrade）。

# Design Decisions

- **DD1（落点 / 形态）**：名册=一个文件夹（overview + 每帮手一文件），照 `agent-doc-design §3`；不放 `00` 层（会话身份 ≠ 能力目录，混入破坏分层）。→ AC1/AC6
- **DD2（G1/G2 单源化）**：G1（独立性=上下文隔离）+ G2（诚实兜底）正文上提总述当唯一真源；review §1/§6.4 原地改回指、dangerous §7.3 + verify-schema §4 引用目标改指总述。带地址搬家、原地留指针。→ AC3/AC4
- **DD3（三拆边界 + 不 renumber）**：共享审查流程（§3 多维 / §4 闭环 / §5 简评）留 60_review（复核本质是"把那套流程放进隔离上下文跑"，流程非其私有）；复核专有搬 independent-review、回指共享流程。**保留 review §编号骨架**，搬走小节替换为指针而非删号，防止跨文件 §引用连锁失效。→ AC3/AC8
- **DD4（logic-protocol 轻触）**：不搬 §90 调度描述（那是 logic-protocol 职责），仅末尾加一句名册指针，避免它成 G1 第二正文。→ AC4/AC8
- **DD5（名册表占位）**：名册表先列全三帮手，"更新说明""查过时"标"R4 落地"，本轮只落 independent-review 完整定义。→ AC1
- **DD6（事实校准）**：AGENTS.md 起源改 Sourcegraph 的 Amp 团队发起、Agent Skills 加"截至 2026 上半年"，落生态说明处、对外措辞按 `agent-doc-design §7`。→ AC7
- **DD7（读取顺序）**：README 读取顺序不新增 62 为冷启动必读；目录说明注明"触发式加载"。→ AC5/AC6

# Execution Steps

- [ ] T1 建 `62_Extension_Agents/overview.md`：帮手定义 + G1–G4 + 名册表 + 加载说明 + 生态事实校准 → AC1/AC3/AC4/AC7
- [ ] T2 建 `62_Extension_Agents/independent-review.md`：复核中立定义 + 专有契约，共享流程回指 60_review（依赖 T1）→ AC2/AC8
- [ ] T3 改 review-engine 三拆：§1 独立性段 + §6.4 正文上提改回指；§2/§3.3/§6.1/§6.2/§6.3 搬走留指针；§3/§4/§5 留原地；保留 §编号骨架（依赖 T1/T2）→ AC3/AC4/AC8
- [ ] T4 改 dangerous §7.3 + verify-schema §4：G2 引用改指总述，只动这两处（依赖 T1）→ AC4
- [ ] T5 改 logic-protocol §90：末尾加名册指针（依赖 T1）→ AC4/AC8
- [ ] T6 注册 README：目录树 + 目录说明 + 读取顺序（触发式加载）→ AC5
- [ ] T7 grep 全仓自检：review §6.4 的 G2 引用无漏网、G1/G2 正文单源、指针可解析、无误伤无关 §6.4 → AC3/AC4
- [ ] T8 逐条核 frontmatter / 分层 / 功能等价 → AC6/AC8

# Verification Plan

- AC1/2/5: 读文件确认字段齐全、指针解析（确定性可复现）。
- AC3/4: T7 grep——`§6.4` 区分 review vs 无关；独立性 / 上下文隔离仅总述有正文、review 回指；两处 G2 下游引用已改指总述。
- AC6: 读 frontmatter + 目录层级 + 对照 CLAUDE.md 分层。
- AC7: grep `AGENTS` / `Skills` 措辞已改准。
- AC8: 搬家前后语义逐条对照（P5 独立复核重点核 refute）。
- 全程 P5 升格独立复核（fresh-context 子 agent，验证者≠实现者）。

# Risks / Open Questions

- **误伤风险**：全仓多个无关 §6.4——改 G2 引用只动 dangerous:119、verify-schema:73 两处，T7 grep 兜底。
- **边界风险**：复核专有 vs 共享流程若切不净 → AC3 专项核、独立复核 refute 兜底。
- **renumber 风险**：三拆若删 review §号会连锁——DD3 定"保留骨架、搬走留指针"规避。
- 已定：名册表占位三帮手；总述不进冷启动必读。
