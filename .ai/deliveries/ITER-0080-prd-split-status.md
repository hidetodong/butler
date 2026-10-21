# ITER-0080 · PRD 首切与只读状态

## 本次交付目标

让每份新需求先取得有证据的独立身份再落盘，并能按需求或工作区确定性查看项目中的 PRD 状态。

## 已完成内容

- 首切先判 `new-requirement / new-version / duplicate / ambiguous`，只有全新需求可进入写盘。
- 用首次进入项目的日期化 `prd_id` 建独立目录；身份、模块边界与 Workspace Scope 一次 soft 对齐。
- 新增标准库 `prd-status`：全项目列表、`prd_id` 下钻、workspace 筛选、legacy 只读退化。
- 总索引、单需求索引/模块和 active workspace map 交叉核验；混合布局、漂移和 symlink fail-closed。
- milestone 新指针升级为 `prd_id#module_slug`，Claude/Codex 两端委托同一规则与 CLI。

## 关键变更 / 用户可感知变化

- 第二份需求不会再与第一份需求的模块或版本混在 `prd/` 根。
- `status --workspace <key>` 能找出涉及某个工作区的需求；不同 PRD 的同名模块互不串线。
- legacy 仍可读，但不会被 status 偷偷补日期或伪造 `prd_id`。

## 高层影响范围

- 更新 references/split/update/milestone 规则和 Coder 目录入口。
- 新增 `prd-status` 规则、CLI、14 项行为 fixture 和 7 项结构合同。
- 更新 `/butler:prd`、`$butler-prd`、registry 投影与完整 CI。
- 不实现 R7 update 事务/receipt，不实现 R8 实际代码范围门禁，不写真实 apps 项目。

## 验证方式与结果摘要

- status 14/14、结构 7/7、registry 45 投影、完整 CI exit 0（182 hooks + 三组驻留行为测试）、diff check 通过。
- Goal adjudicator 十项全绿；强审最终 Must Fix 0、Should Fix 0。

## 已知剩余风险 / 延后事项

- update 的确定性事务与持久回执留 R7。
- workspace 自动发现、实际 diff/hook 对账和 apps dogfood 留 R8。
- 未执行 fresh-context 独立复核；Pi 依赖缺失仍按既有 CI 合同警告。

## 引用

- `.ai/iterations/ITER-0080/`
- `.ai/iterations/ITER-0080/evidence/`
- `Coder/40_Context_Management/prd-split.md`
- `Coder/40_Context_Management/prd-status.md`
- `tools/prd-status/`
