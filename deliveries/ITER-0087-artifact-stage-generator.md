# ITER-0087 · 五件套阶段生成器

## 本次交付目标

安全、确定地按阶段生成五件套骨架。

## 已完成内容

- render/init/reset、dry-run、阶段限制与原子写入。
- 已有正文默认不覆盖，强制 reset 必须显式亮牌。

## 关键变更 / 用户可感知变化

AI 可调用固定工具获得正确骨架，不再手写段落结构。

## 高层影响范围

`tools/artifact-pipeline/contract.py`、README 与测试。

## 验证方式与结果摘要

专项 13/13，完整 CI 通过。

## 已知剩余风险 / 延后事项

R3–R4 继续门禁和迁移。

## 引用

- `.ai/iterations/ITER-0087/VERIFY_REPORT.md`
- `.ai/iterations/ITER-0087/evidence/`
