# Goal
- 支撑 AC1–AC16：迭代状态枚举固化（封闭三态）+ hook 规则 ledger_status 机械门禁 + 测试 + 消歧/传播。下文给精确锚点与代码。

# Files / Modules to Change

## 新增
### 1. `templates/hooks/rules/ledger_status.py` 【AC4/AC5/AC6/AC13】
- `RULE_ID = "ledger_status"`；`LEDGER_REL = ".ai/ITERATIONS.md"`；`VALID_STATES = ("active", "closed", "abandoned")`（注释标"镜像 iteration-schema §4.2 封闭枚举"）；`_ITER_RE = re.compile(r"^ITER-\d{4}$")`。
- `evaluate(ctx)`：`target != LEDGER_REL` → allow；取入参文本（`_incoming_text`）；逐行 `raw.strip()`，非 `|` 起头跳过；`cells = [c.strip() for c in line.strip("|").split("|")]`；`len(cells) < 3` 或 `cells[0]` 不匹配 `_ITER_RE` → 跳过；`status = cells[2].lower()`；`status and status not in VALID_STATES` → deny（reason 含 `cells[0]` 与原值 `cells[2]` + 合法枚举；remediation 指三态 + planned 属 milestone-schema §5.3 路线项）。
- `_incoming_text(ctx)`：Write→`tool_input.get("content","")`、Edit→`get("new_string","")`、MultiEdit→`"\n".join(e.get("new_string","") for e in get("edits",[]))`、其他→`""`。

### 2. `templates/hooks/tests/test_ledger_status.py` 【AC8】
- `make_ctx(target, content, tool="Write")`：key = `content`（Write）/`new_string`（Edit）；MultiEdit 单独造 `edits`。
- 用例：合法三态全 allow、`planned` 行 deny（断言 reason 含 `ITER-` 与 `planned`、remediation 含 `milestone-schema`）、`abandoned` allow、非台账路径（`.ai/CONCEPT.md` 含 planned 文本）allow、Edit `new_string` planned deny、MultiEdit planned deny、仅表头+分隔行 allow、空状态单元格 allow、大小写变体（`Active`）allow、`draft`（AC_LIST 态误入）deny。

## 改
### 3. `templates/hooks/butler_gate.py` 【AC7】
- import：`from rules import artifact_chain, ledger_status, phase_gate, protected_paths`。
- `RULE_MODULES = [protected_paths, phase_gate, ledger_status, artifact_chain]`（ledger_status 置于 phase_gate 后、artifact_chain 前；各规则命中条件互斥，first-deny-wins 不冲突）。

### 4. `Coder/20_Workflow_Lifecycle/iteration-schema.md` §4.2 【AC1/AC2】
- 改写为封闭枚举声明：开头加一句"迭代行「状态」是**封闭枚举**，合法值**仅**以下三个，其他值（含 `planned`）对迭代行非法"；保留三态语义；末尾加交叉引用：`planned` 属 `milestone-schema §5.3` 路线图「路线项状态」、非迭代状态；部署项目由 hook `ledger_status` 机械校验本枚举（越界写 `.ai/ITERATIONS.md` 被拦截）。

### 5. `Coder/20_Workflow_Lifecycle/milestone-schema.md` §5.3 【AC3】
- 在「路线项状态取值」一段后加一句消歧：「路线项状态」是路线项自身命名空间，与迭代行状态（`iteration-schema §4.2` 封闭三态）**不是同一字段**；`planned` 路线项「实际 ITER」为 `—`、**不产生迭代台账行**，故 `planned` 不应出现在 `.ai/ITERATIONS.md`。

### 6. `templates/hooks/README.md` 【AC10】
- 目录结构 rules/ 下加 `ledger_status.py     # 校验 .ai/ITERATIONS.md 状态列封闭枚举`。
- 「运行机制」步骤 2 执行顺序更新为 `protected_paths → phase_gate → ledger_status → artifact_chain`。

### 7. `Coder/20_Workflow_Lifecycle/mcv-deployment.md` §5 【AC11】
- §5 首段 hook 能力描述（"源码路径写操作在 P1/P2/P3 产物缺失时被拦截、AC_LIST 未冻结…被拦截、99_Business_Extension 写操作被拦截"）补一项："迭代台账 `.ai/ITERATIONS.md` 状态列出现封闭枚举（active/closed/abandoned）外的值被拦截"。

### 8. `Coder/README.md` 【AC12】
- 使用原则中 hook bullet（P1-P3 产物 + ACK 冻结机械拦截那条）补一句迭代台账状态枚举校验。

### 9. `templates/rule-card.md` / `HUMAN_GUIDE.md` 【AC12】
- 各自查是否含 hook 行为概述；含则补一句迭代台账状态校验，无则不强加（按 AC12 "无则不强加"）。

# Design Decisions
1. **机制 = hook，schema = 契约**：§4.2 是枚举权威定义，hook 的 VALID_STATES 是机械镜像（AC13），注释互指防漂移。
2. **专打台账路径、不走 is_gated**：`.ai/` 被源码写门豁免，新规则按 `target == .ai/ITERATIONS.md` 独立校验，与现有规则零冲突（设计决策 §2）。
3. **逐行 + 固定列序**：依赖 schema 固定列序（状态=第 3 单元格），不依赖表头存在，故 Edit 片段亦可校验；空状态放行不误杀半写行。
4. **复用 bypass**：deny 走 lib/bypass，可 BUTLER_BYPASS 显式绕过——与 butler"机械默认 + 显式绕过"哲学一致（AC7）。
5. **选项 A，不加第四态**：planned 钉回路线项语义，保「不预先占号」。

# Test / Verify Strategy
- AC9：`cd templates/hooks && python3 -m pytest tests/` 全绿（须含既有 + 新用例）。
- AC1/AC2/AC3：grep iteration-schema §4.2 含"封闭枚举/仅/planned…非法/ledger_status"、milestone-schema §5.3 含消歧句。
- AC4-AC7：阅读 ledger_status.py + butler_gate.py 确认路径门、入参提取、RULE_MODULES 接入；pytest 覆盖 deny/allow 分支。
- AC10/AC11/AC12：grep README/mcv-deployment/Coder README 命中。
- AC13：grep ledger_status.py 的 VALID_STATES = ("active","closed","abandoned") 与 §4.2 字面一致。
- AC14：`git diff --name-only` 确认 phase_gate/protected_paths/artifact_chain/lib/* /四 schema/versioning-schema 不在改动名单（lib/* 不改、其他规则不改）。
- AC15：人工核对五约束。
- AC16：归档/delivery/台账核对。

# Rollback
- 新增规则 + 文档改写，无运行态副作用（hook 仅在部署项目生效，且可 bypass）。回退 = `git revert` 本迭代提交。
