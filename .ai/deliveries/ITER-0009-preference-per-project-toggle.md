# ITER-0009 preference 接入项目级配置：per-project 抑制开关

## 本次交付目标
用户希望 preference（偏好探针）也像 `dangerous`/`independent_review` 一样**写进项目级配置** `.ai/local-constraints.md`「Butler 功能开关」。但 ITER-0006 当初**特意把 preference 排除在外**（理由：它跨项目、外置存储，不是项目级状态）。本轮在向用户挑明该冲突、并由用户选定"per-project 抑制开关"语义后，反转那条排除——用**抑制层**调和：preference 进配置，但不破坏其跨项目本质、不引入双真源。

## 已完成内容
- **schema（语义 SSOT）**：`local-constraints-schema §3` 模板「Butler 功能开关」段新增 `preference: on`（默认 on）；§2 必填字段默认更新为"dangerous/independent_review 默认 off、preference 默认 on"；§4.1 把"preference 不纳入"**反转**为 per-project 抑制开关口径——本项目是否运行探针 = 全局未 `/preference off` ∧ 外置 `$PREF` `consent: granted` ∧ 本项目 `preference ≠ off`，三者全真才采集/蒸馏/反哺。
- **引擎**：`preference-probe-engine` 新增 §2.5 项目级抑制开关（生效优先级：全局 off > 全局 consent > 项目开关；非双真源），§2.1 默认常驻标注"受项目级抑制约束"。纯增量，§3 安全底线 / §4 存储契约 / §5-7 采集蒸馏反哺算法 / §9 与 /dangerous 隔离**全未动**。
- **接线**：`logic-protocol §1.3` 会话起始读取增 `preference: off → 本项目抑制`（缺省 on、无需 announce）；§4 Preference Mode 补"per-project 抑制开关落 local-constraints、外置仍为真源"。
- **部署默认**：`mcv-deployment §4` 生成「Butler 功能开关」纳入 `preference: on`（默认 on 安全：实际采集仍需全局同意）。
- **传播（反转排除句）**：`rule-card.md`、`HUMAN_GUIDE.md`（开关表加行 + "关于 preference"注）、`Coder/README.md` 三处旧排除措辞全部反转。

## 关键变更 / 使用者可感知变化
- 现在每个项目的 `.ai/local-constraints.md` 都能看到 `preference: on|off`，与 dangerous/independent_review 并列。
- **`preference: off` 只关掉这一个项目的采集**，不影响全局同意、不动外置数据、不影响别的项目。
- **`on` ≠ 强制采集**：没给过全局同意时，即便 on 也不会采——默认 on 是安全的。
- **真源没变**：consent/signals/profile 仍在外置 `$BUTLER_PREF`（跨项目），这个开关只是本项目采集闸、不双写。
- preference 是只读观察者、低风险，**不需要 dangerous 那种 announce-on-read**，会话起始读到即遵循。

## 高层影响范围
- 改：`Coder/00_System_Prompt/logic-protocol.md`、`Coder/20_Workflow_Lifecycle/{local-constraints-schema,mcv-deployment}.md`、`Coder/70_Extension_Preference/preference-probe-engine.md`、`Coder/README.md`、`templates/rule-card.md`、`HUMAN_GUIDE.md`。
- 不涉及（零改动护栏）：preference 采集/蒸馏/反哺算法（engine §5/§6/§7）、外置存储契约（§4）、§3 安全底线、与 /dangerous 隔离（§9）、`ledger_status` hook、产物链四 schema、versioning-schema、iteration/milestone-schema。

## 验证方式与结果摘要
- 逐 AC（AC1–AC16）grep 落点命中各目标文件，全部通过。
- AC12：四处旧排除句全仓 grep 0 命中（反转彻底，规则不自相矛盾）。
- AC13：五处文件"外置 $BUTLER_PREF 跨项目唯一真源 + 本开关不双写"表述一致，无"项目级真源"矛盾。
- AC14：`git diff --numstat` engine = `12 0`（纯增量），diff 仅 §2.1 + 新增 §2.5；§3-§9 未动。护栏文件全不在改动名单。
- 详见 `.ai/iterations/ITER-0009/VERIFY_REPORT.md`。

## 已知剩余风险 / 延后事项
- 项目开关靠规则纪律（会话起始读 + 遵循），无 hook 强制——与 dangerous/independent_review 同源同险。
- 存量旧项目无 `preference` 字段：按"缺字段=视为 on"兼容，批量回填走 butler-upgrade。
- 版本：本轮不发版；ITER-0009 累积到下次切版，预计 MINOR（新增项目级开关能力）。

## 引用
- `.ai/iterations/ITER-0009/CONCEPT.md`
- `.ai/iterations/ITER-0009/AC_LIST.md`
- `.ai/iterations/ITER-0009/TECH_PLAN.md`
- `.ai/iterations/ITER-0009/VERIFY_REPORT.md`
