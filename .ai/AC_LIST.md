# 修订记录
- 无（本迭代需求一次冻结，无迭代内修订）

# Goal
- 让 butler SOP 支持迭代化需求管理：每个迭代有确定迭代号、落对应文档、锁定需求范围，并在 butler 自身验证机制自洽

# In Scope
- 新增 `iteration-schema.md` 作为迭代机制 SSOT（迭代号、台账、三层落盘、锁定纪律）
- `lifecycle.md` 接入迭代开启 / 冻结 / 修订 / 扩张 / 收口
- `mcv-deployment.md` 把 `ITERATIONS.md` 列入运行态文件、`iterations/` 归档目录按需产生
- `delivery-summary.md` 命名带迭代号、收口三步联动
- `README.md` 注册新文件，`rule-card.md` 加精简迭代约束
- dogfood：归档 ITER-0001、bootstrap 台账、收口 ITER-0002

# Out of Scope
- 不修改 hook 体系（工作区固定路径不变）
- 不回溯重命名历史 `deliveries/` 文件
- 不为已存在的历史 deliveries 逐个补迭代号

# Acceptance Checklist
- [ ] AC1: 存在 `iteration-schema.md`，定义迭代号格式、台账字段、三层落盘关系与锁定纪律，并在 `README.md` 目录结构树与读取顺序说明中注册
- [ ] AC2: `lifecycle.md` 在 P1（开启）、P2（ACK 冻结）、P5（收口三步）、§4（工作区/归档关系）、§5（修订 vs 扩张分流）均接入迭代语义
- [ ] AC3: `mcv-deployment.md §2` 把 `ITERATIONS.md` 列入运行态文件、四件套标注当前迭代工作区、`iterations/` 归档目录按需产生
- [ ] AC4: `delivery-summary.md` 命名口径带迭代号、§7 与 §8.4 与收口三步一致
- [ ] AC5: `templates/rule-card.md` 含精简迭代约束，经占位符可透传到 `CLAUDE.md.template`
- [ ] AC6: hook 体系零改动，且 `is_gated` 对 `.ai/iterations/` 与 `deliveries/` 仍为豁免
- [ ] AC7: dogfood 自洽——`.ai/ITERATIONS.md` 台账与 `.ai/iterations/` 归档、`deliveries/` 交付三者一致，`current` 与状态列不矛盾

# Verification Method
- AC1-AC5: 阅读各目标文件，核对新增/修改段落与本清单逐项映射
- AC6: 检查 `templates/hooks/` 无 diff；复核 `lib/io.py` 的 `GATED_BLACKLIST` 含 `.ai/`、`deliveries/`
- AC7: 列出 `.ai/iterations/` 目录树，比对 `ITERATIONS.md` 行与 `deliveries/` 文件存在性

# Open Questions / Risks
- 无未决问题；三项设计决策已拍板
- 风险：工作区四件套固定路径与归档目录并存，若未来想改成纯迭代目录会触发 hook 改造，已在 `iteration-schema.md §3` 显式约束不得改路径
