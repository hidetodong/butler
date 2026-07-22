# ITER-0079 · 多 PRD 引用与兼容迁移

## 本次交付目标

让一轮工作能准确钉住多份需求的不同版本，并把旧单 PRD 项目显式、可恢复地迁入需求集合，不改写冻结历史。

## 已完成内容

- 用 `prd_refs` 定义 `prd_id + prd_version + module_slugs` 多需求钉版，P3/P5 逐项继承。
- 交付标准库 migration/resolver：inspect、plan、apply、verify、rollback、resolve。
- 用同父 staging、backup、rename 和 receipt 保证迁移失败可恢复，篡改路径 fail-closed。
- 扫描 MILESTONE、active/future、closed history 影响面；closed 只解析、不回写。
- 交付独立迁移指南并接入 HUMAN_GUIDE，行为测试纳入完整 CI。

## 关键变更 / 用户可感知变化

- 同一 AC 可同时钉住需求 A v1.1 与需求 B v2.0，不再共享一个全局版本号。
- 旧 `prd/<slug>.md` 在迁移后仍能结合旧 `prd_version` 和 receipt 找到正确 live/archive bytes。
- 迁移器不会猜首次进入日期，也不会在 verify 前删除 backup。

## 高层影响范围

- 更新 acceptance/tech-plan/verify/references schema。
- 新增 `tools/prd-migrate/`、迁移指南和 16 项结构/行为专项。
- 不实现新 PRD split/status（R6）或确定性 update（R7），不写真实 apps 项目。

## 验证方式与结果摘要

- 行为 11/11、schema/指南 11/11、完整 CI exit 0、175 hooks + inbox 11 + migration 11。
- Goal adjudicator 十项全绿；强审最终 Must Fix 0、Should Fix 0。

## 已知剩余风险 / 延后事项

- 真实 apps 索引变体和权限留 R8 dogfood。
- R6/R7 完成前，迁移成功不等于 split/status/update 全链路完成。
- 未执行 fresh-context 独立复核。

## 引用

- `.ai/iterations/ITER-0079/`
- `.ai/iterations/ITER-0079/evidence/`
- `docs/prd-migration-guide.md`
- `tools/prd-migrate/`
