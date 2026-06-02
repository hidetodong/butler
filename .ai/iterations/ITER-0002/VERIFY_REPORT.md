# Verification Summary
- 本次验证覆盖范围：新增 `iteration-schema.md`，改 `lifecycle.md` / `mcv-deployment.md` / `delivery-summary.md` / `README.md` / `templates/rule-card.md`，并在 butler 自身 dogfood（台账 + 归档 + 交付）
- 总体验收结论：AC1–AC7 全部满足，迭代闭合，可交付

# AC Status
- [x] AC1: `iteration-schema.md` 已建并在 `README.md` 注册
- [x] AC2: `lifecycle.md` 五处接入迭代语义（P1/P2/§4/P5/§5）
- [x] AC3: `mcv-deployment.md §2` 接入台账 / 工作区标注 / 归档目录按需
- [x] AC4: `delivery-summary.md` 命名与收口三步一致
- [x] AC5: `rule-card.md` 含迭代化需求段，经占位符可透传
- [x] AC6: hook 体系零改动，豁免名单含 `.ai/`、`deliveries/`
- [x] AC7: dogfood 三层落盘一致

# Verification Results
- AC1: `iteration-schema.md` 含 §2 迭代号、§3 三层落盘、§4 台账字段、§5 锁定纪律；`README.md` 目录结构树第 50 行与读取顺序说明列表均已注册
- AC2: `lifecycle.md` P1 段"进入 P1 即开启一个迭代"、P2 强制规则"ACK 即视为冻结"、§4"工作区四件套始终对应当前活跃迭代…快照到 `.ai/iterations/`"、P5"迭代收口三步"、§5"修订 vs 扩张分流"五处命中
- AC3: `mcv-deployment.md §2` 运行态文件列表新增 `ITERATIONS.md`、四件套标题改为"阶段产物 / 当前迭代工作区"、新增"迭代归档（首次收口按需产生）"段
- AC4: `delivery-summary.md §3` 命名改 `deliveries/ITER-NNNN-<slug>.md`、§7 新增"收口三步之一"条、§8.4 引用格式改 `ITER-NNNN`
- AC5: `rule-card.md` 在强制工作流与回退规则之间新增"## 迭代化需求"段；`CLAUDE.md.template` 经 `{{RULE_CARD_CONTENT}}` 占位符自动内联，无需双写
- AC6: `git status --porcelain -- templates/hooks/` 输出为空；`lib/io.py:11-12` 的 `GATED_BLACKLIST` 含 `".ai/"`、`"deliveries/"`，归档与交付路径仍豁免
- AC7: `.ai/iterations/` 下 ITER-0001 / ITER-0002 各含四件套；`.ai/ITERATIONS.md` 两行与归档目录、`deliveries/` 文件一一对应，`current: none` 与两行均 `closed` 一致

# Gate Coverage
- 通用质量门禁：规则仓库无单测门禁，采用 grep + 人工核查 + schema 对齐 + git 状态比对四组手段
- Active Profiles：未命中任何 profile，N/A
- Tech Plan Alignment：TECH_PLAN.md 的 Design Decisions 全部兑现（工作区+归档落盘、ITER-NNNN 编号、允许修订/扩张转迭代纪律、dogfood 端到端、未命中 profile）
- References Compliance：本轮无外部参考资料，N/A

# Remaining Risks
- 台账长期增长后需按 `mcv-update.md` 归档冷行；本迭代仅 2 行，未触发
- 迭代纪律是规则约束而非机制强制（hook 不校验台账一致性）；后续可在 `artifact_chain.py` 占位规则里加台账一致性 linter，但本迭代不做

# Handoff / Next Step
- 本迭代已闭合，无跨会话接力需求
- 后续可选增量：台账一致性 hook linter（ITER-0003 候选）
