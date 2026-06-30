# Goal

- 支撑 AC1–AC10：新增 `.ai/PROJECT.md` 常驻项目摘要（状态取向全貌）+ 其格式契约 schema + 冷启动读序接线 + 纳入收口前滚维护 + 部署种子/迁移口径 + butler 自身 dogfood，且不碰四件套字段/AC 脊柱/状态机/hook。

# Files / Modules to Change

- 新增 `Coder/40_Context_Management/project-digest-schema.md` —— `.ai/PROJECT.md` 的格式契约（字段 / 有界 / 指针化 / 维护触发 / 四产物边界）。放 40 而非 20：它与 `handoff-spec.md`、`context-persistence.md` 同属冷启动 / 上下文家族，不是阶段产物（AC1/2/3）。
- 新增 `.ai/PROJECT.md` —— butler 自身全貌摘要种子（真内容，dogfood 验证 schema）（AC8）。
- 改 `Coder/README.md` —— §目录结构 40 下注册新 schema + 文件说明加一行；§读取顺序 / 40 激活说明补"冷启动先读项目 `.ai/PROJECT.md`"（AC4/AC5）。
- 改 `Coder/40_Context_Management/context-persistence.md` —— 冷启动章节补 PROJECT.md 为状态全貌入口 + 读序（PROJECT → ITERATIONS → handoff → 代码）（AC4）。
- 改 `Coder/40_Context_Management/handoff-spec.md` —— §1 定位补：完整 context 的"状态全貌"由 PROJECT.md 承载，handoff 指针可引用它（AC4，边界澄清）。
- 改 `Coder/20_Workflow_Lifecycle/iteration-schema.md` §5.5 + `milestone-schema.md` §7.4 —— 收口加"按需前滚 PROJECT.md"步 + 维护成本声明（AC6）。
- 改 `Coder/20_Workflow_Lifecycle/mcv-deployment.md` —— 部署 `.ai/` 种子清单 + 创建 PROJECT.md 骨架；定已部署项目补建口径（AC7）。
- 评估不改：`templates/rule-card.md`（决策：PROJECT.md 不进强制产物集，不改）；`migrations/`（配方在聚合发布时写，本迭代只定口径）（AC9）。

# Interface / Contract

- **PROJECT.md 字段契约（状态取向，固定 H2 顺序）**：① 目的（这系统是什么 / 给谁解决什么）② 架构与模块地图（主要部分 + 职责 + 指针）③ 关键长期决策与不变量（决策 + 为什么 + 仍成立）④ 现行约束（长期生效的边界 / 纪律）⑤ 已知长期欠债（跨迭代未还的债）⑥ 指针（深内容真源：代码 / deliveries / architecture-overview / 关键 schema）。
- **有界契约**：≤1500 tokens（约 handoff 的 3 倍）；超限压缩措辞或下沉到指针，不删字段。
- **维护契约**：收口时**按需前滚**——多数迭代 0-2 行或不动；overwrite 当前结论、不堆历史（历史归 ITERATIONS / deliveries）。
- **四产物边界契约**：PROJECT=状态积分；ITERATIONS=变更流 delta；02_SESSION_HANDOFF=瞬时断点；MILESTONE=版本范围。schema 写清，无职责重叠。

# State / Boundary

- 本迭代 = R1：只建产物 + 接线 + 纳入收口前滚 + 部署/迁移口径 + dogfood。
- 不做（归 R2 / ITER-0018）：收口执行门禁、冷启动一致性探针、原子收口命令。
- 不做（归 R3 / ITER-0019）：每迭代 changelog 正式化。
- 不碰：四件套字段结构、AC 脊柱、P1-P5 状态机、hook 代码、lifecycle 分流、版本机制。

# Design Decisions

- **Q1 命名 / 落位（定）**：产物 `.ai/PROJECT.md`；schema → `40_Context_Management/project-digest-schema.md`（从 CONCEPT 暂定的 20 改到 40，理由见 Files）。
- **Q2 有界（定）**：≤1500 tokens + 指针化；状态摘要不是百科，深内容指针引用。
- **Q3 不进硬门禁（定）**：PROJECT.md 不进 hook `phase_gate`、不进 rule-card 强制产物集——它是状态摘要不是阶段门禁产物；存在性 / 时效靠收口前滚 + R2 探针兜底。故 rule-card 不改（同时守住本仓"模板单一来源"约束）。
- **Q4 迁移口径（定）**：新部署由 mcv-deployment 建种子；已部署项目补建口径 = 新建 `.ai/PROJECT.md` 种子 + AI 首次据 ITERATIONS/deliveries 回填一次；实际 `migrations/vX.Y.Z.md` 配方在聚合发布时按 `versioning-schema §5` 写。
- **维护成本**：收口前滚"按需"是控成本关键——判据为"本迭代有没有改变某条长期事实（架构/不变量/约束/长期欠债）"，否则不动 PROJECT.md（合 `maintenance-boundaries`）。
- Active profiles：无（Markdown 规则仓）。

# Execution Steps

- [ ] T1 写 `40_Context_Management/project-digest-schema.md`：6 段 H2 字段 + 有界(≤1500t) + 指针化 + 维护触发(收口前滚) + 四产物边界；写作口径指针引用 `artifact-style.md` → AC1/AC2/AC3
- [ ] T2 [P] 改 `Coder/README.md`：§目录结构 40 下加 schema + 文件说明加一行 + §读取顺序/40 补"冷启动先读 PROJECT.md" → AC4/AC5
- [ ] T3 [P] 改 `context-persistence.md` 冷启动章节：PROJECT.md 为状态全貌入口 + 读序 → AC4
- [ ] T4 [P] 改 `handoff-spec.md §1`：状态全貌由 PROJECT.md 承载、handoff 指针引用 → AC4
- [ ] T5 改 `iteration-schema.md §5.5` + `milestone-schema.md §7.4`：收口加"按需前滚 PROJECT.md"步 + 维护成本声明 → AC6
- [ ] T6 改 `mcv-deployment.md`：部署 `.ai/` 种子清单 + 建 PROJECT.md 骨架 + 已部署补建口径 → AC7
- [ ] T7 写 butler 自己的 `.ai/PROJECT.md`（真内容，dogfood）（依赖 T1）→ AC8
- [ ] T8 rule-card 联动裁决：判定不进强制产物集 + 记录理由（rule-card 不改）→ AC9
- [ ] T9 收口前自检：git diff 确认四件套字段/hook/状态机/lifecycle 未碰；本仓五约束 + artifact-style 反面词/嵌套自检 → AC10
- 粒度说明：本迭代多文件、可并行，故展开到任务级；T2–T4 相互独立可并行，T7 依赖 T1，T8/T9 收尾。

# Verification Plan

- 按 `AC_LIST.md` Verification Method 逐项核对；重点：T1 schema 字段/有界/边界完整性（AC1-3）、T7 dogfood `.ai/PROJECT.md` 非空且贴合 butler 现状（AC8）、T9 不变量 git diff（AC10）。

# Risks / Open Questions

- **迁移步型缺口**：`migration-schema` 现有 typed 步（`[rename]`/`[add-field]`/`[regen-claude]`/`[sync-hooks]`/`[restamp]`/`[no-op]`）无"新建文件"型；本迭代只定补建口径，实际配方在聚合发布写时再定是否加 `[add-file]` 步型。
- **与 architecture-overview 重叠**：靠指针化 + 四产物边界契约化解（PROJECT.md 是 AI 维护的状态脊柱，深架构内容指针引用 `architecture-overview`）。
- 无遗留 Must Fix；4 个 P1 开放项已在 Design Decisions 落定。
