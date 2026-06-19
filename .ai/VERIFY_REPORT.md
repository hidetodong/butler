# Verification Summary
- 覆盖范围：迭代状态枚举固化为封闭三态（active/closed/abandoned）——`iteration-schema §4.2` 封闭声明 + `milestone-schema §5.3` 路线项消歧 + 新增 hook 规则 `ledger_status` 机械拦截台账状态列越界值（如 planned）+ 测试 + 传播。
- 总体结论：AC1–AC16 全部满足；hook 全套 `pytest` 82 passed（含新增 13 例），逐 AC grep 落点通过，AC14 零改动经 `git status` 确认护栏文件未入改动名单。ITER-0008 闭合。

# AC Status
- [x] AC1: `iteration-schema §4.2` 改写为封闭枚举（仅 active/closed/abandoned，含 planned 在内的其他值对迭代行非法）
- [x] AC2: §4.2 交叉引用消歧（planned 属 milestone §5.3 路线项）+ 声明由 hook ledger_status 机械校验
- [x] AC3: `milestone-schema §5.3` 增消歧句（路线项状态 vs 迭代状态、planned 路线项不产生台账行、引 iteration-schema §4.2）
- [x] AC4: 新增 `ledger_status.py`，RULE_ID 正确，仅 target==.ai/ITERATIONS.md 生效、其余 allow，零三方依赖
- [x] AC5: 解析 Write/Edit/MultiEdit 入参，逐行识别 ITER-NNNN 行取第 3 列大小写不敏感比对，越界 deny（reason 含迭代号+原值+枚举，remediation 引 milestone-schema §5.3）
- [x] AC6: 表头/分隔行/空状态/非 ITER 行均 allow（pytest 覆盖）
- [x] AC7: `butler_gate.py` import + RULE_MODULES 接入 ledger_status，deny 后走 lib/bypass、退出码契约不变
- [x] AC8: 新增 `test_ledger_status.py`，覆盖合法三态/planned deny/abandoned/非台账路径/Edit/MultiEdit/表头分隔/空状态/大小写/draft/非 ITER 行/空内容
- [x] AC9: `cd templates/hooks && pytest tests/` = 82 passed（既有 + 新增）
- [x] AC10: hook `README.md` 目录结构 + 运行机制执行顺序补 ledger_status
- [x] AC11: `mcv-deployment §5` hook 拦截能力描述补迭代台账状态枚举越界拦截
- [x] AC12: `Coder/README.md` hook bullet + `rule-card.md` 迭代机制各补封闭三态；`HUMAN_GUIDE.md` 无 hook 概述，按 AC12 不强加
- [x] AC13: hook `VALID_STATES = ("active","closed","abandoned")` 与 §4.2 封闭三态字面一致（机械镜像，注释互指）
- [x] AC14: 零改动护栏——phase_gate/protected_paths/artifact_chain、lib/io·lib/bypass、产物链四 schema、versioning-schema 均不在 `git status` 改动名单
- [x] AC15: 未破坏 CLAUDE.md 五约束（分层未混、产物链未动、hook 规则随 rules/ 整目录分发且行为已在 README/部署/Coder README 登记、模板 SSOT 未手写重复、ledger_status frontmatter N/A 为代码文件、相关 schema frontmatter 未动）
- [x] AC16: ITER-0008 归档 + delivery + 台账 closed（P5 收口环节执行）

# Verification Results
- AC1/AC2：`grep` iteration-schema §4.2 命中"封闭枚举/仅/其他值（含 planned）…非法/ledger_status 机械校验/镜像"。
- AC3：`grep` milestone-schema §5.3 命中"与迭代状态消歧/不产生迭代台账行/ledger_status hook 机械拦截/引 iteration-schema §4.2"。
- AC4-AC8：阅读 `ledger_status.py`（路径门 + _incoming_text 三工具分支 + 逐行 ITER_RE + 第 3 列 lower 比对 + deny 文案）与 `butler_gate.py`（import + RULE_MODULES = [protected_paths, phase_gate, ledger_status, artifact_chain]）；pytest 覆盖 allow/deny 全分支。
- AC9：`pytest tests/ -q` → `82 passed`（两次运行一致）。
- AC10/AC11/AC12：`grep` hook README（2 处）、mcv-deployment §5、Coder README、rule-card 命中各落点。
- AC13：`grep` ledger_status.py `VALID_STATES = ("active", "closed", "abandoned")`，与 §4.2 三态逐字一致。
- AC14：`git status --short` 改动名单 = .ai 四件套+台账、iteration-schema、mcv-deployment、milestone-schema、Coder README、hook README、butler_gate.py、rule-card（改）+ ledger_status.py、test_ledger_status.py（新增）；护栏文件全不在内。

# Gate Coverage
- 通用质量门禁：遵守 CLAUDE.md 五约束——分层未混（改动落 20_ schema + templates/hooks + 文档/模板）、产物链未动、新增 hook 规则随 rules/ 整目录分发（无独立注册项要求，行为已在 README §11/部署 §5/Coder README 登记）、模板 SSOT 未手写重复（rule-card 单写、CLAUDE.md.template 经占位符继承）、相关 schema frontmatter 未动。
- Active Profiles：未命中（Markdown 规则仓库 + Python hook），N/A。
- Tech Plan Alignment：TECH_PLAN 九处改动与五项 Design Decisions 全兑现——机制=hook/schema=契约、专打台账不走 is_gated、逐行+固定列序、复用 bypass、选项 A 不加第四态。
- References Compliance：本轮无 `.ai/references/`，N/A。

# Remaining Risks
- 列序假设：规则依赖 schema 固定列序（状态=第 3 列）。schema 是 hook 执行的契约，改列序须同步规则；pytest 覆盖固定列序。
- 新增 deny 条件是 hook 拦截契约扩展：已部署旧项目升级后多一道拦截——附 BUTLER_BYPASS 兜底，且只拦真正越界值，不影响合法三态。
- butler 仓自身不跑该 hook（hook 仅部署到目标项目）；butler 台账靠规则纪律——与现状一致。
- 本轮未校验 `current:` 指针与里程碑台账状态——列为后续候选。

# Handoff / Next Step
- 任务闭合。收口动作：归档四件套→`.ai/iterations/ITER-0008/`、写 `deliveries/ITER-0008-<slug>.md`、台账置 closed + `current: none`。
- 版本：本轮不发版；ITER-0008 累积到下次切版，预计 MINOR（新增 hook 门禁能力）。临时 venv `/tmp/butler-venv` 仅用于本地跑测，非交付物。
