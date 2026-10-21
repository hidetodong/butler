# ITER-0008 迭代状态枚举固化：封闭三态 + hook 机械门禁 ledger_status

## 本次交付目标
用户在一个已部署项目的 `.ai/ITERATIONS.md` 台账里发现了 `planned` 状态。核对发现：`iteration-schema §4.2` 定义的迭代状态只有 `active`/`closed`/`abandoned`，**没有 `planned`**——`planned` 是 `milestone-schema §5.3` 拆分路线图「路线项状态」，被误写进了迭代台账。根因是两张表的「状态」列语义串台 + 预先占号。本轮把迭代状态枚举**固化为封闭三态**，并按用户要求**补上机制**（而非只改文档）：新增 hook 规则机械拦截越界值，保证"枚举不会取错"。

## 已完成内容
- **枚举固化（spec/SSOT）**：`iteration-schema §4.2` 从"列举三个值"升级为"**封闭枚举：合法值仅 active/closed/abandoned，其他（含 planned）对迭代行非法**"，并交叉引用消歧 + 声明由 hook 机械校验。
- **里程碑侧消歧**：`milestone-schema §5.3` 写明「路线项状态」是路线项自身命名空间、与迭代行状态不是同一字段；`planned` 路线项「实际 ITER」恒为 `—`、**不产生迭代台账行**，故不应出现在 `.ai/ITERATIONS.md`。
- **机制（hook 规则 ledger_status）**：新增 `templates/hooks/rules/ledger_status.py`——仅当目标为 `.ai/ITERATIONS.md` 时生效，解析待写文本（Write/Edit/MultiEdit），逐行识别 `ITER-NNNN` 行取「状态」列（固定列序第 3 列）大小写不敏感比对，越界非空值 `deny`（含违规迭代号 + 原值 + 合法枚举 + planned 归属提示）。接入 `butler_gate.py` 的 `RULE_MODULES`（`protected_paths → phase_gate → ledger_status → artifact_chain`），deny 后仍走通用 `lib/bypass`（`BUTLER_BYPASS=1` 可显式绕过），退出码契约不变。
- **测试**：新增 `tests/test_ledger_status.py`（13 例：合法三态/planned·draft deny/非台账路径/Edit·MultiEdit/表头分隔/空状态/大小写/非 ITER 行/空内容）；`pytest tests/` 全套 **82 passed**。
- **传播**：hook `README.md`（目录结构 + 执行顺序）、`mcv-deployment §5`（拦截能力描述）、`Coder/README.md`（hook bullet）、`rule-card.md`（迭代机制补封闭三态，SSOT 经占位符传到部署 CLAUDE.md）。

## 关键变更 / 使用者可感知变化
- 迭代状态现在是**封闭三态**，写明白了 `planned` 不属于迭代——它是里程碑路线图的路线项状态。
- 已部署项目里，**往 `.ai/ITERATIONS.md` 写越界状态（如 planned）会被 hook 拦截**（`exit 2`），给出可读提示；坚持要写需显式 `BUTLER_BYPASS=1` + `.ai/bypass-reason.md`。这就是"枚举不会取错"的机制保证。
- 文档与 hook 两处枚举互为镜像、注释互指，不会各自漂移。

## 高层影响范围
- 新增：`templates/hooks/rules/ledger_status.py`、`templates/hooks/tests/test_ledger_status.py`。
- 改：`templates/hooks/butler_gate.py`、`templates/hooks/README.md`、`Coder/20_Workflow_Lifecycle/{iteration-schema,milestone-schema,mcv-deployment}.md`、`Coder/README.md`、`templates/rule-card.md`。
- 不涉及（零改动护栏）：`phase_gate.py`/`protected_paths.py`/`artifact_chain.py`、`lib/io.py`/`lib/bypass.py`、产物链四 schema、`versioning-schema.md`。

## 验证方式与结果摘要
- 逐 AC（AC1–AC16）grep 落点命中各目标文件，全部通过。
- hook 全套 `pytest tests/` = **82 passed**（既有 + 新增 13 例），两次运行一致。
- AC13 一致性：`ledger_status.VALID_STATES = ("active","closed","abandoned")` 与 §4.2 封闭三态逐字一致。
- AC14 零改动：`git status` 确认护栏文件（其他 hook 规则 / lib / 四 schema / versioning-schema）未入改动名单。
- 详见 `.ai/iterations/ITER-0008/VERIFY_REPORT.md`。

## 已知剩余风险 / 延后事项
- 规则依赖 schema 固定列序（状态=第 3 列）；schema 是 hook 执行的契约，改列序须同步规则（pytest 已覆盖固定列序）。
- 新增 deny 条件属 hook 拦截契约扩展：旧项目升级后多一道拦截，附 bypass 兜底、只拦真正越界值。
- 本轮未校验 `current:` 指针与里程碑台账状态——列为后续候选。
- 版本：本轮不发版；ITER-0008 累积到下次切版，预计 MINOR（新增 hook 门禁能力）。

## 引用
- `.ai/iterations/ITER-0008/CONCEPT.md`
- `.ai/iterations/ITER-0008/AC_LIST.md`
- `.ai/iterations/ITER-0008/TECH_PLAN.md`
- `.ai/iterations/ITER-0008/VERIFY_REPORT.md`
