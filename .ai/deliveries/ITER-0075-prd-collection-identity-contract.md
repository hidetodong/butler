# ITER-0075 · 需求集合与日期化身份契约

## 本次交付目标

把 Butler 的 PRD 模型从“项目只有一份规格持续改版”升级为“项目包含多份独立需求、每份需求独立改版”的声明式地基。

## 已完成内容

- 定义项目级 PRD 总索引与单需求模块索引的两层结构。
- 定义 `YYYY-MM-DD-<requirement-slug>` 稳定 `prd_id`，日期取首次进入当前项目 Butler 体系的日期。
- 定义全新需求、新版、重复与身份歧义四态；歧义时 fail-closed。
- 明确每份需求独立维护模块和 `.archive/vN/`，legacy 单 PRD 结构继续可读但不静默迁移。
- 新增 6 项结构合同测试，并修复完整 CI 暴露的两处状态/文档漂移。

## 关键变更 / 用户可感知变化

- 未来第二份 PRD 不再与第一份的模块、版本和归档混装。
- 标题、版本、源文件名或实现目录变化不会改变已分配的需求身份。
- 仅凭标题或文件名相似不能覆盖旧需求；证据冲突会明确停机。

## 高层影响范围

- 规则真源：`Coder/40_Context_Management/references-schema.md`。
- 导航：`Coder/README.md`、根 `README.md`。
- 保护：`templates/hooks/tests/test_prd_collection_contract.py`。
- 未修改 split/update 算法、AC 多 PRD 钉版、命令、迁移或门禁；这些由 MILE-0009 后续路线承接。

## 验证方式与结果摘要

- 专项结构合同：6/6 通过。
- 完整 CI：最终 exit 0，含 153 项 hooks、双宿主、Markdown、Goal 与状态矩阵。
- Goal completion adjudicator：10 项检查全绿，verdict=`eligible`。
- 强审：1 个 Must Fix 已修复；最终 Must Fix 0、Should Fix 0。

## 已知剩余风险 / 延后事项

- 现行动作层仍按 legacy 单 PRD 路径运行；不得把本次目标结构误报为命令已适配。
- Pi TypeScript 检查在本机缺依赖时按既有 CI 规则降级为警告，不影响本轮合同验证。
- 未执行 fresh-context 独立复核。

## 引用

- `.ai/iterations/ITER-0075/CONCEPT.md`
- `.ai/iterations/ITER-0075/AC_LIST.md`
- `.ai/iterations/ITER-0075/TECH_PLAN.md`
- `.ai/iterations/ITER-0075/VERIFY_REPORT.md`
- `.ai/iterations/ITER-0075/evidence/`
