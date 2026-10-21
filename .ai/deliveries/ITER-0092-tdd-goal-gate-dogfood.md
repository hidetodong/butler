# ITER-0092 · TDD 配对收口接线与 pytest dogfood

## 本次交付目标

让显式采用 TDD 的迭代只有在 P5 拿出有效 Red→Green 配对后才能通过 Goal 完成资格裁决。

## 已完成内容

- Goal 裁决器复用 verification-evidence 的唯一配对算法，新增 `tdd_pairs_valid` 检查。
- VERIFY 固定结构新增 `TDD Pair Status`，Red/Green record 同时进 Evidence Index。
- 用 goal-assurance pytest 完成真实 Red/Green dogfood，`check-tdd` 返回 `[OK] goal-gate`。
- Goal/VERIFY/lifecycle/规则卡/工具 README 与 artifact pipeline 机器真源已同步。

## 关键变更 / 用户可感知变化

TECH_PLAN 未声明 TDD 时行为不变；一旦声明，缺 Red、缺 Green、顺序或命令漂移都会阻止 Goal 收口。

## 高层影响范围

Goal assurance、verification evidence、P5 VERIFY 合同、五件套结构真源与双宿主浓缩规则。

## 验证方式与结果摘要

Goal/evidence 40 项、artifact pipeline 21 项和 200 个 hook 测试通过；最终完整 CI exit 0。Goal 机械裁决全部检查通过，结论为 `eligible`。

## 已知剩余风险 / 延后事项

- 本轮由危险模式自主 ACK，P5 完整强审 Must Fix 0、Should Fix 0；未执行 fresh-context 独立复核。
- V1 仍不证明代码修改时序、Red 失败原因或测试未被改弱；这些增强留在独立候办。

## 引用

- `.ai/iterations/ITER-0092/AC_LIST.md`
- `.ai/iterations/ITER-0092/TECH_PLAN.md`
- `.ai/iterations/ITER-0092/VERIFY_REPORT.md`
- `.ai/iterations/ITER-0092/evidence/`
- `tools/goal-assurance/README.md`
- `tools/verification-evidence/README.md`
