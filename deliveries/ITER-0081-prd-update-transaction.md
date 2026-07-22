# ITER-0081 · 确定性 PRD 改版事务与回执

## 本次交付目标

让指定需求的新版进入项目时，可先看清变化和影响，再以可验证、可恢复的事务完成更新。

## 已完成内容

- 新增标准库 `prd-update`，提供零写 `plan`、事务 `apply`、只读 `verify` 和 hash 门禁 `rollback`。
- update 必须给出显式 `prd_id` 与已确认 JSON spec；模块来源、认亲、删除项和所有三态影响处置缺一不可。
- apply 在排他锁内重算现场，把旧版本完整归档后，在同一 staging 中更新 live、单需求索引、项目总索引和 receipt，再交换整个 PRD collection。
- receipt 持久保存版本、时间、spec/source/tree/archive hash、模块变化、影响与 disposition；status 只读展示最近一次更新。
- 同一 spec 重复执行幂等；现场漂移、并发、symlink、receipt/backup 篡改或故障注入均 fail-closed。

## 用户可感知变化

- `/butler:prd update <prd_id>` 不再依赖对话记忆或手工搬文件，而是由两个宿主共同调用同一个确定性工具。
- planned、active、closed 引用按精确 locator 分开处置，工具只记录决定，不偷偷改写工作产物或历史。
- 更新后可随时 verify；只有当前状态仍与 receipt 完全一致时才能 rollback，避免覆盖后续工作。

## 验证结果

- 12 项事务行为测试、7 项规则/双宿主结构合同全部通过。
- 完整 CI exit 0：189 hooks，以及 inbox、migration、status、update 行为组通过。
- diff check、Goal adjudicator、evidence 归档和项目状态审计通过；最终 Must Fix 0、Should Fix 0。

## 延后事项

- 超大 PRD 的临时磁盘开销与真实仓库规模 dogfood 留 R8。
- workspace 自动发现、TECH_PLAN/实际 diff/hook 范围门禁和 `WorkCode.nosync/apps` e2e 留 R8；仓外写入需明确授权。

## 引用

- `.ai/iterations/ITER-0081/`
- `.ai/iterations/ITER-0081/evidence/`
- `Coder/40_Context_Management/prd-update.md`
- `tools/prd-update/`
- `tools/prd-status/`
