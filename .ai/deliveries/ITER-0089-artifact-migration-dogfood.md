# ITER-0089 · 五件套兼容迁移与 dogfood

## 本次交付目标

无损迁移 legacy live 五件套并完成真实仓 strict dogfood。

## 已完成内容

- plan/apply/verify/rollback 与 hash-gated receipt。
- legacy H1/H2 正文保留、未知/重复段拒绝。
- 当前 Butler 五件套迁移为 strict v1，历史归档未改。

## 关键变更 / 用户可感知变化

迁移不再靠 AI 重排文档；首次 dogfood 暴露的 H1 内容遗漏已回滚并修复。

## 高层影响范围

artifact migration、live `.ai/` 五件套和升级说明。

## 验证方式与结果摘要

最终 21 项专项、strict dogfood 与完整 CI 通过。

## 已知剩余风险 / 延后事项

无阻断风险。

## 引用

- `.ai/iterations/ITER-0089/VERIFY_REPORT.md`
- `.ai/iterations/ITER-0089/evidence/`
