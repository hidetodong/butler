# ITER-0086 · 五件套结构合同

## 本次交付目标

建立五件套结构的唯一机器真源。

## 已完成内容

- 版本化 manifest 定义五产物路径、阶段、段落顺序、字段和表头。
- 五份 canonical 模板固定条件段与 N/A 位置。
- 合同解析器和 7 项负向/正向测试落地。

## 关键变更 / 用户可感知变化

后续生成器和检查器不再从散文 schema 猜结构，而从同一 manifest 工作。

## 高层影响范围

`tools/artifact-pipeline/` 与 `Coder/README.md`。

## 验证方式与结果摘要

合同测试 7/7，完整 CI 通过；证据见归档 Evidence Index。

## 已知剩余风险 / 延后事项

R2–R4 继续生成、门禁和迁移，不阻断 R1。

## 引用

- `.ai/iterations/ITER-0086/VERIFY_REPORT.md`
- `.ai/iterations/ITER-0086/evidence/`
